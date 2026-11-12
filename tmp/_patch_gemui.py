import io
p = r"tools\gem_ui.ps1"
s = io.open(p, encoding="utf-8").read()

old_focus = '''function Set-Focus([IntPtr]$h) {
  if ($h -eq [IntPtr]::Zero) { throw 'window not found' }
  if ([UI]::IsIconic($h)) { [void][UI]::ShowWindow($h, 9) } else { [void][UI]::ShowWindow($h, 5) }
  [void][UI]::BringWindowToTop($h)
  $fg = [UI]::GetForegroundWindow()
  $pidFg = 0
  $tidFg = [UI]::GetWindowThreadProcessId($fg, [ref]$pidFg)
  $tidMe = [UI]::GetCurrentThreadId()
  [void][UI]::AttachThreadInput($tidMe, $tidFg, $true)
  $ok = [UI]::SetForegroundWindow($h)
  [void][UI]::AttachThreadInput($tidMe, $tidFg, $false)
  Start-Sleep -Milliseconds 250
  return ($ok -or ([UI]::GetForegroundWindow() -eq $h))
}'''

new_focus = '''function Set-Focus([IntPtr]$h) {
  if ($h -eq [IntPtr]::Zero) { throw 'window not found' }
  if ([UI]::IsIconic($h)) { [void][UI]::ShowWindow($h, 9) } else { [void][UI]::ShowWindow($h, 5) }
  [void][UI]::BringWindowToTop($h)
  for ($i = 0; $i -lt 4; $i++) {
    [UI]::keybd_event(0x12, 0, 0, [IntPtr]::Zero)
    [UI]::keybd_event(0x12, 0, 2, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 50
    $fg = [UI]::GetForegroundWindow()
    $pidFg = 0
    $tidFg = [UI]::GetWindowThreadProcessId($fg, [ref]$pidFg)
    $tidMe = [UI]::GetCurrentThreadId()
    [void][UI]::AttachThreadInput($tidMe, $tidFg, $true)
    [void][UI]::SetForegroundWindow($h)
    [void][UI]::AttachThreadInput($tidMe, $tidFg, $false)
    Start-Sleep -Milliseconds 120
    if ([UI]::GetForegroundWindow() -eq $h) { return $true }
  }
  return $false
}'''

assert s.count(old_focus) == 1, s.count(old_focus)
s = s.replace(old_focus, new_focus)

n = s.count("    [void](Set-Focus $hwnd)")
s = s.replace("    [void](Set-Focus $hwnd)",
              "    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (no click sent)'; exit 5 }")
print("click guards:", n)

old_shot = "    if (-not (Set-Focus $hwnd)) { Write-Output 'WARN: focus failed' }"
new_shot = "    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (screenshot would be wrong window); retry'; exit 5 }"
assert s.count(old_shot) == 1
s = s.replace(old_shot, new_shot)

io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("patched", p)
