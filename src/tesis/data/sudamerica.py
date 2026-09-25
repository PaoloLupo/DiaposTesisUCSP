"""Contornos de países del oeste de Sudamérica para el mapa de placas.

Natural Earth 1:10m, Admin 0 – Countries (dominio público). ``sudamerica.json``
guarda, por código ADM0_A3, el anillo exterior de cada polígono en
(longitud, latitud): recortado a lon −104.5…−45.5 y lat −20…1.6, simplificado
con Douglas-Peucker (0.012° medidos en Mercator) y sin islas menores de
0.004 grados². No incluye lagos ni aguas interiores.
"""

import json
from pathlib import Path

type Ring = list[tuple[float, float]]

SOURCE_LABEL = "Natural Earth 1:10m"

_raw: dict[str, list[list[list[float]]]] = json.loads(
    Path(__file__).with_name("sudamerica.json").read_text(encoding="utf-8")
)
COUNTRIES: dict[str, list[Ring]] = {
    code: [[(lon, lat) for lon, lat in ring] for ring in rings]
    for code, rings in _raw.items()
}
