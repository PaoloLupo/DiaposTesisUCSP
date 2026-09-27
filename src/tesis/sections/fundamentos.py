"""Bloque 3 · Fundamentos: qué exige la E.070 y la E.030 a una distribución de muros.

La densidad usa la planta real del caso (tb:densidad_ejm). Las verificaciones de
resistencia muestran un ejemplo real por pregunta. La deriva es un esquema
cinemático exagerado, sin solución FEM.
"""

from typing import Literal

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    computed,
    parallel,
    part,
    sequence,
    stagger,
)

from tesis.building import (
    FLOOR_AREA,
    STAIR,
    WALLS,
    WIDTH,
    density,
    draw_plan,
    grow_walls,
    wall_area_sum,
)
from tesis.data.thesis import (
    AXIAL_LIMITS,
    AXIAL_STRESS_FLOOR1,
    AXIAL_WALL,
    CRACKING_FLOOR1,
    DENSITY_MIN,
    DRIFT_LIMIT,
    DRIFTS,
    SHEAR_CAPACITY,
    SHEAR_DEMAND,
)
from tesis.kit import (
    LEFT_EDGE,
    dimension,
    header,
    label,
    panel,
    source,
    status,
    t,
    takeaway,
)
from tesis.theme import (
    BRICK,
    BRICK_SOFT,
    CARD,
    CONCRETE,
    CONCRETE_SOFT,
    DISPLAY,
    FAINT,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PASS,
    RULE,
    STEEL,
)

KICKER = "03 · Fundamentos"


