---
name: yt-chapters
description: >-
  Escribe los capítulos de un vídeo de YouTube a partir de una transcripción,
  validados contra las reglas de YouTube para que se muestren de verdad.
  Úsala para "añade capítulos", "marcas de tiempo", "timestamps", "divide
  este vídeo en secciones".
---

# yt-chapters

```bash
python3 chapters.py transcripcion.srt --target 8
```

## Las reglas, que no son opcionales

Una lista de capítulos que incumple cualquiera de estas no se convierte en capítulos, y nadie te
avisa: el bloque se queda en la descripción sin hacer nada.

- La primera entrada tiene que ser **00:00**.
- Tiene que haber **al menos tres**.
- Cada uno tiene que durar **al menos 10 segundos**.

La herramienta comprueba las tres y te dice cuándo una lista no es válida, en vez de dejar que la pegues.

## Vuelve a titular cada línea

`chapters.py` encuentra bien los LÍMITES: puntúa las pausas que hiciste de verdad según cuánto cambia
el vocabulario a cada lado. Los títulos que genera son las palabras del tema, y son un borrador. Un
capítulo llamado "Miniaturas Títulos Empaquetado" es un marcador de posición. Reescribe cada uno como
la promesa de esa sección, con la voz del usuario, en tres a cinco palabras.

Los capítulos también diagnostican la retención: si una sección no se puede nombrar en cinco
palabras, son dos secciones o es relleno.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
