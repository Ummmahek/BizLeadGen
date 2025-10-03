import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import tldextract

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
USER_AGENT = os.getenv("USER_AGENT") or "Mozilla/5.0"


def parse_crunchbase_listing(url):
    """
    Best-effort extraction of company name and return page url.
    Crunchbase URLs often have company slug at end; we convert slug to a readable name.
    """
    name = url.rstrip('/').split('/')[-1].replace('-', ' ').title()
    return name, url


def serpapi_search(query, num=10):
    """
    Use SerpAPI (Google) to get organic results. Requires SERPAPI_KEY.
    Returns a list of result URLs.
    """
    if not SERPAPI_KEY:
        return []
    params = {"engine": "google", "q": query, "api_key": SERPAPI_KEY, "num": num}
    resp = requests.get("https://serpapi.com/search.json", params=params, timeout=15)
    data = resp.json()
    results = [r.get("link") for r in data.get("organic_results", []) if r.get("link")]
    return results


def extract_domain(url):
    if not url:
        return ""
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return url


def get_company_leads(keyword, location="", limit=20):
    """
    Returns list of dicts: [{company, website, domain, source}, ...]
    Strategy:
     - Prefer SerpAPI with query "keyword location site:crunchbase.com"
     - Fallback: Bing search scraping (best-effort)
    """
    query = f"{keyword} {location} site:crunchbase.com".strip()
    leads = []
    links = []

    # SerpAPI first
    links = serpapi_search(query, num=limit) if SERPAPI_KEY else []

    if not links:
        # Fallback: Bing search scraping (limited reliability)
        q = requests.utils.requote_uri(query)
        url = f"https://www.bing.com/search?q={q}"
        headers = {"User-Agent": USER_AGENT}
        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.text, "lxml")
            anchors = soup.select('li.b_algo h2 a')
            links = [a.get('href') for a in anchors][:limit]
        except Exception:
            links = []

    for link in links[:limit]:
        try:
            if not link:
                continue
            if "crunchbase.com" in link:
                company, page = parse_crunchbase_listing(link)
                leads.append({"company": company, "website": page, "domain": extract_domain(page), "source": "crunchbase"})
            else:
                domain = extract_domain(link)
                name = domain.split('.')[0].replace('-', ' ').title() if domain else "Unknown"
                leads.append({"company": name, "website": link, "domain": domain, "source": "web"})
        except Exception:
            continue

    # basic dedup by domain
    seen = set()
    out = []
    for l in leads:
        d = l.get('domain')
        if d and d not in seen:
            out.append(l)
            seen.add(d)
    return out[:limit]
