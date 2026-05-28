import os
import pandas as pd
import ta

results = []

files = os.listdir("stock_data")

print("開始真實隔日回測...\n")

for file in files:

    try:

        # 讀資料
        stock = pd.read_csv(
            f"stock_data/{file}"
        )

        stock_id = file.replace(
            ".csv",
            ""
        )

        # 收盤價
        close = pd.to_numeric(
            stock["Close"],
            errors="coerce"
        )

        # 成交量
        volume = pd.to_numeric(
            stock["Volume"],
            errors="coerce"
        )

        # 資料不足
        if len(close) < 30:

            continue

        # ===== 關鍵修正 =====
        # 所有選股條件只看到昨天

        close_yesterday = close.iloc[:-1]

        volume_yesterday = volume.iloc[:-1]

        # 今天價格
        today_close = close.iloc[-1]

        # 昨天價格
        yesterday_close = close.iloc[-2]

        # 真正隔日報酬
        next_day_return = (
            (today_close - yesterday_close)
            / yesterday_close
        ) * 100

        # 昨天成交量
        latest_volume = volume_yesterday.iloc[-1]

        volume_in_thousand = (
            latest_volume / 1000
        )

        # 流動性
        if volume_in_thousand < 500:

            continue

        score = 0

        # RSI
        latest_rsi = ta.momentum.RSIIndicator(
            close=close_yesterday
        ).rsi().iloc[-1]

        # 均量
        volume_5ma = (
            volume_yesterday
            .tail(5)
            .mean()
        )

        volume_20ma = (
            volume_yesterday
            .tail(20)
            .mean()
        )

        # 均線
        ma5 = (
            close_yesterday
            .rolling(5)
            .mean()
            .iloc[-1]
        )

        ma20 = (
            close_yesterday
            .rolling(20)
            .mean()
            .iloc[-1]
        )

        # 20日高點
        highest_20 = (
            close_yesterday
            .tail(20)
            .max()
        )

        # 昨天收盤
        latest_close = (
            close_yesterday.iloc[-1]
        )

        # 5日漲幅
        price_5days_ago = (
            close_yesterday.iloc[-6]
        )

        change_percent = (
            (latest_close - price_5days_ago)
            / price_5days_ago
        ) * 100

        # ===== 評分 =====

        # 爆量
        if latest_volume > volume_5ma * 2:

            score += 5

        # 量縮整理
        if volume_5ma < volume_20ma:

            score += 4

        # 箱型突破
        if latest_close >= highest_20:

            score += 4

        # 均線轉強
        if ma5 > ma20:

            score += 2

        # RSI
        if latest_rsi < 75:

            score += 2

        # 漲太多扣分
        if change_percent > 20:

            score -= 4

        # 存結果
        results.append([
            stock_id,
            score,
            round(next_day_return, 2)
        ])

    except:

        continue

# 排序
results.sort(
    key=lambda x: x[1],
    reverse=True
)

# 前30名
top30 = results[:30]

win_count = 0

total_return = 0

print("===== 真實回測結果 =====\n")

for r in top30:

    stock_id = r[0]

    score = r[1]

    ret = r[2]

    total_return += ret

    if ret > 0:

        win_count += 1

    print(
        f"{stock_id} "
        f"分數:{score} "
        f"隔日報酬:{ret}%"
    )

# 統計
win_rate = (
    win_count / len(top30)
) * 100

avg_return = (
    total_return / len(top30)
)

print("\n===== 真實統計 =====\n")

print(
    f"勝率: {round(win_rate,2)}%"
)

print(
    f"平均報酬: {round(avg_return,2)}%"
)