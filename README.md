# 中国十一校化学方向教师目录 · Chemistry Faculty Directory

A browsable, searchable directory of chemistry-related faculty across 11 leading
Chinese universities (化学 / 高分子 / 材料 / 化工 / 化学生物学 units).

## Live page

Open `index.html` directly, or visit the GitHub Pages URL (see repo settings).

Features: full-text search, filters by university / department / research direction,
sorting by name / school / title. Each card shows the professor's title, research
directions, research summary, selected publications, and links to the official
profile, email and personal homepage.

## Covered universities (11)

| University | Records |
|---|---|
| 四川大学 Sichuan University | 500 |
| 南京大学 Nanjing University | 420 |
| 吉林大学 Jilin University | 341 |
| 南开大学 Nankai University | 327 |
| 复旦大学 Fudan University | 306 |
| 上海交通大学 Shanghai Jiao Tong University | 245 |
| 浙江大学 Zhejiang University | 209 |
| 北京大学 Peking University | 198 |
| 中国科学技术大学 USTC | 167 |
| 中国科学院大学 UCAS (专任教师) | 147 |
| 清华大学 Tsinghua University | 88 |
| **Total** | **2,948** |

Scope: chemistry colleges/departments plus chemistry-adjacent units (polymer,
materials, chemical engineering, chemical biology). Administrative staff,
technicians, retirees and postdocs are excluded. For UCAS only the 147
专任教师 are included (not the 970 研究生导师 or the 406 Institute of Chemistry
researchers).

## Data

- `data/faculty.json` — source of truth, one record per researcher (schema below).
- `data/raw/*.json` — per-school coarse rosters scraped from official directories.
- `data/raw/*_fine.json` — enriched per-school records.
- `work/` — scraping, enrichment and consolidation scripts (audit trail).

### Fields

| field | meaning |
|---|---|
| `name` / `name_en` | name (Chinese / English when listed) |
| `school` / `department` | university and college/institute |
| `title` | 教授 / 研究员 / 副教授 / 助理教授 / 院士 ... |
| `subject` | broad subject (化学) |
| `research_directions` | research-direction list (from 研究方向/研究领域) |
| `focus_areas` | finer sub-directions |
| `summary` | short research summary (from the official profile) |
| `publications` | up to 5 selected publications parsed from the profile |
| `homepage` | personal/lab homepage when listed |
| `profile_url` | official university profile page |
| `email` | listed institutional email |
| `sources` | URLs actually used |
| `confidence` | `fine` (enriched) or `coarse` (roster only) |
| `verified` | identity/enrichment verified from a first-party page |

## Method

Two-pass search per the `search_prof` workflow:

1. **Coarse** — scrape each university's official chemistry faculty directory
   (师资队伍 / 教师名录), paginating all rank categories.
2. **Fine** — fetch each individual profile page and extract research directions,
   summary, publications, email and homepage with per-site parsers.

All data is public and first-party (official department profile pages). Nothing
is invented: fields that could not be verified are omitted.

## Accuracy notes

- Names, titles, emails and research text come from the official profile pages.
- `publications` are parsed best-effort from the profile's 代表性论文 / 学术成果
  section; no publication is fabricated.
- Some profiles publish no homepage / publications — those fields are left empty.
- Counts and `generated_at` are recorded in `data/faculty.json`.

## Regenerate

```bash
python scripts/validate_data.py --data data/faculty.json
python scripts/build_site.py --data data/faculty.json --out . \
       --title "中国十一校化学方向教师目录 · Chemistry Faculty Directory"
```
