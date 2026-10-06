import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =========================
# CONFIGURATION
# =========================

st.set_page_config(
    page_title="AeroFlow Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Seuils (modifiables)
TARGET_PRODUCTION = 100   # % objectif de production
ALERT_PRODUCTION = 92     # % en dessous = alerte
TARGET_QUALITY = 98       # % objectif qualité

# Palette
BLUE = "#3B82F6"
CYAN = "#06B6D4"
GREEN = "#22C55E"
ORANGE = "#F59E0B"
RED = "#EF4444"
GREY = "#94A3B8"

# =========================
# STYLE (CSS)
# =========================

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1400px;}

    /* Bandeau d'en-tête */
    .hero {
        background: linear-gradient(120deg, #0F172A 0%, #1E3A8A 55%, #3B82F6 100%);
        padding: 1.8rem 2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(30, 58, 138, 0.25);
    }
    .hero h1 {margin: 0; font-size: 2.2rem; font-weight: 800; letter-spacing: -0.5px; color: white;}
    .hero p {margin: .35rem 0 0 0; opacity: .85; font-size: 1rem;}

    /* Cartes KPI */
    [data-testid="stMetric"] {
        background: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-left: 5px solid #3B82F6;
        padding: 1rem 1.2rem;
        border-radius: 14px;
        transition: transform .15s ease, box-shadow .15s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
    }
    [data-testid="stMetricLabel"] {font-weight: 600; opacity: .8;}
    [data-testid="stMetricValue"] {font-weight: 800; font-size: 2rem;}

    /* Titres de section */
    h2, h3 {font-weight: 700 !important; letter-spacing: -0.3px;}

    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {gap: 6px;}
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        font-weight: 600;
    }

    /* Graphiques dans des cartes */
    [data-testid="stPlotlyChart"] {
        background: rgba(148, 163, 184, 0.05);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 14px;
        padding: .5rem;
    }

    /* Masquer le footer Streamlit */
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


def show(fig):
    """Affiche un graphique Plotly en pleine largeur (compatible anciennes/nouvelles versions)."""
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def style_fig(fig, height=380):
    """Style commun à tous les graphiques."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=13),
        title=dict(font=dict(size=17), x=0.01),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None),
        hoverlabel=dict(font_size=13),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.25)")
    return fig


# =========================
# LOAD DATA
# =========================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def load_data():
    production = pd.read_csv(DATA_DIR / "production.csv", parse_dates=["date"])
    quality = pd.read_csv(DATA_DIR / "quality.csv", parse_dates=["date"])
    planning = pd.read_csv(DATA_DIR / "planning.csv", parse_dates=["date"])

    df = production.merge(quality, on=["date", "line", "product"], how="left")
    df = df.merge(planning, on=["date", "line", "product"], how="left")

    # KPI
    df["production_rate"] = df["units_produced"] / df["target_units"] * 100
    df["defect_rate"] = df["defective_units"] / df["units_inspected"] * 100
    df["schedule_rate"] = df["actual_units"] / df["planned_units"] * 100
    return df


df = load_data()

# =========================
# HEADER
# =========================

st.markdown(
    """
    <div class="hero">
        <h1>✈️ AeroFlow</h1>
        <p>Manufacturing Performance &amp; Data Analytics — production, qualité, temps de cycle et retards</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.markdown("## 🎛️ Filtres")

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "📅 Période",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

selected_lines = st.sidebar.multiselect(
    "🏭 Ligne de production",
    options=sorted(df["line"].unique()),
    default=sorted(df["line"].unique()),
)

selected_products = st.sidebar.multiselect(
    "📦 Produit",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique()),
)

st.sidebar.divider()
st.sidebar.caption("Les KPI et graphiques se mettent à jour automatiquement.")

# =========================
# FILTER DATA
# =========================

filtered_df = df[
    df["line"].isin(selected_lines) & df["product"].isin(selected_products)
]

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["date"].dt.date >= start_date)
        & (filtered_df["date"].dt.date <= end_date)
    ]

if filtered_df.empty:
    st.warning("Aucune donnée pour les filtres sélectionnés.")
    st.stop()

