"""Comprueba la transcripción contra las tablas reales del submódulo TesisUCSP.

No requiere importar el runtime gráfico de Gaanim ni instalar dependencias:
``python -m unittest discover -s tests -v``.
"""

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from tesis.data.planta import FLOOR_AREA, density, wall_area_sum  # noqa: E402
from tesis.data.porticos import BARS, X4, X4_START  # noqa: E402
from tesis.data.thesis import (  # noqa: E402
    AXIAL_LIMITS,
    AXIAL_STRESS_FLOOR1,
    AXIAL_WALL,
    CRACKING_FLOOR1,
    DENSITY_MIN,
    DRIFTS,
    LOAD_SETS,
    MODE_Y,
    MODELS,
    SEISMIC_FORCES,
    SEISMIC_WEIGHT,
    SHEAR_CAPACITY,
    SHEAR_DEMAND,
    WEIGHT_BY_FLOOR,
    crack_failures,
)


def table(chapter: str, label: str) -> str:
    end = chapter.index(f")<{label}>")
    start = chapter.rfind("#apa_tbl(", 0, end)
    assert start >= 0, label
    return chapter[start:end]


def pier_rows(block: str, columns: int) -> dict[str, list[float]]:
    """Filas `[X1], [v1], ...` de una tabla por Pier; acepta `X1_2` y `X1\\_2`."""
    rows: dict[str, list[float]] = {}
    for line in block.splitlines():
        cells = re.findall(r"\[([^\]]*)\]", line)
        if not cells:
            continue
        name = cells[0].replace("\\_", "_")
        if re.fullmatch(r"[XY][0-9](_2)?", name) and len(cells) > columns:
            rows[name] = [float(c) for c in cells[1 : columns + 1]]
    return rows


