# Lemo-Opuscar: instructions for agents

This repository is a library of film styles. Each style has a `styles/<slug>/STYLE.md` (what the style is) and one demo film made entirely in code (`DEMO.md` and `demo/`). People pick a style and ask for a film about **their own** topic. Your job is to direct and produce that film.

| The request | Go to |
|---|---|
| A film about the user's topic (the normal case) | **Style and story**, **Workflow** below |
| "Which styles are there?" / no style chosen | **Finding the style** below |
| Directing: story, sound, rhythm, camera, checks, delivery | [`DIRECTOR.md`](DIRECTOR.md) |
| Building: install, pages, voice, music, mix | [`TECHNIQUE.md`](TECHNIQUE.md) |
| Tool commands and flags | [`core/README.md`](core/README.md) |
| Adding a style to the library (owner only) | [`MAINTAINING.md`](MAINTAINING.md) |

**Films outside `styles/` are the user's: no LemoLab credit, no watermark.**

## Style and story

- **`STYLE.md` is fixed**: the style's invariants (look, colour, type, motion, camera grammar, sound palette, native moves, pitfalls). Keep all of it.
- **Everything else is yours to direct** from the user's topic: story, structure, characters, settings, shots, timings, references, how data is charted. Never bend the topic toward the demo.
- **Treatment first, demo later.** Write your own `TREATMENT.md`, with three candidate structures and your choice (DIRECTOR.md §4), before you open `DEMO.md` or the demo code. Then use the demo only to learn techniques (a brush engine, a rig, a shader, a mix), never its story, arc, shots, props or timeline.
- **Scene styles** (a set-up guide, a spec walkthrough, a museum plate, a trail guide) list use cases in their `STYLE.md`. Read them as grammar for the order in which information arrives and how long each part needs on screen, then build the user's content in your own structure. Swapping text into a demo's `content.json` is only a technical check, never the way to deliver.
- Never build inside `styles/`: copy what you need into the film's project folder.

## Finding the style

Users name a style by its gallery name ("Impasto Oil Painting") or by its folder (`impasto`). Look it up in [`styles/README.md`](styles/README.md). If nothing matches clearly, show the closest two or three and ask.

If the user hasn't picked a style:
- Suggest two or three that fit their topic.
- Show them the full list below in the chat. Don't drop, merge or rename anything.
- Link the gallery, where every style has its demo film: https://lemomo-ai.github.io/lemo-opuscar/

<!-- style-list:start -->
All 43 styles:

- **Hand-drawn & Painting** (7): Crayon Picture Book, Watercolor Brush, Chinese Ink Wash, Impasto Oil Painting, One-line Drawing, Whiteboard Explainer, Urban Sketch · Pen & Wash
- **East Asian Traditions** (4): Shadow Puppetry, Ukiyo-e, Red Paper-cut, Paper-cut Lightbox
- **Print & Printmaking** (5): Risograph Print, Halftone Dossier, Woodcut Print, Copperplate Engraving, Silkscreen Travel Poster
- **Graphic & Type** (7): Swiss Motion Graphics, 60s Spy Title Sequence, Art Deco, Blueprint, Stained Glass, Pictogram Motion, ASCII / CRT Terminal
- **Information & Keynote** (5): Data Storytelling, Isometric Infographic, Dark Tech Keynote, Living Screencast, Sci-fi Hologram HUD
- **Cartoon & Anime** (4): 1930s Rubber Hose Cartoon, 80s Cel Anime, Sci-Fi Sitcom Toon, Mid-century Cartoon
- **Games** (4): 16-bit Pixel RPG, HD-2D, Microgame Frenzy, Game Show Flat
- **Cinema & Eras** (2): 1920s Silent Film, Liminal Found Footage
- **Materials & 3D** (5): Brick Toy, Paper Pop-up Book, Tilt-Shift Miniature, Low-poly Isometric Island, Glass Product Render
<!-- style-list:end -->

## Workflow

1. **Brief.** Make sure the style and the topic are clear, then ask the user once, in a single message (DIRECTOR.md §1):
   - anything about the topic you can't decide yourself (facts; names, logos or products that must appear);
   - whether they have material of their own: a voice recording or a preferred voice, music, photos, logos, fonts;
   - the film's language, if it isn't obvious (default: the language they write in, for voice and subtitles);
   - whether they want to review a storyboard first (default: no);
   - anything missing on their machine: first run `sh plugin/skills/lemo-opuscar/scripts/setup.sh deps` from the library root (core only) and include what it reports. Add the voice and music tiers later, only if the film needs them (TECHNIQUE.md §1).

   Skip what their request already answers. Wait for the reply, fill every other gap with a sensible default, sum up the brief in a few lines and start. Don't come back with more questions.
2. **Treatment.** Write `TREATMENT.md` in the project folder (DIRECTOR.md §4), before you open the demo.
3. **Look.** Render style frames or a model sheet with the real drawing code and check them against `STYLE.md` (DIRECTOR.md §5).
4. **Storyboard, only if the user asked for it** (DIRECTOR.md §5). **Stop and wait for approval.** Otherwise don't stop.
5. **Produce.** Voice → check → score (can run in parallel) → animation → mix → render (TECHNIQUE.md).
6. **Self-check and deliver** (DIRECTOR.md §11).

Report progress in the user's language. If a step fails, read the error, fix the cause and retry; go back to the user only for a decision or something only they can provide.

## Where things go

- The film's project folder is `films/<name>/` in a clone (ignored by git), or `<name>/` in the user's folder in skill mode (see the skill's `SKILL.md`). Wherever a guide says `films/<name>/`, read "the project folder". Work only there, unless the user asks you to work in their own project.
- Run `node core/…` and `sh tools/…` from the library root (`$LIB` in skill mode).
- `core/` has ready-made tools (rendering, TTS, speech check, sampler, sfx, mux). Use them or your own stack, but don't edit `core/` or `styles/` for a user's film.
- Never kill processes you didn't start. Don't leave background processes running.
