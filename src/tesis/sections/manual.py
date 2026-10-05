"""Bloque 4 · Proceso manual: caso de estudio, modelo completo en ETABS, pórticos planos,
criterios y ciclo iterativo."""

import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass

from gaanim import (
    Anchor,
    Anim,
    Box,
    Color,
    Composition,
    Direction,
    Drawable,
    Easing,
    EasingCurve,
    Playable,
    Scene,
    Section,
    SectionStep,
    Text,
    Transition,
    computed,
    parallel,
    sequence,
    stagger,
)

from tesis.app import thesis_image
from tesis.building import (
    AXIS_X,
    AXIS_Y,
    DEPTH,
    STAIR,
    THICKNESS,
    WIDTH,
    draw_plan,
    grow_walls,
)
from tesis.components import (
    compact_step,
    comparison_card,
    enter,
    header,
    page,
    panel,
    phase_heading,
    pill,
    source,
    takeaway_at,
)
from tesis.components import note as caption_note
from tesis.data.planta import STORIES
from tesis.data.porticos import (
    BARS,
    BEAMS,
    MODULAR_RATIO,
    SLAB_DEAD,
    SLAB_LIVE,
    STORY_COUNT,
    STORY_HEIGHT,
    WEIGHT_FACTOR_X4,
    X4,
    X4_POINT_LOADS,
    X4_START,
    X4_TRIBUTARY,
    tributary_x4,
)
from tesis.data.thesis import (
    CASE,
    LOAD_SETS,
    MESH_N16_VARIATION,
    MESH_SIZES,
    MESH_STEP,
    MODE_Y,
    MODEL_CHECKS,
    WEIGHT_BY_FLOOR,
)
from tesis.etabs_model import (
    FRAME,
    OVERLAY,
    SLAB,
    WALL_X,
    EtabsModel,
    Story,
    build_model,
    wall_lines,
)
from tesis.kit import dimension, label, t
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    BRICK_SOFT,
    CARD,
    CONCRETE,
    CONCRETE_SOFT,
    DISPLAY,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
    PAPER_DEEP,
    RULE,
    STEEL,
    STEEL_SOFT,
)
from tesis.vivienda import Iso

KICKER = "04 · Proceso manual"


def case_study(scene: Scene) -> None:
    header(scene, KICKER, "Caso de estudio: vivienda de cuatro pisos en Lima")
    plan = draw_plan(scene, (-2.4, 0.17), 8.1, labels=True, drawn_thickness=0.09)
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
                L.box(value, font_size="27px", color=INK),
                gap="4px",
            )
            for name, value in rows
        ],
        gap="27px",
        within="safe",
        width="fill",
        height="fill",
        padding=("150px", "24px", "110px", "1290px"),
    )
    scene.play(enter(sheet, each=0.04, duration=0.3))
    scene.stop("caso-datos")

    x2 = plan.instances("X2")
    note = t(
        scene,
        "X2: muros de concreto armado en el eje A\npara acercar el centro de rigidez al de masas",
        -2.4,
        -2.78,
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
        "San Bartolomé (2006). Ejemplo de aplicación de la Norma E.070 en el diseño de un "
        "edificio de albañilería confinada. PUCP · Tesis, Tablas 20–21 y Fig. 34 · ′ = simétrico",
    )
    scene.stop("caso-x2")


# La vista 3D de ETABS como la arma el ingeniero: Definir, Dibujar y Asignar.
MODEL_ISO = Iso((-5.6, -0.995), 0.265)
type Phases = tuple[tuple[str, str, tuple[tuple[str, str], ...]], ...]
MODEL_STEPS: Phases = (
    (
        "Definir",
        "Define",
        (
            ("Grillas y pisos", "Ejes 1–7 y A–D; cuatro pisos de 2.46 y 2.52 m"),
            ("Materiales", "Albañilería f'm = 65 y concreto f'c = 175 kgf/cm²"),
            ("Secciones", "Frames, muros shell-thin y losa membrane"),
        ),
    ),
    (
        "Dibujar",
        "Draw",
        (("Frames, muros y losas", "De nodo a nodo, en los cuatro pisos a la vez"),),
    ),
    (
        "Asignar",
        "Assign",
        (
            ("Malla y brazos rígidos", "Malla de 0.50 m en cada muro; brazos a mano"),
            ("Diafragma rígido", "D1 en cada losa: se mueve como un sólido"),
            ("Etiquetas Pier", "Un nombre por muro, el mismo en los cuatro pisos"),
            ("Cargas y masa", "CM 0.10 y CV 0.20 tonf/m²; masa = CM + 25 % CV"),
        ),
    ),
)
# Ventanas «Define»: filas en mono, alineadas por columnas de ancho fijo.
MATERIAL_ROWS = (
    f"{'Material':<14}{'Tipo':<10}{'E kgf/cm²':<11}{'ν':<6}γ kgf/m³",
    f"{'ALB65KGF/CM3':<14}{'Masonry':<10}{'32 500':<11}{'0.25':<6}1 800",
    f"{'C175KGF/CM2':<14}{'Concrete':<10}{'198 431':<11}{'0.15':<6}2 400",
)
SECTION_ROWS = (
    "Frame  C30x13 · CL25x13x13 · CT25x13x13 · V12x20 · V30x20",
    "Wall   M13 · P13    shell-thin · t = 13 cm",
    "Slab   LM12         membrane · t = 12 cm",
)
DIAPHRAGM_CENTER = (8.3, 4.09)  # centroide de la losa sin el vacío de escalera
SELECTED = Color.from_hex("#E2A88C")
ROOF_ARROWS = (
    (1.5, 2),
    (1.5, 6),
    (5, 2),
    (5, 6),
    (8.3, 6),
    (11.6, 2),
    (11.6, 6),
    (15.1, 2),
    (15.1, 6),
)
SWAY = 1.1  # m en la azotea: deformada exagerada


@dataclass
class StepList:
    """Pasos a la derecha, agrupados por fase; cada fase aparece con su primer paso."""

    heads: list[Box]
    rows: list[Box]
    opens: list[int | None]  # fase que abre cada paso, o None

    def enter(self, i: int) -> list[Playable]:
        """Aparece el paso i (y su fase); el anterior pasa a segundo plano."""
        anims: list[Playable] = [
            self.rows[i].animate.fade_in_from(Direction.LEFT, 0.06).duration(0.35)
        ]
        group = self.opens[i]
        if group is not None:
            anims.append(self.heads[group].animate.fade_in().duration(0.3))
        if i:
            anims.append(self.rows[i - 1].animate.opacity(0.4).duration(0.35))
        return anims

    def restore(self) -> list[Playable]:
        return [r.animate.opacity(1).duration(0.4) for r in self.rows]


def _steps_panel(scene: Scene, phases: Phases) -> StepList:
    L = scene.layout
    steps = StepList([], [], [])
    groups: list[Box] = []
    for g, (phase, menu, entries) in enumerate(phases):
        head = phase_heading(scene, name=phase, tag=menu)
        items: list[Box] = []
        for i, (name, text) in enumerate(entries):
            items.append(
                compact_step(scene, number=len(steps.rows) + 1, name=name, text=text)
            )
            steps.rows.append(items[-1])
            steps.opens.append(g if i == 0 else None)
        steps.heads.append(head)
        groups.append(L.column(head, *items, gap="14px"))
    L.column(
        *groups,
        gap="30px",
        within="safe",
        width="fill",
        height="fill",
        justify="start",
        padding=("150px", "24px", "0px", "1014px"),
    )
    return steps


def _pointer(scene: Scene) -> Drawable:
    """Puntero del ratón; su punta es la esquina superior izquierda."""
    tip = [
        (0.0, 0.0),
        (0.0, -0.3),
        (0.072, -0.232),
        (0.118, -0.335),
        (0.158, -0.318),
        (0.113, -0.217),
        (0.205, -0.212),
    ]
    return (
        scene.geometry.polygon(tip)
        .fill(INK)
        .stroke(CARD, 0.016)
        .z_index(OVERLAY + 15)
        .hidden()
    )


def _click(scene: Scene, x: float, y: float) -> Composition:
    ring = (
        scene.geometry.circle(0.05)
        .no_fill()
        .stroke(BRICK, 0.012)
        .move_to(x, y)
        .z_index(OVERLAY + 14)
        .hidden()
    )
    return sequence(
        ring.animate.fade_in().duration(0.04),
        parallel(
            ring.animate.scale_to(3.2).duration(0.4),
            ring.animate.fade_out().duration(0.4),
        ),
    )


