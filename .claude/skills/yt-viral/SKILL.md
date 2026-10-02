---
name: yt-viral
description: >-
  Encuentra lo que de verdad está funcionando en el nicho del usuario en
  YouTube, ordénalo según cuánto superó cada vídeo a su propio canal y nombra
  la fórmula. Úsala para "qué está funcionando ahora", "busca vídeos virales
  de mi nicho", "por qué ha petado esto", análisis de la competencia o un
  archivo de referencias (swipe file).
---

# yt-viral

Las visitas en bruto ordenan por tamaño del canal, no por ideas. Esto ordena por **cuántas veces
supera cada vídeo la mediana de su propio canal**, que es la única forma de la pregunta que habla
del vídeo.

```bash
python3 swipe.py recopilados.json --min 2.0
```

## Cómo reunir los datos

Necesitas al menos **cuatro vídeos por canal** o la mediana no significa nada; la herramienta se
salta ese canal y te avisa. Reúnelos como prefiera el usuario: `yt-dlp --flat-playlist -J` contra la
URL de un canal es lo más rápido, la página pública sirve y una lista hecha a mano también.

```json
[{"channel":"...","title":"...","views":412000,"url":"...","duration":613}]
```

**Lee, no rastrees.** Solo listados públicos, nunca una sesión iniciada, nunca las credenciales de la
cuenta del usuario.

## Cómo leer el resultado

El multiplicador es la señal. La línea de la fórmula es una valoración del TÍTULO, comparado con
[las 21 fórmulas](../yt-script/hooks.json): no es una afirmación sobre por qué funcionó el vídeo, y
debes decirlo al presentarla.

Qué entregar: los cinco mejores con su multiplicador, la fórmula de cada uno y la ÚNICA cosa de
estructura que tienen en común. Después, la frase difícil: cuál de ellos podría hacer el usuario esta
misma semana, con su voz y con lo que tiene.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
