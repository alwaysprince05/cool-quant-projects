"""Simulation + Plotly figure builders for the interactive dashboard."""
from __future__ import annotations

import base64
import json
from typing import Any

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.ndimage import gaussian_filter
from scipy.stats import norm


def _decode_plotly_binary_arrays(obj: Any) -> Any:
    """Plotly Python may emit ndarray-like dicts {dtype, bdata, shape?}; Plotly.js needs nested lists."""
    if isinstance(obj, dict):
        if "bdata" in obj and "dtype" in obj:
            raw = base64.b64decode(obj["bdata"])
            dtype = np.dtype(obj["dtype"])
            arr = np.frombuffer(raw, dtype=dtype)
            if "shape" in obj:
                sh = obj["shape"]
                if isinstance(sh, str):
                    shape = tuple(int(x.strip()) for x in sh.split(",") if x.strip())
                elif isinstance(sh, (list, tuple)):
                    shape = tuple(int(x) for x in sh)
                else:
                    shape = ()
                if shape:
                    arr = arr.reshape(shape)
            return arr.tolist()
        return {k: _decode_plotly_binary_arrays(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_decode_plotly_binary_arrays(x) for x in obj]
    return obj


def _fig_to_json(fig: go.Figure) -> dict[str, Any]:
    return _decode_plotly_binary_arrays(json.loads(fig.to_json()))


def bs(S, K, T, r, sigma, cp=1):
    T = np.maximum(T, 1e-9)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    price = cp * (S * norm.cdf(cp * d1) - K * np.exp(-r * T) * norm.cdf(cp * d2))
    delta = cp * norm.cdf(cp * d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = (
        -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T))
        - cp * r * K * np.exp(-r * T) * norm.cdf(cp * d2)
    ) / 365
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100
    return price, delta, gamma, theta, vega