def _define_window(
    scene: Scene, title: str, rows: Sequence[str], top: float, *, head: bool
) -> tuple[list[Drawable], list[Text], list[float]]:
    """Ventana de ETABS: título con la ruta del menú y filas que se escriben."""
    left, width, pitch = -5.8, 5.25, 0.27
    first = top - 0.62
    height = 0.62 + pitch * len(rows) + 0.08
    frame = (
        scene.geometry.rect(width, height)
        .fill(CARD)
        .stroke(RULE, 0.016)
        .move_to(left + width / 2, top - height / 2)
        .z_index(OVERLAY)
    )
    caption = t(
        scene,
        title,
        left + 0.2,
        top - 0.2,
        font=MONO,
        size=0.12,
        color=INK_SOFT,
        anchor=Anchor.LEFT,
    ).z_index(OVERLAY + 1)
    rule = (
        scene.geometry.line(left, top - 0.4, left + width, top - 0.4)
        .stroke(RULE, 0.01)
        .z_index(OVERLAY + 1)
    )
    ys = [first - i * pitch for i in range(len(rows))]
    texts = [
        t(
            scene,
            row,
            left + 0.52,
            y,
            font=MONO,
            size=0.125,
            color=MUTED if head and i == 0 else INK,
            anchor=Anchor.LEFT,
        ).z_index(OVERLAY + 1)
        for i, (row, y) in enumerate(zip(rows, ys, strict=True))
    ]
    return [frame, caption, rule], texts, ys


def _section_icons(scene: Scene, x: float, ys: Sequence[float]) -> list[Drawable]:
    """Frame, muro y losa en miniatura, con los colores del modelo."""
    frame_y, wall_y, slab_y = ys
    frame = scene.geometry.group(
        [
            scene.geometry.line(x, frame_y - 0.1, x, frame_y + 0.1).stroke(FRAME, 0.02),
            scene.geometry.circle(0.022)
            .fill(FRAME)
            .no_stroke()
            .move_to(x, frame_y - 0.1),
            scene.geometry.circle(0.022)
            .fill(FRAME)
            .no_stroke()
            .move_to(x, frame_y + 0.1),
        ]
    )
    mini = Iso((x - 0.12, wall_y - 0.06), 0.075)
    wall = (
        scene.geometry.polygon(
            [mini(0, 0, 0), mini(3, 0, 0), mini(3, 0, 2), mini(0, 0, 2)]
        )
        .fill(WALL_X)
        .stroke(BRICK, 0.008)
    )
    flat = Iso((x - 0.15, slab_y), 0.06)
    slab = (
        scene.geometry.polygon(
            [flat(0, 0, 0), flat(3, 0, 0), flat(3, 2, 0), flat(0, 2, 0)]
        )
        .fill(SLAB)
        .stroke(CONCRETE, 0.008)
    )
    return [g.z_index(OVERLAY + 2).hidden() for g in (frame, wall, slab)]


