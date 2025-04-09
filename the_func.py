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
    # 预处理：时间、星期、自然周
    def preprocess(data):
        df = pd.DataFrame(data)
        df['pdate'] = pd.to_datetime(df['pdate'])
        df = df.sort_values(by='pdate').reset_index(drop=True)
        df['weekday'] = df['pdate'].dt.dayofweek
        df['weekday_name'] = df['pdate'].dt.day_name()
        df['year_week'] = df['pdate'].dt.strftime('%G-W%V')
        df['day_number'] = df.index + 1  # 月维度用
        return df

    def extract_single_week(df):
        all_weeks = df['year_week'].unique()
        latest_week = sorted(all_weeks)[-1]
        df_week = df[df['year_week'] == latest_week]
        return df_week, latest_week

    def get_week_date_range_label(df):
        start = df['pdate'].min().strftime('%Y-%m-%d')
        end = df['pdate'].max().strftime('%Y-%m-%d')
        return f"{start} ~ {end}"

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

    def extract_day_label(date_str):
        return pd.to_datetime(date_str).strftime("%-m月%-d号")

    def generate_report(metric_name, summary1, summary2, week_label1, week_label2):
        total1 = summary1["total"]
        total2 = summary2["total"]
        avg1 = summary1["daily_avg"]
        avg2 = summary2["daily_avg"]
        peak_val1 = summary1["peak_value"]
        peak_val2 = summary2["peak_value"]
        peak_day1 = extract_day_label(summary1["peak_day"])
        peak_day2 = extract_day_label(summary2["peak_day"])

        total_growth = growth_rate(total2, total1)
        avg_growth = growth_rate(avg2, avg1)
        peak_growth = growth_rate(peak_val2, peak_val1)

        return (
            f"{metric_name}方面：\n"
            f"{week_label1} 总营收为 {int(total1):,} 元，{week_label2} 为 {int(total2):,} 元，增长率为 {total_growth}。\n"
            f"{week_label1} 日均营收为 {int(avg1):,} 元，{week_label2} 为 {int(avg2):,} 元，增长率为 {avg_growth}。\n"
            f"{week_label1} 单日峰值为 {peak_day1} {int(peak_val1):,} 元，{week_label2} 为 {peak_day2} {int(peak_val2):,} 元，增长率为 {peak_growth}。\n"
        )

    def generate_echarts_line(metric, table_data, first_label, second_label):
        x_data = [row["日期"] for row in table_data]
        first_data = [row["第一组"] for row in table_data]
        second_data = [row["第二组"] for row in table_data]

        return [{
            "xAxis": {
                "type": "category",
                "data": x_data
            },
            "yAxis": {
                "type": "value"
            },
            "legend": {
                "data": [first_label, second_label]
            },
            "series": [
                {
                    "name": first_label,
                    "data": first_data,
                    "type": "line",
                    "smooth": True
                },
                {
                    "name": second_label,
                    "data": second_data,
                    "type": "line",
                    "smooth": True
                }
            ]
        }]

    # 主流程
    is_month_mode = dimensions == ["month"]

    df1 = preprocess(data_source1)
    df2 = preprocess(data_source2)

    if is_month_mode:
        first_df, second_df = df1, df2
    else:
        df1, _ = extract_single_week(df1)
        df2, _ = extract_single_week(df2)
        is_df1_first = pd.to_datetime(df1['pdate'].min()) <= pd.to_datetime(df2['pdate'].min())
        first_df, second_df = (df1, df2) if is_df1_first else (df2, df1)

    first_label = get_week_date_range_label(first_df)
    second_label = get_week_date_range_label(second_df)

    weekday_map = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    output = {}

    for metric in metrics:
        summary1 = calculate_summary(first_df, metric)
        summary2 = calculate_summary(second_df, metric)

        # 汇总输出
        output[f"{metric}_summary"] = {
            "第一组时间范围": first_label,
            "第二组时间范围": second_label,
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

        # 表格数据构建
        table_data = []

        if is_month_mode:
            max_days = max(len(first_df), len(second_df))
            for i in range(max_days):
                label = f"第{i+1}天"
                val1 = first_df.iloc[i][metric] if i < len(first_df) else 0
                val2 = second_df.iloc[i][metric] if i < len(second_df) else 0
                table_data.append({
                    "日期": label,
                    "第一组": round(val1, 2),
                    "第二组": round(val2, 2),
                    "增长率": growth_rate(val2, val1)
                })
        else:
            for i in range(7):
                label = weekday_map[i]
                val1 = first_df[first_df['weekday'] == i][metric].sum()
                val2 = second_df[second_df['weekday'] == i][metric].sum()
                table_data.append({
                    "日期": label,
                    "第一组": round(val1, 2),
                    "第二组": round(val2, 2),
                    "增长率": growth_rate(val2, val1)
                })

        output[f"{metric}_table"] = table_data
        output[f"{metric}_tablemd"] = build_markdown_table(table_data)
        output[f"{metric}_report"] = generate_report(metric, summary1, summary2, first_label, second_label)

        if output_type == "line":
            output[f"{metric}_line"] = generate_echarts_line(metric, table_data, first_label, second_label)

    return output