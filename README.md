# Project SpearPhish 🛡️🎣
### A Multi-Stage Phishing Detection Funnel

**Status:** Research Prototype (Completed Dec 2025)  
**Paper:** [View Final Report](docs/Group9_AI4E_FinalPaper.pdf)

## 💡 Overview
SpearPhish is a 3-layer cybersecurity detection system designed to identify sophisticated phishing attacks that bypass traditional filters. It uses a "funnel" approach:
1.  **Layer 1 (NLP):** Analyzes email text for urgency and semantic triggers (Logistic Regression).
2.  **Layer 2 (Redirects):** Follows URL redirect chains to detect obfuscation.
3.  **Layer 3 (Structural):** Scans the final landing page HTML for phishing signatures (XGBoost).

## 🚀 Key Results
* **NLP Layer:** 96% F1-Score on text classification.
* **Structural Layer:** 80% Accuracy on live-scraped URLs.
* **Engineering Pivot:** Solved critical "Link Rot" in historical datasets by building a custom scraper to harvest 2,000+ live URLs from OpenPhish/Tranco.

## 📂 Repository Structure
* `notebooks/`: Contains the Jupyter notebooks used for data exploration, scraping, and model training.
    * *Note: These are research artifacts containing the raw experimental code.*
* `docs/`: The final IEEE-formatted research paper and presentation slides.

## 🛠️ Tech Stack
* **ML/AI:** Python, Scikit-Learn, XGBoost, Pandas, BeautifulSoup
* **Web/App:** FastAPI, Next.js (Prototype)

## 👥 Team
* **Robert Maina** https://www.linkedin.com/in/robert-kirathe/
* **Djibrilla Boubacar** https://www.linkedin.com/in/djibrilla/
* **Rhoda Ojetola** https://www.linkedin.com/in/rhoda-ojetola/
* **Samuel Chukwuma** https://www.linkedin.com/in/samuel-chukwuma-b85ba0285/
---
*This project was completed as the final capstone for the AI for Engineers course at CMU Africa.*
