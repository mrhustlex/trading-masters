"""Master consolidated screen — runs ALL trading-master methods on a ticker list
and prints a single matrix: which masters flag each stock, plus a "strongest ideas"
list (flagged by 3+ methods).

Methods wired:
  Minervini VCP      -> scripts/minervini_scanner.py  (analyze)
  O'Neil CAN SLIM    -> skills/oneil-canslim/references/canslim.py (analyze)
  Weinstein Stage    -> skills/weinstein-stage/references/stage.py (analyze)
  Darvas Box         -> skills/darvas-box/references/darvas.py (analyze)
  Wyckoff            -> skills/wyckoff/references/wyckoff.py (analyze)
  Buffett/Graham     -> skills/buffett-graham/references/value.py (analyze)
  Peter Lynch PEG    -> skills/peter-lynch/references/peg.py (analyze)
  Greenblatt Magic   -> skills/greenblatt-magic/references/magic.py (magic) [rank pass]

Run:
  python3 master_screen.py NVDA APH AMD MU TER GRMN EMR NTAP SMCI GLW BB SNDK
  python3 master_screen.py --universe universe.txt --top 25
"""
import sys, os, time, warnings, argparse
warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")            # trading-masters/
SKILLS = os.path.join(ROOT, "skills")      # trading-masters/skills

# --- import each method's module safely ---
def load(rel):
    p = os.path.join(ROOT, rel)            # rel is like "skills/.../x.py" or "minervini_scanner.py"
    sys.path.insert(0, os.path.dirname(p))
    try:
        mod = __import__(os.path.basename(p).replace(".py",""))
        return mod
    except Exception as e:
        print(f"  [warn] could not load {rel}: {e}", file=sys.stderr)
        return None

M = {
    "Minervini_VCP": (lambda: (__import__("minervini_scanner")))(),
    "O'Neil_CANSLIM": load("skills/oneil-canslim/references/canslim.py"),
    "Weinstein_Stage": load("skills/weinstein-stage/references/stage.py"),
    "Darvas_Box": load("skills/darvas-box/references/darvas.py"),
    "Wyckoff": load("skills/wyckoff/references/wyckoff.py"),
    "Buffett_Value": load("skills/buffett-graham/references/value.py"),
    "Lynch_PEG": load("skills/peter-lynch/references/peg.py"),
    "Greenblatt_Magic": load("skills/greenblatt-magic/references/magic.py"),
}

def safe(fn, t):
    try: return fn(t)
    except Exception: return None

def flags(t):
    """Return dict method-> (bool pass, short note)."""
    out = {}
    # Minervini VCP
    if M["Minervini_VCP"]:
        r = safe(M["Minervini_VCP"].analyze, t)
        if r: out["VCP"] = (bool(r.get("vcp_validated")), f"RS{r.get('rs')}")
    # O'Neil CANSLIM
    if M["O'Neil_CANSLIM"]:
        r = safe(M["O'Neil_CANSLIM"].analyze, t)
        if r: out["CANSLIM"] = (bool(r.get("passed")), r.get("base",""))
    # Weinstein Stage
    if M["Weinstein_Stage"]:
        r = safe(M["Weinstein_Stage"].classify, t)
        if r: out["Stage2"] = (r.get("stage")==2, f"S{r.get('stage')}")
    # Darvas
    if M["Darvas_Box"]:
        r = safe(M["Darvas_Box"].analyze, t)
        if r: out["Darvas"] = (r.get("break")=="YES" or r.get("newBox")=="YES",
                                f"{r.get('floor')}-{r.get('ceiling')}")
    # Wyckoff
    if M["Wyckoff"]:
        r = safe(M["Wyckoff"].analyze, t)
        if r: out["Wyckoff"] = (r.get("accum")=="Y", "accum" if r.get("accum")=="Y" else "")
    # Buffett value
    if M["Buffett_Value"]:
        r = safe(M["Buffett_Value"].analyze, t)
        if r: out["Value"] = (bool(r.get("passed")), f"sc{r.get('score')}")
    # Lynch PEG
    if M["Lynch_PEG"]:
        r = safe(M["Lynch_PEG"].analyze, t)
        if r: out["PEG<=1"] = (bool(r.get("passed")), f"peg{r.get('peg')}")
    # Greenblatt Magic (rank pass: appears in top list)
    if M["Greenblatt_Magic"]:
        try:
            rk = M["Greenblatt_Magic"].magic(t)
            out["Magic"] = (rk is not None, "rank" if rk else "")
        except Exception: out["Magic"] = (False, "")
    return out

ORDER = ["VCP","CANSLIM","Stage2","Darvas","Wyckoff","Value","PEG<=1","Magic"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="*")
    ap.add_argument("--universe", default=os.path.join(HERE,"universe.txt"))
    ap.add_argument("--top", type=int, default=999)
    a = ap.parse_args()
    if a.tickers: tkrs = a.tickers
    elif os.path.exists(a.universe): tkrs = open(a.universe).read().split()
    else: tkrs = ["NVDA","APH","AMD","MU","TER","GRMN","EMR","NTAP","SMCI","GLW","BB","SNDK"]
    tkrs = tkrs[:a.top]
    print(f"\n=== MASTER SCREEN: {len(tkrs)} tickers x 8 methods ===\n")
    hdr = f"{'TKR':<6}" + "".join(f"{c:>9}" for c in ORDER) + f"{'#hit':>6}"
    print(hdr)
    results = []
    for t in tkrs:
        fl = flags(t)
        row = f"{t:<6}"
        hits = 0
        for c in ORDER:
            if c in fl:
                ok, note = fl[c]
                if ok: hits += 1
                row += f"{(('Y '+note) if ok else '-'):>9}"
            else:
                row += f"{'-':>9}"
        row += f"{hits:>6}"
        print(row)
        if hits: results.append((t, hits, fl))
    results.sort(key=lambda x:-x[1])
    print("\n=== STRONGEST IDEAS (flagged by 3+ masters) ===")
    strong = [r for r in results if r[1] >= 3]
    if strong:
        for t, h, fl in strong:
            ms = [c for c in ORDER if c in fl and fl[c][0]]
            print(f"  {t}: {h}/8  -> {', '.join(ms)}")
    else:
        print("  (none flagged by 3+ on this list)")
    print("\nLegend: VCP=Minervini, CANSLIM=O'Neil, Stage2=Weinstein, Darvas=Box breakout,")
    print("        Wyckoff=accumulation, Value=Buffett/Graham, PEG<=1=Lynch, Magic=Greenblatt rank")

if __name__ == "__main__":
    main()
