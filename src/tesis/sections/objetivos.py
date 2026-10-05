"""Bloque 2 · Objetivos, hipótesis y método de la investigación."""

import re

from gaanim import (
    Bounds,
    Box,
    Color,
    Direction,
    Drawable,
    Easing,
    Playable,
    Scene,
    Section,
    SectionStep,
    Text,
    Transition,
    parallel,
    sequence,
    stagger,
)

from tesis.building import draw_plan, grow_walls
from tesis.components import (
    PX,
    enter,
    hairline,
    header,
    note,
    objective_card,
    page,
    source,
    stage,
)
from tesis.data.thesis import CASE, MODELS
from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    DISPLAY,
    INK,
    INK_SOFT,
    MODEL_COLORS,
    MONO,
    MUTED,
    PASS,
    STEEL,
)

KICKER = "02 · Objetivos y método"


# Objetivo general, textual (tesis, §1.3.1). Entre corchetes, las palabras que se
# subrayan: cada clave es un concepto que baja al esquema de la hipótesis.
OBJECTIVE = (
    "Desarrollar [marco:un marco de trabajo] para la [auto:automatización] del diseño "
    "de la distribución de muros en planta para edificios de "
    "[alba:albañilería confinada] conforme a los requerimientos establecidos en "
    "[norma:la norma E.070] y su aplicación mediante un programa de desarrollo propio "
    "capaz de [api:interactuar] con el software comercial [etabs:ETABS]."
)
TOKEN = re.compile(r"\[(\w+):([^\]]+)\]([.,]?)|(\S+)")


def _keys(source: str) -> dict[str, str]:
    return {
        name: phrase for name, phrase, _mark, _word in TOKEN.findall(source) if name
    }


# La hipótesis (§1.4) como relación entre esos conceptos: con qué palabra y en qué
# cuerpo (px) llega cada clave a su sitio en el esquema.
CONCEPTS = {
    "marco": ("un marco de trabajo", 36),
    "auto": ("automatizado", 36),
    "api": ("integrado", 28),
    "etabs": ("ETABS", 36),
    "norma": ("verificaciones normativas", 36),
    "alba": ("albañilería confinada", 30),
}

# Cada palabra del objetivo es una caja que mide la línea completa: las de un
# renglón comparten borde inferior y la línea base queda a una distancia fija.
WORD_PX = 44
WORD = {"font": DISPLAY, "font_size": f"{WORD_PX}px", "color": INK}
BASELINE = 0.064  # de la base de la caja a la línea base (Aleo a 44 px)
UNDERLINE = 0.025  # grosor del subrayado (3 px)
UNDERLINE_DROP = 0.07  # de la línea base al eje del subrayado (Aleo a 44 px)


def _prose(scene: Scene, source: str) -> tuple[Box, dict[str, Box], list[Box]]:
    """Párrafo compuesto palabra a palabra en una fila que salta de línea.

    Cada palabra es su propia caja: las claves (entre corchetes) se pueden medir y
    subrayar. Devuelve el párrafo, las claves por nombre y las demás palabras en
    orden de lectura.
    """
    L = scene.layout
    tokens: list[Box] = []
    keys: dict[str, Box] = {}
    words: list[Box] = []
    for name, phrase, mark, word in TOKEN.findall(source):
        if word:
            box = L.box(word, **WORD)
            words.append(box)
            tokens.append(box)
            continue
        key = keys[name] = L.box(phrase, **WORD)
        if mark:
            # La puntuación va pegada a la clave, fuera de su subrayado.
            stop = L.box(mark, **WORD)
            words.append(stop)
            tokens.append(L.row(key, stop, gap="0px"))
        else:
            tokens.append(key)
    paragraph = L.row(
        *tokens, wrap=True, column_gap="11px", row_gap="18px", align="end", width="fill"
    )
    return paragraph, keys, words


def _baseline(bounds: Bounds, px: float = WORD_PX) -> float:
    return bounds.bottom + BASELINE * px / WORD_PX


def _underline(scene: Scene, bounds: Bounds, px: float = WORD_PX) -> Drawable:
    """Filete bajo una palabra medida, a la altura de un subrayado tipográfico."""
    return (
        scene.geometry.rect(bounds.right - bounds.left, UNDERLINE)
        .fill(BRICK)
        .no_stroke()
        .move_to(
            (bounds.left + bounds.right) / 2,
            _baseline(bounds, px) - UNDERLINE_DROP * px / WORD_PX,
        )
    )


def _word(scene: Scene, phrase: str, px: float, bounds: Bounds) -> Text:
    """Texto libre sobre la línea base de una caja medida (para viajar entre cajas)."""
    return scene.text(
        phrase, font=DISPLAY, size=px / PX, color=BRICK, wrap=False
    ).move_to((bounds.left + bounds.right) / 2, _baseline(bounds, px))


def _node(scene: Scene, tag: str, *body: Drawable) -> Box:
    """Concepto del esquema: rótulo en versalitas sobre sus palabras."""
    return scene.layout.column(note(scene, text=tag, size="15px"), *body, gap="10px")


