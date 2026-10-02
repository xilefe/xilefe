---
name: yt-edit
description: >-
  Convierte la transcripción de una grabación en bruto en una lista de
  decisiones de edición: silencios, muletillas y repeticiones, con códigos de
  tiempo. Úsala para "edita esto", "quita los silencios", "acorta este
  vídeo", "me enrollé", o cualquier petición de recortar material a partir de
  una transcripción.
---

# yt-edit

Una lista de decisiones de edición (EDL) a partir de una transcripción con marcas de tiempo. Imprime
los cortes. Tú los aplicas.

```bash
python3 deadair.py transcripcion.srt              # srt, vtt o json de whisper
python3 deadair.py transcripcion.srt --floor 0.35 --json
```

¿Todavía no hay transcripción? Pídela o genérala primero: `whisper`, `faster-whisper` o los
subtítulos automáticos que crea YouTube al subir un vídeo oculto sirven. No adivines los tiempos.

## Qué encuentra

- **SILENCIO**: huecos más largos que el umbral, recortados por el MEDIO para que a los dos lados
  quede una respiración. Cortar pegado a la voz es lo que hace que una toma acortada suene sin aliento.
- **MULETILLA**: fragmentos que no son más que "eh", "pues nada", "o sea", "básicamente".
- **REPETICIÓN**: una frase que se vuelve a empezar. Se compara con el último fragmento que tenía
  habla de verdad, no con el anterior literal, porque la mayoría de las repeticiones tienen un "eh"
  entre los dos intentos.

## Qué no hace

No toca el vídeo. No opina sobre tus recursos (B-roll). Un recorte del 40% en el informe es un
40% del HABLA; si el vídeo tiene una demostración larga sin voz, ese número está mal. Compara el
informe con el material antes de fiarte de la duración final.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
