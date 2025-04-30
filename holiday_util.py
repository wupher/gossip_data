import pandas as pd

holiday_df = pd.read_csv("./data/chinese_holidays.csv")
holiday_df["date"] = pd.to_datetime(holiday_df["date"])

def merge_holiday(original_df: pd.DataFrame, holiday_data: pd.DataFrame) -> pd.DataFrame:
    """
    Merge original dataframe with holiday dataframe to add Chinese holiday information.

    Args:
        original_df: Input dataframe containing date column 'pdate'
        holiday_data: Holiday reference dataframe containing date and holiday information

    Returns:
        pd.DataFrame: Merged dataframe with holiday information
    """
    result_df = pd.merge(
        original_df,
        holiday_data[["date", "weekday", "description"]],
        left_on='pdate',
        right_on='date',
        how='left'
    )
    result_df = result_df.drop(columns=["date"])
    return result_df


