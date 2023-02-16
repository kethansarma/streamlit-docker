import time  # to simulate a real time data, time loop
import datetime
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

def set_date_range() -> list:
    """Set Date Range
    Returns:
        list: ["2006-05-1", "2021-02-28"]
    """
    st.write("## Date Range")
    default_date_range = [datetime.date(2020, 1, 1), datetime.date.today()]
    date_range = st.date_input(
        "Selector",
        value=default_date_range,
        min_value=datetime.date(2020, 1, 1),
        max_value=datetime.date.today(),
    )
    if st.button("Reset Date Range"):
        date_range = default_date_range
    date_range = list(date_range)
    date_range.sort()
    if len(date_range) == 2:
        return date_range
    else:
        return date_range + date_range
st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)
date_range = set_date_range()
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# read csv from a github repo
dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# read csv from a URL
@st.cache_data()
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

df = get_data()

# dashboard title
st.title("Real-Time / Live Data Science Dashboard")

# top-level filters
job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

# creating a single-element container
placeholder = st.empty()

# dataframe filter
df = df[df["job"] == job_filter]

# near real-time / live feed simulation
for seconds in range(200):

    df["age_new"] = df["age"] * np.random.choice(range(1, 5))
    df["balance_new"] = df["balance"] * np.random.choice(range(1, 5))

    # creating KPIs
    avg_age = np.mean(df["age_new"])

    count_married = int(
        df[(df["marital"] == "married")]["marital"].count()
        + np.random.choice(range(1, 30))
    )

    balance = np.mean(df["balance_new"])

    with placeholder.container():

        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Age ⏳",
            value=round(avg_age),
            delta=round(avg_age) - 10,
        )
        
        kpi2.metric(
            label="Married Count 💍",
            value=int(count_married),
            delta=-10 + count_married,
        )
        
        kpi3.metric(
            label="A/C Balance ＄",
            value=f"$ {round(balance,2)} ",
            delta=-round(balance / count_married) * 100,
        )

        # create two columns for charts
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.density_heatmap(
                data_frame=df, y="age_new", x="marital"
            )
            st.plotly_chart(fig, use_container_width=True) 
            # st.write(fig)
            
        with fig_col2:
            st.markdown("### Second Chart")
            fig2 = px.histogram(data_frame=df, x="age_new")
            # st.write(fig2)
            st.plotly_chart(fig2, use_container_width=True) 

        st.markdown("### Detailed Data View")
        st.dataframe(df)
        time.sleep(1)