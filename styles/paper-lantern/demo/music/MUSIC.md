# A Mooncake's Longing: score candidates

None of the candidates was auditioned. They were shortlisted from source-page metadata (title, tags, description, instrument list) plus librosa analysis. Raw data in `analysis.json`.

**How to read the data**
- **arc** is the RMS loudness of each 5 s window in dB, with the loudest frame of the whole track at 0 dB. One row per 30 s; closer to 0 is louder.
- **RMS dBFS** is the track's average level, used to match track volumes before mixing.
- **Tempo** is librosa's beat estimate. Unreliable for free-tempo piano and folk solo pieces.
- **perc** is the share of percussive energy after HPSS separation; below 0.05 means essentially no drums.
- **pent** is the share of harmonic chroma energy that falls on the best-matching major pentatonic scale. High values (above 0.75) mean pure pentatonic, i.e. the sound of the Chinese gong mode; the semitones of Japanese miyako-bushi / in scales score low here.

**Narration timing reference**: estimated from `vo/dur.json` plus a 0.9 s gap per line, total narration is about 111 s. Scaled ×1.12 to a 125 s film, the rough cue points are:
- Kitchen L03–L06 ≈ 10–28 s
- "And so, I set off" L10 ≈ 45 s
- Journey L11–L14 ≈ 47–72 s
- Box opened, Grandma's note L16–L17 ≈ 79–86 s
- Twist L19–L21 ≈ 93–107 s
- Su Shi / "may we all live long" L22–L23 ≈ 109–117 s
- "Happy Mid-Autumn" L25 ≈ 122 s

---

## Ranking

### No. 1 (first choice): Ripples → Nu Flute relay (Kevin MacLeod, CC BY 4.0)
- **Why**
  - Real guzheng (Ripples) and dizi + strings (Nu Flute).
  - Ripples is 0.83 pentatonic, pure gong mode; it sounds Chinese rather than Japanese.
  - Neither has drums (perc 0.017 / 0.006).
  - Compatible keys, both centred on C pentatonic, so they crossfade directly.
  - Cleanest licence: CC BY 4.0, no Content ID risk.
- **Splice plan**
  1. Ripples from 0:00 covers film 0 to ~46 s: kitchen, packing, "And so, I set off". The first 10 s are very quiet (-18/-17 dB); the guzheng really enters after 10 s.
  2. Nu Flute comes in with a 4 s crossfade at about 42 s of the film and plays out naturally (82.8 s), landing exactly at film 125 s.
  3. Nu Flute's own cue points then map onto the film as:
     - the 35 s swell (+3.8 dB) → film ~77 s, the box opening and Grandma's note.
     - the 65 s dip (-6.3 dB) → film ~107 s, a breath before the Su Shi line.
     - the 70 s swell (+4.3 dB) → film ~112 s, right on "may we all live long".
     - the ending after 80 s → the final "Happy Mid-Autumn".
  4. If the final narration timing changes, shift Nu Flute's start so its 70 s peak lands on L23.
- **Levels**: Ripples averages about -22 dBFS, Nu Flute about -18.7 dBFS. Bring Nu Flute down about 3 dB at the join.
- **Risks**
  - Nu Flute is tagged "Somber" and leans gently melancholy, but it is also tagged "Uplifting", which fits the "longing + reunion" tone.
  - Ripples is listed as "Koto" in incompetech's instrument list, but the description clearly says Chinese guzheng, and the chroma analysis supports pentatonic.

### No. 2: NastelBom "Asian - Asian China Chinese Music" (Pixabay, single track with its own arc)
- **Why**
  - The most authentically Chinese of the batch: 0.84 pentatonic, pure gong mode; described as "traditional Chinese instruments", category string quartet.
  - No drums (perc 0.01).
  - Built-in arc: very quiet 0–20 s → full entry at 20 s → dip 110–130 s → big swell at 130 s (+6.3 dB) through to the end at 170 s.
- **Use**: the track is 178 s, so fitting it to a 125 s film needs one cut.
  - Cut about 25 s from the 20–110 s plateau, e.g. 55→80 s, with the join on a bar line.
  - After the cut the dip falls at film ~85–105 s (the twist) and the swell at ~105 s (Su Shi / the moon).
- **Risks (important)**
  - The Pixabay page is marked **"Content ID Registered"**. YouTube may auto-claim it; keep the Pixabay download page as proof of licence for disputes. Chinese platforms are generally unaffected.
  - The master is very loud (-13.5 dBFS); bring it down about 8 dB to match the others.

### No. 3: Scott Buckley "Echoes Of Home" (CC BY 4.0, Western orchestral, best arc)
- **Why**
  - The loudness curve is a textbook long crescendo: starts at -22 dB, -14 by 55 s, -12 by 75 s, peak around 145–155 s (-7 dB).
  - The composer describes it as warm, nostalgic orchestral music, close to Zelda / Ghibli.
  - No drums (perc 0.028).
