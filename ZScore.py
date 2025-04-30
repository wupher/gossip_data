import pandas as pd
from scipy.stats import zscore

def zscore_outliner(analysis_data: pd.DataFrame, col: str = "origin_revenue", threshold: float = 2.0):
    group = analysis_data.copy()
    group["zscore"] = zscore(group[col].fillna(0))
    group["anomaly"] = group["zscore"].apply(
        lambda z:"高异常" if z > threshold else ("低异常" if z < - threshold else "正常")
    )
    return group