def density_check(scene: Scene) -> None:
    header(scene, KICKER, "Densidad de muros: cada dirección se revisa por separado")

    plan = draw_plan(scene, (-3.45, 0.0), 7.3, grid=False, drawn_thickness=0.09)
    area_note = t(
        scene,
        f"Planta típica · $A_p$ = {FLOOR_AREA:.2f} m² · t = 0.13 m",
        -3.45,
        -2.05,
        font=MONO,
        size=0.15,
        color=MUTED,
        anchor=Anchor.TOP,
    )
    # Presentación gradual de la planta: primero el contorno y los ejes, luego
    # los muros por dirección, cada grupo con su entrada en la leyenda.
    stair_note = t(
        scene,
        "escalera",
        *plan.to_scene((STAIR[0] + STAIR[2]) / 2, (STAIR[1] + STAIR[3]) / 2),
        font=MONO,
        size=0.12,
        color=MUTED,
        anchor=Anchor.CENTER,
    )
    gx, gy, arm = LEFT_EDGE + 0.2, -2.55, 0.45
    axes = [
        scene.geometry.arrow(
            gx, gy, gx + arm, gy, head_length=0.1, head_width=0.1, body_width=0.018
        )
        .fill(BRICK)
        .no_stroke(),
        scene.geometry.arrow(
            gx, gy, gx, gy + arm, head_length=0.1, head_width=0.1, body_width=0.018
        )
        .fill(STEEL)
        .no_stroke(),
    ]
    axis_labels = [
        t(
            scene,
            "X",
            gx + arm + 0.08,
            gy,
            font=MONO,
            size=0.14,
            color=BRICK,
            anchor=Anchor.LEFT,
        ),
        t(
            scene,
            "Y",
            gx,
            gy + arm + 0.08,
            font=MONO,
            size=0.14,
            color=STEEL,
            anchor=Anchor.BOTTOM,
        ),
    ]
    scene.play(
        stagger(
            plan.slab.animate.fade_in().duration(0.5),
            parallel(
                plan.void.animate.fade_in().duration(0.3),
                stair_note.animate.fade_in().duration(0.3),
            ),
            area_note.animate.fade_in().duration(0.3),
            parallel(
                *[a.animate.grow_arrow().duration(0.4) for a in axes],
                *[a.animate.fade_in().duration(0.4) for a in axis_labels],
            ),
            each=0.25,
        )
    )

    legend_y = 2.3

    def legend(x: float, color: str, text: str) -> list[Drawable]:
        swatch = (
            scene.geometry.rect(0.3, 0.09)
            .fill(color)
            .no_stroke()
            .move_to(x + 0.15, legend_y)
        )
        name = t(
            scene,
            text,
            x + 0.4,
            legend_y,
            size=0.16,
            color=INK_SOFT,
            anchor=Anchor.LEFT,
        )
        return [swatch, name]

    masonry_x = [
        d
        for name, d in plan.walls.items()
        if name.startswith("X") and name.split("_")[0] != "X2"
    ]
    groups = [
        (legend(LEFT_EDGE + 0.2, BRICK, "Muros en X"), masonry_x),
        (legend(LEFT_EDGE + 2.3, STEEL, "Muros en Y"), plan.by_direction("Y")),
        (legend(LEFT_EDGE + 4.4, CONCRETE, "Concreto (X2)"), plan.instances("X2")),
    ]
    for items, walls in groups:
        scene.play(
            parallel(
                *[i.animate.fade_in().duration(0.3) for i in items],
                grow_walls(walls, total=0.5, duration=0.35),
            )
        )
    scene.play(stair_note.animate.fade_out().duration(0.3))
    scene.stop("densidad-planta")
    scene.wait(0.05)  # que la pausa no capture el primer trazo de la fórmula

    x0 = 1.15
    formula = scene.text.equation(
        part("d", "D"),
        "=",
        "frac(",
        part("area", "sum L t", color=BRICK),
        ",",
        part("ap", "A_p"),
        ")",
        ">=",
        part("req", "frac(Z U S N, 56)", color=STEEL),
        size=0.42,
    ).move_to(x0, 2.35, Anchor.TOP_LEFT)
    minimum = scene.text.equation(
        'D_"mín" = frac(0.45 dot 1 dot 1 dot 4, 56) =',
        part("v", f'{DENSITY_MIN * 100:.2f} "%"', color=STEEL),
        size=0.3,
    ).move_to(x0, 1.12, Anchor.TOP_LEFT)
    scene.play([formula.animate.write().duration(0.9)])
    scene.play(minimum.animate.fade_in_from(Direction.UP, 0.08).duration(0.5))

    # L y t no se leen a escala de planta: un inset amplía el muro X1′ de la esquina
    # y lo acota. Las cotas viven en una capa que solo muestra el inset.
    wall = next(w for w in WALLS if w.name == "X1")
    wx0, wy = plan.to_scene(WIDTH - wall.end, wall.fixed)
    wx1, _ = plan.to_scene(WIDTH - wall.start, wall.fixed)
    zoom, half = 2.3, 0.045  # medio espesor dibujado
    cotas = [
        dimension(
            scene,
            (wx0, wy - half),
            (wx1, wy - half),
            f"L = {wall.length:.2f} m",
            side="below",
            offset=0.16,
            size=0.16 / zoom,
            width=0.01 / zoom,
        ),
        dimension(
            scene,
            (wx1, wy - half),
            (wx1, wy + half),
            f"t = {wall.thickness:.2f} m",
            side="right",
            offset=0.1,
            size=0.16 / zoom,
            width=0.01 / zoom,
        ),
    ]
    for cota in cotas:
        cota.view_layer("cotas")
    detail = scene.camera.inset(
        ((wx0 + wx1) / 2 + 0.06, wy + 0.14),
        zoom=zoom,
        at=(4.3, -1.1),
        size=4.4,
        shape="rect",
        color=INK_SOFT,
        layers=["cotas"],
    )
    scene.play(
        [
            detail.animate.pop_out().duration(0.8),
            # En su capa solo las ve el inset; entran cuando la pantalla ya brotó.
            *[c.animate.fade_in().duration(0.3).delay(0.6) for c in cotas],
        ]
    )
    scene.stop("densidad-formula")
    # El inset vuelve al muro antes de sumar por dirección.
    scene.play(detail.animate.pop_in().duration(0.5))

    rows: tuple[tuple[Literal["X", "Y"], float], ...] = (("X", 0.2), ("Y", -1.45))
    for direction, y in rows:
        color = BRICK if direction == "X" else STEEL
        tag = label(
            scene, f"Dirección {direction}", x0, y + 0.3, color=color, size=0.15
        )
        sum_label = scene.text.equation(f"sum (L t)_{direction} =", size=0.28).move_to(
            x0, y - 0.28, Anchor.LEFT
        )
        counter = scene.viz.rolling_number(
            0,
            decimals=2,
            suffix=" m²",
            font_family=DISPLAY,
            weight=700,
            font_size=0.3,
            mode="odometer",
            color=INK,
        )
        counter.move_to(x0 + 1.55, y - 0.28, Anchor.LEFT)
        track_left, track_w = x0 + 2.95, 2.9
        track = (
            scene.geometry.rect(track_w, 0.16)
            .fill(FAINT)
            .no_stroke()
            .move_to(track_left + track_w / 2, y - 0.28)
        )
        ratio = computed(
            lambda v: min(v / FLOOR_AREA / 0.06, 1.0), inputs=[counter.parameter]
        )
        bar = scene.geometry.fill_level(
            track, color, direction="left", keep_outline=False
        ).set_fill_level(ratio)
        threshold_x = track_left + track_w * DENSITY_MIN / 0.06
        tick = scene.geometry.line(threshold_x, y - 0.1, threshold_x, y - 0.46).stroke(
            INK, 0.018
        )
        tick_label = t(
            scene,
            "mín",
            threshold_x,
            y - 0.5,
            font=MONO,
            size=0.12,
            color=MUTED,
            anchor=Anchor.TOP,
        )
        result = scene.text.equation(
            f"D_{direction} = frac({wall_area_sum(direction):.2f}, {FLOOR_AREA:.2f}) =",
            part("v", f'{density(direction) * 100:.2f} "%"', color=color),
            ">=",
            f'{DENSITY_MIN * 100:.2f} "%"',
            size=0.27,
        ).move_to(x0, y - 0.72, Anchor.TOP_LEFT)
        other = "Y" if direction == "X" else "X"
        dim = [w.animate.opacity(0.15).duration(0.4) for w in plan.by_direction(other)]
        lit = [w.animate.opacity(1).duration(0.4) for w in plan.by_direction(direction)]
        scene.play(
            [
                *dim,
                *lit,
                *[
                    i.animate.fade_in().duration(0.35)
                    for i in (
                        tag,
                        sum_label,
                        counter.visual,
                        track,
                        bar,
                        tick,
                        tick_label,
                    )
                ],
            ]
        )
        cumulative = 0.0
        steps = []
        for name, drawable in plan.walls.items():
            if not name.startswith(direction):
                continue
            wall = next(w for w in WALLS if w.name == name.split("_")[0])
            cumulative += wall.area
            steps.append(
                [
                    drawable.animate.indicate().duration(0.3),
                    counter.animate.set(round(cumulative, 2)).duration(0.28),
                ]
            )
        for step in steps:
            scene.play(step)
        if direction == "X":
            x2 = plan.walls["X2"]
            note = t(
                scene,
                'X2 · concreto: $t_"eq" = t thin E_c slash E_m$ = 0.794 m',
                -3.9,
                -2.45,
                font=MONO,
                size=0.15,
                color=CONCRETE,
                anchor=Anchor.TOP,
            )
            scene.play(
                [
                    x2.animate.indicate().duration(0.5),
                    note.animate.fade_in().duration(0.4),
                ]
            )
        chip = status(scene, density(direction) >= DENSITY_MIN, 6.6, y - 0.9, size=0.16)
        scene.play(
            [
                result.animate.fade_in_from(Direction.UP, 0.06).duration(0.5),
                chip.animate.fade_in().duration(0.3),
            ]
        )
        scene.stop(f"densidad-{direction.lower()}")

    scene.play([w.animate.opacity(1).duration(0.4) for w in plan.all_walls])
    takeaway(
        scene,
        "Cumple en ambas direcciones; Y queda más cerca del mínimo",
        y=-3.22,
    )
    source(
        scene,
        "Tesis · Tabla 22, p. 57 (E.070, art. 19.2b) · Z = 0.45, U = 1, S = 1, N = 4 · "
        "planta de San Bartolomé (2006)",
    )
    scene.stop("densidad-conclusion")