def full_model(scene: Scene) -> None:
    header(scene, KICKER, "El modelo completo se arma en ETABS en ocho pasos")
    model = build_model(scene, MODEL_ISO)
    iso = model.iso
    top = model.height
    steps = _steps_panel(scene, MODEL_STEPS)
    step = steps.enter

    # 1 · Grillas en la base y pisos que suben desde ella hasta su cota.
    level_labels = [
        t(
            scene,
            f"{name:<7}{z:5.2f}",
            iso(0, 0, z)[0] - 0.42,
            iso(0, 0, z)[1],
            font=MONO,
            size=0.11,
            color=MUTED if z == 0 else INK_SOFT,
            anchor=Anchor.RIGHT,
        ).hidden()
        for name, z in STORIES
    ]
    tx, ty = -6.95, 2.2
    triad: list[Drawable] = []
    for (dx, dy), name, color in (
        ((0.866, -0.5), "X", BRICK),
        ((0.866, 0.5), "Y", STEEL),
        ((0.0, 1.0), "Z", INK_SOFT),
    ):
        end = (tx + 0.4 * dx, ty + 0.4 * dy)
        triad.append(
            scene.geometry.arrow(
                tx, ty, *end, head_length=0.08, head_width=0.08, body_width=0.016
            )
            .fill(color)
            .no_stroke()
            .hidden()
        )
        triad.append(
            t(
                scene,
                name,
                end[0] + 0.1 * dx + (0.05 if dx else 0),
                end[1] + 0.1 * dy,
                size=0.13,
                weight=900,
                color=color,
                anchor=Anchor.CENTER,
            ).hidden()
        )
    for story, lab in zip(model.stories, level_labels[1:], strict=True):
        rise = story.z1 * iso.scale
        story.edge.drawable.shift_by(0, -rise)
        lab.shift_by(0, -rise)
    scene.play(
        [
            *step(0),
            stagger(*[g.animate.create().duration(0.5) for g in model.grid], each=0.04),
            stagger(
                *[b.animate.fade_in().duration(0.25) for b in model.bubbles],
                each=0.03,
            ).delay(0.3),
            stagger(*[p.animate.fade_in().duration(0.3) for p in triad], each=0.05),
            level_labels[0].animate.fade_in().duration(0.3).delay(0.5),
        ]
    )
    scene.play(
        stagger(
            *[
                parallel(
                    story.edge.drawable.animate.fade_in().duration(0.2),
                    story.edge.drawable.animate.shift_by(0, story.z1 * iso.scale)
                    .duration(0.8)
                    .easing(Easing.SMOOTH),
                    lab.animate.fade_in().duration(0.2),
                    lab.animate.shift_by(0, story.z1 * iso.scale)
                    .duration(0.8)
                    .easing(Easing.SMOOTH),
                )
                for story, lab in zip(model.stories, level_labels[1:], strict=True)
            ],
            each=0.22,
        )
    )
    scene.stop("mct-grillas")

    # 2 · Materiales y 3 · secciones: el ingeniero llena las ventanas de «Define».
    materials, material_texts, material_ys = _define_window(
        scene, "Define › Material Properties", MATERIAL_ROWS, 2.6, head=True
    )
    swatches = [
        scene.geometry.rect(0.15, 0.15)
        .fill(color)
        .no_stroke()
        .move_to(-5.53, y)
        .z_index(OVERLAY + 2)
        .hidden()
        for color, y in ((BRICK, material_ys[1]), (CONCRETE, material_ys[2]))
    ]
    sections, section_texts, section_ys = _define_window(
        scene, "Define › Section Properties", SECTION_ROWS, 0.95, head=False
    )
    icons = _section_icons(scene, -5.53, section_ys)

    def typed(text: Text, row: str, cps: float = 60) -> Anim:
        return text.animate.typewriter(cps=cps, cursor="▍", keep_cursor=False).duration(
            len(row) / cps
        )

    scene.play(
        [
            *step(1),
            *[
                m.animate.fade_in_from(Direction.UP, 0.06).duration(0.35)
                for m in materials
            ],
            sequence(
                material_texts[0].animate.fade_in().duration(0.25),
                parallel(
                    swatches[0].animate.grow_from_center().duration(0.2),
                    typed(material_texts[1], MATERIAL_ROWS[1]),
                ),
                parallel(
                    swatches[1].animate.grow_from_center().duration(0.2),
                    typed(material_texts[2], MATERIAL_ROWS[2]),
                ),
            ).delay(0.3),
        ]
    )
    scene.play(
        [
            *step(2),
            *[
                m.animate.fade_in_from(Direction.UP, 0.06).duration(0.35)
                for m in sections
            ],
            sequence(
                *[
                    parallel(icon.animate.fade_in().duration(0.2), typed(text, row))
                    for icon, text, row in zip(
                        icons, section_texts, SECTION_ROWS, strict=True
                    )
                ]
            ).delay(0.3),
        ]
    )
    scene.wait(0.3)
    scene.stop("mct-propiedades")

    # 4 · Dibujo en Story4 con «Similar Stories»: cada clic aparece en los cuatro pisos.
    def at_top(x: float, y: float) -> tuple[float, float]:
        return iso(x, y, top)

    pointer = _pointer(scene).move_to(*at_top(6.0, 4.0), Anchor.TOP_LEFT)

    def point_to(
        x: float, y: float, duration: float = 0.4, easing: Easing = Easing.SMOOTH
    ) -> Anim:
        return (
            pointer.animate.move_to(*at_top(x, y), Anchor.TOP_LEFT)
            .duration(duration)
            .easing(easing)
        )

    windows = [
        *materials,
        *material_texts,
        *swatches,
        *sections,
        *section_texts,
        *icons,
    ]
    scene.play(
        [
            *step(3),
            *[w.animate.fade_out().duration(0.3) for w in windows],
            pointer.animate.fade_in().duration(0.3).delay(0.2),
        ]
    )
    first = [(0.0, 0.0), (3.0, 0.0)]
    for node in first:
        scene.play(point_to(*node))
        scene.play(
            [
                _click(scene, *at_top(*node)),
                *[
                    s.columns[node].drawable.animate.create().duration(0.4)
                    for s in model.stories
                ],
            ]
        )
    others = [
        shape.drawable
        for s in model.stories
        for node, shape in s.columns.items()
        if node not in first
    ]
    scene.play(
        stagger(
            *[c.animate.create().duration(0.3) for c in others],
            total=0.9,
            origin=at_top(3, 0),
        )
    )
    # Viga X1: se arrastra de nodo a nodo.
    span = ((0.0, 0.0), (3.0, 0.0))
    scene.play(point_to(*span[0]))
    scene.play(
        [
            point_to(*span[1], 0.6, Easing.LINEAR),
            *[
                s.beams[span]
                .drawable.animate.create()
                .duration(0.6)
                .easing(Easing.LINEAR)
                for s in model.stories
            ],
        ]
    )
    scene.play(
        stagger(
            *[
                shape.drawable.animate.create().duration(0.3)
                for s in model.stories
                for key, shape in s.beams.items()
                if key != span
            ],
            total=0.9,
            origin=at_top(3, 0),
        )
    )
    # Muro X1: «Draw Walls» de un nodo al otro; el shell se extiende tras el cursor.
    scene.play(point_to(*span[0]))
    for s in model.stories:
        x1 = s.walls["X1"]
        a0, _, _, a1 = x1.points
        x1.drawable.points([iso(*a0), iso(*a0), iso(*a1), iso(*a1)])
    scene.play(
        [
            point_to(*span[1], 0.7, Easing.LINEAR),
            *[
                s.walls["X1"]
                .drawable.animate.points([iso(*p) for p in s.walls["X1"].points])
                .duration(0.7)
                .easing(Easing.LINEAR)
                for s in model.stories
            ],
        ]
    )
    scene.play(
        stagger(
            *[
                shape.drawable.animate.fade_in().duration(0.3)
                for s in model.stories
                for name, shape in s.walls.items()
                if name != "X1"
            ],
            total=1.1,
            origin=at_top(3, 0),
        )
    )
    # Losas: rectángulo de esquina a esquina; el vacío de escalera ya está en la losa.
    band = (
        scene.geometry.polygon(
            [at_top(0, 0), at_top(WIDTH, 0), at_top(WIDTH, DEPTH), at_top(0, DEPTH)]
        )
        .no_fill()
        .stroke(INK_SOFT, 0.012)
        .z_index(OVERLAY + 13)
        .hidden()
    )
    band.points([at_top(0, 0)] * 4)
    scene.play(point_to(0, 0))
    scene.play(
        [
            _click(scene, *at_top(0, 0)),
            band.animate.fade_in().duration(0.05),
            band.animate.points(
                [at_top(0, 0), at_top(WIDTH, 0), at_top(WIDTH, DEPTH), at_top(0, DEPTH)]
            )
            .duration(0.9)
            .easing(Easing.SMOOTH),
            point_to(WIDTH, DEPTH, 0.9),
        ]
    )
    scene.play(
        [
            band.animate.fade_out().duration(0.3),
            pointer.animate.fade_out().duration(0.3),
            stagger(
                *[
                    parallel(
                        s.slab.drawable.animate.fade_in().duration(0.4),
                        s.void.drawable.animate.fade_in().duration(0.4),
                    )
                    for s in model.stories
                ],
                each=0.15,
            ),
        ]
    )
    scene.stop("mct-dibujo")

    # 5 · Se ocultan las losas, aparece la malla y la cámara entra a un nudo.
    mesh = [
        part.drawable
        for s in model.stories
        for parts in s.mesh.values()
        for part in parts
    ]
    scene.play(
        [
            *step(4),
            *[
                s.slab.drawable.animate.opacity(0.16).duration(0.6)
                for s in model.stories
            ],
        ]
    )
    scene.play(stagger(*[m.animate.create().duration(0.5) for m in mesh], total=1.6))
    junction = (3.0, 0.0)
    story2 = model.stories[1]
    focus = iso(*junction, (story2.z0 + story2.z1) / 2)
    detail = _junction_detail(scene, model, story2, junction)
    scene.play(
        [
            *[lab.animate.fade_out().duration(0.4) for lab in level_labels],
            scene.camera.animate.to(
                scene.camera.state_2d((focus[0] - 0.45, focus[1]), 3.2)
            )
            .duration(1.3)
            .easing(Easing.ease_in_out(EasingCurve.CUBIC)),
            stagger(
                *[d.animate.fade_in().duration(0.3) for d in detail], each=0.02
            ).delay(1.0),
        ]
    )
    scene.stop("mct-malla")
    scene.play(
        [
            *[d.animate.fade_out().duration(0.3) for d in detail],
            scene.camera.animate.reset()
            .duration(1.1)
            .easing(Easing.ease_in_out(EasingCurve.CUBIC))
            .delay(0.2),
            *[lab.animate.fade_in().duration(0.4).delay(0.9) for lab in level_labels],
        ]
    )

    # 6 · Diafragma rígido: cada losa liga sus nudos a un centro D1.
    centers: list[Drawable] = []
    spokes: list[Drawable] = []
    waves: list[Composition] = []
    for s in model.stories:
        c = iso(*DIAPHRAGM_CENTER, s.z1)
        lines = [
            scene.geometry.dashed_line(
                *c, *iso(*node, s.z1), dash_length=0.035, gap_length=0.03
            )
            .stroke(INK_SOFT, 0.007)
            .z_index(s.overlay)
            .hidden()
            for node in s.columns
        ]
        dot = model.ride(
            scene.geometry.circle(0.04)
            .fill(INK)
            .stroke(CARD, 0.01)
            .move_to(*c)
            .z_index(OVERLAY + 10)
            .hidden(),
            s.z1,
        )
        spokes += lines
        centers.append(dot)
        # La losa se enciende mientras sus nudos quedan ligados al centro.
        waves.append(
            parallel(
                dot.animate.grow_from_center().duration(0.25),
                stagger(
                    *[ln.animate.create().duration(0.45) for ln in lines], each=0.006
                ),
                sequence(
                    s.slab.drawable.animate.opacity(0.55).duration(0.3),
                    s.slab.drawable.animate.opacity(0.16).duration(0.5).delay(0.3),
                ),
            )
        )
    d1 = model.ride(
        t(
            scene,
            "D1",
            iso(*DIAPHRAGM_CENTER, top)[0] - 0.08,
            iso(*DIAPHRAGM_CENTER, top)[1] - 0.05,
            font=MONO,
            size=0.11,
            weight=700,
            color=INK,
            anchor=Anchor.TOP_RIGHT,
        )
        .z_index(OVERLAY + 11)
        .hidden(),
        top,
    )
    scene.play(
        [
            *step(5),
            stagger(*waves, each=0.3),
            d1.animate.fade_in().duration(0.3).delay(1.0),
        ]
    )
    scene.play([ln.animate.opacity(0.7).duration(0.4) for ln in spokes])
    scene.stop("mct-diafragma")

    # 7 · Etiquetas Pier: se elige X1 en un piso y la etiqueta llega a los cuatro.
    x1_label_z = [(s.z0 + s.z1) / 2 for s in model.stories]
    x1_labels = [
        model.ride(
            t(
                scene,
                "X1",
                *iso(1.5, 0, z),
                font=MONO,
                size=0.11,
                weight=700,
                color=BRICK_DEEP,
                anchor=Anchor.CENTER,
            )
            .z_index(OVERLAY + 11)
            .hidden(),
            z,
        )
        for z in x1_label_z
    ]
    tags: list[Drawable] = []
    for line in model.lines:
        if line.name == "X1":
            continue
        x, y = iso(*line.middle, top)
        tags.append(
            model.ride(
                t(
                    scene,
                    line.label,
                    x,
                    y + 0.03,
                    font=MONO,
                    size=0.1,
                    weight=700,
                    color=BRICK_DEEP if line.direction == "X" else STEEL,
                    anchor=Anchor.BOTTOM,
                )
                .z_index(OVERLAY + 11)
                .hidden(),
                top,
            )
        )
    pick = iso(1.5, 0, (model.stories[-1].z0 + top) / 2)
    pointer.move_to(*at_top(5.0, 2.0), Anchor.TOP_LEFT)
    x1_walls = [s.walls["X1"].drawable for s in model.stories]
    scene.play([*step(6), pointer.animate.fade_in().duration(0.3)])
    scene.play(
        pointer.animate.move_to(*pick, Anchor.TOP_LEFT)
        .duration(0.5)
        .easing(Easing.SMOOTH)
    )
    scene.play(
        [
            _click(scene, *pick),
            *[w.animate.fill(SELECTED).duration(0.25) for w in x1_walls],
        ]
    )
    scene.play(
        [
            stagger(
                *[
                    lab.animate.fade_in_from(Direction.DOWN, 0.05).duration(0.3)
                    for lab in reversed(x1_labels)
                ],
                each=0.12,
            ),
            *[w.animate.fill(WALL_X).duration(0.4).delay(0.6) for w in x1_walls],
            pointer.animate.fade_out().duration(0.3).delay(0.6),
        ]
    )
    scene.play(
        stagger(
            *[tag.animate.fade_in().duration(0.25) for tag in tags],
            total=1.0,
            origin=pick,
        )
    )
    scene.stop("mct-pier")

    # 8 · Cargas sobre las losas y masa sísmica concentrada en cada diafragma.
    arrows = [
        model.ride(
            scene.geometry.arrow(
                *iso(x, y, top + 1.5),
                *iso(x, y, top),
                head_length=0.07,
                head_width=0.07,
                body_width=0.012,
            )
            .fill(INK_SOFT)
            .no_stroke()
            .z_index(OVERLAY + 12)
            .hidden(),
            top,
        )
        for x, y in ROOF_ARROWS
    ]
    roof_cm, roof_cv = LOAD_SETS["Azotea"]
    typical_cm, typical_cv = LOAD_SETS["Piso típico"]
    loads = [
        t(
            scene,
            text,
            -2.55,
            y,
            font=MONO,
            size=0.11,
            color=color,
            anchor=Anchor.LEFT,
        ).hidden()
        for text, y, color in (
            (f"Azotea     CM {roof_cm:.2f} · CV {roof_cv:.2f} tonf/m²", 2.5, INK),
            (
                f"Pisos 1–3  CM {typical_cm:.2f} · CV {typical_cv:.2f} tonf/m²",
                2.27,
                INK_SOFT,
            ),
        )
    ]
    weights = WEIGHT_BY_FLOOR["MCT"]
    masses: list[Drawable] = []
    mass_labels: list[Drawable] = []
    for s, w in zip(model.stories, weights, strict=True):
        cx, cy = iso(*DIAPHRAGM_CENTER, s.z1)
        r = 0.075 * math.sqrt(w / max(weights))
        masses.append(
            model.ride(
                scene.geometry.circle(r)
                .fill(BRICK)
                .stroke(CARD, 0.012)
                .move_to(cx, cy)
                .z_index(OVERLAY + 12)
                .hidden(),
                s.z1,
            )
        )
        mass_labels.append(
            model.ride(
                pill(
                    scene,
                    f"{w:.1f} tonf",
                    cx + 0.14,
                    cy,
                    size=0.1,
                    pad=(0.06, 0.025),
                    color=INK,
                    border=RULE,
                    anchor=Anchor.LEFT,
                ).z_index(OVERLAY + 12),
                s.z1,
            )
        )
    scene.play(
        [
            *step(7),
            *[ln.animate.fade_out().duration(0.4) for ln in spokes],
            stagger(*[a.animate.grow_arrow().duration(0.4) for a in arrows], each=0.05),
            stagger(
                *[x.animate.fade_in().duration(0.3) for x in loads], each=0.15
            ).delay(0.3),
        ]
    )
    scene.play(
        stagger(
            *[
                parallel(
                    m.animate.grow_from_center().duration(0.3),
                    lab.animate.fade_in_from(Direction.LEFT, 0.05).duration(0.3),
                )
                for m, lab in zip(masses, mass_labels, strict=True)
            ],
            each=0.15,
        )
    )
    # Con el modelo completo, el análisis modal: el modo 3 es la traslación en Y.
    modal = [
        label(scene, "Análisis modal", -7.3, -2.55, color=MUTED, size=0.13),
        t(
            scene,
            f"Modo {MODE_Y['modo']} · T = {MODE_Y['T']:.3f} s",
            -7.3,
            -2.83,
            font=MONO,
            size=0.13,
            color=INK,
        ),
        t(
            scene,
            f"traslación en Y · {MODE_Y['UY'] * 100:.0f} % de la masa",
            -7.3,
            -3.08,
            size=0.15,
            color=INK_SOFT,
        ),
        t(scene, "deformada exagerada", -7.3, -3.32, font=MONO, size=0.1, color=MUTED),
    ]
    scene.play(
        [
            *steps.restore(),
            stagger(*[m.animate.fade_in().duration(0.3) for m in modal], each=0.08),
        ]
    )
    source(
        scene,
        "Tesis · §5.3.1, pp. 58–67 (Figuras 23–34, Tabla 24); Figura 21, p. 47; Figura 40, p. 74; "
        "Tabla 28, p. 77 · modelo esquemático del MCT",
    )
    scene.stop(
        "mct-analisis",
        loop=sequence(
            parallel(*model.sway(SWAY, 0.6)),
            parallel(*model.sway(-SWAY, 1.2)),
            parallel(*model.sway(0.0, 0.6)),
        ),
    )


