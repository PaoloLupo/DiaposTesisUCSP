"""Bloque 7 · Resultados: comparación descriptiva de MCT, MSTA y MSTO (cap. 8).

Todas las cifras salen de ``tesis.data.thesis``; las diferencias relativas se
calculan con la misma base que las notas de las tablas del capítulo 8.
"""

from gaanim import (
    Anchor,
    Axis,
    Color,
    CoordinateSpace,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    stagger,
)

from tesis.building import DEPTH, WALLS, WIDTH, Plan, draw_plan
from tesis.data.thesis import (
    CRACKING_FLOOR1,
    DRIFT_LIMIT,
    DRIFTS,
    FLOORS,
    MODELS,
    SEISMIC_FORCES,
    SEISMIC_WEIGHT,
    SHEAR_CAPACITY,
    SHEAR_DEMAND,
    crack_failures,
    relative,
)
from tesis.components import chip, compare_table, enter, header, page, pill, source
from tesis.kit import LEFT_EDGE, label, t
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    CONCRETE_SOFT,
    DISPLAY,
    FAIL,
    FAIL_SOFT,
    INK,
    INK_SOFT,
    MODEL_COLORS,
    MONO,
    MUTED,
    PAPER_DEEP,
    PASS,
    PASS_SOFT,
    STEEL,
    STEEL_SOFT,
)

KICKER = "07 · Resultados"
SOFT = {"MCT": BRICK_SOFT, "MSTA": STEEL_SOFT, "MSTO": CONCRETE_SOFT}

MATRIX = [
    ("Norma sismorresistente", ("E.030 vigente", "E.030 vigente", "E.030 (2003)")),
    ("Factor de zona", ("Z = 0.45", "Z = 0.45", "Z = 0.40")),
    ("Sismo ortogonal 100 % + 30 %", ("sí", "sí", "no")),
    ("Peralte de columnas", ("≥ 0.25 m", "≥ 0.25 m", "0.20 m")),
    ("Idealización de muros", ("áreas (shell)", "barras", "barras")),
    ("Programa de análisis", ("ETABS", "ETABS", "SAP2000")),
    ("Procesamiento", ("Alba · API", "hojas de cálculo", "San Bartolomé (2006)")),
]


def models(scene: Scene) -> None:
    header(scene, KICKER, "Tres modelos del mismo edificio: qué cambia entre ellos")
    names = {
        "MCT": "completo tridimensional",
        "MSTA": "simplificado actualizado",
        "MSTO": "simplificado original",
    }
    models_ = list(names)
    table = compare_table(
        scene,
        columns=[(m, names[m], MODEL_COLORS[m], SOFT[m]) for m in models_],
        rows=[
            (
                aspect,
                [
                    (
                        values[j],
                        values[j] != values[0],
                        MODEL_COLORS[m] if values[j] != values[0] else INK_SOFT,
                    )
                    for j, m in enumerate(models_)
                ],
            )
            for aspect, values in MATRIX
        ],
    )
    L = scene.layout
    logic = L.column(
        *[
            L.row(
                chip(
                    scene,
                    text=pair,
                    color=color,
                    background=CARD,
                    border=color,
                    font=DISPLAY,
                    width="250px",
                ),
                L.box(text, font_size="26px", color=INK),
                gap="24px",
                align="center",
            )
            for pair, text, color in [
                (
                    "MCT ↔ MSTA",
                    "misma norma: la diferencia viene de la idealización y del procesamiento",
                    BRICK,
                ),
                (
                    "MSTA ↔ MSTO",
                    "misma idealización: la diferencia viene de la norma (E.030 y E.070)",
                    STEEL,
                ),
            ]
        ],
        gap="16px",
        width="fill",
    )
    page(scene, body=[table, logic], gap="36px", top="185px", justify="start")
    scene.play(enter(table, each=0.03, duration=0.25))
    scene.stop("modelos-matriz")

    scene.play(enter(logic, each=0.1))
    source(
        scene,
        "Tesis · §8.1 Diferencias encontradas entre los modelos analizados, p. 126 · la propuesta E.070 (2019) "
        "se adoptó como caso de análisis",
    )
    scene.stop("modelos-logica")


