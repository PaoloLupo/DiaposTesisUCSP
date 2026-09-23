"""Bloque 5 · Marco de trabajo: qué se automatiza, flujo general, módulos y trazabilidad."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    sequence,
    stagger,
)

from tesis.building import density, wall_area_sum
from tesis.data.thesis import DENSITY_MIN, SHEAR_CAPACITY, SHEAR_DEMAND
from tesis.diagram import decision, io, link, process, terminal
from tesis.kit import LEFT_EDGE, header, label, panel, pill, source, status, t, takeaway
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    FAIL,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PAPER_DEEP,
    PASS,
    RULE,
    STEEL,
    STEEL_SOFT,
)

KICKER = "05 · Marco de trabajo"


def scope(scene: Scene) -> None:
    header(
        scene,
        KICKER,
        "Se automatiza lo repetitivo; las decisiones siguen en el ingeniero",
    )
    crit_label = label(
        scene, "Un proceso es clave si…", LEFT_EDGE, 2.42, color=MUTED, size=0.14
    )
    criteria = [
        "se repite en cada iteración",
        "maneja muchos datos iguales",
        "expone a errores de transcripción",
        "aplica un criterio normativo explícito",
        "alimenta la revisión del ingeniero",
    ]
    chips: list[Drawable] = []
    x = LEFT_EDGE
    y = 1.95
    for c in criteria:
        w_, _ = scene.text.measure(c, size=0.2, font="Lato")
        if x + w_ + 0.4 > 7.3:
            x, y = LEFT_EDGE, y - 0.5
        chips.append(
            pill(
                scene,
                c,
                x,
                y,
                size=0.2,
                font="Lato",
                color=INK,
                background=PAPER_DEEP,
                anchor=Anchor.LEFT,
            )
        )
        x += w_ + 0.5
    scene.play(
        [
            crit_label.animate.fade_in().duration(0.3),
            stagger(
                *[
                    c.animate.fade_in_from(Direction.UP, 0.06).duration(0.3)
                    for c in chips
                ],
                each=0.08,
            ),
        ]
    )
    scene.stop("criterios-procesos-clave")

    columns = [
        (
            LEFT_EDGE,
            "Ingeniero estructural",
            STEEL,
            STEEL_SOFT,
            [
                ("Estructura", "define la distribución de muros"),
                ("Modela y analiza", "construye el modelo en ETABS"),
                ("Interpreta", "lee diagnósticos y resultados"),
                ("Decide", "modifica muros, espesores o materiales"),
            ],
        ),
        (
            1.0,
            "Marco de trabajo · Alba",
            BRICK,
            BRICK_SOFT,
            [
                ("Extracción", "lee y valida datos del modelo por API"),
                ("Verificación", "ejecuta los módulos E.070 y E.030"),
                ("Retroalimentación", "señala muro, piso, dirección y valores"),
                ("Reporte", "documenta la iteración en PDF"),
            ],
        ),
    ]
    for x0, name, color, soft, items in columns:
        w = 6.3
        card = panel(scene, x0, 0.75, w, 3.35, fill=CARD, anchor=Anchor.TOP_LEFT)
        band = panel(
            scene,
            x0,
            0.75,
            w,
            0.55,
            fill=soft,
            border=None,
            anchor=Anchor.TOP_LEFT,
            radius=0.1,
        )
        title = t(
            scene,
            name,
            x0 + 0.25,
            0.475,
            size=0.24,
            weight=900,
            color=color,
            anchor=Anchor.LEFT,
        )
        rows: list[Drawable] = []
        for i, (head, body) in enumerate(items):
            yy = -0.05 - i * 0.66
            rows.append(
                scene.geometry.circle(0.06)
                .fill(color)
                .no_stroke()
                .move_to(x0 + 0.35, yy - 0.12)
            )
            rows.append(t(scene, head, x0 + 0.6, yy, size=0.22, weight=900, color=INK))
            rows.append(t(scene, body, x0 + 2.75, yy, size=0.21, color=INK_SOFT))
        scene.play(
            stagger(
                card.animate.fade_in().duration(0.3),
                band.animate.fade_in().duration(0.3),
                title.animate.fade_in().duration(0.3),
                stagger(*[r.animate.fade_in().duration(0.25) for r in rows], each=0.04),
                each=0.1,
            )
        )
    to_alba = link(scene, (-0.85, 0.05), (0.85, 0.05), color=MUTED)
    to_eng = link(scene, (0.85, -1.5), (-0.85, -1.5), color=MUTED)
    lab1 = t(scene, "modelo", 0, 0.12, size=0.15, color=MUTED, anchor=Anchor.BOTTOM)
    lab2 = t(
        scene, "diagnóstico", 0, -1.43, size=0.15, color=MUTED, anchor=Anchor.BOTTOM
    )
    scene.play(
        [
            to_alba.animate.create().duration(0.4),
            to_eng.animate.create().duration(0.4),
            lab1.animate.fade_in().duration(0.3),
            lab2.animate.fade_in().duration(0.3),
        ]
    )
    takeaway(
        scene,
        "El marco no genera la estructuración ni modifica el modelo: asiste la evaluación",
        y=-3.1,
    )
    source(
        scene,
        "Tesis · cap. 6, Procesos clave para la automatización y Evaluación de cumplimiento",
    )
    scene.stop("reparto")


def general_flow(scene: Scene) -> None:
    header(
        scene, KICKER, "El flujo general separa datos inconsistentes de incumplimientos"
    )
    y1, y2, y3 = 1.3, -1.05, -2.72
    loop_zone = panel(
        scene,
        -2.95,
        2.25,
        9.7,
        3.95,
        fill=PAPER_DEEP,
        border=None,
        radius=0.2,
        anchor=Anchor.TOP_LEFT,
    )
    loop_tag = label(
        scene, "Se repite en cada iteración", -2.7, 2.08, color=MUTED, size=0.13
    )
    t0 = terminal(scene, -6.75, y1, "Inicio", w=0.95)
    p1 = io(
        scene,
        -4.55,
        y1,
        2.55,
        1.0,
        "Proyecto configurado\ny modelo analizado\nen ETABS",
        size=0.185,
    )
    r2 = process(
        scene,
        -1.35,
        y1,
        2.55,
        1.0,
        "Importar y validar\ndatos mediante\nla API",
        border=BRICK,
        size=0.185,
    )
    r3 = process(
        scene,
        1.8,
        y1,
        2.55,
        1.0,
        "Procesar, clasificar\ny organizar por muro,\npiso y dirección",
        size=0.185,
    )
    r4 = process(
        scene,
        4.95,
        y1,
        2.55,
        1.0,
        "Ejecutar los módulos\nde verificación\nnormativa",
        border=BRICK,
        size=0.185,
    )
    p5 = io(
        scene,
        4.95,
        y2,
        2.7,
        1.0,
        "Consolidar resultados\ncon diagnósticos\ny trazabilidad",
        size=0.185,
    )
    d6 = decision(scene, 1.8, y2, 2.4, 1.35, "¿Nueva\niteración?", size=0.19)
    r9 = process(
        scene,
        -1.35,
        y2,
        2.55,
        1.0,
        "Modificar el modelo\nen ETABS y volver\na analizar",
        fill=STEEL_SOFT,
        border=STEEL,
        size=0.185,
    )
    p7 = io(scene, 1.8, y3, 2.55, 0.72, "Generar reporte PDF", size=0.19)
    t8 = terminal(scene, 4.35, y3, "Fin", w=0.9)
    diag = panel(
        scene, -6.95, -0.35, 3.45, 1.3, fill=CARD, border=RULE, anchor=Anchor.TOP_LEFT
    )
    diag_t = t(
        scene,
        "Dato ausente o incompatible:\nse emite un diagnóstico y se\ndetiene el módulo afectado.\nNo es un incumplimiento.",
        -6.75,
        -0.5,
        size=0.16,
        color=INK_SOFT,
    )
    links = [
        link(scene, (-6.27, y1), (-5.95, y1)),
        link(scene, (-3.12, y1), (-2.65, y1)),
        link(scene, (-0.07, y1), (0.5, y1)),
        link(scene, (3.08, y1), (3.65, y1)),
        link(scene, (4.95, y1 - 0.5), (4.95, y2 + 0.5)),
        link(scene, (3.55, y2), (3.02, y2)),
    ]
    yes = link(scene, (0.6, y2), (-0.05, y2), color=STEEL)
    back = link(scene, (-1.35, y2 + 0.5), (-1.35, y1 - 0.5), color=STEEL)
    no = link(scene, (1.8, y2 - 0.68), (1.8, y3 + 0.37))
    end = link(scene, (3.1, y3), (3.88, y3))
    to_diag = scene.geometry.dashed_line(
        -1.9, y1 - 0.5, -3.55, -0.35, dash_length=0.07, gap_length=0.05
    ).stroke(MUTED, 0.014)
    yes_t = t(
        scene,
        "sí",
        0.3,
        y2 + 0.08,
        size=0.16,
        weight=900,
        color=STEEL,
        anchor=Anchor.BOTTOM,
    )
    no_t = t(
        scene,
        "no",
        1.95,
        y2 - 0.95,
        size=0.16,
        weight=900,
        color=INK_SOFT,
        anchor=Anchor.LEFT,
    )

    scene.play(
        stagger(
            t0.animate.fade_in().duration(0.3),
            links[0].animate.create().duration(0.2),
            p1.animate.fade_in().duration(0.3),
            links[1].animate.create().duration(0.2),
            r2.animate.fade_in().duration(0.3),
            links[2].animate.create().duration(0.2),
            r3.animate.fade_in().duration(0.3),
            links[3].animate.create().duration(0.2),
            r4.animate.fade_in().duration(0.3),
            each=0.18,
        )
    )
    scene.play(
        stagger(
            to_diag.animate.create().duration(0.4),
            diag.animate.fade_in().duration(0.3),
            diag_t.animate.fade_in().duration(0.3),
            each=0.15,
        )
    )
    scene.stop("flujo-importacion")
    scene.play(
        stagger(
            links[4].animate.create().duration(0.25),
            p5.animate.fade_in().duration(0.3),
            links[5].animate.create().duration(0.2),
            d6.animate.fade_in().duration(0.3),
            stagger(
                yes.animate.create().duration(0.25),
                yes_t.animate.fade_in().duration(0.2),
                r9.animate.fade_in().duration(0.3),
                back.animate.create().duration(0.3),
                each=0.12,
            ),
            stagger(
                no.animate.create().duration(0.25),
                no_t.animate.fade_in().duration(0.2),
                p7.animate.fade_in().duration(0.3),
                end.animate.create().duration(0.2),
                t8.animate.fade_in().duration(0.3),
                each=0.12,
            ),
            each=0.2,
        )
    )
    scene.play(
        [
            loop_zone.animate.fade_in().duration(0.5),
            loop_tag.animate.fade_in().duration(0.5),
        ]
    )
    token = scene.geometry.circle(0.1).fill(BRICK).no_stroke().move_to(-1.35, y1 + 0.62)
    scene.play(token.animate.fade_in().duration(0.2))
    path = [
        (1.8, y1 + 0.62),
        (4.95, y1 + 0.62),
        (5.55, y2 + 0.62),
        (1.8, y2 + 0.8),
        (-0.3, y2 - 0.25),
        (-1.35, y1 + 0.62),
    ]
    scene.play(sequence(*[token.animate.move_to(x, y).duration(0.45) for x, y in path]))
    scene.play(token.animate.fade_out().duration(0.2))
    source(
        scene,
        "Tesis · cap. 6, fig:flujo_marco y Evaluación de cumplimiento y retroalimentación al usuario",
    )
    scene.stop("flujo-general")


def density_module(scene: Scene) -> None:
    header(
        scene, KICKER, "Cada verificación es un módulo con entradas, reglas y salidas"
    )
    tabs = ["Densidad", "Esfuerzo axial", "Fisuración y corte", "Derivas"]
    tab_items: list[Drawable] = []
    x = 0.55
    for i, name in enumerate(tabs):
        w_, _ = scene.text.measure(name, size=0.17, font="Lato")
        tab_items.append(
            pill(
                scene,
                name,
                x,
                2.47,
                size=0.17,
                font="Lato",
                weight=900 if i == 0 else 400,
                color=BRICK_DEEP if i == 0 else MUTED,
                background=BRICK_SOFT if i == 0 else PAPER_DEEP,
                anchor=Anchor.LEFT,
            )
        )
        x += w_ + 0.5
    scene.play(
        stagger(*[c.animate.fade_in().duration(0.25) for c in tab_items], each=0.06)
    )

    cx, w = -2.85, 5.3
    ys = [1.95, 1.12, 0.36, -0.32, -1.0, -1.68, -2.44, -3.18]
    nodes = [
        io(
            scene,
            cx,
            ys[0],
            w,
            0.6,
            "Parámetros Z, U, S, N, $A_p$ · tabla de muros (etiqueta, L, t, material)",
            size=0.165,
        ),
        decision(
            scene,
            cx,
            ys[1],
            3.9,
            0.85,
            "¿Datos completos y unidades compatibles?",
            size=0.165,
        ),
        process(
            scene,
            cx,
            ys[2],
            w,
            0.5,
            "Clasificar muros por dirección (X / Y) y material",
            size=0.175,
        ),
        process(
            scene,
            cx,
            ys[3],
            w,
            0.5,
            "Aporte efectivo: albañilería L·t · concreto L·t·Ec/Em",
            size=0.175,
        ),
        process(
            scene, cx, ys[4], w, 0.5, "Sumar los aportes de cada dirección", size=0.175
        ),
        process(
            scene,
            cx,
            ys[5],
            w,
            0.5,
            '$D_"mín" = Z U S N slash 56$   ·   $D = sum L t slash A_p$',
            size=0.175,
        ),
        decision(scene, cx, ys[6], 3.4, 0.8, '¿$D_X$ y $D_Y >= D_"mín"$?', size=0.175),
        io(
            scene,
            cx,
            ys[7],
            w,
            0.5,
            "Tabla comparativa y relación de muros considerados",
            size=0.165,
        ),
    ]
    arrows = [
        link(
            scene,
            (cx, ys[i] - (0.43 if i in (1, 6) else 0.3)),
            (cx, ys[i + 1] + (0.43 if i + 1 in (1, 6) else 0.3)),
        )
        for i in range(len(ys) - 1)
    ]
    side_error = t(
        scene,
        "no → diagnóstico,\nsin resultado",
        cx - 2.05,
        ys[1] + 0.05,
        size=0.14,
        color=FAIL,
        anchor=Anchor.RIGHT,
    )
    side_fail = t(
        scene,
        "no → registra dirección\ne incumplimiento",
        cx - 1.8,
        ys[6] + 0.05,
        size=0.14,
        color=FAIL,
        anchor=Anchor.RIGHT,
    )
    values = [
        "Z = 0.45 · U = 1 · S = 1 · N = 4 · $A_p$ = 136.51 m²",
        "✓ sin datos faltantes: continúa",
        "13 tramos en X (X2 de concreto) · 13 en Y",
        'X2: $t_"eq"$ = 0.13 × $E_c slash E_m$ = 0.794 m',
        f"$Sigma_X$ = {wall_area_sum('X'):.2f} m²  ·  $Sigma_Y$ = {wall_area_sum('Y'):.2f} m²",
        f'$D_"mín"$ = {DENSITY_MIN * 100:.2f} %  ·  $D_X$ = {density("X") * 100:.2f} %  ·  $D_Y$ = {density("Y") * 100:.2f} %',
        "✓ ambas direcciones cumplen",
        "salida: tabla y muros usados en el cálculo",
    ]
    value_items: list[Drawable] = []
    leaders: list[Drawable] = []
    for y, text in zip(ys, values, strict=True):
        leaders.append(
            scene.geometry.dashed_line(
                cx + w / 2 + 0.12, y, 0.45, y, dash_length=0.05, gap_length=0.05
            ).stroke(RULE, 0.01)
        )
        value_items.append(
            t(
                scene,
                text,
                0.55,
                y,
                font=MONO,
                size=0.17,
                color=PASS if text.startswith("✓") else INK,
                anchor=Anchor.LEFT,
            )
        )
    token = (
        scene.geometry.circle(0.09)
        .fill(BRICK)
        .no_stroke()
        .move_to(cx - w / 2 - 0.25, ys[0])
    )
    scene.play(stagger(*[n.animate.fade_in().duration(0.25) for n in nodes], each=0.06))
    scene.play(
        [
            *[a.animate.create().duration(0.3) for a in arrows],
            side_error.animate.fade_in().duration(0.3),
            side_fail.animate.fade_in().duration(0.3),
        ]
    )
    scene.stop("modulo-densidad")
    scene.play(token.animate.fade_in().duration(0.2))
    for i, y in enumerate(ys):
        scene.play(
            [
                token.animate.move_to(
                    cx - w / 2 - 0.25 if i not in (1, 6) else cx - 2.25, y
                ).duration(0.3),
                nodes[i].animate.indicate().duration(0.35),
                leaders[i].animate.create().duration(0.3),
                value_items[i]
                .animate.fade_in_from(Direction.LEFT, 0.08)
                .duration(0.35),
            ]
        )
    scene.play(token.animate.fade_out().duration(0.2))
    source(
        scene,
        "Tesis · cap. 6, fig:flujo_densidad (E.070 art. 19.2) · valores: cap. 5, tb:densidad_ejm",
    )
    scene.stop("modulo-recorrido")


def traceability(scene: Scene) -> None:
    header(scene, KICKER, "Cada resultado conserva su origen: modelo, piso y dirección")
    inputs = [
        (
            "Desde ETABS · API",
            BRICK,
            BRICK_SOFT,
            [
                "Geometría de muros y niveles",
                "Materiales y secciones",
                "Resultados: P, V, M y desplazamientos",
                "Etiquetas Pier, casos y combinaciones",
            ],
        ),
        (
            "Declarado por el usuario",
            STEEL,
            STEEL_SOFT,
            [
                "Datos del proyecto",
                "Z, U, S y factores de irregularidad",
                "f'm, f'c · N y A_p",
                "Nombres de combinaciones a usar",
            ],
        ),
    ]
    items: list[Drawable] = []
    for i, (name, color, soft, rows) in enumerate(inputs):
        y0 = 2.4 - i * 2.35
        items.append(
            panel(scene, LEFT_EDGE, y0, 4.85, 2.15, fill=CARD, anchor=Anchor.TOP_LEFT)
        )
        items.append(
            panel(
                scene,
                LEFT_EDGE,
                y0,
                4.85,
                0.48,
                fill=soft,
                border=None,
                anchor=Anchor.TOP_LEFT,
                radius=0.1,
            )
        )
        items.append(
            t(
                scene,
                name,
                LEFT_EDGE + 0.22,
                y0 - 0.24,
                size=0.2,
                weight=900,
                color=color,
                anchor=Anchor.LEFT,
            )
        )
        for j, row in enumerate(rows):
            items.append(
                t(
                    scene,
                    "· " + row,
                    LEFT_EDGE + 0.22,
                    y0 - 0.66 - j * 0.35,
                    size=0.19,
                    color=INK,
                )
            )
    core = scene.geometry.circle(0.85).fill(BRICK).no_stroke().move_to(-0.95, 0.05)
    core_t = t(
        scene,
        "Alba",
        -0.95,
        0.05,
        font="Aleo",
        size=0.4,
        weight=700,
        color="#FFFFFF",
        anchor=Anchor.CENTER,
    )
    arrows = [
        link(scene, (-2.4, 1.3), (-1.65, 0.45), color=MUTED),
        link(scene, (-2.4, -1.2), (-1.65, -0.35), color=MUTED),
        link(scene, (-0.08, 0.05), (0.9, 0.05), color=MUTED),
    ]
    outputs = [
        "Resumen del proyecto y parámetros",
        "Densidad provista vs. requerida",
        "Esfuerzo axial por muro y nivel",
        "Fisuración y resistencia global",
        "Derivas: tabla y gráfico por dirección",
        "Fecha, combinaciones y diagnósticos",
    ]
    out_card = panel(scene, 1.05, 2.4, 6.25, 4.5, fill=CARD, anchor=Anchor.TOP_LEFT)
    out_band = panel(
        scene,
        1.05,
        2.4,
        6.25,
        0.48,
        fill=PAPER_DEEP,
        border=None,
        anchor=Anchor.TOP_LEFT,
        radius=0.1,
    )
    out_title = t(
        scene,
        "Salidas · interfaz y reporte PDF",
        1.27,
        2.16,
        size=0.2,
        weight=900,
        color=INK,
        anchor=Anchor.LEFT,
    )
    out_rows = [
        t(scene, f"{i + 1:02d}  {row}", 1.27, 1.7 - i * 0.55, size=0.21, color=INK)
        for i, row in enumerate(outputs)
    ]
    scene.play(stagger(*[x.animate.fade_in().duration(0.25) for x in items], each=0.03))
    scene.play(
        stagger(
            arrows[0].animate.create().duration(0.3),
            arrows[1].animate.create().duration(0.3),
            core.animate.grow_from_center().duration(0.4),
            core_t.animate.fade_in().duration(0.3),
            arrows[2].animate.create().duration(0.3),
            each=0.12,
        )
    )
    scene.play(
        stagger(
            out_card.animate.fade_in().duration(0.3),
            out_band.animate.fade_in().duration(0.3),
            out_title.animate.fade_in().duration(0.3),
            stagger(
                *[
                    r.animate.fade_in_from(Direction.LEFT, 0.06).duration(0.25)
                    for r in out_rows
                ],
                each=0.06,
            ),
            each=0.1,
        )
    )
    scene.stop("entradas-salidas")

    record_label = label(
        scene, "Un registro trazable del caso", LEFT_EDGE, -2.28, color=MUTED, size=0.13
    )
    demand, capacity = SHEAR_DEMAND["X"]["MCT"][0], SHEAR_CAPACITY["X"]["MCT"][0]
    parts = [
        ("MCT", BRICK_DEEP, BRICK_SOFT),
        ("Piso 1", INK, PAPER_DEEP),
        ("X-X", INK, PAPER_DEEP),
        ("Resistencia global", INK, PAPER_DEEP),
        (f"$V_E$ = {demand:.3f}", INK, PAPER_DEEP),
        (f"$sum V_m$ = {capacity:.3f} tonf", INK, PAPER_DEEP),
    ]
    chips: list[Drawable] = []
    x = LEFT_EDGE
    for text, color, bg in parts:
        w_, _ = scene.text.measure(text, size=0.17, font=MONO)
        chips.append(
            pill(
                scene,
                text,
                x,
                -2.75,
                size=0.17,
                color=color,
                background=bg,
                anchor=Anchor.LEFT,
            )
        )
        x += w_ + 0.5
    chip = status(
        scene, capacity >= demand, x - 0.05, -2.75, anchor=Anchor.LEFT, size=0.17
    )
    scene.play(
        [
            record_label.animate.fade_in().duration(0.3),
            stagger(
                *[
                    c.animate.fade_in_from(Direction.UP, 0.08).duration(0.3)
                    for c in [*chips, chip]
                ],
                each=0.1,
            ),
        ]
    )
    takeaway(
        scene,
        "Del reporte se puede volver al modelo, al piso y a la dirección de cada valor",
        y=-3.3,
    )
    source(
        scene,
        "Tesis · cap. 6, Especificación de entradas y salidas · registro: cap. 8, tb:cortss_comp y tb:resco_comp",
    )
    scene.stop("trazabilidad")


SECTION = Section(
    "marco",
    [
        SectionStep(
            name="Marco · qué se automatiza",
            build=scope,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Criterios de proceso clave (cap. 6): se repite, muchos datos con la misma "
                "estructura, expuesto a transcripción, criterio normativo explícito, produce "
                "información para la revisión. Cuatro procesos: extracción, verificación, evaluación "
                "con retroalimentación y reportes. El marco no genera la estructuración ni modifica "
                "la distribución: esas decisiones siguen en el ingeniero."
            ),
        ),
        SectionStep(
            name="Marco · flujo general",
            build=general_flow,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. fig:flujo_marco. Antes de verificar se valida: una etiqueta, combinación o "
                "parámetro faltante detiene el módulo con un diagnóstico, y eso no es un "
                "incumplimiento normativo. Luego se procesa por muro, piso y dirección, se ejecutan "
                "los módulos y se consolidan resultados. Si el ingeniero modifica el modelo, se vuelve "
                "a analizar y a importar; si no, se genera el reporte."
            ),
        ),
        SectionStep(
            name="Marco · módulo de densidad",
            build=density_module,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.25 min. fig:flujo_densidad como ejemplo de módulo: entradas, validación, "
                "clasificación, aporte efectivo (concreto con Ec/Em), suma, comparación y salida. "
                "A la derecha, los valores del caso en cada paso. Los otros módulos (axial, "
                "fisuración y corte, derivas) siguen la misma estructura con sus diagramas del cap. 6."
            ),
        ),
        SectionStep(
            name="Marco · entradas, salidas y trazabilidad",
            build=traceability,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Entradas separadas: lo que se lee del modelo por API y lo que declara el "
                "usuario. Salidas: interfaz y PDF de la misma iteración. El registro de ejemplo es "
                "la resistencia global del piso 1 en X-X del modelo MCT: V_E = 149.805 tonf y "
                "ΣV_m = 203.032 tonf. Es un agregado de piso, no un Pier individual."
            ),
        ),
    ],
)
