---
name: yt-retention
description: >-
  Lee una exportación de retención de audiencia de YouTube Studio, encuentra
  dónde se va realmente la gente y di qué cambiar. Úsala para "por qué la
  gente deja de ver", "mi retención es mala", un gráfico o CSV de retención
  pegado, o "arregla mi ritmo".
---

# yt-retention

El gráfico de retención es la única opinión sincera que te da YouTube. Casi nadie lo exporta.

```bash
python3 retention.py retencion.csv --duration 600
python3 retention.py retencion.csv --transcript transcripcion.srt
```

Cómo conseguir el archivo: Studio -> un vídeo -> Estadísticas -> Interacción -> el gráfico de
retención de la audiencia -> el icono de descarga -> "Retención de la audiencia".

## Tres problemas distintos

- **FUGA EN EL GANCHO**: lo que se pierde en los primeros 30 segundos. Menos del 25% es sano. Siempre
  es lo primero que hay que arreglar, y siempre está en los primeros quince segundos del guion, nunca
  en la edición.
- **CAÍDAS**: bajadas bruscas puntuales. Una caída es un momento: un cambio de tema sin avisar, un
  patrocinio, una introducción larga. Con `--transcript` la herramienta muestra qué se estaba
  diciendo ahí, que es lo que hace que el informe sirva para actuar y no solo sea curioso.
- **GOTEO**: la pérdida constante en la parte central. Un goteo uniforme es cuestión de ritmo. Se
  arregla recortando, no reescribiendo.

## Qué entregar

Nombra la fuga más grande y un cambio para ella. No una lista de cinco. Después, solo si te lo piden,
el resto. Y si la fuga del gancho está sana y el goteo es plano, di que el vídeo está bien y que el
problema es el título y la miniatura: mándalo a `/yt-package`.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