def weight_forces(scene: Scene) -> None:
    header(
        scene, KICKER, "Peso y fuerza sísmica: la norma pesa más que la idealización"
    )
    # Peso sísmico total: barras desde cero para no exagerar diferencias pequeñas.
    base_y, scale = -2.3, 4.0 / 500
    xs = {"MCT": -5.9, "MSTA": -4.35, "MSTO": -2.8}
    title_l = label(
        scene, "Peso sísmico total P (tonf)", LEFT_EDGE, 2.45, color=MUTED, size=0.14
    )
    axis = scene.geometry.line(LEFT_EDGE + 0.4, base_y, -1.9, base_y).stroke(
        INK_SOFT, 0.015
    )
    bars: list[Drawable] = []
    labels: list[Drawable] = []
    for model, value in zip(MODELS, SEISMIC_WEIGHT, strict=True):
        h = value * scale
        mask = (
            scene.geometry.rect(1.05, h)
            .no_fill()
            .no_stroke()
            .move_to(xs[model], base_y + h / 2)
        )
        bars.append(
            scene.geometry.fill_level(
                mask, MODEL_COLORS[model], 0, direction="up", keep_outline=False
            )
        )
        labels.append(
            t(
                scene,
                f"{value:.1f}",
                xs[model],
                base_y + h + 0.1,
                font=MONO,
                size=0.18,
                color=INK,
                anchor=Anchor.BOTTOM,
            )
        )
        labels.append(
            t(
                scene,
                model,
                xs[model],
                base_y - 0.12,
                size=0.2,
                weight=900,
                color=MODEL_COLORS[model],
                anchor=Anchor.TOP,
            )
        )
    scene.play(
        [title_l.animate.fade_in().duration(0.3), axis.animate.create().duration(0.4)]
    )
    scene.play(
        stagger(*[b.animate.fill_level(1).duration(0.7) for b in bars], each=0.12)
    )
    scene.play(stagger(*[x.animate.fade_in().duration(0.3) for x in labels], each=0.04))
    d1 = relative(SEISMIC_WEIGHT[0], SEISMIC_WEIGHT[1])
    d2 = relative(SEISMIC_WEIGHT[1], SEISMIC_WEIGHT[2])
    notes = [
        pill(
            scene,
            f"MSTA pesa {d1:.2f} % más que MCT",
            LEFT_EDGE,
            -2.95,
            size=0.17,
            color=BRICK_DEEP,
            background=BRICK_SOFT,
            anchor=Anchor.LEFT,
            font="Lato",
            weight=700,
        ),
        pill(
            scene,
            f"MSTO pesa {abs(d2):.2f} % menos",
            LEFT_EDGE + 3.35,
            -2.95,
            size=0.17,
            color=INK_SOFT,
            background=PAPER_DEEP,
            anchor=Anchor.LEFT,
            font="Lato",
            weight=700,
        ),
    ]
    scene.play(stagger(*[n.animate.fade_in().duration(0.3) for n in notes], each=0.15))
    scene.stop("peso-sismico")

    # Fuerza sísmica por nivel: barras horizontales agrupadas, piso 4 arriba.
    x0, fscale = 0.9, 5.6 / 180
    title_r = label(
        scene, "Fuerza sísmica por nivel (tonf)", 0.2, 2.45, color=MUTED, size=0.14
    )
    groups: list[Drawable] = []
    values_text: list[Drawable] = []
    fills: list[Drawable] = []
    for k, floor in enumerate(reversed(FLOORS)):
        yc = 1.75 - k * 1.2
        groups.append(
            t(
                scene,
                f"Piso {floor}",
                0.2,
                yc,
                size=0.2,
                weight=900,
                color=INK,
                anchor=Anchor.LEFT,
            )
        )
        for j, model in enumerate(MODELS):
            value = SEISMIC_FORCES[model][floor - 1]
            y = yc + 0.3 - j * 0.3
            w = value * fscale
            mask = (
                scene.geometry.rect(w, 0.22)
                .no_fill()
                .no_stroke()
                .move_to(x0 + w / 2, y)
            )
            fills.append(
                scene.geometry.fill_level(
                    mask, MODEL_COLORS[model], 0, direction="right", keep_outline=False
                )
            )
            values_text.append(
                t(
                    scene,
                    f"{value:.1f}",
                    x0 + w + 0.1,
                    y,
                    font=MONO,
                    size=0.14,
                    color=INK_SOFT,
                    anchor=Anchor.LEFT,
                )
            )
    scene.play(
        [
            title_r.animate.fade_in().duration(0.3),
            *[g.animate.fade_in().duration(0.3) for g in groups],
        ]
    )
    scene.play(
        stagger(*[f.animate.fill_level(1).duration(0.5) for f in fills], each=0.04)
    )
    scene.play(
        stagger(*[v.animate.fade_in().duration(0.2) for v in values_text], each=0.02)
    )
    top_msta = relative(SEISMIC_FORCES["MCT"][3], SEISMIC_FORCES["MSTA"][3])
    top_msto = relative(SEISMIC_FORCES["MSTA"][3], SEISMIC_FORCES["MSTO"][3])
    callout = t(
        scene,
        f"Piso 4: MSTA {top_msta:.2f} % mayor que MCT  ·  MSTO {abs(top_msto):.1f} % menor que MSTA",
        0.2,
        -3.05,
        size=0.2,
        weight=700,
        color=INK,
        anchor=Anchor.LEFT,
    )
    scene.play(callout.animate.fade_in().duration(0.4))
    source(
        scene,
        "Tesis · Tablas 50 y 51, pp. 129–130 · diferencias con la base de las notas de cada tabla",
    )
    scene.stop("fuerzas-altura")