- **Use**: start at 35 s into the track, aligned with film 0 s.
  - The peak then lands at film ~110–120 s, right on "may we all live long".
  - Fade out over the last 5 s of the film.
- **Weakness**: no Chinese instruments (0.63 pentatonic, Western harmony). If a Chinese flavour matters, use it as a fallback or combine it with No. 1 (guzheng at the start, this orchestra for the climax).

### No. 4: NourishedByMusic "Mo Li Hua - Chinese Jasmine Flower" (Pixabay)
- Dizi-led. 0.79 pentatonic, no drums, almost no low end (energy below 250 Hz is only 0.4%).
- Very quiet master (-27.8 dBFS); needs about 8 dB of gain.
- **Arc**: steady for the first 100 s → dip 100–135 s → re-entry at 135 s (+8.8 dB) → fade from 170 s.
- **Why not higher**: the "Mo Li Hua" (Jasmine Flower) melody is too recognisable; it pulls attention from the narration and steers associations toward Jiangnan / jasmine instead of the moon and homesickness.

### No. 5: Scott Buckley "The Long Way Home" (CC BY 4.0)
- **Character**
  - The composer describes it as simple, nostalgic piano, almost a lullaby, with soft strings and synths.
  - The quietest and least intrusive.
  - Settles into a quiet coda after about 125 s.
- **Weakness**: no soft start (the first window is already -8 dB), almost flat overall, and no Chinese flavour. A safe fallback when you want "soft, never in the way".

---

## Candidate details

### 1. `km_Ripples.mp3`
- **Title / composer**: Ripples / Kevin MacLeod
- **Licence**: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
- **Attribution**: "Ripples" Kevin MacLeod (incompetech.com) / Licensed under Creative Commons: By Attribution 4.0 License / http://creativecommons.org/licenses/by/4.0/
- **Source**: https://incompetech.com/music/royalty-free/mp3-royaltyfree/Ripples.mp3 (catalogue page: https://incompetech.com/music/royalty-free/music.html)
- **Length**: 3:25 (205.5 s)
- **Tempo**: catalogue says 57 BPM; librosa estimates 117 (a double-time error)
- **Instruments and mood from the source page**
  - Instrument list says "Koto".
  - The description calls it the lonely plucking of a Chinese guzheng, calm as flowing water, suited to introspective, Asian-themed content.
  - Feel tags: Calming, Mystical, Relaxed.
- **Analysis**
  - RMS -22.2 dBFS, spectral centroid 893 Hz.
  - Energy split: low 0.17 / mid 0.82 / high 0.01.
  - perc 0.017, pent(C) 0.83.
- **5 s loudness curve (dB)**:
  - 0–25 s: -18 -17 -13 -15 -11 -12
  - 30–55 s: -16 -11 -14 -14 -16 -15
  - 60–85 s: -14 -16 -11 -13 -16 -12
  - 90–115 s: -10 -13 -14 -14 -13 -12
  - 120–145 s: -13 -14 -21 -13 -9 -12
  - 150–175 s: -10 -11 -13 -11 -16 -14
  - 180–205 s: -13 -9 -12 -21 -50 (end)
- **Swells**: 10 s (+4.1), 70 s (+3.8), a brief pause at 130 s (-7.8) then a swell at 140 s (+8.4, the biggest in the track), 185 s (+4.3); fades from about 195 s.
- **Verdict**: a steady guzheng bed, good under narration.

### 2. `km_Nu_Flute.mp3`
- **Title / composer**: Nu Flute / Kevin MacLeod
- **Licence**: CC BY 4.0
- **Attribution**: "Nu Flute" Kevin MacLeod (incompetech.com) / Licensed under Creative Commons: By Attribution 4.0 License / http://creativecommons.org/licenses/by/4.0/
- **Source**: https://incompetech.com/music/royalty-free/mp3-royaltyfree/Nu%20Flute.mp3
- **Length**: 1:23 (82.8 s)
- **Tempo**: catalogue says 60 BPM; librosa estimates 129 (a double-time error)
- **Instruments and mood from the source page**
  - Instrument list: Flute, Strings. The description says it is a dizi.
  - Feel tags: Calming, Relaxed, Somber, Uplifting.
- **Analysis**
  - RMS -18.7 dBFS, spectral centroid 967 Hz.
  - Energy split: low 0.31 / mid 0.68.
  - perc 0.006, pent(C) 0.61 (the string harmony includes F, a Western orchestration).
- **5 s loudness curve (dB)**:
  - 0–25 s: -9 -8 -5 -9 -6 -8
  - 30–55 s: -9 -5 -6 -8 -8 -8
  - 60–80 s: -8 -14 -7 -10 -46 (end)
