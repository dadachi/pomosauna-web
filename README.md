# PomoSauna

A calm Pomodoro focus timer. A monk meditates through 25 minutes of sauna heat,
then cools beneath a waterfall — work alongside him.

**Live:** https://dadachi.github.io/pomosauna-web/

- A single static `index.html` — vanilla JS, Canvas, and Web Audio. No build
  step, no dependencies, no sign-up.
- Fully synthesized sound: a per-phase mixer lets you choose the cue and
  ambience sounds, set their volume, and mute them; preferences are saved
  locally.
- A circular countdown ring that takes on each phase's colour — tap it to
  pause/resume.

## Run it

Just open `index.html` in a browser, or serve the folder over HTTP (needed for
Web Audio):

```sh
python3 -m http.server 8000
# then visit http://localhost:8000
```
