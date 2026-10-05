"""Bloque 5 · Marco de trabajo: qué se automatiza, flujo general, módulos y trazabilidad."""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from gaanim import (
    Anchor,
    Box,
    Composition,
    Direction,
    Drawable,
    Easing,
    EasingCurve,
    Scene,
    Section,
    SectionStep,
    Transition,
    parallel,
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
    source_block,
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


KEY_PROCESS = [
    "Se repite en cada iteración",
    "Muchos datos iguales",
    "Riesgo de transcripción",
    "Criterio normativo explícito",
    "Alimenta la revisión",
]
ROLE_ROW = "118px"


def scope(scene: Scene) -> None:
    header(scene, KICKER, "Se automatiza lo repetitivo")
    L = scene.layout
    criteria = L.column(
        note(scene, text="Un proceso es clave si…"),
        L.row(
            *[
                L.box(
                    text,
                    font_size="25px",
                    color=INK,
                    background=PAPER_DEEP,
                    padding=("10px", "18px"),
                )
                for text in KEY_PROCESS
            ],
            gap="14px",
            width="fill",
        ),
        gap="16px",
        width="fill",
    )
    engineer = role_column(
        scene,
        title="Ingeniero estructural",
        color=STEEL,
        row_height=ROLE_ROW,
        rows=[
            ("Estructura", "define la distribución de muros"),
            ("Modela y analiza", "construye el modelo en ETABS"),
            ("Interpreta", "lee diagnósticos y resultados"),
            ("Decide", "cambia muros o materiales"),
        ],
    )
    alba = role_column(
        scene,
        title="Marco de trabajo · Alba",
        color=BRICK,
        row_height=ROLE_ROW,
        rows=[
            ("Extracción", "lee y valida el modelo por API"),
            ("Verificación", "ejecuta los módulos E.070 y E.030"),
            ("Retroalimentación", "señala muro, piso y dirección"),
            ("Reporte", "documenta la iteración en PDF"),
        ],
    )
    # Estructura → Extracción y Retroalimentación → Interpreta.
    gutter = arrow_gutter(
        scene,
        slots=[("modelo", True), None, ("diagnóstico", False), None],
        row_height=ROLE_ROW,
    )
    table = L.row(engineer, gutter, alba, gap="24px", width="fill")
    page(scene, body=[criteria, table], gap="56px", top="200px")
    scene.play(enter(criteria))
    scene.stop("criterios-procesos-clave")

    scene.play(enter(engineer, each=0.05, duration=0.3))
    scene.play(enter(alba, each=0.05, duration=0.3))
    scene.play(enter(gutter, each=0.15, duration=0.4))
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
    # Aviso del dato ausente: símbolo, rótulo y dos líneas cortas, en una caja a su
    # medida; el texto va encima de la caja, que se crea después de medirlo.
    dx, dy = -6.7, -0.6
    warn = scene.geometry.group(
        [
            scene.geometry.circle(0.17)
            .no_fill()
            .stroke(FAIL, 0.03)
            .move_to(dx + 0.17, dy - 0.15),
            t(
                scene,
                "!",
                dx + 0.17,
                dy - 0.15,
                size=0.22,
                weight=900,
                color=FAIL,
                anchor=Anchor.CENTER,
            ),
        ]
    ).z_index(1)
    diag_lines = [
        t(
            scene,
            "Dato ausente o incompatible",
            dx + 0.5,
            dy,
            size=0.19,
            weight=900,
            color=FAIL,
        ),
        t(
            scene,
            "diagnóstico: se detiene el módulo",
            dx + 0.5,
            dy - 0.36,
            size=0.17,
            color=INK_SOFT,
        ),
        t(
            scene,
            "no es un incumplimiento",
            dx + 0.5,
            dy - 0.64,
            size=0.17,
            weight=700,
            color=INK,
        ),
    ]
    for line in diag_lines:
        line.z_index(1)
    diag_right = max(line.bounds().right for line in diag_lines) + 0.25
    diag = panel(
        scene,
        dx - 0.25,
        dy + 0.25,
        diag_right - dx + 0.25,
        1.3,
        fill=CARD,
        border=RULE,
        anchor=Anchor.TOP_LEFT,
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
        -1.9, y1 - 0.5, diag_right, dy + 0.25, dash_length=0.07, gap_length=0.05
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
            warn.animate.fade_in().duration(0.3),
            *[line.animate.fade_in().duration(0.3) for line in diag_lines],
            each=0.12,
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


@dataclass(frozen=True)
class FlowStep:
    """Nodo de un diagrama de módulo; ``no`` es la rama negativa de una decisión."""

    kind: Literal["io", "process", "decision"]
    text: str
    no: str | None = None
    w: float | None = None  # sin ancho, el del carril

    def h(self, size: float) -> float:
        """Alto según las líneas y la letra; el rombo necesita holgura para el texto."""
        lines = self.text.count("\n") + 1
        return lines * 1.55 * size + (0.555 if self.kind == "decision" else 0.235)

    def reach(self, size: float) -> float:
        """Media altura hasta donde llega una flecha: el vértice o poco antes del borde."""
        return self.h(size) / 2 + (0.0 if self.kind == "decision" else 0.04)


@dataclass(frozen=True)
class Module:
    """Diagrama del cap. 6 en dos carriles: se muestra como evidencia, sin recorrido."""

    tab: int
    stop: str
    source: str
    size: float
    lanes: tuple[tuple[FlowStep, ...], tuple[FlowStep, ...]]


@dataclass(frozen=True)
class Chart:
    """Diagrama dibujado: nodos y centros por carril, flechas y ramas «no»."""

    nodes: list[list[Drawable]]
    ys: list[list[float]]
    arrows: list[Drawable]
    notes: list[Drawable]
    flow: list[tuple[Drawable, bool]]  # orden de lectura; True si es flecha

    @property
    def pieces(self) -> list[Drawable]:
        return [d for d, _ in self.flow] + self.notes

    def entrance(self) -> Composition:
        return sequence(
            stagger(
                *[
                    d.animate.grow_arrow().duration(0.25)
                    if arrow
                    else d.animate.fade_in().duration(0.25)
                    for d, arrow in self.flow
                ],
                each=0.05,
            ),
            parallel(*[n.animate.fade_in().duration(0.25) for n in self.notes]),
        )


DENSITY = (
    FlowStep(
        "io",
        "Parámetros Z, U, S, N, $A_p$ · tabla de muros (etiqueta, L, t, material)",
    ),
    FlowStep(
        "decision",
        "¿Datos completos y unidades compatibles?",
        no="no → diagnóstico,\nsin resultado",
        w=3.9,
    ),
    FlowStep("process", "Clasificar muros por dirección (X / Y) y material"),
    FlowStep("process", "Aporte efectivo: albañilería L·t · concreto L·t·Ec/Em"),
    FlowStep("process", "Sumar los aportes de cada dirección"),
    FlowStep("process", '$D_"mín" = Z U S N slash 56$   ·   $D = sum L t slash A_p$'),
    FlowStep(
        "decision",
        '¿$D_X$ y $D_Y >= D_"mín"$?',
        no="no → registra dirección\ne incumplimiento",
        w=3.4,
    ),
    FlowStep("io", "Tabla comparativa y relación de muros considerados"),
)

# Figuras 44 a 46 sin Inicio ni Fin, como el diagrama de densidad. Los dos carriles
# tienen tantos pasos como filas: así ambos llenan el alto.
EVIDENCE = (
    Module(
        tab=1,
        stop="modulo-axial",
        source="Tesis · Figura 44, p. 107 (E.070, art. 19.1b)",
        size=0.2,
        lanes=(
            (
                FlowStep(
                    "io",
                    "Tabla por muro, nivel y dirección:\netiqueta, $P_m$, L, t, h, $f'_m$",
                ),
                FlowStep(
                    "process",
                    "Validar combinación de servicio,\ngeometría, material y unidades",
                ),
                FlowStep("process", "Recorrer los registros por muro y nivel"),
                FlowStep("process", "$sigma_m = P_m slash (L t)$"),
                FlowStep(
                    "process",
                    '$sigma_"adm1" = 0.2 f\'_m [1 - (h slash 35 t)^2]$   ·   '
                    '$sigma_"adm2" = 0.15 f\'_m$',
                ),
            ),
            (
                FlowStep(
                    "decision",
                    '¿$sigma_m <= sigma_"adm1"$\ny $sigma_m <= sigma_"adm2"$?',
                    no="no → «no cumple»: identifica\nmuro, nivel y dirección",
                    w=3.0,
                ),
                FlowStep(
                    "process",
                    'Estado «cumple»: registrar $sigma_m$, $sigma_"adm1"$ y $sigma_"adm2"$',
                ),
                FlowStep("process", "Repetir en todos los muros sin perder su origen"),
                FlowStep(
                    "process", "Consolidar e identificar el muro y nivel más exigidos"
                ),
                FlowStep("io", "Resultados y mensajes de diagnóstico"),
            ),
        ),
    ),
    Module(
        tab=2,
        stop="modulo-corte",
        source="Tesis · Figura 45, p. 109 (E.070, arts. 26.2 y 26.3)",
        size=0.19,
        lanes=(
            (
                FlowStep(
                    "io",
                    "Tabla por muro, nivel y dirección:\n"
                    "etiqueta, $V_e$, $M_e$, $P_g$, L, t, $v'_m$",
                ),
                FlowStep(
                    "process",
                    "Validar casos de carga, geometría, propiedades y unidades",
                ),
                FlowStep("process", "Recorrer cada muro con su nivel y dirección"),
                FlowStep(
                    "process",
                    "$alpha = V_e L slash M_e$, con $1 slash 3 <= alpha <= 1$",
                ),
                FlowStep("process", "$V_m = 0.5 v'_m alpha t L + 0.23 P_g$"),
                FlowStep(
                    "decision",
                    "¿$V_e <= 0.55 V_m$?",
                    no="no → registra el muro\ncon fisuración",
                    w=2.8,
                ),
            ),
            (
                FlowStep("process", "Registrar demanda, capacidad y estado por muro"),
                FlowStep("process", "Agrupar por entrepiso y dirección de análisis"),
                FlowStep("process", "$sum V_(m i)$   ·   $V_(E i) = 2 sum V_(e i)$"),
                FlowStep(
                    "decision",
                    "¿$sum V_(m i) >= V_(E i)$?",
                    no="no → registra entrepiso y\ndirección con insuficiencia",
                    w=3.2,
                ),
                FlowStep(
                    "process", "Generar tablas de fisuración y resistencia global"
                ),
                FlowStep("io", "Resultados y diagnósticos"),
            ),
        ),
    ),
    Module(
        tab=3,
        stop="modulo-derivas",
        source="Tesis · Figura 46, p. 110 (E.030, Tabla N.° 11)",
        size=0.2,
        lanes=(
            (
                FlowStep(
                    "io",
                    "Desplazamientos por nivel y dirección:\n"
                    "$u_i$, $u_(i-1)$, $h_i$ y factor $c$",
                ),
                FlowStep("process", "Validar caso sísmico, unidades y alturas"),
                FlowStep(
                    "process", "Ordenar niveles por elevación y separar por dirección"
                ),
                FlowStep("process", "$delta_i = abs(u_i - u_(i-1))$"),
                FlowStep("process", "$Delta_i slash h_i = c dot delta_i slash h_i$"),
            ),
            (
                FlowStep(
                    "decision",
                    "¿$Delta_i slash h_i <= 0.005$?",
                    no="no → registra nivel,\ndirección y distorsión",
                    w=3.2,
                ),
                FlowStep("process", "Estado «cumple»"),
                FlowStep("process", "Registrar distorsión y límite"),
                FlowStep(
                    "process", "Identificar la distorsión máxima y el nivel crítico"
                ),
                FlowStep("io", "Tabla y gráfico por dirección"),
            ),
        ),
    ),
)
# Pestañas centradas bajo el título; los diagramas ocupan todo el alto restante.
TAB_Y = 2.55
CHART_TOP, CHART_BOTTOM = 2.15, -3.45
LANE_X, LANE_W = (-3.55, 3.55), 5.6


def _rows(lanes: Sequence[Sequence[FlowStep]], size: float) -> list[list[float]]:
    """Centros y por carril: filas compartidas, repartidas de arriba abajo."""
    count = max(len(lane) for lane in lanes)
    heights = [
        max(lane[i].h(size) for lane in lanes if i < len(lane)) for i in range(count)
    ]
    gap = (CHART_TOP - CHART_BOTTOM - sum(heights)) / (count - 1)
    assert gap > 0.1, f"el diagrama no cabe (separación {gap:.2f})"
    centers: list[float] = []
    y = CHART_TOP
    for h in heights:
        centers.append(y - h / 2)
        y -= h + gap
    return [centers[: len(lane)] for lane in lanes]


def _flow_node(
    scene: Scene, step: FlowStep, cx: float, cy: float, w: float, size: float
) -> Drawable:
    h = step.h(size)
    if step.kind == "io":
        return io(scene, cx, cy, w, h, step.text, size=size)
    if step.kind == "decision":
        return decision(scene, cx, cy, w, h, step.text, size=size)
    return process(scene, cx, cy, w, h, step.text, size=size)


def _draw_chart(
    scene: Scene,
    lanes: Sequence[Sequence[FlowStep]],
    xs: Sequence[float],
    *,
    size: float,
    width: float,
) -> Chart:
    """Dibuja un diagrama por carriles; el último paso de uno lleva al primero del otro."""
    ys = _rows(lanes, size)
    nodes: list[list[Drawable]] = []
    arrows: list[Drawable] = []
    notes: list[Drawable] = []
    flow: list[tuple[Drawable, bool]] = []
    for lane, (steps, cx, centers) in enumerate(zip(lanes, xs, ys, strict=True)):
        column: list[Drawable] = []
        for i, (step, cy) in enumerate(zip(steps, centers, strict=True)):
            w = step.w or width
            arrow: Drawable | None = None
            if i > 0:
                arrow = link(
                    scene,
                    (cx, centers[i - 1] - steps[i - 1].reach(size)),
                    (cx, cy + step.reach(size)),
                )
            elif lane > 0:
                last, lx, ly = lanes[lane - 1][-1], xs[lane - 1], ys[lane - 1][-1]
                turn = (lx + cx) / 2
                arrow = link(
                    scene,
                    (lx + (last.w or width) / 2 + 0.04, ly),
                    (turn, ly),
                    (turn, cy),
                    (cx - w / 2 - 0.04, cy),
                )
            if arrow is not None:
                arrows.append(arrow)
                flow.append((arrow, True))
            node = _flow_node(scene, step, cx, cy, w, size)
            column.append(node)
            flow.append((node, False))
            if step.no is not None:
                # La rama «no» se escribe hacia fuera del carril.
                outer = lane == 0
                notes.append(
                    t(
                        scene,
                        step.no,
                        cx + (w / 2 + 0.1) * (-1 if outer else 1),
                        cy + 0.05,
                        size=round(size * 0.82, 3),
                        color=FAIL,
                        anchor=Anchor.RIGHT if outer else Anchor.LEFT,
                    )
                )
        nodes.append(column)
    return Chart(nodes, ys, arrows, notes, flow)


def _tabs(scene: Scene, names: Sequence[str]) -> tuple[list[Box], list[Box]]:
    """Pestañas centradas, cada una activa e inactiva en el mismo lugar."""
    on: list[Box] = []
    off: list[Box] = []
    for name in names:
        for boxes, active in ((on, True), (off, False)):
            boxes.append(
                pill(
                    scene,
                    name,
                    0,
                    TAB_Y,
                    size=0.17,
                    font="Lato",
                    weight=900 if active else 400,
                    color=BRICK_DEEP if active else MUTED,
                    background=BRICK_SOFT if active else PAPER_DEEP,
                    anchor=Anchor.LEFT,
                )
            )
    widths = [
        max(a.bounds().width, b.bounds().width) for a, b in zip(on, off, strict=True)
    ]
    gap = 0.18
    x = -(sum(widths) + gap * (len(widths) - 1)) / 2
    for a, b, width in zip(on, off, widths, strict=True):
        a.move_to(x, TAB_Y, Anchor.LEFT)
        b.move_to(x, TAB_Y, Anchor.LEFT)
        x += width + gap
    return on, off


def density_module(scene: Scene) -> None:
    header(
        scene, KICKER, "Cada verificación es un módulo con entradas, reglas y salidas"
    )
    tab_on, tab_off = _tabs(
        scene, ["Densidad", "Esfuerzo axial", "Fisuración y corte", "Derivas"]
    )
    scene.play(
        stagger(
            *[
                (tab_on if i == 0 else tab_off)[i].animate.fade_in().duration(0.25)
                for i in range(len(tab_on))
            ],
            each=0.06,
        )
    )

    cx, w = -2.85, 5.3
    chart = _draw_chart(scene, [DENSITY], [cx], size=0.17, width=w)
    nodes, ys, arrows = chart.nodes[0], chart.ys[0], chart.arrows
    side_error, side_fail = chart.notes
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
    reference = source(
        scene,
        "Tesis · Figura 43, p. 105 (E.070, art. 19.2) · valores: Tabla 22, p. 57",
    )
    scene.stop("modulo-recorrido")

    # Los otros tres módulos pasan como evidencia: misma estructura, sin recorrido.
    shown: list[Drawable] = [
        *nodes,
        *arrows,
        side_error,
        side_fail,
        *leaders,
        *value_items,
        reference,
    ]
    active = 0
    for module in EVIDENCE:
        chart = _draw_chart(scene, module.lanes, LANE_X, size=module.size, width=LANE_W)
        reference = source_block(scene, reference=module.source)
        scene.play(
            [
                *[d.animate.fade_out().duration(0.3) for d in shown],
                tab_on[active].animate.fade_out().duration(0.3),
                tab_off[active].animate.fade_in().duration(0.3),
                tab_off[module.tab].animate.fade_out().duration(0.3),
                tab_on[module.tab].animate.fade_in().duration(0.3),
                chart.entrance().delay(0.3),
                reference.animate.fade_in().duration(0.3).delay(0.3),
            ]
        )
        scene.stop(module.stop)
        shown, active = [*chart.pieces, reference], module.tab


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
                "1.5 min. Figura 43 (p. 105) como ejemplo de módulo: entradas, validación, "
                "clasificación, aporte efectivo (concreto con Ec/Em), suma, comparación y salida. "
                "A la derecha, los valores del caso en cada paso. Luego tres pasadas rápidas, "
                "unos 5 s cada una y sin recorrerlas: esfuerzo axial (Fig. 44), fisuración y corte "
                "(Fig. 45, por muro y luego por entrepiso) y derivas (Fig. 46). Basta decir que "
                "siguen la misma estructura: datos, validación, cálculo, decisión y salida."
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
