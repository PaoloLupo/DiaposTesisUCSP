"""Componentes editoriales compartidos por todas las diapositivas.

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
    CAPTION,
    CARD,
    DISPLAY,
    FAIL,
    FAIL_SOFT,
    INK,
    INK_SOFT,
    KICKER,
    MONO,
    MUTED,
    PASS,
    PASS_SOFT,
    RULE,
    SANS,
    TITLE,
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


def header(
    scene: Scene, kicker: str, title: str, *, rule: bool = False
) -> list[Drawable]:
    """Kicker en versalitas terracota y título-afirmación en Aleo."""
    kick = t(scene, kicker.upper(), LEFT_EDGE, 3.98, style=KICKER)
    head = t(scene, title, LEFT_EDGE, 3.66, style=TITLE)
    items: list[Drawable] = [kick, head]
    anims = [
        kick.animate.fade_in_from(Direction.RIGHT, 0.12).duration(0.45),
        head.animate.write().duration(1),
    ]
    if rule:
        line = scene.geometry.line(length= RIGHT_EDGE- LEFT_EDGE).stroke(
            RULE, 0.012
        ).next_to(head, Direction.DOWN)
        items.append(line)
        anims.append(line.animate.create().duration(0.6))
    scene.play(stagger(*anims, each=0.12))
    return items


def source(scene: Scene, reference: str) -> Text:
    caption = t(scene, reference, LEFT_EDGE, -3.72, style=CAPTION)
    scene.play(caption.animate.fade_in().duration(0.3))
    return caption


def takeaway(
    scene: Scene, content: str, y: float = -3.05, *, color: Color = INK
) -> Drawable:
    """Mensaje final de la diapositiva: marca terracota + frase en negrita."""
    mark = (
        scene.geometry.rect(0.07, 0.34)
        .fill(BRICK)
        .no_stroke()
        .move_to(LEFT_EDGE + 0.035, y)
    )
    text = t(
        scene,
        content,
        LEFT_EDGE + 0.3,
        y,
        size=0.3,
        color=color,
        weight=700,
        anchor=Anchor.LEFT,
    )
    scene.play(
        [
            mark.animate.grow_from_center().duration(0.35),
            text.animate.fade_in_from(Direction.LEFT, 0.12).duration(0.55),
        ]
    )
    return scene.geometry.group([mark, text])


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
) -> Drawable:
    """Etiqueta compacta con fondo redondeado; se ubica por su centro o una esquina."""
    return scene.slides.badge(
        content,
        padding=pad,
        font_size=size,
        font=font,
        weight=weight,
        color=color,
        background=background,
        border=border if border is not None else background,
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
    """Chip de diagnóstico: CUMPLE en verde o NO CUMPLE en rojo."""
    return pill(
        scene,
        "✓  CUMPLE" if ok else "✕  NO CUMPLE",
        x,
        y,
        color=PASS if ok else FAIL,
        background=PASS_SOFT if ok else FAIL_SOFT,
        size=size,
        font=SANS,
        weight=900,
        anchor=anchor,
    )


def panel(
    scene: Scene,
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: Color | str = CARD,
    border: Color | str | None = RULE,
    radius: float = 0.12,
    anchor: Anchor = Anchor.CENTER,
) -> Drawable:
    box = scene.geometry.rounded_rect(w, h, radius).fill(fill)
    box = box.stroke(border, 0.014) if border is not None else box.no_stroke()
    return box.move_to(x, y, anchor)


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