def _junction_detail(
    scene: Scene, model: EtabsModel, story: Story, node: tuple[float, float]
) -> list[Drawable]:
    """Lo que se ve al acercarse a un nudo: nodos de la malla, frames y brazo rígido.

    Todo mide lo que debe medir a 3.2 aumentos; fuera del acercamiento estaría oculto.
    """
    iso = model.iso
    z0, z1 = story.z0, story.z1
    x_node, _ = node
    parts: list[Drawable] = []
    nz = math.ceil((z1 - z0) / MESH_STEP - 1e-6)
    shared: list[tuple[float, float, float]] = []
    for name in ("X1", "Y3"):
        line = next(ln for ln in model.lines if ln.name == name)
        (ax, ay), (bx, by) = line.a, line.b
        nu = math.ceil(math.hypot(bx - ax, by - ay) / MESH_STEP - 1e-6)
        for i in range(nu + 1):
            for j in range(nz + 1):
                p = (
                    ax + (bx - ax) * i / nu,
                    ay + (by - ay) * i / nu,
                    z0 + (z1 - z0) * j / nz,
                )
                on_frame = (
                    j in (0, nz) or abs(p[0] - x_node) < 1e-6 and abs(p[1]) < 1e-6
                )
                if on_frame:
                    shared.append(p)
                    continue
                parts.append(
                    scene.geometry.circle(0.0065)
                    .fill(INK_SOFT)
                    .no_stroke()
                    .move_to(*iso(*p))
                    .z_index(OVERLAY + 8)
                    .hidden()
                )
    parts += [
        scene.geometry.circle(0.009)
        .fill(BRICK)
        .no_stroke()
        .move_to(*iso(*p))
        .z_index(OVERLAY + 8)
        .hidden()
        for p in shared
    ]
    # Brazo rígido al extremo de la viga X1, en la cara de la columna (End Length Offset).
    parts.append(
        scene.geometry.line(*iso(x_node - 0.3, 0, z1), *iso(x_node, 0, z1))
        .stroke(INK, 0.014)
        .z_index(OVERLAY + 8)
        .hidden()
    )
    rows = nz  # filas de la malla en el piso
    notes = (
        ("Brazo rígido en la cara de la columna", (x_node - 0.15, 0, z1)),
        ("Shell M13 · malla de 0.50 m", (1.25, 0, (z0 + z1) / 2 + 0.2)),
        ("Nodos compartidos: malla y frames", (x_node, 0, z0 + 4 * (z1 - z0) / rows)),
        ("Frame · columna de confinamiento", (x_node, 0, z0 + 0.25)),
    )
    for i, (text, target) in enumerate(notes):
        tx, ty = iso(*target)
        y = 0.55 - i * 0.3
        parts.append(
            t(
                scene,
                text,
                -7.18,
                y,
                font=MONO,
                size=0.052,
                color=INK,
                anchor=Anchor.LEFT,
            )
            .z_index(OVERLAY + 9)
            .hidden()
        )
        parts.append(
            scene.geometry.line(-6.0, y, tx, ty)
            .stroke(INK_SOFT, 0.004)
            .z_index(OVERLAY + 9)
            .hidden()
        )
        parts.append(
            scene.geometry.circle(0.011)
            .no_fill()
            .stroke(INK, 0.004)
            .move_to(tx, ty)
            .z_index(OVERLAY + 9)
            .hidden()
        )
    return parts


# Pórticos planos (MSTA): cada muro se prepara en CAD y en la hoja antes de dibujarse.
FRAME_STEPS: Phases = (
    (
        "Preparar",
        "CAD · Excel",
        (
            (
                "Sección transformada",
                "Columnas × n = Ec/Em = 6.1; muros transversales como alas",
            ),
            (
                "Centroide y propiedades",
                "cg, A1, A2 e I de cada muro con la rutina SECTRANS",
            ),
            (
                "Áreas tributarias",
                "Método del sobre: CM y CV de la losa para cada muro",
            ),
        ),
    ),
    (
        "Dibujar",
        "Draw",
        (
            ("Barras en el centroide", "Un frame por muro, empotrado en la base"),
            ("Brazos rígidos y dinteles", "Brazo hasta el borde del muro; vigas T y L"),
        ),
    ),
    (
        "Asignar",
        "Assign",
        (
            ("Secciones General", "Rigidez solo en su plano; peso × Ac/A1"),
            ("Cargas puntuales", "La carga tributaria de cada muro, en cada piso"),
            ("Diafragma rígido", "D1 une los pórticos planos en cada nivel"),
        ),
    ),
)
WALL_T = THICKNESS
SEC_K = 1.45  # unidades de escena por metro en el detalle de X4
SEC_O = (-5.6, -1.25)  # cara exterior de la columna izquierda, sobre el eje del muro
COL_LEFT, COL_RIGHT = 0.25, 0.30  # columnas de los extremos, a lo largo del muro
FLANGE = 2.61  # ala de Y4 en la sección transformada (Figura 35)
PLAN_CENTER, PLAN_WIDTH = (-3.2, 0.45), 7.0
TRIBUTARY = Color.from_hex("#EBC4B2")  # área tributaria de X4, terracota aclarada
CONSOLE_LINES = (
    "Comando: ST  (SECTRANS)",
    "f'c = 175 · f'm = 65  →  n = Ec/Em = 6.105",
    "[1/3] Muro principal: X4",
    "[2/3] Columnas de confinamiento: espesor × n",
    "[3/3] Muros ortogonales: Y4 entra como ala",
    "Unión booleana y propiedades de la región",
    "Centroide marcado en la capa CG_MUROS",
)
CONSOLE_Y = (-2.93, -3.23)  # renglón anterior y renglón activo
# Losas a ambos lados de X4 (m): arriba entre los ejes C y D, abajo entre A y C.
SLAB_ABOVE = (3.0, 5.0, 7.0, 8.0)
SLAB_BELOW = (3.0, 0.0, 7.0, 5.0)
FRAME_WINDOW = (
    "Material  ALB65KGF/CM2    Shape  General",
    f"A1 = {X4['A1']:.3f} m²   As2 = {X4['A2']:.3f} m²   I33 = {X4['I3']:.3f} m⁴",
    "Fuera del plano: As3, I22 y J × 0.0001",
    f"Masa y peso × {WEIGHT_FACTOR_X4:.3f}  (= As2 / A1)",
)


