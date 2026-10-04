#!/bin/sh
# Rebuild "TRANQUILITY.LOG" from scratch: sh styles/ascii-crt/demo/build.sh (run from any directory)
set -e
cd "$(dirname "$0")/../../.."
PY=.venv/bin/python; D=styles/ascii-crt/demo; S=styles/ascii-crt
$PY core/tts/tts.py $D/lines.json $D/voices_raw                  # 1. Kokoro voice-over (am_echo, speed 0.8)
$PY $D/voice_fx.py                                               # 2. AI voice: light ring mod + comb resonance + band-pass → voices/
$PY core/tts/asr_check.py $D/lines.json $D/voices                # 3. whisper check per line (mismatches: 0) + per-word timings words.json (for word-by-word typing in the log bar)
$PY $D/music/score.py                                            # 4. original analog-synth score → music/score.wav + stems (~6s)
node core/render/events.mjs $D                                   # 5. timeline → events.json (keyboard/handshake/landing/VO events)
$PY $D/mix.py                                                    # 6. synthesised foley + VO ducking + score → mix.wav
node $D/tools/subs.mjs $D && $PY core/render/srt.py $D/out/subs.json $S/ascii-crt.srt   # 7. subtitles
node core/render/video.mjs $D --fps 24 --workers 3 --out $D/out/video24.mp4             # 8. frame-by-frame render (1435 frames, ~35s)
sh core/render/mux.sh $D/out/video24.mp4 $D/mix.wav $S/ascii-crt.mp4 24 0               # 9. mux: −14 LUFS, no grain (noise is in the picture)
node core/render/still.mjs $D 39.4 --q 'nosub=1' --out $D/out/still --prefix sf_ && cp $D/out/still/sf_39.4.jpg $D/stills/styleframe.jpg
node core/render/still.mjs $D 0 --q 'frame=poster' --out $D/out/still --prefix po_ && cp $D/out/still/po_0.jpg $S/poster.jpg
