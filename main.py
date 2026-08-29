import sys
from pathlib import Path

# TODO: ARREGLAR ESTE ARTIFICIO
# Gaanim ejecuta el punto de entrada mediante ``runpy``. Por eso ``src`` no se
# añade automáticamente a la ruta de imports como ocurre con ``python main.py``.
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from tesis.app import create_scene
from tesis.sections import context, title

scene = create_scene()

title.build(scene)
context.build(scene)

scene.render()
