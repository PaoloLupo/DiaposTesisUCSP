"""Preview the six animated dividers: gaanim examples/section_index.py."""

from tesis.app import create_scene
from tesis.section_index import SECTIONS, SectionIndex

scene = create_scene()
index = SectionIndex(scene)
for key, _ in SECTIONS:
    index.show(key)

scene.render()
