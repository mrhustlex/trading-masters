"""Joel Greenblatt Magic Formula ranker (yfinance-based).
Run:  python3 magic.py --universe ../../scripts/universe.txt --top 20
      python3 magic.py AAPL KO JPM XOM
ROC = EBIT / (Net Fixed Assets + Net Working Capital)
Earnings Yield = EBIT / Enterprise Value
Rank 1..N on each, sum ranks, lowest combined rank = best (quality + cheap).
"""
import sys, os, time, random, warnings, argparse
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))

def get(t):
    for _ in range(3):
        try:
            tk = yf.Ticker(t)
            return tk.info, tk.financials
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return {}, None

def magic(t):
    info, fin = get(t)
    if not info: return None
    sector = (info.get('sector') or '')
    if sector in ('Financial Services','Insurance','Banks','Utilities'): return None
    mcap = info.get('marketCap'); pe = info.get('trailingPE')
    if not mcap or mcap < 2e9: return None   # skip micro/small caps
    debt = info.get('totalDebt') or 0
    cash = info.get('totalCash') or 0
    ev = mcap + debt - cash
    ebit = None
    if fin is not None:
        try:
            ebit = fin.loc['EBIT'].dropna()
            ebit = ebit.iloc[0] if len(ebit) else None
        except Exception: ebit = None
    if ebit is None or ebit <= 0 or ev <= 0: return None
    ey = ebit / ev                      # earnings yield
    # ROC denominator: net fixed assets + net working capital (Greenblatt).
    # Balance-sheet fields often missing from .info -> pull from .balance_sheet.
    bs = None
    try: bs = yf.Ticker(t).balance_sheet
    except Exception: bs = None
    def bsv(col):
        if bs is None: return 0
        try:
            v = bs.loc[col].dropna()
            return v.iloc[0] if len(v) else 0
        except Exception: return 0
    nfa = bsv('Property Plant Equipment') or bsv('Net Property Plant Equipment') or 0
    ca = bsv('Current Assets'); cl = bsv('Current Liabilities')
    wc = (ca - cl) if (ca and cl) else 0
    cap = nfa + wc
    ta = bsv('Total Assets')
    if cap <= 0 and ta: cap = ta * 0.5
    if cap <= 0: return None
    roc = ebit / cap
    return dict(tkr=t, ey=ey, roc=roc, pe=round(pe,1) if pe else None)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"..","..","scripts","universe.txt"))
    ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()
    if a.tickers: tkrs = a.tickers
    elif os.path.exists(a.universe): tkrs = open(a.universe).read().split()
    else: tkrs = ["AAPL","KO","JPM","XOM"]
    rows = []
    for t in tkrs[:120]:
        r = magic(t)
        if r: rows.append(r)
    if not rows:
        print("No rankable stocks (data/network)."); return
    df = pd.DataFrame(rows)
    df['rk_roc'] = df['roc'].rank(ascending=False).astype(int)
    df['rk_ey'] = df['ey'].rank(ascending=False).astype(int)
    df['combined'] = df['rk_roc'] + df['rk_ey']
    df = df.sort_values('combined').head(a.top)
    print(f"{'Rank':<5}{'TKR':<6}{'EY%':>7}{'ROC%':>8}{'PE':>7}  combined")
    for i,(_,r) in enumerate(df.iterrows(),1):
        print(f"{i:<5}{r['tkr']:<6}{r['ey']*100:>7.1f}{r['roc']*100:>8.1f}{r['pe'] if r['pe'] else 0:>7}  {int(r['combined'])}")

if __name__ == "__main__":
    main()
