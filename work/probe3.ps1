$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$out = @()
# MSE: find first faculty link row
$c = Get-Content -Raw -Encoding UTF8 "$dir\mse.html"
$i = $c.IndexOf("textvalue=")
$out += "MSE first textvalue ctx:"
$out += $c.Substring([Math]::Max(0,$i-300), 700)
# DCP: locate the main content table (look for marker 研究方向 or 系师资表)
$d = Get-Content -Raw -Encoding UTF8 "$dir\dcp.html"
$m = $d.IndexOf("系师资表")
$out += "DCP 系师资表 idx: $m"
if ($m -ge 0) { $out += $d.Substring([Math]::Max(0,$m-200), 1200) }
Set-Content -Path "$dir\probe_out2.txt" -Value $out -Encoding UTF8
Write-Output "done"