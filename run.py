#!/usr/bin/env python3
import os
import subprocess
import sys

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def show_menu():
    clear_screen()
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                   🕷️  WEB SCRAPER & API DISCOVERY TOOL 🕷️                  ║
╚════════════════════════════════════════════════════════════════════════════╝

This powerful tool helps you:
  ✅ Scrape any website automatically
  ✅ Discover hidden API endpoints
  ✅ Capture all network traffic
  ✅ Save data in organized formats

╔════════════════════════════════════════════════════════════════════════════╗
║                              MAIN MENU                                     ║
╚════════════════════════════════════════════════════════════════════════════╝

  [1] 🌐 Scrape a Website (with browser visible)
  [2] 🔍 Scrape a Website (headless mode - faster)
  [3] 📁 View Previous Results
  [4] ℹ️  Help & Examples
  [5] 🚪 Exit

""")

def scrape_with_browser():
    clear_screen()
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                     🌐 SCRAPE WITH VISIBLE BROWSER                         ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    url = input("Enter the URL to scrape (e.g., https://example.com): ").strip()
    
    if not url:
        print("\n❌ No URL provided!")
        input("\nPress Enter to continue...")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n🚀 Starting scrape of: {url}")
    print("📺 Browser window will open - please wait...\n")
    
    subprocess.run([sys.executable, "scraper.py", url])
    
    input("\n\n✅ Press Enter to return to menu...")

def scrape_headless():
    clear_screen()
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                       🔍 SCRAPE IN HEADLESS MODE                           ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    url = input("Enter the URL to scrape (e.g., https://example.com): ").strip()
    
    if not url:
        print("\n❌ No URL provided!")
        input("\nPress Enter to continue...")
        return
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"\n🚀 Starting headless scrape of: {url}")
    print("⚡ Running in background (faster)...\n")
    
    subprocess.run([sys.executable, "scraper.py", url, "--headless"])
    
    input("\n\n✅ Press Enter to return to menu...")

def view_results():
    clear_screen()
    print("╔════════════════════════════════════════════════════════════════════════════╗")
    print("║                          📁 PREVIOUS RESULTS                               ║")
    print("╚════════════════════════════════════════════════════════════════════════════╝\n")
    
    if not os.path.exists('scrape_results'):
        print("❌ No results folder found yet. Run a scrape first!\n")
        input("Press Enter to continue...")
        return
    
    files = os.listdir('scrape_results')
    
    if not files:
        print("📭 No scraping results saved yet.\n")
        input("Press Enter to continue...")
        return
    
    api_files = [f for f in files if f.endswith('_apis.txt')]
    json_files = [f for f in files if f.endswith('.json')]
    
    print(f"📊 Total files saved: {len(files)}\n")
    print(f"   • API endpoint files: {len(api_files)}")
    print(f"   • Complete data files: {len(json_files)}")
    print(f"   • HTML files: {len([f for f in files if f.endswith('.html')])}\n")
    
    if api_files:
        print("Latest API discoveries:\n")
        for f in sorted(api_files, reverse=True)[:5]:
            print(f"   📄 {f}")
    
    print(f"\n💡 All files are in the 'scrape_results' folder")
    
    input("\n\nPress Enter to continue...")

def show_help():
    clear_screen()
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                            ℹ️  HELP & EXAMPLES                              ║
╚════════════════════════════════════════════════════════════════════════════╝

🎯 WHAT THIS TOOL DOES:

This tool automates the process of analyzing websites by:
  • Opening the website in a real browser (Chromium)
  • Recording ALL network traffic (images, scripts, API calls, etc.)
  • Identifying API endpoints automatically
  • Extracting page content and HTML
  • Saving everything in organized files

🔍 WHAT YOU GET:

After scraping, you'll find these files in the 'scrape_results' folder:

  1. [domain]_[timestamp]_apis.txt
     → List of all discovered API endpoints with responses

  2. [domain]_[timestamp].json
     → Complete data: all requests, responses, and metadata

  3. [domain]_[timestamp].html
     → The full HTML content of the page

📝 EXAMPLE URLS TO TRY:

  • https://jsonplaceholder.typicode.com/
  • https://reqres.in/
  • Any e-commerce site to see their API calls
  • News websites to discover their content APIs

💡 TIPS:

  • Use "visible browser" mode to see what's happening
  • Use "headless mode" for faster scraping
  • The tool captures AJAX calls, fetch requests, and GraphQL
  • Look for 'application/json' responses to find APIs

⚠️  IMPORTANT:

  • Only scrape websites you have permission to access
  • Respect robots.txt and terms of service
  • Be mindful of rate limiting

""")
    input("Press Enter to return to menu...")

def main():
    while True:
        show_menu()
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            scrape_with_browser()
        elif choice == '2':
            scrape_headless()
        elif choice == '3':
            view_results()
        elif choice == '4':
            show_help()
        elif choice == '5':
            clear_screen()
            print("\n👋 Thanks for using Web Scraper & API Discovery Tool!\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid option. Please choose 1-5.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        print("\n\n👋 Goodbye!\n")
        sys.exit(0)