def _link(scene: Scene, top: Box, bottom: str) -> tuple[Box, Drawable]:
    """Relación entre dos conceptos: el verbo encima de la flecha y el medio debajo."""
    L = scene.layout
    arrow = scene.geometry.arrow(0, 0, 1.9, 0).fill(INK_SOFT).no_stroke()
    column = L.column(
        top,
        arrow,
        L.box(bottom, font_size="20px", color=INK_SOFT, text_align="center"),
        gap="6px",
        align="center",
        width="fill",
    ).item(grow=1)
    return column, arrow


def _role(scene: Scene, tag: str, value: Drawable) -> Box:
    """Papel de un concepto en la investigación (variable), en el color de la hipótesis."""
    return scene.layout.column(
        note(scene, text=tag, color=STEEL, size="14px"),
        value,
        gap="6px",
        padding=("18px", "0px", "0px", "0px"),
    )


def purpose(scene: Scene) -> None:
    header(scene, KICKER, "Del objetivo general a una hipótesis verificable")
    L = scene.layout

    # Arriba, el objetivo general a todo el ancho.
    goal_tag = note(scene, text="Objetivo general", color=BRICK, size="18px")
    objective, obj_keys, obj_words = _prose(scene, OBJECTIVE)

    # Abajo, la hipótesis como esquema: propuesta → software → efecto esperado,
    # dentro del ámbito de la albañilería confinada.
    concepts = {
        name: L.box(phrase, font=DISPLAY, font_size=f"{px}px", color=BRICK)
        for name, (phrase, px) in CONCEPTS.items()
    }
    permit = L.box("permitirá", font=DISPLAY, font_size="28px", weight=700, color=STEEL)
    link_api, arrow_api = _link(scene, concepts["api"], "mediante su API")
    link_data, arrow_data = _link(scene, permit, "extrae y procesa los datos")
    captions = {
        "etabs": L.box("modelo de elementos finitos", font_size="20px", color=INK_SOFT),
        "norma": L.box("ejecutadas y documentadas", font_size="20px", color=INK_SOFT),
    }
    shift = scene.geometry.arrow(0, 0, 0.26, 0).fill(MUTED).no_stroke()
    independent = _role(
        scene,
        "Variable independiente",
        L.row(
            L.box("método manual", font_size="21px", color=INK_SOFT),
            shift,
            L.box("automatizado", font_size="21px", weight=700, color=INK),
            gap="10px",
            align="center",
        ),
    )
    dependent = _role(
        scene,
        "Variable dependiente",
        L.box("cumplimiento normativo", font_size="21px", weight=700, color=INK),
    )
    proposal = _node(
        scene, "Propuesta", concepts["marco"], concepts["auto"], independent
    )
    software = _node(scene, "Software comercial", concepts["etabs"], captions["etabs"])
    effect = _node(
        scene, "Efecto esperado", concepts["norma"], captions["norma"], dependent
    )
    chain = L.row(
        proposal,
        link_api,
        software,
        link_data,
        effect,
        gap="28px",
        align="start",
        width="fill",
    )
    # Ámbito: una llave horizontal que abarca todo el esquema.
    ticks = [L.box(width="2px", height="18px", background=MUTED) for _ in range(2)]
    spans = [hairline(scene, color=MUTED) for _ in range(2)]
    domain = L.box("para edificaciones de", font_size="22px", color=INK_SOFT)
    scope = L.row(
        ticks[0],
        spans[0],
        domain,
        concepts["alba"],
        spans[1],
        ticks[1],
        gap="14px",
        align="center",
        width="fill",
    )
    hyp_tag = note(scene, text="Hipótesis", color=STEEL, size="18px")
    hyp_rule = hairline(scene)
    heading = L.row(hyp_tag, hyp_rule, gap="18px", align="center", width="fill")

    page(
        scene,
        body=[
            L.column(goal_tag, objective, gap="22px", width="fill"),
            L.column(heading, chain, scope, gap="26px", width="fill"),
        ],
        top="200px",
        gap="46px",
    )
    # Medir antes del primer play: recién maquetadas, las cajas se miden solas;
    # después, cada bounds() recompila toda la presentación hasta aquí.
    obj_bounds = {name: box.bounds() for name, box in obj_keys.items()}
    slots = {name: box.bounds() for name, box in concepts.items()}

    # Las cajas de los conceptos solo reservan su sitio: las palabras que llegan
    # desde el objetivo son textos libres que se transforman en ellas.
    for box in concepts.values():
        box.opacity(0)

    scene.play(
        stagger(
            goal_tag.animate.fade_in().duration(0.3),
            stagger(
                *[
                    box.animate.fade_in_from(Direction.UP, 0.05).duration(0.3)
                    for box in objective.walk()
                ],
                each=0.012,
            ),
            each=0.15,
        )
    )
    scene.stop("objetivo-general")

    # Palabras clave: se subrayan en el orden de lectura.
    lines = {name: _underline(scene, bd) for name, bd in obj_bounds.items()}
    scene.play(
        stagger(
            *[
                parallel(
                    line.animate.grow_from_edge(Direction.LEFT).duration(0.45),
                    obj_keys[name].children[0].animate.fill(BRICK).duration(0.45),
                )
                for name, line in lines.items()
            ],
            each=0.28,
        )
    )
    scene.stop("palabras-clave")

    # Hipótesis: el objetivo queda de fondo y una copia de cada palabra subrayada
    # baja a su sitio en el esquema (cambiando de forma si la palabra cambia),
    # con su subrayado.
    scene.play(
        parallel(
            *[box.animate.opacity(0.35).duration(0.5) for box in obj_words],
            hyp_tag.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.4),
            hyp_rule.animate.grow_from_edge(Direction.LEFT).duration(0.6),
        )
    )
    travel: list[Playable] = []
    for name, start in obj_bounds.items():
        phrase, px = CONCEPTS[name]
        slot = slots[name]
        traveler = _word(scene, _keys(OBJECTIVE)[name], WORD_PX, start)
        target = _word(scene, phrase, px, slot).opacity(0)
        line = _underline(scene, start)
        line_target = _underline(scene, slot, px).opacity(0)
        travel.append(
            sequence(
                parallel(
                    traveler.animate.fade_in().duration(0.01),
                    line.animate.fade_in().duration(0.01),
                ),
                parallel(
                    traveler.animate.transform_to(target)
                    .duration(1.1)
                    .easing(Easing.SMOOTH),
                    line.animate.transform_to(line_target)
                    .duration(1.1)
                    .easing(Easing.SMOOTH),
                ),
            )
        )
    scene.play(stagger(*travel, each=0.12))

    # Las relaciones se dibujan en el orden en que se lee la hipótesis.
    scene.play(
        stagger(
            proposal.children[0].animate.fade_in().duration(0.3),
            parallel(
                arrow_api.animate.grow_from_edge(Direction.LEFT).duration(0.45),
                link_api.children[2].animate.fade_in().duration(0.35),
            ),
            parallel(
                software.children[0].animate.fade_in().duration(0.3),
                captions["etabs"].animate.fade_in().duration(0.3),
            ),
            parallel(
                permit.animate.fade_in_from(Direction.DOWN, 0.05).duration(0.35),
                arrow_data.animate.grow_from_edge(Direction.LEFT).duration(0.45),
                link_data.children[2].animate.fade_in().duration(0.35),
            ),
            parallel(
                effect.children[0].animate.fade_in().duration(0.3),
                captions["norma"].animate.fade_in().duration(0.3),
            ),
            parallel(
                domain.animate.fade_in().duration(0.35),
                spans[0].animate.grow_from_edge(Direction.RIGHT).duration(0.5),
                spans[1].animate.grow_from_edge(Direction.LEFT).duration(0.5),
                *[tick.animate.fade_in().duration(0.2).delay(0.4) for tick in ticks],
            ),
            each=0.3,
        )
    )
    source(
        scene,
        "Tesis · §1.3.1 Objetivo general, §1.4 Hipótesis y §1.5 Variables de la investigación, pp. 3–4",
    )
    scene.stop("hipotesis")

    # Variables: el método de diseño (propuesta) incide en el cumplimiento
    # normativo (efecto esperado).
    scene.play(
        stagger(
            enter(independent, direction=Direction.UP, duration=0.35, each=0.08),
            enter(dependent, direction=Direction.UP, duration=0.35, each=0.08),
            each=0.35,
        )
    )
    scene.stop("variables")


