"""Símbolos de diagrama de flujo con la tipografía de la presentación."""

from gaanim import Anchor, Color, Drawable, Scene

from tesis.kit import t
from tesis.theme import CARD, INK, INK_SOFT, RULE

ARROW = {"head_length": 0.13, "head_width": 0.13, "body_width": 0.022}


def _label(
    scene: Scene, text: str, cx: float, cy: float, size: float, color: Color | str
) -> Drawable:
    return t(scene, text, cx, cy, size=size, color=color, anchor=Anchor.CENTER)


def process(
    scene: Scene,
    cx: float,
    cy: float,
    w: float,
    h: float,
    text: str,
    *,
    fill: Color | str = CARD,
    border: Color | str = RULE,
    size: float = 0.18,
    color: Color | str = INK,
) -> Drawable:
    box = scene.geometry.rect(w, h).fill(fill).stroke(border, 0.014).move_to(cx, cy)
    return scene.geometry.group([box, _label(scene, text, cx, cy, size, color)])


def io(
    scene: Scene,
    cx: float,
    cy: float,
    w: float,
    h: float,
    text: str,
    *,
    fill: Color | str = CARD,
    border: Color | str = RULE,
    size: float = 0.18,
    color: Color | str = INK,
) -> Drawable:
    k = 0.18
    shape = (
        scene.geometry.polygon(
            [
                (cx - w / 2 + k, cy + h / 2),
                (cx + w / 2 + k, cy + h / 2),
                (cx + w / 2 - k, cy - h / 2),
                (cx - w / 2 - k, cy - h / 2),
            ]
        )
        .fill(fill)
        .stroke(border, 0.014)
    )
    return scene.geometry.group([shape, _label(scene, text, cx, cy, size, color)])


def decision(
    scene: Scene,
    cx: float,
    cy: float,
    w: float,
    h: float,
    text: str,
    *,
    fill: Color | str = CARD,
    border: Color | str = RULE,
    size: float = 0.17,
    color: Color | str = INK,
) -> Drawable:
    shape = (
        scene.geometry.polygon(
            [(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)]
        )
        .fill(fill)
        .stroke(border, 0.014)
    )
    return scene.geometry.group([shape, _label(scene, text, cx, cy, size, color)])


def terminal(
    scene: Scene,
    cx: float,
    cy: float,
    text: str,
    *,
    w: float = 1.0,
    h: float = 0.46,
    fill: Color | str = INK,
    color: Color | str = "#FFFFFF",
    size: float = 0.17,
) -> Drawable:
    pill = (
        scene.geometry.rounded_rect(w, h, h / 2).fill(fill).no_stroke().move_to(cx, cy)
    )
    return scene.geometry.group([pill, _label(scene, text, cx, cy, size, color)])


def link(
    scene: Scene, *points: tuple[float, float], color: Color | str = INK_SOFT
) -> Drawable:
    start, *via, end = points
    return (
        scene.geometry.connector(start, end, via=via or None, **ARROW)
        .fill(color)
        .no_stroke()
    )
