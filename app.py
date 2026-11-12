
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from datetime import datetime, time
from zoneinfo import ZoneInfo
from pathlib import Path


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="App Atlas | Global App Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

IST = ZoneInfo("Asia/Kolkata")

START_TIME = time(18, 0)
END_TIME = time(20, 0)

DATA_DIR = Path(__file__).parent / "data"

# Automatic refresh every minute
try:
    from streamlit_autorefresh import st_autorefresh
    st_autorefresh(
        interval=60 * 1000,
        key="app_atlas_refresh"
    )
except ImportError:
    pass

current_time = datetime.now(IST)
current_clock = current_time.time().replace(tzinfo=None)

GRAPH_AVAILABLE = START_TIME <= current_clock < END_TIME


# =========================================================
# 2. CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1220;
    color: #edf3ff;
}

[data-testid="stHeader"] {
    background-color: transparent;
}

[data-testid="stSidebar"] {
    background-color: #101a2b;
    border-right: 1px solid #263750;
}

[data-testid="stSidebar"] * {
    color: #e6edf7;
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #f1f6ff !important;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #1b2a43, #142137);
    border: 1px solid #30435f;
    padding: 18px;
    border-radius: 15px;
}

div[data-testid="stMetric"] label {
    color: #9fb2cc !important;
}

div[data-testid="stMetricValue"] {
    color: #72e7cd !important;
}

div[data-testid="stMetricDelta"] {
    color: #72e7cd !important;
}

.stSelectbox label,
.stFileUploader label,
.stNumberInput label {
    color: #dce8f8 !important;
}

.stButton button {
    background-color: #72e7cd;
    color: #0b1725;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

.stButton button:hover {
    background-color: #a0f5e2;
    color: #0b1725;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #30435f;
    border-radius: 12px;
}

hr {
    border-color: #30435f;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 3. HELPER FUNCTIONS
# =========================================================

def parse_installs(value):

    if pd.isna(value):
        return 0

    value = str(value).strip()

    if value.lower() in ["nan", "null", ""]:
        return 0

    value = value.replace(",", "").replace("+", "").strip()

    try:
        return float(value)
    except (ValueError, TypeError):
        return 0


def format_number(value):
    return f"{value:,.0f}"


def clean_columns(df):

    df = df.copy()

    df.columns = [
        str(column).strip().replace("\ufeff", "")
        for column in df.columns
    ]

    return df


def find_column(df, possible_names):

    lookup = {
        str(column).strip().lower(): column
        for column in df.columns
    }

    for name in possible_names:

        if name.lower() in lookup:
            return lookup[name.lower()]

    return None


def apply_chart_theme(fig, height=420):

    fig.update_layout(
        height=height,
        paper_bgcolor="#101a2b",
        plot_bgcolor="#101a2b",
        font=dict(
            color="#dce8f8",
            family="Arial"
        ),
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=30
        ),
        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        )
    )

    fig.update_xaxes(
        gridcolor="#293b55",
        zerolinecolor="#293b55"
    )

    fig.update_yaxes(
        gridcolor="#293b55",
        zerolinecolor="#293b55"
    )

    return fig


# =========================================================
# 4. DASHBOARD HEADER
# =========================================================

with st.container(border=True):

    st.caption("GLOBAL APP INTELLIGENCE PLATFORM")

    st.title("🌍 APP ATLAS")

    st.write(
        "Discover app install patterns, category performance "
        "and geographic insights through interactive analytics."
    )


# =========================================================
# 5. SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🌍 APP ATLAS")

    st.caption("Global App Intelligence Dashboard")

    st.divider()

    st.subheader("📁 Upload Datasets")

    play_file = st.file_uploader(
        "Upload Play Store CSV",
        type=["csv"],
        key="play_csv"
    )

    geo_file = st.file_uploader(
        "Upload Country-Level Installs CSV",
        type=["csv"],
        key="geo_csv"
    )

    st.divider()

    st.subheader("⚙️ Dashboard Settings")

    highlight_limit = st.number_input(
        "Install highlight threshold",
        min_value=1,
        value=1_000_000,
        step=100_000
    )

    st.divider()

    st.subheader("🕒 Graph Schedule")

    st.write("**6:00 PM – 8:00 PM IST**")

    st.caption(
        "Current IST: " +
        current_time.strftime("%I:%M:%S %p")
    )

    if GRAPH_AVAILABLE:
        st.success("Graphs are active.")
    else:
        st.warning("Graphs are currently hidden.")


# =========================================================
# 6. LOAD PLAY STORE DATA
# =========================================================

play_path = DATA_DIR / "Play Store Data.csv"

if not play_path.exists():

    alternate_path = DATA_DIR / "Play Store Data(4).csv"

    if alternate_path.exists():
        play_path = alternate_path


try:

    if play_file is not None:

        df = pd.read_csv(play_file)

    elif play_path.exists():

        df = pd.read_csv(play_path)

    else:

        df = None

except Exception as error:

    st.error(f"Unable to read Play Store CSV: {error}")
    st.stop()


if df is None:

    st.warning(
        "Please upload your Play Store CSV from the sidebar "
        "or place it inside the data folder."
    )

    st.stop()


