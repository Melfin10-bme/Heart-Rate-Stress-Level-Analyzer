from __future__ import annotations
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.hrv import preprocess, time_domain_metrics

st.set_page_config(page_title="Session Explorer", page_icon="📊", layout="wide")

st.markdown("## 📊 Session Explorer")
st.caption("Upload multiple sessions to compare HR and HRV metrics.")

files = st.file_uploader("Upload one or more CSV files", type=["csv"], accept_multiple_files=True)

if not files:
    st.info("Upload CSV files to compare sessions.")
    st.stop()

rows = []
plots = []
for f in files:
    try:
        df = preprocess(pd.read_csv(f))
    except Exception as e:
        st.warning(f"Failed to parse {f.name}: {e}")
        continue
    td = time_domain_metrics(df["rr_ms"].values)
    mean_hr = df["heart_rate"].mean() if not df.empty else float("nan")
    rows.append(dict(
        file=f.name,
        mean_hr_bpm=mean_hr,
        sdnn_ms=td["sdnn"],
        rmssd_ms=td["rmssd"],
        pnn50_percent=td["pnn50"],
        n=len(df),
    ))
    fig = px.line(df, x="timestamp", y="heart_rate", title=f"HR over time — {f.name}",
                  labels={"timestamp":"Time", "heart_rate":"Heart Rate (bpm)"})
    fig.update_layout(height=300, margin=dict(l=10,r=10,t=30,b=10))
    plots.append(fig)

st.markdown("### Summary Table")
st.dataframe(pd.DataFrame(rows))

st.markdown("### Plots")
for fig in plots:
    st.plotly_chart(fig, use_container_width=True)
