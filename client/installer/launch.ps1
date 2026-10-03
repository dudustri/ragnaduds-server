# RagnaDuds launcher for Windows: the desktop / Start menu shortcuts open this window. It checks the website for a
# newer client (patch.json: every game file with its size and sha256), downloads only the files that changed,
# then the green PLAY button starts the game (with the next login picture: they take turns).
# Same retro look as the installer. No internet / website down / game already open: you can still play.
# Our state: ragnaduds-patch.json in the game folder (path -> sha256 of what's installed).
# Keep this file ASCII-only (PowerShell 5.1 reads it as ANSI).

Add-Type -AssemblyName System.Windows.Forms, System.Drawing
[System.Windows.Forms.Application]::EnableVisualStyles()
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$d = Split-Path -Parent $MyInvocation.MyCommand.Path
$cfg = Get-Content -LiteralPath (Join-Path $d 'ragnaduds-install.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$statePath = Join-Path $d 'ragnaduds-patch.json'

# ---------- colors + fonts (same as the installer and the website) ----------
function RGB($r, $g, $b) { [Drawing.Color]::FromArgb($r, $g, $b) }
$cBg = RGB 20 18 31; $cPanel = RGB 34 29 51; $cInk = RGB 246 236 210; $cGold = RGB 255 209 102
$cWood = RGB 107 79 42; $cGoldEdge = RGB 201 162 91; $cBlue = RGB 124 196 255; $cPink = RGB 255 143 177
$cGreen = RGB 126 224 129; $cGreenDark = RGB 92 191 95; $cShadow = RGB 122 62 18
$script:fonts = New-Object Drawing.Text.PrivateFontCollection
$pixelFamily = $null
foreach ($f in @((Join-Path $d 'PressStart2P-Regular.ttf'), (Join-Path $d 'installer\PressStart2P-Regular.ttf'))) {
  if (-not $pixelFamily -and (Test-Path -LiteralPath $f)) { try { $script:fonts.AddFontFile($f); $pixelFamily = $script:fonts.Families[0] } catch { } }
}
function PixelFont($size) {
  if ($pixelFamily) { New-Object Drawing.Font($pixelFamily, $size) } else { New-Object Drawing.Font('Consolas', ($size + 3), [Drawing.FontStyle]::Bold) }
}
$bodyFont = New-Object Drawing.Font('Consolas', 9.5)
$smallFont = New-Object Drawing.Font('Consolas', 8.5)

# ---------- window: photo on top, retro panel below ----------
$W = 440; $panelH = 300
$workH = [Windows.Forms.Screen]::PrimaryScreen.WorkingArea.Height
$photoH = [int][Math]::Max([double]200, [Math]::Min([double]420, [double]($workH - $panelH - 80)))
$form = New-Object Windows.Forms.Form
$form.Text = $cfg.title; $form.ClientSize = New-Object Drawing.Size($W, ($photoH + $panelH + 10))
$form.FormBorderStyle = 'FixedDialog'; $form.MaximizeBox = $false; $form.StartPosition = 'CenterScreen'
$form.BackColor = $cBg; $form.ForeColor = $cInk
$ico = Join-Path $d 'ragnaduds.ico'; if (Test-Path -LiteralPath $ico) { $form.Icon = New-Object Drawing.Icon $ico }
$photo = Join-Path $d 'duds_ok_bg.png'
if (Test-Path -LiteralPath $photo) {
  $pic = New-Object Windows.Forms.PictureBox
  $pic.Image = [Drawing.Image]::FromFile($photo); $pic.SizeMode = 'Zoom'; $pic.BackColor = $cBg
  $pic.Location = New-Object Drawing.Point(10, 8); $pic.Size = New-Object Drawing.Size(($W - 20), $photoH)
  $form.Controls.Add($pic)
} else { $photoH = 0 }
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
$IW = $W - 20 - 44
function Add-Label($text, $x, $y, $w, $h, $font, $color) {
  $l = New-Object Windows.Forms.Label; $l.Text = $text; $l.AutoSize = $false; $l.BackColor = $cPanel
  $l.Location = New-Object Drawing.Point($x, $y); $l.Size = New-Object Drawing.Size($w, $h)
  $l.Font = $font; $l.ForeColor = $color
  $panel.Controls.Add($l); return $l
}
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
$status = Add-Label 'Checking for updates...' 22 76 $IW 34 $bodyFont $cInk
$script:progress = 0
$bar = New-Object Windows.Forms.Panel; $bar.Location = New-Object Drawing.Point(22, 114); $bar.Size = New-Object Drawing.Size($IW, 18)
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
$pct = Add-Label '' 22 136 $IW 16 $smallFont $cInk
$notes = Add-Label '' 22 156 $IW 64 $smallFont $cGreen
$errBox = New-Object Windows.Forms.TextBox
$errBox.Multiline = $true; $errBox.ReadOnly = $true; $errBox.ScrollBars = 'Vertical'; $errBox.WordWrap = $true
$errBox.Location = New-Object Drawing.Point(22, 156); $errBox.Size = New-Object Drawing.Size($IW, 64)
$errBox.BackColor = [Drawing.Color]::Black; $errBox.ForeColor = (RGB 255 107 107); $errBox.BorderStyle = 'FixedSingle'
$errBox.Font = $smallFont; $errBox.Visible = $false
$panel.Controls.Add($errBox)

function New-Button($text, $x, $w) {
  $b = New-Object Windows.Forms.Button; $b.Text = $text; $b.Location = New-Object Drawing.Point($x, 232)
  $b.Size = New-Object Drawing.Size($w, 36); $b.ForeColor = [Drawing.Color]::Black
  $b.FlatStyle = 'Flat'; $b.FlatAppearance.BorderColor = [Drawing.Color]::Black; $b.FlatAppearance.BorderSize = 3
  $b.Font = PixelFont 9
  $panel.Controls.Add($b); return $b
}
$play = New-Button 'PLAY' 22 ([int]($IW * 2 / 3) - 6)
$play.Enabled = $false; $play.BackColor = RGB 85 85 85
$closeBtn = New-Button 'CLOSE' (22 + [int]($IW * 2 / 3) + 6) ([int]($IW / 3) - 6)
$closeBtn.BackColor = RGB 85 85 85; $closeBtn.ForeColor = $cInk
$closeBtn.Add_Click({ $script:cancel = $true; $form.Close() })
function Enable-Play($text) {
  $play.Text = $text; $play.BackColor = $cGreen; $play.Enabled = $true; [Windows.Forms.Application]::DoEvents()
}

# ---------- the game: next login picture (DATA.INI line 0 = one of our login GRFs), then the exe ----------
function Start-Game {
  try {
    $lp = $cfg.login_pics; $grfs = @($lp.grfs)
    if ($grfs.Count -gt 1) {
      $ini = Join-Path $d $lp.ini
      $lines = [IO.File]::ReadAllLines($ini)
      $cur = ($lines | Where-Object { $_ -match '^\s*0\s*=' } | Select-Object -First 1) -replace '^\s*0\s*=\s*', ''
      $pick = $grfs[([array]::IndexOf($grfs, $cur.Trim()) + 1) % $grfs.Count]
      for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^\s*0\s*=') { $lines[$i] = "0=$pick" } }
      [IO.File]::WriteAllLines($ini, $lines)
    }
  } catch { }   # a picture problem must never stop the game from starting
  $exe = Join-Path $d $cfg.exe
  if ($cfg.args) { Start-Process -FilePath $exe -ArgumentList $cfg.args -WorkingDirectory $d }
  else { Start-Process -FilePath $exe -WorkingDirectory $d }
}
$play.Add_Click({ Start-Game; $form.Close() })

# ---------- update ----------
function Get-Sha($path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash.ToLower() }
function Save-State($state) {
  $o = New-Object PSObject; foreach ($k in $state.Keys) { $o | Add-Member -NotePropertyName $k -NotePropertyValue $state[$k] }
  [IO.File]::WriteAllText($statePath, ($o | ConvertTo-Json -Compress), (New-Object Text.UTF8Encoding($false)))
}
function New-Request($url) {
  $r = [Net.HttpWebRequest]::Create($url); $r.Timeout = 15000; $r.ReadWriteTimeout = 30000
  $r.Headers.Add('Cookie', "rd_auth=$($cfg.patch.token)"); $r.AllowAutoRedirect = $false; $r.UserAgent = 'RagnaDuds-Launcher'
  return $r
}
function Get-Url($rel) { $cfg.patch.url + ((($rel -split '/') | ForEach-Object { [Uri]::EscapeDataString($_) }) -join '/') }

function Update-Game {
  if (-not $cfg.patch -or -not $cfg.patch.url) { $status.Text = 'Ready.'; return 'This install has no auto-update (reinstall once from the website to get it).' }
  $running = Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.Path -and $_.Path.StartsWith($d + '\', [StringComparison]::OrdinalIgnoreCase) }
  if ($running) { $status.Text = 'The game is already open: updates are checked next time.'; return '' }

  # the list of files on the website
  $resp = (New-Request ($cfg.patch.url + 'patch.json')).GetResponse()
  if ([int]$resp.StatusCode -ne 200) { $resp.Close(); throw 'The website did not send the update list (login changed? reinstall from the website).' }
  $reader = New-Object IO.StreamReader($resp.GetResponseStream(), [Text.Encoding]::UTF8)
  $remote = $reader.ReadToEnd() | ConvertFrom-Json; $reader.Close(); $resp.Close()

  # what we have: our state file, or (first time) the files on disk
  $state = @{}
  if (Test-Path -LiteralPath $statePath) {
    $old = Get-Content -LiteralPath $statePath -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($p in $old.PSObject.Properties) { $state[$p.Name] = $p.Value }
  }
  $first = $state.Count -eq 0
  $todo = @(); $total = [double]0; $i = 0; $list = @($remote.files)
  foreach ($e in $list) {
    $rel = [string]$e[0]; $size = [int64]$e[1]; $sha = [string]$e[2]
    if ($e.Count -gt 3 -and $e[3] -ne 'win') { continue }            # Linux-only launcher files
    $local = Join-Path $d ($rel -replace '/', '\')
    $have = Test-Path -LiteralPath $local
    if ($have -and $first) {
      if ((Get-Item -LiteralPath $local).Length -ne $size) { $have = $false }
      elseif ($size -lt 64MB -and (Get-Sha $local) -ne $sha) { $have = $false }   # big archives: size is enough
      else { $state[$rel] = $sha }
    }
    $i++; if ($i % 40 -eq 0) { $status.Text = "Checking files... $i / $($list.Count)"; Set-Progress (100.0 * $i / $list.Count); [Windows.Forms.Application]::DoEvents() }
    if (-not $have -or $state[$rel] -ne $sha -or (Get-Item -LiteralPath $local).Length -ne $size) { $todo += ,@($rel, $size, $sha); $total += $size }
  }
  if ($first) { Save-State $state }

  # files the new version doesn't have any more
  $names = New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)
  foreach ($e in $list) { [void]$names.Add([string]$e[0]) }
  $removed = 0
  foreach ($k in @($state.Keys)) {
    if (-not $names.Contains($k)) {
      $f = Join-Path $d ($k -replace '/', '\')
      if (Test-Path -LiteralPath $f) { Remove-Item -LiteralPath $f -Force -ErrorAction SilentlyContinue; $removed++ }
      $state.Remove($k)
    }
  }
  if ($todo.Count -eq 0) {
    Set-Progress 1000; $status.Text = "Up to date ($($remote.version))."
    if ($removed) { Save-State $state }
    return ''
  }

  # download the changed files
  $done = [double]0; $buf = New-Object byte[] (1MB); $n = 0
  $tmp = Join-Path $d '.patch'; [void](New-Item -ItemType Directory -Force -Path $tmp)
  foreach ($t in $todo) {
    if ($script:cancel) { throw 'Update cancelled.' }
    $rel = $t[0]; $n++
    $status.Text = "Updating $n / $($todo.Count): $rel"
    $part = Join-Path $tmp ([IO.Path]::GetFileName(($rel -replace '/', '\')) + '.part')
    $resp = (New-Request (Get-Url $rel)).GetResponse()
    if ([int]$resp.StatusCode -ne 200) { $resp.Close(); throw "Download failed: $rel" }
    $in = $resp.GetResponseStream(); $out = [IO.File]::Create($part)
    try {
      while (($k = $in.Read($buf, 0, $buf.Length)) -gt 0) {
        $out.Write($buf, 0, $k); $done += $k
        Set-Progress (1000.0 * $done / [Math]::Max([double]1, $total))
        $pct.Text = '{0:N0}%   {1:N1} / {2:N1} MB' -f ($script:progress / 10), ($done / 1MB), ($total / 1MB)
        [Windows.Forms.Application]::DoEvents()
        if ($script:cancel) { throw 'Update cancelled.' }
      }
    } finally { $out.Dispose(); $in.Dispose(); $resp.Close() }
    if ((Get-Sha $part) -ne $t[2]) { Remove-Item -LiteralPath $part -Force; throw "Damaged download: $rel (try again)" }
    $local = Join-Path $d ($rel -replace '/', '\')
    [void](New-Item -ItemType Directory -Force -Path (Split-Path -Parent $local))
    Move-Item -LiteralPath $part -Destination $local -Force
    $state[$rel] = $t[2]; Save-State $state
  }
  Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue
  Set-Progress 1000; $pct.Text = ''
  $status.Text = "Updated! ($($remote.version))"
  return ("Updated $($todo.Count) file(s), {0:N1} MB" -f ($total / 1MB)) + $(if ($removed) { ", removed $removed old file(s)" } else { '' })
}

$form.Add_Shown({
  [Windows.Forms.Application]::DoEvents()
  try {
    $msg = Update-Game
    if ($msg) { $notes.Text = $msg }
    Enable-Play 'PLAY'
  } catch {
    if ($script:cancel) { return }
    $status.Text = "Couldn't update right now. You can still play."
    $errBox.Text = "RagnaDuds launcher ($($cfg.title)): $($_.Exception.Message)"
    $errBox.Visible = $true; $notes.Visible = $false
    Enable-Play 'PLAY ANYWAY'
  }
})
[void]$form.ShowDialog()