df = clean_columns(df)


# =========================================================
# 7. IDENTIFY COLUMNS
# =========================================================

category_col = find_column(df, ["Category"])

installs_col = find_column(df, ["Installs"])

app_col = find_column(df, ["App"])

rating_col = find_column(df, ["Rating"])

reviews_col = find_column(df, ["Reviews"])


if category_col is None or installs_col is None:

    st.error(
        "Your dataset must contain Category and Installs columns."
    )

    st.stop()


# =========================================================
# 8. DATA CLEANING
# =========================================================

df[category_col] = (
    df[category_col].astype(str).str.strip()
)

df["Install_Count"] = (
    df[installs_col].apply(parse_installs)
)

df = df[
    df[category_col].notna()
    & (df[category_col] != "")
    & (df[category_col].str.lower() != "nan")
].copy()


# Exclude categories starting with A, C, G and S

excluded_prefixes = ("A", "C", "G", "S")

eligible_df = df[
    ~df[category_col].str.upper().str.startswith(
        excluded_prefixes
    )
].copy()


if eligible_df.empty:

    st.warning("No eligible categories found.")

    st.stop()


# =========================================================
# 9. TOP 5 CATEGORY ANALYSIS
# =========================================================

category_summary = (
    eligible_df.groupby(category_col, as_index=False)
    .agg(
        Total_Installs=("Install_Count", "sum"),
        App_Count=(category_col, "count")
    )
    .sort_values(
        "Total_Installs",
        ascending=False
    )
)

top_categories = category_summary.head(5).copy()

if top_categories.empty:

    st.warning("No category data available.")

    st.stop()


top_category_names = top_categories[category_col].tolist()

top_apps_df = eligible_df[
    eligible_df[category_col].isin(top_category_names)
].copy()


total_installs = int(
    top_categories["Total_Installs"].sum()
)

total_apps = len(top_apps_df)

best_category = top_categories.iloc[0][category_col]


# =========================================================
# 10. DASHBOARD OVERVIEW — ALL DAY
# =========================================================

st.divider()

st.header("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Top 5 Categories",
        len(top_categories)
    )

with col2:

    st.metric(
        "Total Installs",
        format_number(total_installs)
    )

with col3:

    st.metric(
        "Apps Analysed",
        format_number(total_apps)
    )

with col4:

    st.metric(
        "Leading Category",
        best_category
    )


# =========================================================
# 11. GRAPHS — ONLY BETWEEN 6 PM AND 8 PM IST
# =========================================================