PANEL_Y = 0.0
PANEL_H = 3.3


def _profile_panel(
    scene: Scene,
    cx: float,
    x_max: float,
    step: float | None,
    precision: int,
    series: dict[str, tuple[float, ...]],
    *,
    width: float = 5.6,
    height: float = PANEL_H,
) -> tuple[CoordinateSpace, list[Drawable]]:
    """Perfil por piso: eje vertical 1-4 y un trazo con marcadores por modelo.

    ``step=None`` deja las marcas automáticas, que se recalculan con ``view_to``.
    """
    x_axis = Axis.linear(0, x_max)
    if step is not None:
        x_axis = x_axis.ticks(step)
    plane = scene.viz.cartesian_2d(
        x_axis.numbers("fixed", precision=precision),
        Axis.linear(0.5, 4.5).ticks(1).numbers("fixed", precision=0),
        width=width,
        height=height,
        grid=False,
        y_grid=True,
    )
    plane.move_to(cx, PANEL_Y)
    visuals: list[Drawable] = []
    for model, values in series.items():
        color = MODEL_COLORS[model]
        visuals.append(
            plane.plot_data(list(values), list(FLOORS), color=color, width=0.03)
        )
        visuals.append(plane.scatter_data(list(values), list(FLOORS), color=color))
    return plane, visuals


def _panel_titles(
    scene: Scene, cx: float, direction: str, axis_label: str
) -> list[Drawable]:
    return [
        t(
            scene,
            f"Dirección {direction}-{direction}",
            cx,
            2.05,
            size=0.24,
            weight=900,
            color=INK,
            anchor=Anchor.CENTER,
        ),
        t(scene, axis_label, cx, -2.25, size=0.17, color=MUTED, anchor=Anchor.TOP),
        t(scene, "piso", cx - 3.2, 1.72, size=0.15, color=MUTED, anchor=Anchor.LEFT),
    ]


