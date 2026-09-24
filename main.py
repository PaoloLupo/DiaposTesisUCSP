from tesis.app import create_scene
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

# El orden de la exposición se edita aquí. Para ensayar solo algunos bloques:
# gaanim . --sections resultados,conclusiones  (o --from resultados).
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
portada.build(scene)
index = SectionIndex(scene)
for section in BLOCKS:
    index.build(section)
scene.render()
