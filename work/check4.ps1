$j = Get-Content -Raw -Encoding UTF8 "D:\USTC-AI\chem-faculty\data\raw\ustc.json" | ConvertFrom-Json
Write-Output ("JSON OK. school=" + $j.school + " ; source_urls=" + $j.source_urls.Count + " ; professors=" + $j.professors.Count)
$out=@()
foreach($d in ($j.professors.department | Select-Object -Unique)){
  $list = $j.professors | Where-Object { $_.department -eq $d }
  $out += "== $d ($($list.Count)) =="
  $list | Select-Object -First 3 | ForEach-Object { $out += ("  F: " + $_.name + " / " + $_.title + " / " + $_.research_area) }
  $list | Select-Object -Last 3 | ForEach-Object { $out += ("  L: " + $_.name + " / " + $_.title + " / " + $_.research_area) }
}
Set-Content -Path "D:\USTC-AI\chem-faculty\work\final.txt" -Value $out -Encoding UTF8