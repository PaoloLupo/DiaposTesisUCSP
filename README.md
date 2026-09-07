# Diapositivas Tesis

## Editar y previsualizar

Edita `main.py` y ejecuta:

```powershell
.\run.ps1
```

Los recursos van en `assets/`; las salidas generadas van en `exports/`.

El proyecto usa `Section`, `SectionStep`, rellenos reactivos y conectores del checkout
local de Gaanim indicado por `GAANIM_ROOT`. `run.ps1` utiliza su runtime de
desarrollo y prepara las rutas de sus DLL; el ejecutable global instalado
todavía no incorpora estas APIs. Los argumentos se resuelven desde este proyecto.
La wheel de autoría y su hash están fijados en `uv.lock`; instala los tipos con
`uv sync`.

## Entradas de sección

El índice animado resume la exposición en seis bloques: Problemática, Objetivos,
Fundamentos, Propuesta, Resultados y Conclusiones. Un rail global persistente ocupa
el borde inferior, con el nombre de cada sección justo encima y el contenido más arriba.
Una franja gris suave y una línea superior separan la navegación del contenido.
El tramo activo avanza por segmento de contenido y su nombre se destaca con `ACCENT`;
el número y el título principal acompañan el cambio.
Conserva el fondo, la tipografía y `ACCENT` del proyecto.

`main.py` usa `build` para mostrar la entrada y calcular el avance automáticamente
a partir de la sección declarada en el módulo de contenido:

```python
section_index.build(
    context.SECTION,
    transition=Transition.cross_fade(0.4),
)
```

`context.SECTION` es un `Section` de Gaanim. Cada `SectionStep` declara su nombre,
builder, transición y notas. Gaanim abre el segmento y entrega la escena original
al builder, que crea contenido sin llamar a `scene.segment()`.
El rail utiliza `SectionProgress.fraction` al entrar en cada paso;
las llamadas a `scene.stop()` no cambian el progreso.
Para añadir o quitar segmentos, edita los pasos de `SECTION`.
Reutiliza esa instancia al repetir la sección para obtener nombres únicos.
`show()` sigue disponible para mostrar únicamente una entrada de sección.

Las claves disponibles son `problematica`, `objetivos`, `fundamentos`, `propuesta`,
`resultados` y `conclusiones`. Cada entrada tiene su propia pausa para exponer.
También admite saltos, regresos y repetir una sección.

Para ver una demo de los seis cambios:

```powershell
.\run.ps1 examples/section_index.py
```

## Problemática

`src/tesis/sections/context.py` desarrolla tres momentos con pausas para exponer:

1. Contexto nacional: mapa, contador y materiales predominantes en paredes.
2. Distribución en planta: muros en X/Y y elementos de confinamiento.
3. Proceso convencional: ETABS, hojas de cálculo, verificación e iteración manual.

Las tarjetas usan `layout.card`; `NODE_CARD` en `src/tesis/theme.py` centraliza
el contorno, las dimensiones y los puertos con nombre. El helper de contenido
solo define los textos y su disposición editorial.
Las flechas del flujo usan `geometry.connector` entre puertos de las tarjetas.
El retorno es un único conector con puntos intermedios relativos a esas anclas;
al mover una tarjeta se actualizan sus conexiones. `ARROW_STYLE` centraliza
las dimensiones, y cada conector admite `animate.create()`.

Se basa en `01_intro.typ` (Problemática y Justificación) y la introducción de
`05_analisismanual.typ` de la tesis. Cada segmento incluye notas del expositor.
La planta es conceptual, sin escala, y no representa una comprobación estructural.

Los estilos y flujos de texto están centralizados en `src/tesis/theme.py`.
Las tarjetas del proceso usan `scene.layout.stack` con posiciones relativas a
su caja. El contador y el relleno del mapa comparten un único parámetro:
`computed(..., inputs=[amount])` convierte el porcentaje a una fracción para
`fill_level`, por lo que solo se anima `amount`.

El gráfico actualiza la referencia INEI 2017 de la tesis con los
[tabulados oficiales de vivienda del Censo 2025](https://proyectos.inei.gob.pe/dir-segmentacion-ci/postcensal/prod/adjuntos/censos-2025/descarga_datos/tabulados/00/vivienda/Caracter%C3%ADsticas_de_la_vivienda.xlsx),
hoja **VIV6**, cuadro 6, rango **B7:K7**. Los datos y su fuente se conservan en
`src/tesis/data/materiales_inei.py`. El 61,8 % corresponde al material de las
paredes exteriores; no mide la proporción de albañilería confinada. El relleno
del mapa ilustra el indicador nacional y no una distribución por región.

## Exportar

```powershell
.\run.ps1 export . --output exports/video.mp4 --quality production
```

## Validar

```powershell
.\run.ps1 check .
```
