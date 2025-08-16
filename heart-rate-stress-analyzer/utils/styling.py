import streamlit as st

def inject_css():
    st.markdown(
        """
        <style>
        .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        .metric-card {
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.06);
            background: #fff;
            border: 1px solid #eef1f6;
        }
        .metric-title { font-size: 0.9rem; color: #64748B; }
        .metric-value { font-size: 1.6rem; font-weight: 700; color: #0F172A; }
        .badge {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-weight: 600;
        }
        .badge-low { background: #ECFDF5; color: #065F46; }
        .badge-medium { background: #FEF3C7; color: #92400E; }
        .badge-high { background: #FEE2E2; color: #991B1B; }
        </style>
        """,
        unsafe_allow_html=True
    )
