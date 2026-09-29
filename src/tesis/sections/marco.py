"""Bloque 5 · Marco de trabajo: qué se automatiza, flujo general, módulos y trazabilidad."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Easing,
    EasingCurve,
    Scene,
    Section,
    SectionStep,
    Transition,
    sequence,
    stagger,
)

from tesis.building import density, wall_area_sum
from tesis.components import (
    arrow_gutter,
    chip,
    column_list,
    enter,
    header,
    note,
    page,
    panel,
    pill,
    role_column,
    source,
)
from tesis.components import takeaway as takeaway_box
from tesis.data.thesis import DENSITY_MIN, SHEAR_CAPACITY, SHEAR_DEMAND
from tesis.diagram import decision, io, link, process, terminal
from tesis.kit import label, t
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    DISPLAY,
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
        "Se automatiza lo repetitivo; decide el ingeniero",
    )
    L = scene.layout
    criteria = L.column(
        note(scene, text="Un proceso es clave si…"),
        # Los criterios completan el rótulo, en gris para no competir con la tabla.
        L.box(
            "se repite en cada iteración, maneja muchos datos iguales, expone a errores "
            "de transcripción, aplica un criterio normativo explícito y alimenta la "
            "revisión del ingeniero.",
            font_size="28px",
            color=INK_SOFT,
            width="90%",
        ),
        gap="14px",
        width="fill",
    )
    engineer = role_column(
        scene,
        title="Ingeniero estructural",
        color=STEEL,
        rows=[
            ("Estructura", "define la distribución de muros"),
            ("Modela y analiza", "construye el modelo en ETABS"),
            ("Interpreta", "lee diagnósticos y resultados"),
            ("Decide", "modifica muros, espesores o materiales"),
        ],
    )
    alba = role_column(
        scene,
        title="Marco de trabajo · Alba",
        color=BRICK,
        rows=[
            ("Extracción", "lee y valida datos del modelo por API"),
            ("Verificación", "ejecuta los módulos E.070 y E.030"),
            ("Retroalimentación", "señala muro, piso, dirección y valores"),
            ("Reporte", "documenta la iteración en PDF"),
        ],
    )
    # Estructura → Extracción y Retroalimentación → Interpreta.
    gutter = arrow_gutter(
        scene, slots=[("modelo", True), None, ("diagnóstico", False), None]
    )
    table = L.row(engineer, gutter, alba, gap="24px", width="fill")
    closing = takeaway_box(
        scene,
        text="El marco no genera la estructuración ni modifica el modelo: asiste la evaluación",
    )
    page(scene, body=[criteria, table, closing], gap="44px", top="200px")
    scene.play(enter(criteria))
    scene.stop("criterios-procesos-clave")

    scene.play(enter(engineer, each=0.05, duration=0.3))
    scene.play(enter(alba, each=0.05, duration=0.3))
    scene.play(enter(gutter, each=0.15, duration=0.4))
    scene.play(enter(closing))
    source(
        scene,
        "Tesis · §6.1 Procesos clave para la automatización, p. 98; §6.1.3 Evaluación de cumplimiento, p. 100",
    )
    scene.stop("reparto")


def general_flow(scene: Scene) -> None:
    header(scene, KICKER, "El flujo separa datos inconsistentes de incumplimientos")
    y1, y2, y3 = 1.3, -1.05, -2.72
    loop_zone = panel(
        scene,
        -2.95,
        2.25,
        9.7,
        3.95,
        fill=PAPER_DEEP,
        border=None,
        anchor=Anchor.TOP_LEFT,
    )
    loop_tag = label(
        scene, "Se repite en cada iteración", -2.7, 2.08, color=MUTED, size=0.13
    )
    # Pulso terracota que da una vuelta al lazo por los centros de las cajas. Se
    # crea antes que ellas para quedar detrás: solo se ve sobre las flechas.
    lap = (
        scene.geometry.polygon([(-1.35, y1), (4.95, y1), (4.95, y2), (-1.35, y2)])
        .no_fill()
        .stroke(BRICK, 0.11)
        .trim(0.0, 0.0)
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
            links[0].animate.grow_arrow().duration(0.2),
            p1.animate.fade_in().duration(0.3),
            links[1].animate.grow_arrow().duration(0.2),
            r2.animate.fade_in().duration(0.3),
            links[2].animate.grow_arrow().duration(0.2),
            r3.animate.fade_in().duration(0.3),
            links[3].animate.grow_arrow().duration(0.2),
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
            links[4].animate.grow_arrow().duration(0.25),
            p5.animate.fade_in().duration(0.3),
            links[5].animate.grow_arrow().duration(0.2),
            d6.animate.fade_in().duration(0.3),
            stagger(
                yes.animate.grow_arrow().duration(0.25),
                yes_t.animate.fade_in().duration(0.2),
                r9.animate.fade_in().duration(0.3),
                back.animate.grow_arrow().duration(0.3),
                each=0.12,
            ),
            stagger(
                no.animate.grow_arrow().duration(0.25),
                no_t.animate.fade_in().duration(0.2),
                p7.animate.fade_in().duration(0.3),
                end.animate.grow_arrow().duration(0.2),
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
    # El pulso recorre el lazo y se recoge donde empezó.
    tail = 0.1
    scene.play(
        sequence(
            lap.animate.trim(end=tail)
            .duration(0.45)
            .easing(Easing.ease_in(EasingCurve.CUBIC)),
            lap.animate.trim(offset=1 - tail).duration(1.9).easing(Easing.LINEAR),
            lap.animate.trim(start=tail)
            .duration(0.45)
            .easing(Easing.ease_out(EasingCurve.CUBIC)),
        )
    )
    source(
        scene,
        "Tesis · Figura 42, p. 103; §6.1.3 Evaluación de cumplimiento y retroalimentación al usuario, p. 100",
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
        x = tab_items[-1].bounds().right + 0.18
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
            *[a.animate.grow_arrow().duration(0.3) for a in arrows],
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
        "Tesis · Figura 43, p. 105 (E.070, art. 19.2) · valores: Tabla 22, p. 57",
    )
    scene.stop("modulo-recorrido")


def traceability(scene: Scene) -> None:
    header(scene, KICKER, "Cada resultado conserva su origen: modelo, piso y dirección")
    L = scene.layout
    api = column_list(
        scene,
        title="Desde ETABS · API",
        color=BRICK,
        size="22px",
        gap="12px",
        items=[
            "Geometría de muros y niveles",
            "Materiales y secciones",
            "Resultados: P, V, M y desplazamientos",
            "Etiquetas Pier, casos y combinaciones",
        ],
    )
    declared = column_list(
        scene,
        title="Declarado por el usuario",
        color=STEEL,
        size="22px",
        gap="12px",
        items=[
            "Datos del proyecto",
            "Z, U, S y factores de irregularidad",
            "f'm, f'c · N y A_p",
            "Nombres de combinaciones a usar",
        ],
    )
    inputs = L.column(api, declared, gap="24px", width="fill").item(grow=1)
    core = L.box(
        "Alba",
        font=DISPLAY,
        font_size="48px",
        weight=700,
        color="#FFFFFF",
        background=BRICK,
        width="190px",
        height="190px",
        radius="full",
        align="center",
        justify="center",
    ).item(shrink=0)
    arrow_in = scene.geometry.arrow(0, 0, 0.7, 0).fill(MUTED).no_stroke()
    arrow_out = scene.geometry.arrow(0, 0, 0.7, 0).fill(MUTED).no_stroke()
    hub = L.row(arrow_in, core, arrow_out, gap="14px", align="center").item(shrink=0)
    outputs = column_list(
        scene,
        title="Salidas · interfaz y reporte PDF",
        color=INK,
        size="22px",
        gap="14px",
        items=[
            f"{i + 1:02d}  {row}"
            for i, row in enumerate(
                [
                    "Resumen del proyecto y parámetros",
                    "Densidad provista vs. requerida",
                    "Esfuerzo axial por muro y nivel",
                    "Fisuración y resistencia global",
                    "Derivas: tabla y gráfico por dirección",
                    "Fecha, combinaciones y diagnósticos",
                ]
            )
        ],
    )
    flow = L.row(inputs, hub, outputs, gap="36px", align="center", width="fill").item(
        grow=1
    )

    demand, capacity = SHEAR_DEMAND["X"]["MCT"][0], SHEAR_CAPACITY["X"]["MCT"][0]
    ok = capacity >= demand
    record = L.column(
        note(scene, text="Un registro trazable del caso"),
        L.row(
            chip(scene, text="MCT", color=BRICK_DEEP, background=BRICK_SOFT),
            chip(scene, text="Piso 1"),
            chip(scene, text="X-X"),
            chip(scene, text="Resistencia global"),
            chip(scene, text=f"V_E = {demand:.3f}"),
            chip(scene, text=f"ΣV_m = {capacity:.3f} tonf"),
            L.box(
                "✓ Cumple" if ok else "✕ No cumple",
                font_size="26px",
                weight=900,
                color=PASS if ok else FAIL,
            ),
            gap="14px",
            align="center",
        ),
        gap="14px",
        width="fill",
    )
    closing = takeaway_box(
        scene,
        text="Del reporte se puede volver al modelo, al piso y a la dirección de cada valor",
    )
    page(scene, body=[flow, record, closing], gap="30px", top="180px")
    scene.play(enter(api, each=0.04, duration=0.25))
    scene.play(enter(declared, each=0.04, duration=0.25))
    scene.play(enter(hub, each=0.15, duration=0.4))
    scene.play(enter(outputs, each=0.06, duration=0.25))
    scene.stop("entradas-salidas")

    scene.play(enter(record, each=0.06, duration=0.3))
    scene.play(enter(closing))
    source(
        scene,
        "Tesis · §6.3 Especificación de entradas y salidas, p. 111 · registro: Tablas 53 y 54, pp. 133–134",
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
                "1 min. Figura 42 (p. 103). Antes de verificar se valida: una etiqueta, combinación o "
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
                "1.25 min. Figura 43 (p. 105) como ejemplo de módulo: entradas, validación, "
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
