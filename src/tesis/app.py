from pathlib import Path

from gaanim import Background, Scene

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROJECT_MANIFEST = PROJECT_ROOT / "gaanim.toml"


def create_scene() -> Scene:
    scene = Scene(
        frame=(16, 9),
        # background=Background.shader(
        #     PROJECT_ROOT / "assets" / "background.wgsl", fallback="#03060B"
        # ),
        margin=0.5,
    )
    # TODO: load_project deberia aceptar tambien Path y no str
    scene.assets.load_project(str(PROJECT_MANIFEST))
    scene.canvas.set_theme("paper")
    # scene.canvas.set_fonts(font="Century Gothic")
    return scene
