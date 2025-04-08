# What for

用于 KTVME 的 AI 经营助手项目。

生成一个函数用于分析传过来的数据，进行统计，生成描述，返回表格/图表数据。


## prompts

我需要生成一个 Python 函数，这是它的声明。
def compare_analysis(
    data_source1: json,  # 对比组1的数据（必需）
    data_source2: json,  # 对比组2的数据（必需）
    metrics: List[str],                      # 需要对比的核心指标（如["CTR", "ConversionRate"]
    dimensions: List[str],                   # 分组维度（如 ["date"]）
    output_type: str ="table/line折线图"        # 输出图表形式  
) 

这是第一个输入参数 `data_source1` 的示例，它是一个 json 对象:

```json
datasource1 = [
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

```

这是 `data_source2` ： 

```json
datasource2=[
  
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

```
它们都是一组营业数据集合。 pdate 代表每个明细数据的日期(yyyy-MM-dd)格式。 origin_revenue, voucher_box_revenue 代表各种经营数据。

metrics 参数告诉函数，要对具体哪个值进行统计和分析，比如 metrics = ['origin_revenue'] 对应统计 `origin_revenue`。 注意这里 metrics 允许多个值，所以可能不止一个数据需要进行统计。

dimensions = ['pdate'] 这参数是统计的时间，可以为 'pdate' 用于按星期几来进行比较。

如果是按周，将 pdate 转成星期几并比较 data_source1 与 data_source2 的同一星期数据进行比较。并计算同一星期天数的对比，类似以下：

"三月份第一周总营收为120000元，第二周为13000元，同比增长10%。
第一周日均营收为1000元，第二周为14400，同比增长10%。
第一周单日峰值为3月8号29990元，第二周为3月11号xxxy元，"

函数需要计算两组数据的总营收， 日均营收， 峰值。并对 source1, source2 的数据进行对比，计算增长率和回退率。

还要生成类似 >>>
"table":[
            {
                '日期':"周一",
                '第一周':"1000"
                '第2周':"1000"
                 '增长率':"20%"
            }，
            {
                '日期':"周2",
                '第一周':"1000"
                '第2周':"1000"
                '增长率':"20%"
            }，
            {
                '日期':"周3",
                '第一周':"1000"
                '第2周':"1000"
                '增长率':"20%"
            }
>>> 
这样的表格。

### echarts

 "line":[
            // echarts line配置 output_type=line 时返回
            //可能多份配置
            {
                  xAxis: {
                    type: 'category',
                    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
                  },
                  yAxis: {
                    type: 'value'
                  },
                  legend: {
                    data: ['上周', '本周']
                  },
                  series: [
                    {
                      data: [752380, 2760570, 1472260, 1702150, 1566400, 2729400, 1315300],
                      type: 'line',
                      name:"上周",
                      smooth: true
                    },
                    {
                      name:"本周",
                      data: [828570, 968990, 1347980, 1407380, 1893160, 1536000, 1217400],
                      type: 'line',
                      smooth: true
                    }
                  ]
            }     
        ]
