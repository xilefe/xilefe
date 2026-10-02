---
name: yt-seo
description: >-
  Escribe la descripción, las etiquetas y el texto pensado para la búsqueda
  de un vídeo de YouTube, apuntando a lo que una persona real escribe en el
  buscador. Úsala para "escríbeme la descripción", "etiquetas", "tags", "SEO",
  "ayuda a que encuentren este vídeo", "nadie encuentra esto".
---

# yt-seo

La búsqueda es una palanca más pequeña que el título y la miniatura, y más grande de lo que la gente
cree en los vídeos atemporales. Si el vídeo está pensado para el feed de suscriptores, dilo y dedica
el esfuerzo a `/yt-package`.

## Antes de escribir

1. Lee `~/.claude/youtube/voice.md` si existe. Es el perfil de voz del usuario: cómo habla delante
   de la cámara, las palabras que nunca usa, a quién le habla y lo que no va a afirmar. Si no existe,
   pide **tres de sus propios vídeos**, léelos o transcríbelos, deduce la voz y escribe el archivo.
   Un guion con la voz equivocada es peor que no tener guion, porque tiene que leerlo en voz alta.
2. No te inventes nunca un número, un resultado ni una fuente. Si una cifra lo reforzaría y no la
   tienes, pídela o escribe la frase sin ella.

## La descripción

- **Las dos primeras líneas son las únicas que lee alguien.** Salen antes de "...más" y son el
  fragmento que aparece en la búsqueda. Di qué les da el vídeo, con las palabras que habrían escrito.
- Después, el enlace o el recurso, si lo hay, para que quede a la vista sin desplegar.
- Después, los capítulos (los escribe `/yt-chapters`).
- Después, la versión larga: qué se cubre, para quién es y qué da por sabido.

## Etiquetas, con sinceridad

Las etiquetas pesan poco y YouTube lo ha dicho. Úsalas para desambiguar (variantes de escritura,
nombres de herramientas, las abreviaturas que la gente escribe de verdad) y para. Quince son más
que suficientes. Una pared de etiquetas no es una estrategia, y meter etiquetas que no tienen nada
que ver va contra las normas.

## La prueba de las búsquedas

Antes de entregar nada, escribe las tres búsquedas que este vídeo debería ganar y comprueba que el
título y las dos primeras líneas de la descripción contienen las palabras de esas búsquedas. Si no
las contienen, el problema es el título, no la descripción.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
