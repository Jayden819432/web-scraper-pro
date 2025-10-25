# 🕷️ Web Scraper Pro - API Discovery Tool

[![Build Status](https://github.com/Jayden819432/web-scraper-pro/workflows/Build%20Windows%20EXE/badge.svg)](https://github.com/Jayden819432/web-scraper-pro/actions)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)](https://github.com/Jayden819432/web-scraper-pro/releases)
[![Python](https://img.shields.io/badge/Python-3.11-green)](https://www.python.org/)

**Professional Web Scraper & API Discovery Tool** - Automatically discover hidden APIs from any website! Available as a Windows .exe with beautiful GUI or command-line tool.

## ✨ Features

### 🎨 Professional GUI (Windows .exe)
- **Beautiful Dark Theme Interface** - Modern, professional design
- **One-Click Operation** - No coding required!
- **Real-time Progress** - See what's happening as it scrapes
- **Instant Results Access** - View results folder with one click

### 🔍 Powerful Scraping Engine
- **🌐 Scrape Any Website** - Enter any URL and go
- **🎯 API Discovery** - Automatically find hidden API endpoints
- **📡 Network Traffic Monitoring** - Capture ALL HTTP/HTTPS requests
- **💾 Multiple Export Formats** - JSON, HTML, and TXT files
- **⚡ Headless Mode** - Fast background scraping
- **🔒 Safe & Secure** - No data sent anywhere, all local processing

### 💻 Windows 10/11 Support
- **Pre-built .exe files** - No Python installation needed!
- **Automatic builds** - GitHub Actions creates fresh .exe on every update
- **Portable** - Run from anywhere, no installation required

## How It Works

The tool uses Selenium with network interception capabilities to:
1. Open the target website in a real Chromium browser
2. Monitor all network traffic (images, scripts, API calls, etc.)
3. Identify and extract API endpoints (looking for JSON responses)
4. Save all the captured data in organized formats

## 🚀 Quick Start (Windows Users)

### Download the .exe (No Installation!)

1. **Go to [Releases](https://github.com/Jayden819432/web-scraper-pro/releases)**
2. **Download `WebScraperPro.exe`** (GUI version - recommended!)
3. **Double-click to run** - That's it!

> **Note:** Windows may show a security warning. Click "More info" → "Run anyway"

### Using the GUI

1. **Enter a URL** (e.g., `https://httpbin.org/`)
2. **Choose headless mode** (optional, for faster scraping)
3. **Click "Start Scraping"**
4. **View results** in the `scrape_results` folder!

### Using the Command Line

Download `WebScraperCLI.exe` instead:

```bash
WebScraperCLI.exe https://example.com
WebScraperCLI.exe https://example.com --headless
```

## 🐍 For Developers (Python)

### From Source Code:

```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI version
python scraper_gui.py

# Run CLI version
python scraper.py https://example.com

# Run interactive menu
python run.py
```

## Output Files

After scraping, you'll find these files in the `scrape_results` folder:

1. **`[domain]_[timestamp]_apis.txt`** - List of all discovered API endpoints with responses
2. **`[domain]_[timestamp].json`** - Complete data: all requests, responses, and metadata
3. **`[domain]_[timestamp].html`** - The full HTML content of the page

## What Gets Captured

- ✅ All HTTP/HTTPS requests
- ✅ API endpoints (especially JSON responses)
- ✅ Request/response headers
- ✅ Response bodies for APIs
- ✅ Page HTML content
- ✅ All domains contacted by the website

## Example Use Cases

- Discover hidden APIs used by websites
- Analyze what data a website requests
- Reverse-engineer web applications
- Research web traffic patterns
- Find API documentation
- Monitor website behavior

## Important Notes

- Only scrape websites you have permission to access
- Respect robots.txt and terms of service
- Be mindful of rate limiting
- This tool is for educational and research purposes

## Technical Details

- **Language**: Python 3.11
- **Browser**: Chromium (automated via Selenium)
- **Network Capture**: Selenium-Wire for traffic interception
- **Dependencies**: selenium, selenium-wire, webdriver-manager
