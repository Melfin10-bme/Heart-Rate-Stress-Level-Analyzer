import numpy as np
import pandas as pd

# Convert HR (bpm) → RR intervals (ms)
def bpm_to_rr_ms(hr_bpm: np.ndarray) -> np.ndarray:
    hr_bpm = np.asarray(hr_bpm, dtype=float)
    hr_bpm = np.where(hr_bpm <= 0, np.nan, hr_bpm)
    return 60000.0 / hr_bpm  # ms

# HRV time-domain metrics
def time_domain_metrics(rr_ms: np.ndarray) -> dict:
    rr = np.asarray(rr_ms, dtype=float)
    rr = rr[~np.isnan(rr)]
    if rr.size < 2:
        return dict(mean_rr=np.nan, sdnn=np.nan, rmssd=np.nan, pnn50=np.nan)

    diff = np.diff(rr)
    sdnn = np.std(rr, ddof=1)
    rmssd = np.sqrt(np.mean(diff**2))
    nn50 = np.sum(np.abs(diff) > 50.0)  # >50 ms
    pnn50 = 100.0 * nn50 / diff.size

    return dict(
        mean_rr=float(np.mean(rr)),
        sdnn=float(sdnn),
        rmssd=float(rmssd),
        pnn50=float(pnn50),
    )

# Stress estimation
def estimate_stress(mean_hr: float, rmssd: float) -> tuple[str, str]:
    if np.isnan(mean_hr) or np.isnan(rmssd):
        return "Unknown", "Insufficient data to estimate stress."
    if mean_hr > 90 and rmssd < 20:
        return "High", "High HR and very low RMSSD suggest elevated stress."
    if (mean_hr > 80) or (rmssd < 30):
        return "Medium", "Moderately elevated HR or low RMSSD."
    return "Low", "Normal HR and healthy RMSSD."

# Preprocessing with column detection
def preprocess(df: pd.DataFrame, ts_col: str = None, hr_col: str = None) -> pd.DataFrame:
    df = df.copy()

    # Guess timestamp column if not provided
    if ts_col is None:
        for c in df.columns:
            if "time" in c.lower() or "date" in c.lower():
                ts_col = c
                break

    # Guess heart rate column if not provided
    if hr_col is None:
        for c in df.columns:
            if c.lower() in ["heart_rate", "hr", "bpm", "heartrate"]:
                hr_col = c
                break

    # If no timestamp column, create synthetic timeline
    if ts_col is None:
        df["timestamp"] = pd.date_range("2025-01-01", periods=len(df), freq="5S")
    else:
        df["timestamp"] = pd.to_datetime(df[ts_col], errors="coerce")

    # Require HR column
    if hr_col is None:
        raise ValueError("No valid heart rate column found. Please name it 'heart_rate', 'hr', or 'bpm'.")

    df["heart_rate"] = pd.to_numeric(df[hr_col], errors="coerce")

    # Clean & sort
    df = df.dropna(subset=["timestamp", "heart_rate"]).sort_values("timestamp").reset_index(drop=True)

    # Add RR interval column
    df["rr_ms"] = bpm_to_rr_ms(df["heart_rate"].values)

    return df
