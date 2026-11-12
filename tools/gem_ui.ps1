param(
  [Parameter(Mandatory=$true)][ValidateSet('rect','focus','shot','click','dclick','move','key','type','wheel','place')][string]$Action,
  [int]$X = 0,
  [int]$Y = 0,
  [int]$W = 1900,
  [int]$Hh = 1300,
  [string]$Out = '',
  [string]$Key = '',
  [string]$Text = '',
  [int]$Wheel = 0,
  [string]$TitleMatch = 'Google Gemini',
  [int]$SettleMs = 350
)

Add-Type -AssemblyName System.Drawing
Add-Type -AssemblyName System.Windows.Forms

Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class UI {
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint dx, uint dy, uint d, IntPtr e);
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint f, IntPtr e);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
  public struct RECT { public int L, T, R, B; }
}
"@

[void][UI]::SetProcessDPIAware()

function Get-TargetWindow {
  param([string]$pattern)
  $script:found = [IntPtr]::Zero
  $cb = [UI+EnumProc]{
    param($h, $l)
    if ([UI]::IsWindowVisible($h)) {
      $sb = New-Object System.Text.StringBuilder 1024
      [void][UI]::GetWindowText($h, $sb, 1024)
      if ($sb.ToString() -match $pattern) { $script:found = $h }
    }
    return $true
  }
  [void][UI]::EnumWindows($cb, [IntPtr]::Zero)
  return $script:found
}

function Set-Focus([IntPtr]$h) {
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
}

$hwnd = Get-TargetWindow $TitleMatch
if ($hwnd -eq [IntPtr]::Zero) { Write-Output 'ERROR: WINDOW_NOT_FOUND'; exit 3 }
$r = New-Object UI+RECT
[void][UI]::GetWindowRect($hwnd, [ref]$r)
$w = $r.R - $r.L; $hgt = $r.B - $r.T

switch ($Action) {
  'rect' {
    Write-Output ("H={0} L={1} T={2} W={3} H={4}" -f $hwnd, $r.L, $r.T, $w, $hgt)
  }
  'place' {
    [void][UI]::SetProcessDPIAware()
    Add-Type @"
using System;
using System.Runtime.InteropServices;
public class UIPlace {
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr a, int x, int y, int cx, int cy, uint f);
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
}
"@
    [void][UIPlace]::ShowWindow($hwnd, 9)
    [void][UIPlace]::SetWindowPos($hwnd, [IntPtr]::Zero, $X, $Y, $W, $Hh, 0x0040)
    Start-Sleep -Milliseconds 500
    [void][UI]::GetWindowRect($hwnd, [ref]$r)
    Write-Output ("PLACED={0},{1} {2}x{3}" -f $r.L, $r.T, ($r.R - $r.L), ($r.B - $r.T))
  }
  'focus' {
    $ok = Set-Focus $hwnd
    Write-Output ("FOCUS={0} fg={1}" -f $ok, [UI]::GetForegroundWindow())
  }
  'shot' {
    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (screenshot would be wrong window); retry'; exit 5 }
    Start-Sleep -Milliseconds $SettleMs
    [void][UI]::GetWindowRect($hwnd, [ref]$r)
    $bmp = New-Object System.Drawing.Bitmap ($r.R - $r.L), ($r.B - $r.T)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($r.L, $r.T, 0, 0, $bmp.Size)
    $g.Dispose()
    $bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Output ("SHOT={0} {1}x{2} at {3},{4}" -f $Out, ($r.R - $r.L), ($r.B - $r.T), $r.L, $r.T)
  }
  'move' {
    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (no click sent)'; exit 5 }
    [void][UI]::SetCursorPos($r.L + $X, $r.T + $Y)
    Write-Output ("MOVE={0},{1}" -f ($r.L + $X), ($r.T + $Y))
  }
  'click' {
    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (no click sent)'; exit 5 }
    $px = $r.L + $X; $py = $r.T + $Y
    [void][UI]::SetCursorPos($px, $py)
    Start-Sleep -Milliseconds 60
    [UI]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 40
    [UI]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds $SettleMs
    Write-Output ("CLICK={0},{1} title=[{2}]" -f $px, $py, ((Get-TargetWindow $TitleMatch)))
  }
  'dclick' {
    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (no click sent)'; exit 5 }
    $px = $r.L + $X; $py = $r.T + $Y
    [void][UI]::SetCursorPos($px, $py)
    Start-Sleep -Milliseconds 60
    [UI]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)
    [UI]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 80
    [UI]::mouse_event(0x0002, 0, 0, 0, [IntPtr]::Zero)
    [UI]::mouse_event(0x0004, 0, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds $SettleMs
    Write-Output ("DCLICK={0},{1}" -f $px, $py)
  }
  'wheel' {
    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (no click sent)'; exit 5 }
    [void][UI]::SetCursorPos($r.L + $X, $r.T + $Y)
    Start-Sleep -Milliseconds 60
    $delta = $Wheel
    [UI]::mouse_event(0x0800, 0, 0, [uint32]$delta, [IntPtr]::Zero)
    Start-Sleep -Milliseconds $SettleMs
    Write-Output ("WHEEL={0} at {1},{2}" -f $delta, ($r.L + $X), ($r.T + $Y))
  }
  'key' {
    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (no click sent)'; exit 5 }
    $vk = [int][char]$Key
    [UI]::keybd_event([byte]$vk, 0, 0, [IntPtr]::Zero)
    Start-Sleep -Milliseconds 40
    [UI]::keybd_event([byte]$vk, 0, 2, [IntPtr]::Zero)
    Start-Sleep -Milliseconds $SettleMs
    Write-Output ("KEY={0}" -f $Key)
  }
  'type' {
    if (-not (Set-Focus $hwnd)) { Write-Output 'ERROR: FOCUS_FAILED (no click sent)'; exit 5 }
    $keys = New-Object System.Collections.Generic.List[object]
    foreach ($ch in $Text.ToCharArray()) {
      $upper = [char]::IsUpper($ch)
      $vk = 0
      $needShift = $upper
      if ($upper) { $ch = [char]::ToLower($ch) }
      if ($ch -match '[a-z]') { $vk = [int][char]([string]$ch).ToUpper() - 0 }
      elseif ($ch -match '[0-9]') { $vk = [int][char]$ch }
      elseif ($ch -eq ' ') { $vk = 0x20 }
      elseif ($ch -eq ':') { $vk = 0xBA; $needShift = $true }
      elseif ($ch -eq '/') { $vk = 0xBF }
      elseif ($ch -eq '-') { $vk = 0xBD }
      elseif ($ch -eq '.') { $vk = 0xBE }
      if ($vk -eq 0) { continue }
      [UI]::keybd_event([byte]0x10, 0, $(if ($needShift) {0} else {2}), [IntPtr]::Zero)
      [UI]::keybd_event([byte]$vk, 0, 0, [IntPtr]::Zero)
      [UI]::keybd_event([byte]$vk, 0, 2, [IntPtr]::Zero)
      [UI]::keybd_event([byte]0x10, 0, 2, [IntPtr]::Zero)
      Start-Sleep -Milliseconds 12
    }
    Write-Output ("TYPED={0}" -f $Text.Length)
  }
}
