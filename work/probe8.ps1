$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$out = @()
$c = Get-Content -Raw -Encoding UTF8 "$dir\polymer.html"
$out += "len: $($c.Length)"
$rows = [regex]::Matches($c, '(?s)<tr[^>]*>.*?</tr>')
$out += "tr count: $($rows.Count)"
$n=0
foreach($r in $rows){ if($r.Value -match 'href'){ $n++; $cells=[regex]::Matches($r.Value,'(?s)<t[dh][^>]*>.*?</t[dh]>'); $vals=@(); foreach($cell in $cells){ $t=($cell.Value -replace '<[^>]+>','' -replace '&nbsp;',' ' -replace '\s+',' ').Trim(); $vals+=$t }; if($n -le 6){ $out += "ROW $n : " + ($vals -join ' | ') } } }
$out += "rows with href: $n"
$out += "has 姓名: " + ($c.IndexOf("姓名") -ge 0)
Set-Content -Path "$dir\polymer_probe.txt" -Value $out -Encoding UTF8
Write-Output "done"