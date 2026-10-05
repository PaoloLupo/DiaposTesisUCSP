"""Modelo simplificado tridimensional por pórticos planos (MSTA) del caso de estudio.

Geometría transcrita del modelo de ETABS del autor (``MODELOSIMPLIFICADO.e2k``, en cm,
aquí en m): una barra vertical por muro, en el centroide de su sección transformada, y
en cada nivel brazos rígidos (del centroide al borde del muro) y dinteles. Mismo origen
que ``tesis.data.planta`` (ejes 1 y A). Las propiedades vienen de ``tb:geome`` (Tabla 26)
y las cargas tributarias, de la hoja de cálculo del autor (método del sobre).
Módulo sin dependencias de Gaanim para poder probarlo con ``unittest``.
"""

import math
from typing import Literal

STORY_HEIGHT = 2.52  # m, los cuatro pisos del MSTA tienen la misma altura
STORY_COUNT = 4

# Muro (etiqueta Pier; ′ = simétrico) y posición en planta de su barra.
BARS: tuple[tuple[str, float, float], ...] = (
    ("X1", 1.5000, 0.0000),
    ("X2", 6.3151, 0.0000),
    ("X2′", 10.2851, 0.0000),
    ("X1′", 15.1002, 0.0000),
    ("Y1", 0.0000, 0.9349),
    ("Y1′", 16.6002, 0.9349),
    ("Y3", 3.0000, 1.1468),
    ("Y3′", 13.6002, 1.1468),
    ("Y5", 7.0000, 2.8533),
    ("Y5′", 9.6002, 2.8533),
    ("X3", 1.5000, 4.0000),
    ("X7", 8.3001, 4.0000),
    ("X3′", 15.1002, 4.0000),
    ("X4", 4.1468, 5.0300),
    ("X4′", 12.4534, 5.0300),
    ("Y7", 8.3001, 5.4651),
    ("Y4", 3.0000, 6.5151),
    ("Y4′", 13.6002, 6.5151),
    ("Y6", 7.0000, 6.8533),
    ("Y6′", 9.6002, 6.8533),
    ("Y2", 0.0000, 7.0652),
    ("Y2′", 16.6002, 7.0652),
    ("X5", 1.5000, 8.0001),
    ("X6", 6.0652, 8.0001),
    ("X6′", 10.5350, 8.0001),
    ("X5′", 15.1002, 8.0001),
)

