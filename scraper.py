"""
Click Export on every osinthandbook.com category page, save CSVs, merge to JSON.
Usage: python export_scraper.py [--output knowledge/osinthandbook_web.json]
"""
import csv, io, json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
import httpx, xml.etree.ElementTree as ET

BASE = "https://www.osinthandbook.com"
SITEMAP = f"{BASE}/sitemap.xml"

SKIP = {"", "/", "/add-resource", "/sitemap.xml", "/about", "/terms", "/contact",
        "/404", "/volunteer-work"}


def fetch_category_urls() -> list[str]:
    resp = httpx.get(SITEMAP, timeout=15, follow_redirects=True)
    root = ET.fromstring(resp.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [loc.text.strip() for loc in root.findall(".//sm:loc", ns) if loc.text]
    skip_terms = ["/blog", "/tag/", "/author/", "/page/"]
    return [
        u for u in urls
        if u.startswith(BASE)
        and u[len(BASE):] not in SKIP
        and not any(s in u for s in skip_terms)
    ]


def export_page(page, url: str) -> list[dict] | None:
    """Navigate to url, click Export, capture CSV download, return tool list."""
    try:
        with page.expect_download(timeout=20000) as dl_info:
            page.goto(url, wait_until="networkidle", timeout=25000)
            time.sleep(0.5)
            # Click Export button
            export_btn = page.locator('button:has-text("Export"), [role="button"]:has-text("Export")').first
            export_btn.click(timeout=8000)

        download = dl_info.value
        content = download.path()
        if not content:
            return None

        text = Path(content).read_text(encoding="utf-8", errors="replace")
        reader = csv.DictReader(io.StringIO(text))
        tools = []
        for row in reader:
            name = (row.get("Tool Name") or row.get("Name") or "").strip()
            url_val = (row.get("Urls") or row.get("URL") or row.get("Link") or "").strip()
            desc = (row.get("Description") or "").strip()
            if name and url_val:
                tools.append({"name": name, "url": url_val, "description": desc})
        return tools

    except Exception as e:
        return None


def run(output_path: str = "knowledge/osinthandbook_web.json") -> None:
    print("Fetching sitemap...", flush=True)
    urls = fetch_category_urls()
    print(f"{len(urls)} category pages to export", flush=True)

    results: dict[str, list[dict]] = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(accept_downloads=True)
        ctx.set_extra_http_headers({"User-Agent": "Mozilla/5.0"})
        page = ctx.new_page()

        for i, url in enumerate(urls):
            slug = url.replace(BASE + "/", "").strip("/")
            tools = export_page(page, url)
            if tools:
                results[slug] = tools
                print(f"  [{i+1}/{len(urls)}] {slug}: {len(tools)} tools", flush=True)
            else:
                print(f"  [{i+1}/{len(urls)}] {slug}: 0 (no export or empty)", flush=True)

        ctx.close()
        browser.close()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    categories = [
        {
            "slug": slug,
            "name": slug.replace("-", " ").title(),
            "tools": tools,
        }
        for slug, tools in sorted(results.items())
    ]

    total = sum(len(c["tools"]) for c in categories)
    data = {
        "source": "osinthandbook.com",
        "year": 2026,
        "total_categories": len(categories),
        "total_tools": total,
        "categories": categories,
    }

    out.write_text(json.dumps(data, indent=2))
    print(f"\nDone: {len(categories)} categories, {total} tools → {out}")


if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "knowledge/osinthandbook_web.json"
    run(output)
