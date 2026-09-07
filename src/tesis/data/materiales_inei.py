"""INEI, Censos Nacionales 2025, Características de la vivienda.

Hoja VIV6, cuadro 6: fila 7, Perú / Viviendas particulares, B7:K7.
Universo: viviendas particulares con ocupantes presentes (no población).
Se conserva el orden descendente para facilitar la comparación en pantalla.
"""

SOURCE_URL = (
    "https://proyectos.inei.gob.pe/dir-segmentacion-ci/postcensal/prod/"
    "adjuntos/censos-2025/descarga_datos/tabulados/00/vivienda/"
    "Caracter%C3%ADsticas_de_la_vivienda.xlsx"
)
SOURCE_LABEL = "INEI · Censos Nacionales 2025 · Cuadro 6"

MATERIALES_ORDENADOS = sorted(
    [
        ("Ladrillo\no bloque", 6_283_079),
        ("Adobe", 1_914_324),
        ("Madera", 923_006),
        ("Tapia", 435_795),
        ("Triplay /\ncalamina /\nestera", 317_806),
        ("Quincha", 123_433),
        ("Piedra\n+ barro", 66_852),
        ("Piedra\n/ sillar", 66_081),
        ("Otro", 37_147),
    ],
    key=lambda item: item[1],
    reverse=True,
)
TOTAL_VIVIENDAS = 10_167_523

MATERIALES = [material for material, _ in MATERIALES_ORDENADOS]
PORCENTAJES = [
    100 * viviendas / TOTAL_VIVIENDAS for _, viviendas in MATERIALES_ORDENADOS
]
CHART_DATA = {
    "id": [str(index) for index in range(len(MATERIALES))],
    "material": MATERIALES,
    "color_material": MATERIALES,
    "viviendas_porcentaje": PORCENTAJES,
    "rotulo": [f"{porcentaje:.1f}%" for porcentaje in PORCENTAJES],
}