def _mini_wall(
    scene: Scene, cx: float, cy: float, w: float, h: float
) -> list[Drawable]:
    """Muro confinado simplificado: ladrillos en soga, columnas y solera."""
    col, beam = 0.22, 0.2
    panel_ = (
        scene.geometry.rect(w - 2 * col, h - beam)
        .fill(BRICK_SOFT)
        .no_stroke()
        .move_to(cx, cy - beam / 2)
    )
    # Una hilada por grupo; cada hilada se desplaza medio ladrillo (aparejo de soga).
    brick_w, brick_h, joint = 0.3, 0.1, 0.025
    left, right = cx - w / 2 + col, cx + w / 2 - col
    bottom = cy - h / 2
    courses: list[Drawable] = []
    for r in range(int((h - beam) / (brick_h + joint))):
        y = bottom + joint + brick_h / 2 + r * (brick_h + joint)
        x = left - (brick_w / 2 if r % 2 else 0)
        bricks: list[Drawable] = []
        while x < right - 0.02:
            a, b = max(x, left), min(x + brick_w, right)
            if b - a > 0.05:
                bricks.append(
                    scene.geometry.rect(b - a - joint, brick_h)
                    .fill("#C57457")  # BRICK aclarado sobre la tarjeta
                    .no_stroke()
                    .move_to((a + b) / 2, y)
                )
            x += brick_w
        courses.append(scene.geometry.group(bricks))
    cols = [
        scene.geometry.rect(col, h)
        .fill(CONCRETE_SOFT)
        .stroke(CONCRETE, 0.01)
        .move_to(x, cy)
        for x in (cx - w / 2 + col / 2, cx + w / 2 - col / 2)
    ]
    top = (
        scene.geometry.rect(w, beam)
        .fill(CONCRETE_SOFT)
        .stroke(CONCRETE, 0.01)
        .move_to(cx, cy + h / 2 - beam / 2)
    )
    base = scene.geometry.line(
        cx - w / 2 - 0.25, cy - h / 2, cx + w / 2 + 0.25, cy - h / 2
    ).stroke(INK_SOFT, 0.016)
    return [panel_, *courses, *cols, top, base]


