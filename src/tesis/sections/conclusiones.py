"""Bloque 8 · Conclusiones: objetivos, hallazgos, alcance y cierre."""

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    stagger,
)

from tesis.app import thesis_image
from tesis.building import draw_plan, grow_walls
from tesis.components import (
    enter,
    finding_card,
    header,
    numbered_row,
    page,
    source,
    takeaway,
)
from tesis.data.thesis import (
    DRIFTS,
    relative,
)
from tesis.kit import LEFT_EDGE, t
from tesis.theme import (
    BRICK,
    BRICK_SOFT,
    CARD,
    CONCRETE,
    CONCRETE_SOFT,
    DISPLAY,
    GOLD,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PAPER_DEEP,
    RULE,
    STEEL,
)

KICKER = "08 · Conclusiones"

OBJECTIVES = [
    (
        "Identificar",
        "La extracción de resultados, la clasificación de muros y la transcripción\n"
        "a plantillas son actividades críticas y automatizables.",
    ),
    (
        "Desarrollar",
        "Se especificaron procesos, diagramas de flujo y trazabilidad para densidad,\n"
        "esfuerzo axial, fisuración, resistencia al corte y derivas.",
    ),
    (
        "Aplicar",
        "Alba se conecta con ETABS mediante su API, ejecuta las verificaciones y\n"
        "entrega diagnósticos visuales y reportes técnicos automáticos.",
    ),
    (
        "Evaluar",
        "En el caso, el modelo completo permitió extraer y organizar fuerzas y\n"
        "deformaciones; la idealización cambia resultados y diagnósticos.",
    ),
]


def objectives(scene: Scene) -> None:
    header(scene, KICKER, "Los cuatro objetivos se cumplieron en el caso de estudio")
    rows = [
        numbered_row(scene, number=i + 1, name=verb, text=text.replace("\n", " "))
        for i, (verb, text) in enumerate(OBJECTIVES)
    ]
    hypothesis = takeaway(
        scene,
        tag="Hipótesis",
        text="El marco integrado a ETABS por API sistematiza la extracción, el "
        "procesamiento, la verificación y la documentación.",
        display=False,
    )
    page(scene, body=[*rows, hypothesis], top="220px", gap="24px")
    for row in rows:
        scene.play(enter(row))
    scene.play(enter(hypothesis, direction=Direction.UP, each=0.15))
    source(
        scene,
        "Tesis · Conclusiones, p. 135 · se sostiene para el caso estudiado (muestra no probabilística)",
    )
    scene.stop("objetivos-cumplidos")


def _mesh_wall(scene: Scene) -> Drawable:
    """Muro confinado como área con malla; al lado, apagada, la barra que lo idealiza."""
    g = scene.geometry
    w, h, c = 1.45, 1.35, 0.13
    parts: list[Drawable] = [g.rect(w, h).fill(BRICK_SOFT).no_stroke()]
    parts += [
        g.line(-w / 2 + w * i / 6, -h / 2, -w / 2 + w * i / 6, h / 2).stroke(
            BRICK, 0.012
        )
        for i in range(1, 6)
    ]
    parts += [
        g.line(-w / 2, -h / 2 + h * j / 5, w / 2, -h / 2 + h * j / 5).stroke(
            BRICK, 0.012
        )
        for j in range(1, 5)
    ]
    parts += [
        g.rect(c, h + c)
        .fill(CONCRETE_SOFT)
        .stroke(CONCRETE, 0.014)
        .move_to(side * (w + c) / 2, c / 2)
        for side in (-1, 1)
    ]
    parts.append(
        g.rect(w, c).fill(CONCRETE_SOFT).stroke(CONCRETE, 0.014).move_to(0, (h + c) / 2)
    )
    bar = w / 2 + c + 0.5
    parts.append(g.line(bar, -h / 2, bar, h / 2 + c / 2).stroke(RULE, 0.05))
    parts.append(
        g.line(bar - 0.28, h / 2 + c / 2, bar + 0.28, h / 2 + c / 2).stroke(RULE, 0.09)
    )
    return g.group(parts)


def _directional(scene: Scene) -> Drawable:
    """Planta con el sismo en X al 100 % y en Y al 30 %."""
    g = scene.geometry
    w, h = 2.3, 1.25
    origin = (-0.55, -0.2)
    x_tip, y_tip = origin[0] + 1.45, origin[1] + 0.44
    return g.group(
        [
            g.rect(w, h).fill(PAPER_DEEP).stroke(RULE, 0.014),
            g.arrow(*origin, x_tip, origin[1], head_length=0.16, head_width=0.16)
            .fill(STEEL)
            .no_stroke(),
            g.arrow(*origin, origin[0], y_tip, head_length=0.14, head_width=0.14)
            .fill(STEEL)
            .no_stroke()
            .opacity(0.55),
            t(
                scene,
                "100 %",
                x_tip,
                origin[1] + 0.12,
                font=MONO,
                size=0.17,
                color=STEEL,
                anchor=Anchor.BOTTOM_RIGHT,
            ),
            t(
                scene,
                "30 %",
                origin[0] + 0.1,
                y_tip,
                font=MONO,
                size=0.17,
                color=STEEL,
                anchor=Anchor.LEFT,
            ),
        ]
    )


