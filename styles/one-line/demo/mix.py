"""Mix: pen-nib scratch (synthesised from pen speed, the film's most important sound) + pen down + ink bleed + room tone + VO + solo cello
python styles/one-line/demo/mix.py → demo/mix.wav (48k stereo, loudness left to mux.sh's two-pass loudnorm)"""
import sys, os, json, numpy as np, soundfile as sf, librosa
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, ROOT)
from core.audio.sfx import SR, add, bp, lp, hp, compress, limit
from scipy.signal import sosfilt, butter
HERE = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(HERE, 'events.json'))); ev = E['ev']
DUR = E['dur'] + 0.5
N = int(DUR * SR)
rng = np.random.default_rng(11)
get = lambda typ: [e for e in ev if e['type'] == typ]
track = get('track')[0]['data']          # [t, speed, screen_x(0..1), style, dry]

# ---------- pen-nib scratch ----------
tt = np.array([r[0] for r in track]); v = np.array([r[1] for r in track], float); px = np.array([r[2] for r in track]); dry = np.array([r[4] for r in track])
style = [r[3] for r in track]
kid = np.array([s == 'kid' for s in style], float); old = np.array([s == 'old' for s in style], float)
T = np.arange(N) / SR
V = np.interp(T, tt, v); PX = np.interp(T, tt, px); DRY = np.interp(T, tt, dry); KID = np.interp(T, tt, kid); OLD = np.interp(T, tt, old)
# smooth the envelope (pen speed → loudness: fast = loud and bright; slow = dull and "wet")
def smooth(x, ms):
    n = max(1, int(SR * ms / 1000)); k = np.ones(n) / n; return np.convolve(x, k, 'same')
amp = smooth(np.clip(V / 520, 0, 1.5) ** 0.5, 30)
# paper-fibre grain: random small "clicks", density follows pen speed
grain = np.zeros(N)
dens = np.clip(V / 520, 0, 2) * 90 + (V > 5) * 25            # per second
p = dens / SR; hits = rng.random(N) < p
idx = np.nonzero(hits)[0]; grain[idx] = rng.standard_normal(len(idx)) * (0.5 + rng.random(len(idx)))
grain = bp(grain, 2500, 9000, 2)
white = rng.standard_normal(N)
hiss_hi = bp(white, 2200, 7500, 2)                          # fast: bright
hiss_lo = bp(white, 700, 2400, 2)                           # slow: dull
bright = np.clip(V / 700, 0, 1)
scr = amp * ((0.55 + 0.45 * bright) * hiss_hi + (1 - bright) * 0.8 * hiss_lo) + amp * 1.6 * grain
# old age: sound breaks up where the ink breaks; child: lighter, more broken
gate = 1 - DRY * 0.9 * (smooth((rng.random(N) < 12 / SR).astype(float), 40) > 0.004)
scr *= np.where(OLD > 0.5, 0.75 + 0.25 * gate, 1.0)
kidwob = 0.55 + 0.45 * smooth((rng.random(N) < 18 / SR).astype(float) * 40, 25).clip(0, 1)
scr *= 1 - KID * (1 - 0.7 * kidwob)
scr = lp(scr, 9000, 2)
scr *= 0.13
pan = (PX - .5) * 1.1
pen = np.stack([scr * np.sqrt(np.clip(.5 - pan / 2, 0, 1)), scr * np.sqrt(np.clip(.5 + pan / 2, 0, 1))], 1).astype(np.float32)

sfx = np.zeros((N, 2), np.float32)
sfx += pen
# pen down: light wooden "tap" + dull paper thud
for e in get('tap'):
    d = int(.25 * SR); t = np.arange(d) / SR
    tick = np.sin(2 * np.pi * 2300 * t) * np.exp(-t / .004) * .5 + bp(rng.standard_normal(d), 1500, 6000) * np.exp(-t / .006) * .6
    thud = np.sin(2 * np.pi * 140 * t) * np.exp(-t / .03) * .5
    add(sfx, ((tick + thud) * .22).astype(np.float32), e['t'] - .005, 1.0, -.15)
