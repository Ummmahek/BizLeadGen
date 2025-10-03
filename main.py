"""
Main entry for BizLeadGen
Usage:
    python main.py

This will prompt for keyword and location, run scraping, enrichment and save leads.csv
"""
import os
import time
import pandas as pd
from dotenv import load_dotenv
from lead_scraper import get_company_leads
from email_finder import find_company_emails
from ai_readiness import ai_readiness_score
from utils import normalize_domain

load_dotenv()

OUTPUT_CSV = "leads.csv"


def main():
    print("=== BizLeadGen — Caprae submission demo ===")
    keyword = input("Enter target keyword/industry (e.g. 'AI healthcare startups'): ").strip()
    location = input("Enter location (e.g. 'USA' or leave blank): ").strip()

    print('\n[INFO] Scraping leads (this may take 10-60s depending on APIs)...')
    raw_leads = get_company_leads(keyword, location, limit=50)
    print(f"[INFO] {len(raw_leads)} raw leads collected")

    enriched = []
    for i, lead in enumerate(raw_leads, start=1):
        domain = normalize_domain(lead.get("website") or lead.get("domain") or "")
        print(f"[{i}/{len(raw_leads)}] {lead.get('company')} ({domain})")
        emails = find_company_emails(domain, lead.get("company")) if domain else []
        score = ai_readiness_score(domain) if domain else 0

        enriched.append({
            "Company": lead.get("company"),
            "Website": domain or lead.get("website") or lead.get("domain"),
            "Industry": keyword,
            "Email": emails[0] if emails else "Not found",
            "Source": lead.get("source", "search"),
            "AI-Readiness Score": score
        })
        # small rate-limit-friendly pause
        time.sleep(0.7)

    df = pd.DataFrame(enriched)
    df.drop_duplicates(subset=["Website"], inplace=True)
    df.sort_values(by="AI-Readiness Score", ascending=False, inplace=True)
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"\n[SUCCESS] {len(df)} leads written to {OUTPUT_CSV}")
    print("Tip: open the CSV, pick top-scoring leads for outreach or further enrichment.")


if __name__ == '__main__':
    main()
