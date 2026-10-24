# Diapositivas de tesis

Sustentación animada en Gaanim de la tesis *Marco de trabajo para la automatización del
diseño de la distribución de muros en planta para edificios de albañilería confinada*
(UCSP). Pensada para **30 minutos**: 8 bloques, 34 diapositivas de contenido, 8 divisores
de agenda y una portada (43 segmentos, 101 pausas).

## Ejecutar

```powershell
uv sync          # wheel de Gaanim para autocompletado, ruff y pyright
gaanim .
gaanim --present .
just check       # estilo, tipos, pruebas de datos y gaanim check
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
| 03 Fundamentos | Densidad con la planta real · tres verificaciones de resistencia · deriva · estado del arte | 4:45 | 10:30 |
| 04 Proceso manual | Caso de estudio · modelo completo en ETABS · pórticos planos · criterios de modelamiento · ciclo manual | 5:30 | 16:00 |
| 05 Marco de trabajo | Qué se automatiza · flujo general · módulo de densidad y diagramas de los otros tres · trazabilidad | 4:00 | 20:00 |
| 06 Alba | Arquitectura · API de ETABS · interfaz · reporte · partes del reporte | 3:15 | 23:15 |
| 07 Resultados | Modelos · peso y fuerzas · derivas · cortante · resistencia | 4:45 | 28:00 |
| 08 Conclusiones | Objetivos · hallazgos · recomendaciones · cierre | 2:45 | 30:45 |
| Divisores | 8 × ~6 s | 0:50 | ≈ 31:35 |

Si hace falta recortar, las diapositivas que menos afectan el argumento son
*Proceso manual · criterios de modelamiento*, *Alba · API de ETABS* y *Resultados · cortante*:
basta quitarlas de la lista de `SectionStep` de su bloque.

## Sistema visual

- **Papel y ladrillo:** fondo cálido `#F6F3EC`, tinta `#1D2129` y terracota `#B8532F`.
- **Colores con significado fijo:** terracota = albañilería, dirección X y modelo MCT;
  azul acero = dirección Y y MSTA; gris concreto = concreto y MSTO; verde y rojo solo para
  *cumple* / *no cumple*.
- **Tipografía incrustada** en `assets/fonts` (todas con licencia OFL): Aleo para títulos y
  cifras, Lato para el texto, IBM Plex Mono para etiquetas técnicas; las ecuaciones usan la
  matemática de Typst. La presentación no depende de las fuentes instaladas en el equipo.
- **Títulos-afirmación:** cada título dice la conclusión de la diapositiva; el kicker indica el
  bloque y la línea inferior, la fuente en la tesis.
- **Un mismo edificio en toda la exposición:** la planta de San Bartolomé (2006) se dibuja como
  geometría (`tesis.building`) con los muros y etiquetas Pier del modelo de ETABS. Se reutiliza
  en la portada, la densidad, el caso de estudio, la resistencia global
  y el cierre.
- **Modelos en 3D real:** la vivienda de Problemática, el modelo completo (MCT) y los pórticos
  planos (MSTA) viven en el mundo 3D de Gaanim, en metros y con los colores planos del deck.
  Cada toma (`tesis.model3d.Shot`, una órbita `camera.state_orbit` de Gaanim) los encuadra en
  perspectiva a la izquierda del panel de pasos, y `orbit_to` pasa de una toma a otra rodeando
  el foco: de la planta a la vista 3D, a un nudo, a un pórtico de frente o alrededor del modelo.
  La capa 2D no se mueve con la cámara, y cada diapositiva empieza en la vista 2D
  (`Section(..., camera="reset")`, en `section_index.py`).

## Dónde editar

| Cambio | Archivo |
| --- | --- |
| Orden de los bloques | `main.py` |
| Colores, tipografías y tema | `src/tesis/theme.py` |
| Encabezado, fuente, frase final y demás componentes de layout | `src/tesis/components.py` |
| Texto por coordenadas, chips de estado, numerales y cotas | `src/tesis/kit.py` |
| Símbolos de diagramas de flujo | `src/tesis/diagram.py` |
| Dibujo de la planta del caso | `src/tesis/building.py` |
| Mundo 3D (z hacia arriba, en metros): tomas, órbitas, rótulos sobre puntos 3D | `src/tesis/model3d.py` |
| Modelo de ETABS (MCT) en 3D: áreas, frames, malla y deformada | `src/tesis/etabs_model.py` |
| Tomas de cámara del MCT y del MSTA (`MCT_*`, `MSTA_*`) | `src/tesis/sections/manual.py` |
| Vivienda confinada en 3D, hilada por hilada | `src/tesis/vivienda.py` |
| Bloque de la subducción (Nazca bajo la Sudamericana) | `src/tesis/subduccion.py` |
| Pórticos planos (MSTA): barras, brazos y dinteles | `src/tesis/data/porticos.py` |
| Muros, longitudes y densidad del caso | `src/tesis/data/planta.py` |
| Cifras transcritas de la tesis | `src/tesis/data/thesis.py` |
| Datos INEI 2025 | `src/tesis/data/materiales_inei.py` |
| Páginas del reporte de Alba (recortes del anexo) | `tools/render_report.py` → `assets/reporte/` |
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
uv run python -m unittest discover -s tests -v
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

