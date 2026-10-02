#!/usr/bin/env python3
"""swipe.py - ordena vídeos recopilados según cuánto superó cada uno a SU PROPIO canal y nombra la fórmula.

    python3 swipe.py recopilados.json
    python3 swipe.py recopilados.json --min 2.0 --json

La entrada es una lista que has reunido, un objeto por vídeo:

    [{"channel":"Un canal","title":"...","views":412000,"url":"...","duration":613}, ...]

Las visitas en bruto ordenan por tamaño del canal, no por ideas. Un vídeo de 400.000 visitas en un
canal de 2 millones de suscriptores es un martes cualquiera; uno de 400.000 en un canal cuya mediana
es 30.000 es lo que merece la pena estudiar. Por eso cada vídeo se puntúa como un MÚLTIPLO DE LA
MEDIANA DE SU PROPIO CANAL, que necesita al menos cuatro vídeos por canal para significar algo: la
herramienta lo avisa en vez de ordenar ruido sin decir nada.

La fórmula sale de yt-script/hooks.json, comparada con el TÍTULO (en español o en inglés). Es una
valoración de las palabras que se ven, no una afirmación sobre por qué funcionó el vídeo.
"""
import json, os, re, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "..", "yt-script", "hooks.json"), encoding="utf-8"))["hooks"]

def classify(title):
    scored = []
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, title, re.I))
        if n: scored.append((n, f["name"]))
    scored.sort(reverse=True)
    return scored[0][1] if scored else "Sin clasificar"

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    lo = float(a[a.index("--min") + 1]) if "--min" in a else 1.5
    files = [x for x in a if not x.startswith("--") and not re.match(r"^[\d.]+$", x)]
    if not files or not os.path.exists(files[0]): print(__doc__); sys.exit(1)
    rows = json.load(open(files[0]))
    if isinstance(rows, dict): rows = rows.get("videos", [])
    by = {}
    for r in rows: by.setdefault(r.get("channel", "?"), []).append(r)
    out, thin = [], []
    for ch, vids in by.items():
        views = [float(v.get("views", 0) or 0) for v in vids]
        med = statistics.median(views) if views else 0
        if len(vids) < 4:
            thin.append((ch, len(vids)))
            continue
        for v in vids:
            m = (float(v.get("views", 0) or 0) / med) if med else 0
            out.append({"channel": ch, "title": v.get("title", ""), "views": int(v.get("views", 0) or 0),
                        "median": int(med), "multiple": round(m, 2),
                        "formula": classify(v.get("title", "")), "url": v.get("url", "")})
    out = [r for r in out if r["multiple"] >= lo]
    out.sort(key=lambda r: -r["multiple"])
    if as_json: print(json.dumps({"outliers": out, "skipped_thin_channels": thin}, indent=1)); return
    print(f"\n  {len(rows)} vídeos de {len(by)} canales, destacados a partir de {lo}x\n")
    for r in out[:25]:
        print(f"    {r['multiple']:5.2f}x  {r['views']:>9,}  vs {r['median']:>9,} mediana  {r['channel'][:22]:<22} {r['title'][:52]}")
        print(f"            {r['formula']}")
    if not out: print("    ninguno supera el umbral: reúne más vídeos por canal o baja --min")
    if thin:
        print(f"\n  se han saltado {len(thin)} canal(es) con menos de 4 vídeos: una mediana de uno o")
        print( "  dos vídeos no es una mediana: " + ", ".join(f"{c} ({n})" for c, n in thin[:6]))
    counts = {}
    for r in out: counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    if counts:
        print("\n  fórmulas entre los destacados")
        for f, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"    {n:2d}x  {f}")
    print()

if __name__ == "__main__":
    main()
