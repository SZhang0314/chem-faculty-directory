$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$c = Get-Content -Raw -Encoding UTF8 "$dir\chem_szdw.html"
$rows = [regex]::Matches($c, '(?s)<tr[^>]*>.*?</tr>')
$n=0
foreach($r in $rows){ if($r.Value -match 'href=' -and $r.Value -match 'page.htm|faculty|staff'){ $n++ } }
Write-Output "chem rows w/ profile link: $n"
$d = Get-Content -Raw -Encoding UTF8 "$dir\dcp.html"
$rows2 = [regex]::Matches($d, '(?s)<tr[^>]*>.*?</tr>')
$n2=0
foreach($r in $rows2){ if($r.Value -match 'page.htm|list.htm' -and $r.Value -match 'dcp.ustc'){ $n2++ } }
Write-Output "dcp rows: $n2"