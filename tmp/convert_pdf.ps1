param([Parameter(Mandatory=$true)][string]$src, [Parameter(Mandatory=$true)][string]$pdf)
$ErrorActionPreference = 'Stop'
$code = 1
try {
  $pp = New-Object -ComObject PowerPoint.Application
  $pp.Visible = -1
  $pres = $pp.Presentations.Open($src, -1, 0, 0)
  $pres.SaveAs($pdf, 32)
  $pres.Close()
  $pp.Quit()
  $code = 0
} catch {
  Write-Output ("ERROR: " + $_.Exception.Message)
  $code = 2
}
Start-Sleep -Milliseconds 500
[Environment]::Exit($code)
