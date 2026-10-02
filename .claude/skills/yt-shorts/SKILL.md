---
name: yt-shorts
description: >-
  Encuentra los Shorts escondidos dentro de un vídeo largo y escríbelos,
  usando la transcripción para elegir momentos que se entienden solos. Úsala
  para "saca shorts de esto", "recórtalo en clips", "reaprovecha este vídeo",
  "qué fragmentos corto".
---

# yt-shorts

Un Short sacado de un vídeo largo no es un clip del mejor momento. Es un momento que **se sostiene
sin el vídeo que lo rodea**, y de esos hay muchos menos.

## Cómo elegir

Lee la transcripción y busca tramos de 20 a 55 segundos en los que se cumplan las tres cosas:

1. Empieza con una idea completa. Si la primera frase necesita el minuto anterior, no es un Short.
2. Tiene un giro: una afirmación y luego algo que la complica o la demuestra.
3. Termina en una frase, no en algo que se va apagando.

Ordena los candidatos y enséñale al usuario los cinco mejores con sus códigos de tiempo y su primera
frase, para que pueda descartar uno sin leerse toda la transcripción.

## Cómo escribir cada uno

- **Una primera frase NUEVA.** La del vídeo largo da por hecho un contexto que este espectador no
  tiene. Escribe la sustituta y pásala por `../yt-script/hookscore.py`.
- **Texto en pantalla para los dos primeros segundos**, con palabras distintas de las que se dicen.
- **Un punto de bucle**: qué plantea la última frase para que la primera la responda.
- Nota de encuadre vertical: qué se pierde al recortar un plano 16:9 y si importa.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