SPECIFIC = [
    (
        "Identificar",
        "el proceso manual de\ndiseño de la distribución\nde muros con un software\nde elementos finitos y\nhojas de cálculo.",
        "Flujo manual · cap. 5",
    ),
    (
        "Desarrollar",
        "un marco de trabajo para\nautomatizar el diseño de la\ndistribución en planta, a partir\nde actividades críticas y\nrepetitivas, con diagramas de flujo.",
        "Diagramas · cap. 6",
    ),
    (
        "Aplicar",
        "el marco en un programa\nque interactúa con ETABS\nmediante su interfaz de\nprogramación (API).",
        "Alba + API · cap. 7",
    ),
    (
        "Evaluar",
        "los resultados del caso\ncomparando alternativas\nde modelamiento y la\nverificación normativa.",
        "Comparación · cap. 8",
    ),
]


def specific(scene: Scene) -> None:
    header(scene, KICKER, "Cuatro objetivos específicos, cuatro productos")
    cards = [
        objective_card(
            scene,
            number=i + 1,
            verb=verb,
            text=body.replace("\n", " "),
            product=product,
        )
        for i, (verb, body, product) in enumerate(SPECIFIC)
    ]
    page(
        scene,
        body=[
            scene.layout.row(*cards, gap="32px", align="stretch", width="fill"),
        ],
        gap="48px",
    )
    for card in cards:
        scene.play(
            enter(card, direction=Direction.UP, distance=0.08, duration=0.4, each=0.06)
        )
    # scene.play(enter(flow, duration=0.5, each=0.3))
    source(scene, "Tesis · §1.3.2 Objetivos específicos, p. 4")
    scene.stop("objetivos-especificos")


# Metodología: cuatro etapas a todo el alto, cada una con su gráfico animado (SVG
# en assets/metodo), y el caso de estudio al pie. Sin resultados: esos llegan en
# el bloque de resultados.
ART = "metodo"
STAGE_HEAD = "71px"  # filete + número y nombre + separación: hasta el gráfico
SLOT = "400px"  # alto común de los gráficos de las etapas

