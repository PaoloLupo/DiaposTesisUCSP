"""Componentes editoriales compartidos por todas las diapositivas.

Retícula de 16 × 9 unidades: margen lateral en x = ±7.3, encabezado sobre
y = 2.75, contenido entre y = 2.5 e y = -3.5, fuente en y = -3.8 y el riel de
avance debajo de y = -4.1.
"""

from gaanim import (
    Anchor,
    Color,
    Direction,
    Drawable,
    Scene,
    Text,
    TextFlow,
    TextStyle,
    stagger,
)

from tesis.theme import (
    BODY,
    BRICK,
    CAPTION,
    CARD,
    CENTER,
    DISPLAY,
    FAIL,
    FAIL_SOFT,
    INK,
    INK_SOFT,
    KICKER,
    LEFT,
    MONO,
    MUTED,
    PASS,
    PASS_SOFT,
    RIGHT,
    RULE,
    SANS,
    TITLE,
)

LEFT_EDGE = -7.3
RIGHT_EDGE = 7.3


def plain(content: str) -> str:
    """Escapa `_` fuera de `$...$`: la marca `_x_` de Gaanim es cursiva, no subíndice."""
    pieces = content.split("$")
    for i in range(0, len(pieces), 2):
        pieces[i] = pieces[i].replace("\\_", "_").replace("_", "\\_")
    return "$".join(pieces)


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
    flow: TextFlow | None = None,
) -> Text:
    """Texto posicionado por una esquina o su centro; alineación según el ancla."""
    if flow is None:
        if anchor in (Anchor.TOP, Anchor.CENTER, Anchor.BOTTOM):
            flow = CENTER
        elif anchor in (Anchor.TOP_RIGHT, Anchor.RIGHT, Anchor.BOTTOM_RIGHT):
            flow = RIGHT
        else:
            flow = LEFT
    return scene.text(
        plain(content),
        style=style,
        flow=flow,
        size=size,
        color=color,
        weight=weight,
        font=font,
    ).move_to(x, y, anchor)


def header(
    scene: Scene, kicker: str, title: str, *, rule: bool = True
) -> list[Drawable]:
    """Kicker en versalitas terracota y título-afirmación en Aleo."""
    kick = t(scene, kicker.upper(), LEFT_EDGE, 3.98, style=KICKER)
    head = t(scene, title, LEFT_EDGE, 3.66, style=TITLE)
    items: list[Drawable] = [kick, head]
    anims = [
        kick.animate.fade_in_from(Direction.RIGHT, 0.12).duration(0.45),
        head.animate.fade_in_from(Direction.UP, 0.10).duration(0.6),
    ]
    if rule:
        line = scene.geometry.line(LEFT_EDGE, 2.78, RIGHT_EDGE, 2.78).stroke(
            RULE, 0.012
        )
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
    color: Color | str = INK_SOFT,
    background: Color | str = CARD,
    border: Color | str | None = None,
    size: float = 0.19,
    font: str = MONO,
    weight: int | None = None,
    pad: tuple[float, float] = (0.16, 0.07),
    anchor: Anchor = Anchor.CENTER,
) -> Drawable:
    """Etiqueta compacta con fondo redondeado; se ubica por su centro o una esquina."""
    content = plain(content)
    width, height = scene.text.measure(content, size=size, font=font)
    w = width + 2 * pad[0]
    h = max(height, size * 0.9) + 2 * pad[1]
    cx, cy = _anchor_center(x, y, w, h, anchor)
    box = scene.geometry.rounded_rect(w, h, h / 2).fill(background)
    box = box.stroke(border, 0.012) if border is not None else box.no_stroke()
    box.move_to(cx, cy)
    label = scene.text(
        content, size=size, font=font, color=color, weight=weight, flow=CENTER
    )
    label.move_to(cx, cy, Anchor.CENTER)
    return scene.geometry.group([box, label])


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
    cx, cy = _anchor_center(x, y, w, h, anchor)
    box = scene.geometry.rounded_rect(w, h, radius).fill(fill)
    box = box.stroke(border, 0.014) if border is not None else box.no_stroke()
    return box.move_to(cx, cy)


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
    offset: float = 0.35,
    color: Color | str = MUTED,
    size: float = 0.15,
    width: float = 0.01,
) -> Drawable:
    """Cota de plano: línea desplazada, marcas a 45° y rótulo centrado."""
    (x0, y0), (x1, y1) = start, end
    horizontal = abs(y1 - y0) < abs(x1 - x0)
    if horizontal:
        a, b = (x0, y0 + offset), (x1, y1 + offset)
        ext = [
            (
                (x0, y0 + 0.04 * (1 if offset > 0 else -1)),
                (x0, a[1] + 0.06 * (1 if offset > 0 else -1)),
            ),
            (
                (x1, y1 + 0.04 * (1 if offset > 0 else -1)),
                (x1, b[1] + 0.06 * (1 if offset > 0 else -1)),
            ),
        ]
    else:
        a, b = (x0 + offset, y0), (x1 + offset, y1)
        ext = [
            (
                (x0 + 0.04 * (1 if offset > 0 else -1), y0),
                (a[0] + 0.06 * (1 if offset > 0 else -1), y0),
            ),
            (
                (x1 + 0.04 * (1 if offset > 0 else -1), y1),
                (b[0] + 0.06 * (1 if offset > 0 else -1), y1),
            ),
        ]
    parts: list[Drawable] = [scene.geometry.line(a, b).stroke(color, width)]
    parts += [scene.geometry.line(p, q).stroke(color, width) for p, q in ext]
    for px, py in (a, b):
        parts.append(
            scene.geometry.line((px - 0.06, py - 0.06), (px + 0.06, py + 0.06)).stroke(
                color, width * 1.8
            )
        )
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    if horizontal:
        tag = t(
            scene,
            text,
            mx,
            my + (0.06 if offset > 0 else -0.06),
            font=MONO,
            size=size,
            color=color,
            anchor=Anchor.BOTTOM if offset > 0 else Anchor.TOP,
        )
    else:
        tag = t(
            scene,
            text,
            mx + (0.08 if offset > 0 else -0.08),
            my,
            font=MONO,
            size=size,
            color=color,
            anchor=Anchor.LEFT if offset > 0 else Anchor.RIGHT,
        )
    parts.append(tag)
    return scene.geometry.group(parts)


def _anchor_center(
    x: float, y: float, w: float, h: float, anchor: Anchor
) -> tuple[float, float]:
    dx = {
        Anchor.LEFT: 1,
        Anchor.TOP_LEFT: 1,
        Anchor.BOTTOM_LEFT: 1,
        Anchor.RIGHT: -1,
        Anchor.TOP_RIGHT: -1,
        Anchor.BOTTOM_RIGHT: -1,
    }.get(anchor, 0)
    dy = {
        Anchor.TOP: -1,
        Anchor.TOP_LEFT: -1,
        Anchor.TOP_RIGHT: -1,
        Anchor.BOTTOM: 1,
        Anchor.BOTTOM_LEFT: 1,
        Anchor.BOTTOM_RIGHT: 1,
    }.get(anchor, 0)
    return x + dx * w / 2, y + dy * h / 2
