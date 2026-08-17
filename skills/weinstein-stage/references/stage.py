"""Stan Weinstein Stage Analysis classifier (yfinance-based).
Run:  python3 stage.py NVDA APH SMCI
      python3 stage.py --universe universe.txt
Prints stage (1-4), MA slopes, volume trend, Stage-2 breakout flag. Also SPY stage.
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

def classify(t):
    h = get_hist(t)
    if h is None: return None
    close, vol = h['Close'], h['Volume']
    price = close.iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]
    ma150 = close.rolling(150).mean()
    ma150_now = ma150.iloc[-1]; ma150_prev = ma150.iloc[-63] if len(ma150)>63 else ma150.iloc[0]
    ma200 = close.rolling(200).mean().iloc[-1]
    slope_up = ma150_now > ma150_prev
    vol_now = vol.iloc[-20:].mean(); vol_prev = vol.iloc[-60:-20].mean()
    vol_up = vol_now > vol_prev
    # Stage
    if price > ma150_now and ma150_now > ma200 and slope_up and price > ma50:
        stage = 2
    elif price < ma150_now and ma150_now < ma200 and not slope_up:
        stage = 4
    else:
        # 1 vs 3: base (price near/under flattening MA, early low vol) or top (price near MA, churn)
        stage = 1 if not slope_up else 3
    # Stage-2 breakout: just crossed above 150MA in last 20d on strong vol
    crossed = (close.iloc[-20:-1] < ma150.iloc[-20:-1]).any() and price > ma150_now
    brk = crossed and (vol.iloc[-1] > 1.5*vol.iloc[-50:].mean())
    return dict(tkr=t, price=round(price,2), stage=stage,
                ma150=round(ma150_now,2), ma200=round(ma200,2),
                slope="up" if slope_up else "down", vol_trend="rising" if vol_up else "falling",
                stage2_breakout=brk)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"..","universe.txt"))
    a = ap.parse_args()
    if a.tickers: tkrs = a.tickers
    elif os.path.exists(a.universe): tkrs = open(a.universe).read().split()
    else: tkrs = ["NVDA","APH","SMCI"]
    # market filter
    spy = classify("SPY")
    print(f"MARKET (SPY) stage: {spy['stage']} ({'BUY individual stage-2' if spy['stage']==2 else 'STAND ASIDE' if spy['stage']!=2 else ''})\n")
    print(f"{'TKR':<6}{'Price':>9}  Stage  MA150slope  VolTrend   Stage2-breakout")
    for t in tkrs[:60]:
        r = classify(t)
        if not r: continue
        print(f"{r['tkr']:<6}{r['price']:>9}   S{r['stage']}    {r['slope']:<8}  {r['vol_trend']:<8}  {'YES' if r['stage2_breakout'] else ''}")

if __name__ == "__main__":
    main()
