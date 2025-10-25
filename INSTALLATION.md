# 🕷️ Web Scraper Pro - Installation Guide

## For Windows Users (Recommended - No Coding Required!)

### Option 1: Download Pre-built EXE (Easiest)

1. **Go to Releases Page:**
   - Visit: https://github.com/Jayden819432/web-scraper-pro/releases
   
2. **Download the EXE:**
   - Download `WebScraperPro.exe` for the GUI version (recommended)
   - Or download `WebScraperCLI.exe` for command-line version

3. **Install Chrome:**
   - Make sure you have Google Chrome installed
   - Download from: https://www.google.com/chrome/

4. **Run the Program:**
   - Double-click `WebScraperPro.exe`
   - If Windows shows a security warning:
     - Click "More info"
     - Click "Run anyway"
   - The professional interface will open!

5. **Start Scraping:**
   - Enter any website URL (e.g., https://example.com)
   - Click "Start Scraping"
   - Results will be saved in the `scrape_results` folder

### Option 2: Run from Source Code (For Developers)

If you want to modify the code or run from source:

1. **Install Python 3.11:**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"

2. **Download This Repository:**
   - Click the green "Code" button → "Download ZIP"
   - Extract the ZIP file to a folder

3. **Install Requirements:**
   ```bash
   cd web-scraper-pro
   pip install -r requirements.txt
   ```

4. **Run the GUI Version:**
   ```bash
   python scraper_gui.py
   ```

5. **Or Run the CLI Version:**
   ```bash
   python scraper.py https://example.com
   ```

## For Linux/Mac Users

### Prerequisites:
```bash
# Install Python 3.11
sudo apt-get install python3.11  # Ubuntu/Debian
brew install python@3.11         # macOS

# Install Chrome/Chromium
sudo apt-get install chromium-browser  # Ubuntu/Debian
brew install chromium                   # macOS
```

### Installation:
```bash
# Clone repository
git clone https://github.com/Jayden819432/web-scraper-pro.git
cd web-scraper-pro

# Install dependencies
pip install -r requirements.txt

# Run GUI version
python3 scraper_gui.py

# Or run CLI version
python3 scraper.py https://example.com
```

## Features

### GUI Version (WebScraperPro.exe)
- ✨ Professional dark theme interface
- 🖱️ Simple point-and-click operation
- 📊 Real-time progress updates
- 💾 One-click access to results
- 🎯 Headless mode toggle

### CLI Version (WebScraperCLI.exe / scraper.py)
- ⚡ Fast command-line operation
- 🤖 Perfect for automation
- 📝 Scriptable and batch processing
- 🔧 Advanced options

## What Gets Saved

After scraping, you'll find these files in `scrape_results/`:

1. **`[domain]_[timestamp]_apis.txt`**
   - Human-readable list of all discovered API endpoints
   - Includes request methods, status codes, and response previews

2. **`[domain]_[timestamp].json`**
   - Complete structured data
   - All requests, responses, headers, and metadata

3. **`[domain]_[timestamp].html`**
   - Full HTML source code of the scraped page

## Troubleshooting

### Windows Security Warning
- This is normal for downloaded executables
- Click "More info" → "Run anyway"
- Or run from source code instead

### "Chrome not found" Error
- Install Google Chrome from https://www.google.com/chrome/
- Or install Chromium browser

### "Module not found" Error (Source Code)
- Make sure you installed requirements: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.11+)

### Firewall Issues
- Windows Firewall may ask for permission
- Click "Allow access" to let the browser run

## Usage Examples

### GUI Mode
1. Launch `WebScraperPro.exe`
2. Enter URL: `https://jsonplaceholder.typicode.com/`
3. Enable "Headless Mode" for faster scraping
4. Click "Start Scraping"
5. Click "View Results" when complete

### CLI Mode
```bash
# Basic scraping
WebScraperCLI.exe https://example.com

# Headless mode (faster)
WebScraperCLI.exe https://example.com --headless

# From source
python scraper.py https://httpbin.org/ --headless
```

## Support

- **GitHub Issues:** https://github.com/Jayden819432/web-scraper-pro/issues
- **Source Code:** https://github.com/Jayden819432/web-scraper-pro

## Legal Notice

This tool is for educational and research purposes only. Always:
- ✅ Get permission before scraping websites
- ✅ Respect robots.txt files
- ✅ Follow terms of service
- ✅ Be mindful of rate limiting