def _legend(scene: Scene, y: float) -> list[Drawable]:
    items: list[Drawable] = []
    x = -2.3
    for model in MODELS:
        items.append(
            scene.geometry.circle(0.07)
            .fill(MODEL_COLORS[model])
            .no_stroke()
            .move_to(x, y)
        )
        items.append(
            t(
                scene,
                model,
                x + 0.18,
                y,
                size=0.2,
                weight=900,
                color=MODEL_COLORS[model],
                anchor=Anchor.LEFT,
            )
        )
        x += 1.75
    return items


def _draw_panels(
    scene: Scene,
    x_max: float,
    step: float | None,
    precision: int,
    data: dict[str, dict[str, tuple[float, ...]]],
    axis_label: str,
    *,
    limit: float | None = None,
    titles: bool = True,
):
    planes: list[CoordinateSpace] = []
    groups: list[list[Drawable]] = []
    for direction, cx in (("X", -3.6), ("Y", 3.6)):
        plane, visuals = _profile_panel(
            scene, cx, x_max, step, precision, data[direction]
        )
        extras: list[Drawable] = []
        if limit is not None:
            extras.append(
                plane.plot_data([limit, limit], [0.5, 4.5], color=FAIL, width=0.022)
            )
        labels = _panel_titles(scene, cx, direction, axis_label) if titles else []
        scene.play(
            [
                plane.animate.create().duration(0.6),
                *[x.animate.fade_in().duration(0.3) for x in labels],
            ]
        )
        scene.play(
            stagger(*[v.animate.create().duration(0.5) for v in visuals], each=0.1)
        )
        if extras:
            scene.play([e.animate.create().duration(0.4) for e in extras])
        planes.append(plane)
        groups.append(visuals + extras)
    return planes, groups


def drifts(scene: Scene) -> None:
    header(scene, KICKER, "Derivas: todas muy por debajo del límite de 0.005")
    legend = _legend(scene, 2.45)
    scene.play([x.animate.fade_in().duration(0.3) for x in legend])
    series = {
        d: {m: tuple(v * 100 for v in DRIFTS[d][m]) for m in MODELS} for d in ("X", "Y")
    }
    planes, _ = _draw_panels(
        scene, 0.55, None, 2, series, "distorsión (%)", limit=DRIFT_LIMIT * 100
    )
    # El límite se rotula sobre su propia línea, en gris, en lugar de explicarse abajo.
    tags: list[Drawable] = []
    for plane, cx in zip(planes, (-3.6, 3.6), strict=True):
        lx, ly = plane.data_to_local(DRIFT_LIMIT * 100, 4.5)
        tags.append(
            t(
                scene,
                "límite E.030 · 0.5 %",
                cx + lx + 0.1,
                PANEL_Y + ly,
                size=0.16,
                color=MUTED,
                anchor=Anchor.TOP_LEFT,
            )
        )
    limit_note = scene.geometry.group(tags)
    scene.play(limit_note.animate.fade_in().duration(0.3))
    scene.stop("derivas-limite")

    # Detalle 0–0.2 %: la misma escala en X e Y; el límite queda fuera de la ventana.
    scene.play(
        [
            *[p.animate.view_to((0, 0.2), (0.5, 4.5)).duration(1.2) for p in planes],
            limit_note.animate.fade_out().duration(0.4),
        ]
    )
    d_msta = relative(DRIFTS["X"]["MCT"][3], DRIFTS["X"]["MSTA"][3])
    d_msto = relative(DRIFTS["X"]["MCT"][3], DRIFTS["X"]["MSTO"][3])
    notes = [
        t(
            scene,
            f"MCT es hasta {d_msta:.2f} % menor que MSTA (X, piso 4) y {d_msto:.1f} % menor que MSTO",
            0,
            -2.85,
            size=0.21,
            weight=700,
            color=INK,
            anchor=Anchor.CENTER,
        ),
        t(
            scene,
            "Excepción: en el piso 1 MCT supera ligeramente a MSTA en ambas direcciones",
            0,
            -3.2,
            size=0.18,
            color=INK_SOFT,
            anchor=Anchor.CENTER,
        ),
    ]
    scene.play(stagger(*[n.animate.fade_in().duration(0.4) for n in notes], each=0.15))
    source(scene, "Tesis · Tabla 52, p. 131 · detalle 0–0.2 %, misma escala en X e Y")
    scene.stop("derivas-detalle")