def strength_checks(scene: Scene) -> None:
    header(scene, KICKER, "Tres verificaciones de resistencia, por muro y por piso")
    w, gap = 4.6, 0.25
    axial = AXIAL_STRESS_FLOOR1["MCT"] / 10  # tonf/m² → kgf/cm²
    limit = min(AXIAL_LIMITS)
    ve, cap = CRACKING_FLOOR1["MCT"]["X1"]
    demand, capacity = SHEAR_DEMAND["X"]["MCT"][0], SHEAR_CAPACITY["X"]["MCT"][0]
    cards = [
        {
            "tag": "Gravedad",
            "color": INK_SOFT,
            "question": "¿La compresión en el muro\nes admisible?",
            "eq": [
                "sigma_m = P_m slash (L t)",
                "sigma_m <= 0.2 f'_m [1 - (h slash 35 t)^2] <= 0.15 f'_m",
            ],
            "case": f"{AXIAL_WALL} · piso 1 · MCT",
            "value": f"{axial:.2f} ≤ {limit:.2f} kgf/cm²",
            "share": f"{axial / limit * 100:.0f} % del límite",
        },
        {
            "tag": "Sismo moderado",
            "color": STEEL,
            "question": "¿Se evita la fisuración\npor corte del muro?",
            "eq": ["V_e <= 0.55 V_m", "V_m = 0.5 v'_m alpha t L + 0.23 P_g"],
            "case": "X1 · piso 1 · MCT",
            "value": f"{ve:.2f} ≤ {cap:.2f} tonf",
            "share": f"{ve / cap * 100:.0f} % de $0.55 V_m$",
        },
        {
            "tag": "Sismo severo",
            "color": BRICK,
            "question": "¿Los muros del piso resisten\nen conjunto?",
            "eq": ["sum V_(m i) >= V_(E i)", "V_(E i) = 2 sum V_(e i)"],
            "case": "Piso 1 · X-X · MCT",
            "value": f"{capacity:.1f} ≥ {demand:.1f} tonf",
            "share": f"demanda / capacidad = {demand / capacity:.2f}",
        },
    ]
    for i, spec in enumerate(cards):
        x0 = LEFT_EDGE + i * (w + gap)
        cx = x0 + w / 2
        frame = panel(scene, x0, 2.4, w, 5.7, fill=CARD, anchor=Anchor.TOP_LEFT)
        drawing: list[Drawable] = []
        loads: list[Drawable] = []
        if i < 2:
            drawing = _mini_wall(scene, cx, 1.1, 2.6, 1.5)
            if i == 0:
                arrow = (
                    scene.geometry.arrow(
                        cx,
                        2.3,
                        cx,
                        1.88,
                        head_length=0.14,
                        head_width=0.2,
                        body_width=0.04,
                    )
                    .fill(INK)
                    .no_stroke()
                )
                loads = [
                    scene.geometry.arrow(
                        cx + dx,
                        2.2,
                        cx + dx,
                        1.88,
                        head_length=0.1,
                        head_width=0.12,
                        body_width=0.025,
                    )
                    .fill(INK_SOFT)
                    .no_stroke()
                    for dx in (-0.9, -0.45, 0.45, 0.9)
                ]
                p_lab = t(
                    scene,
                    "$P_m$",
                    cx + 1.1,
                    2.1,
                    font=MONO,
                    size=0.24,
                    color=INK,
                    anchor=Anchor.LEFT,
                )
                extras = [arrow, *loads, p_lab]
            else:
                arrow = (
                    scene.geometry.arrow(
                        cx - 2.1,
                        1.75,
                        cx - 1.32,
                        1.75,
                        head_length=0.16,
                        head_width=0.16,
                        body_width=0.035,
                    )
                    .fill(STEEL)
                    .no_stroke()
                )
                cracks = [
                    scene.geometry.dashed_line(
                        cx - 0.95, 0.45, cx + 0.95, 1.6, dash_length=0.08, gap_length=0.05
                    ).stroke(STEEL, 0.02),
                    scene.geometry.dashed_line(
                        cx + 0.95, 0.45, cx - 0.95, 1.6, dash_length=0.08, gap_length=0.05
                    )
                    .stroke(STEEL, 0.02)
                    .opacity(0.35),
                ]
                v_lab = t(
                    scene,
                    "$V_e$",
                    cx - 2.1,
                    1.88,
                    font=MONO,
                    size=0.24,
                    color=STEEL,
                    anchor=Anchor.BOTTOM_LEFT,
                )
                extras = [arrow, v_lab, *cracks]
        else:
            plan = draw_plan(
                scene,
                (cx, 1.35),
                3.4,
                grid=False,
                drawn_thickness=0.055,
                color_y="#C9CED6",
                slab_fill="#F1EDE6",
            )
            arrow = (
                scene.geometry.arrow(
                    cx - 2.15,
                    1.35,
                    cx - 1.8,
                    1.35,
                    head_length=0.14,
                    head_width=0.16,
                    body_width=0.035,
                )
                .fill(BRICK)
                .no_stroke()
            )
            drawing = [plan.slab, plan.void, *plan.all_walls]
            extras = [
                arrow,
                t(
                    scene,
                    "$V_E$",
                    cx - 2.15,
                    1.5,
                    font=MONO,
                    size=0.24,
                    color=BRICK,
                    anchor=Anchor.BOTTOM_LEFT,
                ),
            ]
        tag = label(scene, spec["tag"], x0 + 0.3, 0.2, color=spec["color"], size=0.15)
        question = t(
            scene, spec["question"], x0 + 0.3, -0.05, size=0.24, weight=700, color=INK
        )
        eq1 = scene.text.equation(spec["eq"][0], size=0.3).move_to(
            x0 + 0.3, -0.85, Anchor.TOP_LEFT
        )
        eq2 = scene.text.equation(spec["eq"][1], size=0.22, color=INK_SOFT).move_to(
            x0 + 0.3, -1.45, Anchor.TOP_LEFT
        )
        divider = scene.geometry.line(x0 + 0.3, -2.0, x0 + w - 0.3, -2.0).stroke(
            RULE, 0.01
        )
        case = t(
            scene, spec["case"], x0 + 0.3, -2.12, font=MONO, size=0.15, color=MUTED
        )
        value = t(
            scene, spec["value"], x0 + 0.3, -2.42, size=0.26, weight=900, color=INK
        )
        share = t(scene, spec["share"], x0 + 0.3, -2.8, size=0.17, color=INK_SOFT)
        chip = status(scene, True, x0 + w - 0.3, -2.62, anchor=Anchor.RIGHT, size=0.15)
        scene.play(
            stagger(
                frame.animate.fade_in().duration(0.3),
                stagger(
                    *[d.animate.fade_in().duration(0.3) for d in drawing], each=0.01
                ),
                stagger(
                    *[
                        (
                            e.animate.grow_arrow()
                            if any(e is a for a in (arrow, *loads))
                            else e.animate.fade_in()
                        ).duration(0.35)
                        for e in extras
                    ],
                    each=0.08,
                ),
                tag.animate.fade_in().duration(0.3),
                question.animate.fade_in_from(Direction.UP, 0.06).duration(0.4),
                eq1.animate.write().duration(0.6),
                eq2.animate.fade_in().duration(0.4),
                divider.animate.create().duration(0.3),
                stagger(
                    case.animate.fade_in().duration(0.3),
                    value.animate.fade_in().duration(0.3),
                    share.animate.fade_in().duration(0.3),
                    chip.animate.fade_in().duration(0.3),
                    each=0.08,
                ),
                each=0.12,
            )
        )
        scene.stop(f"verificacion-{i + 1}")
    source(
        scene,
        "Tesis · Figuras 44 y 45, pp. 107 y 109 (E.070, arts. 19.1b, 26.2 y 26.3) · "
        "valores: Tablas 31, 35 y 37, pp. 82, 86 y 88",
    )
    scene.stop("verificaciones-fuente")


