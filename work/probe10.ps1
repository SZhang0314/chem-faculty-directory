$dir = "D:\USTC-AI\chem-faculty\work"
$c = Get-Content -Raw -Encoding UTF8 "$dir\chem_szdw.html"
$idx = $c.IndexOf("谢 毅")
$rs = $c.LastIndexOf("<tr", $idx); $re = $c.IndexOf("</tr>", $idx)
$row = $c.Substring($rs, $re-$rs+5)
$cells = [regex]::Matches($row, '(?s)<t[dh][^>]*>.*?</t[dh]>')
$out=@("cell count: $($cells.Count)")
$n=0; foreach($cell in $cells){ $n++; $t=($cell.Value -replace '<[^>]+>','' -replace '&nbsp;',' ' -replace '\s+',' ').Trim(); $out += "[$n] '$t'" }
Set-Content -Path "$dir\chem_cells.txt" -Value $out -Encoding UTF8
Write-Output "done"