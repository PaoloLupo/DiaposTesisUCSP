"""Problemática: contexto nacional → distribución en planta → trabajo manual.

Base: TesisUCSP/01_intro.typ (Problemática y Justificación) y
TesisUCSP/05_analisismanual.typ (introducción del proceso convencional).
Las plantas son esquemas conceptuales, no resultados de análisis estructural.
"""

from math import hypot

from gaanim import (
    BLACK,
    ORANGE,
    Anchor,
    Axis,
    ChartSpec,
    Color,
    Direction,
    Field,
    Scale,
    Scene,
    Transition,
    stagger,
)

from tesis.data.materiales_inei import CHART_DATA, MATERIALES, PORCENTAJES, SOURCE_LABEL
from tesis.section_index import SectionIndex
from tesis.theme import ACCENT

INK_MUTED = "#626878"
RULE = "#C9CDDA"
WARM = "#B7791F"


def _text(
    scene: Scene,
    content: str,
    x: float,
    y: float,
    *,
    size: float = 0.28,
    color: Color = BLACK,
    center: bool = False,
):
    return (
        scene.text(
            content,
            size=size,
            text_align="center" if center else "left",
            line_spacing=1.18,
        )
        .fill(color)
        .move_to(x, y, Anchor.CENTER if center else Anchor.TOP_LEFT)
    )


def _header(scene: Scene, step: str, headline: str):
    title = _text(scene, headline, -7.2, 3.35, size=0.51)
    rule = scene.geometry.line(-7.2, 2.6, 7.2, 2.6).stroke(ACCENT, 0.035)
    scene.play(
        [
            title.animate.write(),
            rule.animate.create(),
        ],
        duration=0.8,
    )


def _arrow(scene: Scene, x1: float, y1: float, x2: float, y2: float, color: Color):
    """Arrow dimensions in scene units, including a restrained 0.18-unit head."""
    length = hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    head = min(0.18, length * 0.3)
    points = [
        (0, 0.018),
        (length - head, 0.018),
        (length - head, 0.075),
        (length, 0),
        (length - head, -0.075),
        (length - head, -0.018),
        (0, -0.018),
    ]
    return (
        scene.geometry.polygon(
            [
                (x1 + along * ux - across * uy, y1 + along * uy + across * ux)
                for along, across in points
            ]
        )
        .fill(color)
        .no_stroke()
    )


