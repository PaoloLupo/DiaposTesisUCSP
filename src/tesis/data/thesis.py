"""Datos transcritos de la tesis, commit d1d0b73. Orden de niveles: 1, 2, 3, 4.

Cambiar aquí los números de las gráficas; revisar también la tabla citada.
Los porcentajes se calculan desde los valores, no se copian de la discusión.
``tests/test_thesis_data.py`` contrasta cada serie con las tablas Typst reales.
"""

REVISION = "d1d0b7383044e7466e50df72852da9ff2fb6300e"
MODELS = ("MCT", "MSTA", "MSTO")
FLOORS = (1, 2, 3, 4)

MODEL_NAMES = {
    "MCT": "Modelo completo tridimensional",
    "MSTA": "Modelo simplificado tridimensional actualizado",
    "MSTO": "Modelo simplificado tridimensional original",
}

# 05_analisismanual.typ, <tb:info_gen>, <tb:carac_mat> y predimensionamiento.
CASE = {
    "ubicacion": "Lima, suelo de cascajo",
    "uso": "Vivienda",
    "pisos": 4,
    "altura": 2.40,  # m, piso a techo
    "planta": (16.6, 8.0),  # m
    "area": 136.51,  # m²
    "losa": 0.12,  # m, maciza bidireccional
    "espesor": 0.13,  # m, aparejo de soga
    "fm": 65.0,  # kgf/cm²
    "vm": 8.1,  # kgf/cm²
    "fc": 175.0,  # kgf/cm²
    "Em": 32_500.0,  # kgf/cm²
    "Ec": 200_000.0,  # kgf/cm²
    "Z": 0.45,
    "U": 1.0,
    "S": 1.0,
}
DENSITY_MIN = CASE["Z"] * CASE["U"] * CASE["S"] * CASE["pisos"] / 56

# 08_comparacion.typ, <tb:pesos_comp>, tonf. Totales y por nivel (1..4).
SEISMIC_WEIGHT = (451.840, 456.566, 432.110)
WEIGHT_BY_FLOOR = {
    "MCT": (121.334, 121.334, 121.334, 87.835),
    "MSTA": (122.205, 122.205, 122.205, 89.950),
    "MSTO": (116.870, 116.870, 116.870, 81.500),
}

# 08_comparacion.typ, <tb:peso_comp>: fuerza sísmica en altura Fi, tonf.
SEISMIC_FORCES = {
    "MCT": (169.441, 150.393, 112.298, 55.155),
    "MSTA": (171.212, 152.070, 113.786, 56.359),
    "MSTO": (144.040, 127.600, 94.840, 45.700),
}

# 08_comparacion.typ, <tb:dist_comp>. Distorsiones adimensionales.
DRIFTS = {
    "X": {
        "MCT": (0.000913, 0.001214, 0.001181, 0.000974),
        "MSTA": (0.000884, 0.001263, 0.001299, 0.001128),
        "MSTO": (0.0009893, 0.0015821, 0.0016786, 0.0014464),
    },
    "Y": {
        "MCT": (0.000987, 0.001315, 0.001329, 0.001128),
        "MSTA": (0.000977, 0.001363, 0.001394, 0.001196),
        "MSTO": (0.0010339, 0.0015375, 0.0015714, 0.0013571),
    },
}
# Límite para albañilería, Tabla N.° 11 de la E.030; caps. 5 y 6.
DRIFT_LIMIT = 0.005

# 08_comparacion.typ, <tb:cortss_comp> (demanda V_E) y <tb:resco_comp> (ΣV_m), tonf.
SHEAR_DEMAND = {
    "X": {
        "MCT": (149.805, 143.820, 106.096, 53.192),
        "MSTA": (151.213, 143.586, 105.606, 51.238),
        "MSTO": (126.280, 119.140, 86.440, 40.640),
    },
    "Y": {
        "MCT": (151.569, 140.027, 103.783, 50.797),
        "MSTA": (170.371, 152.288, 113.828, 57.234),
        "MSTO": (157.680, 140.560, 104.540, 50.580),
    },
}
SHEAR_CAPACITY = {
    "X": {
        "MCT": (203.032, 218.577, 203.520, 188.147),
        "MSTA": (146.756, 188.368, 193.773, 183.562),
        "MSTO": (159.559, 197.110, 191.897, 180.622),
    },
    "Y": {
        "MCT": (247.868, 237.030, 226.513, 216.369),
        "MSTA": (196.633, 239.546, 236.702, 220.789),
        "MSTO": (204.134, 239.002, 230.567, 212.515),
    },
}

