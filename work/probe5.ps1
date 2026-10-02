$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$out = @()
$d = Get-Content -Raw -Encoding UTF8 "$dir\dcp.html"
# find the first data row containing 朱清时 within a table; get its <tr>...</tr>
$idx = $d.LastIndexOf("朱清时")
$rs = $d.LastIndexOf("<tr", $idx)
$re = $d.IndexOf("</tr>", $idx)
$row = $d.Substring($rs, $re-$rs+5)
$out += "ROW cells:"
$cells = [regex]::Matches($row, '(?s)<td.*?</td>')
$n=0; foreach($cell in $cells){ $n++; $txt = ($cell.Value -replace '<[^>]+>','' -replace '&nbsp;',' ' -replace '\s+',' ').Trim(); $out += "  [$n] $txt" }
# header: search upward for a tr containing 姓名
$hidx = $d.LastIndexOf("姓名", $idx)
if ($hidx -ge 0) { $hrs=$d.LastIndexOf("<tr",$hidx); $hre=$d.IndexOf("</tr>",$hidx); $hr=$d.Substring($hrs,$hre-$hrs+5); $out += "HEADER cells:"; $hc=[regex]::Matches($hr,'(?s)<t[dh].*?</t[dh]>'); $k=0; foreach($cell in $hc){$k++;$txt=($cell.Value -replace '<[^>]+>','' -replace '&nbsp;',' ' -replace '\s+',' ').Trim(); $out += "  [$k] $txt"} }
Set-Content -Path "$dir\dcp_probe.txt" -Value $out -Encoding UTF8
Write-Output "done"