# =========================
# KPI VALUES
# =========================

production_rate = filtered_df["production_rate"].mean()
quality_rate = 100 - filtered_df["defect_rate"].mean()
cycle_time = filtered_df["cycle_time_min"].mean()
total_delays = filtered_df["delay_hours"].sum()

# =========================
# KPI CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🎯 Production Achievement",
    f"{production_rate:.1f}%",
    delta=f"{production_rate - TARGET_PRODUCTION:+.1f} pts vs objectif",
)
col2.metric(
    "✅ Quality Rate",
    f"{quality_rate:.2f}%",
    delta=f"{quality_rate - TARGET_QUALITY:+.2f} pts vs objectif",
)
col3.metric(
    "⏱️ Average Cycle Time",
    f"{cycle_time:.1f} min",
)
col4.metric(
    "⚠️ Total Delays",
    f"{total_delays:.0f} h",
    delta=None,
)

st.write("")

# =========================
# ALERT
# =========================

line_performance = (
    filtered_df.groupby("line")["production_rate"].mean().sort_values()
)

worst_line = line_performance.index[0]
worst_performance = line_performance.iloc[0]

if worst_performance < ALERT_PRODUCTION:
    st.warning(
        f"**Attention requise** : la ligne **{worst_line}** "
        f"n'atteint que **{worst_performance:.1f}%** de son objectif de production.",
        icon="⚠️",
    )
else:
    st.success("Aucun problème critique de performance de production détecté.", icon="✅")

# =========================
# TABS
# =========================

tab_prod, tab_ops, tab_data = st.tabs(
    ["📈 Production", "🛠️ Qualité & Opérations", "🗂️ Données"]
)

