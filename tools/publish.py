"""Publica el deck en la rama ``publicar`` para abrirlo en el reproductor web.

Exporta el paquete completo a ``exports/`` (no se versiona), lo aligera con
``gaanim pack --web`` y lo deja como único commit de la rama ``publicar``. Cada
publicación reemplaza ese commit, así que el historial no crece. El reproductor lo
abre desde raw.githubusercontent.com, que envía CORS (GitHub Releases no):

``uv run python tools/publish.py [--no-push] [--dirty]``
"""

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "publicar"
NAME = "DiaposTesisUCSP.gaanim"
FULL = ROOT / "exports" / NAME
RAW = f"https://raw.githubusercontent.com/PaoloLupo/DiaposTesisUCSP/{BRANCH}/{NAME}"
PLAYER = f"https://paololupo.github.io/gaanim/reproductor/?src={RAW}"
LIMIT = 100 * 1024 * 1024  # GitHub rechaza archivos de más de 100 MB


def git(*args: str, data: bytes | None = None) -> str:
    done = subprocess.run(
        ["git", *args], cwd=ROOT, input=data, capture_output=True, check=True
    )
    return done.stdout.decode().strip()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publica el deck para el reproductor web."
    )
    parser.add_argument(
        "--no-push", action="store_true", help="arma el commit sin subirlo"
    )
    parser.add_argument(
        "--dirty", action="store_true", help="publica aunque haya cambios sin commit"
    )
    args = parser.parse_args()
    dirty = bool(git("status", "--porcelain", "--untracked-files=no"))
    if dirty and not args.dirty:
        sys.exit(
            "Hay cambios sin commit; la publicación debe salir de un commit (o --dirty)."
        )

    subprocess.run(["gaanim", "export", ".", "-o", str(FULL)], cwd=ROOT, check=True)
    with tempfile.TemporaryDirectory() as tmp:
        web = Path(tmp) / NAME
        subprocess.run(["gaanim", "pack", str(FULL), str(web), "--web"], check=True)
        size = web.stat().st_size
        if size >= LIMIT:
            sys.exit(
                f"El paquete web pesa {size / 2**20:.1f} MB; GitHub admite hasta 100 MB."
            )
        blob = git("hash-object", "-w", str(web))

    # Un árbol con el paquete solo y un commit sin padres: reemplaza la rama entera.
    tree = git("mktree", "-z", data=f"100644 blob {blob}\t{NAME}\0".encode())
    source = git("rev-parse", "--short", "HEAD")
    branch = git("branch", "--show-current")
    message = f"{NAME} desde {source} ({branch})"
    if dirty:
        message += ", con cambios sin commit"
    commit = git("commit-tree", tree, "-m", message)
    git("update-ref", f"refs/heads/{BRANCH}", commit)
    print(f"{BRANCH} → {commit[:7]}: {message}, {size / 2**20:.1f} MB")
    if args.no_push:
        return
    subprocess.run(
        ["git", "push", "--force", "origin", f"{commit}:refs/heads/{BRANCH}"],
        cwd=ROOT,
        check=True,
    )
    print(f"Reproductor: {PLAYER}")


if __name__ == "__main__":
    main()
