import os
import requests
from dotenv import load_dotenv

load_dotenv()
HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

def hunter_domain_search(domain):
    """
    Use Hunter.io Domain Search API to find emails for a domain.
    Replace with Clearbit/Snov if desired.
    """
    if not HUNTER_API_KEY or not domain:
        return []
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json().get('data', {})
            emails = [e.get('value') for e in data.get('emails', []) if e.get('value')]
            return emails
    except Exception:
        return []
    return []

COMMON_PATTERNS = [
    "info@{d}",
    "contact@{d}",
    "hello@{d}",
    "admin@{d}"
]

def guess_emails(domain, company_name=None):
    if not domain:
        return []
    return [p.format(d=domain) for p in COMMON_PATTERNS]

def find_company_emails(domain, company_name=None):
    """
    First try Hunter.io, otherwise return guessed/common emails.
    """
    domain = domain.strip().lower()
    if not domain:
        return []
    emails = hunter_domain_search(domain)
    if emails:
        return emails
    return guess_emails(domain, company_name)
