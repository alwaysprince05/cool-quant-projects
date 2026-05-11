"""FastAPI app: interactive Plotly APIs + static dashboard."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from web.compute import compute_p1, compute_p2, compute_p3

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="Cool Quant Projects", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/p1")
def api_p1(
    K: float = Query(100.0, ge=50, le=200),
    r: float = Query(0.05, ge=0.0, le=0.2),
    sigma: float = Query(0.25, ge=0.05, le=1.0),
    T0: float = Query(1.0, ge=0.1, le=3.0),
    seed: int = Query(42),
):
    return compute_p1(K=K, r=r, sigma=sigma, T0=T0, seed=seed)


@app.get("/api/p2")
def api_p2(
    n_paths: int = Query(3000, ge=200, le=15000),
    n_days: int = Query(252, ge=60, le=504),
    mu_ann: float = Query(0.12, ge=-0.2, le=0.5),
    sig_ann: float = Query(0.22, ge=0.05, le=0.8),
    df_t: int = Query(4, ge=2, le=30),
    shock_prob: float = Query(0.07, ge=0.0, le=0.3),
    seed: int = Query(7),
    fan_paths: int = Query(60, ge=10, le=200),
):
    return compute_p2(
        n_paths=n_paths,
        n_days=n_days,
        mu_ann=mu_ann,
        sig_ann=sig_ann,
        df_t=df_t,
        shock_prob=shock_prob,
        seed=seed,
        fan_paths=fan_paths,
    )


@app.get("/api/p3")
def api_p3(
    n_days: int = Query(504, ge=120, le=2000),
    win: int = Query(30, ge=10, le=120),
    seed: int = Query(99),
):
    return compute_p3(n_days=n_days, win=win, seed=seed)


app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
