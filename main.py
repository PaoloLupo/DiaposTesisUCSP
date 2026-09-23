import os

from tesis.app import create_scene
from tesis.review import finish
from tesis.section_index import SectionIndex
from tesis.sections import (
    alba,
    conclusiones,
    fundamentos,
    manual,
    marco,
    objetivos,
    portada,
    problematica,
    resultados,
)

scene = create_scene()

# El orden de la exposición se edita aquí. Para ensayar o revisar solo algunos
# bloques: TESIS_BLOCKS="resultados,conclusiones" gaanim .
BLOCKS = (
    problematica.SECTION,
    objetivos.SECTION,
    fundamentos.SECTION,
    manual.SECTION,
    marco.SECTION,
    alba.SECTION,
    resultados.SECTION,
    conclusiones.SECTION,
)
selected = {key for key in os.environ.get("TESIS_BLOCKS", "").split(",") if key}

portada.build(scene)
index = SectionIndex(scene)
for section in BLOCKS:
    if not selected or section.key in selected:
        index.build(section)
finish(scene)
