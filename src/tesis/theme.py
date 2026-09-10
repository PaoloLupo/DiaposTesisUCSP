from typing import Literal, TypedDict

from gaanim import BLACK, Anchor, Color, TextFlow, TextStyle


class ArrowStyle(TypedDict):
    head_length: float
    head_width: float
    body_width: float


class NodeCardStyle(TypedDict):
    direction: Literal["column", "row", "stack"]
    width: float
    height: float
    padding: float
    border: Color | str
    border_width: float
    radius: float
    ports: dict[str, Anchor | tuple[Anchor, tuple[float, float]]]


ACCENT = Color.from_hex("#e26d5c")
INK_MUTED = "#626878"
RULE = "#C9CDDA"
WARM = "#B7791F"

BODY = TextStyle(size=0.28, color=BLACK)
HEADING = TextStyle(size=0.5, color=BLACK)
NODE_TITLE = TextStyle(size=0.32, color=BLACK)
NODE_BODY = TextStyle(size=0.24, color=Color(INK_MUTED))
NODE_NUMBER = TextStyle(size=0.23, color=ACCENT)
LEFT_FLOW = TextFlow(align="left", line_spacing=1.18)
CENTER_FLOW = TextFlow(align="center", line_spacing=1.18)
ARROW_STYLE: ArrowStyle = {"head_length": 0.18, "head_width": 0.15, "body_width": 0.036}
NODE_CARD: NodeCardStyle = {
    "direction": "stack", "width": 3.8, "height": 1.75, "padding": 0,
    "border": RULE, "border_width": 0.025, "radius": 0.08,
    "ports": {
        "entrada": (Anchor.LEFT, (-0.10, 0)),
        "salida": (Anchor.RIGHT, (0.05, 0)),
        "retorno_inicio": (Anchor.BOTTOM, (0, -1.225)),
        "retorno_bajada": (Anchor.BOTTOM, (0, -1.775)),
        "retorno_inferior": (Anchor.LEFT, (-0.2, -2.65)),
        "retorno_giro": (Anchor.LEFT, (-0.2, 0)),
        "retorno_fin": (Anchor.LEFT, (-0.01, 0)),
    },
}
