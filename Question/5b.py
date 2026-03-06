import tkinter as tk
from tkinter import messagebox
import requests 
import threading
import time

API_KEY = "bbebddfb4df3535c9df9d79a78c994e6" 
CITIES = ["Kathmandu", "Pokhara", "Lalitpur", "Biratnagar", "Chitwan"]
URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nepal Weather Latency Analyzer")
        self.root.geometry("500x500")


        tk.Label(root, text="Multi-threaded Weather Collector", font=("Arial", 14, "bold")).pack(pady=10)
        
        self.display = tk.Text(root, height=15, width=55, state='disabled', bg="#f0f0f0")
        self.display.pack(pady=10)

        self.btn_seq = tk.Button(root, text="Run Sequential", command=self.run_sequential, bg="#ff9999", width=15)
        self.btn_seq.pack(side=tk.LEFT, padx=40)

        self.btn_para = tk.Button(root, text="Run Parallel", command=self.run_parallel, bg="#99ff99", width=15)
        self.btn_para.pack(side=tk.RIGHT, padx=40)

        self.footer = tk.Label(root, text="Status: Ready", fg="blue")
        self.footer.pack(side=tk.BOTTOM, pady=10)

    def write_to_log(self, text):
        self.display.config(state='normal')
        self.display.insert(tk.END, text + "\n")
        self.display.config(state='disabled')
        self.display.see(tk.END)

    def fetch_data(self, city):
        """Standard function to fetch API data"""
        try:
            start = time.time()
            response = requests.get(URL.format(city, API_KEY), timeout=5)
            elapsed = time.time() - start
            if response.status_code == 200:
                temp = response.json()['main']['temp']
                return f"SUCCESS: {city} -> {temp}°C (Took {elapsed:.2f}s)"
            return f"FAILED: {city} (API Error)"
        except:
            return f"ERROR: {city} (Connection Timeout)"

    def run_sequential(self):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)
        self.write_to_log("--- Starting Sequential Fetch ---")
        
        start_total = time.perf_counter()
        for city in CITIES:
            result = self.fetch_data(city)
            self.write_to_log(result)
        
        end_total = time.perf_counter()
        self.footer.config(text=f"Sequential Total Time: {end_total - start_total:.2f} seconds")

    def run_parallel(self):
        self.display.config(state='normal')
        self.display.delete('1.0', tk.END)
        self.write_to_log("--- Starting Parallel (Multi-threaded) Fetch ---")
        
        start_total = time.perf_counter()
        threads = []
        results = []

    
        def thread_worker(city):
            res = self.fetch_data(city)
            results.append(res)

        for city in CITIES:
            t = threading.Thread(target=thread_worker, args=(city,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        for r in results:
            self.write_to_log(r)

        end_total = time.perf_counter()
        self.footer.config(text=f"Parallel Total Time: {end_total - start_total:.2f} seconds")

if __name__ == "__main__":

    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()