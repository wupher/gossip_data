import pandas as pd
from statsmodels.tsa.seasonal import STL


def stl_outliner(analysis_data: pd.DataFrame, col: str = "origin_revenue", threshold: float = 1.2, period: int = 7):
    """
    根据 STL 算法检测异常数据
    :param analysis_data: pd.DataFrame，输入数据
    :param col: str，要分析的列名
    :param threshold: float，异常值的阈值
    :param period: int，STL 分解的周期长度，默认7
    :return: 带有标记异常数据的 DataFrame
    """
    group = analysis_data.copy()
    stl = STL(group[col].fillna(0), period=period, robust=True)
    result = stl.fit()

    # 获取残差部分
    group["residual"] = result.resid
    # 根据阈值标记异常
    group["anomaly"] = group["residual"].apply(
        lambda resid: "高异常" if resid > threshold else ("低异常" if resid < -threshold else "正常")
    )
    return group

