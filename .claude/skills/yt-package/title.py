#!/usr/bin/env python3
"""title.py - revisa la pareja título + miniatura de YouTube antes de publicarla.

    python3 title.py --title "..." --thumb "LA IA LO HIZO"
    python3 title.py titulos.txt            # uno por línea, ordenados
    python3 title.py --title "..." --json

La unidad es la pareja, no el título. Un título que repite el texto de la miniatura desperdicia la
mitad de lo que invita al clic, y es el error más común que comprueba esto.

Longitud: YouTube corta hacia los 60 caracteres en la búsqueda en ordenador y hacia los 40 en el
feed de inicio del móvil. Se informan los dos porque son fallos distintos: el corte en ordenador
pierde el final, el del móvil puede perder el tema.

Reconoce español e inglés.
"""
import json, re, sys, os

DESKTOP, MOBILE, HARD = 60, 40, 100
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","ultimate","best","powerful",
         "secret","revolutionary","mindblowing","epic","perfect","complete","everything",
         "increíble","increible","brutal","bestial","locura","enorme","definitivo","definitiva",
         "mejor","potente","secreto","revolucionario","alucinante","épico","épica","epico","epica",
         "perfecto","perfecta","completo","completa","todo","impresionante","espectacular"}
STOP = {"the","a","an","of","for","to","in","on","and","or","is","are","with","your","you","my","i",
        "this","that","it","how","what","why",
        "el","la","los","las","un","una","unos","unas","de","del","al","para","por","en","y","o",
        "es","son","con","tu","tus","mi","mis","yo","este","esta","esto","ese","esa","eso","lo",
        "que","qué","cómo","como","porqué","se","te","me","su","sus"}

# "por qué" son dos palabras donde el inglés usa una ("why"): se cuenta como una sola
def words(t): return re.findall(r"[\w']+", re.sub(r"\bpor qu[eé]\b", "porqué", t.lower()))

def check(title, thumb=None):
    t = title.strip()
    n = len(t)
    issues, good = [], []
    if n > HARD: issues.append(("longitud", f"{n} caracteres - el límite de YouTube es {HARD}"))
    elif n > DESKTOP: issues.append(("longitud", f"{n} caracteres - la búsqueda en ordenador corta hacia los {DESKTOP}"))
    else: good.append(f"{n} caracteres, dentro del corte de {DESKTOP} en ordenador")
    if n > MOBILE:
        head = t[:MOBILE].rsplit(" ", 1)[0]
        issues.append(("móvil", f'el feed del móvil muestra más o menos "{head}..." - comprueba que el tema se ve'))
    caps = [w for w in t.split() if len(w) > 2 and w.isupper()]
    if len(caps) > 2: issues.append(("gritos", f"{len(caps)} palabras en mayúsculas - dos es el techo antes de parecer spam"))
    elif caps: good.append(f"{len(caps)} palabra{'s' if len(caps) > 1 else ''} en mayúsculas para dar énfasis")
    v = [w for w in words(t) if w in VAGUE]
    if v: issues.append(("vago", f"{', '.join(sorted(set(v)))} - cámbialo por un número, un nombre o una fecha"))
    nums = re.findall(r"\d[\d,.]*%?", t)
    if nums: good.append(f"lleva una cifra concreta ({', '.join(nums[:3])})")
    else: issues.append(("sin-número", "sin número, fecha ni nombre - el arreglo más fiable"))
    if t.endswith("?"): good.append("pregunta abierta en el título")
    front = [w for w in words(t)[:3] if w not in STOP]
    if not front: issues.append(("arranque", "las tres primeras palabras son relleno - adelanta el tema"))
    if thumb:
        tw, hw = set(words(t)) - STOP, set(words(thumb)) - STOP
        shared = tw & hw
        if shared:
            issues.append(("repetido", f"la miniatura repite el título en {', '.join(sorted(shared))} - "
                                       "la miniatura debe decir lo que el título no dice"))
        else:
            good.append("miniatura y título usan palabras distintas")
        if len(words(thumb)) > 4:
            issues.append(("miniatura", f"{len(words(thumb))} palabras en la miniatura - tres es el techo al tamaño del feed"))
    score = max(0, min(100, 100 - 14 * len(issues) + 4 * len(good)))
    return {"title": t, "chars": n, "score": score, "issues": issues, "good": good}

def show(r):
    print(f'\n  "{r["title"]}"')
    print(f"  {r['chars']} caracteres   nota {r['score']}/100")
    for k, m in r["issues"]: print(f"    x  {k:<12} {m}")
    for m in r["good"]:      print(f"    ok              {m}")

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    thumb = a[a.index("--thumb") + 1] if "--thumb" in a else None
    if "--title" in a:
        rows = [check(a[a.index("--title") + 1], thumb)]
    elif a and os.path.exists(a[0]):
        rows = [check(l, thumb) for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1)
    rows.sort(key=lambda r: -r["score"])
    if as_json: print(json.dumps(rows, indent=1)); return
    for r in rows: show(r)
    print()

if __name__ == "__main__":
    main()
