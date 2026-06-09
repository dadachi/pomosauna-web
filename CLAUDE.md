# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

PomoSauna is a Pomodoro focus timer rendered as a single static `index.html` —
vanilla JS, Canvas 2D, and the Web Audio API. **No build step, no dependencies,
no package.json, no tests, no framework.** Everything (markup, CSS, all logic)
lives in `index.html`, with the script wrapped in one IIFE.

A monk meditates through a 25-minute "sauna" phase, then a 5-minute "waterfall"
phase, cycling forever.

## Running & verifying

Serve over HTTP (don't open via `file://` — browsers block Web Audio there):

```sh
python3 -m http.server 8000   # then visit http://localhost:8000
```

- **Web Audio needs a user gesture** to start — the "Enter the sauna" button calls
  `ensureAudio()`, which lazily creates the `AudioContext`. Audio cannot start
  before that click.
- **`?fast=1`** shortens phases to 25s / 5s (instead of 25min / 5min) for quickly
  exercising phase transitions and the countdown ring.
- There is no test suite. Verify changes by serving the page and driving it in a
  browser (e.g. Playwright MCP). The canvas only repaints inside the
  `requestAnimationFrame` `tick` loop, so after a state change (e.g. clicking
  Skip), **wait a frame before screenshotting** or you'll capture the stale frame.

## Architecture (all in `index.html`)

- **State machine** — `state` holds the phase/timer; `PHASE = { SAUNA: "sauna",
  WATER: "water" }`. `enterPhase()` / `advancePhase()` drive the cycle. The `tick`
  loop (rAF) decrements `state.remaining`, calls `updateHud()` every frame while
  running, and `render()` always.
- **Rendering** — `render()` paints a background gradient then `drawSaunaScene()`
  / `drawWaterScene()`, plus `drawMonk()` and particle pools (`steam`, `drops`).
  The canvas is full-window behind the HUD (which is `pointer-events: none`).
- **Audio (fully synthesized, no audio files)** — two registries:
  - `CUE_SOUNDS` — one-shot sounds, `play(ac, now, v)` (löyly hiss, bell, bowl…).
  - `AMBIENT_SOUNDS` — looping sounds, `make(ac, v)` returning `{ setVol, stop }`
    (fire, waterfall, wind…). `ambientHandle()` / `loopNoise()` are the factories.
  - Dispatch: `playCue(phaseKey)`, `startAmbient(phaseKey)`, `stopAmbient(phaseKey)`.
    Live ambient handles are stored in `audio.ambient.{sauna,water}`.
- **Sound mixer & persistence** — the `sound` object is keyed by phase
  (`"sauna"`/`"water"`, deliberately matching the `PHASE` values) → channel
  (`cue`/`ambient`) → `{ mute, vol, id }`. Persisted to `localStorage` under
  `pomosauna.prefs` via `loadSound()` / `saveSound()`; `loadSound()` also migrates
  an older flat `{ muteCues, muteAmbient }` format. `buildMixer()` builds the
  per-channel UI (mute button, volume slider, sound `<select>`).
- **Countdown ring** — an SVG ring around the timer. `updateRing()` sets
  `stroke-dashoffset` and the knob position; its colour comes from the `--ring`
  CSS var, set per phase to `var(--ring-sauna)` / `var(--ring-water)`. The whole
  ring is a transparent tap target (`#ringTap`) that toggles pause.

## Project conventions / constraints

- **Colours: Palette 6 only.** Every colour (CSS *and* canvas) must come from
  Refactoring UI Palette 6, documented in `docs-private/palette-6.md`. CSS vars:
  `--sauna-1/2`, `--water-1/2`, `--ink`, `--ring-sauna`, `--ring-water`. When
  changing colours, stay within the palette; alpha (opacity) may vary freely
  since transparency is compositing, not a new colour.
- **`docs-private/` is gitignored** — internal notes (monetization, App Store ASO,
  the palette reference) live there and are intentionally *not* committed.
- **`*.png` is gitignored except `og-preview.png`** (a real tracked asset — the
  1200×630 social-share image referenced by the Open Graph tags). Scratch
  screenshots won't be accidentally committed.
- **Don't rename the `pomosauna.prefs` localStorage key** — it would orphan every
  user's saved sound preferences. The key stays lowercase even though the display
  name is camelCase.
- **Display name is `PomoSauna`** (camelCase) everywhere user-visible (title,
  start-screen heading, dynamic `document.title`).

## Deploy

Hosted on GitHub Pages from the public repo **`dadachi/pomosauna-web`** (origin),
live at https://dadachi.github.io/pomosauna-web/. Pushing `main` triggers a Pages
rebuild. The repo deliberately has a **clean single-commit history** (no
`docs-private/` ever in public history); the full development history is preserved
locally on the **`full-history`** branch, which is never pushed.

GoatCounter (cookieless analytics) is loaded via a snippet before `</body>`;
no `integrity=` hash is used because GoatCounter's `count.js` is mutable.

## gstack

Use the `/browse` skill from gstack for all web browsing. **Never** use
`mcp__claude-in-chrome__*` tools.

Available gstack skills: `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`,
`/plan-design-review`, `/design-consultation`, `/design-shotgun`, `/design-html`,
`/review`, `/ship`, `/land-and-deploy`, `/canary`, `/benchmark`, `/browse`,
`/connect-chrome`, `/qa`, `/qa-only`, `/design-review`, `/setup-browser-cookies`,
`/setup-deploy`, `/setup-gbrain`, `/retro`, `/investigate`, `/document-release`,
`/document-generate`, `/codex`, `/cso`, `/autoplan`, `/plan-devex-review`,
`/devex-review`, `/careful`, `/freeze`, `/guard`, `/unfreeze`, `/gstack-upgrade`,
`/learn`.
