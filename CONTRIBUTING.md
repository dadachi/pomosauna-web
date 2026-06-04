# Contributing to PomoSauna

Thanks for your interest! PomoSauna is intentionally tiny, and contributions
that keep it that way are very welcome.

## The shape of this project

The **entire app is one file**: [`index.html`](index.html). Markup, CSS, and all
JavaScript (wrapped in a single IIFE) live there. There is:

- **No build step**, no bundler, no transpiler.
- **No dependencies** and no `package.json`.
- **No test suite** — you verify changes by running the page in a browser.

Vanilla JS, Canvas 2D, and the Web Audio API only. Please don't introduce a
framework, a build tool, or an npm dependency without opening an issue to
discuss it first.

## Running it locally

Serve over HTTP (not `file://` — browsers block Web Audio there):

```sh
python3 -m http.server 8000   # then visit http://localhost:8000
```

- Web Audio needs a **user gesture** to start, so click **"Enter the sauna"**
  before expecting any sound.
- Append **`?fast=1`** to shorten the phases to 25s / 5s (instead of 25min /
  5min) so you can exercise phase transitions and the countdown ring quickly.

## Colours: Refactoring UI Palette 6 only

Every colour — in both CSS **and** the canvas — must come from Refactoring UI
Palette 6, exposed as CSS variables (`--sauna-1/2`, `--water-1/2`, `--ink`,
`--ring-sauna`, `--ring-water`). When you change colours, stay within the
palette. Alpha/opacity may vary freely (transparency is compositing, not a new
colour).

A CI check (`scripts/check-palette.py`, run by the `palette` job in
[`.github/workflows/checks.yml`](.github/workflows/checks.yml)) **fails the
build if any colour falls outside the palette.** You can run it yourself before
pushing:

```sh
python3 scripts/check-palette.py index.html
```

## A few conventions

- The display name is **`PomoSauna`** (camelCase) everywhere user-visible.
- Don't rename the `pomosauna.prefs` `localStorage` key — it would orphan every
  existing user's saved sound preferences. (The key stays lowercase even though
  the display name is camelCase.)
- Keep the diff small and the page self-contained.

## Submitting changes

1. Fork the repo and create a branch off `main`.
2. Make your change in `index.html` (and `scripts/` if relevant).
3. Test it in a browser — both phases, the mixer, and the countdown ring — and
   confirm the palette check passes.
4. Open a pull request describing **what** changed and **why**. Screenshots or a
   short clip help a lot for visual changes.

`main` is protected: PRs require a passing `palette` check before they can be
merged.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By
participating you agree to uphold it.