# 05_analisismanual.typ, <tb:agriet_xy> (MCT) y <tb:agriet_xy_pp> (MSTA).
# Piso 1: (V_e, 0.55 V_m) en tonf por Pier. Cumple si V_e <= 0.55 V_m.
CRACKING_FLOOR1 = {
    "MCT": {
        "X1": (7.032, 10.471),
        "X3": (6.405, 9.442),
        "X4": (7.050, 10.854),
        "X5": (7.923, 11.808),
        "X6": (5.703, 7.996),
        "X7": (6.676, 10.526),
        "X1_2": (7.033, 10.471),
        "X3_2": (6.405, 9.442),
        "X4_2": (7.050, 10.854),
        "X5_2": (7.923, 11.808),
        "X6_2": (5.703, 7.996),
        "Y1": (3.727, 8.924),
        "Y2": (3.687, 8.870),
        "Y3": (5.445, 11.302),
        "Y4": (5.513, 10.381),
        "Y5": (6.707, 10.933),
        "Y6": (6.133, 10.906),
        "Y7": (8.318, 13.725),
        "Y1_2": (5.214, 8.916),
        "Y2_2": (5.136, 8.848),
        "Y3_2": (6.280, 11.302),
        "Y4_2": (6.391, 10.381),
        "Y5_2": (6.972, 10.933),
        "Y6_2": (6.262, 10.906),
    },
    "MSTA": {
        "X1": (7.146, 6.501),
        "X3": (6.725, 9.074),
        "X4": (6.985, 8.268),
        "X5": (7.907, 7.066),
        "X6": (6.042, 7.002),
        "X7": (5.997, 4.891),
        "X1_2": (7.146, 6.501),
        "X3_2": (6.725, 9.074),
        "X4_2": (6.985, 8.268),
        "X5_2": (7.907, 7.066),
        "X6_2": (6.042, 7.002),
        "Y1": (4.079, 6.163),
        "Y2": (4.077, 6.156),
        "Y3": (5.821, 8.986),
        "Y4": (5.756, 8.325),
        "Y5": (7.038, 9.714),
        "Y6": (6.862, 9.017),
        "Y7": (9.727, 12.193),
        "Y1_2": (6.063, 5.988),
        "Y2_2": (6.076, 5.998),
        "Y3_2": (7.516, 8.860),
        "Y4_2": (7.408, 8.169),
        "Y5_2": (7.457, 9.594),
        "Y6_2": (7.306, 8.985),
    },
}

# 05_analisismanual.typ, <tb:esf_ax_comp>: σ_m del piso 1 en tonf/m² (MCT).
# Límites de la misma tabla en kgf/cm²: 0.2 f'm [1 − (h/35t)²] y 0.15 f'm.
AXIAL_WALL = "X7"
AXIAL_STRESS_FLOOR1 = {"MCT": 86.0, "MSTA": 34.892}  # tonf/m², muro X7
AXIAL_LIMITS = (9.383, 9.75)  # kgf/cm²

# 04_consideraciones.typ: evidencia de criterios de modelamiento.
MESH_STEP = 0.5  # m, malla N8: variación < 1 % respecto de N16 (tb:disc_p)
MESH_SIZES = (2.0, 1.0, 0.5, 0.25, 0.125)  # m, mallas N2 … N32 del muro de prueba
MESH_N16_VARIATION = 0.01  # %, mayor variación de deriva de N16 frente a N8
# Diferencia de cada modelo de prueba frente al de referencia, en %, con el signo de
# las tablas: peso total, fuerza sísmica, deriva y momento de mayor valor absoluto.
MODEL_CHECKS = {
    # Apoyo empotrado (MAE) frente a apoyo fijo o simple (MAF): tb:P_apo … tb:mom_apo.
    "apoyo": {"peso": 0.00, "fuerza": 0.00, "deriva": -2.63, "momento": 1.89},
    # Sin columnas ni vigas de confinamiento (MSC) frente al modelo con ellas (MCC).
    "confinamiento": {"peso": -5.96, "fuerza": -5.96, "deriva": 38.50},
    # Opciones por defecto de ETABS (MPD) frente al modelo ajustado (MM).
    "automaticas": {"peso": 0.02, "fuerza": 0.03, "deriva": -10.53},
}
NO_CONFINEMENT_DRIFT = MODEL_CHECKS["confinamiento"]["deriva"]
AUTOMATIC_DRIFT = MODEL_CHECKS["automaticas"]["deriva"]

# 05_analisismanual.typ, <tb:asig_cargas>: (CM de acabados, CV) en tonf/m² por Load Set.
LOAD_SETS = {"Piso típico": (0.10, 0.20), "Azotea": (0.10, 0.10)}
LIVE_MASS_SHARE = 0.25  # fig:mass_s: masa = 100 % CM + 25 % CV (edificación común)
# <tb:an_mod>, MCT: el modo 3 es la traslación pura en Y.
MODE_Y = {"modo": 3, "T": 0.171, "UY": 0.8048}


def crack_failures(model: str) -> list[str]:
    return [pier for pier, (ve, cap) in CRACKING_FLOOR1[model].items() if ve > cap]


def relative(a: float, b: float) -> float:
    """Diferencia relativa (b - a) / b en %, como en las notas de las tablas del cap. 8."""
    return (b - a) / b * 100