# ---------- TAB PRODUCTION ----------
with tab_prod:
    daily_production = (
        filtered_df.groupby("date")[["units_produced", "target_units"]]
        .sum()
        .reset_index()
    )

    fig_production = go.Figure()
    fig_production.add_trace(
        go.Scatter(
            x=daily_production["date"],
            y=daily_production["units_produced"],
            name="Produit",
            mode="lines+markers",
            line=dict(color=BLUE, width=3, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(59,130,246,0.12)",
        )
    )
    fig_production.add_trace(
        go.Scatter(
            x=daily_production["date"],
            y=daily_production["target_units"],
            name="Objectif",
            mode="lines",
            line=dict(color=ORANGE, width=2, dash="dash"),
        )
    )
    fig_production.update_layout(
        title="Production journalière vs objectif",
        xaxis_title=None,
        yaxis_title="Unités",
        hovermode="x unified",
    )
    show(style_fig(fig_production, height=420))

    c1, c2 = st.columns(2)

    with c1:
        line_perf = (
            filtered_df.groupby("line")["production_rate"].mean().reset_index()
        )
        line_perf["status"] = line_perf["production_rate"].apply(
            lambda v: "Critique" if v < ALERT_PRODUCTION
            else ("À surveiller" if v < TARGET_PRODUCTION else "OK")
        )

        fig_line = px.bar(
            line_perf,
            x="line",
            y="production_rate",
            color="status",
            color_discrete_map={"OK": GREEN, "À surveiller": ORANGE, "Critique": RED},
            text=line_perf["production_rate"].round(1).astype(str) + "%",
            title="Réalisation de la production par ligne",
            labels={"production_rate": "Réalisation (%)", "line": "Ligne"},
        )
        fig_line.add_hline(
            y=TARGET_PRODUCTION,
            line_dash="dash",
            line_color=GREY,
            annotation_text="Objectif",
        )
        fig_line.update_traces(textposition="outside", marker_cornerradius=6)
        show(style_fig(fig_line))

    with c2:
        product_perf = (
            filtered_df.groupby("product")["production_rate"].mean().reset_index()
        )
        fig_product = px.bar(
            product_perf.sort_values("production_rate"),
            x="production_rate",
            y="product",
            orientation="h",
            text=product_perf.sort_values("production_rate")["production_rate"].round(1).astype(str) + "%",
            title="Réalisation de la production par produit",
            labels={"production_rate": "Réalisation (%)", "product": "Produit"},
            color_discrete_sequence=[CYAN],
        )
        fig_product.update_traces(textposition="outside", marker_cornerradius=6)
        show(style_fig(fig_product))

# ---------- TAB OPERATIONS ----------
with tab_ops:
    c1, c2 = st.columns(2)

    with c1:
        quality_line = (
            filtered_df.groupby("line")["defect_rate"].mean().reset_index()
        )
        fig_quality = px.bar(
            quality_line,
            x="line",
            y="defect_rate",
            text=quality_line["defect_rate"].round(2).astype(str) + "%",
            title="Taux de défauts par ligne",
            labels={"defect_rate": "Taux de défauts (%)", "line": "Ligne"},
            color="defect_rate",
            color_continuous_scale=["#22C55E", "#F59E0B", "#EF4444"],
        )
        fig_quality.update_traces(textposition="outside", marker_cornerradius=6)
        fig_quality.update_coloraxes(showscale=False)
        show(style_fig(fig_quality))

    with c2:
        delay_line = (
            filtered_df.groupby("line")["delay_hours"].sum().reset_index()
        )
        fig_delay = px.bar(
            delay_line,
            x="line",
            y="delay_hours",
            text=delay_line["delay_hours"].round(0).astype(int).astype(str) + " h",
            title="Retards cumulés par ligne",
            labels={"delay_hours": "Retard (heures)", "line": "Ligne"},
            color_discrete_sequence=[RED],
        )
        fig_delay.update_traces(textposition="outside", marker_cornerradius=6)
        show(style_fig(fig_delay))

    c3, c4 = st.columns(2)

    with c3:
        cycle_line = (
            filtered_df.groupby("line")["cycle_time_min"].mean().reset_index()
        )
        fig_cycle = px.bar(
            cycle_line,
            x="line",
            y="cycle_time_min",
            text=cycle_line["cycle_time_min"].round(1).astype(str) + " min",
            title="Temps de cycle moyen par ligne",
            labels={"cycle_time_min": "Temps de cycle (min)", "line": "Ligne"},
            color_discrete_sequence=[BLUE],
        )
        fig_cycle.update_traces(textposition="outside", marker_cornerradius=6)
        show(style_fig(fig_cycle))

    with c4:
        daily_delay = (
            filtered_df.groupby("date")["delay_hours"].sum().reset_index()
        )
        fig_trend = px.area(
            daily_delay,
            x="date",
            y="delay_hours",
            title="Évolution des retards dans le temps",
            labels={"delay_hours": "Retard (heures)", "date": ""},
            color_discrete_sequence=[ORANGE],
        )
        fig_trend.update_traces(line_shape="spline")
        show(style_fig(fig_trend))

# ---------- TAB DATA ----------
with tab_data:
    display_df = filtered_df[
        [
            "date",
            "line",
            "product",
            "units_produced",
            "target_units",
            "production_rate",
            "defect_rate",
            "cycle_time_min",
            "delay_hours",
        ]
    ].copy()

    display_df["date"] = display_df["date"].dt.date

    st.dataframe(
        display_df,
        hide_index=True,
        column_config={
            "date": st.column_config.DateColumn("Date", format="DD/MM/YYYY"),
            "line": "Ligne",
            "product": "Produit",
            "units_produced": st.column_config.NumberColumn("Produit", format="%d"),
            "target_units": st.column_config.NumberColumn("Objectif", format="%d"),
            "production_rate": st.column_config.ProgressColumn(
                "Réalisation",
                format="%.1f%%",
                min_value=0,
                max_value=120,
            ),
            "defect_rate": st.column_config.NumberColumn("Défauts", format="%.2f%%"),
            "cycle_time_min": st.column_config.NumberColumn("Cycle (min)", format="%.1f"),
            "delay_hours": st.column_config.NumberColumn("Retard (h)", format="%.1f"),
        },
        height=520,
    )

    st.download_button(
        "⬇️ Télécharger les données filtrées (CSV)",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name="aeroflow_data.csv",
        mime="text/csv",
    )