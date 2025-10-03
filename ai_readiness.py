import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()
USER_AGENT = os.getenv("USER_AGENT") or "Mozilla/5.0"

# Keyword buckets with heuristic points
AI_KEYWORDS = [
    ("artificial intelligence", 20),
    ("machine learning", 20),
    ("data science", 15),
    ("automation", 10),
    ("predictive analytics", 15),
    ("deep learning", 20),
]
TECH_KEYWORDS = [
    ("api", 5),
    ("cloud", 5),
    ("saas", 5),
    ("platform", 5)
]
JOB_KEYWORDS = ["data scientist", "machine learning engineer", "ml engineer", "data engineer"]

def fetch_text_from_homepage(domain):
    """
    Try https then http; return cleaned lowercase text if successful.
    """
    if not domain:
        return ""
    urls = [f"https://{domain}", f"http://{domain}"]
    headers = {"User-Agent": USER_AGENT}
    text = ""
    for u in urls:
        try:
            r = requests.get(u, timeout=8, headers=headers)
            if r.status_code == 200 and 'text/html' in r.headers.get('Content-Type', ''):
                soup = BeautifulSoup(r.text, 'lxml')
                text = soup.get_text(separator=' ', strip=True).lower()
                break
        except Exception:
            continue
    return text

def ai_readiness_score(domain):
    """
    Simple heuristic scoring (0-100).
    """
    text = fetch_text_from_homepage(domain)
    if not text:
        return 0

    score = 0
    # AI keywords
    for kw, pts in AI_KEYWORDS:
        if kw in text:
            score += pts

    # tech keywords
    for kw, pts in TECH_KEYWORDS:
        if kw in text:
            score += pts

    # job page heuristics
    if 'careers' in text or 'join us' in text or 'jobs' in text:
        for j in JOB_KEYWORDS:
            if j in text:
                score += 10

    # clamp
    if score > 100:
        score = 100
    return score