def _drift_bars(scene: Scene, share: float) -> Drawable:
    """Deriva con la sección mínima actual frente a columnas de 0.25 m."""
    g = scene.geometry
    tall, width, gap = 1.45, 0.5, 0.4
    short = tall * share
    base = -0.65
    left, right = -(width + gap) / 2, (width + gap) / 2
    return g.group(
        [
            g.rect(width, tall)
            .fill(CONCRETE_SOFT)
            .no_stroke()
            .move_to(left, base + tall / 2),
            g.rect(width, short)
            .fill(STEEL)
            .no_stroke()
            .move_to(right, base + short / 2),
            g.dashed_line(
                left - width / 2,
                base + tall,
                right + width / 2,
                base + tall,
                dash_length=0.06,
                gap_length=0.05,
            ).stroke(MUTED, 0.012),
            g.arrow(
                right,
                base + tall - 0.02,
                right,
                base + short + 0.06,
                head_length=0.12,
                head_width=0.13,
            )
            .fill(STEEL)
            .no_stroke(),
            g.line(left - width, base, right + width, base).stroke(INK_SOFT, 0.014),
            t(
                scene,
                "E.070",
                left,
                base - 0.1,
                size=0.15,
                color=MUTED,
                anchor=Anchor.TOP,
            ),
            t(
                scene,
                "0.25 m",
                right,
                base - 0.1,
                size=0.15,
                color=STEEL,
                anchor=Anchor.TOP,
            ),
        ]
    )


def findings(scene: Scene) -> None:
    header(scene, KICKER, "Lo que muestra el caso: idealización, norma y criterio")
    # Solo lo escrito en las Conclusiones; el 22.61 % sale de la Tabla 52.
    norm_gap = relative(DRIFTS["X"]["MSTA"][2], DRIFTS["X"]["MSTO"][2])
    tiles = [
        (_mesh_wall(scene), "MCT", "menos conservador\ny más detallado", BRICK),
        (_directional(scene), "E.030", "más exigente\nque la de 2003", STEEL),
        (
            _drift_bars(scene, 1 - norm_gap / 100),
            f"−{norm_gap:.2f} %",
            "deriva con columnas\nde 0.25 m",
            STEEL,
        ),
        (
            scene.media.image(
                thesis_image("cap7/ui_alba.png"), width=2.8, height=2.0, fit="contain"
            ),
            "Alba",
            "apoyo de código\nlibre",
            BRICK,
        ),
    ]
    cards = [
        finding_card(scene, picture=picture, value=value, text=text, color=color)
        for picture, value, text, color in tiles
    ]
    quote = takeaway(
        scene, text="El criterio del ingeniero sigue siendo el factor determinante"
    )
    page(
        scene,
        body=[
            scene.layout.row(
                *cards, gap="28px", align="stretch", width="fill", height="fill"
            ),
            quote,
        ],
        gap="36px",
    )
    for card in cards:
        scene.play(
            enter(card, direction=Direction.UP, distance=0.08, duration=0.3, each=0.08)
        )
    scene.play(enter(quote, direction=Direction.UP, duration=0.5, each=0.1))
    source(scene, "Tesis · Conclusiones, pp. 135–136 · Tabla 52, p. 131")
    scene.stop("hallazgos")


# Las siete recomendaciones (p. 137), agrupadas por a quién le toca continuar.
RECOMMENDATIONS = [
    ("Modelamiento", STEEL, "Modelos completos con elementos área"),
    ("Modelamiento", STEEL, "Fuerzas en uniones T y L"),
    ("Modelamiento", STEEL, "Análisis no lineal con macromodelos"),
    ("Alba", BRICK, "Diseño de confinamientos en Alba"),
    ("Alba", BRICK, "Código libre al día con el RNE"),
    ("Nuevos usos", GOLD, "CNN para irregularidades en planta"),
    ("Nuevos usos", GOLD, "Alba como recurso docente"),
]