def materials(scene: Scene, section_index: SectionIndex | None = None):
    _ = scene.segment(
        "Problemática",
        Transition.cross_fade(0.55),
        notes=(
            "Base: tesis, capítulo 1, Problemática. Introducir la presencia de la "
            "albañilería y el contexto sísmico del Perú. El gráfico actualiza la "
            "referencia INEI 2017 de la tesis con el tabulado de viviendas INEI 2025. "
            "El porcentaje mide material predominante en paredes, no acredita "
            "confinamiento ni desempeño sísmico. El relleno del mapa es un "
            "indicador ilustrativo nacional, no una distribución geográfica."
        ),
    )
    if section_index is not None:
        section_index.advance(1, 3)
    _header(
        scene, "01  CONTEXTO NACIONAL", "*Un material extendido* en un país sísmico"
    )

    scene.camera.save("contexto-general")
    # SVG stroke widths are local to the asset and scale with its geometry.
    outline = (
        scene.media.svg("peru.svg")
        .no_fill()
        .stroke(INK_MUTED, 2.0)
        .scale_to(0.0054)
        .move_to(0, -0.2)
    )
    amount = scene.viz.parameter(0.0)
    percentage = (
        scene.viz.readout(amount, format=".1f", suffix="%", font_size=0.8)
        .fill(BLACK)
        .move_to(-0.7, -0.95)
    )
    fill = scene.geometry.fill_level(
        outline,
        ORANGE,
        0.0,
        direction="up",
        keep_outline=False,
    ).z_index(-1)
    map_group = scene.geometry.group([outline, fill, percentage])
    caption = _text(
        scene,
        "Viviendas con paredes de\n*ladrillo o bloque de concreto*",
        0,
        -2.85,
        size=0.27,
        center=True,
    )
    scene.play(outline.animate.write(), duration=0.85)
    scene.play(
        [
            amount.animate.set(PORCENTAJES[0]),
            fill.animate.fill_level(PORCENTAJES[0] / 100),
            percentage.animate.fade_in(),
            caption.animate.fade_in(),
        ],
        duration=1.35,
    )
    scene.stop("material-predominante")

    # Explicit overview restoration prevents a map detail from cropping the chart.
    scene.play(
        [
            map_group.animate.shift_by(-4.65, 0),
            caption.animate.shift_by(-4.65, 0),
            scene.camera.animate.restore("contexto-general"),
        ],
        duration=0.85,
    )
    colors = [
        ORANGE,
        "#B7791F",
        "#8B5E3C",
        "#A16207",
        "#64748B",
        "#D97706",
        "#78716C",
        "#94A3B8",
        "#475569",
    ]
    spec = (
        ChartSpec(CHART_DATA, key="id")
        .mark("bar", width=0.72, label_position="outside", label_offset=0.18)
        .encode(
            x="material",
            y="viviendas_porcentaje",
            label="rotulo",
            color=Field(
                "color_material", scale=Scale.category(MATERIALES).colors(colors)
            ),
        )
        .axes(x=Axis.category(MATERIALES), y=Axis.linear(0, 70).ticks(10))
    )
    chart = scene.viz.chart(spec).scale_to(0.68).move_to(2.65, -0.45)
    chart_title = _text(
        scene, "Material predominante en paredes", 2.65, 1.85, size=0.30, center=True
    )
    units = _text(scene, "Viviendas (%)", -1.5, 1.85, size=0.20, color=INK_MUTED)
    source = _text(
        scene,
        f"Fuente: {SOURCE_LABEL}",
        2.65,
        -3.25,
        size=0.19,
        color=INK_MUTED,
        center=True,
    )
    scope = _text(
        scene,
        "El material de la pared no identifica el sistema estructural.",
        0,
        -3.65,
        size=0.24,
        color=INK_MUTED,
        center=True,
    )
    scene.play(
        [
            chart.layer("axes").animate.create(),
            chart_title.animate.fade_in(),
            units.animate.fade_in(),
        ],
        duration=0.65,
    )
    scene.play(
        stagger(
            chart.layer("marks").animate.grow_from_center().duration(1.0),
            chart.layer("labels").animate.fade_in().duration(0.6),
            source.animate.fade_in().duration(0.4),
            each=0.35,
        )
    )
    scene.play(scope.animate.fade_in(), duration=0.45)
    scene.stop("materiales-listo")


def _wall_plan(scene):
    """A schematic, unscaled plan with separate wall families in X and Y."""
    cx, cy = -3.9, -0.25
    boundary = (
        scene.geometry.rect(4.7, 3.35).no_fill().stroke(RULE, 0.025).move_to(cx, cy)
    )
    horizontal = []
    vertical = []
    endpoints = set()
    for x, y, width in [
        (-1.55, 1.55, 1.4),
        (1.25, 1.55, 2.0),
        (-1.35, -1.55, 1.8),
        (1.575, -1.55, 1.35),
        (-1.25, 0.0, 2.0),
        (1.575, 0.0, 1.35),
    ]:
        horizontal.append(
            scene.geometry.rect(width, 0.13)
            .fill(ORANGE)
            .no_stroke()
            .move_to(cx + x, cy + y)
        )
        endpoints.update(
            (round(cx + x + offset, 4), round(cy + y, 4))
            for offset in (-width / 2, width / 2)
        )
    for x, y, height in [
        (-2.25, 0.775, 1.55),
        (-2.25, -1.075, 0.95),
        (2.25, 0.0, 3.1),
        (0.25, 0.9, 1.3),
        (0.25, -1.05, 1.0),
    ]:
        vertical.append(
            scene.geometry.rect(0.13, height)
            .fill(ACCENT)
            .no_stroke()
            .move_to(cx + x, cy + y)
        )
        endpoints.update(
            (round(cx + x, 4), round(cy + y + offset, 4))
            for offset in (-height / 2, height / 2)
        )
    x_arrow = _arrow(scene, cx - 1.2, -2.45, cx + 1.2, -2.45, ORANGE)
    y_arrow = _arrow(scene, -6.75, -1.45, -6.75, 0.95, ACCENT)
    x_label = _text(scene, "X", cx + 1.5, -2.45, size=0.28, color=WARM, center=True)
    y_label = _text(scene, "Y", -6.75, 1.3, size=0.28, color=ACCENT, center=True)
    return (
        boundary,
        horizontal,
        vertical,
        [x_arrow, x_label],
        [y_arrow, y_label],
        sorted(endpoints),
    )


