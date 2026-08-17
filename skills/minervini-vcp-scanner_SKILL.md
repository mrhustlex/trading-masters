---
name: minervini-vcp-scanner
description: "Scan US stocks with Mark Minervini's SEPA / Volatility Contraction Pattern (VCP) methodology to build a ranked breakout watchlist. yfinance-based, real VCP detection, PE/fPE output, optional auto chart generation. Designed so a layman can replicate the strategy end-to-end."
version: 3.0.0
author: Hei
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [trading, stocks, minervini, vcp, momentum, screener, sepa, swing-trading]
---

# Minervini VCP Scanner — Layman's Replication Guide (v3.0)

> **Goal of this skill:** let ANYONE (zero trading background) find the exact kind of
> stock Mark Minervini buys, understand WHY it qualifies, and know the precise
> buy / stop / target / position-size rules — then run the included scanner to
> generate a watchlist + charts they can verify themselves.

---

## 0. What is this strategy in plain English?

Mark Minervini is a US Investing Champion who turned a small account into millions
using one repeatable idea: **buy the strongest stocks at the exact moment they
finish "coiling" and break out to new highs — with a tiny, predefined stop.**

The whole method rests on three ideas a beginner can hold in their head:

1. **Trend first.** Only trade stocks already going up hard (Stage 2). Never catch
   falling knives (Stage 4) or dead sideways stocks (Stage 1).
2. **Contraction = energy building.** The best breakouts come after volatility
   *shrinks* — a tight, low-volume pause near the highs. This is the VCP.
3. **Risk is fixed, upside is open.** You ALWAYS know your exit (stop ≈ 7% below
   entry) BEFORE you buy. You never risk more than ~1–2% of your account on one
   trade. The win rate can be <50% and you still make money (math below).

> ⚠️ **This is education, not financial advice.** Past performance ≠ future results.
> Minervini himself lost money early; the edge comes from discipline + repetition,
> not from any single pick.

---

## 1. The people / sources (verified)

- **Mark Minervini** — author of *Think and Trade Like a Champion* (2013) and
  *Trade Like a Stock Market Wizard* (2013). 1997 U.S. Investing Champion (+155% in
  1 year). Method = **SEPA** (Specific Entry Point Analysis) + **VCP**.
- **J Law (超績投資客 @jlawstock)** — Hong Kong trader who teaches VCP in Cantonese
  on YouTube (playlist "technical analysis", ~700K views). His screencast is the
  practical, example-driven companion to Minervini's books and is why this skill's
  notes were originally written in Chinese. **Key J Law adjustment:** prefer
  *Sales (revenue) growth acceleration* over EPS, because fast-growth names
  (biotech, software) often have no earnings yet but revenue is always rising.
- Primary references: Minervini's two books; Stan Weinstein *Secrets for Profiting
  in Bull and Bear Markets* (the 4-stage model); William O'Neil CAN SLIM (the
  pivot/breakout concept). The Deepvue "Master the VCP" webinar (YouTube
  `j65mVPySzng`) is a good free visual walkthrough.

---

## 2. The mental model — Stage analysis (Weinstein)

A stock's life cycles through 4 stages. **You only ever buy in Stage 2.**

| Stage | What it looks like | What you do |
|-------|-------------------|-------------|
| 1 | Flat, low-volume base (bottoming) | Wait |
| **2** | **Higher highs/lows, price above rising MAs** | ✅ **BUY here** |
| 3 | Goes sideways at the top, smart money sells | Sell / avoid |
| 4 | Lower lows, MAs rolling over | Short / stay out |

**How to SEE Stage 2 on a chart (no math needed):**
- The 3 lines (50-day, 150-day, 200-day moving averages) are all **sloping up**.
- They stack in order: **price > 50-day > 150-day > 200-day** (shortest on top).
- Pullbacks are *shallow* and find support at the 50-day line, then resume up.

---

## 3. The Trend Template — 8 yes/no questions (the filter)

Before ANY pattern talk, a stock must pass ALL 8. This alone removes ~95% of stocks.

