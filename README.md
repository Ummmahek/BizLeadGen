# BizLeadGen  
**AI-Ready Lead Generation Tool for Caprae Capital Internship Submission**

BizLeadGen is a business-focused lead generation tool built for Caprae Capital’s AI-Readiness Pre-Screening Challenge.  
Unlike a generic scraper, this tool not only finds companies and contacts but also assigns an **AI-Readiness Score** — helping identify businesses that are most transformable with AI.  

---

## ✨ Features
- 🔍 Scrapes company leads (via Crunchbase/Google using SerpAPI or fallback Bing scraping)  
- 📧 Enriches with corporate emails (via Hunter.io API or smart guesses if no key)  
- 🤖 Computes **AI-Readiness Score (0–100)** from company websites using keyword + job signal heuristics  
- 🧹 Deduplicates & ranks companies by score  
- 📊 Exports results into `leads.csv` for easy review  

---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR_USERNAME/BizLeadGen.git
   cd BizLeadGen
