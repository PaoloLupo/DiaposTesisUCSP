# Diapositivas Tesis

## Editar y previsualizar

Edita `main.py` y ejecuta:

```powershell
gaanim .
```

Los recursos van en `assets/`; las salidas generadas van en `exports/`.

## Entradas de sección

El índice animado resume la exposición en seis bloques: Problemática, Objetivos,
Fundamentos, Propuesta, Resultados y Conclusiones. Un rail global persistente ocupa
el borde inferior, con el nombre de cada sección justo encima y el contenido más arriba.
Una franja gris suave y una línea superior separan la navegación del contenido.
El tramo activo avanza por segmento de contenido y su nombre se destaca con `ACCENT`;
el número y el título principal acompañan el cambio.
Conserva el fondo, la tipografía y `ACCENT` del proyecto.

`main.py` ya lo muestra antes de la problemática. Para las siguientes partes,
reutiliza la misma instancia de `SectionIndex` y llama a `show` antes de construir
el contenido del bloque:

```python
section_index.show("objetivos", transition=Transition.cross_fade(0.4))
# Construir aquí los segmentos de objetivos.
```

Las claves disponibles son `problematica`, `objetivos`, `fundamentos`, `propuesta`,
`resultados` y `conclusiones`. Cada entrada tiene su propia pausa para exponer.
También admite saltos, regresos y repetir una sección.

Para ver una demo de los seis cambios:

```powershell
gaanim examples/section_index.py
```

## Problemática

`src/tesis/sections/context.py` desarrolla tres momentos con pausas para exponer:

1. Contexto nacional: mapa, contador y materiales predominantes en paredes.
2. Distribución en planta: muros en X/Y y elementos de confinamiento.
3. Proceso convencional: ETABS, hojas de cálculo, verificación e iteración manual.

Se basa en `01_intro.typ` (Problemática y Justificación) y la introducción de
`05_analisismanual.typ` de la tesis. Cada segmento incluye notas del expositor.
La planta es conceptual, sin escala, y no representa una comprobación estructural.

El gráfico actualiza la referencia INEI 2017 de la tesis con los
[tabulados oficiales de vivienda del Censo 2025](https://proyectos.inei.gob.pe/dir-segmentacion-ci/postcensal/prod/adjuntos/censos-2025/descarga_datos/tabulados/00/vivienda/Caracter%C3%ADsticas_de_la_vivienda.xlsx),
hoja **VIV6**, cuadro 6, rango **B7:K7**. Los datos y su fuente se conservan en
`src/tesis/data/materiales_inei.py`. El 61,8 % corresponde al material de las
paredes exteriores; no mide la proporción de albañilería confinada. El relleno
del mapa ilustra el indicador nacional y no una distribución por región.

## Exportar

```powershell
gaanim export . --output exports/video.mp4 --quality production
```

## Validar

```powershell
gaanim check .
```
