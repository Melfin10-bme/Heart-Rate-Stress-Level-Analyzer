import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.hrv import preprocess, time_domain_metrics, estimate_stress
from utils.styling import inject_css

st.set_page_config(
    page_title="Heart Rate & Stress Analyzer",
    page_icon="🫀",
    layout="wide",
)

inject_css()

st.title("🫀 Heart Rate & Stress Level Analyzer")
st.caption("Upload your heart rate data, compute HRV, and estimate stress levels.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    window_s = st.slider("RMSSD window (seconds)", 30, 300, 60, step=15)
    uploaded_file = st.file_uploader("Upload CSV (timestamp + heart_rate)", type=["csv"])
    use_sample = st.checkbox("Use sample dataset")

# Load Data
if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
elif use_sample:
    df_raw = pd.read_csv("sample_data/sample_heart_rate.csv")
else:
    st.info("Please upload a CSV file or use the sample dataset.")
    st.stop()

# Column selection (in case auto-detect fails)
st.subheader("📑 Column Selection")
cols = df_raw.columns.tolist()
ts_col = st.selectbox("Select Timestamp Column", options=["None"] + cols, index=0 if "timestamp" in [c.lower() for c in cols] else 0)
hr_col = st.selectbox("Select Heart Rate Column", options=cols, index=1 if len(cols) > 1 else 0)

# Process Data
try:
    df = preprocess(df_raw, ts_col=None if ts_col == "None" else ts_col, hr_col=hr_col)
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.stop()

# Metrics
mean_hr = df["heart_rate"].mean()
min_hr = df["heart_rate"].min()
max_hr = df["heart_rate"].max()
td = time_domain_metrics(df["rr_ms"].values)
stress_label, rationale = estimate_stress(mean_hr, td["rmssd"])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Mean HR", f"{mean_hr:.1f} bpm")
with col2:
    st.metric("SDNN", f"{td['sdnn']:.1f} ms")
with col3:
    st.metric("RMSSD", f"{td['rmssd']:.1f} ms")

badge_class = {"Low": "badge-low", "Medium": "badge-medium", "High": "badge-high"}.get(stress_label, "badge")
st.markdown(f'**Stress Level:** <span class="badge {badge_class}">{stress_label}</span> — {rationale}', unsafe_allow_html=True)

# Plot HR over time
st.subheader("📈 Heart Rate Over Time")
fig = px.line(df, x="timestamp", y="heart_rate", labels={"timestamp": "Time", "heart_rate": "Heart Rate (bpm)"})
st.plotly_chart(fig, use_container_width=True)

# Data Preview
st.subheader("📊 Data Preview")
st.dataframe(df.head(20))
