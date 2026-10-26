import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="COVID-19 Global Impact Dashboard", page_icon="📊", layout="wide")
BASE=Path(__file__).resolve().parent
DATA=BASE/"data/covid_synthetic_clean.csv"
st.title("COVID-19 Global Impact Dashboard")
st.error("SYNTHETIC PRACTICE DATA — NOT OFFICIAL COVID-19 STATISTICS. For demonstration only; no real country statistics are represented.")
df=pd.read_csv(DATA, parse_dates=["date"])
with st.sidebar:
    st.header("Filters")
    countries=st.multiselect("Country", sorted(df.country.unique()), default=sorted(df.country.unique()))
    low,high=df.date.min().date(),df.date.max().date()
    dates=st.date_input("Date range", value=(low,high), min_value=low, max_value=high)
if len(dates)!=2: st.info("Select a start and end date."); st.stop()
start,end=pd.Timestamp(dates[0]),pd.Timestamp(dates[1])
f=df[df.country.isin(countries)&df.date.between(start,end)].copy()
if f.empty: st.warning("No records match these filters."); st.stop()
latest=f.sort_values("date").groupby("country").tail(1)
c1,c2,c3=st.columns(3)
c1.metric("Total cumulative cases",f"{int(latest.total_cases.sum()):,}")
c2.metric("Total cumulative deaths",f"{int(latest.total_deaths.sum()):,}")
c3.metric("Vaccination coverage", "Not available", help="Population denominator is absent. Coverage is not calculated from vaccination counts alone.")
st.caption("Case and death KPIs sum the latest available cumulative observation for each selected country within the selected date range.")
left,right=st.columns(2)
with left:
    st.subheader("Daily new cases and 7-day average")
    fig=px.line(f,x="date",y=["new_cases","cases_7d_avg"],color="country",labels={"date":"Date","value":"Cases","variable":"Series","country":"Country"})
    # Distinguish series in legend labels
    fig.for_each_trace(lambda t: t.update(name=f"{t.name} — {'7-day avg' if 'cases_7d_avg' in t.name else 'daily'}"))
    st.plotly_chart(fig,use_container_width=True)
with right:
    st.subheader("Cumulative deaths over time")
    st.plotly_chart(px.line(f,x="date",y="total_deaths",color="country",labels={"date":"Date","total_deaths":"Cumulative deaths","country":"Country"}),use_container_width=True)
st.subheader("Country comparison — cumulative cases at end of selected range")
compare=latest.sort_values("total_cases",ascending=False)
st.plotly_chart(px.bar(compare,x="country",y="total_cases",color="country",labels={"country":"Country","total_cases":"Cumulative cases"}),use_container_width=True)
with st.expander("Data preview and limitations"):
    st.write("Synthetic demonstration data only. Counts are fabricated and are not official statistics. Vaccination coverage cannot be computed because a valid population denominator is not part of this dashboard's dataset.")
    st.dataframe(f, use_container_width=True)
    st.download_button("Download filtered data CSV",f.to_csv(index=False).encode(),"filtered_covid_data.csv","text/csv")
