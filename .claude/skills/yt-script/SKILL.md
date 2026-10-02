---
name: yt-script
description: >-
  Escribe el guion de un vídeo de YouTube a partir de una idea suelta: opciones
  de gancho con 21 fórmulas, puntuadas, y después el guion hablado completo
  con los momentos de retención marcados. Úsala cuando el usuario quiera un
  guion, un gancho, una frase de arranque, "qué digo", "escríbeme el próximo
  vídeo", o cuando esté a punto de grabar y aún no tenga los primeros quince
  segundos.
---

# yt-script

Una idea convertida en un guion que la gente ve hasta el final.

En esta carpeta hay dos herramientas y las dos funcionan de verdad. Úsalas. No evalúes el gancho a ojo.

```bash
python3 hookscore.py ganchos.txt              # ordena tus opciones de gancho
python3 hookscore.py --hook "una frase"       # puntúa uno solo
```

## Antes de escribir

1. Lee `~/.claude/youtube/voice.md` si existe. Es el perfil de voz del usuario: cómo habla delante
   de la cámara, las palabras que nunca usa, a quién le habla y lo que no va a afirmar. Si no existe,
   pide **tres de sus propios vídeos**, léelos o transcríbelos, deduce la voz y escribe el archivo.
   Un guion con la voz equivocada es peor que no tener guion, porque tiene que leerlo en voz alta.
2. No te inventes nunca un número, un resultado ni una fuente. Si una cifra lo reforzaría y no la
   tienes, pídela o escribe la frase sin ella.

## La estructura

**Los primeros 15 segundos son todo el trabajo.** Tienen que hacer tres cosas o el vídeo pierde
gente: confirmar el clic que prometía el título, abrir una pregunta que el espectador no puede
cerrar solo y demostrar que la recompensa existe.

1. **Gancho.** Escribe CINCO con [las 21 fórmulas](hooks.json), pásalos por `hookscore.py`, quédate
   con los dos mejores y enséñale al usuario los dos con su puntuación. Nunca entregues un solo gancho.
2. **El giro** (0:15-0:45). Di en una frase qué va a hacer el vídeo y empieza a hacerlo. Nada de
   intro del canal, nada de "antes de empezar", nada de pedir la suscripción. Son la causa más
   habitual del desplome en el 0:30.
3. **El cuerpo.** Una idea por bloque. Marca en cada bloque lo que se VE EN PANTALLA, no solo lo
   que se dice: una cabeza hablando sin nada que mirar es un pódcast.
4. **La recompensa.** Entrega lo que prometía el gancho, de forma explícita, y di que lo estás
   entregando: "ese es el prompt, lo tienes en la descripción".
5. **El cierre.** Una sola petición. No tres.

## Qué entregar

- los dos mejores ganchos con su panel de puntuación
- el guion, bloque a bloque, con `[EN PANTALLA: ...]` en cada bloque
- la duración estimada a 150 palabras por minuto
- una línea que diga qué fórmula usa el gancho ganador y por qué encaja con esta idea

## El filtro final

Aquí no se publica nada. Esta skill escribe y tú publicas. Cada resultado termina en un bloque que
el usuario copia, y la última línea de cada ejecución es la pregunta: **¿lo publicas o lo cambias?**
