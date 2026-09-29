"""Bloque 4 · Proceso manual: caso de estudio, idealizaciones, criterios y ciclo iterativo."""

import math

from gaanim import (
    Anchor,
    Direction,
    Drawable,
    Scene,
    Section,
    SectionStep,
    Transition,
    computed,
    stagger,
)

from tesis.app import thesis_image
from tesis.building import DEPTH, WIDTH, draw_plan, grow_walls
from tesis.data.thesis import (
    AUTOMATIC_DRIFT,
    CASE,
    MESH_STEP,
    NO_CONFINEMENT_DRIFT,
)
from tesis.components import enter, header, image_card, page, panel, source, takeaway_at
from tesis.components import note as caption_note
from tesis.components import takeaway as takeaway_box
from tesis.kit import dimension, label, t
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    CONCRETE,
    DISPLAY,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PAPER_DEEP,
    RULE,
    STEEL,
)

KICKER = "04 · Proceso manual"


def case_study(scene: Scene) -> None:
    header(scene, KICKER, "Caso de estudio: vivienda de cuatro pisos en Lima")
    plan = draw_plan(scene, (-2.45, -0.3), 7.5, labels=True, drawn_thickness=0.085)
    ox, oy = plan.origin
    s = plan.scale
    dims = [
        dimension(
            scene, (ox, oy), (ox + WIDTH * s, oy), "16.60 m", side="below", offset=0.45
        ),
        dimension(
            scene,
            (ox + WIDTH * s, oy),
            (ox + WIDTH * s, oy + DEPTH * s),
            "8.00 m",
            side="right",
        ),
    ]
    scene.play(
        stagger(
            stagger(*[g.animate.create().duration(0.5) for g in plan.grid], each=0.03),
            stagger(
                *[b.animate.fade_in().duration(0.25) for b in plan.bubbles], each=0.02
            ),
            plan.slab.animate.fade_in().duration(0.4),
            plan.void.animate.fade_in().duration(0.3),
            grow_walls(plan.all_walls, total=0.8, duration=0.35),
            stagger(
                *[lab.animate.fade_in().duration(0.25) for lab in plan.labels.values()],
                each=0.015,
            ),
            stagger(*[d.animate.fade_in().duration(0.4) for d in dims], each=0.1),
            each=0.2,
        )
    )
    rows = [
        ("Ubicación", "Lima · suelo de cascajo (S1)"),
        ("Uso", "Vivienda · U = 1.0"),
        ("Altura", f"{CASE['pisos']} pisos · {CASE['altura']:.2f} m de piso a techo"),
        (
            "Planta",
            f"{CASE['planta'][0]:.1f} × {CASE['planta'][1]:.1f} m · A = {CASE['area']:.2f} m²",
        ),
        ("Losa", "maciza de 12 cm · diafragma rígido"),
        ("Albañilería", f"t = 13 cm · f'm = {CASE['fm']:.0f} kgf/cm²"),
        ("Concreto", f"f'c = {CASE['fc']:.0f} kgf/cm² · muros X2"),
        ("Sismo", "Zona 4 · Z = 0.45 · S = 1.0"),
    ]
    L = scene.layout
    sheet = L.column(
        *[
            L.column(
                caption_note(scene, text=name, size="17px"),
                L.box(value, font_size="26px", color=INK),
                gap="4px",
            )
            for name, value in rows
        ],
        gap="17px",
        within="safe",
        width="fill",
        height="fill",
        padding=("200px", "24px", "110px", "1266px"),
    )
    scene.play(enter(sheet, each=0.04, duration=0.3))
    scene.stop("caso-datos")

    x2 = plan.instances("X2")
    note = t(
        scene,
        "X2: muros de concreto armado en el eje A\npara acercar el centro de rigidez al de masas",
        -2.45,
        -3.0,
        size=0.2,
        color=CONCRETE,
        weight=700,
        anchor=Anchor.TOP,
    )
    scene.play(
        [
            *[w.animate.indicate().duration(0.8) for w in x2],
            note.animate.fade_in().duration(0.5),
        ]
    )
    source(
        scene,
        "Tesis · Tablas 20 y 21, pp. 52–53; Figura 34, p. 66 · planta de San Bartolomé (2006), "
        "etiquetas Pier del modelo en ETABS (′ = simétrico _2)",
    )
    scene.stop("caso-x2")


