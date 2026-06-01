# On the Internet, Nobody Knows You're an LLM Bot: Artifacts

This repository accompanies the paper:

***“On the Internet, Nobody Knows You're an LLM Bot: Unmasking Web Agents with Multi-Layer Fingerprinting.”***

Its purpose is to facilitate the reproduction of the experiments and results presented in the paper.

## Contents

This repository includes:

* Automation scripts used for **Selenium**, **Puppeteer**, **Playwright**, **Crawl4AI**, **Crawl4AI-Stealth**, **BrowserUse**, and **BrowserUse-Stealth**;
* Details of the collected **JA4 fingerprints**;
* The core architecture of our **honeysites** (anonymized and excluding credentials) as well as the **tshark** script for collecting network traffic;
* The final **active** and **passive** datasets, from which IP addresses and other identifying information have been removed for privacy reasons;
* Six analysis notebooks used to reproduce the results presented in **Sections 5–7** and **Appendix** of the paper;
* The code and data used to generate **Figure 2** and **Tables 3, 4, 5, 6, 9, 10, and 11**.

## Repository Structure

```text
Analysis/
├── active_tests_with_TLS_IP_layers.csv
├── active_tests_browser_layers.csv
├── active_tests_with_TLS_IP_layers.csv
├── df_attributes_scores.csv
├── df_values_scores.csv
├── antibots_mechanisms.ipynb
├── ip_layer.ipynb
├── tls_layer.ipynb
├── browser_fingerprinting_layer.ipynb
├── bots_classification.ipynb
└── README.md

Honeysites/
├── api/
├── db/
├── main/
├── nginx1/
├── ...
├── nginx9/
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── favicon.ico
├── logrotate
├── nginx.conf
├── tshark_script.sh
└── README.md

JA4/
├── JA4_details.txt
└── README.md

PassiveTraffic/
├── passive_data.csv
├── passive_traffic.ipynb
└── README.md

Scripts/
├── BrowserUse/
|    └── browseruse_script.py
├── Crawl4AI/
|    ├── normal_stealth_script.py
|    └── undetected_browser_script.py
├── Playwright/
|    └── bot.py
├── Puppeteer/
|    └── bot.js
├── Selenium/
|    └── bot.py
└── README.md
```
