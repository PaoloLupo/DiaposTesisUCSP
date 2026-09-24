# Diapositivas de tesis

Sustentación animada en Gaanim de la tesis *Marco de trabajo para la automatización del
diseño de la distribución de muros en planta para edificios de albañilería confinada*
(UCSP). Pensada para **30 minutos**: 8 bloques, 31 diapositivas de contenido, 8 divisores
de agenda y una portada (40 segmentos, 72 pausas).

## Ejecutar

```powershell
gaanim .
gaanim --present .
gaanim check . --strict
```

En presentación: espacio o flecha derecha para avanzar, izquierda para volver, `O` para buscar
una escena y `P` para la vista del expositor con las notas. Cada nota empieza con el tiempo
sugerido y cita la tabla o figura de la tesis que respalda la diapositiva.

Para ensayar solo algunos bloques:

```powershell
gaanim . --sections resultados,conclusiones
gaanim . --from resultados
```

Las claves son `problematica`, `objetivos`, `fundamentos`, `manual`, `marco`, `alba`,
`resultados` y `conclusiones`; cada bloque incluye su divisor. El guion se ejecuta completo,
así que el estado del riel y la agenda es el mismo que en la exposición entera.

## Recorrido de 30 minutos

Los tiempos incluyen la explicación oral; las pausas (`scene.stop`) esperan al expositor.

| Bloque | Diapositivas | Tiempo | Acumulado |
| --- | --- | ---: | ---: |
| Portada | Título y planta del caso dibujándose | 0:45 | 0:45 |
| 01 Problemática | Material de las viviendas (INEI 2025) · muro confinado y sismo · traslado manual y pregunta | 3:00 | 3:45 |
| 02 Objetivos y método | Objetivo general e hipótesis · objetivos específicos · metodología | 2:00 | 5:45 |
| 03 Fundamentos | Densidad con la planta real · tres verificaciones de resistencia · deriva | 4:00 | 9:45 |
| 04 Proceso manual | Caso de estudio · áreas vs barras · criterios de modelamiento · ciclo manual | 3:30 | 13:15 |
| 05 Marco de trabajo | Qué se automatiza · flujo general · módulo de densidad · trazabilidad | 3:45 | 17:00 |
| 06 Alba | Arquitectura · API de ETABS · interfaz · reporte | 3:00 | 20:00 |
| 07 Resultados | Modelos · peso y fuerzas · derivas · cortante · resistencia · fisuración | 6:00 | 26:00 |
| 08 Conclusiones | Objetivos · hallazgos · alcance y futuro · cierre | 2:45 | 28:45 |
| Divisores | 8 × ~6 s | 0:50 | ≈ 29:35 |

Si hace falta recortar, las diapositivas que menos afectan el argumento son
*Proceso manual · criterios de modelamiento*, *Alba · API de ETABS* y *Resultados · cortante*:
basta quitarlas de la lista de `SectionStep` de su bloque.

## Sistema visual

- **Papel y ladrillo:** fondo cálido `#F6F3EC`, tinta `#1D2129` y terracota `#B8532F`.
- **Colores con significado fijo:** terracota = albañilería, dirección X y modelo MCT;
  azul acero = dirección Y y MSTA; gris concreto = concreto y MSTO; verde y rojo solo para
  *cumple* / *no cumple*.
- **Tipografía incrustada** en `assets/fonts` (todas con licencia OFL): Aleo para títulos y
  cifras, Lato para el texto, Cascadia Mono para etiquetas técnicas; las ecuaciones usan la
  matemática de Typst. La presentación no depende de las fuentes instaladas en el equipo.
- **Títulos-afirmación:** cada título dice la conclusión de la diapositiva; el kicker indica el
  bloque y la línea inferior, la fuente en la tesis.
