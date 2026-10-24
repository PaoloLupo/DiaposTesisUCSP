[windows]
set shell := ["powershell.exe", "-NoLogo", "-Command"]

play:
    gaanim .

# Revisión antes de un commit: estilo, tipos, datos de la tesis y el guion, sin avisos.
check:
    uv run ruff check .
    uv run ruff format --check .
    uv run pyright
    uv run python -m unittest discover -s tests
    gaanim check . --strict

# Formatea y aplica los arreglos seguros de ruff.
fmt:
    uv run ruff format .
    uv run ruff check --fix .

# Paquete completo en exports/ (no se versiona): sirve para exportar video y para check.
export:
    gaanim export . -o exports/DiaposTesisUCSP.gaanim

# Exporta, aligera con gaanim pack --web y sube a la rama publicar (un solo commit).
publish *args:
    uv run python tools/publish.py {{args}}

# Una imagen por pausa en snapshots/DiaposTesisUCSP/current (p. ej. just capture --stops 12,30).
capture *args:
    gaanim --diff --example . --capture-stops --capture-only --tests-root snapshots {{args}}

# Aprueba las pausas actuales como referencia; se hace antes de empezar un cambio.
baseline *args:
    gaanim --diff --example . --capture-stops --bless --tests-root snapshots {{args}}

# Captura las pausas y las compara con la referencia; informe en snapshots/report/index.html.
# Tras actualizar Gaanim, los bordes cambian por antialiasing: just diff --pixel-threshold 24
diff *args:
    gaanim --diff --example . --capture-stops --tests-root snapshots --output snapshots/report {{args}}

# Exporta en orden un tramo (segundos o nombres de pausa) en snapshots/sequence. Las
# pausas se capturan con saltos; las transiciones se revisan como se reproducen:
# just sequence reporte-parte-1 reporte-parte-2
sequence from to:
    if (Test-Path snapshots/sequence) { Remove-Item -Recurse -Force snapshots/sequence }
    gaanim export . -o snapshots/sequence/f_%04d.png --quality draft --from {{from}} --to {{to}}

# Actualiza el wheel de autocompletado (PyPI). El motor es gaanim.exe: gaanim update.
upgrade:
    uv lock --upgrade-package gaanim
    uv sync
