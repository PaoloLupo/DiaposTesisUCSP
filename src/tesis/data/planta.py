"""Geometría y aportes de los muros del caso de estudio (San Bartolomé, 2006).

Coordenadas en metros con el origen de ETABS (esquina inferior izquierda), según
la vista de Pier Labels del cap. 5 (``imagenes/cap5/PIERS.png``). Las longitudes
y espesores efectivos provienen de ``tb:densidad_ejm``; la mitad derecha es
simétrica respecto de x = 8.3 m y sus etiquetas llevan el sufijo ``_2``.
Módulo sin dependencias de Gaanim para poder probarlo con ``unittest``.
"""

from dataclasses import dataclass
from typing import Literal

WIDTH = 16.6  # m
DEPTH = 8.0  # m
AXIS_X = {"1": 0.0, "2": 3.0, "3": 7.0, "4": 8.3, "5": 9.6, "6": 13.6, "7": 16.6}
AXIS_Y = {"A": 0.0, "B": 4.0, "C": 5.0, "D": 8.0}
STAIR = (7.0, 1.0, 9.6, 4.0)  # vacío de escalera: x0, y0, x1, y1
FLOOR_AREA = 136.51  # m², tb:info_gen y tb:densidad_ejm
THICKNESS = 0.13  # m, aparejo de soga


@dataclass(frozen=True)
class Wall:
    name: str
    direction: Literal["X", "Y"]
    fixed: float  # coordenada del eje del muro
    start: float
    end: float
    length: float  # L de tb:densidad_ejm, incluye columnas
    thickness: float  # t efectivo; X2 usa el espesor transformado
    count: int  # N: 2 si el muro se repite por simetría
    material: Literal["albañilería", "concreto"] = "albañilería"

    @property
    def area(self) -> float:
        return self.length * self.thickness

    @property
    def contribution(self) -> float:
        return self.area * self.count


# Mitad izquierda del edificio; X7 e Y7 cruzan el eje de simetría (N = 1).
WALLS = (
    Wall("X1", "X", 0.0, -0.065, 3.065, 3.13, 0.13, 2),
    Wall("X2", "X", 0.0, 5.565, 7.0, 1.435, 0.794, 2, "concreto"),
    Wall("X3", "X", 4.0, -0.065, 3.065, 3.12, 0.13, 2),
    Wall("X4", "X", 5.0, 3.0, 6.105, 3.105, 0.13, 2),
    Wall("X5", "X", 8.0, -0.065, 3.065, 3.13, 0.13, 2),
    Wall("X6", "X", 8.0, 4.46, 7.065, 2.605, 0.13, 2),
    Wall("X7", "X", 4.0, 6.935, 9.665, 2.73, 0.13, 1),
    Wall("Y1", "Y", 0.0, -0.065, 2.54, 2.605, 0.13, 2),
    Wall("Y2", "Y", 0.0, 5.47, 8.065, 2.595, 0.13, 2),
    Wall("Y3", "Y", 3.0, -0.065, 3.035, 3.10, 0.13, 2),
    Wall("Y4", "Y", 3.0, 4.965, 8.065, 3.10, 0.13, 2),
    Wall("Y5", "Y", 7.0, 0.965, 4.065, 3.10, 0.13, 2),
    Wall("Y6", "Y", 7.0, 4.97, 8.065, 3.095, 0.13, 2),
    Wall("Y7", "Y", 8.3, 3.94, 8.065, 4.125, 0.13, 1),
)


def density(direction: Literal["X", "Y"]) -> float:
    return sum(w.contribution for w in WALLS if w.direction == direction) / FLOOR_AREA


def wall_area_sum(direction: Literal["X", "Y"]) -> float:
    return sum(w.contribution for w in WALLS if w.direction == direction)