- **Un mismo edificio en toda la exposición:** la planta de San Bartolomé (2006) se dibuja como
  geometría (`tesis.building`) con los muros y etiquetas Pier del modelo de ETABS. Se reutiliza
  en la portada, la densidad, el caso de estudio, la resistencia global, el mapa de fisuración
  y el cierre.

## Dónde editar

| Cambio | Archivo |
| --- | --- |
| Orden de los bloques | `main.py` |
| Colores, tipografías y tema | `src/tesis/theme.py` |
| Encabezado, fuentes, chips de estado, cotas | `src/tesis/kit.py` |
| Símbolos de diagramas de flujo | `src/tesis/diagram.py` |
| Dibujo de la planta del caso | `src/tesis/building.py` |
| Muros, longitudes y densidad del caso | `src/tesis/data/planta.py` |
| Cifras transcritas de la tesis | `src/tesis/data/thesis.py` |
| Datos INEI 2025 | `src/tesis/data/materiales_inei.py` |
| Divisores y riel de avance | `src/tesis/section_index.py` |
| Contenido de cada bloque | `src/tesis/sections/<bloque>.py` |

Cada bloque termina con su `SECTION`: una lista de `SectionStep(name, build, notes)`. Para
añadir una diapositiva, escribe su función y agrega el paso. El tema usa `text_markup=False`:
`*` y `_` son literales (`tb:dist_comp`) y los subíndices se escriben como matemática:
`"$V_e$ (tonf)"`.

## Datos y fuentes

El submódulo [TesisUCSP](https://github.com/PaoloLupo/TesisUCSP) contiene la tesis; las
cifras corresponden al commit `d1d0b73`, que revierte el título a «…automatización del diseño
de la distribución de muros…» (la portada usa ese título).

```powershell
git submodule update --init --recursive
python -m unittest discover -s tests -v
```

Las pruebas leen las tablas Typst reales y verifican pesos por nivel, fuerzas en altura,
derivas, cortantes y resistencias (cap. 8), fisuración por muro y esfuerzo axial (cap. 5), y
que la densidad calculada desde la planta coincide con `tb:densidad_ejm` (4.80 % y 3.74 %).

Matices que conviene respetar al exponer (también están en las notas):

- La comparación es descriptiva: MCT, MSTA y MSTO difieren en norma, idealización, programa y
  procesamiento; no mide una tasa de error ni un ahorro de tiempo de Alba.
- MCT vs MSTA aísla la idealización (misma norma); MSTA vs MSTO aísla la norma.
- El dato INEI 2025 es el material de las paredes exteriores; no acredita confinamiento.
- La deriva animada y el ciclo manual son esquemas; sus valores del caso se citan aparte.

## Revisión por capturas

`gaanim --diff --capture-stops` captura sin ventana el estado de cada pausa, sin código de
revisión en el guion:

```powershell
gaanim --diff --example . --capture-stops --no-gui --tests-root snapshots
gaanim --diff --example . --capture-stops --stops 12,30 --no-gui --tests-root snapshots
gaanim --diff --example . --capture-stops --sections resultados --no-gui --tests-root snapshots
```

Las imágenes (`stop_0001.png`, …) y `stops.json` (pausa, instante, segmento) quedan en
`snapshots/DiaposTesisUCSP/current/`. Las pausas se numeran desde 1.

## Actualizar Gaanim

El proyecto usa el wheel local de `../../rust/gaanim/target/wheels`. Tras reconstruirlo
(`just wheel` en Gaanim) conserva la versión 0.2.0, así que hay que forzar la reinstalación:

```powershell
just reinstall
```

## Exportar

```powershell
gaanim export . --output exports/tesis.mp4 --quality production
```

La exportación ignora las pausas y genera una secuencia continua de ~3.5 minutos de animación.

## Notas para Gaanim

`GAANIM_NOTAS.md` recoge el estado de los bugs y mejoras de Gaanim encontrados durante el
rediseño: qué ya se resolvió, qué sigue abierto, cómo reproducirlo y el rodeo aplicado aquí.
