"""Export subtitles: python core/render/srt.py cues.json out.srt
cues.json = [{"t0": 1.2, "t1": 3.4, "text": "..."}, ...] (written by the film itself: e.g. save the timeline that drives on-screen subtitles as JSON, so the .srt matches the on-screen subtitle intervals;
  events.mjs exports {dur, ev} (sound-effect events), not subtitles)
Overlapping adjacent cues are trimmed to end where the next one starts"""
import sys, json
if len(sys.argv) < 3: print('usage: python core/render/srt.py cues.json out.srt', file=sys.stderr); sys.exit(2)
cues = sorted(json.load(open(sys.argv[1], encoding='utf-8')), key=lambda c: c['t0'])
for k in range(len(cues) - 1): cues[k]['t1'] = min(cues[k]['t1'], cues[k + 1]['t0'])
def fmt(s):
    ms = int(round(max(0, s) * 1000))   # round to whole ms first, then split, so carries aren't lost (1.9996 → 00:00:02,000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
out = '\n'.join(f"{k + 1}\n{fmt(c['t0'])} --> {fmt(c['t1'])}\n{c['text']}\n" for k, c in enumerate(cues))
open(sys.argv[2], 'w', encoding='utf-8').write(out); print(sys.argv[2], len(cues), 'cues')
