#!/usr/bin/env python3
"""
Professional GUI for Web Scraper & API Discovery Tool
Built with tkinter for Windows compatibility
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
import json
from datetime import datetime
from queue import Queue
from scraper import WebScraper

class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper & API Discovery Tool - Professional Edition")
        self.root.geometry("900x700")
        self.root.configure(bg='#1e1e1e')
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Dark.TFrame', background='#1e1e1e')
        self.style.configure('Dark.TLabel', background='#1e1e1e', foreground='#ffffff', font=('Segoe UI', 10))
        self.style.configure('Title.TLabel', background='#1e1e1e', foreground='#00d4ff', font=('Segoe UI', 18, 'bold'))
        self.style.configure('Dark.TButton', background='#0078d4', foreground='#ffffff', font=('Segoe UI', 10, 'bold'), borderwidth=0)
        self.style.map('Dark.TButton', background=[('active', '#005a9e')])
        
        self.is_scraping = False
        self.message_queue = Queue()
        self.create_widgets()
        self.process_queue()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
        title = ttk.Label(main_frame, text="🕷️ Web Scraper & API Discovery", style='Title.TLabel')
        title.grid(row=0, column=0, pady=(0, 10))
        
        subtitle = ttk.Label(main_frame, text="Professional Edition - Discover Hidden APIs Instantly", style='Dark.TLabel')
        subtitle.grid(row=1, column=0, pady=(0, 20))
        
        input_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        input_frame.columnconfigure(1, weight=1)
        
        url_label = ttk.Label(input_frame, text="Target URL:", style='Dark.TLabel')
        url_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.url_entry = tk.Entry(input_frame, font=('Segoe UI', 11), bg='#2d2d2d', fg='#ffffff', 
                                   insertbackground='#ffffff', relief=tk.FLAT, borderwidth=2)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), ipady=5)
        self.url_entry.insert(0, "https://")
        
        options_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        options_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.headless_var = tk.BooleanVar(value=True)
        headless_check = tk.Checkbutton(options_frame, text="Headless Mode (Faster)", 
                                        variable=self.headless_var, bg='#1e1e1e', fg='#ffffff',
                                        selectcolor='#2d2d2d', font=('Segoe UI', 10),
                                        activebackground='#1e1e1e', activeforeground='#00d4ff')
        headless_check.grid(row=0, column=0, sticky=tk.W)
        
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.grid(row=4, column=0, pady=15)
        
        self.scrape_btn = tk.Button(button_frame, text="🚀 Start Scraping", command=self.start_scrape,
                                     bg='#0078d4', fg='#ffffff', font=('Segoe UI', 12, 'bold'),
                                     relief=tk.FLAT, padx=30, pady=10, cursor='hand2',
                                     activebackground='#005a9e', activeforeground='#ffffff')
        self.scrape_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="⏹ Stop", command=self.stop_scrape,
                                   bg='#d13438', fg='#ffffff', font=('Segoe UI', 12, 'bold'),
                                   relief=tk.FLAT, padx=30, pady=10, cursor='hand2',
                                   activebackground='#a82327', activeforeground='#ffffff',
                                   state=tk.DISABLED)
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        results_btn = tk.Button(button_frame, text="📁 View Results", command=self.open_results_folder,
                                bg='#107c10', fg='#ffffff', font=('Segoe UI', 12, 'bold'),
                                relief=tk.FLAT, padx=30, pady=10, cursor='hand2',
                                activebackground='#0e5c0e', activeforeground='#ffffff')
        results_btn.grid(row=0, column=2, padx=5)
        
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=15)
        
        status_label = ttk.Label(main_frame, text="Status & Results:", style='Dark.TLabel', font=('Segoe UI', 11, 'bold'))
        status_label.grid(row=6, column=0, sticky=tk.W, pady=(0, 5))
        
        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, height=20,
                                                      bg='#0d1117', fg='#00ff00',
                                                      font=('Consolas', 9), relief=tk.FLAT,
                                                      insertbackground='#00ff00')
        self.output_text.grid(row=7, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(7, weight=1)
        
        self.status_bar = ttk.Label(main_frame, text="Ready to scrape", style='Dark.TLabel',
                                     font=('Segoe UI', 9), relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=8, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.log("✨ Web Scraper & API Discovery Tool - Professional Edition")
        self.log("📋 Enter a URL and click 'Start Scraping' to begin\n")
        
    def process_queue(self):
        """Process messages from the worker thread safely on the main thread"""
        from queue import Empty
        try:
            while True:
                msg = self.message_queue.get_nowait()
                msg_type = msg.get('type')
                
                if msg_type == 'log':
                    self.output_text.insert(tk.END, msg['message'] + "\n")
                    self.output_text.see(tk.END)
                elif msg_type == 'status':
                    self.status_bar.config(text=msg['message'])
                elif msg_type == 'done':
                    self.scrape_btn.config(state=tk.NORMAL)
                    self.stop_btn.config(state=tk.DISABLED)
                    self.is_scraping = False
                elif msg_type == 'info_dialog':
                    messagebox.showinfo(msg['title'], msg['message'])
                elif msg_type == 'error_dialog':
                    messagebox.showerror(msg['title'], msg['message'])
        except Empty:
            pass
        
        self.root.after(100, self.process_queue)
    
    def log(self, message):
        """Thread-safe logging"""
        self.message_queue.put({'type': 'log', 'message': message})
        
    def update_status(self, message):
        """Thread-safe status update"""
        self.message_queue.put({'type': 'status', 'message': message})
        
    def start_scrape(self):
        url = self.url_entry.get().strip()
        
        if not url or url == "https://":
            messagebox.showwarning("Invalid URL", "Please enter a valid URL to scrape.")
            return
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)
        
        self.is_scraping = True
        self.scrape_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        
        self.log(f"{'='*80}")
        self.log(f"🔍 Starting scrape of: {url}")
        self.log(f"{'='*80}\n")
        self.update_status("Scraping in progress...")
        
        thread = threading.Thread(target=self.scrape_thread, args=(url,))
        thread.daemon = True
        thread.start()
        
    def scrape_thread(self, url):
        try:
            scraper = WebScraper()
            scraper.gui_log = self.log
            
            headless = self.headless_var.get()
            scraper.scrape(url, show_browser=not headless)
            
            self.log(f"\n{'='*80}")
            self.log(f"📊 SCRAPING COMPLETED")
            self.log(f"{'='*80}\n")
            self.log(f"📄 Page Title: {scraper.page_content.get('title', 'N/A')}")
            self.log(f"🔗 Final URL: {scraper.page_content.get('url', 'N/A')}")
            self.log(f"📦 Total Requests: {len(scraper.all_requests)}")
            self.log(f"🎯 API Endpoints Found: {len(scraper.api_endpoints)}\n")
            
            if scraper.api_endpoints:
                self.log(f"{'='*80}")
                self.log(f"🔥 DISCOVERED API ENDPOINTS:")
                self.log(f"{'='*80}\n")
                
                for idx, endpoint in enumerate(scraper.api_endpoints, 1):
                    self.log(f"[{idx}] {endpoint['method']} {endpoint['url']}")
                    self.log(f"    Status: {endpoint['status']}")
                    self.log(f"    Content-Type: {endpoint['content_type']}")
                    
                    if endpoint.get('body'):
                        try:
                            body_json = json.loads(endpoint['body'])
                            body_preview = json.dumps(body_json, indent=2)[:300]
                            self.log(f"    Response Preview:\n{body_preview}...\n")
                        except:
                            self.log(f"    Response: {endpoint['body'][:200]}...\n")
            else:
                self.log("ℹ️  No API endpoints detected\n")
            
            self.log("\n✅ Results saved to 'scrape_results' folder!")
            self.update_status("Scraping completed successfully!")
            
            self.message_queue.put({
                'type': 'info_dialog',
                'title': 'Success',
                'message': (f"Scraping completed!\n\n"
                           f"API Endpoints Found: {len(scraper.api_endpoints)}\n"
                           f"Total Requests: {len(scraper.all_requests)}\n\n"
                           f"Results saved in 'scrape_results' folder.")
            })
            
        except Exception as e:
            self.log(f"\n❌ ERROR: {str(e)}\n")
            self.update_status("Scraping failed!")
            self.message_queue.put({
                'type': 'error_dialog',
                'title': 'Error',
                'message': f"Scraping failed:\n{str(e)}"
            })
        finally:
            self.message_queue.put({'type': 'done'})
            
    def stop_scrape(self):
        self.is_scraping = False
        self.log("\n⏹ Stopping scrape...\n")
        self.update_status("Stopped")
        self.scrape_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def open_results_folder(self):
        results_dir = os.path.join(os.getcwd(), 'scrape_results')
        
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
            messagebox.showinfo("Info", "Results folder created. No scrapes yet!")
            return
        
        try:
            if os.name == 'nt':
                os.startfile(results_dir)
            elif os.name == 'posix':
                import subprocess
                subprocess.run(['xdg-open', results_dir])
            else:
                messagebox.showinfo("Results Location", f"Results are saved in:\n{results_dir}")
        except Exception as e:
            messagebox.showinfo("Results Location", f"Results are saved in:\n{results_dir}")

def main():
    root = tk.Tk()
    app = ScraperGUI(root)
    
    def on_closing():
        if app.is_scraping:
            if messagebox.askokcancel("Quit", "Scraping in progress. Do you want to quit?"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