def _mct_wall(scene: Scene, cx: float, cy: float, w: float, h: float) -> list[Drawable]:
    """Dos pisos de muro como malla de áreas; confinamientos como barras."""
    stories = 2
    sh = h / stories
    parts: list[Drawable] = []
    parts.append(scene.geometry.rect(w, h).fill(BRICK_SOFT).no_stroke().move_to(cx, cy))
    nx, ny = 8, 8
    for i in range(1, nx):
        x = cx - w / 2 + i * w / nx
        parts.append(
            scene.geometry.line(x, cy - h / 2, x, cy + h / 2).stroke(BRICK, 0.01)
        )
    for j in range(1, ny):
        y = cy - h / 2 + j * h / ny
        parts.append(
            scene.geometry.line(cx - w / 2, y, cx + w / 2, y).stroke(BRICK, 0.01)
        )
    for x in (cx - w / 2, cx + w / 2):
        parts.append(
            scene.geometry.line(x, cy - h / 2, x, cy + h / 2).stroke(CONCRETE, 0.07)
        )
    for k in range(1, stories + 1):
        y = cy - h / 2 + k * sh
        parts.append(
            scene.geometry.line(cx - w / 2, y, cx + w / 2, y).stroke(CONCRETE, 0.07)
        )
    for k in range(stories + 1):
        y = cy - h / 2 + k * sh
        for i in range(nx + 1):
            parts.append(
                scene.geometry.circle(0.028)
                .fill(INK)
                .no_stroke()
                .move_to(cx - w / 2 + i * w / nx, y)
            )
    parts.append(
        scene.geometry.line(
            cx - w / 2 - 0.3, cy - h / 2, cx + w / 2 + 0.3, cy - h / 2
        ).stroke(INK_SOFT, 0.02)
    )
    parts.append(
        t(
            scene,
            "malla shell",
            cx + w / 2 + 0.2,
            cy + h / 4,
            font=MONO,
            size=0.14,
            color=BRICK_DEEP,
            anchor=Anchor.LEFT,
        )
    )
    parts.append(
        t(
            scene,
            "frame",
            cx + w / 2 + 0.2,
            cy - h / 2 + 0.25,
            font=MONO,
            size=0.14,
            color=CONCRETE,
            anchor=Anchor.LEFT,
        )
    )
    return parts


def _mst_frame(
    scene: Scene, cx: float, cy: float, w: float, h: float
) -> list[Drawable]:
    """Pórtico plano: barra en el centroide, brazos rígidos y vigas."""
    stories = 2
    sh = h / stories
    parts: list[Drawable] = [
        scene.geometry.rect(w, h).no_fill().stroke(RULE, 0.014).move_to(cx, cy),
    ]
    parts.append(
        scene.geometry.line(cx, cy - h / 2, cx, cy + h / 2).stroke(STEEL, 0.08)
    )
    for k in range(1, stories + 1):
        y = cy - h / 2 + k * sh
        parts.append(scene.geometry.line(cx - w / 2, y, cx + w / 2, y).stroke(INK, 0.1))
        parts.append(
            scene.geometry.line(cx - w / 2 - 0.8, y, cx - w / 2, y).stroke(STEEL, 0.035)
        )
        parts.append(
            scene.geometry.line(cx + w / 2, y, cx + w / 2 + 0.8, y).stroke(STEEL, 0.035)
        )
        for x in (cx - w / 2, cx, cx + w / 2):
            parts.append(
                scene.geometry.circle(0.05).fill(INK).no_stroke().move_to(x, y)
            )
    parts.append(
        scene.geometry.line(
            cx - w / 2 - 0.9, cy - h / 2, cx + w / 2 + 0.9, cy - h / 2
        ).stroke(INK_SOFT, 0.02)
    )
    parts.append(
        scene.geometry.circle(0.06).fill(INK).no_stroke().move_to(cx, cy - h / 2)
    )
    parts.append(
        t(
            scene,
            "brazo rígido",
            cx - w / 4,
            cy + h / 2 + 0.1,
            font=MONO,
            size=0.14,
            color=INK,
            anchor=Anchor.BOTTOM,
        )
    )
    parts.append(
        t(
            scene,
            "barra",
            cx + 0.12,
            cy - h / 4,
            font=MONO,
            size=0.14,
            color=STEEL,
            anchor=Anchor.LEFT,
        )
    )
    parts.append(
        t(
            scene,
            "viga",
            cx + w / 2 + 0.4,
            cy + h / 2 + 0.1,
            font=MONO,
            size=0.14,
            color=STEEL,
            anchor=Anchor.BOTTOM,
        )
    )
    return parts


