#!/usr/bin/env python3
"""chapters.py - capítulos de YouTube a partir de una transcripción con tiempos.

    python3 chapters.py transcripcion.srt            # o .vtt / .json de whisper
    python3 chapters.py transcripcion.srt --target 8 --json

Imprime un bloque de descripción que puedes pegar directamente debajo de un vídeo. Las reglas de
YouTube se comprueban aquí en vez de darse por hechas: la lista tiene que empezar en 00:00, necesita
al menos tres entradas y cada capítulo tiene que durar al menos 10 segundos. Un bloque que incumple
alguna no se convierte en capítulos y nadie te avisa, por eso esto lo comprueba.

Los límites salen de los huecos (las pausas que hiciste de verdad entre secciones), puntuados por lo
larga que fue la pausa y por cuánto cambia el vocabulario a cada lado. Es un primer borrador que
vuelves a titular, no un resumidor. Reconoce español e inglés.
"""
import json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "yt-edit"))
from deadair import load, parse_ts  # noqa: E402  (same parser, one implementation)

STOP = set("the a an of for to in on and or is are was were be been with this that it as at by from "
           "you your i my we our they them he she but so if then than there here what which who how "
           "when where why not no yes do does did just really very like about into over out up down "
           "can could will would should have has had get got make made go going went one two".split()) | set(
           "para como cómo pero esto esta este estos estas todo toda todos todas cuando cuándo donde "
           "dónde porque entonces también aquí ahí allí hacer hago hace hacemos tiene tienes tengo "
           "tenemos puede puedes puedo podemos vamos sobre entre desde hasta más menos algo nada cosa "
           "cosas bueno pues vale ahora solo sólo mismo misma otro otra otros otras cada había sido "
           "estar estoy está están estamos eres somos quiero quieres decir digo dice creo mucho mucha "
           "muchos muchas poco bien ellos ellas nosotros vosotros ustedes usted vídeo video vídeos "
           "videos verdad tipo bastante siempre nunca luego antes después tanto cual cuál cuales "
           "quien quién sabes mira mirad gente básicamente basicamente realmente".split())

def keywords(text):
    return {w for w in re.findall(r"[^\W\d_](?:[^\W\d_]|'){3,}", text.lower()) if w not in STOP}

def mmss(t):
    t = int(t); h, m, s = t // 3600, (t % 3600) // 60, t % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def main():
    a = sys.argv[1:]
    as_json = "--json" in a; a = [x for x in a if x != "--json"]
    target = int(a[a.index("--target") + 1]) if "--target" in a else 7
    a = [x for x in a if not x.startswith("--") and not x.isdigit()]
    if not a or not os.path.exists(a[0]): print(__doc__); sys.exit(1)
    cues = load(a[0])
    if len(cues) < 6: print("hay muy pocos fragmentos para dividir en capítulos"); sys.exit(1)
    dur = cues[-1][1]
    cand = []
    for i in range(1, len(cues)):
        gap = cues[i][0] - cues[i - 1][1]
        before = " ".join(c[2] for c in cues[max(0, i - 12):i])
        after = " ".join(c[2] for c in cues[i:i + 12])
        kb, ka = keywords(before), keywords(after)
        shift = 1 - (len(kb & ka) / len(kb | ka)) if (kb | ka) else 0
        cand.append((gap * 1.6 + shift * 3.2, cues[i][0], i))
    cand.sort(reverse=True)
    picked, MIN = [0.0], 10.0
    for _, t, i in cand:
        if len(picked) >= target: break
        if all(abs(t - p) >= MIN for p in picked) and dur - t >= MIN:
            picked.append(t)
    picked.sort()
    chapters = []
    for n, t in enumerate(picked):
        end = picked[n + 1] if n + 1 < len(picked) else dur
        text = " ".join(c[2] for c in cues if c[0] >= t and c[1] <= end)
        kw = [w for w in keywords(text)]
        kw.sort(key=lambda w: -text.lower().count(w))
        title = " ".join(w.capitalize() for w in kw[:3]) or "Sección"
        chapters.append({"start": round(t, 2), "label": mmss(t), "draft_title": title,
                         "seconds": round(end - t, 2)})
    ok = len(chapters) >= 3 and chapters[0]["start"] == 0 and all(c["seconds"] >= MIN for c in chapters)
    if as_json:
        print(json.dumps({"valid": ok, "chapters": chapters}, indent=1)); return
    print()
    for c in chapters: print(f"  {c['label']} {c['draft_title']}")
    print(f"\n  {len(chapters)} capítulos"
          f"{'' if ok else '  -- NO VÁLIDO: YouTube necesita 3 o más, la primera en 00:00 y 10 s como mínimo cada uno'}")
    print("  Vuelve a titular cada línea antes de pegarla. Son las palabras del tema, no las tuyas.\n")

if __name__ == "__main__":
    main()
