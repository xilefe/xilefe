#!/usr/bin/env python3
"""retention.py - lee una exportación de retención de audiencia de YouTube Studio y encuentra las fugas.

    python3 retention.py retencion.csv
    python3 retention.py retencion.csv --transcript transcripcion.srt   # dice qué se decía en cada caída
    python3 retention.py retencion.csv --json

Consigue el archivo en Studio: un vídeo -> Estadísticas -> Interacción -> el gráfico de retención de
la audiencia -> el icono de descarga -> "Retención de la audiencia". Dos columnas: una posición
(porcentaje o segundos) y el porcentaje que sigue viendo.

Informa de tres cosas, porque son tres problemas distintos con tres arreglos distintos:
  FUGA EN EL GANCHO   lo que perdiste en los primeros 30 segundos
  CAÍDAS              bajadas bruscas puntuales: un momento concreto en el que la gente se fue
  GOTEO               el ritmo de pérdida constante en la parte central

Con --transcript imprime lo que estabas diciendo en cada caída, que es la única versión de este
informe sobre la que puedes actuar sin revisar el vídeo tú mismo.
"""
import csv, json, os, re, sys

def load_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        for r in csv.reader(fh):
            nums = []
            for c in r:
                c = c.strip().replace("%", "").replace(",", "")
                try: nums.append(float(c))
                except ValueError: nums.append(None)
            vals = [n for n in nums if n is not None]
            if len(vals) >= 2: rows.append((vals[0], vals[1]))
    return rows

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    tr = a[a.index("--transcript") + 1] if "--transcript" in a else None
    files = [x for x in a if not x.startswith("--") and x != tr]
    if not files or not os.path.exists(files[0]): print(__doc__); sys.exit(1)
    rows = load_csv(files[0])
    if len(rows) < 8: print("no se han podido leer al menos 8 puntos de datos de ese csv"); sys.exit(1)
    xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
    pct_axis = max(xs) <= 100.5
    dur = None
    if "--duration" in a: dur = float(a[a.index("--duration") + 1])
    def at(x): return (x / 100.0 * dur) if (pct_axis and dur) else x
    start = ys[0] or 100.0
    # GANCHO: los primeros 30 segundos, o el primer 10% si el eje es un porcentaje y no hay duración
    cutoff = 30.0 if not pct_axis else (30.0 / dur * 100 if dur else 10.0)
    hook_end = min((y for x, y in rows if x <= cutoff), default=start)
    hook_leak = start - hook_end
    drops = []
    for i in range(1, len(rows)):
        d = ys[i - 1] - ys[i]
        span = xs[i] - xs[i - 1] or 1
        drops.append((d / span, xs[i - 1], xs[i], d))
    drops.sort(reverse=True)
    cliffs = [{"from": round(a1, 2), "to": round(b1, 2), "lost": round(d, 2),
               "at_seconds": round(at(a1), 1) if (not pct_axis or dur) else None}
              for _, a1, b1, d in drops[:5] if d > 0.8]
    mid = [d for d, x0, _, _ in [(r[0], r[1], r[2], r[3]) for r in drops] if x0 > cutoff]
    slide = sum(mid) / len(mid) if mid else 0
    said = {}
    if tr and os.path.exists(tr):
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
        from deadair import load as load_cues
        cues = load_cues(tr)
        for c in cliffs:
            if c["at_seconds"] is None: continue
            t = c["at_seconds"]
            near = [q[2] for q in cues if q[0] <= t + 4 and q[1] >= t - 4]
            said[str(c["from"])] = " ".join(near)[:140]
    out = {"points": len(rows), "start": start, "hook_leak": round(hook_leak, 2),
           "end": ys[-1], "cliffs": cliffs, "slide_per_unit": round(slide, 3), "said": said}
    if as_json: print(json.dumps(out, indent=1)); return
    print(f"\n  {files[0]}   {len(rows)} puntos   {ys[0]:.1f}% -> {ys[-1]:.1f}%\n")
    verdict = "sana" if hook_leak < 25 else "con fuga" if hook_leak < 40 else "grave"
    print(f"  FUGA EN EL GANCHO   {hook_leak:.1f}% perdido en el arranque   [{verdict}]")
    print(f"                      menos de 25 es sano para esta duración. Arregla la primera frase antes que nada.\n")
    print("  CAÍDAS              los momentos en los que la gente se fue de verdad")
    for c in cliffs:
        where = f"{c['at_seconds']:.0f}s" if c["at_seconds"] is not None else f"{c['from']}"
        print(f"    -{c['lost']:5.1f}%  en {where:>8}" + (f"   \"{said.get(str(c['from']),'')}\"" if said else ""))
    if not cliffs: print("    ninguna de más del 0,8%: la pérdida es todo goteo, no momentos")
    print(f"\n  GOTEO               {slide:.3f}% por unidad en la parte central")
    print( "                      un goteo uniforme es cuestión de ritmo, no de contenido. Recorta la parte central, no la reescribas.\n")

if __name__ == "__main__":
    main()
