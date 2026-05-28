# OSINT Tools and Resources Handbook 2026

A machine-readable dataset of OSINT tools scraped from [osinthandbook.com](https://www.osinthandbook.com) — the live, updated successor to the i-intelligence OSINT Handbook.

The original 2020 PDF is intentionally difficult to extract programmatically. This repo fixes that.

## Data

| File | Description |
|------|-------------|
| `data/tools.json` | All tools by category — JSON, structured |
| `data/tools.csv` | Flat CSV: `category, tool_name, url` |
| `data/handbook_2020_categories.json` | Category index from the 2020 PDF (45 categories, 7,442 tools) |

### tools.json structure

```json
{
  "source": "osinthandbook.com",
  "year": 2026,
  "total_categories": 49,
  "total_tools": 732,
  "categories": [
    {
      "slug": "academic-research-tools",
      "name": "Academic Research Tools",
      "tools": [
        { "name": "Google Scholar", "url": "https://scholar.google.com/" }
      ]
    }
  ]
}
```

## Coverage

49 categories scraped from osinthandbook.com. The site paginates — each category shows up to 20 tools in the initial render. Run the scraper to pull updated data.

## Scraper

Requires Python 3.11+ and Playwright:

```bash
pip install playwright httpx
playwright install chromium

# Scrape a batch of category URLs
python scraper.py '["https://www.osinthandbook.com/academic-research-tools"]' output.json
```

The scraper uses headless Chromium to render the JS-heavy site and extracts tool name + URL pairs from each category page.

## Categories

Academic Research Tools · Add-On Security · Android Emulators · Anti-Malware · Books And Reading · Browser Tests · Business Registers · Checking Cyber Reputation · Chrome Extensions · Collation And Tabular Analysis · Company Profiling · Cryptocurrency Research · Dark Web Research · Data Scrapers · Document And Reference Management · Document Checking · Document Search · Downloading Videos · Exploit Search Engines · Fact Checking · File And Ftp Search · Font Identification · Forums And Discussion Boards · Glossaries And Dictionaries · Image Analysis · Investigating Phone Numbers · Live Streaming And Webcams · Mastodon · Media Monitoring · Names And Naming Conventions · News Directories · Notetaking · Osint Books · Osint Challenges And Ctfs · Osint Podcasts · Pdf Management · Public Records · Researching Airplanes · Researching Automotive Vehicles · Researching Domains · Researching Ips · Researching Railways · Rss Mixing · Satellite Imagery · Searching Pastebins · Slideshow And Presentation Tools · Social Media Monitoring · Twitter X · Unit Conversion · Validating E-Mails · Video Editors And Converters · Virtual Machines · Vpn Services · Web History And Site Capture · Wikipedia · Working With Citations · Working With Hashes · Working With Hashtags

## Related

- [osint-handbook](https://github.com/Nicholas-Kloster/osint-handbook) — CLI tool that uses this data to investigate targets (IP, domain, email, username, crypto)
- [osinthandbook.com](https://www.osinthandbook.com) — the source
