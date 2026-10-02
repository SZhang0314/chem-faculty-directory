$ErrorActionPreference = "Stop"
$dir = "D:\USTC-AI\chem-faculty\work"
$outPath = "D:\USTC-AI\chem-faculty\data\raw\ustc.json"
New-Item -ItemType Directory -Force -Path (Split-Path $outPath) | Out-Null

function HtmlToText($s) {
    if ($null -eq $s) { return "" }
    $t = $s -replace '(?s)<script.*?</script>', ''
    $t = $t -replace '(?s)<style.*?</style>', ''
    $t = $t -replace '<[^>]+>', ' '
    $t = $t -replace '&nbsp;', ' '
    $t = $t -replace '&amp;', '&'
    $t = $t -replace '&#39;', "'"
    $t = $t -replace '&quot;', '"'
    $t = $t -replace '\s+', ' '
    return $t.Trim()
}

function Get-Cells($rowHtml) {
    $cells = [regex]::Matches($rowHtml, '(?s)<t[dh][^>]*>.*?</t[dh]>')
    $res = @()
    foreach ($c in $cells) { $res += ,@{ html = $c.Value; text = (HtmlToText $c.Value) } }
    return $res
}

function Get-Link($cellHtml) {
    $m = [regex]::Match($cellHtml, 'href="([^"]+)"')
    if ($m.Success) { return $m.Groups[1].Value }
    return ""
}

# Normalize a URL that may be relative
function AbsUrl($url, $base) {
    if ([string]::IsNullOrWhiteSpace($url)) { return "" }
    if ($url -match '^https?://') { return $url }
    if ($url.StartsWith('/')) { return ($base.TrimEnd('/') + $url) }
    return $url
}

$professors = @()

# ---------- 化学系 (chem.ustc.edu.cn/2476/list.htm) ----------
# columns: 姓名 | (blank) | 职称 | 专业 | 联系电话 | 电子信箱
$c = Get-Content -Raw -Encoding UTF8 "$dir\chem_szdw.html"
$rows = [regex]::Matches($c, '(?s)<tr[^>]*>.*?</tr>')
foreach ($r in $rows) {
    if ($r.Value -notmatch 'page\.htm|faculty\.ustc|staff\.ustc|team\.ustc|x-mol|zhanglab|renlab|yllu') { continue }
    $cells = Get-Cells $r.Value
    if ($cells.Count -lt 3) { continue }
    $name = $cells[0].text
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Length -gt 12) { continue }
    if ($name -match '姓名|职称|专业|联系|信箱') { continue }
    $link = Get-Link $cells[0].html
    $title = ""
    $area = ""
    if ($cells.Count -ge 3) { $title = $cells[1].text; $area = $cells[2].text }
    $professors += [ordered]@{
        name = $name; name_en = ""; title = $title; research_area = $area;
        profile_url = (AbsUrl $link "https://chem.ustc.edu.cn"); department = "化学系"
    }
}

# ---------- 化学物理系 (dcp.ustc.edu.cn/4437/list.htm) ----------
# columns: 姓名 | 职称 | 电话 | 电子邮件 | 备注
$d = Get-Content -Raw -Encoding UTF8 "$dir\dcp.html"
$rows = [regex]::Matches($d, '(?s)<tr[^>]*>.*?</tr>')
foreach ($r in $rows) {
    if ($r.Value -notmatch 'href="[^"]*(page\.htm|list\.htm)"') { continue }
    if ($r.Value -notmatch 'dcp\.ustc\.edu\.cn') { continue }
    $cells = Get-Cells $r.Value
    if ($cells.Count -lt 2) { continue }
    $name = $cells[0].text
    $name = ($name -replace '[\*＊]', '').Trim()
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Length -gt 12) { continue }
    if ($name -match '姓名|职称|电话|邮件|备注') { continue }
    $link = Get-Link $cells[0].html
    $title = $cells[1].text
    $professors += [ordered]@{
        name = $name; name_en = ""; title = $title; research_area = "";
        profile_url = (AbsUrl $link "https://dcp.ustc.edu.cn"); department = "化学物理系"
    }
}

# ---------- 材料科学与工程系 (mse.ustc.edu.cn/3334/list.htm) ----------
# columns: 姓名 | 职称 | 电话 | email | talent | position
$m = Get-Content -Raw -Encoding UTF8 "$dir\mse.html"
$rows = [regex]::Matches($m, '(?s)<tr[^>]*>.*?</tr>')
foreach ($r in $rows) {
    if ($r.Value -notmatch 'textvalue') { continue }
    $cells = Get-Cells $r.Value
    if ($cells.Count -lt 2) { continue }
    $name = $cells[0].text
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Length -gt 12) { continue }
    $link = Get-Link $cells[0].html
    $title = $cells[1].text
    $professors += [ordered]@{
        name = $name; name_en = ""; title = $title; research_area = "";
        profile_url = (AbsUrl $link "https://mse.ustc.edu.cn"); department = "材料科学与工程系"
    }
}

# ---------- 高分子科学与工程系 (polymer.ustc.edu.cn page) ----------
# columns: 姓名 | 职称 | 邮箱 | 电话
$p = Get-Content -Raw -Encoding UTF8 "$dir\polymer.html"
$rows = [regex]::Matches($p, '(?s)<tr[^>]*>.*?</tr>')
foreach ($r in $rows) {
    if ($r.Value -notmatch 'href=') { continue }
    $cells = Get-Cells $r.Value
    if ($cells.Count -lt 2) { continue }
    $name = $cells[0].text
    if ([string]::IsNullOrWhiteSpace($name) -or $name.Length -gt 12) { continue }
    if ($name -match '姓名|职称|邮箱|电话') { continue }
    $link = Get-Link $cells[0].html
    $title = $cells[1].text
    $professors += [ordered]@{
        name = $name; name_en = ""; title = $title; research_area = "";
        profile_url = (AbsUrl $link "https://polymer.ustc.edu.cn"); department = "高分子科学与工程系"
    }
}

# normalize names: strip asterisk markers and internal spaces
foreach ($p in $professors) {
    $p.name = ($p.name -replace '[\*＊]', '' -replace '\s+', '').Trim()
    $p.title = ($p.title -replace '\s+', ' ').Trim()
    $p.title = $p.title -replace '([，、。：；])\s+', '$1'
    $p.research_area = ($p.research_area -replace '\s+', ' ').Trim()
}

$result = [ordered]@{
    school = "中国科学技术大学"
    source_urls = @(
        "https://scms.ustc.edu.cn/41112/list.htm",
        "https://chem.ustc.edu.cn/2476/list.htm",
        "https://dcp.ustc.edu.cn/4437/list.htm",
        "https://mse.ustc.edu.cn/3334/list.htm",
        "https://polymer.ustc.edu.cn/2010/1123/c25100a474969/page.htm"
    )
    professors = $professors
}

$json = $result | ConvertTo-Json -Depth 5
[System.IO.File]::WriteAllText($outPath, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Output "TOTAL: $($professors.Count)"
Write-Output "Written: $outPath"