## Revisión

`just check` corre ruff (estilo), pyright (tipos, modo estándar), las pruebas de datos y
`gaanim check`. Las versiones de ruff y pyright están fijadas en el grupo `dev` de
`pyproject.toml` y `uv sync` las instala; `just fmt` formatea y aplica los arreglos seguros.

`gaanim check` corre con `--strict`: cualquier aviso hace fallar la revisión. El riel de
avance está en el margen a propósito y lo declara con `outside_safe_on_purpose()`.

### Capturas

Cada pausa se captura sin ventana y se compara con una referencia aprobada (`gaanim --diff`):

```powershell
just baseline                 # antes de un cambio: aprueba las pausas actuales
just diff                     # después: compara; informe en snapshots/report/index.html
just diff --stops 80-86       # solo algunas pausas (o --sections resultados)
just capture --stops 12,30    # captura sin comparar, en snapshots/DiaposTesisUCSP/current
```

Las pausas se numeran desde 1. Tras actualizar Gaanim, los bordes de líneas y textos cambian
por antialiasing; `just diff --pixel-threshold 24` deja solo los cambios visibles.

Las capturas saltan a cada pausa y no muestran lo que pasa entre una y otra. Las transiciones
(el índice que se despliega, el sismo, el vuelo de una página) se revisan exportando el tramo
en orden, como se reproduce:

```powershell
just sequence reporte-parte-1 reporte-parte-2   # nombres de pausa o segundos
```

Los cuadros quedan en `snapshots/sequence/`, 30 por segundo.

## Gaanim

El guion necesita Gaanim 0.17.1. Lo que usa de esa versión:
- los cambios de layout simultáneos;
- el recorte de imágenes al reproducir en orden;
- `deform` en copias;
- la lectura de paquetes con muchas copias;
- `scene.viz.map`;
- `outside_safe_on_purpose()`.

Con la release v0.17.0 el deck no carga. Mientras 0.17.1 no esté en PyPI, `pyproject.toml`
toma el wheel de `C:/Tools/gaanim` (`[tool.uv.sources]`); al publicarse, se quita esa sección
y se corre `uv lock`.

Gaanim llega en dos piezas:

- **El motor** (`gaanim.exe`, en `C:/Tools/gaanim`) ejecuta, presenta, captura y exporta. Se
  actualiza con `gaanim update` (última release) o copiando un build de `main`.
- **El wheel** (`gaanim` en `pyproject.toml`) solo aporta los stubs para el autocompletado y
  pyright. Se actualiza con `just upgrade`.

## Exportar

```powershell
just publish                                                     # para el navegador
just export                                                      # paquete completo
gaanim export . --output exports/tesis.mp4 --quality production  # video
```

`just publish` exporta el paquete completo a `exports/` (que no se versiona), lo aligera con
`gaanim pack --web` (de unos 54 a 25 MB) y lo deja como único commit de la rama `publicar`.
Cada publicación reemplaza ese commit, así que el historial no crece. Sale de un commit: con
cambios sin commit se niega, salvo `just publish --dirty`; `--no-push` arma la rama sin subirla.
El reproductor web lo abre desde `raw.githubusercontent.com`, que envía CORS (las descargas de
GitHub Releases no):

<https://paololupo.github.io/gaanim/reproductor/?src=https://raw.githubusercontent.com/PaoloLupo/DiaposTesisUCSP/publicar/DiaposTesisUCSP.gaanim>

El paquete completo de `exports/` sirve para exportar video y para `gaanim check`. La
exportación ignora las pausas y genera una secuencia continua de unos 6.3 minutos de animación
(380.7 s).

## Bugs y mejoras de Gaanim

Los bugs y mejoras de Gaanim que aparecen al trabajar en el deck se registran como issues en
[PaoloLupo/gaanim](https://github.com/PaoloLupo/gaanim/issues). Cada rodeo del guion lleva un
comentario «gaanim #NNN»; al cerrarse la issue se quita el rodeo y se compara con `just diff`.
Queda uno: #733 (los rótulos de la retícula del mapa no toman la fuente del tema, en
`theme.py`).
