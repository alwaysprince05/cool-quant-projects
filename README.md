---
title: Cool Quant Projects
emoji: 📊
colorFrom: dark-blue
colorTo: slate
sdk: docker
pinned: false
license: mit
short_description: Premium Quant Finance Dashboard — Option Greeks, Monte Carlo Drawdowns, & Correlation Dynamics.
---

# 🚀 Cool Quant Projects: Interactive Terminal

A high-performance quantitative finance dashboard for simulation-driven visualizations. Analyze **Option Greek Manifolds**, **Monte Carlo Drawdown Topologies**, and **Markov-Switching Correlations** in a premium, interactive environment.

### 🔗 [View Live App on Hugging Face Spaces](https://huggingface.co/spaces/alwaysprince05e/cool-quant-projects)

---

## 💎 Premium Features

- **Interactive 3D Manifolds:** Rotate and zoom into Option Greeks (Gamma, Theta) and P&L surfaces.
- **Advanced Risk Metrics:** Real-time calculation of **Sharpe Ratio**, **95% VaR**, and **CVaR (Conditional VaR)** for simulated paths.
- **Regime-Switching Dynamics:** Explore how asset correlations change during "Calm" vs. "Crisis" regimes using Markov-chain simulations.
- **High-Resolution Exports:** All simulations are built on Plotly and can be exported as high-res PNGs for research reports.
- **Premium Dark UI:** A professional-grade interface built with glassmorphism, modern typography (Inter/Fira Code), and fluid micro-animations.

---

## 🛠 Repository Structure

```
cool-quant-projects/
├── web/                           # Core Application
│   ├── app.py                     # FastAPI Backend & API Routes
│   ├── compute.py                 # Quant Logic (Black-Scholes, Monte Carlo, Markov-Switching)
│   ├── requirements.txt           # Python Dependencies
│   ├── run_dashboard.sh           # Local Execution Script
│   └── static/                    # Premium UI (HTML/CSS/JS)
├── gallery/                       # Static PNG Exports
├── Dockerfile                     # Hugging Face Spaces Deployment Configuration
├── README.md                      # Documentation
└── LICENSE                        # MIT License
```

---

## 📈 Dashboard Modules

### 1. Option Greeks Manifold
Visualize the sensitivity of European options to price and time.
- **P&L Surface:** Dynamic P&L based on Spot Price vs. Days to Expiration (DTE).
- **Gamma/Theta Surfaces:** Analyze the rate of change in Delta and the impact of time decay across the manifold.

### 2. Drawdown Topology (Monte Carlo)
Simulate thousands of portfolio paths with fat-tailed returns.
- **Fat-Tailed Shocks:** Mixture of Normal and Student-t distributions for realistic market stress.
- **Risk Analytics:** Instant display of **Sharpe Ratio**, **Value at Risk (VaR)**, and **Conditional VaR (CVaR)**.
- **Density Surface:** A 3D view of drawdown probability over time.

### 3. Correlation Regime Dynamics
Analyze how multi-asset portfolios behave during market shifts.
- **Markov-Switching:** Two-state simulation (Calm vs. Crisis) with unique correlation matrices.
- **Rolling Correlations:** Observe "correlation to one" phenomena during simulated stress events.

---

## 🚀 Quick Start (Local Development)

### 1. Clone the Repository
```bash
git clone https://github.com/alwaysprince05/cool-quant-projects.git
cd cool-quant-projects/cool-quant-projects
```

### 2. Run with Helper Script (Automatic Venv)
```bash
chmod +x web/run_dashboard.sh
./web/run_dashboard.sh
```
Visit **http://127.0.0.1:8844** in your browser.

### 3. Manual Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r web/requirements.txt
python -m uvicorn web.app:app --host 127.0.0.1 --port 8844
```

---

## 🐳 Docker & Cloud Deployment

This project is optimized for **Hugging Face Spaces** using the Docker SDK.

```bash
docker build -t quant-terminal .
docker run -p 7860:7860 quant-terminal
```

---

## 📜 License
MIT — See [LICENSE](LICENSE) for details.

**Maintained by [@alwaysprince05](https://github.com/alwaysprince05)**
l risk](https://en.wikipedia.org/wiki/Financial_risk)  
- [Correlation and dependence](https://en.wikipedia.org/wiki/Correlation_and_dependence)  

---

## License

MIT — see [LICENSE](LICENSE).
