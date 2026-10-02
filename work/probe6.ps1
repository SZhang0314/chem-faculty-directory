$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$out = @()
$c = Get-Content -Raw -Encoding UTF8 "$dir\mse.html"
# Find headings/section titles
foreach($kw in @("材料科学与工程系","高分子科学与工程系","教授","副教授","特任","博士后","研究人员","工程技术","党政管理","院士","退休")){ $i=$c.IndexOf($kw); $out += "$kw => idx $i" }
# extract all rows with textvalue
$rows = [regex]::Matches($c, '(?s)<tr[^>]*>.*?</tr>')
$out += "total tr rows: $($rows.Count)"
$n=0
foreach($r in $rows){
  if($r.Value -match 'textvalue'){ $n++; $cells=[regex]::Matches($r.Value,'(?s)<t[dh].*?</t[dh]>'); $names=@(); foreach($cell in $cells){ $t=($cell.Value -replace '<[^>]+>','' -replace '&nbsp;',' ' -replace '\s+',' ').Trim(); if($t -ne ''){$names+=$t} }; if($n -le 3){ $out += "ROW $n : " + ($names -join ' | ') } }
}
$out += "rows with textvalue: $n"
Set-Content -Path "$dir\mse_probe.txt" -Value $out -Encoding UTF8
Write-Output "done"