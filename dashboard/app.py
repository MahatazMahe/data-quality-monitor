import io
import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "quality.db"
CUSTOMER_DATA_PATH = BASE_DIR / "data" / "raw" / "customers.csv"


st.set_page_config(
    page_title="Data Quality Monitor",
    page_icon="DQ",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Theme: dark mode + purple accent palette
# ---------------------------------------------------------------------------
BG_DEEP = "#0e0b1a"        # app background
BG_PANEL = "#171225"       # cards / sidebar background
BG_PANEL_ALT = "#1e1832"   # slightly lighter panel (hover / inputs)
BORDER = "#332a52"         # subtle borders
TEXT_PRIMARY = "#f1eefb"   # near-white with a violet tint
TEXT_MUTED = "#a79fc4"     # muted lavender-grey

ACCENT = "#a78bfa"         # primary purple (violet-400)
ACCENT_STRONG = "#7c3aed"  # deeper purple (violet-600)
ACCENT_SOFT = "#c4b5fd"    # light purple (violet-300)
ACCENT_GLOW = "#8b5cf6"    # violet-500

STATUS_GOOD_BG = "#15241f"
STATUS_GOOD_FG = "#4ade80"
STATUS_GOOD_BORDER = "#1f4d3a"

STATUS_WARN_BG = "#2a2016"
STATUS_WARN_FG = "#fbbf24"
STATUS_WARN_BORDER = "#5a4420"

STATUS_CRIT_BG = "#2a1620"
STATUS_CRIT_FG = "#fb7185"
STATUS_CRIT_BORDER = "#5a2035"

# Purple sequence for charts (dark-friendly, light-to-deep violet)
PURPLE_SEQUENCE = [
    "#c4b5fd",
    "#a78bfa",
    "#8b5cf6",
    "#7c3aed",
    "#6d28d9",
    "#5b21b6",
]

PLOTLY_TEMPLATE = "plotly_dark"


st.markdown(
    f"""
    <style>

    /* ---------- App-wide dark background ---------- */
    .stApp {{
        background-color: {BG_DEEP};
        color: {TEXT_PRIMARY};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {BG_PANEL};
        border-right: 1px solid {BORDER};
    }}

    section[data-testid="stSidebar"] * {{
        color: {TEXT_PRIMARY};
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }}

    .main-title {{
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, {ACCENT_SOFT}, {ACCENT_GLOW});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }}

    .subtitle {{
        color: {TEXT_MUTED};
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }}

    .section-title {{
        font-size: 1.15rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
        color: {TEXT_PRIMARY};
        border-left: 3px solid {ACCENT};
        padding-left: 0.6rem;
    }}

    .status-good {{
        background: {STATUS_GOOD_BG};
        color: {STATUS_GOOD_FG};
        border: 1px solid {STATUS_GOOD_BORDER};
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}

    .status-warning {{
        background: {STATUS_WARN_BG};
        color: {STATUS_WARN_FG};
        border: 1px solid {STATUS_WARN_BORDER};
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}

    .status-critical {{
        background: {STATUS_CRIT_BG};
        color: {STATUS_CRIT_FG};
        border: 1px solid {STATUS_CRIT_BORDER};
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    }}

    /* ---------- Metric cards ---------- */
    [data-testid="stMetric"] {{
        background: {BG_PANEL};
        border: 1px solid {BORDER};
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 0 0 1px rgba(167, 139, 250, 0.05);
        transition: border-color 0.15s ease;
    }}

    [data-testid="stMetric"]:hover {{
        border-color: {ACCENT};
    }}

    [data-testid="stMetricValue"] {{
        font-size: 1.8rem;
        color: {TEXT_PRIMARY};
    }}

    [data-testid="stMetricLabel"] {{
        color: {TEXT_MUTED};
    }}

    [data-testid="stMetricDelta"] svg {{
        color: {ACCENT_SOFT};
    }}

    /* ---------- Misc widgets ---------- */
    div[data-baseweb="select"] > div {{
        background-color: {BG_PANEL_ALT};
        border-color: {BORDER};
        color: {TEXT_PRIMARY};
    }}

    .stTextInput input {{
        background-color: {BG_PANEL_ALT};
        color: {TEXT_PRIMARY};
        border-color: {BORDER};
    }}

    .stDataFrame {{
        border: 1px solid {BORDER};
        border-radius: 8px;
        overflow: hidden;
    }}

    .stDownloadButton button, .stButton button {{
        background-color: {ACCENT_STRONG};
        color: #ffffff;
        border: 1px solid {ACCENT};
        border-radius: 8px;
    }}

    .stDownloadButton button:hover, .stButton button:hover {{
        background-color: {ACCENT_GLOW};
        border-color: {ACCENT_SOFT};
        color: #ffffff;
    }}

    hr {{
        border-color: {BORDER};
    }}

    .streamlit-expanderHeader {{
        background-color: {BG_PANEL};
        border: 1px solid {BORDER};
        border-radius: 8px;
        color: {TEXT_PRIMARY};
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


@st.cache_data(ttl=30)
def load_run_history():
    connection = get_connection()

    query = """
        SELECT
            run_id,
            dataset_id,
            run_timestamp,
            overall_score
        FROM quality_runs
        ORDER BY run_id
    """

    result = pd.read_sql_query(query, connection)

    connection.close()

    return result


@st.cache_data(ttl=30)
def load_metrics(run_id):
    connection = get_connection()

    query = """
        SELECT
            metric_name,
            metric_value
        FROM quality_metrics
        WHERE run_id = ?
        ORDER BY metric_id
    """

    result = pd.read_sql_query(
        query,
        connection,
        params=(run_id,),
    )

    connection.close()

    return result


@st.cache_data(ttl=30)
def load_issues(run_id):
    connection = get_connection()

    query = """
        SELECT
            column_name,
            issue_type,
            issue_count,
            severity
        FROM quality_issues
        WHERE run_id = ?
        ORDER BY issue_count DESC
    """

    result = pd.read_sql_query(
        query,
        connection,
        params=(run_id,),
    )

    connection.close()

    return result


@st.cache_data(ttl=30)
def load_dataset_info(dataset_id):
    connection = get_connection()

    query = """
        SELECT
            dataset_name,
            file_name,
            row_count,
            column_count
        FROM datasets
        WHERE dataset_id = ?
    """

    result = pd.read_sql_query(
        query,
        connection,
        params=(dataset_id,),
    )

    connection.close()

    return result


@st.cache_data(ttl=30)
def load_customer_data():
    if not CUSTOMER_DATA_PATH.exists():
        return pd.DataFrame()

    return pd.read_csv(CUSTOMER_DATA_PATH)


def score_status(score):
    if score >= 98:
        return "Healthy"
    elif score >= 95:
        return "Warning"
    return "Critical"


def status_html(score):
    status = score_status(score)

    if status == "Healthy":
        return '<span class="status-good">● Healthy</span>'

    if status == "Warning":
        return '<span class="status-warning">● Warning</span>'

    return '<span class="status-critical">● Critical</span>'


run_history = load_run_history()

if run_history.empty:
    st.error(
        "No quality runs found. Run pipeline.py before starting the dashboard."
    )
    st.stop()


latest_run_id = int(run_history.iloc[-1]["run_id"])

st.sidebar.title("Data Quality Monitor")
st.sidebar.caption("Customer data pipeline")

selected_run = st.sidebar.selectbox(
    "Quality Run",
    run_history["run_id"].tolist(),
    index=len(run_history) - 1,
)


selected_run = int(selected_run)

selected_row = run_history[
    run_history["run_id"] == selected_run
].iloc[0]

dataset_id = int(selected_row["dataset_id"])

overall_score = float(selected_row["overall_score"])
run_timestamp = selected_row["run_timestamp"]


metrics = load_metrics(selected_run)
issues = load_issues(selected_run)
dataset_info = load_dataset_info(dataset_id)
customer_data = load_customer_data()


metric_values = dict(
    zip(
        metrics["metric_name"],
        metrics["metric_value"],
    )
)


st.sidebar.divider()

st.sidebar.markdown("### Run Information")

st.sidebar.write(
    f"**Run ID:** {selected_run}"
)

st.sidebar.write(
    f"**Executed:** {run_timestamp}"
)

st.sidebar.write(
    f"**Status:** {score_status(overall_score)}"
)


st.markdown(
    '<div class="main-title">Data Quality Monitor</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Customer data quality monitoring and validation"
    "</div>",
    unsafe_allow_html=True,
)


header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown(
        f"### Quality Run #{selected_run}"
    )

with header_right:
    st.markdown(
        status_html(overall_score),
        unsafe_allow_html=True,
    )


if not dataset_info.empty:
    dataset = dataset_info.iloc[0]

    st.caption(
        f"{dataset['dataset_name']}  •  "
        f"{int(dataset['row_count']):,} records  •  "
        f"{int(dataset['column_count'])} columns"
    )


st.divider()


previous_runs = run_history[
    run_history["run_id"] < selected_run
]

previous_score = None

if not previous_runs.empty:
    previous_score = float(
        previous_runs.iloc[-1]["overall_score"]
    )


delta = None

if previous_score is not None:
    delta = overall_score - previous_score


k1, k2, k3, k4, k5 = st.columns(5)


with k1:
    st.metric(
        "Overall Quality",
        f"{overall_score:.2f}%",
        delta=(
            f"{delta:+.2f}%"
            if delta is not None
            else None
        ),
    )


with k2:
    st.metric(
        "Completeness",
        f"{metric_values.get('Completeness', 0):.2f}%",
    )


with k3:
    st.metric(
        "Validity",
        f"{metric_values.get('Validity', 0):.2f}%",
    )


with k4:
    st.metric(
        "Uniqueness",
        f"{metric_values.get('Uniqueness', 0):.2f}%",
    )


with k5:
    st.metric(
        "Consistency",
        f"{metric_values.get('Consistency', 0):.2f}%",
    )


st.markdown(
    '<div class="section-title">Quality Trend</div>',
    unsafe_allow_html=True,
)


trend_fig = go.Figure()

trend_fig.add_trace(
    go.Scatter(
        x=run_history["run_id"],
        y=run_history["overall_score"],
        mode="lines+markers",
        name="Overall Quality",
        line=dict(color=ACCENT_SOFT, width=3),
        marker=dict(
            color=ACCENT_GLOW,
            size=8,
            line=dict(color=ACCENT_SOFT, width=1),
        ),
        fill="tozeroy",
        fillcolor="rgba(139, 92, 246, 0.12)",
        hovertemplate=(
            "Run %{x}<br>"
            "Quality: %{y:.2f}%"
            "<extra></extra>"
        ),
    )
)

trend_fig.add_hline(
    y=95,
    line_dash="dash",
    line_color="#fbbf24",
    annotation_text="95% threshold",
    annotation_font_color="#fbbf24",
)

trend_fig.update_layout(
    template=PLOTLY_TEMPLATE,
    paper_bgcolor=BG_PANEL,
    plot_bgcolor=BG_PANEL,
    font=dict(color=TEXT_PRIMARY),
    height=360,
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20,
    ),
    xaxis_title="Pipeline Run",
    yaxis_title="Quality Score (%)",
    yaxis=dict(
        range=[
            max(
                90,
                run_history["overall_score"].min() - 2,
            ),
            100,
        ],
        gridcolor=BORDER,
    ),
    xaxis=dict(gridcolor=BORDER),
    hovermode="x unified",
)

st.plotly_chart(
    trend_fig,
    use_container_width=True,
)


left, right = st.columns(2)


with left:

    st.markdown(
        '<div class="section-title">Quality Dimensions</div>',
        unsafe_allow_html=True,
    )

    chart_data = pd.DataFrame(
        {
            "Metric": list(metric_values.keys()),
            "Score": list(metric_values.values()),
        }
    )

    dimension_fig = px.bar(
        chart_data,
        x="Metric",
        y="Score",
        text="Score",
        range_y=[90, 100],
        color="Metric",
        color_discrete_sequence=PURPLE_SEQUENCE,
    )

    dimension_fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )

    dimension_fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=BG_PANEL,
        plot_bgcolor=BG_PANEL,
        font=dict(color=TEXT_PRIMARY),
        height=380,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        xaxis_title="",
        yaxis_title="Score (%)",
        showlegend=False,
        yaxis=dict(gridcolor=BORDER),
        xaxis=dict(gridcolor=BORDER),
    )

    st.plotly_chart(
        dimension_fig,
        use_container_width=True,
    )


with right:

    st.markdown(
        '<div class="section-title">Issues by Severity</div>',
        unsafe_allow_html=True,
    )

    severity_data = (
        issues
        .groupby("severity", as_index=False)["issue_count"]
        .sum()
        .sort_values("issue_count", ascending=False)
    )

    severity_fig = px.pie(
        severity_data,
        names="severity",
        values="issue_count",
        hole=0.58,
        color_discrete_sequence=PURPLE_SEQUENCE,
    )

    severity_fig.update_traces(
        marker=dict(line=dict(color=BG_PANEL, width=2))
    )

    severity_fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor=BG_PANEL,
        plot_bgcolor=BG_PANEL,
        font=dict(color=TEXT_PRIMARY),
        height=380,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        showlegend=True,
    )

    st.plotly_chart(
        severity_fig,
        use_container_width=True,
    )


st.divider()


st.markdown(
    '<div class="section-title">Column Quality</div>',
    unsafe_allow_html=True,
)


if not customer_data.empty:

    completeness = (
        customer_data.notna().mean() * 100
    )

    column_quality = pd.DataFrame(
        {
            "Column": completeness.index,
            "Completeness": completeness.values,
        }
    )

    column_quality["Status"] = column_quality[
        "Completeness"
    ].apply(
        lambda x: (
            "Healthy"
            if x >= 99
            else "Warning"
            if x >= 95
            else "Critical"
        )
    )

    column_quality["Completeness"] = (
        column_quality["Completeness"]
        .round(2)
    )

    column_quality = column_quality.sort_values(
        "Completeness"
    )

    st.dataframe(
        column_quality,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Completeness": st.column_config.ProgressColumn(
                "Completeness",
                min_value=0,
                max_value=100,
                format="%.2f%%",
            ),
        },
    )

else:

    st.warning(
        "Customer CSV could not be loaded."
    )


st.divider()


st.markdown(
    '<div class="section-title">Issue Explorer</div>',
    unsafe_allow_html=True,
)


f1, f2, f3 = st.columns([1, 1, 2])


with f1:

    severity_options = [
        "All"
    ] + sorted(
        issues["severity"].dropna().unique().tolist()
    )

    selected_severity = st.selectbox(
        "Severity",
        severity_options,
    )


with f2:

    column_options = [
        "All"
    ] + sorted(
        issues["column_name"].dropna().unique().tolist()
    )

    selected_column = st.selectbox(
        "Column",
        column_options,
    )


with f3:

    search_term = st.text_input(
        "Search issues",
        placeholder="e.g. email, missing, duplicate",
    )


filtered_issues = issues.copy()


if selected_severity != "All":

    filtered_issues = filtered_issues[
        filtered_issues["severity"]
        == selected_severity
    ]


if selected_column != "All":

    filtered_issues = filtered_issues[
        filtered_issues["column_name"]
        == selected_column
    ]


if search_term:

    search_mask = (
        filtered_issues["issue_type"]
        .str.contains(
            search_term,
            case=False,
            na=False,
        )
        |
        filtered_issues["column_name"]
        .str.contains(
            search_term,
            case=False,
            na=False,
        )
    )

    filtered_issues = filtered_issues[
        search_mask
    ]


st.dataframe(
    filtered_issues,
    use_container_width=True,
    hide_index=True,
)


csv_data = filtered_issues.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download filtered issues",
    data=csv_data,
    file_name=f"quality_issues_run_{selected_run}.csv",
    mime="text/csv",
)


st.divider()


with st.expander("Dataset Preview"):

    if not customer_data.empty:

        preview_rows = st.slider(
            "Rows to display",
            min_value=5,
            max_value=50,
            value=10,
        )

        st.dataframe(
            customer_data.head(preview_rows),
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No customer dataset available."
        )


with st.expander("Project Information"):

    st.write(
        """
        This dashboard monitors the quality of a customer
        dataset across multiple pipeline executions.

        The pipeline evaluates:

        • Completeness
        • Validity
        • Uniqueness
        • Consistency

        Detected issues are stored in SQLite and exposed
        through this interactive monitoring interface.
        """
    )
