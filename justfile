[windows]
set shell := ["powershell.exe", "-NoLogo", "-Command"]

play:
    gaanim .

export:
    gaanim export . -o exports/DiaposTesisUCSP.gaanim

# Reinstala el wheel local de Gaanim aunque conserve el mismo número de versión.
reinstall:
    uv lock --upgrade-package gaanim
    uv sync --reinstall-package gaanim

# Una imagen por pausa en snapshots/DiaposTesisUCSP/current (p. ej. just capture --stops 12,30).
capture *args:
    gaanim --diff --example . --capture-stops --capture-only --tests-root snapshots {{args}}
