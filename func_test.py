from pprint import pprint

from the_func import compare_analysis

data_source1 =  [
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


data_source2 = [
{
    "pdate": "2025-03-10",
    "origin_revenue": 828570.00,
    "voucher_box_revenue": 83770.00
  },
  {
    "pdate": "2025-03-11",
    "origin_revenue": 968990.00,
    "voucher_box_revenue": 84590.00
  },
  {
    "pdate": "2025-03-12",
    "origin_revenue": 1347980.00,
    "voucher_box_revenue": 29980.00
  },
  {
    "pdate": "2025-03-13",
    "origin_revenue": 1407380.00,
    "voucher_box_revenue": 84780.00
  },
  {
    "pdate": "2025-03-14",
    "origin_revenue": 1893160.00,
    "voucher_box_revenue": 101760.00
  },
  {
    "pdate": "2025-03-15",
    "origin_revenue": 1536000.00,
    "voucher_box_revenue": 134000.00
  },
  {
    "pdate": "2025-03-16",
    "origin_revenue": 1217400.00,
    "voucher_box_revenue": 188200.00
  }
]

result = compare_analysis(data_source1, data_source2, metrics=["origin_revenue", 'voucher_box_revenue'],
                          dimensions=["month"], output_type="line")
pprint(result)

