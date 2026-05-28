"""Run by parallel agents: scrape a batch of osinthandbook.com pages."""
import json, sys, time
from playwright.sync_api import sync_playwright

EXTRACT = """() => {
    const tools = [];
    const headings = document.querySelectorAll('h3, h4, h5');
    for (const h of headings) {
        const name = h.textContent.trim();
        if (!name || name.length > 100) continue;
        const card = h.parentElement?.parentElement;
        if (!card) continue;
        const link = card.querySelector('a[href^="http"]:not([href*="osinthandbook.com"])');
        if (link) tools.push({ name, url: link.href });
    }
    return tools;
}"""

def scrape_batch(urls: list[str]) -> dict:
    results = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_extra_http_headers({"User-Agent": "Mozilla/5.0"})
        for url in urls:
            slug = url.split("osinthandbook.com/")[-1].strip("/")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(0.4)
                tools = page.evaluate(EXTRACT)
                if tools:
                    results[slug] = tools
                    print(f"  {slug}: {len(tools)} tools", flush=True)
                else:
                    print(f"  {slug}: 0 tools", flush=True)
            except Exception as e:
                print(f"  {slug}: ERROR {e}", flush=True)
        browser.close()
    return results

if __name__ == "__main__":
    urls = json.loads(sys.argv[1])
    out_file = sys.argv[2]
    results = scrape_batch(urls)
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved {len(results)} pages to {out_file}")
