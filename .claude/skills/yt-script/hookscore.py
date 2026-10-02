#!/usr/bin/env python3
"""hookscore.py - puntúa un gancho de YouTube antes de malgastar una toma en él.

Cinco propiedades, de 0 a 100 cada una, y un veredicto que es un 60% la media y un 40% la más débil.
El peso del eslabón más débil es deliberado: un gancho con cuatro propiedades fuertes y una muerta
pierde gente por la muerta, y la media lo esconde.

    python3 hookscore.py ganchos.txt            # un gancho por línea, ordenados
    python3 hookscore.py --hook "una frase"     # puntúa un solo gancho
    python3 hookscore.py --json ganchos.txt     # salida para máquinas

Reconoce español e inglés.

QUÉ PUEDE Y QUÉ NO PUEDE DECIRTE. Medido con 74 ganchos reales de formato corto en inglés (primeros
15 segundos de subtítulos automáticos, los 8 mejores y los 8 peores por visitas de cinco canales):
separa bien los ganchos malos a propósito de los reales, y casi no separa los éxitos de un creador
de sus fracasos. Las listas de palabras en español son una adaptación sin calibrar. Toma una nota
baja como motivo para mirar otra vez, y nunca una nota alta como una promesa.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
FORMULAS = json.load(open(os.path.join(HERE, "hooks.json"), encoding="utf-8"))["hooks"]

FILLER = {"basically","actually","literally","just","really","very","so","kind","sort","like",
          "guys","hey","welcome","today","video","subscribe","channel",
          "básicamente","basicamente","literalmente","realmente","simplemente","muy","pues","bueno",
          "tipo","chicos","chicas","gente","hola","bienvenidos","bienvenidas","hoy","vídeo",
          "suscríbete","suscribete","canal"}
VAGUE = {"amazing","incredible","insane","crazy","huge","massive","game","changer","secret",
         "powerful","ultimate","best","revolutionary","mind","blowing","unbelievable",
         "increíble","increible","increíbles","brutal","bestial","locura","enorme","enormes",
         "secreto","secretos","potente","definitivo","definitiva","mejor","revolucionario",
         "alucinante","impresionante","espectacular","épico","épica","epico","epica"}
CONCRETE = re.compile(r"\b(\d[\d,.]*\s?(%|k|m|x|s|m|h)?|\$\d|\d+\s?(second|minute|hour|day|week|month|year)s?"
                      r"|\d+\s?(segundos?|minutos?|horas?|d[ií]as?|semanas?|mes(es)?|años?)|\d[\d,.]*\s?€)", re.I)
YOU = re.compile(r"\b(you|your|you're|youre|yourself"
                 r"|t[uú]|tus|te|ti|contigo|usted|ustedes|vosotr[oa]s|os|vuestr[oa]s?"
                 # en español el "tú" suele ir en el verbo: "si tienes", "¿sabes por qué...?"
                 r"|tienes|eres|est[aá]s|haces|puedes|quieres|sabes|necesitas|vas|subes|publicas)\b", re.I)
STAKE = re.compile(r"\b(lose|lost|wasting|waste|quit|fail|broke|cost|risk|before|stop|never|die|dying|dead"
                   r"|perder|pierdes|perdiste|perdido|desperdicias|malgastas|tirando|dejarlo|abandonar"
                   r"|fracasa\w*|cuesta|cost[oó]|riesgo|antes|nunca|jam[aá]s|muere|muerto|deja de)\b", re.I)
CURIOSITY = re.compile(r"\b(why|how|what|which|until|before|but|nobody|almost|except|reason|actually"
                       r"|por qu[eé]|c[oó]mo|qu[eé]|cu[aá]l|hasta|pero|nadie|casi|excepto|salvo|raz[oó]n"
                       r"|motivo|en realidad)\b", re.I)

def words(t): return re.findall(r"[\w'%$.]+", t.lower())

def specificity(t):
    w = words(t)
    if not w: return 0
    nums = len(CONCRETE.findall(t))
    vague = sum(1 for x in w if x in VAGUE)
    filler = sum(1 for x in w if x in FILLER)
    s = 34 + nums * 22 - vague * 16 - filler * 5
    # los nombres propios que no abren la frase cuentan como cosas con nombre
    s += min(18, 6 * sum(1 for x in t.split()[1:] if x[:1].isupper()))
    return max(0, min(100, s))

def address(t):
    n = len(YOU.findall(t))
    first = 30 if YOU.search(" ".join(t.split()[:6])) else 0
    return max(0, min(100, 26 + n * 20 + first))

def stakes(t):
    n = len(STAKE.findall(t))
    return max(0, min(100, 22 + n * 26 + (14 if CONCRETE.search(t) else 0)))

def curiosity(t):
    n = len(CURIOSITY.findall(t))
    q = 18 if t.strip().endswith("?") else 0
    # un gancho que se responde solo no deja ninguna pregunta abierta
    closed = -18 if re.search(r"\b(because|so that|which means|porque|para que|lo que significa|es decir)\b",
                              t, re.I) else 0
    return max(0, min(100, 24 + n * 17 + q + closed))

def brevity(t):
    n = len(words(t))
    if n == 0: return 0
    # 9-24 palabras es lo que cabe de un gancho hablado a ~150 palabras/min en 10 segundos
    if 9 <= n <= 24: return 100
    if n < 9:  return max(30, 100 - (9 - n) * 11)
    return max(10, 100 - (n - 24) * 7)

PROPS = [("CONCRECIÓN", specificity), ("INTERPELA", address), ("EN JUEGO", stakes),
         ("CURIOSIDAD", curiosity), ("BREVEDAD", brevity)]

def classify(t):
    best, hits = None, 0
    for f in FORMULAS:
        n = sum(1 for p in f["match"] if re.search(p, t, re.I))
        if n > hits: best, hits = f, n
    return (best["name"] if best else "Sin clasificar"), hits

def score(t):
    parts = {n: fn(t) for n, fn in PROPS}
    vals = list(parts.values())
    verdict = round(0.6 * (sum(vals) / len(vals)) + 0.4 * min(vals))
    name, hits = classify(t)
    return parts, verdict, name, hits

def band(v): return "FUERTE" if v >= 72 else "APROVECHABLE" if v >= 55 else "DÉBIL"

def report(t, parts, verdict, name, hits):
    print(f"\n  {t.strip()}")
    print(f"  {'-' * min(72, max(20, len(t.strip())))}")
    for k, v in parts.items():
        print(f"    {k:<12} {v:3d}  {'#' * (v // 5)}")
    print(f"    {'VEREDICTO':<12} {verdict:3d}  {band(verdict)}")
    print(f"    fórmula      {name}" + (f"  ({hits} patrón{'es' if hits != 1 else ''} coincide{'n' if hits != 1 else ''})" if hits else "  (ninguna fórmula coincide: suele ser un resumen, no un gancho)"))
    low = min(parts, key=parts.get)
    print(f"    más débil    {low} - {FIX[low]}")

FIX = {
 "CONCRECIÓN": "cambia un adjetivo por un número, un nombre o una fecha",
 "INTERPELA": "háblale de tú en las seis primeras palabras",
 "EN JUEGO": "di qué le cuesta seguir haciéndolo como hasta ahora",
 "CURIOSIDAD": "quita la mitad de la frase que se responde sola",
 "BREVEDAD": "de 9 a 24 palabras. Léelo en voz alta y para donde te quedes sin aire",
}

def main():
    a = sys.argv[1:]
    as_json = "--json" in a
    a = [x for x in a if x != "--json"]
    if "--hook" in a:
        lines = [a[a.index("--hook") + 1]]
    elif a and os.path.exists(a[0]):
        lines = [l for l in open(a[0]).read().splitlines() if l.strip()]
    else:
        print(__doc__); sys.exit(1 if not a else 0)
    out = []
    for t in lines:
        parts, verdict, name, hits = score(t)
        out.append({"hook": t.strip(), "properties": parts, "verdict": verdict,
                    "band": band(verdict), "formula": name, "matched": hits})
    out.sort(key=lambda r: -r["verdict"])
    if as_json:
        print(json.dumps([{k: v for k, v in r.items() if k != "matched"} for r in out], indent=1)); return
    for r in out:
        report(r["hook"], r["properties"], r["verdict"], r["formula"], r["matched"])
    if len(out) > 1:
        print(f"\n  ganador: {out[0]['hook'].strip()}  ({out[0]['verdict']}, {out[0]['band']})\n")

if __name__ == "__main__":
    main()
