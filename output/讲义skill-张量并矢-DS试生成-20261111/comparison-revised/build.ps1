# -*- coding: utf-8 -*-
"""Build the revised comparison booklet end to end.

Run in comparison-revised/:  powershell -File build.ps1
Steps: render crops -> xelatex x2 -> render pages -> numeric/reference checks
       -> quote checks -> PDF checks -> verification.txt + delivery-manifest.json.
All native-command output is saved under checks/.
"""
$ErrorActionPreference = "Stop"
Push-Location $PSScriptRoot
New-Item -ItemType Directory -Force -Path "$PSScriptRoot\checks" | Out-Null
try {
    Write-Host "== 1/7 crops =="
    python -B render_crops.py 2>&1 | Tee-Object -FilePath "checks\render_crops.log"
    if ($LASTEXITCODE -ne 0) { throw "render_crops.py failed" }

    Write-Host "== 2/7 xelatex pass 1 =="
    cmd /c "xelatex -halt-on-error -interaction=nonstopmode comparison.tex > checks\xelatex-pass1.log 2>&1"
    if ($LASTEXITCODE -ne 0) { throw "xelatex pass 1 failed" }

    Write-Host "== 3/7 xelatex pass 2 =="
    cmd /c "xelatex -halt-on-error -interaction=nonstopmode comparison.tex > checks\xelatex-pass2.log 2>&1"
    if ($LASTEXITCODE -ne 0) { throw "xelatex pass 2 failed" }

    Write-Host "== 4/7 page renders =="
    python -B render_pages.py 2>&1 | Tee-Object -FilePath "checks\render_pages.log"
    if ($LASTEXITCODE -ne 0) { throw "render_pages.py failed" }

    Write-Host "== 5/7 numeric checks =="
    python -B verify_old_new_math.py 2>&1 | Tee-Object -FilePath "checks\verify_old_new_math.log"
    if ($LASTEXITCODE -ne 0) { throw "numeric checks failed" }

    Write-Host "== 5/7 quote checks =="
    python -B check_claims.py 2>&1 | Tee-Object -FilePath "checks\check_claims.log"
    if ($LASTEXITCODE -ne 0) { throw "source quote checks failed" }

    Write-Host "== 6/7 PDF checks =="
    python -B check_compare.py --strict 2>&1 | Tee-Object -FilePath "checks\check_compare.log"
    if ($LASTEXITCODE -ne 0) { throw "comparison checks failed" }

    Write-Host "== 7/7 verification.txt and manifest =="
    python -B verification_report.py 2>&1 | Tee-Object -FilePath "checks\verification_report.log"
    if ($LASTEXITCODE -ne 0) { throw "verification report failed" }
}
finally {
    Pop-Location
}