def outlook(scene: Scene) -> None:
    header(scene, KICKER, "La investigación deja siete líneas para continuar")
    L = scene.layout
    tiles = [
        L.column(
            L.box(width="fill", height="5px", background=color),
            L.box(f"{i + 1}", font=DISPLAY, font_size="76px", weight=700, color=color),
            L.box(text, font_size="29px", weight=700, color=INK).item(grow=1),
            L.box(
                group.upper(),
                font_size="16px",
                weight=900,
                color=color,
                letter_spacing=0.03,
            ),
            gap="16px",
            padding=("28px", "30px"),
            background=CARD,
            border=RULE,
            border_width="2px",
            width="fill",
            height="fill",
        ).item(grow=1)
        for i, (group, color, text) in enumerate(RECOMMENDATIONS)
    ]
    rows = [
        L.row(*tiles[:4], gap="28px", align="stretch", width="fill").item(grow=1),
        L.row(*tiles[4:], gap="28px", align="stretch", width="fill").item(grow=1),
    ]
    page(scene, body=rows, gap="28px")
    scene.play(
        stagger(
            *[
                enter(
                    tile, direction=Direction.UP, distance=0.08, duration=0.3, each=0.05
                )
                for tile in tiles
            ],
            each=0.12,
        )
    )
    source(scene, "Tesis · Recomendaciones, p. 137")
    scene.stop("recomendaciones")


def closing(scene: Scene) -> None:
    plan = draw_plan(scene, (3.9, 0.0), 6.3, drawn_thickness=0.075)
    thanks = t(
        scene, "Gracias", LEFT_EDGE, 1.7, font=DISPLAY, size=1.2, weight=700, color=INK
    )
    prompt = t(
        scene,
        "Quedamos atentos a las preguntas\ny observaciones del jurado.",
        LEFT_EDGE,
        -0.25,
        size=0.3,
        color=INK_SOFT,
    )
    authors = t(
        scene,
        "Paolo Cesar Guillen Lupo  ·  Pamela Lucyla Banda Alarta",
        LEFT_EDGE,
        -1.65,
        size=0.22,
        weight=700,
        color=INK,
    )
    advisor = t(
        scene,
        "Asesor: Mgtr. David Miguel Chalco Pari",
        LEFT_EDGE,
        -2.05,
        size=0.2,
        color=MUTED,
    )
    scene.play(
        stagger(
            thanks.animate.fade_in_from(Direction.UP, 0.12).duration(0.7),
            prompt.animate.fade_in().duration(0.5),
            authors.animate.fade_in().duration(0.4),
            advisor.animate.fade_in().duration(0.4),
            each=0.15,
        )
    )
    scene.play(
        stagger(
            stagger(*[g.animate.create().duration(0.5) for g in plan.grid], each=0.03),
            stagger(
                *[b.animate.fade_in().duration(0.25) for b in plan.bubbles], each=0.02
            ),
            plan.slab.animate.fade_in().duration(0.5),
            plan.void.animate.fade_in().duration(0.3),
            grow_walls(plan.all_walls, total=0.9, duration=0.35),
            each=0.2,
        )
    )
    scene.stop("preguntas")


SECTION = Section(
    "conclusiones",
    [
        SectionStep(
            name="Conclusiones · objetivos",
            build=objectives,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Retomar cada objetivo específico con su conclusión (Conclusiones, p. 135). La hipótesis se "
                "sostiene para el caso: el marco integra de forma reproducible extracción, "
                "procesamiento, verificación y documentación. No se afirma una reducción medida de "
                "tiempo o de errores: no se midió."
            ),
        ),
        SectionStep(
            name="Conclusiones · hallazgos",
            build=findings,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Lo que dicen las Conclusiones (pp. 135–136). (1) El MCT reduce "
                "conservadurismo innecesario y da más detalle: las áreas reparten mejor la carga de "
                "losa y cuentan el aporte de los muros ortogonales. (2) La E.030 vigente es más "
                "rigurosa que la de 2003: combinación direccional 100 % + 30 % y factores sísmicos "
                "mayores. (3) Las columnas de 0.25 m de la propuesta E.070 reducen las derivas hasta "
                "22.61 % y neutralizan esa exigencia. (4) Alba es una herramienta de apoyo de código "
                "libre. Cerrar con el criterio del usuario como factor determinante."
            ),
        ),
        SectionStep(
            name="Conclusiones · recomendaciones",
            build=outlook,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Recomendaciones (p. 137): modelos completos con elementos área, fuerzas en "
                "intersecciones T y L (un confinamiento solo puede tener una etiqueta Pier), diseño "
                "de confinamientos en Alba, mantenimiento del código libre con el RNE, análisis no "
                "lineal con macromodelos, CNN para irregularidades en planta y uso educativo."
            ),
        ),
        SectionStep(
            name="Cierre",
            build=closing,
            transition=Transition.cross_fade(0.6),
            notes="Agradecer y abrir la ronda de preguntas. Mantener esta diapositiva durante la discusión.",
        ),
    ],
)
