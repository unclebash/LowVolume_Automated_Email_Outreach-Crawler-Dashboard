# Low-Volume Automated Email Outreach, Crawler, & Dashboard

A lightweight, automated B2B pipeline designed to crawl target websites for contact information, sync outreach leads directly to a Google Sheets document, and batch-dispatch beautiful HTML brand templates via the Gmail API.

## Features

1. **Lead Crawler (`crawler.py` & `batch_crawl.py`)**: Automates scraping public domains and business listings to gather emails and contact names.
2. **Google Sheets Sync (`sheets_client.py`)**: Automatically syncs discovered leads to a remote Google Sheet document.
3. **Gmail Dispatcher (`main.py`)**: Authenticates via OAuth2 and sends custom HTML brand messages to the contacts listed in your CSV.
4. **Terminal Dashboard (`dashboard.py`)**: Inspects template integrity, counts prospects, and shows the pipeline's active metrics.

---

## Getting Started

### 1. Prerequisites
Install required Google client and parsing packages:
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib beautifulsoup4 requests
```

### 2. Configure Google Cloud Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable the **Gmail API** and **Google Sheets API**.
3. Create OAuth Client ID credentials (type: Desktop App), download the client secrets JSON file, and rename it to `credentials.json` in this directory.

### 3. Run the Pipeline
1. Run the crawler to gather prospects:
   ```bash
   python batch_crawl.py
   ```
2. Check your lead count and load status:
   ```bash
   python dashboard.py
   ```
3. Run the email outreach dispatcher:
   ```bash
   python main.py
   ```
   *Note: On your first run, a browser window will open requesting you to sign in to the Google account from which you wish to send emails.*
