$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$out = @()
$d = Get-Content -Raw -Encoding UTF8 "$dir\dcp.html"
# count faculty li entries
$li = [regex]::Matches($d, 'class="col_item_link')
$out += "dcp col_item_link count: $($li.Count)"
# Find occurrences of 教授 in text to locate table
$m = [regex]::Matches($d, '教授')
$out += "dcp 教授 count: $($m.Count)"
# Locate a faculty name like 朱清时 in main body (not nav)
$idx = $d.IndexOf("朱清时")
$out += "first 朱清时 idx: $idx ; total len $($d.Length)"
$idx2 = $d.LastIndexOf("朱清时")
$out += "last 朱清时 idx: $idx2"
if ($idx2 -ge 0) { $out += "ctx around last:"; $out += $d.Substring([Math]::Max(0,$idx2-400), 1000) }
Set-Content -Path "$dir\probe_out3.txt" -Value $out -Encoding UTF8
Write-Output "done"