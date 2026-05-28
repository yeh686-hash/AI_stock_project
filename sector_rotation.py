import pandas as pd

# ===== 讀取歷史 =====

df = pd.read_csv(
    "sector_history.csv"
)

# ===== 日期排序 =====

dates = sorted(
    df["日期"].unique()
)

# ===== 至少需要兩天 =====

if len(dates) < 2:

    print("歷史資料不足")

    exit()

today = dates[-1]

yesterday = dates[-2]

# ===== 今天 =====

today_df = df[
    df["日期"] == today
]

# ===== 昨天 =====

yesterday_df = df[
    df["日期"] == yesterday
]

# ===== 建立昨天字典 =====

yesterday_map = {}

for _, row in yesterday_df.iterrows():

    yesterday_map[
        row["族群"]
    ] = row["平均分數"]

# ===== 分析升溫 =====

results = []

for _, row in today_df.iterrows():

    sector = row["族群"]

    today_score = row["平均分數"]

    yesterday_score = yesterday_map.get(
        sector,
        0
    )

    diff = round(
        today_score - yesterday_score,
        2
    )

    results.append([

        sector,
        yesterday_score,
        today_score,
        diff

    ])

# ===== DataFrame =====

result_df = pd.DataFrame(

    results,

    columns=[

        "族群",
        "昨日分數",
        "今日分數",
        "變化"

    ]

)

# ===== 排序 =====

result_df = result_df.sort_values(

    by="變化",

    ascending=False

)

# ===== 顯示 =====

print("\n===== 主流升溫排行 =====\n")

print(result_df.head(20))