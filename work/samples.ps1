$j = Get-Content -Raw -Encoding UTF8 "D:\USTC-AI\chem-faculty\data\raw\ustc.json" | ConvertFrom-Json
$j.professors | Where-Object { $_.department -eq "化学系" } | Select-Object -First 6 | ForEach-Object { Write-Output ($_.name + " => " + $_.profile_url) }
Write-Output "---dcp---"
$j.professors | Where-Object { $_.department -eq "化学物理系" } | Select-Object -First 4 | ForEach-Object { Write-Output ($_.name + " => " + $_.profile_url) }
Write-Output "---mse---"
$j.professors | Where-Object { $_.department -eq "材料科学与工程系" } | Select-Object -First 4 | ForEach-Object { Write-Output ($_.name + " => " + $_.profile_url) }
Write-Output "---poly---"
$j.professors | Where-Object { $_.department -eq "高分子科学与工程系" } | Select-Object -First 4 | ForEach-Object { Write-Output ($_.name + " => " + $_.profile_url) }