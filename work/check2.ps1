$j = Get-Content -Raw -Encoding UTF8 "D:\USTC-AI\chem-faculty\data\raw\ustc.json" | ConvertFrom-Json
Write-Output "valid JSON, total = $($j.professors.Count)"
$j.professors | Where-Object { $_.name -match '\*' } | ForEach-Object { Write-Output ("ASTERISK: [" + $_.department + "] '" + $_.name + "'") }
$j.professors | Where-Object { $_.title -eq '' } | ForEach-Object { Write-Output ("EMPTY TITLE: [" + $_.department + "] '" + $_.name + "'") }
Write-Output "--- sample records ---"
$j.professors | Where-Object { $_.department -eq "化学系" } | Select-Object -First 1 | ConvertTo-Json -Depth 4
$j.professors | Where-Object { $_.department -eq "高分子科学与工程系" } | Select-Object -First 1 | ConvertTo-Json -Depth 4
$j.professors | Where-Object { $_.department -eq "化学物理系" } | Select-Object -Last 1 | ConvertTo-Json -Depth 4
$j.professors | Where-Object { $_.department -eq "材料科学与工程系" } | Select-Object -Last 1 | ConvertTo-Json -Depth 4