def idealizations(scene: Scene) -> None:
    header(scene, KICKER, "Dos formas de idealizar el mismo muro: áreas o barras")
    columns = [
        (
            -3.7,
            "MCT · modelo completo tridimensional",
            BRICK,
            _mct_wall,
            [
                "Muros: elementos shell-thin con malla de 0.5 m",
                "Confinamientos: elementos frame con nodos compatibles",
                "Cargas: metrado automático del volumen modelado",
                "Fuerzas por muro: integración en secciones Pier",
            ],
        ),
        (
            3.7,
            "MSTA / MSTO · pórticos planos",
            STEEL,
            _mst_frame,
            [
                "Muros: barras en el centroide de la sección transformada",
                "Brazos rígidos hasta los bordes del muro",
                "Cargas: áreas tributarias (método del sobre)",
                "Diafragma rígido que integra los pórticos",
            ],
        ),
    ]
    for cx, name, color, draw, bullets in columns:
        tag = label(scene, name, cx, 2.45, color=color, size=0.16, anchor=Anchor.TOP)
        drawing = draw(scene, cx, 0.8, 2.6, 2.1)
        texts: list[Drawable] = []
        for i, line in enumerate(bullets):
            y = -0.7 - i * 0.48
            texts.append(
                scene.geometry.circle(0.045)
                .fill(color)
                .no_stroke()
                .move_to(cx - 3.1, y - 0.12)
            )
            texts.append(t(scene, line, cx - 2.9, y, size=0.22, color=INK))
        scene.play(
            stagger(
                tag.animate.fade_in().duration(0.3),
                stagger(
                    *[d.animate.fade_in().duration(0.3) for d in drawing], each=0.006
                ),
                stagger(
                    *[
                        x.animate.fade_in_from(Direction.LEFT, 0.06).duration(0.3)
                        for x in texts
                    ],
                    each=0.05,
                ),
                each=0.25,
            )
        )
        scene.stop(f"idealizacion-{'mct' if color is BRICK else 'mst'}")
    divider = scene.geometry.line(0, 2.4, 0, -2.6).stroke(RULE, 0.012)
    scene.play(divider.animate.create().duration(0.4))
    takeaway_at(
        scene,
        "La idealización y la asignación de cargas cambian las fuerzas que llegan a cada muro",
        y=-3.15,
    )
    source(
        scene,
        "Tesis · §4.5, p. 49; §5.3.1 y §5.3.2, pp. 58 y 67 · esquemas conceptuales",
    )
    scene.stop("idealizaciones")


def criteria(scene: Scene) -> None:
    header(scene, KICKER, "El modelo depende de decisiones que el software no toma")
    cards = [
        (
            "cap4/Moelo_SC.png",
            f"+{NO_CONFINEMENT_DRIFT:.1f} %",
            "más deriva",
            "Si se omiten columnas y vigas\nde confinamiento; el peso\nsísmico baja 5.96 %.",
            BRICK,
        ),
        (
            "cap4/mesh_auto.png",
            f"−{abs(AUTOMATIC_DRIFT):.1f} %",
            "menos deriva",
            "Con las opciones automáticas\nde ETABS: puntos de inserción,\nbrazos rígidos y malla.",
            BRICK,
        ),
        (
            "cap4/Prueba_Mesh.png",
            f"{MESH_STEP:.1f} m",
            "malla suficiente",
            "Malla N8: variación menor a\n1 % frente a N16 en el muro\nde prueba de 4 pisos.",
            STEEL,
        ),
        (
            "cap5/PIERS.png",
            "X1 … Y7",
            "etiquetas Pier",
            "Una etiqueta por muro, igual\nen todos los pisos; con ella\nse agrupan las fuerzas.",
            STEEL,
        ),
    ]
    built = [
        image_card(
            scene,
            picture=scene.media.image(
                thesis_image(image), width=2.9, height=2.25, fit="contain"
            ),
            value=big,
            unit=unit,
            body=body.replace("\n", " "),
            color=color,
        )
        for image, big, unit, body, color in cards
    ]
    row = scene.layout.row(
        *built, gap="32px", align="stretch", width="fill", height="fill"
    )
    closing = takeaway_box(
        scene,
        text="Alba lee el modelo tal como fue construido: el criterio del ingeniero sigue siendo clave",
    )
    page(scene, body=[row, closing], gap="40px")
    for card in built:
        scene.play(
            enter(card, direction=Direction.UP, distance=0.08, duration=0.3, each=0.08)
        )
    scene.play(enter(closing))
    source(
        scene,
        "Tesis · Tablas 8, 14, 16 y 19, pp. 35, 42, 44 y 49; Figura 34, p. 66 · capturas de ETABS de la tesis",
    )
    scene.stop("criterios-modelamiento")


