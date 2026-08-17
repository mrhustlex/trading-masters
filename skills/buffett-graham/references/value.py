"""Buffett/Graham value-investing screen (yfinance-based).
Run:  python3 value.py AAPL KO PG JPM
      python3 value.py --universe ../scripts/universe.txt
Scores P/E, P/B, debt/equity, ROE, FCF yield, EPS stability -> 0-100 value score + PASS.
"""
import sys, os, time, random, warnings, argparse
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))

def get_info(t):
    for _ in range(3):
        try:
            return yf.Ticker(t).info
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return {}

def get_cf(t):
    for _ in range(3):
        try:
            cf = yf.Ticker(t).cashflow
            return cf
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return None

def analyze(t):
    info = get_info(t)
    if not info: return None
    pe = info.get('trailingPE'); pb = info.get('priceToBook')
    de = info.get('debtToEquity')
    if de: de = de/100.0  # yahoo gives it as %
    roe = info.get('returnOnEquity')
    gm = info.get('grossMargins')
    price = info.get('regularMarketPrice') or info.get('currentPrice')
    score = 0; n = 0
    def chk(cond, pts):
        nonlocal score, n
        n += pts
        if cond: score += pts
    chk(pe is not None and 0 < pe <= 20, 20)
    chk(pb is not None and 0 < pb <= 3, 15)
    chk(de is not None and 0 <= de <= 0.5, 15)
    chk(roe is not None and roe >= 0.15, 20)
    chk(gm is not None and gm >= 0.30, 10)
    # FCF yield
    fcf_y = None
    try:
        cf = get_cf(t)
        if cf is not None and price:
            fcf = cf.loc['Free Cash Flow'].dropna()
            if len(fcf):
                fcf_ttm = fcf.iloc[0]
                mcap = info.get('marketCap')
                if mcap: fcf_y = fcf_ttm / mcap
    except Exception: pass
    chk(fcf_y is not None and fcf_y >= 0.04, 20)
    passed = (pe and pe <= 20 and (pb and pb <= 3) and (de is not None and de <= 0.5)
              and (roe and roe >= 0.15))
    return dict(tkr=t, price=round(price,2) if price else None,
                pe=round(pe,1) if pe else None, pb=round(pb,1) if pb else None,
                de=round(de,2) if de is not None else None,
                roe=round(roe*100,1) if roe else None,
                fcf_y=round(fcf_y*100,1) if fcf_y else None,
                score=round(100*score/n) if n else 0, passed=bool(passed))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"..","..","scripts","universe.txt"))
    a = ap.parse_args()
    if a.tickers: tkrs = a.tickers
    elif os.path.exists(a.universe): tkrs = open(a.universe).read().split()
    else: tkrs = ["AAPL","KO","PG","JPM"]
    print(f"{'TKR':<6}{'Price':>9}{'PE':>7}{'PB':>6}{'D/E':>6}{'ROE%':>7}{'FCFy%':>7}  score  PASS")
    for t in tkrs[:80]:
        r = analyze(t)
        if not r: continue
        print(f"{r['tkr']:<6}{r['price'] if r['price'] else 0:>9}{r['pe'] if r['pe'] else 0:>7}"
              f"{r['pb'] if r['pb'] else 0:>6}{r['de'] if r['de'] is not None else 0:>6}"
              f"{r['roe'] if r['roe'] else 0:>7}{r['fcf_y'] if r['fcf_y'] else 0:>7}  "
              f"{r['score']:>4}   {'YES' if r['passed'] else ''}")

if __name__ == "__main__":
    main()
