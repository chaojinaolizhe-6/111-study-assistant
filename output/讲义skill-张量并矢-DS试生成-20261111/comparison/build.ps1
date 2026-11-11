# -*- coding: utf-8 -*-
"""Build the full comparison deliverable from a clean checkout of comparison/.

Run in comparison/:  powershell -File build.ps1
Steps: render crops -> xelatex x2 -> render pages -> numeric checks ->
       PDF checks -> verification.txt.
"""
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
try {
    Write-Host "== 1/6 crops =="
    python -B render_crops.py
    if ($LASTEXITCODE -ne 0) { throw "render_crops.py failed" }

    Write-Host "== 2/6 xelatex pass 1 =="
    xelatex -halt-on-error -interaction=nonstopmode comparison.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "xelatex pass 1 failed" }

    Write-Host "== 3/6 xelatex pass 2 =="
    xelatex -halt-on-error -interaction=nonstopmode comparison.tex | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "xelatex pass 2 failed" }

    Write-Host "== 4/6 page renders =="
    python -B render_pages.py
    if ($LASTEXITCODE -ne 0) { throw "render_pages.py failed" }

    Write-Host "== 5/6 checks =="
    python -B verify_old_new_math.py
    if ($LASTEXITCODE -ne 0) { throw "numeric checks failed" }
    python -B check_compare.py --strict
    if ($LASTEXITCODE -ne 0) { throw "comparison checks failed" }

    Write-Host "== 6/6 verification.txt =="
    python -B verification_report.py
    if ($LASTEXITCODE -ne 0) { throw "verification report failed" }
}
finally {
    Pop-Location
}
