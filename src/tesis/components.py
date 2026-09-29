"""Componentes de layout de la exposición, con el estilo editorial de la tesis.

Complementan a ``tesis.kit`` (que coloca por coordenadas): aquí cada pieza es una
caja de ``scene.layout`` que reparte su propio espacio. Cada componente devuelve una
``Box``; ``enter`` la revela pieza por pieza.

Unidades de diseño: el fotograma mide 1080 px de alto = 9 unidades de escena, es
decir 120 px por unidad.
"""

from gaanim import (
    Anchor,
    Box,
    Color,
    Direction,
    Drawable,
    Easing,
    Scene,
    component,
    stagger,
)

from tesis.theme import (
    BRICK,
    CAPTION,
    KICKER,
    TITLE,
    BRICK_DEEP,
    CARD,
    DISPLAY,
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

SIDE = "24px"  # margen lateral de la retícula (x = ±7.3 sobre un área segura de ±7.5)


@component
def page(
    scene: Scene,
    *,
    body: list[Drawable],
    top: str = "200px",
    bottom: str = "110px",
    gap: str = "40px",
    justify: str = "start",
) -> Box:
    """Columna raíz sobre el área segura, debajo del encabezado y encima de la fuente."""
    return scene.layout.column(
        *body,
        gap=gap,
        justify=justify,
        within="safe",
        width="fill",
        height="fill",
        padding=(top, SIDE, bottom, SIDE),
    )


@component
def hairline(
    scene: Scene, *, color: Color = RULE, thickness: str = "2px", width: str = "fill"
) -> Box:
    """Filete que ocupa el ancho disponible."""
    return scene.layout.box(width=width, height=thickness, background=color)


@component
def stat_card(
    scene: Scene, *, value: str, title: str, detail: str, color: Color = BRICK
) -> Box:
    """Cifra grande, afirmación y detalle bajo una barra de color.

    Estirada por su fila, la afirmación crece y empuja el detalle al fondo: los
    detalles de tarjetas vecinas quedan alineados aunque los títulos difieran.
    """
    L = scene.layout
    return L.box(
        L.box(width="fill", height="6px", background=color),
        L.box(value, font=DISPLAY, font_size="74px", weight=700, color=color),
        L.box(title, font_size="28px", weight=900, color=INK).item(grow=1),
        L.box(detail, font_size="24px", color=INK_SOFT),
        padding=("36px", "30px"),
        gap="24px",
        background=CARD,
        border=RULE,
        border_width="2px",
    ).item(grow=1)


@component
def numbered_row(scene: Scene, *, number: int, name: str, text: str) -> Box:
    """Fila de una lista numerada con marca de cumplido, sobre un filete."""
    L = scene.layout
    return L.column(
        L.row(
            L.box(
                f"{number}",
                font=DISPLAY,
                font_size="60px",
                weight=700,
                color=BRICK,
                width="60px",
            ).item(shrink=0),
            L.box(name, font_size="32px", weight=900, color=INK, width="230px").item(
                shrink=0
            ),
            L.box(text, font_size="27px", color=INK_SOFT).item(grow=1),
            scene.geometry.checkmark(0.26).stroke(PASS, 0.05).no_fill(),
            gap="28px",
            align="center",
            width="fill",
        ),
        hairline(scene, color="#E6E0D5"),
        gap="18px",
        width="fill",
    )


@component
def column_list(
    scene: Scene,
    *,
    title: str,
    items: list[str],
    color: Color = BRICK,
    size: str = "30px",
    gap: str = "34px",
) -> Box:
    """Encabezado de columna sobre un filete de su color y una lista con guiones."""
    L = scene.layout
    rows = [
        L.row(
            L.box(width="20px", height="3px", background=color).item(shrink=0),
            L.box(item, font_size=size, color=INK),
            gap="20px",
            align="center",
        )
        for item in items
    ]
    return L.column(
        L.box(title, font_size="31px", weight=900, color=color),
        hairline(scene, color=color, thickness="3px"),
        *rows,
        gap=gap,
        width="fill",
    ).item(grow=1)


@component
def takeaway(
    scene: Scene,
    *,
    text: str,
    tag: str | None = None,
    tag_color: Color = PASS,
    display: bool = True,
) -> Box:
    """Mensaje final bajo un filete fino; con ``tag``, un rótulo en versalitas encima.

    ``display`` usa Aleo (cita); sin él, Lato en negrita (enunciado).
    """
    L = scene.layout
    body = (
        L.box(text, font=DISPLAY, font_size="32px", weight=700, color=INK, width="85%")
        if display
        else L.box(text, font_size="27px", weight=700, color=INK)
    )
    label = (
        [
            L.box(
                tag.upper(),
                font_size="17px",
                weight=900,
                color=tag_color,
                letter_spacing=0.03,
            )
        ]
        if tag
        else []
    )
    return L.column(hairline(scene), *label, body, gap="20px", width="fill")


@component
def note(
    scene: Scene,
    *,
    text: str,
    color: Color = MUTED,
    size: str = "17px",
    upper: bool = True,
) -> Box:
    """Rótulo técnico en mayúsculas espaciadas (o nota corrida si ``upper`` es falso)."""
    return scene.layout.box(
        text.upper() if upper else text,
        font_size=size,
        weight=900 if upper else 400,
        color=color,
        letter_spacing=0.03 if upper else 0,
    )


@component
def objective_card(
    scene: Scene, *, number: int, verb: str, text: str, product: str
) -> Box:
    """Tarjeta de un objetivo: número, verbo, enunciado y producto en tipografía técnica.

    El enunciado crece, así el producto queda al fondo aunque los textos difieran.
    """
    L = scene.layout
    return L.box(
        L.box(f"{number}", font=DISPLAY, font_size="108px", weight=700, color=BRICK),
        L.box(verb, font_size="43px", weight=900, color=INK),
        L.box(text, font_size="28px", color=INK_SOFT).item(grow=1),
        L.box(product, font=MONO, font_size="19px", color=BRICK_DEEP),
        padding="36px",
        gap="20px",
        background=CARD,
        border=RULE,
        border_width="2px",
    ).item(grow=1)


@component
def fact(scene: Scene, *, name: str, value: str) -> Box:
    """Dato de la ficha metodológica: filete, rótulo y valor en Aleo."""
    L = scene.layout
    return L.column(
        hairline(scene, thickness="2px"),
        note(scene, text=name, size="17px"),
        L.box(value, font=DISPLAY, font_size="43px", weight=700, color=INK),
        gap="14px",
    ).item(grow=1)


@component
def step(scene: Scene, *, number: int, name: str, text: str, last: bool = False) -> Box:
    """Etapa numerada: un círculo unido por un filete a la siguiente, y su descripción."""
    L = scene.layout
    circle = L.box(
        f"{number}",
        width="72px",
        height="72px",
        radius="full",
        background=STEEL_SOFT,
        border=STEEL,
        border_width="3px",
        align="center",
        justify="center",
        font=DISPLAY,
        font_size="36px",
        weight=700,
        color=STEEL,
    ).item(shrink=0)
    link = [] if last else [hairline(scene, color=STEEL, thickness="3px")]
    return L.column(
        L.row(circle, *link, gap="12px", align="center", width="fill"),
        L.box(name, font_size="29px", weight=900, color=INK),
        L.box(text, font_size="23px", color=INK_SOFT),
        gap="16px",
    ).item(grow=1)


def enter(
    box: Box,
    *,
    direction: Direction = Direction.LEFT,
    distance: float = 0.06,
    duration: float = 0.35,
    each: float = 0.07,
):
    """Revela una caja pieza por pieza, en cascada, del fondo al frente."""
    return box.reveal(
        direction=direction, distance=distance, duration=duration, each=each
    )


@component
def image_card(
    scene: Scene,
    *,
    picture: Drawable,
    value: str,
    unit: str,
    body: str,
    color: Color = BRICK,
) -> Box:
    """Tarjeta con una captura arriba, una cifra en Aleo, su rótulo y una explicación.

    La explicación crece: las tarjetas vecinas terminan a la misma altura.
    """
    L = scene.layout
    return L.box(
        L.box(picture, width="fill", height="300px", align="center", justify="center"),
        L.box(value, font=DISPLAY, font_size="62px", weight=700, color=color),
        note(scene, text=unit, color=color, size="17px"),
        L.box(body, font_size="24px", color=INK_SOFT).item(grow=1),
        gap="18px",
        padding=("30px", "30px", "30px", "30px"),
        background=CARD,
        border=RULE,
        border_width="2px",
        width="fill",
        height="fill",
    ).item(grow=1)


ROW_HEIGHT = "84px"
HEADING_HEIGHT = "84px"


@component
def role_column(
    scene: Scene, *, title: str, rows: list[tuple[str, str]], color: Color = BRICK
) -> Box:
    """Rol con su nombre sobre un filete de color y filas «acción — descripción».

    El encabezado y las filas tienen altura fija: dos columnas vecinas (y la que
    las une, ver ``arrow_slot``) quedan alineadas fila a fila.
    """
    L = scene.layout
    body = [
        L.row(
            L.box(head, font_size="30px", weight=900, color=INK, width="300px").item(
                shrink=0
            ),
            L.box(text, font_size="28px", color=INK_SOFT),
            align="center",
            width="fill",
            height=ROW_HEIGHT,
        )
        for head, text in rows
    ]
    return L.column(
        L.box(
            title,
            font_size="34px",
            weight=900,
            color=color,
            height=HEADING_HEIGHT,
            width="fill",
            justify="end",
            padding=("0px", "0px", "12px", "0px"),
        ),
        hairline(scene, color=color, thickness="3px"),
        *body,
        gap="0px",
        width="fill",
    ).item(grow=1)


@component
def arrow_gutter(
    scene: Scene, *, slots: list[tuple[str, bool] | None], width: str = "220px"
) -> Box:
    """Columna entre dos ``role_column``: una flecha rotulada por fila indicada.

    ``slots`` tiene una entrada por fila: ``(rótulo, hacia_la_derecha)`` o ``None``.
    """
    L = scene.layout
    cells: list[Box] = []
    for slot in slots:
        if slot is None:
            cells.append(L.box(width="fill", height=ROW_HEIGHT))
            continue
        text, rightwards = slot
        x0, x1 = (0.0, 1.5) if rightwards else (1.5, 0.0)
        arrow = scene.geometry.arrow(x0, 0, x1, 0).fill(MUTED).no_stroke()
        cells.append(
            L.column(
                L.box(text, font_size="22px", color=MUTED),
                arrow,
                gap="4px",
                align="center",
                justify="center",
                width="fill",
                height=ROW_HEIGHT,
            )
        )
    return L.column(
        L.box(width="fill", height="87px"),
        *cells,
        width=width,
    ).item(shrink=0)


@component
def chip(
    scene: Scene,
    *,
    text: str,
    color: Color = INK,
    background: Color = PAPER_DEEP,
    border: Color | None = None,
    font: str = MONO,
    width: str | None = None,
) -> Box:
    """Etiqueta compacta de esquinas rectas, en tipografía técnica."""
    props: dict[str, str] = {"border": border, "border_width": "2px"} if border else {}
    if width:
        props["width"] = width
    return scene.layout.box(
        text,
        font=font,
        font_size="24px",
        color=color,
        background=background,
        padding=("10px", "18px"),
        **props,
    )


LABEL_WIDTH = "470px"


@component
def compare_table(
    scene: Scene,
    *,
    columns: list[tuple[str, str, Color, Color]],
    rows: list[tuple[str, list[tuple[str, bool, Color]]]],
) -> Box:
    """Tabla de comparación: una columna por modelo bajo su encabezado de color.

    ``columns`` da ``(nombre, subtítulo, color, fondo)``; ``rows`` da el aspecto y, por
    columna, ``(texto, resaltado, color)``. Los rótulos y las celdas comparten anchos,
    así las filas quedan alineadas sin coordenadas.
    """
    L = scene.layout
    head = L.row(
        L.box(width=LABEL_WIDTH).item(shrink=0),
        *[
            L.column(
                L.box(name, font=DISPLAY, font_size="40px", weight=700, color=color),
                L.box(sub, font_size="22px", color=INK_SOFT),
                gap="4px",
                align="center",
                padding=("22px", "10px"),
                background=soft,
                width="fill",
            ).item(grow=1)
            for name, sub, color, soft in columns
        ],
        gap="12px",
        width="fill",
    )
    body = [
        L.column(
            L.row(
                L.box(
                    aspect, font_size="26px", weight=700, color=INK, width=LABEL_WIDTH
                ).item(shrink=0),
                *[
                    L.box(
                        text,
                        font_size="26px",
                        weight=900 if bold else 400,
                        color=color,
                        align="center",
                        width="fill",
                    ).item(grow=1)
                    for text, bold, color in cells
                ],
                gap="12px",
                align="center",
                width="fill",
            ),
            hairline(scene, color="#E6E0D5"),
            gap="12px",
            width="fill",
        )
        for aspect, cells in rows
    ]
    return L.column(head, *body, gap="12px", width="fill")


PX = 120.0  # px de diseño por unidad de escena
SAFE_TOP = 60.0  # el área segura empieza a 60 px del borde del fotograma


def _px(units: float) -> str:
    return f"{units * PX:.1f}px"


@component
def header_block(scene: Scene, *, kicker: str, title: str) -> Box:
    """Kicker en versalitas terracota y título-afirmación en Aleo, en la esquina superior."""
    L = scene.layout
    return L.column(
        scene.text(kicker.upper(), style=KICKER),
        scene.text(title, style=TITLE, wrap=False),
        gap="5px",
        within="safe",
        width="fill",
        height="fill",
        justify="start",
        padding=("2px", SIDE, "0px", SIDE),
    )


def header(scene: Scene, kicker: str, title: str) -> Box:
    """Coloca el encabezado y lo anima: el título sube palabra por palabra."""
    block = header_block(scene, kicker=kicker, title=title)
    kick, head = block.children
    scene.play(
        stagger(
            kick.animate.fade_in_from(Direction.RIGHT, 0.12)
            .duration(0.5)
            .easing(Easing.SMOOTH_SPRING),
            head.animate.reveal(style="slide_up", by="word", stagger=0.045).duration(
                0.9
            ),
            each=0.12,
        )
    )
    return block


@component
def source_block(scene: Scene, *, reference: str) -> Box:
    """Fuente de la diapositiva, sobre el riel de avance (a y = -3.72)."""
    return scene.layout.column(
        scene.text(reference, style=CAPTION, wrap=False),
        within="safe",
        width="fill",
        height="fill",
        justify="start",
        padding=(f"{(4.5 + 3.72) * PX - SAFE_TOP - 3:.1f}px", SIDE, "0px", SIDE),
    )


def source(scene: Scene, reference: str) -> Box:
    block = source_block(scene, reference=reference)
    scene.play(block.animate.fade_in().duration(0.3))
    return block


@component
def takeaway_block(scene: Scene, *, text: str, y: float, color: Color = INK) -> Box:
    """Frase final en Aleo bajo un filete; ``y`` es el centro vertical de la frase."""
    L = scene.layout
    rule_y = y + 0.36
    return L.column(
        hairline(scene, thickness="2px"),
        scene.text(text, font=DISPLAY, size=0.3, weight=700, color=color),
        gap="18px",
        within="safe",
        width="fill",
        height="fill",
        justify="start",
        padding=(f"{(4.5 - rule_y) * PX - SAFE_TOP - 1:.1f}px", SIDE, "0px", SIDE),
    )


def takeaway_at(
    scene: Scene, content: str, y: float = -3.05, *, color: Color = INK
) -> Box:
    """Mensaje final de la diapositiva: filete fino encima y frase en Aleo."""
    block = takeaway_block(scene, text=content, y=y, color=color)
    rule, text = block.children
    scene.play(
        [
            rule.animate.grow_from_edge(Direction.LEFT).duration(0.5),
            text.animate.reveal(style="slide_up", by="word", stagger=0.03).duration(
                0.7
            ),
        ]
    )
    return block


@component
def pill_box(
    scene: Scene,
    *,
    text: str,
    color: Color,
    background: Color,
    border: Color | None,
    size: float,
    font: str,
    weight: int | None,
    pad: tuple[float, float],
) -> Box:
    return scene.layout.box(
        text,
        font=font,
        font_size=_px(size),
        weight=weight,
        color=color,
        background=background,
        border=border if border is not None else background,
        border_width="2px",
        padding=(_px(pad[1]), _px(pad[0])),
    )


def pill(
    scene: Scene,
    content: str,
    x: float,
    y: float,
    *,
    color: Color = INK_SOFT,
    background: Color = CARD,
    border: Color | None = None,
    size: float = 0.19,
    font: str = MONO,
    weight: int | None = None,
    pad: tuple[float, float] = (0.16, 0.07),
    anchor: Anchor = Anchor.CENTER,
) -> Box:
    """Etiqueta compacta de esquinas rectas; se ubica por su centro o una esquina."""
    return pill_box(
        scene,
        text=content,
        color=color,
        background=background,
        border=border,
        size=size,
        font=font,
        weight=weight,
        pad=pad,
    ).move_to(x, y, anchor)


@component
def panel_box(
    scene: Scene, *, w: float, h: float, fill: Color, border: Color | None
) -> Box:
    return scene.layout.box(
        width=_px(w),
        height=_px(h),
        background=fill,
        border=border,
        border_width="2px" if border is not None else "0px",
    )


def panel(
    scene: Scene,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: Color = CARD,
    border: Color | None = RULE,
    anchor: Anchor = Anchor.CENTER,
) -> Box:
    """Recuadro de esquinas rectas con filete fino, colocado por coordenadas."""
    return panel_box(scene, w=w, h=h, fill=fill, border=border).move_to(x, y, anchor)
