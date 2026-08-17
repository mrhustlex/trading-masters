---
name: buffett-graham
description: "Warren Buffett + Benjamin Graham value investing. Buy wonderful companies at fair prices within your circle of competence, with a margin of safety. Quantitative screen: P/E, P/B, debt/equity, ROE, FCF yield, moat proxies. yfinance-based scanner."
version: 1.0.0
author: Hei
license: MIT
tags: [trading, stocks, buffett, graham, value-investing, margin-of-safety, moat, quality]
---

# Warren Buffett & Benjamin Graham — Value Investing (v1.0)

> **Goal:** buy a dollar of business for ~50 cents. Graham = deep value / margin of safety;
> Buffett (+Munger) = quality at a fair price, held long. The antithesis of momentum —
> this is the *own-the-business* layer the other 4 skills ignore.

## 0. Plain English
Don't day-trade. Find a business you **understand** (circle of competence), with a
**durable moat** (pricing power), that earns high returns on capital, and buy it at a
price well below what it's worth (margin of safety). Then hold for years.

## 1. Core principles
- **Margin of Safety** (Graham): price ≪ intrinsic value. The gap absorbs being wrong.
- **Circle of Competence** (Buffett): only invest where you can read the business cold. "Too Hard" pile = skip.
- **Economic Moat**: brand / scale / network / switching-costs that protect ROIC for decades.
- **Quality > cheapness** (Buffett's evolution): a great business at a fair price beats a mediocre one cheap.
- **Favourite holding period = forever** (unless thesis breaks).

## 2. Quantifiable screen (as coded in `references/value.py`)
| Check | Rule | Why |
|---|---|---|
| P/E | ≤ 20 (or < market) | not overpriced |
| P/B | ≤ 3 (Graham liked < 1.5) | asset backing |
| Debt/Equity | ≤ 0.5 | financial strength |
| ROE | ≥ 15% | quality / moat |
| FCF yield | ≥ 4% (FCF/price) | real cash, not accounting |
| Earnings stability | positive EPS most of last 5y | predictability |
| Margin of safety | price < ~60% of rough intrinsic (FCF disc.) | Graham's cushion |

## 3. Do / Don't
**DO:** buy wonderful businesses at fair prices; reinvest; be patient; demand a moat + low debt.
**DON'T:** buy what you don't understand; chase hot stocks outside your circle; ignore debt; sell on noise; use lots of leverage; average down a broken thesis.

## 4. Script
`references/value.py` scores a ticker on the above; prints PASS + a 0–100 value score.

```bash
cd <skill>/references
python3 value.py AAPL KO PG JPM
python3 value.py --universe ../scripts/universe.txt
```

## 5. Reality notes
- yfinance gives P/E, P/B, ROE, debt/Equity, FCF (operating cashflow − capex). Intrinsic value = DCF is rough; script uses a conservative FCF-yield margin-of-safety proxy.
- Moat is **qualitative** — the script proxies it with ROE consistency + gross margin; you still judge the moat yourself.
- Buffett's best picks (KO, AAPL) often fail a strict P/E≤20 screen at times — quality can command a higher multiple; treat the screen as a *filter*, not gospel.

## 6. Pitfalls
- ❌ Value traps: cheap for a reason (declining business). Always check the *why*.
- ❌ Ignoring the moat (Graham's cigar-butts can burn).
- ❌ Selling too early on a great compounder; or holding a value trap too long.

---
*Compiled 2026-08-17 from Graham "The Intelligent Investor" + Buffett letters/Berkshire. Not financial advice.*
