import time  # to simulate a real time data, time loop
from datetime import datetime, date, timedelta
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development



now = date.today()
# now = now.strftime("%Y/%m/%d-%H-%M-%S")
# now = datetime.strptime(now, "%Y/%m/%d-%H-%M-%S")

st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
    page_icon="✅",
    layout="wide",
)
st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)
# dashboard title
st.title("Real-Time / Live Data Science Dashboard")
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
default_date_range = [datetime(2015, 1, 8), now]
def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    # np.abs((y_true - y_pred) / y_true) * 100
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
def set_date_range(date_range) -> list:
    """Set Date Range
    Returns:
        list: ["2006-05-1", "2021-02-28"]
    """
    # st.write("## Date Range")
    # current date and time
    
    
    
   
        # date_range = default_date_range
    date_range = list(date_range)
    date_range.sort()
    if len(date_range) == 2:
        return date_range
    else:
        return date_range + date_range

# read csv from a github repo
# dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

# read csv from a URL
@st.cache_data()
def get_data(date_range) -> pd.DataFrame:
    assert len(date_range) == 2
    dates  = pd.read_csv('AESO_data.csv', index_col=1, parse_dates=['date_time'])
    # dates["mape_price"] = dates.apply(lambda x: mean_absolute_percentage_error(x.ACTUAL_POOL_PRICE, x.Forecasted_Price), axis=1)
    # dates["mape_load"] = dates.apply(lambda x: mean_absolute_percentage_error(x.ACTUAL_LOAD, x.Forecasted_load), axis=1)
    # dates["ACTUAL_POOL_PRICE"] + 0.1 * dates["ACTUAL_POOL_PRICE"]
    # dates["Forecasted_load"] = dates["load"] + 0.2 * dates["load"]
    dates = dates.loc[(dates.index > date_range[0] ) & (dates.index <= date_range[1])]
    return dates
 

    
    
    
    # date_range = st.select_slider(
    #     "When do you start?",
    #     value=[datetime(2015, 8, 1, 00,00), now],
    #     # format="YYYY/MM/DD -hh:mm",
    #     min_value=datetime(2015, 8, 1, 00,00),
    #     max_value=now,
    #     # step=timedelta(minutes=15)
    # )
    # st.write(date_range)
m = st.markdown("""
<style>
div.stButton > button:first-child {
    height: 0.5em;
    width: 2em;
    font-size:50px;
}
</style>""", unsafe_allow_html=True)
padding1, dt = st.columns([25,5])
ph1 = dt.empty()
with ph1.container():
    def reset_date():
        st.session_state.date = default_date_range
    date_range = dt.date_input(
        "Date",
        value=default_date_range,
        min_value=date(2015, 1, 8),
        max_value=now,
        key='date'
    )
    # padding, dt = st.columns([25,5])
    dt.button("Reset Date", on_click = reset_date)
# date_range = set_date_range()
# if 'date' not in st.session_state:
#     st.session_state.date = default_date_range


date_range = [date.strftime("%Y-%m-%d %H:%M:%S") for date in date_range]
# start_date_time = datetime.strptime(date_range[0], "%Y-%m-%d %H:%M:%S")
end_date_time = datetime.strptime(date_range[1], "%Y-%m-%d %H:%M:%S") #(date_range[1])
prediction_time = end_date_time + timedelta(days=1)
forecast_date_range = [date_range[0], prediction_time]
df_forecast = get_data(forecast_date_range)





# top-level filters
# job_filter = st.selectbox("Select the Job", pd.unique(df["job"]))

# creating a single-element container
placeholder = padding1.empty()

# creating KPIs
avg_load = np.mean(df_forecast["ACTUAL_LOAD"][-4:])
load_mape = mean_absolute_percentage_error(df_forecast["ACTUAL_LOAD"][-4:], df_forecast["Forecasted_load"][-4:])

