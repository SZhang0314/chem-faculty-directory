$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$out = @()
$c = Get-Content -Raw -Encoding UTF8 "$dir\scms_41112.html"
# find list items in wp_articlecontent / content area
$rows = [regex]::Matches($c, '(?s)<li[^>]*>.*?</li>')
$out += "li count: $($rows.Count)"
foreach($r in $rows){ $t=($r.Value -replace '<[^>]+>','' -replace '&nbsp;',' ' -replace '\s+',' ').Trim(); if($t -match '系|中心'){ $href=[regex]::Match($r.Value,'href="([^"]+)"').Groups[1].Value; $out += "$t => $href" } }
Set-Content -Path "$dir\scms_probe.txt" -Value $out -Encoding UTF8
Write-Output "done"