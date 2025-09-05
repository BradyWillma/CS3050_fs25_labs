# Browser-based, viewport-stable substitution-method demo (Dash + Plotly)
# pip install dash plotly numpy

"""_summary_
	•	T(n) actual (solid line) = the exact value of the recurrence you picked, computed recursively with our chosen base case (e.g., T(1)=1) and halving rule (n//2). It’s a mathematical simulation of the recurrence, not wall-clock timing of code.
	•	c·g(n) (dashed line) = the candidate upper bound you’d try to prove by substitution (e.g., g(n)=n\log n,\; n^2,\; n(\log n)^2), scaled by the slider c.

So you’re comparing the recurrence’s exact values vs a theoretical bound you’re testing. Red markers simply show n where, with your current c, the inequality T(n) \le c\cdot g(n) doesn’t hold for the plotted n. (That doesn’t refute big-O; it may just mean you need a larger c or larger n before it kicks in.)

The “Work by level” tab is also analytic: it plots the recursion-tree outside work per level implied by the recurrence (using the a,b,f(n) you selected), not timings.

"""

import math
from functools import lru_cache
import numpy as np
from typing import List, Tuple

import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# ----------------------------
# Recurrences & helper math
# ----------------------------

@lru_cache(None)
def T_2Tn2_plus_n(n: int) -> float:
    if n <= 1:
        return 1.0
    return 2.0 * T_2Tn2_plus_n(n // 2) + float(n)

@lru_cache(None)
def T_Tn2_plus_n2(n: int) -> float:
    if n <= 1:
        return 1.0
    return T_Tn2_plus_n2(n // 2) + float(n) * float(n)

@lru_cache(None)
def T_2Tn2_plus_nlogn(n: int) -> float:
    if n <= 1:
        return 1.0
    return 2.0 * T_2Tn2_plus_nlogn(n // 2) + float(n) * math.log2(max(n, 2))

# Closed form to avoid deep recursion
def T_linear(n: int) -> float:
    return float(max(n, 1))

def g_nlogn(n: int) -> float:
    if n <= 1:
        return 1.0
    return float(n) * math.log2(n)

def g_n2(n: int) -> float:
    return float(n) * float(n)

def g_nlog2(n: int) -> float:
    if n <= 1:
        return 1.0
    ln = math.log2(n)
    return float(n) * (ln * ln)

def g_n(n: int) -> float:
    return float(n)

def powers_of_two_up_to(exp_k: int) -> List[int]:
    return [2 ** i for i in range(1, exp_k + 1)]

# Registry (plain Unicode; no TeX macros)
RECURRENCES = {
    "2T(n/2) + n   (guess: n log n)": {
        "T": T_2Tn2_plus_n, "g": g_nlogn,
        "suggested_c": 2.0, "dc": True,
        "proof": [
            "Example: T(n) = 2T(n/2) + n",
            "Guess: T(n) ≤ c·n·log₂ n",
            "Substitute: 2·c·(n/2)·log₂(n/2) + n",
            "= c·n·(log₂ n − 1) + n = c·n·log₂ n − (c−1)·n",
            "Holds if c ≥ 1."
        ],
        "f_local": lambda n: float(n), "a": 2, "b": 2
    },
    "T(n/2) + n^2  (guess: n^2)": {
        "T": T_Tn2_plus_n2, "g": g_n2,
        "suggested_c": 1.5, "dc": True,
        "proof": [
            "Example: T(n) = T(n/2) + n²",
            "Guess: T(n) ≤ c·n²",
            "Substitute: c·(n/2)² + n² = (c/4)·n² + n²",
            "≤ c·n² when c ≥ 4/3."
        ],
        "f_local": lambda n: float(n) * float(n), "a": 1, "b": 2
    },
    "2T(n/2) + n log n  (guess: n log^2 n)": {
        "T": T_2Tn2_plus_nlogn, "g": g_nlog2,
        "suggested_c": 1.0, "dc": True,
        "proof": [
            "Example: T(n) = 2T(n/2) + n·log₂ n",
            "Guess with n·log₂ n fails; try T(n) ≤ c·n·(log₂ n)².",
            "Substitution validates for suitable c."
        ],
        "f_local": lambda n: float(n) * math.log2(max(n, 2)), "a": 2, "b": 2
    },
    "T(n-1) + 1   (guess: n)": {
        "T": T_linear, "g": g_n,
        "suggested_c": 1.0, "dc": False,
        "proof": [
            "Example: T(n) = T(n−1) + 1",
            "Guess: T(n) ≤ c·n",
            "Substitute: c·(n−1) + 1 = c·n − (c−1)",
            "≤ c·n when c ≥ 1."
        ]
    }
}

def make_domain(key: str, k: int) -> np.ndarray:
    dc = RECURRENCES[key]["dc"]
    return np.array(powers_of_two_up_to(k) if dc else list(range(1, 2 ** k + 1)), dtype=int)

def series(key: str, k: int, c: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    xs = make_domain(key, k)
    Tfun = RECURRENCES[key]["T"]; gfun = RECURRENCES[key]["g"]
    T_vals = np.array([Tfun(int(n)) for n in xs], dtype=float)
    B_vals = c * np.array([gfun(int(n)) for n in xs], dtype=float)
    return xs, T_vals, B_vals

def work_by_level(key: str, k: int) -> tuple[np.ndarray, np.ndarray, str]:
    info = RECURRENCES[key]
    if not info.get("dc", False):
        n = 2 ** k
        xs = np.arange(n)
        return xs, np.ones_like(xs, dtype=float), "Linear steps: uniform work"
    n = 2 ** k
    a, b = info["a"], info["b"]
    f_local = info["f_local"]
    vals = []
    size = float(n); i = 0
    while size >= 1.0:
        nodes = a ** i
        vals.append(nodes * f_local(max(int(size), 1)))
        i += 1
        size = size / b
    xs = np.arange(len(vals))
    if a == 2 and b == 2 and info["f_local"] == RECURRENCES["2T(n/2) + n   (guess: n log n)"]["f_local"]:
        msg = "Balanced across levels (Case 2 style)"
    elif a == 1 and b == 2:
        msg = "Top-heavy (root dominates)"
    else:
        msg = "Slightly top-skewed (extra log factor)"
    return xs, np.array(vals, dtype=float), msg

# ----------------------------
# Dash App (viewport-stable layout)
# ----------------------------

app = Dash(__name__)
app.title = "Substitution Method — Interactive Demo"

opts = [{"label": k, "value": k} for k in RECURRENCES.keys()]

app.layout = html.Div(
    # Full-viewport grid: header row + content row
    style={
        "height": "100vh", "display": "grid",
        "gridTemplateRows": "56px 1fr", "rowGap": "8px",
        "fontFamily": "Inter, system-ui, sans-serif"
    },
    children=[
        html.Div(
            html.H3("Substitution Method — Interactive Demo", style={"margin": 0, "textAlign": "center"}),
            style={"display": "flex", "alignItems": "center", "justifyContent": "center"}
        ),

        # Content row: left controls (fixed width, scrollable) + right graph area (fills)
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "320px 1fr",
                "columnGap": "14px",
                "height": "100%", "minHeight": 0  # allow children to size within viewport
            },
            children=[
                # LEFT PANEL (scrolls inside)
                html.Div(
                    style={
                        "border": "1px solid #e5e7eb", "borderRadius": "10px",
                        "padding": "12px", "overflowY": "auto", "minHeight": 0
                    },
                    children=[
                        html.Label("Recurrence", style={"fontWeight": 600}),
                        dcc.Dropdown(id="recurrence", options=opts, value=opts[0]["value"], clearable=False),

                        html.Div(style={"height": "12px"}),

                        html.Label("Max n (2^k)", style={"fontWeight": 600}),
                        dcc.Slider(id="k", min=3, max=12, step=1, value=8,
                                   marks={i: f"{i}" for i in range(3, 13)}),

                        html.Div(style={"height": "10px"}),

                        html.Label("c (for bound: c·g(n))", style={"fontWeight": 600}),
                        dcc.Slider(
                            id="c", min=0.25, max=6.0, step=0.05,
                            value=RECURRENCES[opts[0]["value"]]["suggested_c"],
                            tooltip={"placement": "bottom", "always_visible": False},
                        ),

                        html.Div(id="status", style={"marginTop": "10px", "fontStyle": "italic", "fontSize": "14px"}),

                        html.Div(style={"height": "12px"}),

                        html.Label("Proof sketch", style={"fontWeight": 600}),
                        dcc.Markdown(id="proof", style={
                            "whiteSpace": "pre-wrap", "border": "1px solid #eee",
                            "borderRadius": "8px", "padding": "8px", "background": "#fafafa"
                        }),
                    ],
                ),

                # RIGHT PANEL (fixed to viewport, tabbed single graph)
                html.Div(
                    style={
                        "border": "1px solid #e5e7eb", "borderRadius": "10px",
                        "padding": "8px", "display": "grid",
                        "gridTemplateRows": "40px 1fr", "rowGap": "6px",
                        "height": "100%", "minHeight": 0
                    },
                    children=[
                        dcc.Tabs(
                            id="view", value="main",
                            style={"height": "40px"},
                            children=[
                                dcc.Tab(label="T(n) vs bound", value="main"),
                                dcc.Tab(label="Work by level", value="work"),
                            ],
                        ),
                        # This container is locked to remaining viewport space
                        html.Div(
                            style={"height": "100%", "minHeight": 0},  # important: allows inner graph to fit
                            children=[
                                dcc.Graph(
                                    id="graph",
                                    style={"height": "100%"},
                                    config={"displaylogo": False}
                                )
                            ]
                        )
                    ],
                ),
            ],
        ),
    ],
)

@app.callback(
    Output("graph", "figure"),
    Output("status", "children"),
    Output("proof", "children"),
    Input("recurrence", "value"),
    Input("k", "value"),
    Input("c", "value"),
    Input("view", "value"),
)
def update_all(key: str, k: int, c: float, view: str):
    # Proof text (left panel)
    proof_text = "\n".join(RECURRENCES[key]["proof"])

    if view == "work":
        # Work-by-level figure (fills container height; no page growth)
        wx, wvals, msg = work_by_level(key, k)
        fig = go.Figure(go.Bar(x=wx, y=wvals, name="Work per level"))
        fig.update_layout(
            title=f"Work by Level — {msg}",
            margin=dict(l=40, r=10, t=40, b=40),
            legend=dict(orientation="h", y=1.02, x=0),
        )
        status = "Work distribution across recursion levels."
        return fig, status, proof_text

    # Main plot
    xs, T_vals, B_vals = series(key, k, float(c))
    ok = T_vals <= B_vals
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=T_vals, mode="lines", name="T(n) actual"))
    fig.add_trace(go.Scatter(x=xs, y=B_vals, mode="lines", line=dict(dash="dash"), name="c·g(n)"))
    if np.any(~ok):
        fig.add_trace(go.Scatter(
            x=xs[~ok], y=T_vals[~ok], mode="markers",
            marker=dict(size=7), name="fails bound (T > c·g)"
        ))
    fig.update_layout(
        margin=dict(l=40, r=10, t=40, b=40),
        legend=dict(orientation="h", y=1.02, x=0),
        xaxis_title="n",
        yaxis_title="Work / Bound",
    )
    status = "✓ Bound holds for all shown n." if np.all(ok) \
        else f"✗ Bound fails for some n (first n={int(xs[np.argmax(~ok)])}). Try increasing c."
    return fig, status, proof_text

if __name__ == "__main__":
    # Dash >=2.16 uses app.run; older versions still accept run_server.
    if hasattr(app, "run"):
        app.run(debug=False, host="127.0.0.1", port=8050)
    else:
        app.run_server(debug=False, host="127.0.0.1", port=8050)