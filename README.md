# trading-masters

Scanner skills + scripts for the **greatest investors, swing traders & day traders**, each
distilled into a layman-replicable method, a do/don't checklist, and a runnable yfinance
(or pure-math) screen.

> ⚠️ **Education only. Not financial advice.** Past performance ≠ future results.

## Two families

- **Invest / Swing (hold days–years):** Buffett, Lynch, Greenblatt, Munger/Marks/Templeton/Livermore, Minervini, O'Neil, Weinstein, Darvas, Wyckoff.
- **Day trading (intraday 1-min):** Aziz (ORB+VWAP), Brooks (Price Action), Cameron (Momentum). See the **Day-trading set** section.

## The 12 masters

| # | Master | Method | Skill dir | Script | Style |
|---|---|---|---|---|---|
| 1 | **Warren Buffett / Ben Graham** | Value + Margin of Safety | `buffett-graham/` | `value.py` | Own-the-business |
| 2 | **Peter Lynch** | GARP / PEG ≤ 1 | `peter-lynch/` | `peg.py` | Growth-at-value |
| 3 | **Joel Greenblatt** | Magic Formula (ROC + EY rank) | `greenblatt-magic/` | `magic.py` | Mechanical quant |
| 4 | **Jesse Livermore** | Cut losses / pyramid (risk math) | `value-masters/` | `livermore.py` | Speculator discipline |
| 5 | **Charlie Munger** | Mental models / invert / "Too Hard" | `value-masters/` | (checklist) | Judgment |
| 6 | **Howard Marks** | Risk cycles / 2nd-level thinking | `value-masters/` | (checklist) | Risk psychology |
| 7 | **John Templeton** | Buy at max pessimism / global | `value-masters/` | (checklist) | Contrarian |
| 8 | **Mark Minervini** | SEPA / VCP breakout | `scripts/minervini_scanner.py` | (parabola-safe) | Momentum swing |
| 9 | **William O'Neil** | CAN SLIM | `oneil-canslim/` | `canslim.py` | Momentum growth |
| 10 | **Stan Weinstein** | Stage Analysis | `weinstein-stage/` | `stage.py` | Trend timing |
| 11 | **Nicolas Darvas** | Box Theory | `darvas-box/` | `darvas.py` | Box breakout |
| 12 | **Richard Wyckoff** | Accumulation/Distribution | `wyckoff/` | `wyckoff.py` | Smart-money read |

(Counted 9 "masters" by person; Minervini/O'Neil/Weinstein/Darvas/Wyckoff are the
technical/momentum set, the rest are value/quality/judgment.)

## Each master's philosophy + DO / DON'T

### 1. Buffett & Graham — Value
- **Philosophy:** Buy a dollar of business for ~50¢ (margin of safety). Within your
  **circle of competence**. A **durable moat** (pricing power) protects returns. Buffett's
  evolution: *wonderful company at a fair price* > cheap mediocre company. Favourite
  holding period = forever.
- **DO:** demand moat + low debt + high ROE + FCF; be patient; size by conviction.
- **DON'T:** buy what you don't understand; ignore debt; chase hot names; use leverage;
  sell on noise.
- *Check: `python3 buffett-graham/references/value.py AAPL KO JPM`*

### 2. Peter Lynch — GARP
- **Philosophy:** Invest in what you know. **PEG = P/E ÷ EPS growth**. PEG ≤ 1 = fair;
  ≤ 0.5 = cheap growth. Fast growers (20–25%) at a reasonable PEG = his edge.
- **DO:** buy familiar businesses; use PEG; let winners run.
- **DON'T:** buy on tips; hold a decelerating story; over-diversify into names you can't track.
- *Check: `python3 peter-lynch/references/peg.py AAPL NVDA APH`*

### 3. Joel Greenblatt — Magic Formula
- **Philosophy:** Mechanical. Rank by **ROC** (quality) + **Earnings Yield** (cheap);
  buy lowest combined rank; hold ~1yr; rebalance. No emotion.
- **DO:** mechanize; equal-weight 20–30; rebalance annually; ignore news.
- **DON'T:** abandon after a bad year; mix with timing; add "favourites".
- *Check: `python3 greenblatt-magic/references/magic.py --universe scripts/universe.txt --top 20`*

