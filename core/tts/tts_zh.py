"""edge-tts voice-over (Microsoft neural voices; first choice for Chinese, also reads other languages):
    python core/tts/tts_zh.py lines.json out_dir [--voice zh-CN-XiaoxiaoNeural] [--rate +0%] [--pitch +0Hz]
lines.json = [{"id":..., "text":..., "voice":"zh-CN-YunxiNeural", "rate":"+10%", "pitch":"-2Hz", "say":"..."}, ...]
  "say" (optional) = the text actually sent to be read, default same as "text" (use it to spell out numbers/abbreviations as spoken; subtitles still use text).
  Also accepts tts.py's "speed" (multiplier, 1.1 → +10%). Voice list: python -m edge_tts --list-voices
Output is identical to tts.py: out_dir/<id>.wav (24kHz mono, leading/trailing silence trimmed) and out_dir/dur.json.
  Intermediate mp3s are cached in out_dir/.cache/; no network call if text/voice/rate are unchanged (written to .part then renamed, so Ctrl-C never leaves a half file that the next run takes as good;
  broken mp3s in the cache are deleted and re-downloaded automatically).

Needs network: this is Microsoft's online speech service, not a local model. Whether voices made with it may be used commercially: check Microsoft's terms of service yourself.
Exits with an error when the network is down or firewalled (exit code 2; bad input or config is 1); offline alternative: tts.py with "lang":"cmn" (Kokoro, mediocre timbre, verify with asr_check.py).
"""
import sys, io, json, os, re, asyncio, hashlib, subprocess, argparse
import numpy as np, soundfile as sf
SR = 24000


def rate_of(L, default):
    r = L.get('rate')
    if r is None and 'speed' in L: r = float(L['speed'])
    if isinstance(r, (int, float)): r = f'{round((float(r) - 1) * 100):+d}%'   # a number is a speed multiplier
    return r or default


async def synth(text, voice, rate, pitch, path):
    """Download to path: write path.part first and rename only on success, so if path exists it is complete (no interruption, Ctrl-C included, leaves a half file)"""
    import edge_tts
    part = path + '.part'
    last = None
    try:
        for attempt in range(3):   # retry twice on occasional network glitches
            try:
                await edge_tts.Communicate(text, voice, rate=rate, pitch=pitch).save(part)
                if os.path.getsize(part) == 0: raise OSError('the service returned an empty file')
                os.replace(part, path); return
            except Exception as e:
                last = e
                if type(e).__name__ == 'NoAudioReceived': break   # wrong voice name/text, retrying won't help
                await asyncio.sleep(1.5 * (attempt + 1))
        raise last
    finally:
        if os.path.exists(part): os.remove(part)   # clean up on failure and on Ctrl-C


def to_wav(mp3):
    """Decode to 24 kHz mono; returns None for a broken file (caller deletes the cache entry and re-downloads)"""
    try:
        r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', mp3, '-ar', str(SR), '-ac', '1', '-f', 'wav', '-'], capture_output=True, check=True)
    except FileNotFoundError: sys.exit('tts_zh.py: ffmpeg is needed to decode the audio (install it and make sure it is on PATH)')
    except subprocess.CalledProcessError: return None
    try: a, sr = sf.read(io.BytesIO(r.stdout), dtype='float32')
    except Exception: return None
    return (a, sr) if len(a) else None


def plausible(decoded):
    """A cached mp3 must decode to something like a sentence: at least 0.15 s and not silent (a half file often "decodes fine" but is just a bit of silence)"""
    if decoded is None: return False
    a, sr = decoded; return len(a) >= 0.15 * sr and float(np.abs(a).max()) > 1e-3


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('lines'); ap.add_argument('out_dir')
    ap.add_argument('--voice', default='zh-CN-XiaoxiaoNeural'); ap.add_argument('--rate', default='+0%'); ap.add_argument('--pitch', default='+0Hz')
    a = ap.parse_args()
    lines = json.load(open(a.lines, encoding='utf-8'))
    for L in lines:
        r, p = rate_of(L, a.rate), L.get('pitch', a.pitch)
        if not re.fullmatch(r'[+-]\d+%', r): sys.exit(f"tts_zh.py: line '{L['id']}': rate must look like '+10%' or '-5%' (or a speed number like 1.1), got {r!r}")
        if not re.fullmatch(r'[+-]\d+Hz', p): sys.exit(f"tts_zh.py: line '{L['id']}': pitch must look like '-2Hz' or '+0Hz', got {p!r}")
    try: import edge_tts  # noqa: F401
    except ImportError: sys.exit('tts_zh.py: edge-tts is missing: install the voice tier: sh plugin/skills/lemo-opuscar/scripts/setup.sh deps voice')
    os.makedirs(os.path.join(a.out_dir, '.cache'), exist_ok=True); dur = {}
    for n in os.listdir(os.path.join(a.out_dir, '.cache')):
        if n.endswith('.part'): os.remove(os.path.join(a.out_dir, '.cache', n))   # partial file left by an interrupted run
    for L in lines:
        voice, rate, pitch, say = L.get('voice', a.voice), rate_of(L, a.rate), L.get('pitch', a.pitch), L.get('say', L['text'])
        key = hashlib.sha1(json.dumps([voice, rate, pitch, say], ensure_ascii=False).encode('utf-8')).hexdigest()[:16]
        mp3 = os.path.join(a.out_dir, '.cache', key + '.mp3')
        decoded = to_wav(mp3) if os.path.exists(mp3) else None
        if not plausible(decoded): decoded = None
        if decoded is None and os.path.exists(mp3): os.remove(mp3); print(f"tts_zh.py: cached audio for line '{L['id']}' was damaged; fetching it again", file=sys.stderr)
        if decoded is None:
            try: asyncio.run(synth(say, voice, rate, pitch, mp3))
            except Exception as e:
                if type(e).__name__ == 'NoAudioReceived':
                    sys.exit(f"tts_zh.py: no audio came back for line '{L['id']}'. Is the voice name '{voice}' valid (python -m edge_tts --list-voices) and the text speakable?")
                if isinstance(e, ValueError):   # the arguments themselves are wrong (e.g. no such voice), no request was sent
                    sys.exit(f"tts_zh.py: line '{L['id']}': {e}  (voices: python -m edge_tts --list-voices)")
                print(f"tts_zh.py: could not reach Microsoft's speech service for line '{L['id']}': {type(e).__name__}: {str(e)[:200]}\n"
                      "  edge-tts needs a network connection (and can be blocked by a firewall/proxy). Offline alternative: tts.py with \"lang\": \"cmn\".", file=sys.stderr)
                sys.exit(2)   # exit code 2 = network problem; 1 = bad input/config
            decoded = to_wav(mp3)
            if decoded is None: sys.exit(f"tts_zh.py: the audio Microsoft returned for line '{L['id']}' could not be decoded (ffmpeg); try again")
        y, sr = decoded
        nz = np.where(np.abs(y) > (np.abs(y).max() if len(y) else 0) * .02)[0]
        if len(nz): y = y[max(0, nz[0] - int(.03 * sr)): nz[-1] + int(.10 * sr)]   # trim leading/trailing silence; keep a longer tail so the end of the sentence isn't clipped
        else: print('warning: line', L['id'], 'is silent', file=sys.stderr)
        sf.write(os.path.join(a.out_dir, L['id'] + '.wav'), y, sr); dur[L['id']] = round(len(y) / sr, 3)
        print(L['id'], dur[L['id']], L['text'])
    json.dump(dur, open(os.path.join(a.out_dir, 'dur.json'), 'w', encoding='utf-8'), indent=1)


if __name__ == '__main__':
    main()
