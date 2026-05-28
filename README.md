# OSINT Tools and Resources Handbook 2026

A machine-readable dataset of every OSINT tool listed on [osinthandbook.com](https://www.osinthandbook.com) — the live, continuously-updated successor to the i-intelligence OSINT Handbook.

**6,718 tools across 214 categories.** Name, description, and URL for every entry.

The original site is intentionally difficult to extract programmatically. This repo fixes that.

## Data

| File | Format | Contents |
|------|--------|----------|
| `data/tools.json` | JSON | All tools by category — name, description, URL |
| `data/tools.csv` | CSV | Flat: `category, tool_name, description, url` |
| `data/handbook_2020_categories.json` | JSON | Category index from the 2020 PDF (45 categories, 7,442 tools) |

### tools.json structure

```json
{
  "source": "osinthandbook.com",
  "year": 2026,
  "total_categories": 214,
  "total_tools": 6718,
  "categories": [
    {
      "slug": "academic-research-tools",
      "name": "Academic Research Tools",
      "tools": [
        {
          "name": "Google Scholar",
          "url": "https://scholar.google.com/",
          "description": "A freely accessible web search engine for scholarly literature."
        }
      ]
    }
  ]
}
```

## Scraper

Requires Python 3.11+, Playwright, and httpx:

```bash
pip install playwright httpx
playwright install chromium

python scraper.py [output_path]
```

The scraper clicks the **Export** button on each category page — Softr's native CSV export — rather than parsing rendered HTML. This gets 100% of the tools including all paginated results.

## Largest Categories

| Category | Tools |
|----------|-------|
| AI Image Editors | 189 |
| Tool Lists | 192 |
| Researching Domains | 161 |
| Threat Intelligence | 136 |
| Investigating Phone Numbers | 123 |
| Academic Research Tools | 119 |
| Researching IPs | 131 |
| Company Profiling | 104 |
| Finding Data and Statistics | 108 |
| Cryptocurrency Research | 72 |

## Related

- [osint-handbook](https://github.com/Nicholas-Kloster/osint-handbook) — CLI tool that uses this data to investigate targets (IP, domain, email, username, crypto)
- [osinthandbook.com](https://www.osinthandbook.com) — the source
