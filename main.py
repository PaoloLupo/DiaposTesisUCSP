from gaanim import Transition

from tesis.app import create_scene
from tesis.section_index import SectionIndex
from tesis.sections import context, title

scene = create_scene()

title.build(scene)
section_index = SectionIndex(scene)
section_index.show("problematica", transition=Transition.cross_fade(0.4))
context.build(scene)
section_index.show("objetivos", transition=Transition.cross_fade(0.4))
section_index.show("fundamentos", transition=Transition.cross_fade(0.4))
scene.render()