CHECKS = [
    "Espesor efectivo",
    "Esfuerzo axial por gravedad",
    "Densidad de muros",
    "Control de fisuración",
    "Resistencia al corte global",
    "Distorsiones de entrepiso",
    "Refuerzo horizontal",
    "Agrietamiento diagonal",
]


def manual_cycle(scene: Scene) -> None:
    header(
        scene, KICKER, "El proceso manual es un ciclo: cada cambio obliga a repetirlo"
    )
    cx, cy, r = -3.2, -0.3, 2.05
    stages = [
        ("Modelo y análisis\nen ETABS", 180),
        ("Exportar y filtrar\ntablas", 90),
        ("Copiar a hojas\nde cálculo", 0),
        ("Verificar\nE.070 · E.030", 270),
    ]
    ring = scene.geometry.circle(r).no_fill().stroke(RULE, 0.03).move_to(cx, cy)
    nodes: list[Drawable] = []
    for text, angle in stages:
        a = math.radians(angle)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        box = panel(scene, x, y, 2.25, 0.82, fill=CARD, border=RULE)
        caption = t(
            scene, text, x, y, size=0.19, weight=700, color=INK, anchor=Anchor.CENTER
        )
        nodes.append(scene.geometry.group([box, caption]).z_index(5))
    heads = []
    for angle in (135, 45, 315, 225):
        a = math.radians(angle)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        heads.append(
            scene.geometry.regular_polygon(3, 0.13)
            .fill(BRICK)
            .no_stroke()
            .move_to(x, y)
            .rotate_to(a)
            .z_index(3)
        )
    # El marcador reposa sobre el arco, entre nodos, para no tapar sus textos.
    rest = math.radians(158)
    angle = scene.viz.parameter(rest)
    token = scene.geometry.circle(0.11).fill(BRICK).no_stroke().z_index(2)
    token.move_to(
        computed(lambda v: cx + r * math.cos(v), inputs=[angle]),
        computed(lambda v: cy + r * math.sin(v), inputs=[angle]),
    )
    center_label = t(
        scene, "iteración", cx, cy + 0.35, size=0.18, color=MUTED, anchor=Anchor.CENTER
    )
    counter = scene.viz.rolling_number(
        1, font_family=DISPLAY, weight=700, font_size=0.75, color=BRICK
    )
    counter.move_to(cx, cy - 0.25, Anchor.CENTER)
    scene.play(
        stagger(
            ring.animate.create().duration(0.8),
            stagger(*[n.animate.fade_in().duration(0.35) for n in nodes], each=0.15),
            stagger(*[h.animate.fade_in().duration(0.2) for h in heads], each=0.05),
            center_label.animate.fade_in().duration(0.3),
            counter.visual.animate.fade_in().duration(0.3),
            token.animate.fade_in().duration(0.2),
            each=0.2,
        )
    )
    scene.stop("ciclo-manual")

    title = label(
        scene, "Verificaciones en la hoja de cálculo", 1.4, 2.4, color=MUTED, size=0.14
    )
    checks: list[Drawable] = []
    for i, name in enumerate(CHECKS):
        y = 1.95 - i * 0.44
        checks.append(
            t(
                scene,
                f"{i + 1:02d}",
                1.4,
                y,
                font=MONO,
                size=0.16,
                color=BRICK,
                anchor=Anchor.LEFT,
            )
        )
        checks.append(t(scene, name, 1.95, y, size=0.23, color=INK, anchor=Anchor.LEFT))
    scene.play(
        [
            title.animate.fade_in().duration(0.3),
            stagger(
                *[
                    c.animate.fade_in_from(Direction.LEFT, 0.06).duration(0.25)
                    for c in checks
                ],
                each=0.03,
            ),
        ]
    )
    # Dos vueltas del ciclo: cada una repite exportación, filtrado, copia y verificación.
    for lap in (2, 3):
        scene.play(
            [
                angle.animate.set(rest - 2 * math.pi * (lap - 1)).duration(2.2),
                counter.count_to(lap, duration=0.4).delay(1.9),
            ]
        )
    exit_y = cy - r
    exit_arrow = (
        scene.geometry.connector(
            (cx + 1.15, exit_y),
            (1.35, exit_y),
            head_length=0.14,
            head_width=0.14,
            body_width=0.028,
        )
        .fill(INK_SOFT)
        .no_stroke()
    )
    exit_label = t(
        scene,
        "¿todo cumple? sí",
        -0.35,
        exit_y + 0.1,
        size=0.17,
        color=INK_SOFT,
        anchor=Anchor.BOTTOM,
    )
    memory = panel(
        scene, 1.4, exit_y, 5.9, 0.75, fill=PAPER_DEEP, border=None, anchor=Anchor.LEFT
    )
    memory_t = t(
        scene,
        "Revisión de formato y memoria de cálculo en Word",
        1.65,
        exit_y,
        size=0.22,
        weight=700,
        color=INK,
        anchor=Anchor.LEFT,
    )
    scene.play(
        stagger(
            exit_arrow.animate.grow_arrow().duration(0.5),
            exit_label.animate.fade_in().duration(0.3),
            memory.animate.fade_in().duration(0.3),
            memory_t.animate.fade_in().duration(0.3),
            each=0.12,
        )
    )
    takeaway_at(
        scene,
        "Cada iteración repite la exportación, el filtrado y la transcripción de datos",
        y=-3.2,
    )
    source(
        scene,
        "Tesis · Figura 41, p. 80; §5.5.1 Extracción de datos y creación de hoja de cálculo, p. 81",
    )
    scene.stop("ciclo-repeticion")