if GRAPH_AVAILABLE:

    st.divider()

    st.header("📈 Interactive Analytics Dashboard")

    st.success(
        "Analytics are active — available until 8:00 PM IST."
    )

    # -----------------------------------------------------
    # CATEGORY SELECTOR
    # -----------------------------------------------------

    selected_category = st.selectbox(
        "Select a category to explore",
        top_category_names
    )

    selected_data = top_apps_df[
        top_apps_df[category_col] == selected_category
    ].copy()


    # -----------------------------------------------------
    # BAR CHART
    # -----------------------------------------------------

    st.subheader("📊 Top 5 Categories by Installs")

    bar_data = top_categories.copy()

    bar_data["Status"] = np.where(
        bar_data["Total_Installs"] > highlight_limit,
        "Above 1 Million",
        "At or Below Threshold"
    )

    fig_bar = px.bar(
        bar_data.sort_values("Total_Installs"),
        x="Total_Installs",
        y=category_col,
        orientation="h",
        color="Status",
        color_discrete_map={
            "Above 1 Million": "#72e7cd",
            "At or Below Threshold": "#6686b5"
        },
        text="Total_Installs",
        labels={
            "Total_Installs": "Total Installs",
            category_col: "Category"
        }
    )

    fig_bar.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside",
        cliponaxis=False
    )

    fig_bar = apply_chart_theme(fig_bar, 450)

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )


    # -----------------------------------------------------
    # DONUT CHART
    # -----------------------------------------------------

    st.subheader("🍩 Install Share by Category")

    fig_donut = px.pie(
        top_categories,
        names=category_col,
        values="Total_Installs",
        hole=0.60
    )

    fig_donut.update_traces(
        textposition="inside",
        textinfo="percent+label",
        marker=dict(
            line=dict(
                color="#101a2b",
                width=3
            )
        )
    )

    fig_donut = apply_chart_theme(fig_donut, 450)

    st.plotly_chart(
        fig_donut,
        use_container_width=True
    )


    # -----------------------------------------------------
    # SELECTED CATEGORY INSIGHTS
    # -----------------------------------------------------

    st.divider()

    st.subheader("📌 Selected Category Insights")

    selected_installs = int(
        selected_data["Install_Count"].sum()
    )

    d1, d2, d3 = st.columns(3)

    with d1:

        st.metric(
            "Selected Category",
            selected_category
        )

    with d2:

        st.metric(
            "Category Installs",
            format_number(selected_installs)
        )

    with d3:

        st.metric(
            "Number of Apps",
            len(selected_data)
        )


    # -----------------------------------------------------
    # APP DATA TABLE
    # -----------------------------------------------------

    st.divider()

    st.subheader("📋 App Records")

    display_columns = []

    for column in [
        app_col,
        category_col,
        rating_col,
        reviews_col
    ]:

        if column is not None:
            display_columns.append(column)

    display_columns.append("Install_Count")

    table_data = selected_data[
        display_columns
    ].copy()

    table_data = table_data.sort_values(
        "Install_Count",
        ascending=False
    )

    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True
    )


    # -----------------------------------------------------
    # WORLD MAP
    # -----------------------------------------------------

    st.divider()

    st.subheader("🌐 Global Install Distribution")

    geo_path = DATA_DIR / "country_category_installs.csv"

    geo_df = None

    try:

        if geo_file is not None:

            geo_df = pd.read_csv(geo_file)

        elif geo_path.exists():

            geo_df = pd.read_csv(geo_path)

    except Exception as error:

        st.error(f"Unable to read geographic CSV: {error}")


    if geo_df is None:

        st.info(
            "Country-level data is not available. "
            "Upload a genuine geographic CSV containing "
            "Country, Category and Installs columns "
            "to display the world map."
        )

    else:

        geo_df = clean_columns(geo_df)

        country_col = find_column(
            geo_df,
            ["Country", "Country Name", "Country Code", "ISO3"]
        )

        geo_category_col = find_column(
            geo_df,
            ["Category"]
        )

        geo_installs_col = find_column(
            geo_df,
            ["Installs", "Total Installs", "Install_Count"]
        )

        if (
            country_col is None
            or geo_category_col is None
            or geo_installs_col is None
        ):

            st.error(
                "Geographic CSV must contain Country, "
                "Category and Installs columns."
            )

        else:

            geo_df["Map_Installs"] = (
                geo_df[geo_installs_col].apply(parse_installs)
            )

            geo_df[geo_category_col] = (
                geo_df[geo_category_col].astype(str).str.strip()
            )

            geo_df[country_col] = (
                geo_df[country_col].astype(str).str.strip()
            )

            geo_df = geo_df[
                geo_df[geo_category_col].isin(top_category_names)
            ].copy()

            map_categories = sorted(
                geo_df[geo_category_col].dropna().unique().tolist()
            )

            if not map_categories:

                st.warning(
                    "No geographic records match the top five categories."
                )

            else:

                map_category = st.selectbox(
                    "Choose a category for the world map",
                    map_categories,
                    key="map_category"
                )

                map_data = geo_df[
                    geo_df[geo_category_col] == map_category
                ].copy()

                map_data = (
                    map_data.groupby(country_col, as_index=False)
                    .agg(
                        Map_Installs=("Map_Installs", "sum")
                    )
                )

                is_iso3 = map_data[country_col].astype(str).str.fullmatch(
                    r"[A-Za-z]{3}"
                ).all()

                location_mode = (
                    "ISO-3" if is_iso3 else "country names"
                )

                fig_map = px.choropleth(
                    map_data,
                    locations=country_col,
                    locationmode=location_mode,
                    color="Map_Installs",
                    hover_name=country_col,
                    hover_data={
                        "Map_Installs": ":,"
                    },
                    color_continuous_scale=[
                        "#14243b",
                        "#245a70",
                        "#3caeaa",
                        "#72e7cd"
                    ],
                    projection="natural earth",
                    title=f"Global Installs - {map_category}"
                )

                fig_map.update_layout(
                    height=570,
                    paper_bgcolor="#101a2b",
                    plot_bgcolor="#101a2b",
                    font=dict(color="#e6edf7"),
                    margin=dict(
                        l=0,
                        r=0,
                        t=55,
                        b=0
                    ),
                    geo=dict(
                        bgcolor="#101a2b",
                        showframe=False,
                        showcoastlines=True,
                        coastlinecolor="#526781",
                        showland=True,
                        landcolor="#1a2940",
                        showocean=True,
                        oceancolor="#0c1728",
                        showcountries=True,
                        countrycolor="#40536d"
                    )
                )

                st.plotly_chart(
                    fig_map,
                    use_container_width=True
                )

                highlighted = map_data[
                    map_data["Map_Installs"] > highlight_limit
                ]

                st.write(
                    "Countries above "
                    f"{format_number(highlight_limit)} installs: "
                    f"{len(highlighted)}"
                )

                if not highlighted.empty:

                    st.dataframe(
                        highlighted.sort_values(
                            "Map_Installs",
                            ascending=False
                        ),
                        use_container_width=True,
                        hide_index=True
                    )


# =========================================================
# 12. OUTSIDE SCHEDULE
# =========================================================

else:

    st.divider()

    st.info(
        "📊 The interactive graphs and analytical sections "
        "are available only between 6:00 PM and 8:00 PM IST. "
        "Please revisit during the scheduled time. "
        "The dashboard automatically checks availability every minute."
    )


# =========================================================
# 13. FOOTER
# =========================================================

st.divider()

st.caption(
    "APP ATLAS · GLOBAL APP INTELLIGENCE DASHBOARD"
)

st.caption(
    "Built with Python · Streamlit · Pandas · Plotly"
)
