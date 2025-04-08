import json
from typing import List

import pandas as pd


def compare_analysis(
    data_source1: json,
    data_source2: json,
    metrics: List[str],
    dimensions: List[str],
    output_type: str = "table"
):
    def preprocess(data):
        df = pd.DataFrame(data)
        df['pdate'] = pd.to_datetime(df['pdate'])
        df['weekday'] = df['pdate'].dt.dayofweek  # 周一=0, 周日=6
        df['weekday_name'] = df['pdate'].dt.day_name()
        return df

    def calculate_summary(df, metric):
        total = df[metric].sum()
        daily_avg = df[metric].mean()
        peak_value = df[metric].max()
        peak_day = df.loc[df[metric].idxmax(), 'pdate']
        return {
            "total": total,
            "daily_avg": daily_avg,
            "peak_value": peak_value,
            "peak_day": peak_day.strftime('%Y-%m-%d')
        }

    def growth_rate(new, old):
        if old == 0:
            return "N/A"
        return f"{((new - old) / old * 100):.2f}%"

    def build_markdown_table(table_data):
        header = "| 日期 | 第一组 | 第二组 | 增长率 |\n"
        separator = "|------|--------|--------|--------|\n"
        rows = ""
        for row in table_data:
            rows += f"| {row['日期']} | {row['第一组']} | {row['第二组']} | {row['增长率']} |\n"
        return header + separator + rows

    df1 = preprocess(data_source1)
    df2 = preprocess(data_source2)

    output = {}

    for metric in metrics:
        # 汇总统计信息
        summary1 = calculate_summary(df1, metric)
        summary2 = calculate_summary(df2, metric)

        output[f"{metric}_summary"] = {
            "组1总营收": summary1['total'],
            "组2总营收": summary2['total'],
            "总营收增长率": growth_rate(summary2['total'], summary1['total']),
            "组1日均营收": summary1['daily_avg'],
            "组2日均营收": summary2['daily_avg'],
            "日均营收增长率": growth_rate(summary2['daily_avg'], summary1['daily_avg']),
            "组1峰值": f"{summary1['peak_value']}（{summary1['peak_day']}）",
            "组2峰值": f"{summary2['peak_value']}（{summary2['peak_day']}）",
            "峰值增长率": growth_rate(summary2['peak_value'], summary1['peak_value']),
        }

        if output_type == "table":
            # 按周几统计
            weekday_table = []
            weekday_map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

            for i in range(7):
                value1 = df1[df1['weekday'] == i][metric].sum()
                value2 = df2[df2['weekday'] == i][metric].sum()
                row = {
                    "日期": weekday_map[i],
                    "第一组": round(value1, 2),
                    "第二组": round(value2, 2),
                    "增长率": growth_rate(value2, value1)
                }
                weekday_table.append(row)

            output[f"{metric}_table"] = weekday_table
            md_table = build_markdown_table(weekday_table)
            output[f"{metric}_tablemd"] = md_table

    return output