class ComparisonTablesTest(unittest.TestCase):
    """Capítulo 8: comparación de MCT, MSTA y MSTO."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.chapter = (ROOT / "TesisUCSP/08_comparacion.typ").read_text(
            encoding="utf-8"
        )

    def test_seismic_weight_totals_and_floors(self) -> None:
        block = table(self.chapter, "tb:pesos_comp")
        total = re.search(
            r"\[Total\],\s*\[([\d.]+)\],\s*\[([\d.]+)\],\s*\[([\d.]+)\]", block
        )
        assert total is not None
        self.assertEqual(tuple(map(float, total.groups())), SEISMIC_WEIGHT)
        for floor, *values in re.findall(
            r"\[([1-4])\],\s*\[([\d.]+)\],\s*\[([\d.]+)\],\s*\[([\d.]+)\]", block
        ):
            for model, value in zip(MODELS, values, strict=True):
                self.assertEqual(WEIGHT_BY_FLOOR[model][int(floor) - 1], float(value))

    def test_seismic_forces_by_floor(self) -> None:
        rows = re.findall(
            r"\[([1-4])\],\s*\[([\d.]+)\],\s*\[([\d.]+)\],\s*\[([\d.]+)\]",
            table(self.chapter, "tb:peso_comp"),
        )
        self.assertEqual(len(rows), 4)
        for floor, *values in rows:
            for model, value in zip(MODELS, values, strict=True):
                self.assertEqual(SEISMIC_FORCES[model][int(floor) - 1], float(value))

    def test_profiles_match_both_directions_and_all_floors(self) -> None:
        for label, data in [
            ("tb:dist_comp", DRIFTS),
            ("tb:cortss_comp", SHEAR_DEMAND),
            ("tb:resco_comp", SHEAR_CAPACITY),
        ]:
            rows = re.findall(
                r"\[([1-4])\],\s*\[([\d.]+)\],\s*\[([\d.]+)\],\s*\[([\d.]+)\]",
                table(self.chapter, label),
            )
            self.assertEqual(len(rows), 8, label)
            for direction, group in [("X", rows[:4]), ("Y", rows[4:])]:
                for floor, *values in group:
                    for model, value in zip(MODELS, values, strict=True):
                        with self.subTest(
                            table=label, direction=direction, model=model, floor=floor
                        ):
                            self.assertEqual(
                                data[direction][model][int(floor) - 1], float(value)
                            )


class ManualProcessTablesTest(unittest.TestCase):
    """Capítulo 5: verificaciones por muro y densidad del caso."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.chapter = (ROOT / "TesisUCSP/05_analisismanual.typ").read_text(
            encoding="utf-8"
        )

    def test_cracking_floor_one_per_pier(self) -> None:
        for model, label in [("MCT", "tb:agriet_xy"), ("MSTA", "tb:agriet_xy_pp")]:
            rows = pier_rows(table(self.chapter, label), 8)
            self.assertEqual(len(rows), 24, label)
            for pier, values in rows.items():
                with self.subTest(model=model, pier=pier):
                    self.assertEqual(
                        CRACKING_FLOOR1[model][pier], (values[0], values[1])
                    )

    def test_cracking_failures_quoted_in_slides(self) -> None:
        self.assertEqual(crack_failures("MCT"), [])
        self.assertEqual(
            sorted(crack_failures("MSTA")),
            sorted(["X1", "X5", "X7", "X1_2", "X5_2", "Y1_2", "Y2_2"]),
        )

    def test_axial_stress_example(self) -> None:
        for model, label in [("MCT", "tb:esf_ax_comp"), ("MSTA", "tb:esf_ax_pp")]:
            rows = pier_rows(table(self.chapter, label), 6)
            sigma_1, sigma_2, floor_1 = rows[AXIAL_WALL][:3]
            self.assertEqual((sigma_1, sigma_2), AXIAL_LIMITS)
            self.assertEqual(floor_1, AXIAL_STRESS_FLOOR1[model])
        # X7 es el muro más exigido del piso 1 en MCT.
        mct = pier_rows(table(self.chapter, "tb:esf_ax_comp"), 6)
        self.assertEqual(max(mct, key=lambda pier: mct[pier][2]), AXIAL_WALL)

    def test_density_from_plan_matches_table(self) -> None:
        block = table(self.chapter, "tb:densidad_ejm")
        sums = [float(v) for v in re.findall(r"=\s*([\d.]+)\s*slash\s*136\.51", block)]
        self.assertEqual(len(sums), 2)
        self.assertAlmostEqual(wall_area_sum("X"), sums[0], delta=0.005)
        self.assertAlmostEqual(wall_area_sum("Y"), sums[1], delta=0.005)
        self.assertEqual(FLOOR_AREA, 136.51)
        self.assertAlmostEqual(density("X"), 0.0480, delta=0.00005)
        self.assertAlmostEqual(density("Y"), 0.0374, delta=0.00005)
        self.assertAlmostEqual(DENSITY_MIN, 0.032, delta=0.0005)

    def test_load_sets_of_the_full_model(self) -> None:
        block = table(self.chapter, "tb:asig_cargas")
        rows = re.findall(
            r"\[(Piso Típico|Techo Último Piso)\].*?\[\$([\d.]+).*?\[\$([\d.]+)", block
        )
        found = {name: (float(cm), float(cv)) for name, cm, cv in rows}
        self.assertEqual(found["Piso Típico"], LOAD_SETS["Piso típico"])
        self.assertEqual(found["Techo Último Piso"], LOAD_SETS["Azotea"])

    def test_plane_frame_example_wall(self) -> None:
        block = table(self.chapter, "tb:geome")
        row = re.search(
            r"\[X4\],\s*\[([\d.]+)\],\s*\[([\d.]+)\],\s*\[([\d.]+)\],\s*\[([\d.]+)\]",
            block,
        )
        assert row is not None
        cg, a1, a2, i3 = (float(v) for v in row.groups())
        self.assertEqual((cg, a1, a2, i3), (X4["cg"], X4["A1"], X4["A2"], X4["I3"]))
        # Una barra por muro: 14 muros y sus simétricos (X7 e Y7 no se repiten).
        self.assertEqual(len(BARS), 26)
        self.assertEqual(len({name for name, _, _ in BARS}), 26)
        # La barra de X4 está a cg de la cara exterior de la columna de Y4.
        x4 = next((x, y) for name, x, y in BARS if name == "X4")
        self.assertAlmostEqual(x4[0], X4_START + X4["cg"], delta=0.001)

    def test_translation_mode_in_y(self) -> None:
        block = table(self.chapter, "tb:an_mod")
        modes = {
            int(cells[0]): [float(c) for c in cells[1:]]
            for cells in (
                re.findall(r"\[([^\]]*)\]", line) for line in block.splitlines()
            )
            if len(cells) == 7 and cells[0].isdigit()
        }
        period, ux, uy, rz = modes[MODE_Y["modo"]][:4]
        self.assertEqual((period, uy), (MODE_Y["T"], MODE_Y["UY"]))
        self.assertEqual((ux, rz), (0.0, 0.0))  # traslación pura, sin giro
        # Es el modo con más masa en Y.
        self.assertEqual(max(modes, key=lambda m: modes[m][2]), MODE_Y["modo"])


if __name__ == "__main__":
    unittest.main()