def _bar_panel(
    scene: Scene,
    cx: float,
    x_max: float,
    step: float,
    series: dict[str, tuple[float, ...]],
    *,
    width: float = 5.6,
    height: float = PANEL_H,
) -> tuple[CoordinateSpace, list[Drawable], list[Drawable]]:
    """Barras horizontales agrupadas por piso: una por modelo, MCT arriba."""
    plane = scene.viz.cartesian_2d(
        Axis.linear(0, x_max).ticks(step).numbers("fixed", precision=0),
        Axis.linear(0.5, 4.5).ticks(1).numbers("fixed", precision=0),
        width=width,
        height=height,
        grid=False,
        x_grid=True,
    )
    plane.move_to(cx, PANEL_Y)
    bar_h, pitch = 0.19, 0.23
    fills: list[Drawable] = []
    values: list[Drawable] = []
    for j, model in enumerate(series):
        for floor, value in zip(FLOORS, series[model], strict=True):
            x0, y = plane.data_to_local(0, floor)
            x1, _ = plane.data_to_local(value, floor)
            y = PANEL_Y + y + (1 - j) * pitch
            w = x1 - x0
            mask = (
                scene.geometry.rect(w, bar_h)
                .no_fill()
                .no_stroke()
                .move_to(cx + x0 + w / 2, y)
            )
            fills.append(
                scene.geometry.fill_level(
                    mask, MODEL_COLORS[model], 0, direction="right", keep_outline=False
                )
            )
            values.append(
                t(
                    scene,
                    f"{value:.1f}",
                    cx + x1 + 0.08,
                    y,
                    font=MONO,
                    size=0.13,
                    color=INK_SOFT,
                    anchor=Anchor.LEFT,
                )
            )
    return plane, fills, values


def shear(scene: Scene) -> None:
    header(scene, KICKER, "Cortante de sismo severo: en Y, MCT reduce la demanda")
    legend = _legend(scene, 2.45)
    scene.play([x.animate.fade_in().duration(0.3) for x in legend])
    for direction, cx in (("X", -3.6), ("Y", 3.6)):
        plane, fills, values = _bar_panel(scene, cx, 200, 50, SHEAR_DEMAND[direction])
        labels = _panel_titles(scene, cx, direction, "$V_E$ (tonf)")
        scene.play(
            [
                plane.animate.create().duration(0.6),
                *[x.animate.fade_in().duration(0.3) for x in labels],
            ]
        )
        scene.play(
            stagger(*[f.animate.fill_level(1).duration(0.5) for f in fills], each=0.04)
        )
        scene.play(
            stagger(*[v.animate.fade_in().duration(0.2) for v in values], each=0.02)
        )
    y_gap = max(
        relative(SHEAR_DEMAND["Y"]["MCT"][i], SHEAR_DEMAND["Y"]["MSTA"][i])
        for i in range(4)
    )
    x_msto = min(
        relative(SHEAR_DEMAND["X"]["MCT"][i], SHEAR_DEMAND["X"]["MSTO"][i])
        for i in range(4)
    )
    notes = [
        t(
            scene,
            f"Y-Y: MCT hasta {y_gap:.2f} % menor que MSTA; capta el aporte de los muros ortogonales",
            0,
            -2.85,
            size=0.21,
            weight=700,
            color=INK,
            anchor=Anchor.CENTER,
        ),
        t(
            scene,
            f"X-X: MCT ≈ MSTA (confinamientos T/L asignados a X) · la norma vigente eleva $V_E$ hasta "
            f"{abs(x_msto):.1f} % frente a MSTO",
            0,
            -3.2,
            size=0.18,
            color=INK_SOFT,
            anchor=Anchor.CENTER,
        ),
    ]
    scene.play(stagger(*[n.animate.fade_in().duration(0.4) for n in notes], each=0.15))
    source(scene, "Tesis · Tabla 53, p. 133 · $V_E$ de cada entrepiso")
    scene.stop("cortante")


