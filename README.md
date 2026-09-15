# Gravity Simulation Project

A little personal project built for fun in high school: simulating Newtonian gravity between objects, from a single falling ball (1D) up to a full N-body system in 3D. No AI was used to write the physics or logic — the only exception is part of the `dessiner_scene` (display) functions, which handle the pygame/matplotlib rendering and aren't the point of the exercise.

Everything in the code (comments, variable names, input prompts) is in French. This README was written with Claude's help.

## Repository structure

```
.
├── projet_simulation_gravité_récursivité.py   # 1D: one ball falling under gravity
├── projet_sim_gravité_2D.py                   # 2D: two bodies attracting each other
├── projet_sim_3D.py                           # 3D: N bodies attracting each other
├── univers_terre_lune_soleil.json             # example universe: Sun + Earth + Moon
├── univers_systeme_solaire_reel.json          # example universe: Sun + the 8 planets
└── univers_trois_soleils_chaos.json           # example universe: 3-star chaotic system + a planet
```

## Requirements

```bash
pip install pygame numpy matplotlib
```

(`pygame` is used for the 1D/2D scripts, `matplotlib` for the 3D one, `numpy` for the vector math.)

---

## 1. 1D — `projet_simulation_gravité_récursivité.py`

The starting point of the project: a single ball dropped from a height above the Earth's surface, falling under gravity until it hits the ground (`y <= 0`). The physics step is driven by a **recursive function** (`gravité_sim`) that recalculates the force, acceleration, velocity and position, redraws the scene with `pygame`, then calls itself for the next step.

Run it and answer the prompts:

```bash
python projet_simulation_gravité_récursivité.py
```

You'll be asked for:
- the ball's starting height above the ground (m)
- its starting acceleration (usually `0`)
- its starting vertical velocity (m/s)

Earth's mass and the ball's mass (1000 kg) are hardcoded at the top of the file.

## 2. 2D — `projet_sim_gravité_2D.py`

Two objects, each with its own mass, radius, position, and velocity, attracting each other in a 2D plane. Same recursive approach as the 1D version, but now the force is split into x/y components for each object, and both objects move. The simulation stops if the two objects end up at the exact same coordinates.

```bash
python projet_sim_gravité_2D.py
```

You'll be prompted for both objects' mass, radius, starting position (x, y) and starting velocity (x, y).

## 3. 3D / N-body — `projet_sim_3D.py`

The full version: any number of objects (`n ≥ 0`) attracting each other in 3D. Instead of hardcoding two objects, all bodies live in a list of dictionaries called `univers` ("universe"), and the script computes the pairwise distance and gravitational force between **every pair** of objects, then sums up each object's total acceleration. This version uses a `while True` loop rather than recursion. Rendering is done with `matplotlib` in 3D, with trailing paths for each object and a radio-button panel to lock the camera onto a specific body.

```bash
python projet_sim_3D.py
```

On launch it asks if a `univers.json` file is present in the script's folder (`1` for yes, `0` for no). In practice you want to say yes — manual entry for more than a couple of objects isn't really supported (see the comment in the code about that). To use one of the example universes below, just rename it (or copy it) to `univers.json` in the same folder as the script.

### Universe file format

Each object in the JSON is a dictionary with:

```json
{
  "x": 0.0, "y": 0.0, "z": 0.0,
  "vitx": 0.0, "vity": 0.0, "vitz": 0.0,
  "accx": 0.0, "accy": 0.0, "accz": 0.0,
  "M": 5.972e24,
  "R_o": 6371000.0
}
```

- `x`, `y`, `z` — position in meters
- `vitx`, `vity`, `vitz` — velocity in m/s
- `accx`, `accy`, `accz` — acceleration in m/s² (start these at `0`, they're computed by the sim)
- `M` — mass in kg
- `R_o` — radius in meters (used for display scaling)
- `nom` (optional) — a display name; if present it's used in the camera-lock menu and title instead of "Object i"

### Example universes included

| File | What it is |
|---|---|
| `univers_terre_lune_soleil.json` | Sun, Earth and Moon, with roughly real masses, distances and orbital velocities |
| `univers_systeme_solaire_reel.json` | The Sun and all 8 planets (Mercury to Neptune), with realistic masses/distances/velocities |
| `univers_trois_soleils_chaos.json` | Three star-mass bodies (~2×10³⁰ kg) plus a small planet — a chaotic three-body-style setup |

---

## Notes

- The physics is plain Newtonian gravitation: `F = G·(M1·M2)/d²`, with everything in SI units (meters, kilograms, seconds).
- The time step (`pas_de_temps`) is adjustable in each script — smaller means a more accurate but slower simulation, larger means faster but choppier/less stable.
- Progress is printed to the console at every step for debugging.