def drift(scene: Scene) -> None:
    header(scene, KICKER, "Deriva: lo que cuenta es el desplazamiento relativo")
    lower = scene.viz.parameter(0.0)
    upper = scene.viz.parameter(0.0)
    base_y, mid_y, top_y = -2.2, -0.2, 1.8
    base = scene.geometry.line(-6.6, base_y, -1.2, base_y).stroke(INK_SOFT, 0.03)
    hatch = [
        scene.geometry.line(x, base_y, x - 0.15, base_y - 0.15).stroke(MUTED, 0.01)
        for x in [-6.5 + 0.25 * k for k in range(22)]
    ]
    floors = [
        scene.geometry.line(length=4).stroke(STEEL, 0.07).move_to(-3.9, y)
        for y in (mid_y, top_y)
    ]
    floors[0].move_to(computed(lambda v: -3.9 + v, inputs=[lower]), mid_y)
    floors[1].move_to(computed(lambda v: -3.9 + v, inputs=[upper]), top_y)
    columns: list[Drawable] = []
    for dx in (-2, 2):
        p0 = scene.geometry.point_ref(-3.9 + dx, base_y)
        p1 = scene.geometry.point_ref(
            computed(lambda v, o=dx: -3.9 + o + v, inputs=[lower]), mid_y
        )
        p2 = scene.geometry.point_ref(
            computed(lambda v, o=dx: -3.9 + o + v, inputs=[upper]), top_y
        )
        columns += [
            scene.geometry.tracking_line(p0, p1).stroke(STEEL, 0.04),
            scene.geometry.tracking_line(p1, p2).stroke(STEEL, 0.04),
        ]
    labels = [
        t(
            scene,
            "Piso $i$",
            -6.4,
            top_y + 0.1,
            size=0.2,
            color=STEEL,
            anchor=Anchor.BOTTOM_LEFT,
        ),
        t(
            scene,
            "Piso $i − 1$",
            -6.4,
            mid_y + 0.1,
            size=0.2,
            color=STEEL,
            anchor=Anchor.BOTTOM_LEFT,
        ),
    ]
    scene.play(
        [
            base.animate.create().duration(0.5),
            *[h.animate.fade_in().duration(0.4) for h in hatch],
            *[f.animate.fade_in().duration(0.5) for f in floors + columns],
            *[l.animate.fade_in().duration(0.4) for l in labels],
        ]
    )

    x_text = 1.0
    step1 = t(
        scene,
        "1 · Ambos pisos se desplazan lo mismo",
        x_text,
        2.3,
        size=0.26,
        weight=900,
        color=INK,
    )
    scene.play(
        [
            lower.animate.set(0.35).duration(1.3),
            upper.animate.set(0.35).duration(1.3),
            step1.animate.fade_in().duration(0.5),
        ]
    )
    eq_common = scene.text.equation(
        "u_i = u_(i-1) quad arrow.double quad",
        part("d", "Delta u = 0", color=BRICK),
        size=0.4,
    ).move_to(x_text, 1.55, Anchor.TOP_LEFT)
    common_note = t(
        scene,
        "No hay deriva entre esos dos pisos (el primero sí\nse desplaza respecto de la base).",
        x_text,
        0.8,
        size=0.2,
        color=INK_SOFT,
    )
    scene.play(
        [
            eq_common.animate.write().duration(0.7),
            common_note.animate.fade_in().duration(0.5),
        ]
    )
    scene.stop("deriva-movimiento-comun")

    x_low = computed(lambda v: -1.9 + v, inputs=[lower])
    x_up = computed(lambda v: -1.9 + v, inputs=[upper])
    cota = scene.geometry.tracking_line(
        scene.geometry.point_ref(x_low, top_y + 0.45),
        scene.geometry.point_ref(x_up, top_y + 0.45),
    ).stroke(BRICK, 0.045)
    guides = [
        scene.geometry.tracking_line(
            scene.geometry.point_ref(x_low, mid_y),
            scene.geometry.point_ref(x_low, top_y + 0.55),
        ).stroke(RULE, 0.015),
        scene.geometry.tracking_line(
            scene.geometry.point_ref(x_up, top_y),
            scene.geometry.point_ref(x_up, top_y + 0.55),
        ).stroke(BRICK, 0.015),
    ]
    step2 = t(
        scene,
        "2 · El piso superior se desplaza más",
        x_text,
        2.3,
        size=0.26,
        weight=900,
        color=INK,
    )
    scene.play(
        [
            step1.animate.fade_out().duration(0.3),
            eq_common.animate.fade_out().duration(0.3),
            common_note.animate.fade_out().duration(0.3),
            step2.animate.fade_in().duration(0.4),
            *[g.animate.fade_in().duration(0.3) for g in [cota, *guides]],
        ]
    )
    scene.play(upper.animate.set(0.95).duration(1.4))
    du = t(
        scene,
        "$Δ u$",
        -1.3,
        top_y + 0.55,
        font=MONO,
        size=0.2,
        color=BRICK,
        anchor=Anchor.BOTTOM_LEFT,
    )
    height = [
        scene.geometry.line(-6.75, mid_y, -6.75, top_y).stroke(INK_SOFT, 0.018),
        scene.geometry.line(-6.85, mid_y, -6.65, mid_y).stroke(INK_SOFT, 0.018),
        scene.geometry.line(-6.85, top_y, -6.65, top_y).stroke(INK_SOFT, 0.018),
        t(
            scene,
            "$h_i$",
            -6.95,
            (mid_y + top_y) / 2,
            font=MONO,
            size=0.18,
            color=INK_SOFT,
            anchor=Anchor.RIGHT,
        ),
    ]
    equation = scene.text.equation(
        "theta_i = frac(",
        part("c", "c", color=STEEL),
        part("du", "Delta u", color=BRICK),
        ",",
        part("h", "h_i"),
        ") <= 0.005",
        size=0.5,
    ).move_to(x_text, 1.55, Anchor.TOP_LEFT)
    legend = t(
        scene,
        "u: desplazamiento elástico del análisis\n"
        "h: altura de entrepiso (2.40 m en el caso)\n"
        "c: 0.75 R (regular) o 0.85 R (irregular)",
        x_text,
        0.25,
        size=0.2,
        color=INK_SOFT,
    )
    scene.play(
        [
            du.animate.fade_in().duration(0.3),
            *[h.animate.fade_in().duration(0.4) for h in height],
            equation.animate.write().duration(0.9),
            legend.animate.fade_in().duration(0.5),
        ]
    )
    worst = max(DRIFTS["Y"]["MCT"])
    case = panel(scene, x_text, -1.2, 6.1, 1.15, fill=CARD, anchor=Anchor.TOP_LEFT)
    case_tag = label(
        scene, "En el caso (MCT)", x_text + 0.25, -1.4, color=MUTED, size=0.13
    )
    case_value = t(
        scene,
        f"máxima θ = {worst:.5f}  (Y-Y, piso 3)",
        x_text + 0.25,
        -1.68,
        size=0.25,
        weight=900,
        color=INK,
    )
    case_share = t(
        scene,
        f"{worst / DRIFT_LIMIT * 100:.0f} % del límite de albañilería",
        x_text + 0.25,
        -2.0,
        size=0.18,
        color=PASS,
    )
    scene.play(
        stagger(
            case.animate.fade_in().duration(0.3),
            case_tag.animate.fade_in().duration(0.3),
            case_value.animate.fade_in().duration(0.3),
            case_share.animate.fade_in().duration(0.3),
            each=0.08,
        )
    )
    source(
        scene,
        "Tesis · Figura 46, p. 110; E.030, Tabla N.° 11 · esquema con desplazamientos "
        "exagerados; valor del caso: Tabla 52, p. 131",
    )
    scene.stop("deriva-lectura")


