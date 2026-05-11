---
title: Quant Terminal
emoji: 💎
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: true
license: mit
short_description: Professional Quant Finance Terminal — Greeks & Risk.
---

# 💎 Quant Terminal: Institutional-Grade Analytics

A high-performance quantitative finance dashboard for simulation-driven visualizations. Analyze **Option Greek Manifolds**, **Monte Carlo Drawdown Topologies**, and **Markov-Switching Correlations** in a premium, ultra-fast environment.

### 🔗 [View Live App on Hugging Face Spaces](https://huggingface.co/spaces/alwaysprince05e/cool-quant-projects)

---

## 🚀 Key Improvements

- **Ultra-Fast Performance:** Integrated client-side caching for near-instant switching between analysis modules.
- **Institutional Design:** A state-of-the-art terminal interface using glassmorphism, **Outfit** & **JetBrains Mono** typography.
- **Real-Time Monitoring:** Integrated latency and system status tracking.
- **Dynamic Risk Models:** Optimized Monte Carlo engines for deep drawdown analysis.

---

## 💎 Premium Features

- **Interactive 3D Manifolds:** Rotate and zoom into Option Greeks (Gamma, Theta) and P&L surfaces.
- **Advanced Risk Metrics:** Real-time calculation of **Sharpe Ratio**, **95% VaR**, and **CVaR (Conditional VaR)**.
- **Regime-Switching Dynamics:** Explore how asset correlations change during "Calm" vs. "Crisis" regimes.
- **High-Resolution Exports:** All simulations can be exported as high-res PNGs for research reports.
- **Premium Dark UI:** Professional-grade interface with fluid micro-animations and responsive layout.

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
├── Dockerfile                     # Deployment Configuration
├── README.md                      # Documentation
└── LICENSE                        # MIT License
```

---

## 📈 Dashboard Modules

### 1. Option Greeks Manifold
Visualize the sensitivity of European options to price and time.
- **P&L Surface:** Dynamic P&L based on Spot Price vs. Days to Expiration (DTE).
- **Gamma/Theta Surfaces:** Analyze the rate of change in Delta and the impact of time decay.

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
cd cool-quant-projects
```

### 2. Run with Helper Script
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
