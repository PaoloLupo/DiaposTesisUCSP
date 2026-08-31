[windows]
set shell := ["powershell.exe", "-NoLogo", "-Command"]

play:
    gaanim .

[linux]
reinstall:
    uv remove gaanim
    uv add "../../rust/gaanim/target/wheels/gaanim-0.2.0-py3-none-any.whl"