# Diagrama de flujo (flujo.svg, 220 × 290 px del SVG), dibujado a 1.3 px por px.
FLOW = (220, 290, 1.3)
# Geometría de flujo.svg en px del SVG, para remarcar el recorrido encima: las
# flechas que se atraviesan y el contorno de cada símbolo al alcanzarlo.
FLOW_EDGES = {
    "a1": [(110, 30), (110, 54)],
    "a2": [(110, 92), (110, 114)],
    "bucle": [(168, 150), (202, 150), (202, 74), (174, 74)],
    "a3": [(110, 184), (110, 202)],
    "a4": [(110, 240), (110, 256)],
}
FLOW_BOXES = {"proceso": (110, 74, 124, 36), "verificacion": (110, 222, 124, 36)}
FLOW_DECISION = [(110, 116), (168, 150), (110, 184), (52, 150)]
TRACE = 0.035  # grosor del trazo que remarca el recorrido
# Caja de tinta de flujo.svg (px del SVG): el SVG se escala por su tinta, no por
# su lienzo, así que el recorrido se ubica respecto de ella.
FLOW_INK = (46.75, 4.0, 203.5, 284.0)
BRICKS = 24  # ladrillos de norma_e070.svg: ids b0 … b23, hilada por hilada

MODEL_W = 124  # ancho de cada modelo de la etapa 4
MODEL_GAP = 12
PROGRAM_COLS = (170, 150, 170)  # ETABS/Reporte · API/flecha · Alba/Typst
PROGRAM_ROWS = (130, 64, 150)


def _svg(scene: Scene, name: str, width: str, height: str) -> Drawable:
    return scene.media.svg(f"{ART}/{name}.svg").item(
        width=width, height=height, fit="contain"
    )


def _sheet(scene: Scene, name: str, code: str, subject: str) -> tuple[Box, Drawable]:
    """Hoja de una norma con su código encima; devuelve la hoja y el dibujo."""
    L = scene.layout
    art = _svg(scene, name, "175px", "228px")
    title = L.column(
        L.box(code, font=DISPLAY, font_size="34px", weight=700, color=INK),
        L.box(subject, font_size="16px", color=INK_SOFT),
        gap="2px",
    ).item(anchor="top_left", offset=("18px", "-16px"))
    return L.stack(art, title, width="175px", height="228px"), art


def _tool(scene: Scene, art: Drawable, tag: str) -> tuple[Box, Box]:
    """Herramienta: logotipo en un hueco común y su papel debajo.

    Devuelve la columna y el hueco del logotipo, que se mide para mover los datos.
    """
    L = scene.layout
    slot = L.box(art, height="92px", align="center", justify="center")
    column = L.column(
        slot, note(scene, text=tag, size="14px"), gap="8px", align="center"
    )
    return column, slot


def _arrow(
    scene: Scene, x0: float, y0: float, x1: float, y1: float, color: Color = MUTED
) -> Drawable:
    return (
        scene.geometry.arrow(
            x0, y0, x1, y1, head_length=0.11, head_width=0.11, body_width=0.024
        )
        .fill(color)
        .no_stroke()
    )


def _cell(scene: Scene, content: Drawable | None, width: int, height: int) -> Box:
    """Celda de tamaño fijo con su contenido centrado."""
    return scene.layout.box(
        *([content] if content is not None else []),
        width=f"{width}px",
        height=f"{height}px",
        align="center",
        justify="center",
    ).item(shrink=0)


def _center(bounds: Bounds) -> tuple[float, float]:
    return (bounds.left + bounds.right) / 2, (bounds.top + bounds.bottom) / 2


def _pulse(
    scene: Scene, start: tuple[float, float], end: tuple[float, float], color: Color
) -> Drawable:
    """Trazo sobre el cuerpo de una flecha, para recorrerlo con ``show_passing_flash``."""
    return (
        scene.geometry.polyline([start, end]).no_fill().stroke(color, 0.045).z_index(8)
    )


def _bracket(
    scene: Scene, a: int, b: int, title: str, detail: str
) -> tuple[list[Box], Box]:
    """Llave entre dos modelos (por índice): filete con remates y lo que aísla.

    Devuelve las piezas de la llave (en una capa del ancho de la fila de modelos) y
    su rótulo centrado bajo ella.
    """
    L = scene.layout
    step = MODEL_W + MODEL_GAP
    x0 = a * step + MODEL_W / 2 + 6
    x1 = b * step + MODEL_W / 2 - 6
    pieces = [
        L.box(width=f"{x1 - x0:.0f}px", height="2px", background=INK_SOFT).item(
            anchor="left", offset=(f"{x0:.0f}px", "0px")
        ),
        *[
            L.box(width="2px", height="12px", background=INK_SOFT).item(
                anchor="left", offset=(f"{x:.0f}px", "6px")
            )
            for x in (x0, x1 - 2)
        ],
    ]
    label = L.column(
        L.box(title, font_size="20px", weight=900, color=INK),
        L.box(detail, font_size="16px", color=INK_SOFT),
        gap="2px",
        align="center",
        width=f"{step:.0f}px",
    ).item(anchor="left", offset=(f"{(x0 + x1) / 2 - step / 2:.0f}px", "0px"))
    return pieces, label