def _rect(x0: float, y0: float, x1: float, y1: float) -> list[tuple[float, float]]:
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def _envelope(
    x0: float, y0: float, x1: float, y1: float
) -> tuple[list[tuple[tuple[float, float], tuple[float, float]]], tuple[float, float]]:
    """Líneas a 45° del método del sobre en un paño rectangular, y su cumbrera."""
    half = min(x1 - x0, y1 - y0) / 2
    if x1 - x0 >= y1 - y0:
        ridge = ((x0 + half, y0 + half), (x1 - half, y0 + half))
        corners = [((x0, y0), ridge[0]), ((x0, y1), ridge[0])]
        corners += [((x1, y0), ridge[1]), ((x1, y1), ridge[1])]
    else:
        ridge = ((x0 + half, y0 + half), (x0 + half, y1 - half))
        corners = [((x0, y0), ridge[0]), ((x1, y0), ridge[0])]
        corners += [((x0, y1), ridge[1]), ((x1, y1), ridge[1])]
    return [*corners, ridge], ridge[0]


def _cg_symbol(scene: Scene, x: float, y: float, r: float) -> Drawable:
    """Símbolo de centro de gravedad: círculo con dos cuartos llenos."""
    return scene.geometry.group(
        [
            scene.geometry.circle(r).fill(CARD).stroke(INK, r * 0.16).move_to(x, y),
            scene.geometry.sector(x, y, r, 0, math.pi / 2).fill(INK).no_stroke(),
            scene.geometry.sector(x, y, r, math.pi, math.pi / 2).fill(INK).no_stroke(),
        ]
    )


@dataclass
class Ground:
    """Planta hecha de polígonos con vértices en metros: puede inclinarse a la isométrica."""

    shapes: list[tuple[Drawable, list[tuple[float, float]]]]
    walls: list[Drawable]
    grid: list[Drawable]
    bubbles: list[Drawable]

    def tilt(self, iso: Iso, duration: float, delay: float = 0.0) -> list[Playable]:
        """Lleva cada vértice de la planta a su lugar en la base de la isométrica."""
        return [
            d.animate.points([iso(x, y, 0) for x, y in pts])
            .duration(duration)
            .easing(Easing.ease_in_out(EasingCurve.CUBIC))
            .delay(delay)
            for d, pts in self.shapes
        ]


def _ground(
    scene: Scene, to_scene: Callable[[float, float], tuple[float, float]], scale: float
) -> Ground:
    """Losa, muros y grillas de la planta, en polígonos y polilíneas en metros."""
    shapes: list[tuple[Drawable, list[tuple[float, float]]]] = []

    def add(d: Drawable, pts: list[tuple[float, float]]) -> Drawable:
        shapes.append((d, pts))
        return d

    x0, y0, x1, y1 = STAIR
    slab_pts: list[tuple[float, float]] = [
        (0, 0),
        (x0, 0),
        (x0, y0),
        (x0, y1),
        (x1, y1),
        (x1, y0),
        (x0, y0),
        (x0, 0),
        (WIDTH, 0),
        (WIDTH, DEPTH),
        (0, DEPTH),
    ]
    add(
        scene.geometry.polygon([to_scene(*q) for q in slab_pts])
        .fill("#EFEBE3")
        .no_stroke()
        .z_index(1)
        .hidden(),
        slab_pts,
    )
    for pts in (_rect(0, 0, WIDTH, DEPTH), _rect(x0, y0, x1, y1)):
        add(
            scene.geometry.polygon([to_scene(*q) for q in pts])
            .no_fill()
            .stroke(RULE, 0.014)
            .z_index(2)
            .hidden(),
            pts,
        )
    grid: list[Drawable] = []
    bubbles: list[Drawable] = []
    reach = 1.3  # m: las burbujas quedan fuera de la planta
    for name, gx in AXIS_X.items():
        pts = [(gx, -0.3), (gx, DEPTH + reach - 0.4)]
        line = scene.geometry.polyline([to_scene(*q) for q in pts]).no_fill()
        grid.append(add(line.stroke(MUTED, 0.008).z_index(2).hidden(), pts))
        bubbles.append(_grid_bubble(scene, name, *to_scene(gx, DEPTH + reach)))
    for name, gy in AXIS_Y.items():
        pts = [(-reach + 0.4, gy), (WIDTH + 0.3, gy)]
        line = scene.geometry.polyline([to_scene(*q) for q in pts]).no_fill()
        grid.append(add(line.stroke(MUTED, 0.008).z_index(2).hidden(), pts))
        bubbles.append(_grid_bubble(scene, name, *to_scene(-reach, gy)))
    half = 0.07 / scale / 2  # medio espesor dibujado, en metros
    walls: list[Drawable] = []
    for wall in wall_lines():
        (ax, ay), (bx, by) = wall.a, wall.b
        if wall.direction == "X":
            pts = _rect(ax, ay - half, bx, ay + half)
        else:
            pts = _rect(ax - half, ay, ax + half, by)
        color = (
            CONCRETE if wall.concrete else (BRICK if wall.direction == "X" else STEEL)
        )
        shape = scene.geometry.polygon([to_scene(*q) for q in pts]).fill(color)
        walls.append(add(shape.no_stroke().z_index(4).hidden(), pts))
    return Ground(shapes, walls, grid, bubbles)


def _grid_bubble(scene: Scene, name: str, x: float, y: float) -> Drawable:
    ring = (
        scene.geometry.circle(0.14).fill("#F9F7F2").stroke(MUTED, 0.012).move_to(x, y)
    )
    text = t(
        scene, name, x, y, font=MONO, size=0.12, color=INK_SOFT, anchor=Anchor.CENTER
    )
    return scene.geometry.group([ring, text]).z_index(3).hidden()


