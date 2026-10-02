# CLAUDE.md

## Idioma

- Responde siempre en español (de España), aunque el material de origen, los logs o las herramientas
  estén en inglés.
- Todo el contenido para YouTube (guiones, ganchos, títulos, miniaturas, descripciones, capítulos,
  respuestas a comentarios) se escribe en español salvo que se pida otro idioma.
- Los mensajes de commit y las descripciones de pull request también van en español.

## Skills de YouTube

Las skills `yt-*` de `.claude/skills/` están traducidas y adaptadas al español a partir de
[Jakeschincariol/youtube-agent-skill](https://github.com/Jakeschincariol/youtube-agent-skill)
(licencia MIT, ver `.claude/skills/YT-SKILLS-LICENSE`). Los scripts de Python reconocen tanto
español como inglés.

El perfil de voz que leen todas las skills va en `~/.claude/youtube/voice.md`. Todavía no existe.
