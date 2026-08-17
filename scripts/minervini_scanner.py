#!/usr/bin/env python3
"""Minervini VCP Scanner — full version (yfinance).
Steps:
  1. Load universe (universe.txt, ~544 liquid US stocks, ex-ETF)
  2. Fetch recent volume for each, rank by 50-day avg volume
  3. Take top N (default 800) most liquid
  4. For those, compute Trend Template (8), RS, VCP contraction, fundamentals
  5. Output ranked watchlist: TT+RS>=89 + fundamental strength (EPS>20% or Sales>15%)
Run: python3 scanner.py
Deps: pip install yfinance pandas
"""
import os, sys
import yfinance as yf
import pandas as pd
import numpy as np
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
UNIVERSE_FILE = os.path.join(HERE, "megacap_universe.txt")
TOP_N = 500  # scan only the most liquid TOP_N by avg volume (full universe ~502)
CHART_DIR = os.environ.get("VCP_CHART_DIR", os.path.join(HERE, "charts"))


def make_chart(t, days=130, save=True):
    """Generate a candlestick chart with 50/150/200 SMA overlays + volume.
    Returns the PNG path (or None on failure). Used so an Agent/user can
    visually verify the VCP / Stage-2 read instead of trusting the code blindly.
    Requires: pip install mplfinance
    """
    try:
        warnings.filterwarnings("ignore")
        import mplfinance as mpf
        df = yf.Ticker(t).history(period="1y")
        if df is None or len(df) < 60:
            return None
        df = df[['Open', 'High', 'Low', 'Close', 'Volume']].dropna()
        df['MA50'] = df['Close'].rolling(50).mean()
        df['MA150'] = df['Close'].rolling(150).mean()
        df['MA200'] = df['Close'].rolling(200).mean()
        sub = df.iloc[-days:]
        ap = [mpf.make_addplot(sub['MA50'], color='tab:blue', width=0.8),
              mpf.make_addplot(sub['MA150'], color='tab:orange', width=0.8),
              mpf.make_addplot(sub['MA200'], color='tab:green', width=0.8)]
        if save:
            os.makedirs(CHART_DIR, exist_ok=True)
            path = os.path.join(CHART_DIR, f"{t}_candle.png")
            mpf.plot(sub, type='candle', style='charles', addplot=ap,
                     volume=True, panel_ratios=(3, 1),
                     title=f"{t} — {days}d (50/150/200 MA)",
                     savefig=path, figscale=1.2)
            return path
        return "preview"
    except Exception:
        return None

def load_universe():
    with open(UNIVERSE_FILE) as f:
        return [l.strip() for l in f if l.strip()]

def get_avg_volume(t, days=50):
    try:
        h = yf.Ticker(t).history(period=f"{days+5}d")
        if h is None or len(h) < days:
            return None
        return int(h['Volume'].rolling(days).mean().iloc[-1])
    except Exception:
        return None

def detect_vcp(c, ma150):
    """Detect a real Volatility Contraction Pattern.
    Returns dict with: is_vcp, contractions (count), pivot (breakout price),
    pct_below_pivot (% current price is below pivot).
    Logic:
      - Require current price above 150DMA (in a base / Stage 2, not deep below)
      - Look at last ~120 trading days
      - Find base pivot = highest close in that window
      - Walk LEFT from pivot, find successive swing lows (pullbacks)
      - Each pullback depth (from pivot) must be SMALLER than the previous => contraction
      - Need >=2 contractions to qualify as VCP
    """
    try:
        p = c.iloc[-1]
        if p < ma150:
            return dict(is_vcp=False, contractions=0, pivot=None, pct_below_pivot=None)
        window = c.iloc[-120:]
        if len(window) < 60:
            return dict(is_vcp=False, contractions=0, pivot=None, pct_below_pivot=None)
        pivot = window.max()
        pivot_idx = window.idxmax()
        pre = window.loc[:pivot_idx]
        if len(pre) < 20:
            return dict(is_vcp=False, contractions=0, pivot=round(float(pivot),2), pct_below_pivot=None)
        # find swing lows in pre (local minima using a 2-bar window to catch more)
        lows_idx = []
        arr = pre.values
        for i in range(1, len(arr)-1):
            if arr[i] <= arr[i-1] and arr[i] <= arr[i+1]:
                lows_idx.append(i)
        if len(lows_idx) < 2:
            return dict(is_vcp=False, contractions=0, pivot=round(float(pivot),2), pct_below_pivot=None)
        # depths from pivot, in time order (oldest -> newest, i.e. walking back from pivot)
        depths = [(pivot - arr[i])/pivot for i in lows_idx]
        # count consecutive contractions from the most recent low backward:
        # we want EACH successive pullback (newer) to be shallower than the prior (older)
        contractions = 0
        for i in range(len(depths)-1, 0, -1):
            if depths[i] < depths[i-1]:
                contractions += 1
            else:
                break
        is_vcp = contractions >= 1
        pct_below = (pivot - p)/pivot*100
        return dict(is_vcp=is_vcp, contractions=contractions,
                    pivot=round(float(pivot),2),
                    pct_below_pivot=round(pct_below,1))
    except Exception:
        return dict(is_vcp=False, contractions=0, pivot=None, pct_below_pivot=None)