SECTION = Section(
    "fundamentos",
    [
        SectionStep(
            name="Fundamentos · densidad",
            build=density_check,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.5 min. E.070 art. 19.2b. Con la planta real del caso: D_mín = ZUSN/56 = 3.21 % "
                "(Z = 0.45, U = S = 1, N = 4). En X se suman L·t de cada muro (X2 es de concreto y "
                "usa t_eq = t·Ec/Em = 0.794 m): Σ = 6.56 m², D_X = 4.80 %. En Y: Σ = 5.11 m², "
                f"D_Y = 3.74 %. A_p = {FLOOR_AREA} m². Ambas cumplen; Y está más ajustada. "
                "Fuente: Tabla 22 (p. 57). Cumplir densidad no acredita las demás verificaciones."
            ),
        ),
        SectionStep(
            name="Fundamentos · resistencia",
            build=strength_checks,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.5 min. Tres preguntas distintas. Axial (art. 19.1b): X7 del piso 1 en MCT, "
                "σ_m = 86.0 tonf/m² = 8.60 kgf/cm² frente a 9.38 kgf/cm² (92 %), el muro más "
                "exigido del modelo. Fisuración con sismo moderado (art. 26.2): X1, V_e = 7.03 "
                "frente a 0.55 V_m = 10.47 tonf. Resistencia global con sismo severo (art. 26.3): "
                "piso 1 X-X, ΣV_m = 203.0 frente a V_E = 149.8 tonf. Una verificación global "
                "favorable no prueba el cumplimiento local, y viceversa."
            ),
        ),
        SectionStep(
            name="Fundamentos · deriva",
            build=drift,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Primero ambos pisos se mueven igual: Δu = 0 entre ellos. Después solo "
                "sube el desplazamiento superior; la cota terracota es Δu, se amplifica con c y se "
                "divide entre h. El dibujo está exagerado y no es una solución FEM. Límite E.030 "
                "para albañilería: 0.005. En el caso MCT la máxima es 0.00133 (Y, piso 3), 27 % "
                "del límite (Tabla 52 (p. 131))."
            ),
        ),
    ],
)
