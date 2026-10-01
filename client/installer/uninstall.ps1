# RagnaDuds uninstaller for Windows (PowerShell 5.1+). Removes one edition completely: the game folder
# (with settings and screenshots), the desktop + Start menu shortcuts and the "Apps" entry in Windows Settings.
# Started from: Start menu > RagnaDuds > Uninstall ..., Settings > Apps, or "Uninstall RagnaDuds.bat" in the download.
# The installer copies this file into the game folder, next to ragnaduds-install.json (config + where it was installed).
# Keep this file ASCII-only (PowerShell 5.1 reads it as ANSI).

Add-Type -AssemblyName System.Windows.Forms, System.Drawing
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$caption = 'RagnaDuds - Uninstall'
function Say($text, $buttons = 'OK', $icon = 'Information') { [Windows.Forms.MessageBox]::Show($text, $caption, $buttons, $icon) }

try {
  # config: the installed copy (ragnaduds-install.json) or the download's installer\config.json
  $cfgPath = @((Join-Path $here 'ragnaduds-install.json'), (Join-Path $here 'config.json')) |
    Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
  if (-not $cfgPath) { [void](Say 'Config not found next to the uninstaller.' 'OK' 'Error'); exit 1 }
  $cfg = Get-Content -LiteralPath $cfgPath -Raw -Encoding UTF8 | ConvertFrom-Json
  $regKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\RagnaDuds-$($cfg.folder)"

  # where the game is: the recorded folder, this script's folder, the registered one, the default one
  $candidates = @($cfg.dest, $here)
  try { $candidates += (Get-ItemProperty -LiteralPath $regKey -ErrorAction Stop).InstallLocation } catch { }
  $candidates += Join-Path $env:LOCALAPPDATA "RagnaDuds\$($cfg.folder)"
  $dest = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath (Join-Path $_ $cfg.exe)) } | Select-Object -First 1
  if ($dest) { $dest = [IO.Path]::GetFullPath($dest).TrimEnd('\') }

  $what = if ($dest) { "the game folder with your settings and screenshots:`n   $dest`n - " } else { '' }
  if ((Say "Remove $($cfg.title) from this PC?`n`nThis deletes:`n - $($what)the desktop and Start menu shortcuts" 'YesNo' 'Question') -ne 'Yes') { exit 0 }

  if ($dest) {
    # never delete a folder that isn't a game folder (drive root, user folders...)
    $forbidden = @([IO.Path]::GetPathRoot($dest).TrimEnd('\'), $env:USERPROFILE, $env:LOCALAPPDATA, $env:APPDATA,
                   [Environment]::GetFolderPath('Desktop'), [Environment]::GetFolderPath('MyDocuments'), $env:ProgramFiles, ${env:ProgramFiles(x86)})
    if ($forbidden | Where-Object { $_ -and ($_.TrimEnd('\') -eq $dest) }) { throw "Refusing to delete $dest (not a game folder)." }
    # the game must be closed, or Windows keeps its files locked
    while (Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path.StartsWith($dest + '\', [StringComparison]::OrdinalIgnoreCase) }) {
      if ((Say "$($cfg.title) is still open. Close the game, then press Retry." 'RetryCancel' 'Warning') -ne 'Retry') { exit 0 }
    }
  }

  # shortcuts + Windows "Apps" entry
  $programs = Join-Path ([Environment]::GetFolderPath('Programs')) 'RagnaDuds'
  foreach ($lnk in @((Join-Path ([Environment]::GetFolderPath('Desktop')) "$($cfg.shortcut).lnk"),
                     (Join-Path $programs "$($cfg.shortcut).lnk"), (Join-Path $programs "Uninstall $($cfg.shortcut).lnk"))) {
    if (Test-Path -LiteralPath $lnk) { Remove-Item -LiteralPath $lnk -Force }
  }
  if ((Test-Path -LiteralPath $programs) -and -not (Get-ChildItem -LiteralPath $programs -Force)) { Remove-Item -LiteralPath $programs -Force }
  if (Test-Path -LiteralPath $regKey) { Remove-Item -LiteralPath $regKey -Recurse -Force }

  # the game folder (a few seconds for 5 GB): small "please wait" window meanwhile
  if ($dest) {
    $wait = New-Object Windows.Forms.Form
    $wait.Text = $caption; $wait.Size = New-Object Drawing.Size(360, 110); $wait.StartPosition = 'CenterScreen'
    $wait.FormBorderStyle = 'FixedDialog'; $wait.ControlBox = $false
    $l = New-Object Windows.Forms.Label; $l.Text = "Removing $($cfg.title)... please wait."; $l.Dock = 'Fill'; $l.TextAlign = 'MiddleCenter'
    $wait.Controls.Add($l); $wait.Show(); [Windows.Forms.Application]::DoEvents()
    Set-Location $env:TEMP                                   # not inside the folder we delete
    try { Remove-Item -LiteralPath $dest -Recurse -Force -ErrorAction Stop } finally { $wait.Close() }
    $parent = Split-Path -Parent $dest                       # ...\RagnaDuds, if no other edition is left
    if ((Split-Path -Leaf $parent) -eq 'RagnaDuds' -and -not (Get-ChildItem -LiteralPath $parent -Force)) { Remove-Item -LiteralPath $parent -Force }
  }
  [void](Say "$($cfg.title) was removed. Bye! The Porings will miss you (they won't).")
} catch {
  # Ctrl+C on this window copies the whole text: paste it to Duds
  [void](Say ("Uninstall stopped. Press Ctrl+C to copy this and send it to Duds.`n`n" +
              "Message: $($_.Exception.Message)`nScript line: $($_.InvocationInfo.ScriptLineNumber)`n" +
              "Windows: $([Environment]::OSVersion.VersionString), PowerShell $($PSVersionTable.PSVersion)`nFolder: $dest") 'OK' 'Error')
  exit 1
}