def resistance(scene: Scene) -> None:
    header(scene, KICKER, "Resistencia global: MSTA no cumple en el piso 1 X-X")
    legend = _legend(scene, 2.45)
    scene.play([x.animate.fade_in().duration(0.3) for x in legend])
    ratios = {
        d: {
            m: tuple(SHEAR_DEMAND[d][m][i] / SHEAR_CAPACITY[d][m][i] for i in range(4))
            for m in MODELS
        }
        for d in ("X", "Y")
    }
    planes, _ = _draw_panels(
        scene,
        1.2,
        0.2,
        1,
        ratios,
        "demanda / capacidad  ($V_E slash sum V_m$)",
        limit=1.0,
    )
    lx, ly = planes[0].data_to_local(ratios["X"]["MSTA"][0], 1)
    ring = (
        scene.geometry.circle(0.17)
        .no_fill()
        .stroke(FAIL, 0.03)
        .move_to(-3.6 + lx, PANEL_Y + ly)
    )
    scene.play(ring.animate.create().duration(0.4))
    scene.stop("resistencia-grafico")
    demand, cap_msta = SHEAR_DEMAND["X"]["MSTA"][0], SHEAR_CAPACITY["X"]["MSTA"][0]
    cap_mct = SHEAR_CAPACITY["X"]["MCT"][0]
    # El diagnóstico como cifra protagonista: D/C en grande y su lectura al lado.
    box = t(
        scene,
        f"{demand / cap_msta:.3f}",
        LEFT_EDGE,
        -2.62,
        font=DISPLAY,
        size=0.62,
        weight=700,
        color=FAIL,
    )
    box_w = box.bounds().width
    line1 = t(
        scene,
        f"D/C en MSTA · piso 1 · X-X:  $sum V_m$ = {cap_msta:.1f} < $V_E$ = {demand:.1f} tonf",
        LEFT_EDGE + box_w + 0.4,
        -2.75,
        size=0.22,
        weight=900,
        color=INK,
    )
    line2 = t(
        scene,
        f"MCT obtiene $sum V_m$ = {cap_mct:.1f} tonf ({abs(relative(cap_mct, cap_msta)):.1f} % más): "
        "$P_g$ del metrado automático y redistribución de la losa",
        LEFT_EDGE + box_w + 0.4,
        -3.12,
        size=0.19,
        color=INK_SOFT,
    )
    scene.play(
        stagger(
            box.animate.fade_in_from(Direction.UP, 0.08).duration(0.45),
            line1.animate.fade_in().duration(0.4),
            line2.animate.fade_in().duration(0.4),
            each=0.12,
        )
    )
    source(
        scene,
        "Tesis · Tablas 53 y 54, pp. 133–134; Tabla 38, p. 89 (MSTA: «No cumple · replantear»)",
    )
    scene.stop("resistencia-diagnostico")


PASS_WALL = "#86AE97"