def plane_frames(scene: Scene) -> None:
    header(scene, KICKER, "Pórticos planos: cada muro se calcula antes de modelarlo")
    steps = _steps_panel(scene, FRAME_STEPS)
    step = steps.enter
    n = MODULAR_RATIO
    length = X4["L"]
    half = WALL_T / 2
    stretched = half * n

    def sc(x: float, y: float) -> tuple[float, float]:
        return SEC_O[0] + x * SEC_K, SEC_O[1] + y * SEC_K

    def shape(points: list[tuple[float, float]], fill: Color, edge: Color) -> Drawable:
        return (
            scene.geometry.polygon([sc(*p) for p in points])
            .fill(fill)
            .stroke(edge, 0.012)
            .hidden()
        )

    # 1 · La sección real de X4: muro, dos columnas de concreto y el ala de Y4.
    web = shape(_rect(COL_LEFT, -half, length - COL_RIGHT, half), BRICK_SOFT, BRICK)
    flange = shape(_rect(0, half, WALL_T, FLANGE), BRICK_SOFT, BRICK)
    left_col = shape(_rect(0, -half, COL_LEFT, half), CONCRETE_SOFT, CONCRETE)
    right_col = shape(
        _rect(length - COL_RIGHT, -half, length, half), CONCRETE_SOFT, CONCRETE
    )
    pieces = [flange, web, left_col, right_col]
    names = [
        t(scene, text, *sc(x, y), size=0.15, color=color, anchor=anchor).hidden()
        for text, x, y, color, anchor in (
            ("muro X4 · albañilería", 1.55, -0.35, BRICK_DEEP, Anchor.TOP),
            ("columnas de concreto", length, -0.35, CONCRETE, Anchor.TOP_RIGHT),
            ("muro Y4 transversal", WALL_T + 0.12, 1.9, BRICK_DEEP, Anchor.LEFT),
        )
    ]
    console_box = (
        scene.geometry.rect(7.85, 0.7)
        .fill(CARD)
        .stroke(RULE, 0.014)
        .move_to(-3.325, -3.08)
        .hidden()
    )
    console = [
        t(
            scene,
            line,
            -7.05,
            CONSOLE_Y[1],
            font=MONO,
            size=0.12,
            color=INK,
            anchor=Anchor.LEFT,
        ).hidden()
        for line in CONSOLE_LINES
    ]
    shown: list[int] = []  # renglones visibles: anterior y activo

    def say(k: int) -> list[Playable]:
        """Escribe la línea k en el renglón activo; la anterior sube y se atenúa."""
        anims: list[Playable] = []
        if len(shown) == 2:
            anims.append(console[shown.pop(0)].animate.fade_out().duration(0.2))
        if shown:
            line = console[shown[0]]
            anims.append(
                line.animate.shift_by(0, CONSOLE_Y[0] - CONSOLE_Y[1]).duration(0.25)
            )
            anims.append(line.animate.opacity(0.45).duration(0.25))
        shown.append(k)
        anims.append(
            console[k]
            .animate.typewriter(cps=55, cursor="▍", keep_cursor=False)
            .duration(len(CONSOLE_LINES[k]) / 55)
            .delay(0.2)
        )
        return anims

    scene.play(
        [
            *step(0),
            stagger(*[p.animate.fade_in().duration(0.35) for p in pieces], each=0.08),
            stagger(
                *[x.animate.fade_in().duration(0.3) for x in names], each=0.1
            ).delay(0.3),
            console_box.animate.fade_in().duration(0.3),
            sequence(*[parallel(*say(k)) for k in (0, 1)]).delay(0.3),
        ]
    )
    # El ingeniero elige las piezas y la rutina transforma las columnas.
    scene.play(
        [
            *say(2),
            sequence(
                web.animate.fill(SELECTED).duration(0.2),
                web.animate.fill(BRICK_SOFT).duration(0.4).delay(0.3),
            ),
        ]
    )
    columns_dim = dimension(
        scene,
        sc(length, -stretched),
        sc(length, stretched),
        f"{2 * stretched:.2f} m",
        side="right",
        offset=0.3,
    )
    times_n = t(
        scene,
        f"× n = {n:.1f}",
        *sc(length - COL_RIGHT / 2, stretched + 0.12),
        font=MONO,
        size=0.14,
        weight=700,
        color=INK,
        anchor=Anchor.BOTTOM,
    ).hidden()
    scene.play(
        [
            *say(3),
            names[1].animate.fade_out().duration(0.2),
            *[
                col.animate.points(
                    [sc(*p) for p in _rect(x0, -stretched, x1, stretched)]
                )
                .duration(0.8)
                .easing(Easing.SMOOTH)
                .delay(0.4)
                for col, (x0, x1) in (
                    (left_col, (0, COL_LEFT)),
                    (right_col, (length - COL_RIGHT, length)),
                )
            ],
            columns_dim.animate.fade_in().duration(0.3).delay(1.1),
            times_n.animate.fade_in().duration(0.3).delay(1.1),
        ]
    )
    scene.play(
        [
            *say(4),
            sequence(
                flange.animate.fill(SELECTED).duration(0.2),
                flange.animate.fill(BRICK_SOFT).duration(0.4).delay(0.3),
            ),
        ]
    )

    # 2 · La unión de las piezas da la sección transformada, su centroide y propiedades.
    outline = [
        (0, -stretched),
        (COL_LEFT, -stretched),
        (COL_LEFT, -half),
        (length - COL_RIGHT, -half),
        (length - COL_RIGHT, -stretched),
        (length, -stretched),
        (length, stretched),
        (length - COL_RIGHT, stretched),
        (length - COL_RIGHT, half),
        (COL_LEFT, half),
        (COL_LEFT, stretched),
        (WALL_T, stretched),
        (WALL_T, FLANGE),
        (0, FLANGE),
    ]
    region = shape(outline, STEEL_SOFT, STEEL)
    cg = X4["cg"]
    symbol = _cg_symbol(scene, *sc(cg, 0), 0.11).z_index(OVERLAY).hidden()
    cg_dim = dimension(
        scene,
        sc(0, -stretched),
        sc(cg, -stretched),
        f"cg = {cg:.3f} m",
        side="below",
        offset=0.3,
    )
    props = [
        t(
            scene,
            text,
            *sc(0.55, y),
            font=MONO,
            size=0.15,
            color=INK,
            anchor=Anchor.LEFT,
        ).hidden()
        for text, y in (
            (f"A1 = {X4['A1']:.3f} m²   sección transformada", 2.15),
            (f"A2 = {X4['A2']:.3f} m²   corte: L · t", 1.85),
            (f"I3 = {X4['I3']:.3f} m⁴   flexión en su plano", 1.55),
        )
    ]

    def typed(text: Text, cps: float = 60) -> Anim:
        return text.animate.typewriter(cps=cps, cursor="▍", keep_cursor=False)

    scene.play(
        [
            *step(1),
            *say(5),
            region.animate.fade_in().duration(0.5).delay(0.3),
            *[p.animate.fade_out().duration(0.4).delay(0.5) for p in pieces],
            *[
                x.animate.fade_out().duration(0.3)
                for x in (names[0], names[2], columns_dim, times_n)
            ],
        ]
    )
    scene.play(
        [
            *say(6),
            symbol.animate.grow_from_center().duration(0.35),
            cg_dim.animate.fade_in().duration(0.4).delay(0.2),
            sequence(*[typed(p).duration(0.6) for p in props]).delay(0.4),
        ]
    )
    scene.wait(0.2)
    scene.stop("pp-seccion")

    # 3 · La sección vuelve a su lugar en la planta; ahí se reparte la losa (método del sobre).
    plan_scale = PLAN_WIDTH / WIDTH
    plan_origin = (
        PLAN_CENTER[0] - WIDTH * plan_scale / 2,
        PLAN_CENTER[1] - DEPTH * plan_scale / 2,
    )

    def pl(x: float, y: float) -> tuple[float, float]:
        return plan_origin[0] + x * plan_scale, plan_origin[1] + y * plan_scale

    plan = _ground(scene, pl, plan_scale)

    bbox_center = ((0 + length) / 2, (-stretched + FLANGE) / 2)
    land = pl(X4_START + bbox_center[0], 5.0 + bbox_center[1])
    shrink = plan_scale / SEC_K
    dots = [
        scene.geometry.circle(0.045)
        .fill(STEEL)
        .stroke(CARD, 0.01)
        .move_to(*pl(x, y))
        .z_index(6)
        .hidden()
        for _, x, y in BARS
    ]
    x4_dot = next(d for d, (name, _, _) in zip(dots, BARS, strict=True) if name == "X4")
    scene.play(
        [
            *step(2),
            *[
                x.animate.fade_out().duration(0.3)
                for x in (*props, cg_dim, console_box, *[console[j] for j in shown])
            ],
            stagger(*[g.animate.create().duration(0.4) for g in plan.grid], each=0.02),
            stagger(
                *[b.animate.fade_in().duration(0.2) for b in plan.bubbles], each=0.015
            ),
            *[d.animate.fade_in().duration(0.4) for d, _ in plan.shapes[:3]],
            *[w.animate.fade_in().duration(0.4).delay(0.3) for w in plan.walls],
            region.animate.scale_to(shrink)
            .duration(1.0)
            .easing(Easing.SMOOTH)
            .delay(0.2),
            region.animate.move_to(*land)
            .duration(1.0)
            .easing(Easing.SMOOTH)
            .delay(0.2),
            symbol.animate.move_to(*pl(X4_START + cg, 5.0))
            .duration(1.0)
            .easing(Easing.SMOOTH)
            .delay(0.2),
            symbol.animate.scale_to(0.45)
            .duration(1.0)
            .easing(Easing.SMOOTH)
            .delay(0.2),
        ]
    )
    scene.play(
        [
            region.animate.fade_out().duration(0.4),
            symbol.animate.fade_out().duration(0.3).delay(0.3),
            x4_dot.animate.grow_from_center().duration(0.3).delay(0.3),
            stagger(
                *[
                    d.animate.grow_from_center().duration(0.25)
                    for d in dots
                    if d is not x4_dot
                ],
                total=0.8,
            ).delay(0.5),
        ]
    )
    # Las líneas a 45° parten cada paño; X4 recibe un trapecio arriba y un triángulo abajo.
    envelope_lines: list[Drawable] = []
    for panel_box in (SLAB_ABOVE, SLAB_BELOW):
        lines, _ = _envelope(*panel_box)
        envelope_lines += [
            scene.geometry.line(*pl(*a), *pl(*b))
            .stroke(INK_SOFT, 0.012)
            .z_index(5)
            .hidden()
            for a, b in lines
        ]
    ax0, ay0, ax1, ay1 = SLAB_ABOVE
    bx0, _, bx1, by1 = SLAB_BELOW
    above_half = (ay1 - ay0) / 2
    below_half = (bx1 - bx0) / 2
    shares = [
        scene.geometry.polygon([pl(*p) for p in pts])
        .fill(TRIBUTARY)
        .no_stroke()
        .z_index(3)
        .hidden()
        for pts in (
            [
                (ax0, ay0),
                (ax1, ay0),
                (ax1 - above_half, ay0 + above_half),
                (ax0 + above_half, ay0 + above_half),
            ],
            [(bx0, by1), (bx1, by1), (bx0 + below_half, by1 - below_half)],
        )
    ]
    upper, lower = X4_TRIBUTARY
    share_labels = [
        t(
            scene,
            f"{area:.2f} m²",
            *pl(x, y),
            font=MONO,
            size=0.11,
            weight=700,
            color=BRICK_DEEP,
            anchor=Anchor.CENTER,
        )
        .z_index(7)
        .hidden()
        for area, x, y in ((upper, 5.0, 5.55), (lower, 5.0, 4.3))
    ]
    area = tributary_x4()
    sums = [
        t(
            scene, text, -6.75, y, font=MONO, size=0.14, color=color, anchor=Anchor.LEFT
        ).hidden()
        for text, y, color in (
            (f"X4 · A = {upper:.2f} + {lower:.2f} = {area:.2f} m²", -1.65, INK),
            (
                (
                    f"CM = {area:.2f} × {SLAB_DEAD:.3f} = {area * SLAB_DEAD:.2f} tonf    "
                    f"CV = {area:.2f} × {SLAB_LIVE:.2f} = {area * SLAB_LIVE:.2f} tonf"
                ),
                -1.98,
                INK_SOFT,
            ),
        )
    ]
    scene.play(
        [
            stagger(
                *[ln.animate.create().duration(0.5) for ln in envelope_lines], each=0.05
            ),
            stagger(
                *[s.animate.fade_in().duration(0.4) for s in shares], each=0.2
            ).delay(0.6),
            stagger(
                *[x.animate.fade_in().duration(0.3) for x in share_labels], each=0.2
            ).delay(0.8),
            sequence(*[typed(x) for x in sums]).delay(1.0),
        ]
    )
    scene.wait(0.2)
    scene.stop("pp-tributarias")

    # 4 · La planta se inclina hasta la isométrica y desde cada centroide sube una barra.
    iso = MODEL_ISO
    top = STORY_HEIGHT * STORY_COUNT
    levels = [STORY_HEIGHT * (k + 1) for k in range(STORY_COUNT)]
    bars = [
        scene.geometry.polyline([iso(x, y, 0), iso(x, y, top)])
        .no_fill()
        .stroke(STEEL, 0.022)
        .z_index(20)
        .hidden()
        for _, x, y in BARS
    ]
    level_labels = [
        t(
            scene,
            f"Story{k + 1}  {z:5.2f}",
            iso(0, 0, z)[0] - 0.42,
            iso(0, 0, z)[1],
            font=MONO,
            size=0.11,
            color=INK_SOFT,
            anchor=Anchor.RIGHT,
        ).hidden()
        for k, z in enumerate(levels)
    ]
    scene.play(
        [
            *step(3),
            *[
                x.animate.fade_out().duration(0.3)
                for x in (*envelope_lines, *shares, *share_labels, *sums, *plan.bubbles)
            ],
            *plan.tilt(iso, 1.4, 0.3),
            *[
                d.animate.move_to(*iso(x, y, 0))
                .duration(1.4)
                .easing(Easing.ease_in_out(EasingCurve.CUBIC))
                .delay(0.3)
                for d, (_, x, y) in zip(dots, BARS, strict=True)
            ],
            *[w.animate.opacity(0.45).duration(0.6).delay(1.2) for w in plan.walls],
        ]
    )
    scene.play(
        [
            stagger(
                *[b.animate.create().duration(0.7) for b in bars],
                total=1.2,
                origin="center",
            ),
            stagger(
                *[x.animate.fade_in().duration(0.3) for x in level_labels], each=0.1
            ).delay(0.4),
        ]
    )

    # 5 · En cada nivel: brazos rígidos desde el centroide y dinteles entre sus extremos.
    bar_points = {(round(x, 3), round(y, 3)) for _, x, y in BARS}
    by_level: list[tuple[list[Drawable], list[Drawable]]] = []
    frame_a: list[Drawable] = [
        b for b, (_, _, y) in zip(bars, BARS, strict=True) if abs(y) < 1e-6
    ]
    for z in levels:
        arms: list[Drawable] = []
        lintels: list[Drawable] = []
        for kind, a, b in BEAMS:
            if kind == "rigid" and (round(b[0], 3), round(b[1], 3)) in bar_points:
                a, b = b, a  # el brazo nace en la barra
            line = (
                scene.geometry.polyline([iso(*a, z), iso(*b, z)])
                .no_fill()
                .stroke(
                    INK if kind == "rigid" else STEEL,
                    0.034 if kind == "rigid" else 0.012,
                )
                .z_index(22 if kind == "rigid" else 21)
                .hidden()
            )
            (arms if kind == "rigid" else lintels).append(line)
            if abs(a[1]) < 1e-6 and abs(b[1]) < 1e-6:
                frame_a.append(line)
        by_level.append((arms, lintels))
    scene.play(
        [
            *step(4),
            stagger(
                *[
                    sequence(
                        stagger(
                            *[a.animate.create().duration(0.35) for a in arms],
                            each=0.01,
                        ),
                        stagger(
                            *[ln.animate.create().duration(0.35) for ln in lintels],
                            each=0.01,
                        ),
                    )
                    for arms, lintels in by_level
                ],
                each=0.35,
            ),
        ]
    )
    # Un pórtico plano: las barras, brazos y dinteles de un mismo eje (eje A).
    in_frame = {id(x) for x in frame_a}
    others = [
        x
        for x in [
            *bars,
            *[ln for arms, lintels in by_level for ln in (*arms, *lintels)],
        ]
        if id(x) not in in_frame
    ]
    frame_label = t(
        scene,
        "Pórtico plano del eje A",
        *iso(WIDTH, -1.0, 0),
        size=0.17,
        weight=700,
        color=STEEL,
        anchor=Anchor.TOP_LEFT,
    ).hidden()
    scene.play(
        [
            *[x.animate.opacity(0.15).duration(0.5) for x in others],
            frame_label.animate.fade_in().duration(0.4).delay(0.2),
        ]
    )
    scene.stop("pp-porticos")

    # 6 · El ingeniero escribe en ETABS las propiedades que calculó (sección General).
    scene.play(
        [
            *[x.animate.opacity(1).duration(0.5) for x in others],
            frame_label.animate.fade_out().duration(0.3),
        ]
    )
    pointer = _pointer(scene).move_to(*iso(10.0, 4.0, top), Anchor.TOP_LEFT)
    pick = iso(X4_START + X4["cg"], 5.03, levels[2] - 1.0)
    ghost = [
        scene.geometry.polygon(
            [
                iso(X4_START, 5.03, z - STORY_HEIGHT),
                iso(X4_START + length, 5.03, z - STORY_HEIGHT),
                iso(X4_START + length, 5.03, z),
                iso(X4_START, 5.03, z),
            ]
        )
        .fill(STEEL_SOFT)
        .stroke(STEEL, 0.008)
        .opacity(0.75)
        .z_index(19)
        .hidden()
        for z in levels
    ]
    window, window_texts, _ = _define_window(
        scene, "Define › Frame Properties · X4", FRAME_WINDOW, -1.55, head=False
    )
    scene.play([*step(5), pointer.animate.fade_in().duration(0.3)])
    scene.play(
        pointer.animate.move_to(*pick, Anchor.TOP_LEFT)
        .duration(0.6)
        .easing(Easing.SMOOTH)
    )
    scene.play(
        [
            _click(scene, *pick),
            stagger(*[g.animate.fade_in().duration(0.3) for g in ghost], each=0.08),
            *[
                w.animate.fade_in_from(Direction.UP, 0.06).duration(0.35).delay(0.3)
                for w in window
            ],
            sequence(*[typed(x, 70).delay(0.1) for x in window_texts]).delay(0.6),
            pointer.animate.fade_out().duration(0.3).delay(0.6),
        ]
    )
    scene.wait(0.2)
    scene.stop("pp-secciones")

    # 7 · Las cargas tributarias entran como fuerzas en el nudo de cada barra y piso.
    arrows = [
        scene.geometry.arrow(
            *iso(x, y, z + 0.75),
            *iso(x, y, z),
            head_length=0.05,
            head_width=0.05,
            body_width=0.01,
        )
        .fill(BRICK_DEEP)
        .no_stroke()
        .z_index(OVERLAY + 5)
        .hidden()
        for z in levels
        for _, x, y in BARS
    ]
    dead, live = X4_POINT_LOADS
    load_x, load_y = iso(X4_START + X4["cg"], 5.03, levels[2] + 0.75)
    load_tag = pill(
        scene,
        f"X4 · CM {dead:.2f} · CV {live:.2f} tonf",
        load_x - 0.08,
        load_y + 0.02,
        size=0.1,
        pad=(0.06, 0.025),
        color=INK,
        border=RULE,
        anchor=Anchor.BOTTOM_RIGHT,
    ).z_index(OVERLAY + 6)
    scene.play(
        [
            *step(6),
            *[w.animate.fade_out().duration(0.3) for w in (*window, *window_texts)],
            *[g.animate.fade_out().duration(0.4) for g in ghost],
            stagger(
                *[a.animate.grow_arrow().duration(0.3) for a in arrows], total=1.4
            ).delay(0.2),
            load_tag.animate.fade_in_from(Direction.LEFT, 0.05)
            .duration(0.3)
            .delay(1.4),
        ]
    )

    # 8 · Diafragma rígido: cada nivel liga los nudos de todos los pórticos a D1.
    nodes = [(x, y) for _, x, y in BARS]
    spokes: list[Drawable] = []
    waves: list[Composition] = []
    for z in levels:
        c = iso(*DIAPHRAGM_CENTER, z)
        lines = [
            scene.geometry.dashed_line(
                *c, *iso(*node, z), dash_length=0.035, gap_length=0.03
            )
            .stroke(INK_SOFT, 0.007)
            .z_index(23)
            .hidden()
            for node in nodes
        ]
        dot = (
            scene.geometry.circle(0.04)
            .fill(INK)
            .stroke(CARD, 0.01)
            .move_to(*c)
            .z_index(OVERLAY + 7)
            .hidden()
        )
        spokes += lines
        waves.append(
            parallel(
                dot.animate.grow_from_center().duration(0.25),
                stagger(
                    *[ln.animate.create().duration(0.45) for ln in lines], each=0.005
                ),
            )
        )
    d1 = (
        t(
            scene,
            "D1",
            iso(*DIAPHRAGM_CENTER, top)[0] - 0.08,
            iso(*DIAPHRAGM_CENTER, top)[1] - 0.05,
            font=MONO,
            size=0.11,
            weight=700,
            color=INK,
            anchor=Anchor.TOP_RIGHT,
        )
        .z_index(OVERLAY + 8)
        .hidden()
    )
    scene.play(
        [
            *step(7),
            stagger(*waves, each=0.3),
            d1.animate.fade_in().duration(0.3).delay(1.0),
        ]
    )
    scene.play(
        [*[ln.animate.opacity(0.7).duration(0.4) for ln in spokes], *steps.restore()]
    )
    source(
        scene,
        "Tesis · §5.3.2, pp. 67–73 (Tablas 25–27, Figuras 35–39); San Bartolomé (2006), §6 y §7 "
        "· modelo MSTA de ETABS; sección de X4 esquemática",
    )
    scene.stop("pp-diafragma")


