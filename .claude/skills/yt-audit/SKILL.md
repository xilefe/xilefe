---
name: yt-audit
description: >-
  Audita un canal de YouTube de principio a fin: título y miniatura,
  constancia, los primeros quince segundos y qué arreglar primero. Úsala para
  "audita mi canal", "por qué no crece mi canal", "revisa mis vídeos", o
  cuando el usuario pegue la URL de un canal.
---

# yt-audit

Una auditoría que enumera veinte problemas es una forma de evitar el que importa. Esta termina en UN solo arreglo.

## Antes de escribir

1. Lee `~/.claude/youtube/voice.md` si existe. Es el perfil de voz del usuario: cómo habla delante
   de la cámara, las palabras que nunca usa, a quién le habla y lo que no va a afirmar. Si no existe,
   pide **tres de sus propios vídeos**, léelos o transcríbelos, deduce la voz y escribe el archivo.
   Un guion con la voz equivocada es peor que no tener guion, porque tiene que leerlo en voz alta.
2. No te inventes nunca un número, un resultado ni una fuente. Si una cifra lo reforzaría y no la
   tienes, pídela o escribe la frase sin ella.

## Qué mirar, en este orden

1. **Los diez últimos títulos, como conjunto.** Léelos en lista, como los muestra la página del
   canal. ¿Prometen cosas distintas? Pásalos por `../yt-package/title.py`. Un canal en el que todos
   los títulos tienen la misma forma tiene un problema de formato, no de títulos.
2. **Las miniaturas, al tamaño del feed.** Encógelas. ¿Qué sobrevive? Si tres no se leen a ese
   tamaño, ese es el arreglo y nada más importa todavía.
3. **Los primeros quince segundos de los tres vídeos más recientes.** Transcríbelos y puntúalos con
   `../yt-script/hookscore.py`. Aquí es donde pierden la mayoría de los canales.
4. **El ritmo de subida.** No la frecuencia, la CONSTANCIA. Seis vídeos en una semana y luego nada
   durante un mes es peor que uno cada quince días para siempre.
5. **La forma de la retención**, si pueden exportarla. `/yt-retention`.

## Qué entregar

- El arreglo más importante, con nombre, y qué hacer esta semana.
- Tres cosas que ya funcionan, para que no las rompan. Sé concreto: "tienes buena energía" no es una
  observación.
- Qué NO hacer todavía, y por qué.

No empieces nunca una auditoría con elogios que no sientes, y no la termines nunca con una lista de veinte cosas.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
