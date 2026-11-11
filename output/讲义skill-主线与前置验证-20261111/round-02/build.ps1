# Reproducible two-pass build for round-02/sample.tex
# Run from anywhere:  pwsh -File build.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $root
try {
    foreach ($f in @("sample.aux", "sample.out", "sample.toc", "sample.lof", "sample.lot")) {
        if (Test-Path $f) { Remove-Item $f -Force }
    }

    & xelatex -halt-on-error -interaction=nonstopmode sample.tex *> build-pass1.console.log
    if ($LASTEXITCODE -ne 0) {
        throw "first xelatex pass failed (exit $LASTEXITCODE); see build-pass1.console.log"
    }
    Copy-Item sample.log build-pass1.log -Force

    & xelatex -halt-on-error -interaction=nonstopmode sample.tex *> build-pass2.console.log
    if ($LASTEXITCODE -ne 0) {
        throw "second xelatex pass failed (exit $LASTEXITCODE); see build-pass2.console.log"
    }
    Copy-Item sample.log build-pass2.log -Force

    & python -B ..\.dsh\skills\lecture-deepdive\scripts\check_handout.py sample.tex --mode appendix --log sample.log *> check-handout.txt
    if ($LASTEXITCODE -ne 0) {
        throw "check_handout.py reported an error or warning (exit $LASTEXITCODE); see check-handout.txt"
    }

    & python -B check_layout.py *> layout-run.txt
    if ($LASTEXITCODE -ne 0) {
        throw "check_layout.py reported an issue (exit $LASTEXITCODE); see layout-run.txt"
    }

    & python -B render_pages.py *> render-run.txt
    if ($LASTEXITCODE -ne 0) {
        throw "render_pages.py failed (exit $LASTEXITCODE); see render-run.txt"
    }

    $pages = (Select-String -Path sample.log -Pattern "Output written on sample.pdf \(([0-9]+) pages?\)").Matches.Groups[1].Value
    Write-Host "build complete: sample.pdf, $pages pages"
    Write-Host "pass logs: build-pass1.log, build-pass2.log"
    Write-Host "checker: check-handout.txt; layout: layout-report.txt"
    Write-Host "rendered pages: render/"
}
finally {
    Pop-Location
}
