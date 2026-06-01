# Honeysites
## TLS Fingerprinting Data Collector

This repository contains the core architecture for collecting browser and TLS fingerprints for the purpose of LLM bot detection research.


### Overview

The project is composed of:

- A **main Nginx server** (`example.org`) acting as a reverse proxy and entry point.

- **9 Nginx subdomain servers** (`site[x].example.org`) each configured with a different bot mitigation technique. These subdomains simulate various levels of website protection to test how different bots react to them.

- **A Matomo analytics server** (`analytics.example.org`) used to track and analyze client-side behavior.

- **An Express.js API** (`api.example.org`) responsible for:
    - Computing and storing browser fingerprints.
    - Serving blog post content dynamically across the different subdomain websites.

### Subdomain Descriptions

Each subdomain implements a specific bot defense mechanism:

1. [site1](./nginx1/): Implements a robots.txt file to disallow known crawler paths.

2. [site2](./nginx2/): Uses Nginx rules to block requests based on common bot User-Agent headers.

3. [site3](./nginx3/): Integrates Google reCAPTCHA v3.

4. [site4](./nginx4/): Uses Prospo CAPTCHA.

5. [site5](./nginx5/): Integrates Anubis, a bot detection and mitigation tool.

6. [site6](./nginx6/): Uses Cloudflare Turnstile CAPTCHA.

7. [site7](./nginx7/): Relies on Cloudflare’s anti-bot protection mechanisms.

8. [site8](./nginx8/): Combines robots.txt, Anubis, User-Agent blocking, and Prospo CAPTCHA.

9. [site9](./nginx9/): Combines robots.txt, User-Agent blocking, Turnstile CAPTCHA and Cloudflare’s anti-bot protection mechanisms.
