from tesis.app import create_scene
from tesis.sections import context, title

scene = create_scene()

title.build(scene)
context.build(scene)

scene.render()