def _distribution(scene, section_index: SectionIndex | None = None):
    scene.segment(
        "Problemática · distribución",
        Transition.cross_fade(0.55),
        notes=(
            "Base: tesis, capítulo 1, Problemática y Justificación. En el "
            "contexto sísmico peruano, explicar la importancia de distribuir "
            "muros portantes en ambas direcciones y conectarlos con los elementos "
            "de confinamiento. La planta es un esquema conceptual sin escala; "
            "no representa el caso de estudio ni demuestra cumplimiento E.070. "
            "No confundir densidad suficiente con una verificación integral."
        ),
    )
    if section_index is not None:
        section_index.advance(2, 3)
    _header(scene, "02  EXIGENCIA ESTRUCTURAL", "La *distribución de muros* importa")
    boundary, horizontal, vertical, x_axis, y_axis, endpoints = _wall_plan(scene)
    plan_label = _text(
        scene,
        "DISTRIBUCIÓN EN PLANTA",
        -3.9,
        1.85,
        size=0.20,
        color=INK_MUTED,
        center=True,
    )
    caveat = _text(
        scene,
        "Esquema conceptual · sin escala",
        -3.9,
        -3.1,
        size=0.18,
        color=INK_MUTED,
        center=True,
    )
    first = _text(scene, "01", 0.35, 1.6, size=0.25, color=WARM)
    first_title = _text(scene, "*Muros en ambas direcciones*", 1.05, 1.65, size=0.33)
    first_body = _text(
        scene,
        "La densidad de muros se revisa\nen X y en Y.",
        1.05,
        1.0,
        size=0.28,
        color=INK_MUTED,
    )
    takeaway = _text(
        scene,
        "Cada cambio de distribución exige volver a verificar.",
        0,
        -3.6,
        size=0.30,
        color=ACCENT,
        center=True,
    )
    scene.play(
        [
            boundary.animate.create(),
            plan_label.animate.fade_in(),
            caveat.animate.fade_in(),
        ],
        duration=0.55,
    )
    scene.play(
        stagger(
            *[wall.animate.grow_from_center().duration(0.55) for wall in horizontal],
            each=0.07,
        )
    )
    scene.play(
        [item.animate.fade_in() for item in [*x_axis, first, first_title, first_body]],
        duration=0.6,
    )
    scene.play(
        stagger(
            *[wall.animate.grow_from_center().duration(0.55) for wall in vertical],
            each=0.07,
        )
    )
    scene.play([item.animate.fade_in() for item in y_axis], duration=0.4)
    scene.stop("muros-en-dos-direcciones")

    # Confinement markers on the conceptual plan; no force simulation.
    columns = []
    for x, y in endpoints:
        columns.append(
            scene.geometry.rect(0.18, 0.18).fill(BLACK).no_stroke().move_to(x, y)
        )
    scene.play(
        stagger(
            *[col.animate.grow_from_center().duration(0.4) for col in columns],
            each=0.045,
        )
    )
    second = _text(scene, "02", 0.35, -0.35, size=0.25, color=ACCENT)
    second_title = _text(scene, "*Conexión y confinamiento*", 1.05, -0.3, size=0.33)
    second_body = _text(
        scene,
        "Muros y elementos de confinamiento\ndeben trabajar en conjunto.",
        1.05,
        -0.95,
        size=0.28,
        color=INK_MUTED,
    )
    scene.play(
        [item.animate.fade_in() for item in [second, second_title, second_body]],
        duration=0.6,
    )
    scene.play(takeaway.animate.write(), duration=0.9)
    scene.stop("distribucion-y-confinamiento")


