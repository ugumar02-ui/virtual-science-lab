# Virtual Science Lab — AKU-EB

An interactive virtual laboratory for **AKU-EB SSC and HSSC** Physics, Chemistry and
Biology practicals. Students set up the apparatus, take readings, and the app checks
their result against the accepted value — with the same apparatus, procedure and viva
questions as the school lab.

Built with Python and Streamlit. Runs in a browser on a laptop, in the school computer
lab, or on an Android phone.

## Quick start

```bash
cd Projects/virtual-science-lab
./run.sh
```

Then open <http://localhost:8501>.

Or manually:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

## What is inside

**35 practicals** across grades IX–XII, taken from the AKU-EB 2025–26 syllabi.

| Subject | IX | X | XI | XII | Total |
|---|---|---|---|---|---|
| Physics | 4 | 4 | 2 | 2 | 12 |
| Chemistry | 3 | 5 | 2 | 2 | 12 |
| Biology | 7 | 1 | 3 | 0 | 11 |

Every practical carries the **exact AKU-EB topic and activity number** it was built from.
The app shows that reference under the title, and the *Syllabus coverage* page compares
the number of simulations with the number of activities listed in each official table
(205 activities in total). See [`docs/SYLLABUS_COVERAGE.md`](docs/SYLLABUS_COVERAGE.md)
for the full audit.

Every practical has:

- **Theory** and **procedure** written for the AKU-EB paper
- An **interactive simulation** with the real apparatus values (lengths, concentrations,
  voltages, temperatures)
- An **observation table** with realistic experimental noise
- A **result check** — measured value vs accepted value with percentage error
- **Viva questions** with model answers
- A **downloadable lab report** (Markdown) with readings, result and precautions

### The titration canvas

The two volumetric analysis practicals (standardising NaOH, and the molarity of oxalic
acid) open with a **real burette**: a stopcock you can turn, drops that fall into the
conical flask, a meniscus that moves down the scale, and phenolphthalein that flashes
pink and then stays pink at the endpoint. The student reads the burette themselves and
types the titre in — the concentration is then calculated from *their* reading, not from
a hidden model answer.


### Teacher mode

Instructor-only values (true acid concentration, true diameter, spring stiffness) are
hidden from students. Turn on **Teacher mode** in the sidebar to reveal them — useful for
setting different versions of the same practical.

## Project structure

```
virtual-science-lab/
├── app.py                  # Streamlit entry point and navigation
├── content/                # the syllabus: every practical is a dict here
│   ├── physics.py
│   ├── chemistry.py
│   └── biology.py
├── core/                   # simulation engines — pure Python, no Streamlit
│   ├── physics/engines.py
│   ├── chemistry/engines.py
│   ├── biology/engines.py
│   └── registry.py
├── ui/renderer.py          # schema-driven page: controls, plot, table, report
├── ui/canvas.py            # Tier-2 canvas widgets (titration burette)
├── ui/titration_canvas.html
├── tests/                  # engine and canvas tests
└── .streamlit/config.toml  # theme
```

The separation matters: `core/` contains no Streamlit imports, so the same physics and
chemistry can later power a Flutter/desktop build without rewriting the maths.

## Adding a practical

1. Add a function to the right `core/*/engines.py` that returns a dict:

```python
{
    "kind": "quantitative",        # or "qualitative"
    "measured": 9.81,
    "accepted": 9.81,
    "table": [...],                # list of dicts -> observation table
    "series": [...],               # optional plot series
    "notes": ["..."],              # teaching notes shown after the result
    "extras": [("Period T", "2.006", "s")],
}
```

2. Add an entry to `content/physics.py` pointing at `"physics.engines.my_function"`,
   with `controls`, `quantity`, `theory`, `procedure` and `viva`.

No changes to `app.py` or `renderer.py` are needed — the page is generated from the
content schema.

## Tests

```bash
.venv/bin/python -m unittest discover -s tests -v
```

## Deployment

### 1. Streamlit Community Cloud (free, public URL)

1. Push this folder to GitHub.
2. Go to <https://share.streamlit.io>, sign in with GitHub.
3. New app → repository → branch `main` → main file `app.py`.
4. Deploy. You get a URL like `https://your-lab.streamlit.app`.

### 2. School LAN (no internet needed)

```bash
./run-lan.sh
```

Students open `http://<teacher-computer-ip>:8501` on any device on the same Wi-Fi.
Allow port 8501 through the firewall if needed.

### 3. Desktop app (`.AppImage` / `.exe`)

```bash
.venv/bin/pip install pyinstaller
```

Bundle a launcher that runs `streamlit run app.py`, then build with PyInstaller. Add the
`content/`, `core/` and `ui/` folders with `--add-data`. This is the fiddliest target —
do it after the cloud version is working.

### 4. Android

Open the deployed URL in Chrome → menu → **Add to Home screen**. It installs as a PWA
with its own icon and full-screen window. A real APK later is just a thin WebView wrapper
around the same URL.

## Roadmap

- [x] Tier-2 canvas simulation: titration burette with stopcock, drops and endpoint flash
- [ ] Tier-2 canvas simulations: microscope focusing, circuit wiring
- [ ] Student accounts and saved attempts (SQLite → Postgres)
- [ ] Teacher dashboard with class results and common mistakes
- [ ] PDF lab reports matching the AKU-EB format
- [ ] Urdu labels
- [ ] More HSSC practicals (potentiometer, slide-wire bridge, sonometer, Mohr's salt)

## Notes

- All simulations are deterministic for a given "trial run" number, so a student can
  reproduce a reading.
- Values include realistic experimental noise; results are expected to land within a
  few percent of the accepted value, not exactly on it.