def cracking(scene: Scene) -> None:
    header(scene, KICKER, "Fisuración en el piso 1: el diagnóstico depende del modelo")
    for model, cx in (("MCT", -3.75), ("MSTA", 3.75)):
        plan = draw_plan(
            scene,
            (cx, 0.2),
            6.5,
            grid=False,
            labels=False,
            drawn_thickness=0.1,
            color_x="#C9C3B8",
            color_y="#C9C3B8",
        )
        data = CRACKING_FLOOR1[model]
        fails = crack_failures(model)
        head = t(
            scene,
            model,
            cx - 3.25,
            2.62,
            font=DISPLAY,
            size=0.36,
            weight=700,
            color=MODEL_COLORS[model],
        )
        head_w = head.bounds().width
        sub = t(
            scene,
            "modelo completo · Alba"
            if model == "MCT"
            else "pórticos planos · hojas de cálculo",
            cx - 3.25 + head_w + 0.25,
            2.48,
            size=0.18,
            color=INK_SOFT,
        )
        count = t(
            scene,
            f"{len(fails)} de {len(data)}",
            cx - 3.25,
            -1.95,
            font=DISPLAY,
            size=0.5,
            weight=700,
            color=FAIL if fails else PASS,
        )
        count_l = t(
            scene,
            "muros no cumplen $V_e <= 0.55 V_m$",
            cx - 3.25,
            -2.6,
            size=0.2,
            color=INK_SOFT,
        )
        scene.play(
            stagger(
                head.animate.fade_in().duration(0.3),
                sub.animate.fade_in().duration(0.3),
                plan.slab.animate.fade_in().duration(0.4),
                plan.void.animate.fade_in().duration(0.3),
                stagger(
                    *[w.animate.fade_in().duration(0.2) for w in plan.all_walls],
                    each=0.01,
                ),
                each=0.12,
            )
        )
        recolor = []
        tags: list[Drawable] = []
        for pier, (ve, cap) in data.items():
            ok = ve <= cap
            recolor.append(
                plan.walls[pier].animate.fill(PASS_WALL if ok else FAIL).duration(0.4)
            )
            if not ok:
                x, y, anchor = _tag_position(plan, pier)
                tags.append(
                    pill(
                        scene,
                        f"{ve / cap:.2f}",
                        x,
                        y,
                        size=0.13,
                        color=Color.from_hex("#FFFFFF"),
                        background=FAIL,
                        anchor=anchor,
                    )
                )
        # El diagnóstico barre la planta de izquierda a derecha, como una inspección.
        scene.play(stagger(*recolor, total=0.9, origin=plan.to_scene(0, DEPTH / 2)))
        scene.play(
            [
                *[g.animate.fade_in().duration(0.3) for g in tags],
                count.animate.fade_in().duration(0.4),
                count_l.animate.fade_in().duration(0.4),
            ]
        )
        scene.stop(f"fisuracion-{model.lower()}")
    legend = [
        pill(
            scene,
            "X2: concreto, no aplica",
            0.3,
            -3.15,
            size=0.16,
            font="Lato",
            color=INK_SOFT,
            background=PAPER_DEEP,
            anchor=Anchor.LEFT,
        ),
        pill(
            scene,
            "cumple",
            3.0,
            -3.15,
            size=0.16,
            font="Lato",
            weight=700,
            color=PASS,
            background=PASS_SOFT,
            anchor=Anchor.LEFT,
        ),
        pill(
            scene,
            "no cumple · $V_e slash 0.55 V_m$",
            4.3,
            -3.15,
            size=0.16,
            font="Lato",
            weight=700,
            color=FAIL,
            background=FAIL_SOFT,
            anchor=Anchor.LEFT,
        ),
    ]
    scene.play([x.animate.fade_in().duration(0.3) for x in legend])
    source(
        scene,
        "Tesis · Tablas 35 (MCT) y 36 (MSTA), pp. 86–87, sismo moderado, piso 1 · mismo edificio y misma norma",
    )
    scene.stop("fisuracion-comparacion")


def _tag_position(plan: Plan, pier: str) -> tuple[float, float, Anchor]:
    """Etiqueta del cociente junto al muro, sin tapar muros vecinos."""
    base = next(w for w in WALLS if w.name == pier.split("_")[0])
    mirrored = pier.endswith("_2")
    if base.direction == "X":
        x = (base.start + base.end) / 2
        x = WIDTH - x if mirrored else x
        sx, sy = plan.to_scene(x, base.fixed)
        # Bordes: etiqueta por fuera de la planta; muros interiores: por debajo.
        return (
            (sx, sy + 0.16, Anchor.BOTTOM)
            if base.fixed > 7.9
            else (sx, sy - 0.16, Anchor.TOP)
        )
    x = WIDTH - base.fixed if mirrored else base.fixed
    sx, sy = plan.to_scene(x, (base.start + base.end) / 2)
    if x < 0.1:
        return sx - 0.14, sy, Anchor.RIGHT
    return sx + 0.14, sy, Anchor.LEFT