# ink bleeding at the pen stop: a barely audible wet sound (low-passed noise swells slowly then fades)
for e in get('blot'):
    d = int(2.2 * SR); t = np.arange(d) / SR
    wet = lp(rng.standard_normal(d), 900, 2) * np.sin(np.pi * np.clip(t / 2.2, 0, 1)) ** 2
    add(sfx, (wet * .018).astype(np.float32), e['t'], 1.0, .1)
# handover: a very faint rub as the child's hand grips the pen
for e in get('handoff'):
    d = int(.35 * SR); t = np.arange(d) / SR
    rub = bp(rng.standard_normal(d), 900, 3500) * np.sin(np.pi * t / .35) * .025
    add(sfx, rub.astype(np.float32), e['t'] - .1, 1.0, -.2)

# room tone (very faint), cut along with the true-silence spans
room = lp(np.cumsum(rng.standard_normal(N)) * .002, 400, 2); room = room - smooth(room, 500)
room = (room / (np.abs(room).max() + 1e-9) * .004).astype(np.float32)
cues = json.load(open(os.path.join(HERE, 'music', 'cues.json')))
s0, s1 = cues['silence']
gate_room = np.ones(N, np.float32); i0, i1 = int((s0 + .2) * SR), int((s1 - .6) * SR)
gate_room[i0:i1] = .15
sfx += np.stack([room, room], 1) * gate_room[:, None]

# ---------- voice-over ----------
vo = np.zeros((N, 2), np.float32)
duck = np.zeros(N, np.float32)
VO = [{'id': e['id'], 't0': e['t']} for e in get('vo')]
for L in VO:
    y, sr = sf.read(os.path.join(HERE, 'voices', L['id'] + '.wav'))
    if y.ndim > 1: y = y.mean(1)
    y = librosa.resample(y, orig_sr=sr, target_sr=SR)
    y = hp(y, 85, 2); y = lp(y, 7200, 2)                        # am_liam is bright: tame the highs a little
    sos = butter(2, [2500, 4200], 'bandstop', fs=SR, output='sos'); y = 0.75 * y + 0.25 * sosfilt(sos, y)
    y = compress(y / (np.abs(y).max() + 1e-9), thr=.3, ratio=3, att=.004, rel=.1)
    y = y / (np.abs(y).max() + 1e-9) * .5
    add(vo, y.astype(np.float32), L['t0'], 1.0, 0)
    a, b = int(L['t0'] * SR), int((L['t0'] + len(y) / SR) * SR); duck[max(0, a - int(.25 * SR)):min(N, b + int(.3 * SR))] = 1
duck = smooth(duck, 250)

# ---------- music ----------
mus, msr = sf.read(os.path.join(HERE, 'music', 'score.wav')); mus = mus.astype(np.float32)
m = np.zeros((N, 2), np.float32); n = min(N, len(mus)); m[:n] = mus[:n]
m *= (1 - 0.45 * duck)[:, None]                                  # duck about −5 dB under the VO (the cello is quiet already)

sfx[:, 0] *= 1 - 0.35 * duck; sfx[:, 1] *= 1 - 0.35 * duck
mix = m * .55 + vo * 1.0 + sfx * 1.0
mix = limit(mix, .95)
sf.write(os.path.join(HERE, 'mix.wav'), mix.astype(np.float32), SR)
# per-stem level table (every 2 s)
def db(x): return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
for i in range(0, int(DUR), 2):
    sl = slice(i * SR, (i + 2) * SR)
    print(f'{i:2d}s  music {db(m[sl] * .55):6.1f}  vo {db(vo[sl]):6.1f}  pen {db(pen[sl]):6.1f}')
print('mix.wav', mix.shape, 'peak', np.abs(mix).max())
