$j = Get-Content -Raw -Encoding UTF8 "D:\USTC-AI\chem-faculty\data\raw\ustc.json" | ConvertFrom-Json
Write-Output "total=$($j.professors.Count)"
$j.professors | Where-Object { $_.name -match '\*|\s' } | ForEach-Object { Write-Output ("CLEAN-CHECK: '" + $_.name + "'") }
Write-Output "--- dept counts ---"
$j.professors | Group-Object department | Sort-Object Name | ForEach-Object { Write-Output ("  " + $_.Name + " = " + $_.Count) }
Write-Output "--- first of each dept ---"
foreach($d in ($j.professors.department | Select-Object -Unique)){ $x = $j.professors | Where-Object { $_.department -eq $d } | Select-Object -First 1; Write-Output ($d + " :: " + $x.name + " | " + $x.title + " | " + $x.research_area + " | " + $x.profile_url) }