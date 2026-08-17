"""Al Brooks price-action scanner (yfinance 1/5-min).
Run:  python3 priceaction.py NVDA --date 2026-08-17 --tf 1
      python3 priceaction.py AAPL --tf 5
Scores trend-bar strength, EMA20 slope, latest setup (pullback-long/short / climax).
No indicators beyond EMA20; pure bar structure.
"""
import sys, os, argparse, warnings
import yfinance as yf
import pandas as pd, numpy as np
warnings.filterwarnings("ignore")

def get_bars(t, tf=1, days=5):
    df = yf.download(t, period=f"{days}d", interval=f"{tf}m", progress=False, auto_adjust=True)
    if df is None or len(df)==0: return None
    if isinstance(df.columns, pd.MultiIndex): df.columns=[c[0] for c in df.columns]
    df = df[["Open","High","Low","Close","Volume"]].copy()
    df.index = pd.to_datetime(df.index)
    return df

def trend_bar(b):
    rng = b["High"]-b["Low"]
    if rng==0: return 0
    body = abs(b["Close"]-b["Open"])
    close_pos = (b["Close"]-b["Low"])/rng
    if body >= 0.5*rng and close_pos >= 0.6: return 1      # bull trend bar
    if body >= 0.5*rng and close_pos <= 0.4: return -1     # bear trend bar
    return 0

def analyze(t, date=None, tf=1):
    df = get_bars(t, tf, 5)
    if df is None: return None
    if date:
        df = df[df.index.date==pd.Timestamp(date).date()]
    if len(df)==0: return None
    d = df.between_time("09:30","15:59") if len(df)>30 else df
    d["tb"] = d.apply(trend_bar, axis=1)
    d["ema20"] = d["Close"].ewm(span=20).mean()
    d["ema_slope"] = d["ema20"].diff(5)
    # last 20 bars context
    win = d.tail(20)
    tb_ratio = win["tb"].clip(-1,1).mean()          # >0 bullish, <0 bearish
    slope = d["ema_slope"].iloc[-1]
    last = d.iloc[-1]; prev = d.iloc[-2]
    at_ma = abs(last["Close"]-last["ema20"])/last["ema20"] < 0.002
    # setup detection
    setup = "none"
    if tb_ratio > 0.15 and slope > 0 and last["Close"] > last["ema20"]: setup="pullback-LONG (with trend)"
    elif tb_ratio < -0.15 and slope < 0 and last["Close"] < last["ema20"]: setup="pullback-SHORT (with trend)"
    elif tb_ratio > 0.3 and slope <= 0: setup="climax-up (watch reversal)"
    elif tb_ratio < -0.3 and slope >= 0: setup="climax-down (watch reversal)"
    return dict(tkr=t, tf=tf, date=str(d.index[-1].date()),
                bull_bars_pct=round(100*(tb_ratio+1)/2,0), ema_slope=round(slope,3),
                price=round(last["Close"],2), ema20=round(last["ema20"],2),
                at_ma=bool(at_ma), setup=setup)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--date", default=None)
    ap.add_argument("--tf", type=int, default=1)
    a = ap.parse_args()
    for t in a.tickers:
        r = analyze(t, a.date, a.tf)
        if not r: print(f"{t}: no data"); continue
        print(f"{r['tkr']} {r['date']} {r['tf']}m: bull%={r['bull_bars_pct']} "
              f"EMA_slope={r['ema_slope']} price={r['price']} EMA20={r['ema20']} "
              f"@MA={r['at_ma']} -> {r['setup']}")

if __name__ == "__main__":
    main()