- **Swells**: 10 s (+3.9), 35 s (+3.8), a dip at 65 s (-6.3) then a swell at 70 s (+4.3); ends at 80 s.
- **Verdict**: good for the closing section.

### 3. `pb_NastelBom_Asian_China_Chinese_Music.mp3`
- **Title / composer**: Asian - Asian China Chinese Music / NastelBom (Dmitrii Spis)
- **Licence**: Pixabay Content License (https://pixabay.com/service/license-summary/)
  - Free for commercial and non-commercial use, may be modified, no attribution required.
  - The music may not be sold or redistributed on its own.
  - **The page is marked "Content ID Registered"**.
- **Attribution (optional, recommended)**: Music: "Asian - Asian China Chinese Music" by NastelBom via Pixabay
- **Source**: https://pixabay.com/music/classical-string-quartet-asian-asian-china-chinese-music-501705/
  - Audio URL: https://cdn.pixabay.com/download/audio/2026/03/13/audio_494876aaa5.mp3
- **Length**: 2:59 (178.5 s)
- **Tempo**: librosa estimates 89
- **Instruments and mood from the source page**
  - Description: an atmospheric instrumental using traditional Chinese instruments.
  - Genre: Classical String Quartet / China. Mood: Relaxing, Peaceful.
  - Tags: Chinese flute, Chinese festival, Oriental.
  - Not marked as AI-generated on Pixabay.
- **Analysis**
  - RMS -13.5 dBFS (very loud), spectral centroid 1465 Hz.
  - Energy split: mid 0.95.
  - perc 0.010, pent(B) 0.84.
- **5 s loudness curve (dB)**:
  - 0–25 s: -18 -18 -16 -14 -8 -6
  - 30–55 s: -6 -6 -5 -6 -6 -6
  - 60–85 s: -7 -7 -7 -6 -7 -6
  - 90–115 s: -7 -6 -8 -6 -12 -13
  - 120–145 s: -13 -12 -6 -7 -6 -5
  - 150–175 s: -4 -6 -5 -7 -6 -32 (end)
- **Swells**: 20 s (+6.9, full entry), 25 s (+5.2); dip 110–125 s; swell at 130 s (+6.3), peak at 150 s (-4).
- **Verdict**: the most complete arc in a single track, the most authentically Chinese.

### 4. `sb_EchoesOfHome.mp3`
- **Title / composer**: Echoes Of Home / Scott Buckley
- **Licence**: CC BY 4.0
- **Attribution (composer's format)**: 'Echoes Of Home' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au
  - Composer's requirement: for YouTube videos the attribution must be in the video description.
- **Source**: https://www.scottbuckley.com.au/library/echoes-of-home/
  - Audio URL: https://www.scottbuckley.com.au/library/wp-content/uploads/2025/05/EchoesOfHome.mp3
- **Length**: 4:52 (291.7 s)
- **Tempo**: librosa estimates 136 (unreliable)
- **Instruments and mood from the source page**: warm, nostalgic orchestral music, close in spirit to Zelda games and Ghibli films.
- **Analysis**
  - RMS -17.2 dBFS, spectral centroid 857 Hz.
  - Energy split: low 0.72 (a thick bed of strings and bass).
  - perc 0.028, pent 0.63 (Western harmony).
- **5 s loudness curve (dB)**:
  - 0–25 s: -22 -24 -22 -20 -22 -22
  - 30–55 s: -21 -20 -20 -19 -19 -14
  - 60–85 s: -16 -14 -16 -12 -12 -14
  - 90–115 s: -12 -11 -12 -12 -12 -12
  - 120–145 s: -12 -11 -9 -10 -10 -7
  - 150–175 s: -7 -8 -10 -9 -10 -11
  - 180–205 s: -9 -10 -10 -12 -14 -13
  - 210–235 s: -14 -14 -14 -13 -12 -13
  - 240–265 s: -12 -12 -9 -8 -7 -10
  - 270–290 s: -9 -16 -20 -29 -55 (end)
- **Swells**: 55 s (+5.2); slow rise 130–155 s to the main climax (-7); second climax 250–260 s (-7); fades from 275 s.
- **Verdict**: one long crescendo; the climax comes late.

### 5. `pb_MoLiHua_JasmineFlower.mp3`
- **Title / composer**: Mo Li Hua - Chinese Jasmine Flower / NourishedByMusic
- **Licence**: Pixabay Content License. No attribution required; the page is not marked Content ID or AI-generated.
- **Attribution (optional)**: Music: "Mo Li Hua - Chinese Jasmine Flower" by NourishedByMusic via Pixabay
- **Source**: https://pixabay.com/music/china-mo-li-hua-chinese-jasmine-flower-356371/
  - Audio URL: https://cdn.pixabay.com/download/audio/2025/06/07/audio_61d4f3c103.mp3
- **Length**: 3:26 (206.1 s)
- **Tempo**: librosa estimates 99
- **Instruments and mood from the source page**
  - Tags: Chinese, Flute, Oriental, Classical, Instrumental, Ambient.
  - Mood: Bright, Dreamy, Relaxing, Peaceful, Elegant, Floating.
  - Arrangement of the traditional folk song "Mo Li Hua" (Jasmine Flower).
- **Analysis**
  - RMS -27.8 dBFS (very quiet), spectral centroid 1759 Hz.
  - Energy split: low 0.004, mid 0.90, high 0.10.
  - perc 0.009, pent(C) 0.79.
- **5 s loudness curve (dB)**:
  - 0–25 s: -6 -5 -5 -7 -6 -8
  - 30–55 s: -10 -6 -5 -6 -7 -6
  - 60–85 s: -8 -8 -5 -6 -6 -8
  - 90–115 s: -6 -9 -15 -13 -12 -13
  - 120–145 s: -12 -13 -15 -6 -5 -5
  - 150–175 s: -6 -6 -8 -9 -17 -16
  - 180–205 s: -20 -21 -17 -16 -18 -22
- **Swells**: dip at 100 s (-7.3); re-entry at 135 s (+8.8), 140 s (+5.3); fades from 170 s.

### 6. `sb_TheLongWayHome.mp3`
- **Title / composer**: The Long Way Home / Scott Buckley
- **Licence**: CC BY 4.0
- **Attribution**: 'The Long Way Home' by Scott Buckley - released under CC-BY 4.0. www.scottbuckley.com.au
- **Source**: https://www.scottbuckley.com.au/library/the-long-way-home/
  - Audio URL: https://www.scottbuckley.com.au/library/wp-content/uploads/2021/05/sb_thelongwayhome.mp3
- **Length**: 2:53 (172.7 s)
- **Tempo**: librosa estimates 185 (unreliable, free-tempo piano)
- **Instruments and mood from the source page**: soft, simple, nostalgic piano, almost a lullaby; gentle strings and synths carry it drifting home.
- **Analysis**
  - RMS -18.6 dBFS, spectral centroid 482 Hz (very dark, very soft).
  - perc 0.049.
- **5 s loudness curve (dB)**:
  - 0–25 s: -8 -10 -8 -8 -9 -6
  - 30–55 s: -7 -7 -7 -9 -9 -8
  - 60–85 s: -7 -8 -9 -7 -7 -6
  - 90–115 s: -6 -5 -6 -5 -6 -5
  - 120–145 s: -6 -10 -13 -13 -14 -14
  - 150–170 s: -16 -15 -17 -34 -40 (end)
- **Swells**: no obvious sudden entry; 95–120 s is a gentle plateau peak (-5); quiet coda from 125 s.

---

## Considered but not chosen (with reasons)
- **Kevin MacLeod**
  - Shenyang: erhu, pipa, yangqin plus percussion, 129 BPM, too upbeat.
  - Guzheng City: has dhol drums, pitched as "hotel lobby".
  - Cattails: banjo, accordion and erhu, a country-western feel.
  - Senbazuru, Finding Movement, Ishikari Lore: all koto, Japanese in feel.
- **Scott Buckley**
  - Moonlight: piano and strings, 2022; the title fits well, but 25–150 s is one long plateau and there is no Chinese flavour. Download path wp-content/uploads/2022/07/Moonlight.mp3, a possible backup.
  - Amberlight: has a Joe Hisaishi feel, but runs 4:43 with the peak in the middle.
  - Home Was You: folk percussion, perc 0.215.
- **Pixabay**
  - Everything by kaazoom (A Peaceful Morning, Back To Hong Kong, Bamboo and Paper Lanterns, Mountain Spring, etc.): the author's bio says all their work is AI-generated.
  - RainStreetCat, Asian_Background_Music, AiCanvas, JorisVermeer "Gentle Chinese Flute & Strings": either marked AI-generated or mass-produced BGM.
  - VPRODMUSIC "Mid Autumn Festival": percussion and a march feel, perc 0.14, heavy low end; also marked Content ID Registered.
  - VPRODMUSIC "Hoi An Ancient Charm": Vietnamese theme, marked Content ID Registered.
  - "lasting sorrow": anonymous uploader (user ID 38534292), 14 minutes long, sad in tone.
  - Joylo1111 "Plum Blossom (pure piano)": 5:19, leans toward Taiwanese pop piano. A possible alternate.
- **Chinese category on free-stock-music.com**: almost all New Year, epic or EDM, or licensed CC BY-NC / BY-SA, which does not meet the requirements.

## End credits (if using the first choice)
```
Music:
"Ripples" Kevin MacLeod (incompetech.com)
"Nu Flute" Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/
```
