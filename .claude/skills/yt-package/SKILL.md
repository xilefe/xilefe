---
name: yt-package
description: >-
  Escribe y revisa el título y la miniatura de un vídeo de YouTube como una
  sola pareja, comprobando que no se corten, que no se repitan y que no sean
  vagos antes de publicar. Úsala para "ideas de título", "cómo lo llamo",
  "texto de la miniatura", "mi CTR es malo", o cualquier petición de
  renombrar o reempaquetar un vídeo.
---

# yt-package

El título y la miniatura son UNA unidad. Escribirlos por separado es la razón por la que falla casi
todo el empaquetado: la miniatura repite el título y la mitad de lo que invita al clic dice dos veces
lo mismo.

```bash
python3 title.py --title "..." --thumb "LA IA LO HIZO"
python3 title.py titulos.txt            # uno por línea, ordenados
```

## Antes de escribir

1. Lee `~/.claude/youtube/voice.md` si existe. Es el perfil de voz del usuario: cómo habla delante
   de la cámara, las palabras que nunca usa, a quién le habla y lo que no va a afirmar. Si no existe,
   pide **tres de sus propios vídeos**, léelos o transcríbelos, deduce la voz y escribe el archivo.
   Un guion con la voz equivocada es peor que no tener guion, porque tiene que leerlo en voz alta.
2. No te inventes nunca un número, un resultado ni una fuente. Si una cifra lo reforzaría y no la
   tienes, pídela o escribe la frase sin ella.

## Reglas que aplica la herramienta, y por qué

- **60 caracteres** es donde corta la búsqueda en ordenador y **40** el feed de inicio en móvil. Se
  informan los dos porque fallan de forma distinta: el corte en ordenador pierde el final, el del
  móvil puede perder el tema.
- **La miniatura no debe repetir el título.** Palabras distintas, la misma promesa.
- **Tres palabras como máximo en la miniatura.** Al tamaño del feed, una cuarta palabra es una mancha gris.
- **Un número, un nombre o una fecha** gana a cualquier adjetivo.
- **Dos palabras en mayúsculas es el techo** antes de que un título parezca spam.

## Escribe diez, quédate con dos

Genera diez títulos, pásalos todos por `title.py` y enséñale al usuario los tres mejores con su
puntuación y el problema concreto de cada uno. Para el ganador, escribe el encargo de la miniatura:
la expresión, el encuadre, las tres palabras y qué tiene que hacer el fondo para mantener el
contraste al tamaño del feed.

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