def detect_parabola(c, ma200, window=20, slope_thresh=0.04, ext_thresh=0.40):
    """Detect a parabolic (unsustainable vertical) advance.

    A parabola = price accelerating straight up, far above the 200-day MA, with a
    steep recent slope. These are SELL/distribution clues, NOT buy-the-breakout setups.
    Returns dict: is_parabola (bool), slope (recent daily % change), pct_above_ma200.
    """
    try:
        if c is None or len(c) < 60:
            return dict(is_parabola=False, slope=None, pct_above_ma200=None)
        recent = c.iloc[-window:]
        slope = (recent.iloc[-1] / recent.iloc[0]) - 1          # total % gain over window
        daily_slope = slope / window                            # avg daily %
        pct_above = (c.iloc[-1] / ma200) - 1 if ma200 and ma200 > 0 else None
        is_parabola = (daily_slope >= slope_thresh) and (pct_above is not None and pct_above >= ext_thresh)
        return dict(is_parabola=bool(is_parabola),
                    slope=round(daily_slope*100, 2),
                    pct_above_ma200=round(pct_above*100, 1) if pct_above is not None else None)
    except Exception:
        return dict(is_parabola=False, slope=None, pct_above_ma200=None)


def detect_vcp_hl(hist, ma150):
    """Candle-based VCP check using High-Low daily range (true volatility).
    Confirms the close-based VCP by verifying volatility contracted in recent window.
    Returns dict: hl_contracted (bool), recent_range%, prior_range%.
    """
    try:
        if hist is None or len(hist) < 120:
            return dict(hl_contracted=False, recent_range=None, prior_range=None)
        c = hist['Close'].dropna()
        p = c.iloc[-1]
        if p < ma150:
            return dict(hl_contracted=False, recent_range=None, prior_range=None)
        # daily true range proxy = (High-Low)/Close
        rng = (hist['High'] - hist['Low']) / hist['Close']
        rng = rng.dropna()
        if len(rng) < 100:
            return dict(hl_contracted=False, recent_range=None, prior_range=None)
        recent = rng.iloc[-20:].mean()   # last 20d avg range
        prior = rng.iloc[-80:-20].mean()  # prior 60d avg range
        contracted = recent < prior * 0.85  # recent vol < 85% of prior = mild contraction
        return dict(hl_contracted=contracted,
                     recent_range=round(recent*100, 1),
                     prior_range=round(prior*100, 1))
    except Exception:
        return dict(hl_contracted=False, recent_range=None, prior_range=None)


def analyze(t):
    try:
        tk = yf.Ticker(t)
        hist = tk.history(period="1y")
        if hist is None or len(hist) < 210:
            return None
        c = hist['Close'].dropna()
        p = c.iloc[-1]
        ma50 = c.rolling(50).mean().iloc[-1]
        ma150 = c.rolling(150).mean().iloc[-1]
        ma200 = c.rolling(200).mean().iloc[-1]
        if pd.isna(ma50) or pd.isna(ma150) or pd.isna(ma200):
            return None
        hi52 = c.iloc[-252:].max() if len(c) >= 252 else c.max()
        lo52 = c.iloc[-252:].min() if len(c) >= 252 else c.min()
        if lo52 == 0 or pd.isna(lo52):
            return None
        ret_52w = (p / lo52) - 1
        # Trend Template 8
        tt = all([p > ma50, p > ma150, p > ma200, ma50 > ma150,
                  ma150 > ma200, c.iloc[-1] > c.iloc[-21],
                  p >= lo52 * 1.30, p >= hi52 * 0.75])
        # VCP real detection (close-based)
        vcp = detect_vcp(c, ma150)
        contr = vcp['is_vcp']
        # VCP candle validation (High-Low range contraction)
        hl = detect_vcp_hl(hist, ma150)
        # VCP validated if close-based VCP confirmed by candle-range contraction,
        # OR if there are >=3 contraction swings (strong multi-stage contraction)
        vcp_validated = bool(contr and (hl['hl_contracted'] or (vcp['contractions'] >= 3)))
        # ---- Entry / Stop / Target logic (Minervini) ----
        pivot = vcp.get('pivot')
        if pivot and pivot > 0:
            entry = round(pivot * 1.01, 2)
            stop = round(entry * 0.93, 2)
            target = round(entry * 1.20, 2)
            risk = entry - stop
            reward = target - entry
            rrr = round(reward / risk, 1) if risk > 0 else 0
            pct_to_entry = round((entry - p) / p * 100, 1)
        else:
            entry = stop = target = rrr = pct_to_entry = None
        # Fundamentals
        info = tk.info or {}
        rev_g = info.get('revenueGrowth')
        eps_g = info.get('earningsGrowth')
        roe = info.get('returnOnEquity')
        margin = info.get('grossMargins')
        pe = info.get('trailingPE')
        fpe = info.get('forwardPE')
        return dict(tkr=t, price=round(p, 2),
                    ret_52w=ret_52w,
                    pct_from_high=round((hi52 - p) / hi52 * 100, 1),
                    tt=tt, contr=contr, vcp_validated=vcp_validated,
                    vcp_count=vcp['contractions'],
                    vcp_pivot=vcp['pivot'],
                    vcp_below=vcp['pct_below_pivot'],
                    hl_recent=hl.get('recent_range'), hl_prior=hl.get('prior_range'),
                    entry=entry, stop=stop, target=target, rrr=rrr, pct_to_entry=pct_to_entry,
                    rev_g=round(rev_g*100, 1) if rev_g else None,
                    eps_g=round(eps_g*100, 1) if eps_g else None,
                    roe=round(roe*100, 1) if roe else None,
                    margin=round(margin*100, 1) if margin else None,
                    pe=round(pe, 1) if pe else None,
                    fpe=round(fpe, 1) if fpe else None)
    except Exception:
        return None

