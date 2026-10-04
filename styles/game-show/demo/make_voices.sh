#!/bin/sh
# Voice calls: macOS `say` English system voices → ffmpeg pitch shift without tempo change → 44.1 kHz mono wav
# The original project left no generation script; this pipeline was reverse-engineered from voices/lines*.txt when the demo was added to the library (title.wav measures 204 Hz pitch, matching the original; 36 of 40 lines within 30 ms duration error, the rest within 40 ms).
# Each line of lines*.txt: name|voice|rate(say -r)|pitch factor|line
# Usage: sh make_voices.sh [output dir]   default out/voices_regen/ (does not overwrite voices/; copy over by hand once checked)
set -e
cd "$(dirname "$0")"
OD="${1:-out/voices_regen}"; mkdir -p "$OD"
cat voices/lines.txt voices/lines2.txt voices/lines3.txt | while IFS='|' read -r NAME VOICE RATE PITCH TEXT; do
  [ -z "$NAME" ] && continue
  say -v "$VOICE" -r "$RATE" -o "$OD/$NAME.aiff" "$TEXT"
  # say outputs 22050 Hz; asetrate raises the pitch, atempo restores the duration (no silence trimming: the originals weren't trimmed either)
  ffmpeg -y -loglevel error -i "$OD/$NAME.aiff" -af "asetrate=22050*$PITCH,aresample=44100,atempo=1/$PITCH" -ac 1 -ar 44100 "$OD/$NAME.wav"
  rm "$OD/$NAME.aiff"; echo "$NAME ($VOICE)"
done
