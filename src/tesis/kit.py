"""Primitivas de coordenadas compartidas por las diapositivas.

Las piezas compuestas (encabezado, fuente, frase final, etiquetas, recuadros) viven
en ``tesis.components`` como cajas de layout; aquí quedan el texto posicionado, los
rótulos, las cotas y los ayudantes de animación.


Retícula de 16 × 9 unidades: margen lateral en x = ±7.3, encabezado sobre
y = 2.75, contenido entre y = 2.5 e y = -3.5, fuente en y = -3.8 y el riel de
avance debajo de y = -4.1.
"""

from typing import Literal

from gaanim import (
    Anchor,
    Color,
    Direction,
    Drawable,
    Scene,
    Text,
    TextStyle,
    stagger,
)

from tesis.theme import (
    BODY,
    BRICK,
    DISPLAY,
    FAIL,
    MONO,
    MUTED,
    PASS,
    SANS,
)

LEFT_EDGE = -7.3
RIGHT_EDGE = 7.3


def t(
    scene: Scene,
    content: str,
    x: float,
    y: float,
    *,
    style: TextStyle = BODY,
    size: float | None = None,
    color: Color | str | None = None,
    weight: int | None = None,
    font: str | None = None,
    anchor: Anchor = Anchor.TOP_LEFT,
) -> Text:
    """Texto posicionado por una esquina o su centro; las líneas se alinean según el ancla.

    ``*`` y ``_`` son literales (``Theme(text_markup=False)``); los subíndices se
    escriben como matemática: ``"$V_e$"``.
    """
    return scene.text(
        content, style=style, size=size, color=color, weight=weight, font=font
    ).move_to(x, y, anchor)


def status(
    scene: Scene,
    ok: bool,
    x: float,
    y: float,
    *,
    anchor: Anchor = Anchor.CENTER,
    size: float = 0.2,
) -> Drawable:
    """Diagnóstico como texto: «✓ Cumple» en verde o «✕ No cumple» en rojo, sin fondo."""
    return t(
        scene,
        "✓ Cumple" if ok else "✕ No cumple",
        x,
        y,
        size=size,
        color=PASS if ok else FAIL,
        weight=900,
        anchor=anchor,
    )


def dash(scene: Scene, x: float, y: float, *, color: Color = MUTED) -> Drawable:
    """Raya corta como marcador de lista, centrada en ``(x, y)``."""
    return scene.geometry.rect(0.16, 0.024).fill(color).no_stroke().move_to(x, y)


def numeral(
    scene: Scene,
    value: str,
    x: float,
    y: float,
    *,
    color: Color = BRICK,
    size: float = 0.5,
    anchor: Anchor = Anchor.TOP_LEFT,
) -> Text:
    return t(
        scene,
        value,
        x,
        y,
        font=DISPLAY,
        size=size,
        color=color,
        weight=700,
        anchor=anchor,
    )


def label(
    scene: Scene,
    content: str,
    x: float,
    y: float,
    *,
    color: Color | str = MUTED,
    size: float = 0.15,
    anchor: Anchor = Anchor.TOP_LEFT,
) -> Text:
    """Rótulo técnico en mayúsculas espaciadas."""
    return t(
        scene,
        content.upper(),
        x,
        y,
        font=SANS,
        size=size,
        weight=900,
        color=color,
        anchor=anchor,
        style=TextStyle(letter_spacing=0.03),
    )


def appear(
    *items: Drawable,
    each: float = 0.08,
    duration: float = 0.5,
    direction: Direction = Direction.UP,
    distance: float = 0.1,
):
    return stagger(
        *[
            item.animate.fade_in_from(direction, distance).duration(duration)
            for item in items
        ],
        each=each,
    )


def fade(*items: Drawable, duration: float = 0.4):
    return [item.animate.fade_in().duration(duration) for item in items]


def dimension(
    scene: Scene,
    start: tuple[float, float],
    end: tuple[float, float],
    text: str,
    *,
    side: Literal["left", "right", "above", "below"],
    offset: float = 0.35,
    color: Color = MUTED,
    size: float = 0.15,
    width: float = 0.01,
) -> Drawable:
    """Cota de plano en IBM Plex Mono, a ``offset`` del segmento por el lado ``side``.

    Como en los planos, el rótulo de una cota vertical se lee girado.
    """
    return scene.mechanics.dimension_between(
        start,
        end,
        offset,
        side=side,
        label=text,
        label_orientation="aligned" if side in ("left", "right") else "upright",
        font=MONO,
        font_size=size,
        color=color,
        line_width=width,
    )
