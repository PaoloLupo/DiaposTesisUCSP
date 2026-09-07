from gaanim import Transition

from tesis.app import create_scene
from tesis.section_index import SectionIndex
from tesis.sections import context, title

scene = create_scene()

title.build(scene)
section_index = SectionIndex(scene)
section_index.build(
    "problematica", context.SEGMENTS
)
section_index.show("objetivos")
section_index.show("fundamentos")
scene.render()
