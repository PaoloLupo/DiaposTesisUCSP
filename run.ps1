param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RuntimeArgs
)

$ErrorActionPreference = "Stop"
$gaanimRoot = $env:GAANIM_ROOT
if (-not $gaanimRoot) {
    $gaanimRoot = [Environment]::GetEnvironmentVariable("GAANIM_ROOT", "User")
}
if (-not $gaanimRoot) {
    throw "Configura GAANIM_ROOT con el checkout de Gaanim actualizado."
}
$launcher = Join-Path $gaanimRoot "target/debug/gaanim.exe"
$runtime = Join-Path $gaanimRoot "target/debug/gaanim-core.exe"
if (-not (Test-Path -LiteralPath $launcher) -or -not (Test-Path -LiteralPath $runtime)) {
    throw "Falta el runtime de desarrollo. Ejecuta 'just build' en $gaanimRoot."
}
if (-not $RuntimeArgs) {
    $RuntimeArgs = @(".")
}

$previousPath = $env:PATH
Push-Location $gaanimRoot
try {
    $rustLibraries = rustc --print target-libdir
    if ($LASTEXITCODE -ne 0) { throw "No se pudo localizar el runtime de Rust." }
} finally {
    Pop-Location
}
Push-Location $PSScriptRoot
try {
    $env:PATH = "$gaanimRoot/target/debug/deps;$gaanimRoot/target/debug;$rustLibraries;$previousPath"
    & $launcher @RuntimeArgs
    $runtimeExitCode = $LASTEXITCODE
} finally {
    $env:PATH = $previousPath
    Pop-Location
}
exit $runtimeExitCode
