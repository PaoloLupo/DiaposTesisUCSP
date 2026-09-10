from tesis.app import create_scene
from tesis.section_index import SectionIndex
from tesis.sections import context, title

scene = create_scene()

title.build(scene)
section_index = SectionIndex(scene)
section_index.build(context.SECTION)
section_index.build(fundamentos.SECTION)
scene.render()
