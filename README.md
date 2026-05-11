---
title: Cool Quant Projects
emoji: 📊
colorFrom: gray
colorTo: blue
sdk: docker
pinned: false
license: mit
short_description: Interactive quant finance visualizations — FastAPI + Plotly (Greeks, drawdowns, correlations).
---

# Cool Quant Projects

Simulation-driven visualizations for quantitative finance: **Markov regime correlations**, **Monte Carlo drawdown topology**, and **Black–Scholes option Greeks** — as high-resolution Matplotlib exports and as an **interactive browser dashboard** (FastAPI + Plotly).

**Repository:** [github.com/alwaysprince05/cool-quant-projects](https://github.com/alwaysprince05/cool-quant-projects)  
**Maintainer:** [@alwaysprince05](https://github.com/alwaysprince05)  
**License:** [MIT](LICENSE)

---

## What is in this repo

| Layer | What it does |
|--------|----------------|
| **Python scripts** | Original demos: NumPy / SciPy / Matplotlib, save PNG figures. |
| **`web/`** | FastAPI backend + static SPA: change parameters, run simulations, **rotate/zoom** Plotly 3D charts in the browser. |
| **`gallery/`** | Simple HTML page that embeds the exported PNGs (optional static preview). |

No market data APIs or paid feeds — simulations use synthetic returns and closed-form option math.

---

## Repository layout

```
cool-quant-projects/
├── Correlation Regime Dynamics/   # P3 — rolling ρ, regime switching
│   ├── P3 correlations.py
│   ├── readme.md
│   └── p3_correlation_regimes.png # generated
├── Drawdown Topology/             # P2 — fat-tailed paths, drawdown density
│   ├── P2 drawdown.py
│   ├── Readme.d.md
│   └── p2_drawdown_topology.png   # generated
├── Option Greeks Manifold/        # P1 — BS Greeks & P&L surfaces
│   ├── P1 greeks.py
│   └── outputs/p1_greeks_manifold.png
├── web/                           # Interactive dashboard
│   ├── app.py                     # FastAPI routes + static mount
│   ├── compute.py                 # Plotly figure builders + JSON for Plotly.js
│   ├── requirements.txt
│   ├── run_dashboard.sh           # venv + uvicorn (recommended)
│   └── static/index.html          # UI
├── gallery/index.html             # Static gallery of PNGs
├── Dockerfile                     # Hugging Face Spaces (Docker SDK)
├── .dockerignore
├── README.md
└── LICENSE
```

---

## Quick start

### Clone

```bash
git clone https://github.com/alwaysprince05/cool-quant-projects.git
cd cool-quant-projects
```

### Core dependencies (Matplotlib scripts)

**Python 3.10+** recommended (3.8+ should work).

```bash
pip install numpy matplotlib scipy
```

---

## 1. Matplotlib demos (export PNGs)

Run from the **repository root** (`cool-quant-projects/`). Paths use quotes because folder names contain spaces.

### Option Greeks Manifold

```bash
python3 "Option Greeks Manifold/P1 greeks.py"
```

Writes: `Option Greeks Manifold/outputs/p1_greeks_manifold.png`  
Opens an interactive Matplotlib window (`plt.show()`).

### Drawdown topology

```bash
python3 "Drawdown Topology/P2 drawdown.py"
```

Writes: `Drawdown Topology/p2_drawdown_topology.png`

### Correlation regime dynamics

```bash
python3 "Correlation Regime Dynamics/P3 correlations.py"
```

Writes: `Correlation Regime Dynamics/p3_correlation_regimes.png`  
(Script ends after save; no `plt.show()` in the original.)

### Headless / CI (no display)

```bash
export MPLBACKEND=Agg
python3 "Option Greeks Manifold/P1 greeks.py"
```

---

## 2. Interactive web dashboard (recommended)

Browser UI with **tabs** (Greeks / Drawdown / Correlations), **form parameters**, and **Plotly** 3D charts (pan, zoom, rotate).

### Option A — helper script (creates `.venv`, installs web deps)

```bash
chmod +x web/run_dashboard.sh    # first time only
./web/run_dashboard.sh
```

Then open **http://127.0.0.1:8844/** (default port `8844`).

Custom port:

```bash
PORT=9000 ./web/run_dashboard.sh
```

### Option B — manual virtualenv (useful on PEP 668 / Homebrew Python)

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r web/requirements.txt
python -m uvicorn web.app:app --host 127.0.0.1 --port 8844
```

### Web stack versions (`web/requirements.txt`)

| Package | Role |
|---------|------|
| `fastapi` | HTTP API + serves `web/static/` |
| `uvicorn` | ASGI server |
| `plotly` | Figure JSON consumed by Plotly.js in the browser |
| `numpy`, `scipy` | Same numerics as the scripts |

### API (for tooling or `curl`)

| Method | Path | Purpose |
|--------|------|---------|
| `GET` | `/api/health` | Liveness |
| `GET` | `/api/p1?K=100&r=0.05&sigma=0.25&T0=1&seed=42` | Option surfaces |
| `GET` | `/api/p2?n_paths=3000&n_days=252&...` | Drawdown + fan + terminal bar |
| `GET` | `/api/p3?n_days=504&win=30&seed=99` | Correlation panels |

Open **http://127.0.0.1:8844/docs** for interactive OpenAPI when the server is running.

---

## 3. Static PNG gallery (optional)

From repo root, any static file server works, for example:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

Open **http://127.0.0.1:8765/gallery/index.html** to view the three exported figures side by side (refresh PNGs by re-running the Matplotlib scripts above).

---

## Hugging Face Spaces

This repo includes a **`Dockerfile`** so you can host the same FastAPI + Plotly app on [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces).

### Create the Space

1. Log in at [huggingface.co](https://huggingface.co) and open **Spaces → Create new Space**.
2. Choose a name, set visibility (Public is typical for demos), and select **Docker** as the SDK (not Gradio or Streamlit).
3. Under **Space repository**, either:
   - **Duplicate files**: push this GitHub repo to the Space git (clone, add remote `hf`, push), or  
   - **Connect a GitHub repository** (HF “Import from GitHub”) and point it at [alwaysprince05/cool-quant-projects](https://github.com/alwaysprince05/cool-quant-projects) on branch `main`.
4. Ensure the Space root contains the **`Dockerfile`** from this project (already at repo root after you sync).
5. Wait for the build to finish; HF will show **Running** when healthy.

The container runs:

`uvicorn web.app:app --host 0.0.0.0 --port 7860`

(`PORT` is honored if the platform sets it.) Open the Space URL — the UI loads from `/` and APIs from `/api/...`.

### Local Docker check (optional)

```bash
docker build -t cool-quant .
docker run --rm -p 7860:7860 cool-quant
```

Then visit **http://127.0.0.1:7860/**.

---

## Concepts you can explore

- Monte Carlo paths, running maximum, and drawdown distributions  
- Fat-tailed returns (mixture with Student-**t** shocks)  
- Two-state Markov regimes and Cholesky-correlated returns  
- Rolling correlation tensors and “correlation to one” intuition  
- Black–Scholes price, Delta, Gamma, Theta on a spot × time grid  
- Matplotlib 3D (`Poly3DCollection`, surfaces, `GridSpec`)  
- Plotly surfaces / scatter / heatmaps for the web dashboard  

---

## References

- [Monte Carlo method](https://en.wikipedia.org/wiki/Monte_Carlo_method)  
- [Markov chain](https://en.wikipedia.org/wiki/Markov_chain)  
- [Black–Scholes model](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model)  
- [Financial risk](https://en.wikipedia.org/wiki/Financial_risk)  
- [Correlation and dependence](https://en.wikipedia.org/wiki/Correlation_and_dependence)  

---

## License

MIT — see [LICENSE](LICENSE).
