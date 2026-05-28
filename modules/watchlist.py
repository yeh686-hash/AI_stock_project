import pandas as pd
from tabulate import tabulate

# ===== 讀取選股結果 =====

df = pd.read_csv(
    "選股結果.csv"
)

# ===== 排除其他 =====

df = df[
    df["族群"] != "其他"
]

# ===== 排除高風險 =====

df = df[
    df["風險"] != "高"
]

# ===== 成交值過濾 =====

df = df[
    df["成交值"] > 100000000
]

# ===== 排序 =====

df = df.sort_values(

    by=[
        "分數",
        "成交值"
    ],

    ascending=False

)

# ===== 前15檔 =====

watch_df = df.head(15)

# ===== AI等級 =====

grades = []

# ===== AI評語 =====

comments = []

for _, row in watch_df.iterrows():

    # ===== AI等級 =====

    grade = "B"

    if (
        row["分數"] >= 30
        and
        row["成交值"] > 3000000000
        and
        row["RSI"] < 75
    ):

        grade = "S"

    elif row["分數"] >= 25:

        grade = "A"

    grades.append(grade)

    # ===== AI評語 =====

    text = ""

    # ===== 主流強度 =====

    if row["分數"] >= 30:

        text += "高分強勢股 "

    elif row["分數"] >= 25:

        text += "主流觀察股 "

    # ===== RSI =====

    if row["RSI"] >= 75:

        text += "短線過熱 "

    elif row["RSI"] >= 65:

        text += "資金偏強 "

    # ===== 成交值 =====

    if row["成交值"] > 5000000000:

        text += "法人資金活躍 "

    elif row["成交值"] > 1000000000:

        text += "量能健康 "

    # ===== AI族群描述 =====

    if row["族群"] == "高速傳輸":

        text += "AI傳輸主流 "

    elif row["族群"] == "矽光子":

        text += "CPO題材 "

    elif row["族群"] == "AI伺服器":

        text += "AI核心受惠 "

    elif row["族群"] == "重電":

        text += "重電趨勢股 "

    elif row["族群"] == "BBU":

        text += "備援電力題材 "

    comments.append(
        text
    )

# ===== 新增欄位 =====

watch_df["AI等級"] = grades

watch_df["AI評語"] = comments

print("\n===== AI觀察名單 =====\n")

# ===== 對齊表格 =====

table = tabulate(

    watch_df[[

        "AI等級",
        "代號",
        "名稱",
        "族群",
        "分數",
        "成交值",
        "RSI",
        "AI評語"

    ]],

    headers="keys",

    tablefmt="grid",

    showindex=False,

    stralign="center",

    numalign="center"

)

print(table)

# ===== 輸出 =====

watch_df.to_csv(

    "watchlist.csv",

    index=False,

    encoding="utf-8-sig"

)

print("\nwatchlist.csv 已輸出")