"""Identidad visual: papel cálido, tinta y terracota de ladrillo.

Los colores tienen significado estable en toda la exposición:

- BRICK: albañilería, dirección X y el modelo MCT (procesado con Alba).
- STEEL: dirección Y, estructura y el modelo MSTA.
- CONCRETE: concreto armado y el modelo MSTO de referencia.
- PASS / FAIL: solo para diagnósticos de cumplimiento.
"""

from pathlib import Path

from gaanim import Color, TextStyle, Theme

FONTS_DIR = Path(__file__).resolve().parents[2] / "assets" / "fonts"

# Papel y tinta
PAPER = Color.from_hex("#F6F3EC")
PAPER_DEEP = Color.from_hex("#ECE7DD")
CARD = Color.from_hex("#FBF9F5")
INK = Color.from_hex("#1D2129")
INK_SOFT = Color.from_hex("#4B515D")
MUTED = Color.from_hex("#8B8F98")
RULE = Color.from_hex("#D9D3C7")
FAINT = Color.from_hex("#E6E1D6")

# Semántica
BRICK = Color.from_hex("#B8532F")
BRICK_SOFT = Color.from_hex("#F2DED3")
BRICK_DEEP = Color.from_hex("#8E3B1F")
STEEL = Color.from_hex("#2E5B87")
STEEL_SOFT = Color.from_hex("#DCE5EF")
CONCRETE = Color.from_hex("#8A8D93")
CONCRETE_SOFT = Color.from_hex("#E4E3E0")
PASS = Color.from_hex("#2E7A58")
PASS_SOFT = Color.from_hex("#DCEDE3")
FAIL = Color.from_hex("#B42E24")
FAIL_SOFT = Color.from_hex("#F5DCD8")
GOLD = Color.from_hex("#C4902C")

MODEL_COLORS = {"MCT": BRICK, "MSTA": STEEL, "MSTO": CONCRETE}
DIRECTION_COLORS = {"X": BRICK, "Y": STEEL}

# Tipografía
DISPLAY = "Aleo"
SANS = "Lato"
MONO = "IBM Plex Mono"

TITLE = TextStyle(font=DISPLAY, size=0.50, weight=700, color=INK)
KICKER = TextStyle(font=SANS, size=0.17, weight=900, color=BRICK, letter_spacing=0.035)
BODY = TextStyle(font=SANS, size=0.30, color=INK)
SMALL = TextStyle(font=SANS, size=0.23, color=INK_SOFT)
CAPTION = TextStyle(font=SANS, size=0.17, color=MUTED)
TAG = TextStyle(font=MONO, size=0.19, color=INK_SOFT)


def build_theme() -> Theme:
    # font_dir registra cada cara por la familia y el peso que declara su archivo;
    # text_markup=False deja `*` y `_` literales (`tb:dist_comp`) en todo texto.
    return Theme(
        "paper",
        name="tesis-ladrillo",
        colors={
            "background": PAPER,
            "foreground": INK,
            "muted": MUTED,
            "title": INK,
            "accent": BRICK,
            "chart": BRICK,
            "panel": CARD,
            "header": PAPER_DEEP,
            "rule": RULE,
        },
        fonts={"text": SANS, "code": MONO},
        font_dir=FONTS_DIR,
        text_markup=False,
    )
