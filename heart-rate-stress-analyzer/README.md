# Heart Rate & Stress Level Analyzer (Streamlit)

A professional, user-friendly web app to analyze heart rate (HR) data, compute HRV metrics (SDNN, RMSSD, pNN50), and estimate stress level (low/medium/high). Built with **Python + Streamlit**.

## ✨ Features
- Upload **CSV** (timestamp + heart_rate) or use **sample dataset**
- Automatic **preprocessing** & quality checks
- HRV metrics: **SDNN, RMSSD, pNN50**, mean HR, min/max HR
- Simple **stress level estimator** (heuristic, explainable)
- Interactive charts (Plotly): HR over time, RMSSD vs time window
- Export **analysis report (CSV)** and **download plots (PNG)**
- Clean, responsive UI with sidebar controls

## 🗂️ Project Structure
```
heart-rate-stress-analyzer/
├─ app.py
├─ requirements.txt
├─ README.md
├─ .streamlit/
│  └─ config.toml
├─ utils/
│  ├─ hrv.py
│  └─ styling.py
├─ pages/
│  └─ 1_📊_Session_Explorer.py
├─ assets/
│  └─ logo.png
└─ sample_data/
   └─ sample_heart_rate.csv
```

## ▶️ Quick Start
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   ```bash
   streamlit run app.py
   ```

3. **Open in browser** (Streamlit will show the local URL, typically http://localhost:8501)

## 📄 CSV Format
Provide at least these columns:
- `timestamp` — ISO string or any parseable datetime (e.g., `2025-01-01 12:34:56`)
- `heart_rate` — in **bpm** (integers or floats)

Example:
```csv
timestamp,heart_rate
2025-01-01 12:00:00,72
2025-01-01 12:00:05,74
2025-01-01 12:00:10,75
```

> If you only have HR (bpm), we **approximate RR intervals** as `RR(ms) = 60000 / HR`. True HRV from raw RR (IBI) is best, but this approximation works for demonstration and simple monitoring.

## 🧠 Stress Estimation (Explainable Heuristic)
We combine HR and HRV metrics. Defaults (tunable in code):
- If **mean HR > 90** bpm _and_ **RMSSD < 20 ms** → **High Stress**
- Else if **mean HR > 80** bpm _or_ **RMSSD < 30 ms** → **Medium Stress**
- Else → **Low Stress**

This provides an interpretable baseline. You can later drop in a ML model.

## 🧪 Sample Data
We include a synthetic 10-minute dataset at 5-second intervals that simulates normal and mildly elevated HR.

## 🔒 Disclaimer
This app is **not medical advice**. It’s for educational and wellness tracking. Consult healthcare professionals for clinical use.

## 🚀 Deploy
- **Streamlit Cloud**: push this repo to GitHub and deploy in minutes.
- **Docker** (optional):
  ```bash
  docker build -t hr-stress-analyzer .
  docker run -p 8501:8501 hr-stress-analyzer
  ```

## 🛠️ Extend
- Add device ingestion (BLE from wearables / Raspberry Pi HTTP POST)
- Train a classifier (scikit-learn) on labeled stress data
- Store sessions in SQLite + authentication
```

