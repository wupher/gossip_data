import pandas as pd

import holiday_util
from holiday_util import merge_holiday

data =  [
  {
    "pdate": "2025-03-17",
    "origin_revenue": 752380.00,
    "voucher_box_revenue": 65580.00
  },
  {
    "pdate": "2025-03-18",
    "origin_revenue": 2760570.00,
    "voucher_box_revenue": 94570.00
  },
  {
    "pdate": "2025-03-19",
    "origin_revenue": 1472260.00,
    "voucher_box_revenue": 49160.00
  },
  {
    "pdate": "2025-03-20",
    "origin_revenue": 1702150.00,
    "voucher_box_revenue": 69350.00
  },
  {
    "pdate": "2025-03-21",
    "origin_revenue": 1566400.00,
    "voucher_box_revenue": 59800.00
  },
  {
    "pdate": "2025-03-22",
    "origin_revenue": 2729400.00,
    "voucher_box_revenue": 137800.00
  },
  {
    "pdate": "2025-03-23",
    "origin_revenue": 1315300.00,
    "voucher_box_revenue": 145000.00
  }
]

df = pd.DataFrame(data)
df['pdate'] = pd.to_datetime(df['pdate'])
df = df.sort_values(by='pdate').reset_index(drop=True)
df = merge_holiday(df, holiday_util.holiday_df)

print(df)