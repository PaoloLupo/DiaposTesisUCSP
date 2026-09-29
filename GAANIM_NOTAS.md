# Notas para Gaanim

Pendientes encontrados al preparar las diapositivas de tesis con Gaanim, Windows 11. Cada
entrada dice cómo reproducirla, qué se esperaba y el rodeo usado en este proyecto. Solo se
anota lo comprobado renderizando fotogramas; lo resuelto se borra.

Última revisión: Gaanim 0.7.2.

## Bugs y comportamientos inesperados

Ninguno pendiente.

## Mejoras sugeridas

### Avisar o documentar que el texto de una caja no compone matemática

- **Situación:** `scene.layout.box("67 % de $0.55 V_m$")` dibuja el texto literal, con los
  `$` y el guion bajo, mientras que `scene.text("... $0.55 V_m$")` sí compone la fórmula.
  Es coherente (el texto de la caja es tipografía plana), pero no lo dice ningún aviso y
  se descubre mirando el fotograma.
- **Rodeo correcto:** pasar un `scene.text(...)` (o `scene.text.equation(...)`) como hijo de
  la caja; el layout lo coloca como cualquier otro objeto.
- **Propuesta:** una línea en la guía de Layout ("para matemática, usa un texto como hijo")
  o una advertencia de `check` cuando el texto de una caja contiene `$…$`.
- **Comprobado en:** 0.7.2, diapositiva `fundamentos · tres verificaciones`.
