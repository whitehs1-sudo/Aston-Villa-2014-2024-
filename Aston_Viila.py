import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Aston Villa 10-Year Performance Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("data/villa_10yr_matches.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()

st.title("Aston Villa Performance Dashboard (2014–2024)")
st.markdown("""
**Analytical Objective:**  
Analyze Aston Villa’s performance trends over the past decade, identifying how scoring, defensive stability, and match-level efficiency evolved across managerial eras and league contexts.
""")

tab1, tab2 = st.tabs(["Season Trends", "Match-Level Analysis"])

# ---------------- TAB 1 ----------------
with tab1:
    st.header("Season Trends Overview")

    # Sidebar filters
    seasons = sorted(df["Season"].unique())
    season_range = st.sidebar.slider("Season range", min_value=seasons[0], max_value=seasons[-1], value=(seasons[0], seasons[-1]))

    filtered = df[(df["Season"] >= season_range[0]) & (df["Season"] <= season_range[1])]

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Goals Scored", f"{filtered['GF'].mean():.2f}")
    col2.metric("Avg Goals Conceded", f"{filtered['GA'].mean():.2f}")
    col3.metric("Win %", f"{(filtered['Result'] == 'W').mean()*100:.1f}%")

    # Line chart
    season_summary = filtered.groupby("Season")[["GF", "GA"]].mean().reset_index()
    fig_line = px.line(season_summary, x="Season", y=["GF", "GA"], title="Goals Scored vs Conceded (Season Avg)")
    st.plotly_chart(fig_line, use_container_width=True)

    # Bar chart
    points = filtered.groupby("Season")["Points"].sum().reset_index()
    fig_bar = px.bar(points, x="Season", y="Points", title="Total Points per Season")
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown("""
### Interpretation  
Discuss major shifts: relegation season collapse, Championship recovery, and Emery’s tactical impact.
""")

# ---------------- TAB 2 ----------------
with tab2:
    st.header("Match-Level Performance")

    # Filters
    result_filter = st.multiselect("Results", ["W", "D", "L"], default=["W", "D", "L"])
    df2 = filtered[filtered["Result"].isin(result_filter)]

    # Scatter: xG vs xGA
    fig_scatter = px.scatter(df2, x="xG", y="xGA", color="Result", hover_data=["Opponent", "Date"], title="xG vs xGA by Match")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Heatmap
    corr_cols = ["GF", "GA", "xG", "xGA", "Shots", "Possession"]
    corr = df2[corr_cols].corr()
    fig_heat = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", title="Correlation Matrix")
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""
### Interpretation  
Explain which match metrics most strongly align with winning (e.g., xG dominance, low xGA, shot volume).
""")