For each, compute the simple (not exponential) moving averages:
`MA50, MA150, MA200` = average closing price of the last 50 / 150 / 200 days.
Also need: `price` (today's close), `hi52` / `lo52` (highest / lowest close in 1 year).

| # | Rule | Plain check |
|---|------|-------------|
| 1 | price > MA50 | trading above short-term average |
| 2 | price > MA150 | above medium-term average |
| 3 | price > MA200 | above long-term average |
| 4 | MA50 > MA150 | short-term line above medium |
| 5 | MA150 > MA200 | medium line above long-term |
| 6 | MA200 turning up ≥1 month | long-term line sloping up |
| 7 | price ≥ 1.30 × lo52 | at least 30% above its 52-wk low |
| 8 | price ≥ 0.75 × hi52 | within 25% of its 52-wk high (RS ≥70, ideally 90+) |

If ANY is "no" → reject. Survivors are true Stage-2 leaders.

> **In the code**, rule 6 is approximated as `price > price 21 days ago` (price up
> over the last month) because 1-year daily data makes the 200DMA-rising test
> noisy. It's a practical proxy, not the textbook wording — noted so you know.

### RS (Relative Strength) rating
- Minervini cutoff: **RS ≥ 89** (strict: 96). Large-caps: lower to 85.
- RS here = the stock's 52-week return ranked against the market (SPY).
  **Approx formula in code:** `RS = clamp(50 + 50 × (stock_52w_return) / (SPY_52w_return), 1, 99)`.
- ⚠️ **RS ≠ RSI.** RSI is "overbought/oversold" (0–100, different math). Don't confuse them.
- ⚠️ Because the formula pins strong megacaps to 99, **RS alone does NOT rank names** —
  use it only as a pass/fail gate (≥89), then rank by VCP + proximity to pivot.

---

## 4. VCP — the Volatility Contraction Pattern (the entry trigger)

A VCP is a base where pullbacks get *smaller and smaller* — supply is being absorbed.

**Visually (what your eye looks for):**
- Price rallies, then pulls back **−20 to −30%**, then **−10 to −15%**, then **−5 to −8%**.
- Each dip is shallower than the last → volatility is *contracting*.
- Volume *dries up* on the dips; the final tight area has tiny candles.
- The **pivot** = the highest price in that base (the "resistance" to break).
- **Buy signal:** price CLOSES above the pivot on **volume 40–50%+ above average**.
  (Minervini often buys as close to the pivot as possible so the stop can be tight.)

**How the CODE detects it (two independent checks in `scanner.py`):**
1. `detect_vcp(close_prices)` — walks left from the 120-day high, finds successive
   swing lows, requires each newer pullback to be shallower → counts "contractions".
2. `detect_vcp_hl(high,low,close)` — daily range `(High−Low)/Close`; recent 20-day
   avg must be **< 85%** of the prior 60-day avg → "range contracted".
- `vcp_validated = is_vcp AND (range_contracted OR contractions >= 3)`.

**Entry / stop / target math (exactly as coded):**
```
pivot  = highest close in last 120 trading days
entry  = pivot × 1.01          # buy 1% above the pivot breakout
stop   = entry × 0.93          # −7% hard stop
target = entry × 1.20          # +20% first target
RRR    = (target − entry) / (entry − stop)   # ≈ 2.9  (reward:risk)
```

---

## 5. Risk management — the part that actually makes money

This is why a <50% win rate still wins. Minervini's rules, verbatim in spirit:

1. **Hard stop 7–8% below entry. No exceptions.** Use a STOP order, not willpower.
2. **Risk per trade = 1–2% of total account.** Position size is derived FROM the
   stop distance, not chosen first.
   - Example: $100k account, risk 1% = $1,000. Stop is 7% below entry.
   - Shares = `$1,000 / (7% of entry price)`. If entry = $100, stop = $93,
     risk/share = $7 → buy 143 shares (~$14,300, but only $1,000 at risk).
3. **Never average down** (never add to a loser). Add only to winners.
4. **Trail your stop** once profitable: move it to breakeven after a decent gain;
   never let a 2R winner (double your risk) turn into a loss.
5. **Take partial profits** at +20–25%, or when price rockets away from the 50-day line.
6. **Win-rate math:** if avg win ≈ +20% (target) and avg loss ≈ −7% (stop),
   you only need to win ~27% of trades to break even, ~35%+ to profit nicely.
   *Losing is normal; the stops keep you alive to catch the few big runners.*

> J Law / Minervini both stress: **a strategy is only as good as your willingness to
> follow your own rules.** The skill can screen; discipline is on you.

---

## 6. Fundamental filters (SEPA needs trend + fundamentals)

Minervini requires BOTH. The code filter (in `analyze`):
- EPS (earnings) growth **> 20%** YoY, OR
- Revenue (sales) growth **> 15%** YoY, accelerating 2–3 quarters.

Also printed per row (from Yahoo `tk.info`): `PE` (trailing), `fPE` (forward),
gross margin, ROE — so you can avoid absurdly-priced names. No hard PE cutoff by
default (add one if you like), but a forward PE exploding vs trailing is a red flag.

---

## 7. How to RUN the scanner (step by step)

```bash
# 1. deps
pip install yfinance pandas mplfinance

# 2. quick single-ticker check (great for "is XNND a buy?")
cd <skill>/references
python3 -c "import scanner; r=scanner.analyze('NVDA'); print(r)"
#   -> prints tt, rs, vcp_validated, pe, fpe, entry, stop, target, rrr

# 3. full universe scan (502 S&P tickers in universe.txt)
python3 scanner.py
#   output columns: TKR Price RS VCP# VCP✓ %2Piv PE fPE ENTRY STOP TGT RRR

# 4. WITH auto charts (Agent/user eyeballs the setup)
VCP_MAKE_CHARTS=1 VCP_TOP_CHARTS=8 python3 scanner.py
#   charts saved to: <skill>/references/charts/<TKR>_candle.png

# 5. generate a chart for ONE ticker
python3 -c "import scanner; print(scanner.make_chart('DELL'))"
```

**Reading the output:**
- `VCP✓ = Y` → passed trend + RS + fundamentals AND a confirmed volatility contraction.
- `%2Piv` → how far price is below the breakout pivot. **Smaller = fresher breakout candidate.**
- Rank your watchlist by: `VCP✓=Y` first, then smallest `%2Piv`, then highest RS.

---

## 8. Reality notes (learned running this for real — READ THESE)

- **yfinance WORKS in the sandbox** (`pip install yfinance pandas`). No need for the
  old v8 chart-API workaround.
- **Universe files:** `universe.txt` (~502 S&P tickers) or `megacap_universe.txt`
  (cap ≥ $100B). NOT `sp500.txt` (doesn't exist).
- **Yahoo 401 "Invalid Crumb" errors** hit under concurrency. Fixes used: lower
  `ThreadPoolExecutor` workers (4–8) + retry with `time.sleep(random.uniform(2,9))`
  in `analyze`. A naive run got 136/502 data; the retry run got 483/502. Always re-run
  failed tickers.
- **PE/fPE also come from `tk.info`** → can be `None` (printed `0`) or GARBAGE when
  crumb-locked (once returned HWM PE=1701, obviously wrong). Treat PE as a sanity
  check, not gospel.
- **⚠️ The VCP check is STRICTER than the naked eye.** Names that *look* like a VCP
  on the chart (tight base at highs, low volume) sometimes fail `vcp_validated`
  because the 20-day vs 60-day range barely differs (e.g. DELL recent 6.6% vs prior
  6.4% — not <85%). **ALWAYS chart the top candidates and eyeball them.** A clean
  tight base at the highs with low volume IS a buyable VCP even if the code says `-`.
  Never call a mere volatility收缩 "VCP confirmed" without the chart check.
- **Approx RS** pins strong names to 99 — don't use RS to rank, use `VCP✓` + `%2Piv`.

---

## 9. Worked example (real 2026-08-16 scan)

A full S&P scan returned 39 VCP-validated names. The dominant signal was a
**financials cluster** (BNY, SCHW, CFG, MTB, PNC, TFC, USB, BAC, FITB — 11 banks all
coiling <1% below their pivots): a sector-level breakout, the strongest signal.
Meanwhile **NVDA, AVGO, PLTR, COIN, DELL all FAILED VCP** (too extended / not
contracting) — Minervini's method currently avoids the hyped AI names and points at
financials + a few quality tech (GRMN, NTAP, APH passed). See `sample_output.txt`.

**Concrete trade from that scan — BAC:**
- price $64.49, pivot $64.51, entry $65.46, stop $60.88 (−7%), target $78.55 (+20%).
- Account $100k, risk 1% = $1,000. Risk/share = $4.58 → ~218 shares (~$14,270).
- Action: set alert at $65.46; buy ONLY on a close above $65.46 with volume >1.4× avg;
  immediately place stop at $60.88; trail to breakeven after +7%; take 1/3 off at $78.55.

---

## 10. Common pitfalls (don't do these)

- ❌ Using RSI when you mean RS.
- ❌ Buying a Stage 1/3/4 stock (only Stage 2).
- ❌ Chasing an extended stock (far above its MAs, no base).
- ❌ Buying a breakout with NO volume confirmation.
- ❌ Widening your stop after entry ("just a little more room").
- ❌ Averaging down on a loser.
- ❌ Trusting `VCP✓` without charting (see Reality notes).
- ❌ Trading with no stop, or risking >2% of account per trade.
- ❌ Over-diversifying into 20 names (Minervini concentrates; a few high-conviction).

---

## 11. Reference files in this skill
- `references/scanner.py` — runnable scanner (yfinance, real VCP, PE/fPE, chart gen). **Single source of truth for the math.**
- `references/playbook.md` — long-form Chinese Minervini writeup (theory).
- `references/universe.txt` — ~502 S&P tickers.
- `references/megacap_universe.txt` — cap ≥ $100B subset.
- `references/sample_output.txt` — real 39-name scan (2026-08-16) + insights.
- `references/charts/` — auto-generated candlestick PNGs (when `VCP_MAKE_CHARTS=1`).

---
*Compiled 2026-08-16 from Minervini's books, J Law (@jlawstock) VCP teaching, Weinstein
stage analysis, and verified against the live `scanner.py`. Not financial advice.*