def _opening(item: Box) -> Playable:
    """Entrada de una etapa: el filete se traza, el nombre sube y el pie aparece."""
    rule, title, _picture, caption = item.children
    return parallel(
        rule.animate.grow_from_edge(Direction.LEFT).duration(0.5),
        enter(title, direction=Direction.UP, duration=0.35, each=0.08),
        caption.animate.fade_in().duration(0.4).delay(0.3),
    )


def method(scene: Scene) -> None:
    header(
        scene, KICKER, "Investigación aplicada, cuantitativa, sobre un caso de estudio"
    )
    L = scene.layout

    # 1 · Normas: la E.030 con su espectro y la E.070 con un muro confinado.
    e030, e030_art = _sheet(scene, "norma_e030", "E.030", "Sismorresistente")
    e070, e070_art = _sheet(scene, "norma_e070", "E.070", "Albañilería")
    # Algo menos ancha que la etapa: con el ancho justo, la etapa reserva alto de más.
    norms = L.row(e030, e070, gap="22px", align="center")

    # 2 · Diagrama de flujo, en un hueco con las proporciones del SVG.
    fw, fh, fk = FLOW
    flow = _svg(scene, "flujo", f"{fw * fk:.0f}px", f"{fh * fk:.0f}px")
    flow_box = L.box(flow, width=f"{fw * fk:.0f}px", height=f"{fh * fk:.0f}px")
    flow_parts = [
        flow.part(pid)
        for pid in (
            "inicio",
            "a1",
            "proceso",
            "a2",
            "decision",
            "bucle",
            "a3",
            "verificacion",
            "a4",
            "fin",
        )
    ]

    # 3 · Programa, en U: ETABS ⇄ Alba por la API; Alba → Typst → reporte PDF.
    etabs, etabs_slot = _tool(
        scene, _svg(scene, "etabs", "150px", "37px"), "Modelo FEM"
    )
    alba, alba_slot = _tool(scene, _svg(scene, "python", "82px", "82px"), "Alba")
    typst, typst_slot = _tool(scene, _svg(scene, "typst", "130px", "52px"), "Plantilla")
    pdf = L.stack(
        _svg(scene, "reporte", "70px", "91px"),
        L.box("PDF", font=MONO, font_size="12px", weight=700, color=INK).item(
            anchor="top_left", offset=("8px", "-8px")
        ),
        width="70px",
        height="91px",
    )
    pdf_art = pdf.children[0]
    report, report_slot = _tool(scene, pdf, "Reporte")
    api_arrow = (
        scene.geometry.double_arrow(0, 0, 1.0, 0, head_length=0.11, head_width=0.11)
        .fill(MUTED)
        .no_stroke()
    )
    # Lo que viaja por cada flecha, en tipografía técnica: aparece con su pulso.
    payload = [
        L.box(item, font=MONO, font_size="14px", color=BRICK_DEEP)
        for item in ("geometría", "cargas", "fuerzas por pier")
    ]
    api = L.column(
        L.box("API", font=MONO, font_size="18px", weight=700, color=INK_SOFT),
        api_arrow,
        L.column(*payload, gap="2px", align="center"),
        gap="8px",
        align="center",
    )
    down = _arrow(scene, 0, 0, 0, -0.42)
    back = _arrow(scene, 0.95, 0, 0, 0)
    results = L.box(
        "verificaciones",
        font=MONO,
        font_size="14px",
        color=BRICK_DEEP,
        width="fill",
        text_align="right",
        padding=("0px", "14px", "0px", "0px"),
    )
    compile_tag = L.box("compila", font=MONO, font_size="14px", color=BRICK_DEEP)
    c1, c2, c3 = PROGRAM_COLS
    r1, r2, r3 = PROGRAM_ROWS
    program = L.column(
        L.row(
            _cell(scene, etabs, c1, r1),
            _cell(scene, api, c2, r1),
            _cell(scene, alba, c3, r1),
        ),
        L.row(
            _cell(scene, None, c1, r2),
            _cell(scene, results, c2, r2),
            _cell(scene, down, c3, r2),
        ),
        L.row(
            _cell(scene, report, c1, r3),
            _cell(
                scene, L.column(compile_tag, back, gap="8px", align="center"), c2, r3
            ),
            _cell(scene, typst, c3, r3),
        ),
    )

    # 4 · Comparación: el mismo edificio en tres modelos; cada par aísla una causa.
    models = {m: _svg(scene, f"modelo_{m.lower()}", "110px", "128px") for m in MODELS}
    names = {
        m: L.column(
            L.box(m, font=DISPLAY, font_size="26px", weight=700, color=MODEL_COLORS[m]),
            note(scene, text=tag, color=INK_SOFT, size="16px", upper=False),
            gap="2px",
            align="center",
        )
        for m, tag in zip(MODELS, ("áreas", "barras", "barras · 2006"), strict=True)
    }
    lineup = L.row(
        *[
            L.column(
                models[m], names[m], gap="6px", align="center", width=f"{MODEL_W}px"
            ).item(shrink=0)
            for m in MODELS
        ],
        gap=f"{MODEL_GAP}px",
        align="start",
    )
    width = 3 * MODEL_W + 2 * MODEL_GAP
    pair_a, label_a = _bracket(scene, 0, 1, "Idealización", "misma norma")
    pair_b, label_b = _bracket(scene, 1, 2, "Norma", "misma idealización")
    brackets = L.stack(*pair_a, *pair_b, width=f"{width}px", height="22px")
    pair_labels = L.stack(label_a, label_b, width=f"{width}px", height="48px")
    comparison = L.column(lineup, brackets, pair_labels, gap="10px", align="center")

    stages = [
        stage(
            scene,
            number=1,
            name="Revisión normativa",
            picture=norms,
            caption="Normas E.030 y E.070, y bibliografía",
            height=SLOT,
            width="376px",
        ),
        stage(
            scene,
            number=2,
            name="Diagramas de flujo",
            picture=flow_box,
            caption="La lógica de cada verificación",
            height=SLOT,
            width="300px",
        ),
        stage(
            scene,
            number=3,
            name="Programa propio",
            picture=program,
            caption="Alba lee ETABS por la API y redacta el reporte",
            height=SLOT,
            width="500px",
        ),
        stage(
            scene,
            number=4,
            name="Comparación descriptiva",
            picture=comparison,
            caption="Un edificio en tres modelos",
            height=SLOT,
        ),
    ]
    links = [_arrow(scene, 0, 0, 0.3, 0) for _ in range(3)]
    gutters = [
        L.column(
            L.box(height=STAGE_HEAD),
            L.box(link, height=SLOT, align="center", justify="center"),
            width="48px",
        ).item(shrink=0)
        for link in links
    ]
    pipeline = L.row(
        stages[0],
        gutters[0],
        stages[1],
        gutters[1],
        stages[2],
        gutters[2],
        stages[3],
        gap="6px",
        align="start",
        width="fill",
    )

    # Al pie, el caso de estudio sobre el que trabajan el programa y la comparación.
    plan_slot = L.box(width="300px", height="146px").item(shrink=0)
    case_rule = hairline(scene)
    case_text = L.column(
        note(
            scene,
            text="Caso de estudio · muestra no probabilística",
            color=BRICK,
            size="16px",
        ),
        L.box(
            "Edificio de albañilería confinada de 4 pisos",
            font=DISPLAY,
            font_size="32px",
            weight=700,
            color=INK,
        ),
        L.box(
            f"San Bartolomé (2006) · vivienda en Lima · planta de "
            f"{CASE['planta'][0]:.1f} × {CASE['planta'][1]:.1f} m",
            font_size="21px",
            color=INK_SOFT,
        ),
        gap="8px",
    )
    # A la derecha, el tipo de investigación (§1.6.1).
    kind = L.row(
        *[
            L.column(
                note(scene, text=name, size="15px"),
                L.box(value, font=DISPLAY, font_size="30px", weight=700, color=INK),
                gap="6px",
            )
            for name, value in (("Nivel", "Aplicativo"), ("Enfoque", "Cuantitativo"))
        ],
        gap="56px",
    ).item(margin=(0, 0, 0, "auto"))
    case = L.column(
        case_rule,
        L.row(plan_slot, case_text, kind, gap="40px", align="center", width="fill"),
        gap="16px",
        width="fill",
    )

    page(scene, body=[pipeline, case], top="200px", gap="26px")
    # Medir antes de animar: los recorridos se remarcan sobre dibujos del layout.
    flow_area = flow.bounds()
    api_b, down_b, back_b = (d.bounds() for d in (api_arrow, down, back))
    plan_area = plan_slot.bounds()

    # 1 · Las normas llegan; el espectro se traza y el muro se levanta hilada por
    # hilada antes de vaciar su confinamiento.
    scene.play(
        stagger(
            _opening(stages[0]),
            stagger(
                e030.animate.fade_in_from(Direction.UP, 0.1).duration(0.45),
                e070.animate.fade_in_from(Direction.UP, 0.1).duration(0.45),
                each=0.18,
            ),
            parallel(
                e030_art.part("area").animate.fade_in().duration(0.6).delay(0.5),
                e030_art.part("espectro").animate.create().duration(1.1),
                stagger(
                    *[
                        e070_art.part(f"b{i}")
                        .animate.fade_in_from(Direction.DOWN, 0.04)
                        .duration(0.18)
                        for i in range(BRICKS)
                    ],
                    each=0.04,
                ),
            ),
            stagger(
                e070_art.part("columna1")
                .animate.grow_from_edge(Direction.DOWN)
                .duration(0.35),
                e070_art.part("columna2")
                .animate.grow_from_edge(Direction.DOWN)
                .duration(0.35),
                e070_art.part("viga")
                .animate.grow_from_edge(Direction.LEFT)
                .duration(0.4),
                each=0.15,
            ),
            each=0.3,
        )
    )
    source(
        scene,
        "Tesis · §1.6 Metodología de la investigación, pp. 5–6 · §8.1 Diferencias entre los modelos analizados",
    )
    scene.stop("metodo-normas")

    # 2 · El diagrama se arma símbolo por símbolo y se recorre remarcando las
    # flechas que se atraviesan y cada símbolo alcanzado: en terracota la primera
    # pasada y la iteración (no cumple); en verde el camino que cumple.
    ink_left, ink_top, ink_right, _ink_bottom = FLOW_INK
    k = (flow_area.right - flow_area.left) / (ink_right - ink_left)

    def point(sx: float, sy: float) -> tuple[float, float]:
        return (
            flow_area.left + (sx - ink_left) * k,
            flow_area.top - (sy - ink_top) * k,
        )

    def edge(name: str, color: Color) -> Drawable:
        pts = [point(*p) for p in FLOW_EDGES[name]]
        return scene.geometry.polyline(pts).no_fill().stroke(color, TRACE).z_index(8)

    def outline(name: str, color: Color) -> Drawable:
        cx, cy, w, h = FLOW_BOXES[name]
        return (
            scene.geometry.rect(w * k, h * k)
            .no_fill()
            .stroke(color, TRACE)
            .move_to(*point(cx, cy))
            .z_index(8)
        )

    def diamond(color: Color) -> Drawable:
        pts = [point(*p) for p in FLOW_DECISION]
        return scene.geometry.polygon(pts).no_fill().stroke(color, TRACE).z_index(8)

    def trace(item: Drawable, duration: float = 0.35) -> Playable:
        return item.animate.create().duration(duration).easing(Easing.LINEAR)

    no, yes = (
        scene.text(text, font=MONO, size=16 / PX, color=color, wrap=False).move_to(
            *point(*at)
        )
        for text, color, at in (("no", BRICK, (180, 139)), ("sí", INK_SOFT, (124, 195)))
    )
    first = [
        edge("a1", BRICK),
        outline("proceso", BRICK),
        edge("a2", BRICK),
        diamond(BRICK),
    ]
    loop = edge("bucle", BRICK)
    second = [
        diamond(PASS),
        edge("a3", PASS),
        outline("verificacion", PASS),
        edge("a4", PASS),
    ]
    scene.play(
        sequence(
            links[0].animate.grow_arrow().duration(0.35),
            stagger(
                _opening(stages[1]),
                stagger(
                    *[part.animate.fade_in().duration(0.3) for part in flow_parts],
                    each=0.12,
                ),
                each=0.3,
            ),
            parallel(
                no.animate.fade_in().duration(0.3), yes.animate.fade_in().duration(0.3)
            ),
            flow.part("inicio").animate.indicate().duration(0.4),
            *[trace(item) for item in first],
            no.animate.indicate().duration(0.45),
            trace(loop, 0.7),
            first[1].animate.indicate().duration(0.45),
            parallel(trace(second[0], 0.4), first[3].animate.fade_out().duration(0.4)),
            yes.animate.fill(PASS).duration(0.25),
            *[trace(item) for item in second[1:]],
            flow.part("fin").animate.indicate().duration(0.45),
        )
    )
    scene.stop("metodo-diagramas")

    # 3 · Alba pide el modelo por la API y recibe sus datos; Typst compila los
    # resultados en un reporte que marca cada verificación. Cada flujo es un pulso
    # sobre su flecha, con el rótulo de lo que transporta.
    def mid_x(b: Bounds) -> float:
        return (b.left + b.right) / 2

    def mid_y(b: Bounds) -> float:
        return (b.top + b.bottom) / 2

    inset = 0.12  # el pulso no tapa las puntas de las flechas
    api_l, api_r, api_y = api_b.left + inset, api_b.right - inset, mid_y(api_b)
    request = _pulse(scene, (api_r, api_y), (api_l, api_y), STEEL)
    replies = [_pulse(scene, (api_l, api_y), (api_r, api_y), BRICK) for _ in payload]
    to_typst = _pulse(
        scene,
        (mid_x(down_b), down_b.top),
        (mid_x(down_b), down_b.bottom + inset),
        BRICK,
    )
    to_pdf = _pulse(
        scene,
        (back_b.right, mid_y(back_b)),
        (back_b.left + inset, mid_y(back_b)),
        BRICK,
    )

    def flash(item: Drawable, duration: float = 0.55) -> Playable:
        return item.animate.show_passing_flash(time_width=0.45).duration(duration)

    scene.play(
        sequence(
            links[1].animate.grow_arrow().duration(0.35),
            stagger(
                _opening(stages[2]),
                stagger(
                    etabs.animate.fade_in_from(Direction.UP, 0.06).duration(0.4),
                    api.children[0].animate.fade_in().duration(0.3),
                    api_arrow.animate.fade_in().duration(0.3),
                    alba.animate.fade_in_from(Direction.UP, 0.06).duration(0.4),
                    down.animate.grow_arrow().duration(0.3),
                    typst.animate.fade_in_from(Direction.UP, 0.06).duration(0.4),
                    back.animate.grow_arrow().duration(0.35),
                    report.animate.fade_in_from(Direction.UP, 0.06).duration(0.4),
                    each=0.16,
                ),
                each=0.3,
            ),
            flash(request),
            stagger(
                *[
                    parallel(
                        flash(pulse),
                        label.animate.fade_in_from(Direction.LEFT, 0.08).duration(0.4),
                    )
                    for pulse, label in zip(replies, payload, strict=True)
                ],
                each=0.3,
            ),
            alba_slot.animate.indicate().duration(0.5),
            parallel(flash(to_typst, 0.45), results.animate.fade_in().duration(0.35)),
            typst_slot.animate.indicate().duration(0.45),
            parallel(flash(to_pdf), compile_tag.animate.fade_in().duration(0.35)),
            stagger(
                pdf_art.part("formula").animate.fade_in().duration(0.3),
                pdf_art.part("filas").animate.fade_in().duration(0.3),
                pdf_art.part("cumple")
                .animate.fade_in_from(Direction.LEFT, 0.04)
                .duration(0.35),
                each=0.2,
            ),
        )
    )
    scene.stop("metodo-programa")

    # 4 · Los tres modelos se construyen; las llaves dicen qué aísla cada par.
    def build(m: str) -> Playable:
        art = models[m]
        if m == "MCT":
            body = [
                art.part("panel").animate.fade_in().duration(0.3),
                art.part("malla").animate.create().duration(0.8),
                art.part("columnas")
                .animate.grow_from_edge(Direction.DOWN)
                .duration(0.4),
                art.part("losas").animate.grow_from_edge(Direction.LEFT).duration(0.4),
            ]
        else:
            body = [
                art.part("muro").animate.fade_in().duration(0.3),
                art.part("barra").animate.grow_from_edge(Direction.DOWN).duration(0.45),
                art.part("brazos").animate.grow_from_center().duration(0.4),
                art.part("vigas").animate.create().duration(0.4),
                art.part("nudos").animate.fade_in().duration(0.3),
            ]
        return stagger(
            art.part("base").animate.grow_from_center().duration(0.3),
            *body,
            enter(names[m], direction=Direction.UP, duration=0.3, each=0.06),
            each=0.14,
        )

    scene.play(
        sequence(
            links[2].animate.grow_arrow().duration(0.35),
            stagger(
                _opening(stages[3]),
                stagger(*[build(m) for m in MODELS], each=0.35),
                each=0.3,
            ),
            stagger(
                *[
                    stagger(
                        *[
                            p.animate.grow_from_edge(Direction.LEFT).duration(0.35)
                            for p in pair
                        ],
                        label.animate.fade_in_from(Direction.UP, 0.05).duration(0.35),
                        each=0.1,
                    )
                    for pair, label in ((pair_a, label_a), (pair_b, label_b))
                ],
                each=0.45,
            ),
        )
    )
    scene.stop("metodo-comparacion")

    # El caso: la planta de San Bartolomé se levanta desde el núcleo.
    plan = draw_plan(
        scene,
        _center(plan_area),
        plan_area.right - plan_area.left,
        drawn_thickness=0.05,
        grid=False,
    )
    scene.play(
        stagger(
            case_rule.animate.grow_from_edge(Direction.LEFT).duration(0.5),
            parallel(
                plan.slab.animate.fade_in().duration(0.4),
                plan.void.animate.fade_in().duration(0.4),
            ),
            grow_walls(plan.all_walls, total=0.9, duration=0.4),
            enter(case_text, direction=Direction.UP, duration=0.35, each=0.1),
            enter(kind, direction=Direction.UP, duration=0.35, each=0.08),
            each=0.25,
        )
    )
    scene.stop("metodologia")


