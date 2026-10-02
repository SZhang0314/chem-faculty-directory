$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
function Get-Header($file, $marker) {
    $c = Get-Content -Raw -Encoding UTF8 $file
    $th = $c.IndexOf($marker)
    if ($th -lt 0) { return "NOTFOUND" }
    $rs = $c.LastIndexOf("<tr", $th)
    $re = $c.IndexOf("</tr>", $th)
    $row = $c.Substring($rs, $re - $rs + 5)
    return ($row -replace '<[^>]+>', '|' -replace '&nbsp;', ' ' -replace '\|+', '|')
}
$out = @()
$out += "MSE header: " + (Get-Header "$dir\mse.html" "姓名")
$out += "CHEM header: " + (Get-Header "$dir\chem_szdw.html" "姓名")
$out += "APPL header: " + (Get-Header "$dir\applchem.html" "姓名")
Set-Content -Path "$dir\probe_out.txt" -Value $out -Encoding UTF8
Write-Output "done"