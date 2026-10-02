#!/usr/bin/env python3
"""deadair.py - una lista de decisiones de edición (EDL) a partir de una transcripción con tiempos.

    python3 deadair.py transcripcion.srt            # o .vtt, o .json de whisper
    python3 deadair.py transcripcion.srt --floor 0.35 --json

Encuentra tres cosas e imprime los cortes como una lista sobre la que actuar, en orden de tiempo:
  SILENCIO    huecos entre fragmentos hablados más largos que el umbral
  MULETILLA   fragmentos que solo son relleno ("eh", "pues nada", "o sea", "básicamente")
  REPETICIÓN  una frase que se vuelve a empezar: la segunda toma del mismo arranque

Reconoce muletillas en español y en inglés.

LO QUE NO HACE. No corta el archivo. Imprime una EDL, el total que quitaría y la duración en la que
acabarías, y tú lo aplicas en el editor que uses. Nada de esto toca el vídeo.
"""
import json, os, re, sys

FILLER_ONLY = re.compile(r"^[\s,.¿?¡!-]*((um+|uh+|er+|ah+|so|okay|ok|right|yeah|like|anyway|basically|"
                         r"actually|you know|i mean|let me see|hold on|"
                         r"e+h+|e+m+|m+|mm+|este|pues|pues nada|bueno|vale|venga|o sea|tipo|en plan|"
                         r"a ver|s[ií]|sabes|vamos|es decir|digamos|b[aá]sicamente|en fin|nada)[\s,.¿?¡!-]*)+$", re.I)

def parse_ts(s):
    s = s.strip().replace(",", ".")
    p = s.split(":")
    return int(p[0]) * 3600 + int(p[1]) * 60 + float(p[2]) if len(p) == 3 else int(p[0]) * 60 + float(p[1])

def load(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".json"):
        d = json.loads(raw)
        segs = d.get("segments", d if isinstance(d, list) else [])
        return [(float(s["start"]), float(s["end"]), (s.get("text") or "").strip()) for s in segs]
    cues, cur = [], None
    for line in raw.splitlines():
        m = re.match(r"\s*(\d[\d:.,]+)\s*-->\s*(\d[\d:.,]+)", line)
        if m:
            cur = [parse_ts(m.group(1)), parse_ts(m.group(2)), []]
            cues.append(cur)
        elif cur is not None and line.strip() and not line.strip().isdigit():
            cur[2].append(line.strip())
    return [(a, b, " ".join(t)) for a, b, t in cues if t]

def norm(t): return re.sub(r"[^\w ]|[\d_]", "", t.lower()).split()

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    floor = float(a[a.index("--floor") + 1]) if "--floor" in a else 0.45
    a = [x for x in a if not x.startswith("--") and not re.match(r"^[\d.]+$", x)]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if not cues: print("no se ha encontrado ningún fragmento: ¿es un srt, un vtt o un json de whisper?"); sys.exit(1)
    dur = cues[-1][1]
    cuts = []
    for i, (s, e, t) in enumerate(cues):
        if FILLER_ONLY.match(t):
            cuts.append({"kind": "MULETILLA", "start": s, "end": e, "why": t.strip()[:48]})
        if i:
            gap = s - cues[i - 1][1]
            if gap > floor:
                keep = floor / 2
                cuts.append({"kind": "SILENCIO", "start": round(cues[i - 1][1] + keep, 3),
                             "end": round(s - keep, 3), "why": f"hueco de {gap:.2f}s"})
        # Una repetición se compara con el último fragmento que era HABLA de verdad. Compararla con
        # el fragmento anterior literal se salta todas las tomas con un "eh" entre los dos intentos,
        # que son la mayoría.
        if t.strip() and not FILLER_ONLY.match(t):
            j = i - 1
            while j >= 0 and (FILLER_ONLY.match(cues[j][2]) or not cues[j][2].strip()): j -= 1
            if j >= 0:
                a1, b1 = norm(cues[j][2])[:5], norm(t)[:5]
                if len(a1) >= 3 and a1 == b1:
                    cuts.append({"kind": "REPETICIÓN", "start": cues[j][0], "end": cues[j][1],
                                 "why": f'vuelve a empezar "{" ".join(a1)}"'})
    cuts = [c for c in cuts if c["end"] > c["start"]]
    cuts.sort(key=lambda c: c["start"])
    removed = sum(c["end"] - c["start"] for c in cuts)
    if as_json:
        print(json.dumps({"source": a[0], "duration": dur, "cuts": cuts,
                          "removed": round(removed, 3), "out": round(dur - removed, 3)}, indent=1)); return
    print(f"\n  {a[0]}   {dur:.2f}s de entrada, {len(cues)} fragmentos, umbral de silencio {floor}s\n")
    for c in cuts:
        print(f"    {c['kind']:<10} {c['start']:8.2f} -> {c['end']:8.2f}   {c['end']-c['start']:5.2f}s   {c['why']}")
    print(f"\n  {len(cuts)} cortes, {removed:.2f}s quitados, {dur - removed:.2f}s de salida "
          f"({removed / dur * 100:.1f}% más corto)\n")

if __name__ == "__main__":
    main()
