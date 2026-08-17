---
name: brooks-priceaction
description: "Al Brooks price-action day trading. Read every bar in context: trend bars vs doji, with-trend pullbacks, failed breaks, and the 3 push / wedge reversals. Intraday 1-min/5-min. No indicators — pure bar structure + market context."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, day-trading, al-brooks, price-action, candles, trend-bars, pullback, intraday]
---

# Al Brooks — Price Action (v1.0)

> **Goal (day trade):** trade the *context*, not the indicator. Every bar is a battle
> between bulls and bears; read trend bars (big bodies, closes at extremes) vs doji, and
> trade with-trend pullbacks to the moving average, or reversals at climaxes.

## 0. Plain English
Forget RSI/MACD. Look at the candles: a strong bar closing on its high = bulls won that
bar. A string of those = uptrend → buy the *pullback* to the average. A bar that fails to
make a new high after a strong run = exhaustion → fade it.

## 1. Core rules
- **Trend bar** = body ≥ 50% of range, closes near high (bull) / low (bear).
- **With-trend pullback:** in an uptrend, buy when a bear pullback bar fails and the next
  bar closes above its midpoint (signal bar → entry above its high).
- **Reversal:** 2-3 pushes up with shrinking bodies / long wicks = wedge → short the break.
- **Moving average (e.g. EMA 20):** magnet; pullbacks test it; it defines trend direction.
- **Context > signal:** a long signal in a bear trend is a scalp, not a swing.

## 2. Quant screen (`references/priceaction.py`)
Scores the latest 1-min bars: trend strength (trend-bar ratio), MA slope, last signal
(pullback-long / pullback-short / climax-reversal), and whether price is at the MA.

## 3. Do / Don't
**DO:** trade with the 20-MA trend; scale in at pullbacks; respect context (trend vs range).
**DON'T:** trade every signal bar blindly; fade a strong trend; ignore the higher timeframe.

## 4. Script
```bash
cd <skill>/references
python3 priceaction.py NVDA --date 2026-08-17 --tf 1
python3 priceaction.py AAPL --tf 5
```

## 5. Reality notes
- Pure structure: the script flags *setups*, not entries — Brooks insists you read the
  bar's location in the trend. Output is a checklist, not an auto-order.
- Uses EMA20 on 1/5-min bars from yfinance.

## 6. Pitfalls
- ❌ Treating every signal bar as a trade (context is everything).
- ❌ Chasing in a trading range (signals fail).
- ❌ Over-fitting bar math; Brooks' edge is *reading*, the script is a crutch.

---
*Compiled 2026-08-17 from Al Brooks "Reading Price Charts Bar by Bar". Not financial advice.*
