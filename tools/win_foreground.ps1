param([string]$TitleMatch = 'Google Gemini')
Add-Type -AssemblyName System.Windows.Forms
Add-Type @"
using System;
using System.Runtime.InteropServices;
using System.Text;
public class UIFg {
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] public static extern void keybd_event(byte vk, byte scan, uint f, IntPtr e);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint a, uint b, bool f);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
  [DllImport("user32.dll")] public static extern bool SwitchToThisWindow(IntPtr h, bool alt);
  [DllImport("user32.dll")] public static extern IntPtr GetWindow(IntPtr h, uint cmd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr h);
}
"@
[void][UIFg]::SetProcessDPIAware()

$script:found = [IntPtr]::Zero
$cb = [UIFg+EnumProc]{
  param($h, $l)
  if ([UIFg]::IsWindowVisible($h)) {
    $sb = New-Object System.Text.StringBuilder 1024
    [void][UIFg]::GetWindowText($h, $sb, 1024)
    if ($sb.ToString() -match $TitleMatch) { $script:found = $h }
  }
  return $true
}
[void][UIFg]::EnumWindows($cb, [IntPtr]::Zero)
$h = $script:found
if ($h -eq [IntPtr]::Zero) { 'NOT_FOUND'; exit 3 }

for ($i = 0; $i -lt 5; $i++) {
  [void][UIFg]::keybd_event(0x12, 0, 0, [IntPtr]::Zero)
  [void][UIFg]::keybd_event(0x12, 0, 2, [IntPtr]::Zero)
  Start-Sleep -Milliseconds 60
  [void][UIFg]::ShowWindow($h, 5)
  [void][UIFg]::BringWindowToTop($h)
  [void][UIFg]::SetForegroundWindow($h)
  Start-Sleep -Milliseconds 200
  if ([UIFg]::GetForegroundWindow() -eq $h) { "FOREGROUND ok after $i"; exit 0 }
}
[void][UIFg]::SwitchToThisWindow($h, $true)
Start-Sleep -Milliseconds 400
if ([UIFg]::GetForegroundWindow() -eq $h) { 'FOREGROUND ok (SwitchToThisWindow)'; exit 0 }
'FOREGROUND failed'; exit 4
