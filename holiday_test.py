import pandas as pd

import func_test
import holiday_util
from holiday_util import merge_holiday

data =  func_test.data_source1

df = pd.DataFrame(data)
df['pdate'] = pd.to_datetime(df['pdate'])
df = df.sort_values(by='pdate').reset_index(drop=True)
df = merge_holiday(df, holiday_util.holiday_df)

print(df)