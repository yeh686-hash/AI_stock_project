import twstock
import pandas as pd

data = []

# 讀取所有股票
for code in twstock.codes:

    try:

        stock = twstock.codes[code]

        # 只保留4位數股票
        if code.isdigit():

            if len(code) == 4:

                data.append([
                    code,
                    stock.name,
                    stock.type
                ])

    except:

        continue

# 建DataFrame
df = pd.DataFrame(
    data,
    columns=[
        "股票代號",
        "名稱",
        "產業"
    ]
)

# 存CSV
df.to_csv(
    "industry.csv",
    index=False,
    encoding="utf-8-sig"
)

print("產業資料庫建立完成")

print("股票數量:", len(df))