def compute_p1(
    K: float = 100.0,
    r: float = 0.05,
    sigma: float = 0.25,
    T0: float = 1.0,
    seed: int = 42,
    n_spot: int = 90,
    n_time: int = 80,
) -> dict[str, Any]:
    np.random.seed(seed)
    entry_price, *_ = bs(K, K, T0, r, sigma)
    spots = np.linspace(70, 135, n_spot)
    times = np.linspace(0.01, T0, n_time)
    S_g, T_g = np.meshgrid(spots, times)
    price_g, _delta_g, gamma_g, theta_g, _vega_g = bs(S_g, K, T_g, r, sigma)
    pnl_g = price_g - entry_price
    
    # Cap gamma for better visualization of the surface
    gamma_capped = np.minimum(gamma_g, np.percentile(gamma_g, 98))
    theta_cents = theta_g * 100.0

    fig = make_subplots(
        rows=1,
        cols=3,
        specs=[[{"type": "surface"}, {"type": "surface"}, {"type": "surface"}]],
        subplot_titles=(
            f"Long Call P&L (K={K:g}, σ={sigma:.0%})",
            "Gamma (Sensitivity)",
            "Theta (Decay ¢/day)",
        ),
        horizontal_spacing=0.06,
    )

    dte = T_g * 365.0
    fig.add_trace(
        go.Surface(
            x=spots,
            y=dte,
            z=pnl_g,
            colorscale="RdYlGn",
            showscale=True,
            colorbar=dict(title="P&L ($)", len=0.4, y=0.5, x=0.31),
            name="P&L",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Surface(
            x=spots,
            y=dte,
            z=gamma_capped,
            colorscale="Viridis",
            showscale=False,
            name="Gamma",
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Surface(
            x=spots,
            y=dte,
            z=theta_cents,
            colorscale="Magenta",
            showscale=False,
            name="Theta",
        ),
        row=1,
        col=3,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a0a0ff", family="Inter, sans-serif", size=11),
        title=dict(
            text="Option Greeks Manifold Analysis",
            x=0.5,
            font=dict(size=18, color="#fff"),
        ),
        margin=dict(l=0, r=10, t=80, b=0),
        height=550,
    )
    for i in range(1, 4):
        fig.update_scenes(
            dict(
                xaxis=dict(gridcolor="#222", showbackground=False),
                yaxis=dict(gridcolor="#222", showbackground=False),
                zaxis=dict(gridcolor="#222", showbackground=False),
                bgcolor="rgba(0,0,0,0)",
            ),
            row=1,
            col=i,
        )
        if i == 1:
            fig.update_scenes(dict(xaxis_title="Spot", yaxis_title="DTE", zaxis_title="P&L"), row=1, col=1)
        elif i == 2:
            fig.update_scenes(dict(xaxis_title="Spot", yaxis_title="DTE", zaxis_title="Γ"), row=1, col=2)
        else:
            fig.update_scenes(dict(xaxis_title="Spot", yaxis_title="DTE", zaxis_title="Θ"), row=1, col=3)

    return _fig_to_json(fig)


def fat_gbm(n_paths, n_days, mu, sigma, df_t=4, shock_prob=0.07, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    dt = 1.0 / 252.0
    norm_ret = rng.normal(
        (mu - 0.5 * sigma**2) * dt,
        sigma * np.sqrt(dt),
        size=(n_paths, n_days),
    )
    t_shocks = rng.standard_t(df_t, size=(n_paths, n_days)) * sigma * np.sqrt(dt) * 1.5
    mask = rng.random((n_paths, n_days)) < shock_prob
    returns = np.where(mask, t_shocks, norm_ret)
    prices = np.cumprod(1 + returns, axis=1)
    return np.hstack([np.ones((n_paths, 1)), prices])


def compute_p2(
    n_paths: int = 3000,
    n_days: int = 252,
    mu_ann: float = 0.12,
    sig_ann: float = 0.22,
    df_t: int = 4,
    shock_prob: float = 0.07,
    seed: int = 7,
    fan_paths: int = 60,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    paths = fat_gbm(n_paths, n_days, mu_ann, sig_ann, df_t=df_t, shock_prob=shock_prob, rng=rng)
    
    # Calculate returns for Sharpe Ratio
    periodic_returns = paths[:, 1:] / paths[:, :-1] - 1
    mean_ret = np.mean(periodic_returns) * 252
    vol_ret = np.std(periodic_returns) * np.sqrt(252)
    sharpe = mean_ret / vol_ret if vol_ret > 0 else 0
    
    running_max = np.maximum.accumulate(paths, axis=1)
    drawdowns = (paths - running_max) / running_max

    days_arr = np.arange(n_days + 1)
    dd_bins = np.linspace(-0.70, 0.0, 100)
    density = np.zeros((len(days_arr), len(dd_bins) - 1))
    for i, _day in enumerate(days_arr):
        dd_today = drawdowns[:, i]
        h, _ = np.histogram(dd_today, bins=dd_bins, density=True)
        density[i] = h
    density = gaussian_filter(density, sigma=[3, 2])
    DD_mid = (dd_bins[:-1] + dd_bins[1:]) / 2
    log_density = np.log1p(density * 20)

    median_dd = np.median(drawdowns, axis=0) * 100
    p5_dd = np.percentile(drawdowns, 5, axis=0) * 100
    
    # Terminal metrics
    terminal_vals = paths[:, -1]
    var_95 = np.percentile(terminal_vals, 5)
    cvar_95 = np.mean(terminal_vals[terminal_vals <= var_95])
    var_95_pct = (var_95 - 1) * 100
    cvar_95_pct = (cvar_95 - 1) * 100

    radar_colors = [
        [0, "rgb(10,10,20)"],
        [0.2, "rgb(20,40,80)"],
        [0.5, "rgb(40,100,200)"],
        [0.8, "rgb(100,200,255)"],
        [1, "rgb(255,255,255)"],
    ]

    fig = make_subplots(
        rows=1,
        cols=3,
        column_widths=[0.5, 0.25, 0.25],
        specs=[[{"type": "surface"}, {"type": "scatter3d"}, {"type": "xy"}]],
        subplot_titles=(
            "Drawdown Density Surface",
            "Path Projections",
            "Terminal Wealth Distribution",
        ),
        horizontal_spacing=0.08,
    )

    fig.add_trace(
        go.Surface(
            x=days_arr,
            y=DD_mid * 100,
            z=log_density,
            colorscale=radar_colors,
            showscale=True,
            colorbar=dict(title="Density", len=0.4, y=0.5, x=0.45),
        ),
        row=1,
        col=1,
    )
    sample_idx = rng.choice(n_paths, size=min(fan_paths, n_paths), replace=False)
    for idx in sample_idx:
        dd_path = drawdowns[idx] * 100
        final_val = paths[idx, -1]
        color_val = float(np.clip((final_val - 0.5) / 2.0, 0, 1))
        # Gradient from Red (Loss) to Green (Profit)
        r = int(255 * (1 - color_val))
        g = int(255 * color_val)
        b = 100
        col = f"rgb({r},{g},{b})"
        fig.add_trace(
            go.Scatter3d(
                x=days_arr,
                y=dd_path,
                z=np.zeros_like(days_arr),
                mode="lines",
                line=dict(color=col, width=1.5),
                opacity=0.3,
                showlegend=False,
            ),
            row=1,
            col=2,
        )

    fig.add_trace(
        go.Scatter3d(
            x=days_arr,
            y=median_dd,
            z=np.zeros_like(days_arr, dtype=float),
            mode="lines",
            line=dict(color="#00ffcc", width=5),
            name="Median DD",
        ),
        row=1,
        col=2,
    )
    
    val_bins = np.linspace(0.1, 4.0, 80)
    val_mid = (val_bins[:-1] + val_bins[1:]) / 2
    hist_vals, _ = np.histogram(terminal_vals, bins=val_bins, density=True)
    hist_smooth = gaussian_filter(hist_vals, sigma=1.5)
    
    fig.add_trace(
        go.Bar(
            x=val_mid,
            y=hist_smooth,
            marker=dict(
                color=val_mid,
                colorscale="Portland",
                showscale=False
            ),
            name="Density",
        ),
        row=1,
        col=3,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#88dd88", family="Inter, sans-serif", size=10),
        title=dict(
            text=f"Risk Analysis: Sharpe={sharpe:.2f} | 95% VaR={var_95_pct:.1f}% | CVaR={cvar_95_pct:.1f}%",
            x=0.5,
            y=0.95,
            font=dict(size=16, color="#fff")
        ),
        height=550,
        margin=dict(t=100, b=40, l=0, r=10),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0.02),
    )
    
    fig.update_scenes(
        dict(
            xaxis=dict(gridcolor="#333", showbackground=False),
            yaxis=dict(gridcolor="#333", showbackground=False),
            zaxis=dict(gridcolor="#333", showbackground=False),
            bgcolor="rgba(0,0,0,0)",
            aspectmode="manual",
            aspectratio=dict(x=1.5, y=1, z=0.5),
        ),
        row=1,
        col=1,
    )
    fig.update_scenes(
        dict(
            xaxis_title="Day",
            yaxis_title="DD %",
            zaxis=dict(showticklabels=False, title=""),
            bgcolor="rgba(0,0,0,0)",
        ),
        row=1,
        col=2,
    )
    fig.update_xaxes(title_text="Portfolio Value", row=1, col=3, gridcolor="#333")
    fig.update_yaxes(title_text="Probability", row=1, col=3, gridcolor="#333")

    return _fig_to_json(fig)


def corr_calm():
    return np.array(
        [
            [1.00, 0.85, -0.30, 0.05, -0.60, 0.70],
            [0.85, 1.00, -0.25, 0.10, -0.55, 0.65],
            [-0.30, -0.25, 1.00, 0.20, 0.40, -0.20],
            [0.05, 0.10, 0.20, 1.00, -0.10, 0.00],
            [-0.60, -0.55, 0.40, -0.10, 1.00, -0.55],
            [0.70, 0.65, -0.20, 0.00, -0.55, 1.00],
        ]
    )


def corr_crisis():
    return np.array(
        [
            [1.00, 0.95, -0.75, 0.35, -0.85, 0.88],
            [0.95, 1.00, -0.72, 0.32, -0.82, 0.85],
            [-0.75, -0.72, 1.00, 0.60, 0.70, -0.68],
            [0.35, 0.32, 0.60, 1.00, -0.25, 0.28],
            [-0.85, -0.82, 0.70, -0.25, 1.00, -0.80],
            [0.88, 0.85, -0.68, 0.28, -0.80, 1.00],
        ]
    )


def compute_p3(
    n_days: int = 504,
    win: int = 30,
    seed: int = 99,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    n_assets = 6
    assets = ["SPY", "QQQ", "TLT", "GLD", "VIX_inv", "HYG"]
    vols_calm = np.array([0.15, 0.18, 0.10, 0.12, 0.60, 0.08])
    vols_crisis = np.array([0.35, 0.40, 0.20, 0.22, 1.20, 0.28])
    trans = np.array([[0.985, 0.015], [0.05, 0.95]])
    regime = 0
    regimes = []
    returns = np.zeros((n_days, n_assets))
    cc, ck = corr_calm(), corr_crisis()
    for t in range(n_days):
        regime = int(rng.choice(2, p=trans[regime]))
        regimes.append(regime)
        vc = vols_calm if regime == 0 else vols_crisis
        cr = cc if regime == 0 else ck
        cov = np.outer(vc, vc) * cr + 1e-7 * np.eye(n_assets)
        try:
            L = np.linalg.cholesky(cov)
            returns[t] = (L @ rng.normal(0, 1, size=n_assets)) / np.sqrt(252)
        except np.linalg.LinAlgError:
            returns[t] = rng.normal(0, vc / np.sqrt(252))
    regimes = np.array(regimes)
    n_roll = n_days - win
    corr_ts = np.zeros((n_roll, n_assets, n_assets))
    for t in range(n_roll):
        corr_ts[t] = np.corrcoef(returns[t : t + win].T)
    pairs = [(i, j) for i in range(n_assets) for j in range(i + 1, n_assets)]
    pair_labels = [f"{assets[i]}×{assets[j]}" for i, j in pairs]
    n_pairs = len(pairs)
    corr_pair_ts = np.array([[corr_ts[t, i, j] for t in range(n_roll)] for i, j in pairs])
    roll_days = np.arange(n_roll)
    regime_roll = regimes[win : win + n_roll]

    Z = np.stack(
        [gaussian_filter(corr_pair_ts[pi].astype(float), sigma=2.5) for pi in range(n_pairs)]
    )
    avg_s = gaussian_filter(corr_pair_ts.mean(axis=0), sigma=3)
    final_corr = corr_ts[-1]

    fig = make_subplots(
        rows=2,
        cols=2,
        row_heights=[0.5, 0.5],
        column_widths=[0.5, 0.5],
        specs=[
            [{"type": "surface"}, {"type": "xy"}],
            [{"type": "xy"}, {"type": "xy"}],
        ],
        subplot_titles=(
            "Rolling Correlation Surface",
            "Average Correlation (Regime Color)",
            "Final Correlation Matrix",
            "Mean Absolute Correlation by Pair",
        ),
        vertical_spacing=0.15,
        horizontal_spacing=0.12,
    )

    fig.add_trace(
        go.Surface(
            x=roll_days,
            y=np.arange(n_pairs),
            z=Z,
            colorscale="RdBu",
            cmin=-1,
            cmax=1,
            colorbar=dict(title="ρ", len=0.35, y=0.8, x=0.46),
            hovertemplate="Day %{x}<br>Pair %{y}<br>ρ %{z:.2f}<extra></extra>",
        ),
        row=1,
        col=1,
    )

    colors = np.where(regime_roll == 1, "#ff3300", "#3366ff")
    fig.add_trace(
        go.Scatter(
            x=roll_days,
            y=avg_s,
            mode="lines+markers",
            marker=dict(size=4, color=colors.tolist()),
            line=dict(color="#888888", width=1),
            name="avg ρ",
        ),
        row=1,
        col=2,
    )

    fig.add_trace(
        go.Heatmap(
            z=final_corr,
            x=assets,
            y=assets,
            colorscale="RdBu",
            zmin=-1,
            zmax=1,
            colorbar=dict(title="ρ", len=0.35, y=0.2, x=0.46),
        ),
        row=2,
        col=1,
    )

    mean_abs = np.mean(np.abs(corr_pair_ts), axis=1)
    fig.add_trace(
        go.Bar(
            x=pair_labels,
            y=mean_abs,
            marker_color="#38bdf8",
            name="mean |ρ|",
        ),
        row=2,
        col=2,
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#aaaaff", family="Inter, sans-serif", size=10),
        height=850,
        margin=dict(t=100, b=100, l=60, r=20),
        title=dict(
            text="Asset Correlation Dynamics (Markov-Switching Simulation)",
            x=0.5,
            font=dict(size=18, color="#fff"),
        ),
        showlegend=False,
    )
    
    fig.update_xaxes(gridcolor="#222", zerolinecolor="#333", row=1, col=2)
    fig.update_yaxes(gridcolor="#222", zerolinecolor="#333", row=1, col=2)
    fig.update_xaxes(gridcolor="#222", zerolinecolor="#333", row=2, col=2)
    fig.update_yaxes(gridcolor="#222", zerolinecolor="#333", row=2, col=2)
    
    fig.update_xaxes(title_text="Trading Day", row=1, col=2)
    fig.update_yaxes(title_text="Avg ρ", row=1, col=2)
    fig.update_xaxes(tickangle=45, row=2, col=2)
    fig.update_yaxes(title_text="|ρ|", row=2, col=2)

    fig.update_scenes(
        dict(
            xaxis_title="Day",
            yaxis_title="Pair Index",
            zaxis_title="ρ",
            xaxis=dict(gridcolor="#333", showbackground=False),
            yaxis=dict(gridcolor="#333", showbackground=False),
            zaxis=dict(gridcolor="#333", showbackground=False),
            bgcolor="rgba(0,0,0,0)",
        ),
        row=1,
        col=1,
    )

    return _fig_to_json(fig)
