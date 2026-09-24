from pathlib import Path

from gaanim import Scene, PostProcess

from tesis.theme import PAPER, build_theme

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_MANIFEST = PROJECT_ROOT / "gaanim.toml"
THESIS = PROJECT_ROOT / "TesisUCSP"


def thesis_image(relative: str) -> str:
    """Ruta a una figura de la tesis; no se duplican imágenes en assets/."""
    return str(THESIS / "imagenes" / relative)


def create_scene() -> Scene:
    scene = Scene(frame=(16, 9), theme=build_theme(), background=PAPER, margin=0.5)
    scene.assets.load_project(str(PROJECT_MANIFEST))
    return scene