def _percent(value: float) -> str:
    """Diferencia con signo tipográfico; el cero va sin signo."""
    return "0.00 %" if value == 0 else f"{value:+.2f} %".replace("-", "−")


def criteria(scene: Scene) -> None:
    header(scene, KICKER, "El modelo depende de decisiones que el software no toma")
    support = MODEL_CHECKS["apoyo"]
    bare = MODEL_CHECKS["confinamiento"]
    auto = MODEL_CHECKS["automaticas"]
    measured = [
        ("Peso sísmico", "peso"),
        ("Fuerza sísmica", "fuerza"),
        ("Deriva", "deriva"),
    ]
    # (título, frente a qué, captura, cifra, rótulo, filas, color): en el orden del cap. 4.
    cards = [
        (
            "Malla de los muros",
            "muro de prueba de 4 pisos",
            "cap4/Prueba_Mesh.png",
            f"{MESH_STEP:.1f} m",
            "malla suficiente (N8)",
            [
                ("Mallas probadas", "N2 … N32"),
                ("Lado", f"{MESH_SIZES[0]:g} … {MESH_SIZES[-1]:g} m"),
                ("Deriva N16 vs. N8", f"≤ {MESH_N16_VARIATION:.2f} %"),
                ("Criterio", "< 1 %"),
            ],
            STEEL,
        ),
        (
            "Apoyo simple vs. empotrado",
            "empotrado frente a apoyo fijo",
            "cap4/Modelo_empotrado.png",
            f"≤ {max(abs(v) for v in support.values()):.1f} %",
            "basta el apoyo simple",
            [
                *[(name, _percent(support[key])) for name, key in measured],
                ("Momento en muros", _percent(support["momento"])),
            ],
            STEEL,
        ),
        (
            "Sin columnas de confinamiento",
            "frente al modelo confinado",
            "cap4/Moelo_SC.png",
            f"+{bare['deriva']:.1f} %",
            "más deriva",
            [(name, _percent(bare[key])) for name, key in measured],
            BRICK,
        ),
        (
            "Opciones automáticas de ETABS",
            "inserción, brazos rígidos y malla",
            "cap4/mesh_auto.png",
            f"−{abs(auto['deriva']):.1f} %",
            "menos deriva",
            [(name, _percent(auto[key])) for name, key in measured],
            BRICK,
        ),
    ]
    built = [
        comparison_card(
            scene,
            title=title,
            versus=versus,
            picture=scene.media.image(
                thesis_image(image), width=2.9, height=2.6, fit="contain"
            ),
            value=big,
            unit=unit,
            rows=rows,
            color=color,
        )
        for title, versus, image, big, unit, rows, color in cards
    ]
    row = scene.layout.row(
        *built, gap="28px", align="stretch", width="fill", height="fill"
    )
    page(scene, body=[row])
    for card in built:
        scene.play(
            enter(card, direction=Direction.UP, distance=0.08, duration=0.3, each=0.06)
        )
    source(
        scene,
        "Tesis · cap. 4: Tabla 8, p. 35 · Tablas 10–13, pp. 39–40 · Tablas 14–16, pp. 42–44 "
        "· Tablas 17–19, pp. 48–49 · capturas de ETABS de la tesis",
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
            name="Proceso manual · modelo completo en ETABS",
            build=full_model,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.5 min. El MCT se arma en ETABS 22 siguiendo sus menús: Definir, Dibujar y "
                "Asignar (§5.3.1). (1) Grillas en los ejes del plano y cuatro pisos: 2.46 m y "
                "3 × 2.52 m. (2) Materiales: albañilería ALB65 tipo Masonry (Em = 500 f'm, "
                "ν = 0.25, γ = 1800 kgf/m³) y concreto C175 (Ec = 15 000√f'c, ν = 0.15). "
                "(3) Secciones: columnas y vigas como frames; muros M13 y P13 como shell-thin "
                "(membrana y placa); losa maciza LM12 como membrane (E.030, art. 30.8). (4) Se "
                "dibuja de nodo a nodo; con Similar Stories cada elemento aparece en los cuatro "
                "pisos, y los bordes de los shells caen sobre los frames. (5) Ocultando las losas "
                "se ve la malla de 0.50 m (Wall Auto Mesh): sus nodos coinciden con los de "
                "columnas y vigas; los brazos rígidos se asignaron a mano (End Length Offsets, "
                "factor 0.5). (6) Diafragma rígido D1 en cada losa. (7) Etiquetas Pier: un nombre "
                "por muro, igual en todos los pisos; con ellas ETABS integra los esfuerzos de la "
                "malla en fuerzas por muro. (8) Load Sets: CM 0.10 y CV 0.20 tonf/m² (azotea "
                "CV 0.10); masa = CM + 25 % CV: 121.3 tonf por piso típico y 87.8 en la azotea. "
                "Al analizar, el modo 3 (T = 0.171 s) es la traslación pura en Y; la deformada "
                "está exagerada. Dibujo esquemático: el orden de los clics es ilustrativo."
            ),
        ),
        SectionStep(
            name="Proceso manual · pórticos planos",
            build=plane_frames,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1.5 min. Modelo simplificado (MSTA), §5.3.2, con el método de San Bartolomé (2006). "
                "Antes de abrir ETABS, cada muro se prepara a mano. (1) Sección transformada en CAD "
                "con la rutina SECTRANS: las columnas de concreto se convierten en albañilería "
                "multiplicando su espesor por n = Ec/Em ≈ 6.1 y los muros transversales entran como "
                "alas. (2) La rutina une las piezas y da centroide y propiedades: X4 tiene su "
                "centroide a 1.212 m de la cara, no al centro, porque el ala de Y4 está en un "
                "extremo; A1 = 1.038 m², A2 = L t = 0.403 m², I3 = 1.509 m⁴ (Tabla 26). (3) Método "
                "del sobre: líneas a 45° reparten cada paño; X4 recibe 3.38 + 3.64 = 7.02 m², "
                "CM = 2.72 y CV = 1.40 tonf por piso; en el modelo se escalan para sumar el peso "
                "total de la losa (2.91 y 1.50 tonf). (4) En ETABS, una barra por muro en su "
                "centroide, empotrada en la base. (5) Brazos rígidos (material rígido) del centroide "
                "al borde del muro y dinteles T (interiores) o L (perimetrales): cada eje forma un "
                "pórtico plano, como el del eje A. (6) Secciones General con las propiedades "
                "calculadas; rigidez casi nula fuera del plano (× 0.0001) y peso × A2/A1 para no "
                "contar las alas. (7) Las cargas tributarias entran como fuerzas en cada barra y "
                "piso. (8) El diafragma rígido D1 une los pórticos. Contraste con el MCT: aquí la "
                "idealización y las cargas las decide el ingeniero fuera del programa."
            ),
        ),
        SectionStep(
            name="Proceso manual · criterios de modelamiento",
            build=criteria,
            transition=Transition.cross_fade(0.45),
            notes=(
                "1 min. Las cuatro comparaciones del cap. 4, cada una frente a su modelo de "
                "referencia (peso sísmico, fuerza sísmica y deriva; el apoyo también momentos). "
                "(1) Malla: el muro de prueba se analizó con mallas N2 a N32; entre N8 y N16 la deriva "
                "varía 0.01 %, así que basta N8 de 0.5 m. (2) Apoyo: empotrar no cambia peso ni "
                "fuerzas, la deriva baja hasta 2.63 % y el momento sube hasta 1.89 %; sin estudio de "
                "suelos basta el apoyo simple. (3) Sin columnas ni vigas de confinamiento: el peso y "
                "el cortante basal bajan 5.96 % y la deriva sube hasta 38.50 %. (4) Opciones "
                "automáticas de ETABS (inserción, brazos rígidos, malla): peso igual, deriva hasta "
                "10.53 % menor, un modelo más rígido y no conservador."
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