SECTION = Section(
    "resultados",
    [
        SectionStep(
            name="Resultados · modelos comparados",
            build=models,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. MCT: modelo completo en ETABS procesado con Alba. MSTA: pórticos planos "
                "actualizados, ETABS + hojas de cálculo. MSTO: referencia de San Bartolomé (2006) en "
                "SAP2000 con E.030-2003. La lógica de lectura: MCT vs MSTA aísla la idealización y el "
                "procesamiento (misma norma); MSTA vs MSTO aísla la norma (misma idealización). La "
                "comparación es descriptiva: no mide una tasa de error de Alba."
            ),
        ),
        SectionStep(
            name="Resultados · peso y fuerzas",
            build=weight_forces,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Tabla 50 (p. 129): 451.84 / 456.57 / 432.11 tonf. MSTA pesa 1.04 % más que MCT "
                "(áreas tributarias vs volumen modelado); MSTO pesa 5.66 % menos que MSTA por columnas "
                "de 0.20 m. Tabla 51 (p. 130): Fi difiere a lo más 2.14 % entre MCT y MSTA, pero MSTO es "
                "hasta 23.3 % menor que MSTA en el piso 4 por el cambio de Z y de la E.030."
            ),
        ),
        SectionStep(
            name="Resultados · derivas",
            build=drifts,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Primer encuadre con el límite 0.5 %: todas las derivas quedan lejos. "
                "Detalle 0–0.2 %: MCT (áreas) es más rígido; hasta 13.65 % menor que MSTA en X piso 4 "
                "y 32.7 % menor que MSTO. Excepción: piso 1, MCT supera ligeramente a MSTA (X 0.000913 vs "
                "0.000884; Y 0.000987 vs 0.000977). La mayor rigidez de MSTA frente a MSTO se atribuye a "
                "las columnas de 0.25 m."
            ),
        ),
        SectionStep(
            name="Resultados · cortante",
            build=shear,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Tabla 53 (p. 133). En Y, MCT es hasta 11.25 % menor que MSTA: el modelo de áreas "
                "considera el aporte de muros ortogonales. En X ambos casi coinciden porque los "
                "confinamientos de intersecciones T/L se asignaron al Pier de la dirección X (limitación "
                "de ETABS: un elemento no pertenece a dos Pier). MSTO es hasta 30.9 % menor en X por la "
                "E.030-2003."
            ),
        ),
        SectionStep(
            name="Resultados · resistencia global",
            build=resistance,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.25 min. Cociente V_E / ΣV_m por piso: todo por debajo de 1 salvo MSTA, piso 1, X-X: "
                "151.213 / 146.756 = 1.030, que la hoja de cálculo marca como 'No cumple · replantear'. "
                "MCT obtiene 203.032 tonf (38 % más) porque el metrado automático da una P_g más "
                "representativa y la losa redistribuye cargas. El diagnóstico depende del modelo."
            ),
        ),
        SectionStep(
            name="Resultados · fisuración",
            build=cracking,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.25 min. Control de fisuración con sismo moderado en el piso 1 (Tabla 35 (p. 86) y "
                "Tabla 36 (p. 87)). MCT: los 24 muros de albañilería cumplen. MSTA: 7 de 24 no cumplen "
                "(X1, X5, X7, sus simétricos X1′ y X5′, e Y1′, Y2′). Es el mismo edificio y la misma "
                "norma: cambia la idealización. X2 es de concreto y no se evalúa con este criterio."
            ),
        ),
    ],
)
