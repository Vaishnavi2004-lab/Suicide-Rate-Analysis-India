import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# PAGE SETTINGS

st.set_page_config(
    page_title="Suicide Rate Analysis",
    page_icon="📊",
    layout="wide"
)

# CUSTOM CSS

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

h1, h2, h3 {
    color: #00ADB5;
}

.stMetric {
    background-color: #1E1E1E;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# LOAD DATASET

df = pd.read_csv("data/Suicides in India 2001-2012.csv")

# SIDEBAR MENU

with st.sidebar:

    st.markdown("## 📊 Suicide Analytics Dashboard")

    st.markdown(
        "Analyze suicide trends across India using interactive data visualization."
    )

    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "State Analysis", "Year Analysis"],
        icons=["house", "bar-chart", "graph-up"],
        menu_icon="cast",
        default_index=0,
    )

# HOME PAGE

if selected == "Home":

    st.title("📊 Suicide Rate Analysis - India")

    st.markdown("### Analyze suicide trends across India")

    # STATE FILTER

    states = sorted(df["State"].unique())

    st.sidebar.subheader("🔍 Filter Data")

    selected_state = st.sidebar.selectbox(
        "Select State",
        states
    )

    # FILTERED DATA

    filtered_data = df[df["State"] == selected_state]

    # KPI CARDS

    total_cases = filtered_data["Total"].sum()
    total_years = filtered_data["Year"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cases", f"{total_cases:,}")
    col2.metric("Selected State", selected_state)
    col3.metric("Years", total_years)

    # DATASET PREVIEW

    st.subheader("📁 Dataset Preview")

    st.dataframe(filtered_data.head())

    # YEAR-WISE LINE CHART

    st.subheader(f"📈 Year-wise Suicide Trends in {selected_state}")

    year_data = filtered_data.groupby("Year")["Total"].sum().reset_index()

    fig = px.line(
        year_data,
        x="Year",
        y="Total",
        markers=True,
        title=f"Total Suicides Over Years in {selected_state}"
    )

    st.plotly_chart(fig, use_container_width=True)

    # STATE BAR GRAPH

    st.subheader(f"📊 Suicide Cases in {selected_state}")

    state_year = filtered_data.groupby("Year")["Total"].sum().reset_index()

    fig2 = px.bar(
        state_year,
        x="Year",
        y="Total",
        color="Total",
        title=f"Year-wise Suicide Cases in {selected_state}"
    )

    st.plotly_chart(fig2, use_container_width=True)

    # GENDER ANALYSIS

    st.subheader("👨 Male vs 👩 Female Analysis")

    gender_data = filtered_data.groupby("Gender")["Total"].sum().reset_index()

    fig5 = px.pie(
        gender_data,
        names="Gender",
        values="Total",
        title=f"Male vs Female Suicide Distribution in {selected_state}",
        hole=0.4
    )

    st.plotly_chart(fig5, use_container_width=True)

    # AI INSIGHTS

    st.subheader("🤖 AI Generated Insights")

    highest_year_data = filtered_data.groupby("Year")["Total"].sum().reset_index()

    highest_year = highest_year_data.loc[
        highest_year_data["Total"].idxmax(),
        "Year"
    ]

    male_total = filtered_data[
        filtered_data["Gender"] == "Male"
    ]["Total"].sum()

    female_total = filtered_data[
        filtered_data["Gender"] == "Female"
    ]["Total"].sum()

    st.success(f"📌 Selected State: {selected_state}")

    st.info(f"📅 Highest suicide year in {selected_state}: {highest_year}")

    st.warning("👨 Male cases are significantly higher than female cases.")

    st.write(f"👨 Male Total Cases: {male_total:,}")

    st.write(f"👩 Female Total Cases: {female_total:,}")

    # DOWNLOAD BUTTON

    csv = filtered_data.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="📥 Download Filtered Data",
        data=csv,
        file_name='filtered_suicide_data.csv',
        mime='text/csv',
    )

# STATE ANALYSIS PAGE

if selected == "State Analysis":

    st.title("🏙️ State Analysis")

    st.markdown("### Top States with Highest Suicide Cases")

    state_data = df.groupby("State")["Total"].sum().reset_index()

    fig3 = px.bar(
        state_data.sort_values(by="Total", ascending=False).head(10),
        x="State",
        y="Total",
        color="Total",
        title="Top 10 States with Highest Suicide Cases"
    )

    st.plotly_chart(fig3, use_container_width=True)

# YEAR ANALYSIS PAGE

if selected == "Year Analysis":

    st.title("📅 Year Analysis")

    st.markdown("### Suicide Trends Over the Years")

    year_data = df.groupby("Year")["Total"].sum().reset_index()

    fig4 = px.area(
        year_data,
        x="Year",
        y="Total",
        title="Year-wise Suicide Analysis"
    )

    st.plotly_chart(fig4, use_container_width=True)

# FOOTER

st.markdown("---")
st.markdown("### 👩‍💻 Developed by Vaishnavi Sarje")