SECTION = Section(
    "objetivos",
    [
        SectionStep(
            name="Objetivos · general e hipótesis",
            build=purpose,
            transition=Transition.cross_fade(0.45),
            notes=(
                "60 s. Cuatro pausas. (1) Leer el objetivo general completo (§1.3.1). "
                "(2) Subrayar sus claves: marco de trabajo, automatización, albañilería "
                "confinada, norma E.070, interactuar, ETABS. (3) Esas palabras bajan y se "
                "relacionan en la hipótesis (§1.4): un marco automatizado, integrado con "
                "ETABS por su API, permitirá extraer y procesar los datos del modelo y "
                "ejecutar y documentar las verificaciones normativas, en albañilería "
                "confinada. (4) Variables (§1.5): método de diseño (manual o automatizado) "
                "y cumplimiento normativo."
            ),
        ),
        SectionStep(
            name="Objetivos · específicos",
            build=specific,
            transition=Transition.cross_fade(0.45),
            notes=(
                "30 s. Cada objetivo específico tiene un producto concreto en la tesis: el flujo "
                "manual (cap. 5), los diagramas de flujo del marco (cap. 6), el programa Alba "
                "conectado por API (cap. 7) y la comparación de modelos del caso (cap. 8). "
                "Los bloques siguientes recorren estos productos en el mismo orden."
            ),
        ),
        SectionStep(
            name="Objetivos · metodología",
            build=method,
            transition=Transition.cross_fade(0.45),
            notes=(
                "60 s. Cinco pausas, una por etapa. (1) Revisión normativa: análisis "
                "documental de la E.030 (espectro, sismo) y la E.070 (muro confinado). "
                "(2) Diagramas de flujo: cada verificación es proceso, decisión e iteración; "
                "si no cumple se vuelve a proponer la distribución. (3) Programa propio: Alba "
                "(Python) lee el modelo de ETABS por su API, procesa y redacta el reporte en "
                "Typst. (4) Comparación descriptiva: MCT frente a MSTA aísla la idealización "
                "(misma norma); MSTA frente a MSTO aísla la norma (misma idealización). "
                "(5) Todo sobre un caso: San Bartolomé (2006), muestra no probabilística. "
                "Nivel aplicativo y enfoque cuantitativo; no es una validación estadística."
            ),
        ),
    ],
)
