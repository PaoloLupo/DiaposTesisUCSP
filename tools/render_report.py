"""Renderiza el reporte de Alba del anexo de la tesis para las diapositivas del reporte.

Genera ``assets/reporte/miniaturas/pNN.png`` (las 21 páginas a baja resolución, para
la tira del documento) y ``assets/reporte/paginas/pNN.png`` (las páginas que se leen
en la diapositiva, a 200 dpi). Se corre a mano si cambia el anexo:

    uv run --no-project --with pymupdf python tools/render_report.py
"""

from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "TesisUCSP/archivos/anexos/EjemploBartolome.pdf"
OUT = ROOT / "assets/reporte"

THUMB_DPI = 18  # ~150 px de ancho: la tira las muestra a unos 70 px
PAGE_DPI = 200
# Portada y la página que se lee de cada parte (1-based; ver REPORT_PARTS en alba.py).
READ = [1, 3, 6, 8, 14, 15, 21]


def main() -> None:
    doc = pymupdf.open(SOURCE)
    thumbs, pages = OUT / "miniaturas", OUT / "paginas"
    thumbs.mkdir(parents=True, exist_ok=True)
    pages.mkdir(parents=True, exist_ok=True)
    for i, page in enumerate(doc, start=1):
        page.get_pixmap(dpi=THUMB_DPI).save(thumbs / f"p{i:02}.png")
    for i in READ:
        doc[i - 1].get_pixmap(dpi=PAGE_DPI).save(pages / f"p{i:02}.png")
    print(len(doc), "páginas;", len(READ), "a", PAGE_DPI, "dpi")


if __name__ == "__main__":
    main()