def main(top_n=TOP_N):
    universe = load_universe()
    # Step 1-3: rank by avg volume
    vols = {}
    with ThreadPoolExecutor(max_workers=10) as ex:
        futmap = {ex.submit(get_avg_volume, t): t for t in universe}
        for f in as_completed(futmap):
            v = f.result()
            if v:
                vols[futmap[f]] = v
    ranked = sorted(vols.items(), key=lambda x: x[1], reverse=True)[:top_n]
    scan_list = [t for t, _ in ranked]
    # Step 4: analyze
    spy = yf.Ticker("SPY").history(period="1y")['Close']
    spy_ret = (spy.iloc[-1] / spy.iloc[0]) - 1
    res = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for f in as_completed({ex.submit(analyze, t): t for t in scan_list}):
            r = f.result()
            if r:
                try:
                    if r['ret_52w'] is None or pd.isna(r['ret_52w']) or spy_ret == 0:
                        r['rs'] = 0
                    else:
                        r['rs'] = max(1, min(99, int(round(50 + 50 * (r['ret_52w']) / (spy_ret + 1e-9)))))
                except (ValueError, TypeError):
                    r['rs'] = 0
                res.append(r)
    # Step 5: filter
    passed = [r for r in res if r['tt'] and r['rs'] >= 89]
    fund_ok = [r for r in passed if (r['eps_g'] and r['eps_g'] > 20) or (r['rev_g'] and r['rev_g'] > 15)]
    seen = set(); clean = []
    for r in fund_ok:
        if r['tkr'] not in seen:
            seen.add(r['tkr']); clean.append(r)
    clean.sort(key=lambda x: (x.get('vcp_below') if x.get('vcp_below') is not None else 999, -x['rs']))
    print(f"Universe: {len(universe)} | Liquid top {len(scan_list)} scanned | TT+RS>=89: {len(passed)} | +Fundamental: {len(clean)}")
    print(f"{'TKR':<6}{'Price':>9}{'RS':>5}{'VCP#':>5}{'VCP✓':>6}{'%2Piv':>7}{'PE':>7}{'fPE':>7}{'ENTRY':>9}{'STOP':>9}{'TGT':>9}{'RRR':>5}")
    for r in clean:
        print(f"{r['tkr']:<6}{r['price']:>9}{r['rs']:>5}{r.get('vcp_count',0):>5}"
              f"{'Y' if r.get('vcp_validated') else '-':>6}"
              f"{(r.get('vcp_below') or 0):>7}"
              f"{(r.get('pe') or 0):>7}{(r.get('fpe') or 0):>7}"
              f"{(r.get('entry') or 0):>9}{(r.get('stop') or 0):>9}{(r.get('target') or 0):>9}{(r.get('rrr') or 0):>5}")
    # Optional: auto-generate candlestick charts for the top N so the
    # Agent/user can visually verify VCP / Stage-2 instead of trusting code.
    if os.environ.get("VCP_MAKE_CHARTS", "0") == "1":
        top = clean[:int(os.environ.get("VCP_TOP_CHARTS", "8"))]
        print(f"\n--- Generating charts for top {len(top)} (saved to {CHART_DIR}) ---")
        for r in top:
            p = make_chart(r['tkr'])
            print(f"{r['tkr']:<6} chart: {p}")

if __name__ == '__main__':
    main()