def _workflow_node(scene, x, number, title, body):
    outline = (
        scene.geometry.rounded_rect(3.8, 1.75, 0.08)
        .no_fill()
        .stroke(RULE, 0.025)
        .move_to(x, 0.65)
    )
    number_text = _text(scene, number, x, 1.85, size=0.23, color=ACCENT, center=True)
    heading = _text(scene, f"*{title}*", x, 0.95, size=0.32, center=True)
    detail = _text(scene, body, x, 0.3, size=0.24, color=INK_MUTED, center=True)
    return scene.geometry.group([outline, number_text, heading, detail])


def _manual_workflow(scene, section_index: SectionIndex | None = None):
    scene.segment(
        "Problemática · proceso manual",
        Transition.cross_fade(0.55),
        notes=(
            "Base: tesis, capítulo 1, Problemática (últimos dos párrafos) y "
            "capítulo 5, introducción del análisis manual. Presentar el flujo "
            "convencional estudiado: modelo y resultados en ETABS, extracción "
            "y procesamiento mediante hojas de cálculo, verificaciones E.070. "
            "La tesis identifica variabilidad de criterios, errores de "
            "transcripción y verificaciones omitidas como riesgos, no como "
            "frecuencias medidas. El retorno representa la revisión tras "
            "modificar la distribución. Cerrar con el problema de investigación, "
            "sin anticipar resultados de automatización ni sustituir al ingeniero."
        ),
    )
    if section_index is not None:
        section_index.advance(3, 3)
    _header(
        scene, "03  PROCESO CONVENCIONAL", "La verificación depende de *pasos manuales*"
    )
    nodes = [
        _workflow_node(
            scene,
            -5,
            "01",
            "Modelo en ETABS",
            "Geometría y resultados\ndel análisis estructural",
        ),
        _workflow_node(
            scene, 0, "02", "Hojas de cálculo", "Extraer, ordenar\ny procesar datos"
        ),
        _workflow_node(
            scene,
            5,
            "03",
            "Verificación E.070",
            "Revisar requisitos\nde la distribución",
        ),
    ]
    arrows = [_arrow(scene, x, 0.65, x + 1.05, 0.65, ORANGE) for x in (-3.05, 1.95)]
    transfer = [
        _text(scene, "trasladar", x, 1.13, size=0.18, color=WARM, center=True)
        for x in (-2.5, 2.5)
    ]
    scene.play(
        nodes[0].animate.fade_in_from(Direction.DOWN, distance=0.15), duration=0.55
    )
    for index in range(2):
        scene.play(
            [arrows[index].animate.create(), transfer[index].animate.fade_in()],
            duration=0.45,
        )
        scene.play(
            nodes[index + 1].animate.fade_in_from(Direction.DOWN, distance=0.15),
            duration=0.55,
        )
    scene.stop("flujo-manual")

    risks = [
        _text(scene, text, x, -0.95, size=0.25, color=WARM, center=True)
        for x, text in [
            (-5, "Criterios de modelado"),
            (0, "Transcripción de datos"),
            (5, "Verificaciones omitidas"),
        ]
    ]
    scene.play(
        stagger(*[risk.animate.fade_in().duration(0.45) for risk in risks], each=0.2)
    )
    return_path = (
        scene.geometry.polyline(
            [(5, -1.45), (5, -2.0), (-7.1, -2.0), (-7.1, 0.65), (-6.98, 0.65)]
        )
        .no_fill()
        .stroke(ACCENT, 0.035)
    )
    arrow_tip = _arrow(scene, -7.1, 0.65, -6.91, 0.65, ACCENT)
    repeat = _text(
        scene,
        "Modificar la distribución → repetir la revisión",
        0,
        -2.35,
        size=0.24,
        color=ACCENT,
        center=True,
    )
    scene.play([return_path.animate.create(), repeat.animate.fade_in()], duration=0.8)
    scene.play(arrow_tip.animate.create(), duration=0.35)
    scene.stop("iteracion-y-riesgos")

    question = _text(
        scene,
        "¿Cómo *sistematizar* la verificación de la distribución de muros?",
        0,
        -3.45,
        size=0.34,
        center=True,
    )
    scene.play(question.animate.write(), duration=1.25)
    scene.stop("pregunta-del-problema")


def build(scene: Scene, section_index: SectionIndex | None = None):
    materials(scene, section_index)
    _distribution(scene, section_index)
    _manual_workflow(scene, section_index)
