# RagnaDuds launcher upgrade for Windows (PowerShell 5.1+). Started by "Upgrade RagnaDuds.bat" from the small
# "launcher upgrade" download. Gives an EXISTING install the auto-updating launcher without downloading the game
# again: copies launch.ps1 + its files and the config (update address + login token), and points the desktop and
# Start menu shortcuts at the launcher. The launcher's first start checks the files and downloads only what changed.
# Keep this file ASCII-only (PowerShell 5.1 reads it as ANSI).

Add-Type -AssemblyName System.Windows.Forms
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$cfg  = Get-Content (Join-Path $here 'config.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$title = "$($cfg.title) - launcher upgrade"

function Say($text, $icon) { [void][Windows.Forms.MessageBox]::Show($text, $title, 'OK', $icon) }
function Test-Game($d) { $d -and (Test-Path -LiteralPath (Join-Path $d $cfg.exe)) }

# where is the game? the installer's Windows "Apps" entry, the default folder, or ask
$dest = $null
$reg = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\RagnaDuds-$($cfg.folder)"
if (Test-Path $reg) { $dest = (Get-ItemProperty $reg -ErrorAction SilentlyContinue).InstallLocation }
if (-not (Test-Game $dest)) { $dest = Join-Path $env:LOCALAPPDATA "RagnaDuds\$($cfg.folder)" }
if (-not (Test-Game $dest)) {
  $pick = New-Object Windows.Forms.FolderBrowserDialog
  $pick.Description = "Where is $($cfg.title) installed? Pick the game folder (the one with $($cfg.exe))."
  if ($pick.ShowDialog() -ne 'OK') { exit 1 }
  $dest = $pick.SelectedPath
}
if (-not (Test-Game $dest)) {
  Say "$($cfg.exe) is not in that folder. Install the game from the website instead." 'Error'; exit 1
}
if (Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path.StartsWith($dest, 'OrdinalIgnoreCase') }) {
  Say 'The game is open. Close it, then run the upgrade again.' 'Warning'; exit 1
}

try {
  foreach ($f in @('launch.ps1', 'uninstall.ps1', 'duds_ok_bg.png', 'PressStart2P-Regular.ttf', 'ragnaduds.ico')) {
    Copy-Item (Join-Path $here $f) (Join-Path $dest $f) -Force
  }
  $cfg | Add-Member -NotePropertyName dest -NotePropertyValue $dest -Force
  [IO.File]::WriteAllText((Join-Path $dest 'ragnaduds-install.json'), ($cfg | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding($false)))
  # no ragnaduds-patch.json: the launcher's first start compares the files on disk with the website

  $psExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
  $launchArgs = "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$(Join-Path $dest 'launch.ps1')`""
  $ws = New-Object -ComObject WScript.Shell
  $programs = Join-Path ([Environment]::GetFolderPath('Programs')) 'RagnaDuds'
  [void](New-Item -ItemType Directory -Force -Path $programs)
  foreach ($dir in @([Environment]::GetFolderPath('Desktop'), $programs)) {
    $lnk = $ws.CreateShortcut((Join-Path $dir "$($cfg.shortcut).lnk"))
    $lnk.TargetPath = $psExe; $lnk.Arguments = $launchArgs; $lnk.WorkingDirectory = $dest
    $lnk.WindowStyle = 7
    $lnk.IconLocation = (Join-Path $dest 'ragnaduds.ico') + ',0'; $lnk.Description = $cfg.title; $lnk.Save()
  }
  $unArgs = "-NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -File `"$(Join-Path $dest 'uninstall.ps1')`""
  $lnk = $ws.CreateShortcut((Join-Path $programs "Uninstall $($cfg.shortcut).lnk"))
  $lnk.TargetPath = $psExe; $lnk.Arguments = $unArgs; $lnk.WorkingDirectory = $env:TEMP
  $lnk.IconLocation = (Join-Path $dest 'ragnaduds.ico') + ',0'; $lnk.Description = "Uninstall $($cfg.title)"; $lnk.Save()
  [void](New-Item -Path $reg -Force)
  $props = @{ DisplayName = $cfg.title; DisplayIcon = (Join-Path $dest 'ragnaduds.ico'); Publisher = 'RagnaDuds'
              InstallLocation = $dest; UninstallString = "`"$psExe`" $unArgs" }
  foreach ($k in $props.Keys) { [void](New-ItemProperty -Path $reg -Name $k -Value $props[$k] -PropertyType String -Force) }
} catch {
  Say "The upgrade failed: $($_.Exception.Message)" 'Error'; exit 1
}

Say "Done! From now on, open '$($cfg.shortcut)' from your desktop: it checks for updates and downloads only what changed. The first start checks every file, so it takes a little longer." 'Information'
Start-Process -FilePath $psExe -ArgumentList $launchArgs -WorkingDirectory $dest
