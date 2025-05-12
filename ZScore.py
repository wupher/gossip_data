import pandas as pd
from scipy.stats import zscore

def zscore_outliner(analysis_data: pd.DataFrame, col: str = "origin_revenue", threshold: float = 2.0):
    group = analysis_data.copy()
    group["zscore"] = zscore(group[col].fillna(0))
    group["anomaly"] = group["zscore"].apply(
        lambda z:"高异常" if z > threshold else ("低异常" if z < - threshold else "正常")
    )
    return group

def generate_report(group: pd.DataFrame, col: str = "origin_revenue"):
    total_records = len(group)
    anomalies = group[group["anomaly"] != "正常"]
    anomaly_count = len(anomalies)
    anomaly_percentage = (anomaly_count / total_records) * 100 if total_records > 0 else 0
    report = f"检测到 {anomaly_count} 笔异常数据，占比 {anomaly_percentage:.2f}%\n"
    if anomaly_count > 0:
        report += "异常详情：\n"
        for _, row in anomalies.iterrows():
            report += f"{row['pdate'].strftime('%Y-%m-%d')}，{col} {row[col]}，{row['anomaly']}\n"

    return report

