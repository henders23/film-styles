#!/bin/sh
# Rebuild the film from scratch: sh styles/lowpoly-island/demo/build.sh (runs from any directory)
set -e
cd "$(dirname "$0")/../../.."
PY=.venv/bin/python; D=styles/lowpoly-island/demo; S=styles/lowpoly-island
$PY core/tts/tts.py $D/lines.json $D/voices                 # 1. Kokoro voice-over (af_sky)
$PY core/tts/asr_check.py $D/lines.json $D/voices           # 2. whisper check per line
node core/render/events.mjs $D                              # 3. timeline → events.json (growth events carry pitch = the melody voice)
$PY $D/music/score.py                                       # 4. original score: melody synthesised note by note from growth events
$PY $D/music/check.py                                       #    librosa check: key-note onsets / pitch vs picture events, true silence, band energy
$PY $D/mix.py                                               # 5. material foley + ambience bed + VO + score ducking → mix.wav
$PY $D/subs.py && $PY core/render/srt.py $D/out/cues.json $S/lowpoly-island.srt   # 6. subtitles
node core/render/video.mjs $D --fps 24 --workers 3 --out $D/out/video24.mp4        # 7. frame-by-frame render (2× supersampling + GTAO)
sh core/render/mux.sh $D/out/video24.mp4 $D/mix.wav $S/lowpoly-island.mp4 24 0     # 8. mux + −14 LUFS, no grain
