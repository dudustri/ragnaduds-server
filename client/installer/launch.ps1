# RagnaDuds launcher for Windows: shows the next login picture (they take turns), then starts the game.
# The login pictures are GRF archives (ragnaduds_login1.grf, ...): DATA.INI line 0 names the one the game loads
# first, so this just rewrites that line. The RagnaDuds desktop/Start menu shortcuts run this hidden (the
# installer copies it into the game folder, next to ragnaduds-install.json).
# Keep this file ASCII-only (PowerShell 5.1 reads it as ANSI).

$d = Split-Path -Parent $MyInvocation.MyCommand.Path
$cfg = Get-Content -LiteralPath (Join-Path $d 'ragnaduds-install.json') -Raw -Encoding UTF8 | ConvertFrom-Json
try {
  $lp = $cfg.login_pics
  $grfs = @($lp.grfs)
  if ($grfs.Count -gt 1) {
    $ini = Join-Path $d $lp.ini
    $lines = [IO.File]::ReadAllLines($ini)
    $cur = ($lines | Where-Object { $_ -match '^\s*0\s*=' } | Select-Object -First 1) -replace '^\s*0\s*=\s*', ''
    $pick = $grfs[([array]::IndexOf($grfs, $cur.Trim()) + 1) % $grfs.Count]     # the next one: they alternate
    for ($i = 0; $i -lt $lines.Count; $i++) { if ($lines[$i] -match '^\s*0\s*=') { $lines[$i] = "0=$pick" } }
    [IO.File]::WriteAllLines($ini, $lines)
  }
} catch { }   # a picture problem must never stop the game from starting
$exe = Join-Path $d $cfg.exe
if ($cfg.args) { Start-Process -FilePath $exe -ArgumentList $cfg.args -WorkingDirectory $d }
else { Start-Process -FilePath $exe -WorkingDirectory $d }