type BeamKind = Literal["rigid", "VI", "VE"]
# Barras horizontales de cada nivel: brazo rígido, dintel interior (T) o exterior (L).
BEAMS: tuple[tuple[BeamKind, tuple[float, float], tuple[float, float]], ...] = (
    ("rigid", (13.6002, 4.0000), (16.6002, 4.0000)),
    ("VE", (0.0000, 4.0000), (0.0000, 5.4652)),
    ("VE", (0.0000, 2.5349), (0.0000, 4.0000)),
    ("rigid", (0.0000, 0.9349), (0.0000, 2.5349)),
    ("rigid", (0.0000, 5.4652), (0.0000, 7.0652)),
    ("rigid", (16.6002, 0.9349), (16.6002, 2.5349)),
    ("rigid", (0.0000, 4.0000), (3.0000, 4.0000)),
    ("rigid", (16.6002, 5.4652), (16.6002, 7.0652)),
    ("VE", (16.6002, 4.0000), (16.6002, 5.4652)),
    ("rigid", (1.5000, 0.0000), (3.0650, 0.0000)),
    ("rigid", (6.3151, 0.0000), (7.0651, 0.0000)),
    ("VE", (16.6002, 2.5349), (16.6002, 4.0000)),
    ("rigid", (5.5651, 0.0000), (6.3151, 0.0000)),
    ("rigid", (10.2851, 0.0000), (11.0351, 0.0000)),
    ("rigid", (9.5351, 0.0000), (10.2851, 0.0000)),
    ("VE", (3.0650, 0.0000), (5.5651, 0.0000)),
    ("VE", (7.0651, 0.0000), (9.5351, 0.0000)),
    ("rigid", (13.5352, 0.0000), (15.1002, 0.0000)),
    ("VE", (11.0351, 0.0000), (13.5352, 0.0000)),
    ("rigid", (8.3001, 5.4651), (8.3001, 8.0001)),
    ("rigid", (4.4652, 8.0001), (6.0652, 8.0001)),
    ("VE", (3.0650, 8.0001), (4.4652, 8.0001)),
    ("rigid", (6.0652, 8.0001), (7.0652, 8.0001)),
    ("rigid", (9.5350, 8.0001), (10.5350, 8.0001)),
    ("rigid", (10.5350, 8.0001), (12.1350, 8.0001)),
    ("VE", (7.0652, 8.0001), (9.5350, 8.0001)),
    ("rigid", (3.0000, 1.1468), (3.0000, 3.0350)),
    ("rigid", (13.5352, 8.0001), (15.1002, 8.0001)),
    ("rigid", (3.0000, 4.9651), (3.0000, 6.5151)),
    ("VI", (13.6002, 3.0350), (13.6002, 4.0000)),
    ("VE", (12.1350, 8.0001), (13.5352, 8.0001)),
    ("rigid", (1.5000, 8.0001), (3.0650, 8.0001)),
    ("rigid", (13.6002, 1.1468), (13.6002, 3.0350)),
    ("rigid", (4.1468, 5.0300), (6.0350, 5.0300)),
    ("rigid", (13.6002, 4.9651), (13.6002, 6.5151)),
    ("rigid", (7.0000, 0.9651), (7.0000, 2.8533)),
    ("rigid", (7.0000, 4.9651), (7.0000, 6.8533)),
    ("rigid", (7.0000, 2.8533), (7.0000, 4.0651)),
    ("VI", (7.0000, 4.0651), (7.0000, 4.9651)),
    ("VI", (7.0000, 0.0000), (7.0000, 0.9651)),
    ("rigid", (9.6002, 4.9651), (9.6002, 6.8533)),
    ("rigid", (9.6002, 2.8533), (9.6002, 4.0651)),
    ("VI", (9.6002, 4.0651), (9.6002, 4.9651)),
    ("rigid", (9.6002, 0.9651), (9.6002, 2.8533)),
    ("VI", (9.6002, 0.0000), (9.6002, 0.9651)),
    ("VI", (3.0000, 4.0000), (3.0000, 4.9651)),
    ("VI", (3.0000, 3.0350), (3.0000, 4.0000)),
    ("VI", (13.6002, 4.0000), (13.6002, 4.9651)),
    ("VI", (6.0350, 5.0300), (7.0000, 5.0300)),
    ("rigid", (10.5652, 5.0300), (12.4534, 5.0300)),
    ("VI", (9.6002, 5.0300), (10.5652, 5.0300)),
)

# Relación modular de la rutina SECTRANS: Ec/Em = 15 000 √f'c / (500 f'm).
MODULAR_RATIO = 15_000 * math.sqrt(175) / (500 * 65)

# Muro de ejemplo: X4, con el ala de Y4 en un extremo. Fila de tb:geome (Tabla 26);
# el centroide se mide desde la cara exterior de la columna izquierda.
X4 = {"L": 3.10, "cg": 1.212, "A1": 1.038, "A2": 0.403, "I3": 1.509}
X4_START = (
    2.935  # m, cara exterior de la columna de Y4: 2.935 + 1.212 = barra en x = 4.147
)
WEIGHT_FACTOR_X4 = X4["A2"] / X4["A1"]  # el peso de la barra se corrige a L t

# Hoja de cálculo del autor (método del sobre), piso típico: áreas de X4 en m²,
# arriba (losa entre los ejes C y D) y abajo (losa entre los ejes A y C).
X4_TRIBUTARY = (3.3777, 3.6430)
SLAB_DEAD = 0.388  # tonf/m², peso propio 0.288 + acabados 0.10
SLAB_LIVE = 0.20  # tonf/m², sobrecarga de vivienda
# Cargas que recibe la barra de X4 en ETABS (piso típico, tonf): las tributarias
# escaladas para que sumen el peso total de la losa.
X4_POINT_LOADS = (2.9055, 1.4977)


def tributary_x4() -> float:
    return sum(X4_TRIBUTARY)
