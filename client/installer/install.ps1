# RagnaDuds installer for Windows (PowerShell 5.1+, built into Windows 10/11).
# Started by "Install RagnaDuds.bat". Unpacks game.zip with a progress bar and creates
# "RagnaDuds" shortcuts (desktop + Start menu) that start the patched exe with the right arguments.
# After unpacking it checks every file (manifest.json), the exe hash and the server address.
# Run again on the same folder = REINSTALL: files are replaced, files the new version doesn't have are removed,
# settings/screenshots are kept. Also sets up the uninstaller (uninstall.ps1): Start menu + Windows "Apps".
# Same retro look as the Linux installer and the website: photo on top, wooden/gold panel below.
# Keep this file ASCII-only (PowerShell 5.1 reads it as ANSI).

Add-Type -AssemblyName System.Windows.Forms, System.Drawing, System.IO.Compression, System.IO.Compression.FileSystem
[System.Windows.Forms.Application]::EnableVisualStyles()

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$root = Split-Path -Parent $here
$cfg  = Get-Content (Join-Path $here 'config.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$zip  = Join-Path $root 'game.zip'
$script:cancel = $false
$script:done = $false

# ---------- colors + fonts (same as the website) ----------
function RGB($r, $g, $b) { [Drawing.Color]::FromArgb($r, $g, $b) }
$cBg = RGB 20 18 31; $cPanel = RGB 34 29 51; $cInk = RGB 246 236 210; $cGold = RGB 255 209 102
$cWood = RGB 107 79 42; $cGoldEdge = RGB 201 162 91; $cBlue = RGB 124 196 255; $cPink = RGB 255 143 177
$cGreen = RGB 126 224 129; $cGreenDark = RGB 92 191 95; $cShadow = RGB 122 62 18

$script:fonts = New-Object Drawing.Text.PrivateFontCollection        # the website's pixel font
$pixelFamily = $null
try { $script:fonts.AddFontFile((Join-Path $here 'PressStart2P-Regular.ttf')); $pixelFamily = $script:fonts.Families[0] } catch { }
function PixelFont($size) {
  if ($pixelFamily) { New-Object Drawing.Font($pixelFamily, $size) } else { New-Object Drawing.Font('Consolas', ($size + 3), [Drawing.FontStyle]::Bold) }
}
$bodyFont = New-Object Drawing.Font('Consolas', 9.5)
$smallFont = New-Object Drawing.Font('Consolas', 8.5)

# ---------- window: photo on top, retro panel below ----------
$W = 440
$workH = [Windows.Forms.Screen]::PrimaryScreen.WorkingArea.Height
$photoImg = [Drawing.Image]::FromFile((Join-Path $here 'duds_ok_bg.png'))
$photoH = [int][Math]::Max([double]240, [Math]::Min([double]565, [double]($workH - 510)))   # shrink on short screens
$panelH = 440

$form = New-Object Windows.Forms.Form
$form.Text = "$($cfg.title) - Setup"; $form.ClientSize = New-Object Drawing.Size($W, ($photoH + $panelH + 10))
$form.FormBorderStyle = 'FixedDialog'; $form.MaximizeBox = $false; $form.StartPosition = 'CenterScreen'
$form.BackColor = $cBg; $form.ForeColor = $cInk
$form.Icon = New-Object Drawing.Icon (Join-Path $here 'ragnaduds.ico')

$pic = New-Object Windows.Forms.PictureBox
$pic.Image = $photoImg; $pic.SizeMode = 'Zoom'; $pic.BackColor = $cBg
$pic.Location = New-Object Drawing.Point(10, 8); $pic.Size = New-Object Drawing.Size(($W - 20), $photoH)
$form.Controls.Add($pic)

# the panel draws the website's frame: wood outside, black line, gold line inside
$panel = New-Object Windows.Forms.Panel
$panel.Location = New-Object Drawing.Point(10, ($photoH + 14)); $panel.Size = New-Object Drawing.Size(($W - 20), ($panelH - 14))
$panel.BackColor = $cPanel
$panel.Add_Paint({
  param($s, $e)
  $g = $e.Graphics; $w = $s.Width; $h = $s.Height
  $g.DrawRectangle((New-Object Drawing.Pen($cWood, 8)), 4, 4, ($w - 8), ($h - 8))
  $g.DrawRectangle((New-Object Drawing.Pen([Drawing.Color]::Black, 2)), 9, 9, ($w - 18), ($h - 18))
  $g.DrawRectangle((New-Object Drawing.Pen($cGoldEdge, 2)), 12, 12, ($w - 24), ($h - 24))
})
$form.Controls.Add($panel)

function Add-Label($text, $x, $y, $w, $h, $font, $color) {
  $l = New-Object Windows.Forms.Label; $l.Text = $text; $l.AutoSize = $false; $l.BackColor = $cPanel
  $l.Location = New-Object Drawing.Point($x, $y); $l.Size = New-Object Drawing.Size($w, $h)
  $l.Font = $font; $l.ForeColor = $color
  $panel.Controls.Add($l); return $l
}
$IW = $W - 20 - 44                                   # inner width of the panel
# title with the website's stacked shadow (black, then brown, then gold)
$titleBox = New-Object Windows.Forms.Panel; $titleBox.Location = New-Object Drawing.Point(22, 20); $titleBox.Size = New-Object Drawing.Size($IW, 28)
$titleBox.BackColor = $cPanel
$titleFont = PixelFont 15
$titleBox.Add_Paint({
  param($s, $e)
  $g = $e.Graphics; $g.TextRenderingHint = 'SingleBitPerPixelGridFit'
  $g.DrawString('RAGNADUDS', $titleFont, (New-Object Drawing.SolidBrush([Drawing.Color]::Black)), 4, 4)
  $g.DrawString('RAGNADUDS', $titleFont, (New-Object Drawing.SolidBrush($cShadow)), 2, 2)
  $g.DrawString('RAGNADUDS', $titleFont, (New-Object Drawing.SolidBrush($cGold)), 0, 0)
})
$panel.Controls.Add($titleBox)
[void](Add-Label $cfg.edition 22 52 $IW 18 $bodyFont $cInk)
[void](Add-Label '[RagnaDuds, Kafra intern]' 22 74 $IW 16 (PixelFont 7) $cBlue)
$quips = @(
  '"Installing. Don''t touch anything, you degenerate."',
  '"Checking every file. Yes, every single one. Relax."',
  '"The Poring is watching you install. Stay calm."',
  '"Almost there. Hydrate. Or don''t."',
  '"Unpacking gigabytes of nostalgia. Patience, parca."')
$quip = Add-Label '"Thumbs up? Press Install."' 22 92 $IW 34 (New-Object Drawing.Font('Consolas', 9, [Drawing.FontStyle]::Italic)) $cPink
$status = Add-Label 'Ready to install.' 22 128 $IW 34 $bodyFont $cInk

$pathBox = New-Object Windows.Forms.TextBox
$pathBox.Text = Join-Path $env:LOCALAPPDATA "RagnaDuds\$($cfg.folder)"
$pathBox.Location = New-Object Drawing.Point(22, 166); $pathBox.Size = New-Object Drawing.Size(($IW - 44), 22)
$pathBox.BackColor = [Drawing.Color]::Black; $pathBox.ForeColor = $cInk; $pathBox.BorderStyle = 'FixedSingle'; $pathBox.Font = $smallFont
$panel.Controls.Add($pathBox)
$browse = New-Object Windows.Forms.Button; $browse.Text = '...'
$browse.Location = New-Object Drawing.Point(($IW - 16), 165); $browse.Size = New-Object Drawing.Size(38, 23)
$browse.FlatStyle = 'Flat'; $browse.FlatAppearance.BorderColor = [Drawing.Color]::Black; $browse.BackColor = $cGold; $browse.ForeColor = [Drawing.Color]::Black
$browse.Add_Click({ $d = New-Object Windows.Forms.FolderBrowserDialog; if ($d.ShowDialog() -eq 'OK') { $pathBox.Text = Join-Path $d.SelectedPath "RagnaDuds\$($cfg.folder)" } })
$panel.Controls.Add($browse)

# striped green progress bar like the website (0..1000)
$script:progress = 0
$bar = New-Object Windows.Forms.Panel; $bar.Location = New-Object Drawing.Point(22, 198); $bar.Size = New-Object Drawing.Size($IW, 18)
$bar.BackColor = [Drawing.Color]::Black
$bar.Add_Paint({
  param($s, $e)
  $g = $e.Graphics; $fill = [int](($s.Width - 4) * $script:progress / 1000)
  for ($x = 2; $x -lt (2 + $fill); $x += 12) {
    $g.FillRectangle((New-Object Drawing.SolidBrush($cGreen)), $x, 2, [Math]::Min(10, 2 + $fill - $x), ($s.Height - 4))
    if ($x + 10 -lt 2 + $fill) { $g.FillRectangle((New-Object Drawing.SolidBrush($cGreenDark)), ($x + 10), 2, 2, ($s.Height - 4)) }
  }
  $g.DrawRectangle((New-Object Drawing.Pen((RGB 68 68 68), 1)), 0, 0, ($s.Width - 1), ($s.Height - 1))
})
$panel.Controls.Add($bar)
function Set-Progress($v) { $script:progress = [int][Math]::Max([double]0, [Math]::Min([double]1000, [double]$v)); $bar.Invalidate() }
$pct = Add-Label '' 22 220 $IW 16 $smallFont $cInk
$notes = Add-Label '' 22 238 $IW 96 $smallFont $cGreen

# full error text (selectable, scrollable) + a button that copies it, so friends can just paste it to Duds
$errBox = New-Object Windows.Forms.TextBox
$errBox.Multiline = $true; $errBox.ReadOnly = $true; $errBox.ScrollBars = 'Vertical'; $errBox.WordWrap = $true
$errBox.Location = New-Object Drawing.Point(22, 238); $errBox.Size = New-Object Drawing.Size($IW, 96)
$errBox.BackColor = [Drawing.Color]::Black; $errBox.ForeColor = (RGB 255 107 107); $errBox.BorderStyle = 'FixedSingle'
$errBox.Font = $smallFont; $errBox.Visible = $false; $errBox.Cursor = 'Hand'
$panel.Controls.Add($errBox)
$copyBtn = New-Object Windows.Forms.Button; $copyBtn.Text = 'COPY ERROR'; $copyBtn.Visible = $false
$copyBtn.Location = New-Object Drawing.Point(22, 340); $copyBtn.Size = New-Object Drawing.Size($IW, 28)
$copyBtn.FlatStyle = 'Flat'; $copyBtn.FlatAppearance.BorderColor = [Drawing.Color]::Black; $copyBtn.FlatAppearance.BorderSize = 2
$copyBtn.BackColor = (RGB 255 143 177); $copyBtn.ForeColor = [Drawing.Color]::Black; $copyBtn.Font = PixelFont 7
$panel.Controls.Add($copyBtn)
function Copy-Error {
  try { [Windows.Forms.Clipboard]::SetText($errBox.Text); $copyBtn.Text = 'COPIED! PASTE IT TO DUDS' }
  catch { $errBox.SelectAll(); $errBox.Focus(); $copyBtn.Text = 'SELECTED - PRESS CTRL+C' }
}
$copyBtn.Add_Click({ Copy-Error })
$errBox.Add_Click({ Copy-Error })
function Show-Error($err) {
  $lines = @("RagnaDuds installer error ($($cfg.title))", "Message: $($err.Exception.Message)")
  if ($err.InvocationInfo -and $err.InvocationInfo.ScriptLineNumber) { $lines += "Script line: $($err.InvocationInfo.ScriptLineNumber)" }
  $lines += "Windows: $([Environment]::OSVersion.VersionString), PowerShell $($PSVersionTable.PSVersion)"
  $lines += "Folder: $($pathBox.Text)"
  $errBox.Text = $lines -join "`r`n"
  $notes.Visible = $false; $errBox.Visible = $true; $copyBtn.Text = 'COPY ERROR'; $copyBtn.Visible = $true
}
function Hide-Error { $errBox.Visible = $false; $copyBtn.Visible = $false; $notes.Visible = $true }
$START = 'Start and YEAAAAAAAAAAH!'

function New-Button($text, $x, $w) {
  $b = New-Object Windows.Forms.Button; $b.Text = $text; $b.Location = New-Object Drawing.Point($x, 376)
  $b.Size = New-Object Drawing.Size($w, 36); $b.BackColor = $cGold; $b.ForeColor = [Drawing.Color]::Black
  $b.FlatStyle = 'Flat'; $b.FlatAppearance.BorderColor = [Drawing.Color]::Black; $b.FlatAppearance.BorderSize = 3
  $b.Font = PixelFont 8
  $panel.Controls.Add($b); return $b
}
$go = New-Button 'INSTALL' 22 ([int]($IW / 2) - 6)
$cancelBtn = New-Button 'CANCEL' (22 + [int]($IW / 2) + 6) ([int]($IW / 2) - 6)
$cancelBtn.BackColor = RGB 85 85 85; $cancelBtn.ForeColor = $cInk
$cancelBtn.Add_Click({ if ($go.Enabled) { $form.Close() } else { $script:cancel = $true } })

# a new grumpy line every few seconds while it works
$timer = New-Object Windows.Forms.Timer; $timer.Interval = 4500; $script:q = 0
$timer.Add_Tick({ if (-not $script:done -and $go.Enabled -eq $false) { $script:q = ($script:q + 1) % $quips.Count; $quip.Text = $quips[$script:q] } })
$timer.Start()

# ---------- reinstall on top of an existing install ----------
# kept on reinstall: settings, screenshots, chat logs (not in game.zip) + our own files in the game folder
$keepDirs = @('savedata', 'screenshot', 'chat', 'replay')
$keepFiles = @('ragnaduds.ico', 'launch.ps1', 'uninstall.ps1', 'ragnaduds-install.json')
function Test-Installed($d) {
  try { $d = [IO.Path]::GetFullPath($d) } catch { return $false }
  (Test-Path -LiteralPath (Join-Path $d 'ragnaduds-install.json')) -or (Test-Path -LiteralPath (Join-Path $d $cfg.exe))
}
function Update-Mode {
  if ($go.Text -eq $START) { return }
  if (Test-Installed $pathBox.Text) {
    $go.Text = 'REINSTALL'; $status.Text = 'Already installed here. REINSTALL updates it (your settings are kept).'
  } else { $go.Text = 'INSTALL'; $status.Text = 'Ready to install.' }
}
$pathBox.Add_TextChanged({ Update-Mode })
function Get-GameProcess($d) {
  Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path.StartsWith($d + '\', [StringComparison]::OrdinalIgnoreCase) }
}
# after unpacking: delete files the new version doesn't have (e.g. old translation files)
function Remove-OldFiles($d, $list) {
  $new = New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
  foreach ($p in $list) { [void]$new.Add(($p[0] -replace '/', '\')) }
  $removed = 0
  foreach ($f in @(Get-ChildItem -LiteralPath $d -Recurse -File -Force)) {
    $rel = $f.FullName.Substring($d.Length + 1)
    $top = $rel.Split('\')[0]
    if ($rel.Contains('\') -and $keepDirs -contains $top.ToLower()) { continue }
    if (-not $rel.Contains('\') -and $keepFiles -contains $rel.ToLower()) { continue }
    if (-not $new.Contains($rel)) { Remove-Item -LiteralPath $f.FullName -Force; $removed++ }
  }
  # empty folders left behind (deepest first)
  foreach ($dir in @(Get-ChildItem -LiteralPath $d -Recurse -Directory -Force | Sort-Object { $_.FullName.Length } -Descending)) {
    if ($keepDirs -contains $dir.FullName.Substring($d.Length + 1).Split('\')[0].ToLower()) { continue }
    if (-not (Get-ChildItem -LiteralPath $dir.FullName -Force)) { Remove-Item -LiteralPath $dir.FullName -Force }
  }
  return $removed
}

# ---------- the game's font: Gulim (Korean, from Microsoft). Western Windows often lacks it -> blurry/small text ----------
function Test-Gulim {
  if (Test-Path -LiteralPath (Join-Path $env:WINDIR 'Fonts\gulim.ttc')) { return $true }
  $reg = Get-ItemProperty -Path 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts' -ErrorAction SilentlyContinue
  return [bool]($reg -and ($reg.PSObject.Properties.Name | Where-Object { $_ -like 'Gulim*' }))
}
function Install-Gulim {
  # Microsoft's free "Korean Supplemental Fonts" (Windows 10 1809+ / 11), from Windows Update; needs admin once
  $cmd = "Add-WindowsCapability -Online -Name 'Language.Fonts.Kore~~~und-KORE~0.0.1.0'"
  try { Start-Process powershell -Verb RunAs -Wait -WindowStyle Hidden -ArgumentList "-NoProfile -Command $cmd" } catch { }
  return (Test-Gulim)
}

# the game starts through launch.ps1 (in the game folder): it puts a random login picture in place first
function Get-LaunchArgs($dest) { "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$(Join-Path $dest 'launch.ps1')`"" }
function Invoke-Game($dest) {
  $psExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
  Start-Process -FilePath $psExe -ArgumentList (Get-LaunchArgs $dest) -WorkingDirectory $dest -WindowStyle Hidden
}

# ---------- install ----------
$go.Add_Click({
  if ($go.Text -eq $START) { Invoke-Game $pathBox.Text; $form.Close(); return }
  $dest = [IO.Path]::GetFullPath($pathBox.Text).TrimEnd('\')
  if (-not (Test-Path $zip)) { $status.Text = "game.zip not found next to the installer. Unzip the whole download first."; return }
  if ([IO.Path]::GetPathRoot($dest).TrimEnd('\') -eq $dest) { $status.Text = 'Pick a folder, not a whole drive.'; return }
  if (Get-GameProcess $dest) { $status.Text = 'The game is still open: close it, then press REINSTALL again.'; return }
  $reinstall = Test-Installed $dest
  Hide-Error
  $go.Enabled = $false; $browse.Enabled = $false; $pathBox.Enabled = $false; $quip.Text = $quips[0]
  try {
    $archive = [IO.Compression.ZipFile]::OpenRead($zip)
    $total = [double](($archive.Entries | Measure-Object -Property Length -Sum).Sum); $done = 0.0
    $buf = New-Object byte[] (4MB); $status.Text = 'Unpacking the game...'
    foreach ($e in $archive.Entries) {
      if ($script:cancel) { throw 'Installation cancelled.' }
      $target = [IO.Path]::GetFullPath((Join-Path $dest $e.FullName))
      if (-not $target.StartsWith($dest, [StringComparison]::OrdinalIgnoreCase)) { continue }   # unsafe path
      if ($e.FullName.EndsWith('/')) { [void](New-Item -ItemType Directory -Force -Path $target); continue }
      [void](New-Item -ItemType Directory -Force -Path (Split-Path -Parent $target))
      $in = $e.Open(); $out = [IO.File]::Create($target)
      try {
        while (($n = $in.Read($buf, 0, $buf.Length)) -gt 0) {
          $out.Write($buf, 0, $n); $done += $n
          Set-Progress (950.0 * $done / [Math]::Max([double]1, $total))          # doubles: games are > 2 GB
          $pct.Text = '{0:N0}%   {1:N1} / {2:N1} GB' -f ($script:progress / 10), ($done / 1GB), ($total / 1GB)
          [Windows.Forms.Application]::DoEvents()
          if ($script:cancel) { throw 'Installation cancelled.' }
        }
      } finally { $out.Dispose(); $in.Dispose() }
    }
    $archive.Dispose()

    # ---- sanity check: every file present with the right size, exe untouched, client points at our server ----
    $status.Text = 'Checking files...'
    $man = Get-Content (Join-Path $here 'manifest.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    # list of [path, size] pairs (older downloads: an object with one property per file)
    if ($man.files -is [array]) { $list = @($man.files | ForEach-Object { ,@($_[0], $_[1]) }) }
    else { $list = @($man.files.PSObject.Properties | ForEach-Object { ,@($_.Name, $_.Value) }) }
    $bad = @(); $i = 0
    foreach ($p in $list) {
      $f = Join-Path $dest ($p[0] -replace '/', '\')
      if (-not (Test-Path -LiteralPath $f) -or (Get-Item -LiteralPath $f).Length -ne [int64]$p[1]) { $bad += $p[0] }
      $i++; if ($i % 50 -eq 0) { Set-Progress (950 + 30.0 * $i / $list.Count); $pct.Text = "Checking $i / $($list.Count)"; [Windows.Forms.Application]::DoEvents() }
    }
    if ($bad.Count) { throw "$($bad.Count) file(s) missing or damaged, e.g. $($bad[0]). Download again and retry." }
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $dest $cfg.exe)).Hash.ToLower()
    if ($hash -ne $man.exe_sha256) { throw "The game exe doesn't match the packaged one (damaged download?)." }
    foreach ($xml in @('data\clientinfo.xml', 'data\sclientinfo.xml')) {
      $xp = Join-Path $dest $xml
      if (Test-Path -LiteralPath $xp) {
        $txt = [IO.File]::ReadAllText($xp, [Text.Encoding]::GetEncoding(28591))
        if (-not ($txt -match '<address>(.*?)</address>') -or $Matches[1].Trim() -ne $cfg.host) { throw "$xml doesn't point to $($cfg.host)." }
      }
    }
    $noteLines = @("OK: $($list.Count) files checked, client -> $($cfg.host):$($cfg.port)")
    if ($reinstall) {
      $status.Text = 'Removing files from the old version...'; [Windows.Forms.Application]::DoEvents()
      $noteLines += "OK: updated, $(Remove-OldFiles $dest $list) old file(s) removed, settings kept"
    }
    $tcp = New-Object Net.Sockets.TcpClient
    try { $ar = $tcp.BeginConnect($cfg.host, [int]$cfg.port, $null, $null); $online = $ar.AsyncWaitHandle.WaitOne(4000) -and $tcp.Connected } catch { $online = $false } finally { $tcp.Close() }
    if ($online) { $noteLines += 'OK: server is online' } else { $noteLines += 'Note: server did not answer right now (offline?). Installed anyway.' }
    if (-not (Test-Gulim)) {
      $ask = [Windows.Forms.MessageBox]::Show("The game's original font (Gulim) is missing on this PC, so the text would look blurry or too small.`n`nInstall Microsoft's Korean fonts now? (free, from Windows Update, about 30 MB; Windows asks for permission once)", "$($cfg.title) - Font", 'YesNo', 'Question')
      if ($ask -eq 'Yes') {
        $status.Text = 'Installing the game font (Windows Update)...'; [Windows.Forms.Application]::DoEvents()
        if (Install-Gulim) { $noteLines += 'OK: game font (Gulim) installed' }
        else { $noteLines += 'Note: font not installed. Settings > Apps > Optional features > Korean Supplemental Fonts' }
      } else { $noteLines += 'Note: game font (Gulim) missing: text may look blurry' }
    } else { $noteLines += 'OK: game font (Gulim) present' }
    $notes.Text = $noteLines -join "`r`n"

    $status.Text = 'Creating shortcuts...'
    Copy-Item (Join-Path $here 'ragnaduds.ico') (Join-Path $dest 'ragnaduds.ico') -Force
    # launcher (random login picture, then the game) + uninstaller, with the config + where the game is
    foreach ($f in @('launch.ps1', 'uninstall.ps1')) { Copy-Item (Join-Path $here $f) (Join-Path $dest $f) -Force }
    $cfg | Add-Member -NotePropertyName dest -NotePropertyValue $dest -Force
    [IO.File]::WriteAllText((Join-Path $dest 'ragnaduds-install.json'), ($cfg | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding($false)))
    $psExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
    $ws = New-Object -ComObject WScript.Shell
    $programs = Join-Path ([Environment]::GetFolderPath('Programs')) 'RagnaDuds'
    [void](New-Item -ItemType Directory -Force -Path $programs)
    foreach ($dir in @([Environment]::GetFolderPath('Desktop'), $programs)) {
      $lnk = $ws.CreateShortcut((Join-Path $dir "$($cfg.shortcut).lnk"))
      $lnk.TargetPath = $psExe; $lnk.Arguments = (Get-LaunchArgs $dest); $lnk.WorkingDirectory = $dest
      $lnk.WindowStyle = 7                                   # minimized: no console flash
      $lnk.IconLocation = (Join-Path $dest 'ragnaduds.ico') + ',0'; $lnk.Description = $cfg.title; $lnk.Save()
    }
    # uninstaller: Start menu entry + Windows "Apps" entry
    $unArgs = "-NoProfile -ExecutionPolicy Bypass -STA -WindowStyle Hidden -File `"$(Join-Path $dest 'uninstall.ps1')`""
    $lnk = $ws.CreateShortcut((Join-Path $programs "Uninstall $($cfg.shortcut).lnk"))
    $lnk.TargetPath = $psExe; $lnk.Arguments = $unArgs; $lnk.WorkingDirectory = $env:TEMP
    $lnk.IconLocation = (Join-Path $dest 'ragnaduds.ico') + ',0'; $lnk.Description = "Uninstall $($cfg.title)"; $lnk.Save()
    $reg = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\RagnaDuds-$($cfg.folder)"
    [void](New-Item -Path $reg -Force)
    $props = @{ DisplayName = $cfg.title; DisplayIcon = (Join-Path $dest 'ragnaduds.ico'); Publisher = 'RagnaDuds'
                InstallLocation = $dest; UninstallString = "`"$psExe`" $unArgs" }
    foreach ($k in $props.Keys) { [void](New-ItemProperty -Path $reg -Name $k -Value $props[$k] -PropertyType String -Force) }
    foreach ($k in @('NoModify', 'NoRepair')) { [void](New-ItemProperty -Path $reg -Name $k -Value 1 -PropertyType DWord -Force) }
    [void](New-ItemProperty -Path $reg -Name 'EstimatedSize' -Value ([int]($total / 1KB)) -PropertyType DWord -Force)
    Set-Progress 1000; $pct.Text = '100%'; $script:done = $true
    $status.Text = "Done! Look for '$($cfg.shortcut)' on your desktop."
    $quip.Text = '"Done. Now go lose your social life."'
    $cancelBtn.Visible = $false
    $go.Text = $START; $go.Size = New-Object Drawing.Size($IW, 36); $go.Enabled = $true
  } catch {
    $status.Text = 'Stopped. The full error is below: press COPY ERROR and send it to Duds.'
    Show-Error $_
    $quip.Text = '"Something broke. Not my fault. Probably yours."'
    $go.Enabled = $true; $browse.Enabled = $true; $pathBox.Enabled = $true; $script:cancel = $false
  }
})

Update-Mode
[void]$form.ShowDialog()
$timer.Stop()