avg_price = np.mean(df_forecast["ACTUAL_POOL_PRICE"][-4:])
price_mape = mean_absolute_percentage_error(df_forecast["ACTUAL_POOL_PRICE"][-4:], df_forecast["Forecasted_Price"][-4:])

with placeholder.container():
    # st.markdown('###') 
    # create three columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="large")

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="Load",
        value=round(avg_load),
        # delta=round(avg_load) - 10,
    )
    
    kpi2.metric(
        label="MAPE_Load %",
        value=f"{round(load_mape,2)} % "
        # delta=round(-10 + wind_speed),
    )
    
    kpi3.metric(
        label="Price ＄",
        value=f"$ {round(avg_price,2)} "
        # delta=-round(avg_price),
    )

    kpi4.metric(
        label="MAPE_Price %",
        value=f"{round(price_mape,2)} % "
        # delta=-round(avg_price),
    )
    # st.write("## Plots")

# create two columns for charts
fig_col1, fig_col2 = st.columns(2)
# fig_col1 = st.columns(1)
filtered = df_forecast.loc[(df_forecast.index >date_range[0] ) & (df_forecast.index <= date_range[1])]
if date_range[0]==date_range[1]:
    filtered = df_forecast
with fig_col1:
    # st.markdown("### Charts")
    
    d = {
            "time" : df_forecast.index,
            "Forecasted_Price" : pd.Series(df_forecast.Forecasted_Price),
            "ACTUAL_POOL_PRICE" : pd.Series(filtered.ACTUAL_POOL_PRICE)
        }
    df2 = pd.DataFrame(d)
    fig = px.line(df2, x=df2.index, y=["Forecasted_Price","ACTUAL_POOL_PRICE"],
                            # custom_data=["Forecasted_Price","ACTUAL_POOL_PRICE"],
                            title="Price")
    newnames = {'Forecasted_Price':'Forecast', 'ACTUAL_POOL_PRICE': 'Actual'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                    legendgroup = newnames[t.name],
                                    hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                        )
                        )
    fig.update_layout(hovermode="x unified")
    # fig.update_layout(legend=dict(
    #                         yanchor="top",
    #                         y=0.99,
    #                         xanchor="left",
    #                         x=0.01
    #                     ))
    # fig = px.line(df2, x="x", y="y", title="Unsorted Input")
    # fig = px.density_heatmap(
    #     data_frame=df, y="age_new", x="marital"
    # )
    st.plotly_chart(fig, use_container_width=True) 
    # st.write(fig)
    
with fig_col2:
#     st.markdown("### Charts")
    
    d = {
            "time" : df_forecast.index,
            "Forecasted_Load" : pd.Series(df_forecast.Forecasted_load),
            "ACTUAL_LOAD" : pd.Series(filtered.ACTUAL_LOAD)
        }
    df2 = pd.DataFrame(d)
    fig = px.line(df2, x=df2.index, y=["Forecasted_Load","ACTUAL_LOAD"],
                            # custom_data=["Forecasted_Price","ACTUAL_POOL_PRICE"],
                            title="Load")
    newnames = {'Forecasted_Load':'Forecast', 'ACTUAL_LOAD': 'Actual'}
    fig.for_each_trace(lambda t: t.update(name = newnames[t.name],
                                    legendgroup = newnames[t.name],
                                    hovertemplate = t.hovertemplate.replace(t.name, newnames[t.name])
                                        )
                        )
    fig.update_layout(hovermode="x unified")
    # fig = px.line(df2, x="x", y="y", title="Unsorted Input")
    # fig = px.density_heatmap(
    #     data_frame=df, y="age_new", x="marital"
    # )
    st.plotly_chart(fig, use_container_width=True)
st.markdown("### Detailed Data View")
columns = ['temp_c','dew_point_temp_c','rel_hum_%','wind_dir_10s_deg','wind_spd_km_h']
st.dataframe(filtered[columns][-24:])
    # time.sleep(1)