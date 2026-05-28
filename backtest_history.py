import os
import pandas as pd
import ta

# ===== 設定 =====

TOP_N = 30

BACKTEST_DAYS = 60

MIN_VOLUME = 500

# ===== 讀資料 =====

files = os.listdir("stock_data")

daily_results = []

print(
    f"開始 {BACKTEST_DAYS} 天歷史回測...\n"
)

# ===== 每一天回測 =====

for day_offset in range(
    BACKTEST_DAYS,
    0,
    -1
):

    results = []

    # 每檔股票
    for file in files:

        try:

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
            if len(close) < 120:

                continue

            # ===== 切歷史 =====
            # 不能偷看未來

            end_idx = -day_offset

            close_hist = close.iloc[
                :end_idx
            ]

            volume_hist = volume.iloc[
                :end_idx
            ]

            # 如果切完太短
            if len(close_hist) < 30:

                continue

            # ===== 隔日報酬 =====

            today_close = close.iloc[
                end_idx
            ]

            yesterday_close = close.iloc[
                end_idx - 1
            ]

            next_day_return = (
                (today_close - yesterday_close)
                / yesterday_close
            ) * 100

            # ===== 流動性 =====

            latest_volume = (
                volume_hist.iloc[-1]
            )

            volume_in_thousand = (
                latest_volume / 1000
            )

            if volume_in_thousand < MIN_VOLUME:

                continue

            # ===== 評分 =====

            score = 0

            # RSI
            latest_rsi = (
                ta.momentum
                .RSIIndicator(
                    close=close_hist
                )
                .rsi()
                .iloc[-1]
            )

            # 均量
            volume_5ma = (
                volume_hist
                .tail(5)
                .mean()
            )

            volume_20ma = (
                volume_hist
                .tail(20)
                .mean()
            )

            # 均線
            ma5 = (
                close_hist
                .rolling(5)
                .mean()
                .iloc[-1]
            )

            ma20 = (
                close_hist
                .rolling(20)
                .mean()
                .iloc[-1]
            )

            # 20日高點
            highest_20 = (
                close_hist
                .tail(20)
                .max()
            )

            # 最新價格
            latest_close = (
                close_hist.iloc[-1]
            )

            # 5日漲幅
            price_5days_ago = (
                close_hist.iloc[-6]
            )

            change_percent = (
                (latest_close - price_5days_ago)
                / price_5days_ago
            ) * 100

            # ===== 打分 =====

            # 爆量
            if latest_volume > volume_5ma * 2:

                score += 5

            # 量縮整理
            if volume_5ma < volume_20ma:

                score += 4

            # 突破
            if latest_close >= highest_20:

                score += 4

            # 均線
            if ma5 > ma20:

                score += 2

            # RSI
            if latest_rsi < 75:

                score += 2

            # 過熱扣分
            if change_percent > 20:

                score -= 4

            # ===== 存結果 =====

            results.append([
                stock_id,
                score,
                round(next_day_return, 2)
            ])

        except:

            continue

    # ===== 每日排序 =====

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    top_n = results[:TOP_N]

    # ===== 每日統計 =====

    win_count = 0

    total_return = 0

    for r in top_n:

        ret = r[2]

        total_return += ret

        if ret > 0:

            win_count += 1

    # 平均報酬
    avg_return = (
        total_return / len(top_n)
    )

    # 勝率
    win_rate = (
        win_count / len(top_n)
    ) * 100

    daily_results.append([
        avg_return,
        win_rate
    ])

    print(
        f"Day {-day_offset}: "
        f"勝率 {round(win_rate,2)}% "
        f"| 平均報酬 {round(avg_return,2)}%"
    )

# ===== 最終統計 =====

all_returns = [
    x[0]
    for x in daily_results
]

all_win_rates = [
    x[1]
    for x in daily_results
]

final_avg_return = (
    sum(all_returns)
    / len(all_returns)
)

final_avg_winrate = (
    sum(all_win_rates)
    / len(all_win_rates)
)

# 複利概念（簡化）
cumulative_return = 1

for r in all_returns:

    cumulative_return *= (
        1 + r / 100
    )

cumulative_return = (
    (cumulative_return - 1)
    * 100
)

print("\n========== 最終結果 ==========\n")

print(
    f"回測天數: {BACKTEST_DAYS}"
)

print(
    f"每日平均勝率: "
    f"{round(final_avg_winrate,2)}%"
)

print(
    f"每日平均報酬: "
    f"{round(final_avg_return,2)}%"
)

print(
    f"60天累積報酬: "
    f"{round(cumulative_return,2)}%"
)