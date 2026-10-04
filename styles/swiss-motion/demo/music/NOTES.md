# Score notes · Five Rules for a Poster

`score.py` generates the whole score from scratch in about 4 seconds, random seed fixed at 1961: original Motorik score, 120 BPM, A Dorian, 44.5 seconds, 48 kHz stereo 24-bit. Melody and bass roots are read from `../score.json`, the same data as the poster on screen.

## Instruments
- **Drums**: `drum_kit` (MuldjordKit), using kick, snare, closed hi-hat, crash. The motorik beat is kick on 1, 3, 3&, snare on 2, 4, closed hat in 8ths. Cymbals run on their own bus with a 7.5 kHz first-order low-pass.
- **Bass**: `electric_bass` (FreePats fingered electric bass), an 8th-note pulse on the root two octaves down.
- **Arpeggio**: additive numpy sawtooth; the harmonic count itself acts as a low-pass, so there is no aliasing. 16th notes, harmony Am / C / D.
- **Melody**: `glockenspiel` (VCSL) transposed up two octaves, through a 5.2 kHz second-order low-pass, layered over a soft odd-harmonic square wave (an octave up).
- **fx**: the red circle's sine glide (G5 → D5, hold one beat, then to A4), and a −40-cent glockenspiel grace note when it hesitates.

## CREDITS
```
Drums: "MuldjordKit" by Lars Muldjord (drumgizmo.org), FreePats version, licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
Samples (CC0): FreePats project (freepats.zenvoid.org), Versilian Community Sample Library (Versilian Studios)
```

## Self-check (by data only, never checked by ear)
- Peak −1.0 dBFS, no clipped samples, no NaN.
- 8–20 kHz is 9.3 dB below 2–8 kHz.
- RMS per section (dBFS):

  | Section | Rule four 20–24 | Escape 24–26 | Pull-along 26–30 | Halt 30–32 | Scan 32–36 | Poster wall 36–40 |
  |---|---|---|---|---|---|---|
  | RMS | −18.4 | −22.8 | −18.3 | −27.4 | −19.7 | −17.2 (highest) |

- Onset error in the 32–36 s scan section: +0.0 / +0.6 / +2.4 / +3.3 / +2.1 / +2.5 / +1.6 / +2.9 ms; the last one is the red-circle accent. Measured as "the first sample 3× louder than the previous 5 ms"; librosa onset results are also within 3 ms.

## Known issues
- 33.25 (C) and 33.5 (D) are adjacent short notes and the previous glockenspiel note is still ringing, so D's onset energy only jumps 3.6 dB. The transient is still clear, but it doesn't "pop" as much as the other notes.
- 24–26 s is only 4.4 dB below the previous section: once the drums drop out the perceived drop is already large, and the riser needs some presence. If it still feels full in the mix, pull down the fx and arpeggio stems.
- Everything is samples plus synthesis and has not been checked by ear; transposed up two octaves, the glockenspiel may sound a bit like a "music box".
