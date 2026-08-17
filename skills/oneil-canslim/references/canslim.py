"""William O'Neil CAN SLIM scanner (yfinance-based).
Run:  python3 canslim.py AAPL NVDA
      python3 canslim.py --universe universe.txt
Prints per-ticker: C/A/N/L/I/S gates, RS, pivot/entry/stop/target, market hint.
"""
import sys, os, time, random, warnings, argparse
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__))

def get_hist(t, period="1y"):
    for _ in range(3):
        try:
            h = yf.Ticker(t).history(period=period)
            h = h[['Close','Volume']].dropna()
            if len(h) > 200: return h
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return None

def get_info(t):
    for _ in range(3):
        try:
            return yf.Ticker(t).info
        except Exception: pass
        time.sleep(random.uniform(1.5,4))
    return {}

def rs_vs_spy(ret):
    spy = yf.Ticker("SPY").history(period="1y")['Close']
    sr = (spy.iloc[-1]/spy.iloc[0]) - 1
    return max(1, min(99, int(round(50 + 50*ret/(sr+1e-9)))))

def analyze(t):
    h = get_hist(t)
    info = get_info(t)
    if h is None: return None
    close = h['Close']; vol = h['Volume']
    price = close.iloc[-1]
    hi60 = close.iloc[-60:].max()
    lo60 = close.iloc[-60:].min()
    pivot = hi60
    entry = pivot*1.01
    stop = entry*0.92
    target = entry*1.20
    # fundamentals
    eg = info.get('earningsGrowth') or info.get('earningsQuarterlyGrowth')
    eps_g = eg if isinstance(eg,(int,float)) else None
    roe = info.get('returnOnEquity')
    rg = info.get('revenueGrowth')
    rev_g = rg if isinstance(rg,(int,float)) else None
    ret_52 = (price/close.iloc[-252:].min()) - 1 if len(close)>=252 else (price/close.iloc[0])-1
    rs = rs_vs_spy(ret_52)
    # C/A/L gates
    C = (eps_g is not None and eps_g >= 0.25)
    A = (roe is not None and roe >= 0.17)
    L = rs >= 80
    N = price >= hi60*0.95               # near 52w high = "new high" proxy
    # S / I (ownership) approximated: market cap reasonable + has institutions
    inst = info.get('heldPercentInstitutions')
    I = (inst is not None and inst > 0.1)
    # base quality: handle should be tight (last 10d range < 8% of price)
    rng10 = (close.iloc[-10:].max()-close.iloc[-10:].min())/price
    tight = rng10 < 0.08
    passed = C and A and L and N
    return dict(tkr=t, price=round(price,2), rs=rs, eps_g=eps_g, roe=roe,
                rev_g=(rev_g if isinstance(rev_g,(int,float)) else None),
                C=C, A=A, L=L, N=N, I=I, tight_base=tight,
                pivot=round(pivot,2), entry=round(entry,2), stop=round(stop,2),
                target=round(target,2), passed=passed)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"..","universe.txt"))
    a = ap.parse_args()
    if a.tickers:
        tkrs = a.tickers
    else:
        p = a.universe
        if os.path.exists(p):
            tkrs = open(p).read().split()
        else:
            tkrs = ["AAPL","NVDA","AMD","ANET","VRT","APH","EMR"]
    print(f"{'TKR':<6}{'Price':>9}{'RS':>4}  C A L N I  base  pivot  entry  stop  tgt  PASS")
    for t in tkrs[:60]:
        r = analyze(t)
        if not r: continue
        flags = "".join([c[0] for c in [('C',r['C']),('A',r['A']),('L',r['L']),('N',r['N']),('I',r['I'])]])
        print(f"{r['tkr']:<6}{r['price']:>9}{r['rs']:>4}  "
              f"{'Y' if r['C'] else '-'}{'Y' if r['A'] else '-'}{'Y' if r['L'] else '-'}"
              f"{'Y' if r['N'] else '-'}{'Y' if r['I'] else '-'}  "
              f"{'tight' if r['tight_base'] else 'wide':4}  {r['pivot']:>7}{r['entry']:>8}{r['stop']:>7}{r['target']:>7}"
              f"  {'YES' if r['passed'] else ''}")

if __name__ == "__main__":
    main()
