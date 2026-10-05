"""Recorta el reporte de Alba del anexo de la tesis para la diapositiva del reporte.

Genera ``assets/reporte/portada.png`` y una imagen por sección, con la misma
proporción 4:3. Se corre a mano si cambia el anexo:

    uv run --no-project --with pymupdf python tools/render_report.py
"""

from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "TesisUCSP/archivos/anexos/EjemploBartolome.pdf"
OUT = ROOT / "assets/reporte"

# (archivo, página 1-based, y superior del recorte en pt). Ancho útil 40–555 pt.
SECTIONS = [
    ("datos.png", 3, 40),
    ("requisitos.png", 6, 40),
    ("carga-vertical.png", 8, 40),
    ("sismico.png", 14, 40),
    ("sismo-moderado.png", 15, 40),
    ("modelo.png", 21, 40),
]
X0, X1 = 40, 555
ASPECT = 0.75  # alto / ancho del recorte


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(SOURCE)
    doc[0].get_pixmap(dpi=110).save(OUT / "portada.png")
    for name, page, top in SECTIONS:
        clip = pymupdf.Rect(X0, top, X1, top + (X1 - X0) * ASPECT)
        doc[page - 1].get_pixmap(dpi=150, clip=clip).save(OUT / name)
        print(name, page)


if __name__ == "__main__":
    main()
