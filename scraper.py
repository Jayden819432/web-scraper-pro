#!/usr/bin/env python3
import json
import sys
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from datetime import datetime
from urllib.parse import urlparse
import os
import time
import shutil
import subprocess

class WebScraper:
    def __init__(self):
        self.api_endpoints = []
        self.all_requests = []
        self.page_content = {}
        self.gui_log = None
    
    def _find_chromium_binary(self):
        """Dynamically find Chromium/Chrome binary"""
        possible_paths = [
            '/usr/bin/chromium',
            '/usr/bin/chromium-browser',
            '/usr/bin/chrome',
            '/usr/bin/google-chrome',
            '/usr/bin/google-chrome-stable',
        ]
        
        try:
            result = subprocess.run(['which', 'chromium'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        for path in possible_paths:
            if os.path.isfile(path):
                return path
        
        try:
            nix_chromium = subprocess.run(
                ['sh', '-c', 'ls /nix/store/*chromium*/bin/chromium 2>/dev/null | head -1'],
                capture_output=True, text=True, timeout=5
            )
            if nix_chromium.stdout.strip():
                return nix_chromium.stdout.strip()
        except:
            pass
        
        return None
    
    def _find_chromedriver(self):
        """Dynamically find chromedriver"""
        driver_path = shutil.which('chromedriver')
        if driver_path:
            return driver_path
        
        try:
            nix_driver = subprocess.run(
                ['sh', '-c', 'ls /nix/store/*chromedriver*/bin/chromedriver 2>/dev/null | head -1'],
                capture_output=True, text=True, timeout=5
            )
            if nix_driver.stdout.strip():
                return nix_driver.stdout.strip()
        except:
            pass
        
        return None
        
    def scrape(self, url, show_browser=True):
        def log(msg):
            if self.gui_log:
                self.gui_log(msg)
            else:
                print(msg)
        
        log(f"\n{'='*80}")
        log(f"🔍 Starting scrape of: {url}")
        log(f"{'='*80}\n")
        
        chrome_options = Options()
        
        if not show_browser:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        chromium_path = self._find_chromium_binary()
        if chromium_path:
            chrome_options.binary_location = chromium_path
            log(f"📍 Using Chromium at: {chromium_path}")
        else:
            log(f"⚠️  Chromium binary not found, using system default")
        
        driver = None
        try:
            log(f"📡 Starting browser...")
            
            chromedriver_path = self._find_chromedriver()
            if chromedriver_path:
                log(f"📍 Using ChromeDriver at: {chromedriver_path}")
                service = Service(executable_path=chromedriver_path)
                driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                driver = webdriver.Chrome(options=chrome_options)
            
            log(f"📡 Loading page...")
            driver.get(url)
            
            time.sleep(5)
            
            log(f"✅ Page loaded successfully!\n")
            
            self.page_content = {
                'title': driver.title,
                'url': driver.current_url,
                'html': driver.page_source
            }
            
            for request in driver.requests:
                request_data = {
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers),
                    'type': 'request'
                }
                self.all_requests.append(request_data)
                
                if request.response:
                    content_type = request.response.headers.get('Content-Type', '').lower()
                    
                    response_data = {
                        'url': request.url,
                        'method': request.method,
                        'status': request.response.status_code,
                        'content_type': content_type,
                        'headers': dict(request.response.headers),
                        'type': 'response'
                    }
                    
                    if 'application/json' in content_type or '/api/' in request.url or 'graphql' in request.url.lower():
                        try:
                            body = request.response.body.decode('utf-8')
                            response_data['body'] = body
                            self.api_endpoints.append(response_data)
                        except:
                            pass
            
        except Exception as e:
            log(f"⚠️  Error: {e}")
            raise
        finally:
            if driver:
                driver.quit()
        
        self._analyze_results()
        self._save_results(url)
    
    def _analyze_results(self):
        print(f"\n{'='*80}")
        print(f"📊 SCRAPING RESULTS")
        print(f"{'='*80}\n")
        
        print(f"📄 Page Title: {self.page_content.get('title', 'N/A')}")
        print(f"🔗 Final URL: {self.page_content.get('url', 'N/A')}")
        print(f"📦 Total Requests Captured: {len(self.all_requests)}")
        print(f"🎯 API Endpoints Found: {len(self.api_endpoints)}\n")
        
        if self.api_endpoints:
            print(f"{'='*80}")
            print(f"🔥 DISCOVERED API ENDPOINTS:")
            print(f"{'='*80}\n")
            
            for idx, endpoint in enumerate(self.api_endpoints, 1):
                print(f"[{idx}] {endpoint['method']} {endpoint['url']}")
                print(f"    Status: {endpoint['status']}")
                print(f"    Content-Type: {endpoint['content_type']}")
                
                if endpoint.get('body'):
                    try:
                        body_json = json.loads(endpoint['body'])
                        body_preview = json.dumps(body_json, indent=2)[:500]
                        print(f"    Response Preview:\n{body_preview}...")
                    except:
                        body_preview = endpoint['body'][:200]
                        print(f"    Response Preview: {body_preview}...")
                print()
        else:
            print("ℹ️  No API endpoints detected (this website might not use AJAX/API calls)")
        
        unique_domains = set()
        for req in self.all_requests:
            domain = urlparse(req['url']).netloc
            if domain:
                unique_domains.add(domain)
        
        print(f"\n🌐 Unique Domains Contacted: {len(unique_domains)}")
        for domain in sorted(unique_domains)[:10]:
            print(f"   • {domain}")
        if len(unique_domains) > 10:
            print(f"   ... and {len(unique_domains) - 10} more")
    
    def _save_results(self, original_url):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        domain = urlparse(original_url).netloc.replace('.', '_')
        
        os.makedirs('scrape_results', exist_ok=True)
        
        output = {
            'scrape_info': {
                'timestamp': timestamp,
                'target_url': original_url,
                'final_url': self.page_content.get('url'),
                'title': self.page_content.get('title')
            },
            'api_endpoints': self.api_endpoints,
            'all_requests': self.all_requests,
            'page_html': self.page_content.get('html', '')
        }
        
        json_file = f"scrape_results/{domain}_{timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        html_file = f"scrape_results/{domain}_{timestamp}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(self.page_content.get('html', ''))
        
        api_file = f"scrape_results/{domain}_{timestamp}_apis.txt"
        with open(api_file, 'w', encoding='utf-8') as f:
            f.write(f"API Endpoints Discovered from: {original_url}\n")
            f.write(f"Scraped at: {timestamp}\n")
            f.write(f"{'='*80}\n\n")
            
            for idx, endpoint in enumerate(self.api_endpoints, 1):
                f.write(f"[{idx}] {endpoint['method']} {endpoint['url']}\n")
                f.write(f"    Status: {endpoint['status']}\n")
                f.write(f"    Content-Type: {endpoint['content_type']}\n")
                if endpoint.get('body'):
                    f.write(f"    Response:\n{endpoint['body'][:1000]}\n")
                f.write("\n" + "-"*80 + "\n\n")
        
        print(f"\n{'='*80}")
        print(f"💾 RESULTS SAVED:")
        print(f"{'='*80}")
        print(f"📁 Complete Data: {json_file}")
        print(f"📄 HTML Content: {html_file}")
        print(f"🎯 API List: {api_file}")
        print(f"{'='*80}\n")


def main():
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                   🕷️  WEB SCRAPER & API DISCOVERY TOOL 🕷️                  ║
║                                                                            ║
║  This tool will:                                                           ║
║  • Open any website in a real browser                                      ║
║  • Capture ALL network traffic and API calls                              ║
║  • Extract page content and data                                          ║
║  • Save everything in organized files                                     ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        headless = '--headless' in sys.argv
    else:
        url = input("🌐 Enter the URL to scrape (e.g., https://example.com): ").strip()
        
        show_browser_input = input("👀 Show browser while scraping? (y/n, default=y): ").strip().lower()
        headless = show_browser_input == 'n'
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    scraper = WebScraper()
    scraper.scrape(url, show_browser=not headless)
    
    print("\n✨ Scraping complete! Check the 'scrape_results' folder for all saved files.\n")


if __name__ == "__main__":
    main()
