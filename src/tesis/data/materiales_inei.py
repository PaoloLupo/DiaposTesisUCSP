"""Datos de material predominante en paredes, fuente INEI 2025."""

MATERIALES_ORDENADOS = sorted(
    [
        ("Ladrillo\no bloque", 6_283_079),
        ("Adobe", 1_914_324),
        ("Madera", 923_006),
        ("Tapia", 435_795),
        ("Triplay\ncalamina", 317_806),
        ("Quincha", 123_433),
        ("Piedra\ncon barro", 66_852),
        ("Piedra /\nsillar", 66_081),
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
    "rotulo": [f"{porcentaje:.2f}%" for porcentaje in PORCENTAJES],
}