SECTION = Section(
    "manual",
    [
        SectionStep(
            name="Proceso manual · caso de estudio",
            build=case_study,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Caso: 'Ejemplo de aplicación de la Norma E.070' de San Bartolomé (2006), "
                "resuelto originalmente con la E.030-2003 y SAP2000. Lima, cascajo, vivienda de 4 "
                "pisos, losa maciza de 12 cm, muros de 13 cm, f'm = 65 kgf/cm², f'c = 175 kgf/cm². "
                "La planta muestra las etiquetas Pier del modelo de ETABS; ′ indica el muro simétrico "
                "(_2). X2 son muros de concreto en el eje A para controlar la torsión."
            ),
        ),
        SectionStep(
            name="Proceso manual · idealizaciones",
            build=idealizations,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. MCT: muros como áreas shell-thin (membrana + placa) con malla, "
                "confinamientos como frames con nodos compatibles, losas membrane (E.030 art. 30.8), "
                "cargas por volumen modelado; las fuerzas de diseño se integran en secciones Pier. "
                "MST (pórticos planos, San Bartolomé): barras en el centroide de secciones "
                "transformadas (n = Ec/Em, ancho efectivo de muros ortogonales), brazos rígidos, vigas "
                "T/L y cargas por áreas tributarias. MSTA y MSTO usan esta idealización."
            ),
        ),
        SectionStep(
            name="Proceso manual · criterios de modelamiento",
            build=criteria,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Evidencia del cap. 4 con modelos de prueba: sin confinamientos el peso "
                "baja 5.96 % y las derivas suben hasta 38.50 %; con las opciones automáticas de ETABS "
                "(puntos de inserción, brazos rígidos, malla por defecto) las derivas son hasta 10.53 % "
                "menores (modelo más rígido, no conservador); la malla N8 de 0.5 m converge con "
                "variación menor a 1 %. Las etiquetas Pier deben ser únicas y continuas en altura."
            ),
        ),
        SectionStep(
            name="Proceso manual · ciclo iterativo",
            build=manual_cycle,
            transition=Transition.cross_fade(0.45),
            notes=(
                "45 s. Figura 41 (p. 80): modelo → exportar y filtrar tablas → copiar a hojas → "
                "verificar. Si algo no cumple, se busca el origen, se modifica el modelo y se repite "
                "todo. Ocho verificaciones en la hoja de cálculo. El contador de iteraciones es "
                "ilustrativo: la tesis no registró cuántas iteraciones tomó el caso."
            ),
        ),
    ],
)
