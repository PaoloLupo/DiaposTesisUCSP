"""Componentes de layout de la exposición, con el estilo editorial de la tesis.

Complementan a ``tesis.kit`` (que coloca por coordenadas): aquí cada pieza es una
caja de ``scene.layout`` que reparte su propio espacio. Cada componente devuelve una
``Box``; ``enter`` la revela pieza por pieza.

Unidades de diseño: el fotograma mide 1080 px de alto = 9 unidades de escena, es
decir 120 px por unidad.
"""

from gaanim import Box, Color, Direction, Drawable, Scene, component

from tesis.theme import (
    BRICK,
    BRICK_DEEP,
    CARD,
    DISPLAY,
    INK,
    INK_SOFT,
    MONO,
    MUTED,
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
                f"{number}", font=DISPLAY, font_size="60px", weight=700, color=BRICK,
                width="60px",
            ).item(shrink=0),
            L.box(
                name, font_size="32px", weight=900, color=INK, width="230px"
            ).item(shrink=0),
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
    scene: Scene, *, title: str, items: list[str], color: Color = BRICK
) -> Box:
    """Encabezado de columna sobre un filete de su color y una lista con guiones."""
    L = scene.layout
    rows = [
        L.row(
            L.box(width="20px", height="3px", background=color).item(shrink=0),
            L.box(item, font_size="30px", color=INK),
            gap="20px",
            align="center",
        )
        for item in items
    ]
    return L.column(
        L.box(title, font_size="31px", weight=900, color=color),
        hairline(scene, color=color, thickness="3px"),
        *rows,
        gap="34px",
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
        [L.box(tag.upper(), font_size="17px", weight=900, color=tag_color, letter_spacing=0.03)]
        if tag
        else []
    )
    return L.column(hairline(scene), *label, body, gap="20px", width="fill")


@component
def note(
    scene: Scene, *, text: str, color: Color = MUTED, size: str = "17px", upper: bool = True
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
    """Revela una caja pieza por pieza, en cascada, del fondo al frente.

    Un filete o una barra (una caja sin hijos) crece desde el borde; lo demás
    entra desplazándose."""

    def make(piece):
        if isinstance(piece, Box) and not len(piece):
            anim = piece.animate.grow_from_edge(Direction.LEFT)
        else:
            anim = piece.animate.fade_in_from(direction, distance)
        return anim.duration(duration)

    return box.stagger(make, each=each)


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