### 4. Jesse Livermore — Speculator
- **Philosophy:** Cut losses *immediately*; let winners run; **pyramid** only as it goes
  your way (never average down); sit tight through normal corrections.
- **DO:** size by risk; trade with the main trend; take a loss fast.
- **DON'T:** average down; overtrade; let a loss become a disaster.
- *Check: `python3 value-masters/references/livermore.py --account 100000 --risk 1 --entry 178 --stop 165`*

### 5. Charlie Munger — Judgment
- **Philosophy:** Invert ("avoid stupidity, not seek brilliance"); lattice of mental
  models; "Too Hard" pile; patience; say no to most ideas.
- **DO:** read widely; demand quality; be patient; know your limits.
- **DON'T:** trade on tips; confuse activity with wisdom; use leverage.

### 6. Howard Marks — Risk
- **Philosophy:** Risk = chance of **permanent loss**, not volatility. Markets swing
  euphoria↔despair; buy fearful, sell greedy. Second-level thinking.
- **DO:** stress-test the downside; know the cycle position.
- **DON'T:** extrapolate the recent past; follow the crowd; skip margin of safety.

### 7. John Templeton — Contrarian
- **Philosophy:** "Buy at the point of **maximum pessimism**"; global; long horizon.
- **DO:** be brutally contrarian; look worldwide; be patient decades.
- **DON'T:** chase yesterday's winners; fear the unknown market.

### 8–12. Technical/momentum set (Minervini, O'Neil, Weinstein, Darvas, Wyckoff)
- See each skill's SKILL.md. Shared core: **trend + volume + tight risk, never average down,
  parabolas are exits not entries** (`detect_parabola()` flags them).

## Day-trading set (intraday 1-min, separate discipline from the above)

| # | Master | Method | Skill dir | Script |
|---|---|---|---|---|
| 10 | **Andrew Aziz** | Opening Range Breakout + VWAP + ABCD | `aziz-orb/` | `orb.py` |
| 11 | **Al Brooks** | Pure Price Action (bar context, EMA20 pullbacks) | `brooks-priceaction/` | `priceaction.py` |
| 12 | **Ross Cameron** | Momentum / HOD breakout + relative volume | `cameron-momentum/` | `momentum.py` |

**Philosophy (all three):** trade the *first hour* on a catalyst; VWAP / EMA20 is the line
in the sand; 1–2% risk per trade; cut fast. Differ from the swing set: they use **1-min
bars**, never hold overnight, and react to intraday breakouts rather than daily-stage setups.
**DO:** wait for the range/catalyst, confirm with volume+VWAP, trail tight. **DON'T:** chase
after the move ran, hold into the close, widen stops.
> ⚠️ yfinance free 1-min = last ~7 sessions only; for live/backtest scale you'll want a
> paid feed (Polygon/Alpaca). Scripts fetch `period='5d'` 1-min and slice the date.

## Install
```bash
pip install yfinance pandas numpy mplfinance
```

## The full stack (how they fit)
- **Value/quality (1–3):** what's worth owning long-term.
- **Judgment (4–7):** how to think + size + behave.
- **Timing — swing (8–9):** when to enter a momentum name (days–weeks).
- **Timing — day (10–12):** intraday breakout/discipline.
All agree: **cut losses, never average down, demand a margin of safety, be disciplined.**

## Files
```
skills/buffett-graham/    SKILL.md + references/value.py
skills/peter-lynch/       SKILL.md + references/peg.py
skills/greenblatt-magic/   SKILL.md + references/magic.py
skills/value-masters/      SKILL.md + references/livermore.py (Munger/Marks/Templeton/Livermore)
skills/oneil-canslim/      SKILL.md + references/canslim.py
skills/weinstein-stage/    SKILL.md + references/stage.py
skills/darvas-box/         SKILL.md + references/darvas.py
skills/wyckoff/            SKILL.md + references/wyckoff.py
skills/aziz-orb/           SKILL.md + references/orb.py (Opening Range Breakout + VWAP)
skills/brooks-priceaction/ SKILL.md + references/priceaction.py (bar context, EMA20)
skills/cameron-momentum/   SKILL.md + references/momentum.py (HOD breakout + rel-vol)
scripts/                    universe.txt + minervini_scanner.py (detect_parabola) + master_screen.py
README.md  requirements.txt  LICENSE
```

## License
MIT
