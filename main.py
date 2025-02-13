import tkinter as tk
from tkinter import filedialog, messagebox
import time
import threading

class CyberThreatKeywordMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyber Threat Keyword Monitor")
        self.geometry("700x500")
        self.configure(bg="#f0f4f8")  # Light pastel background
        self.keywords = ["malware", "attack", "breach", "ransomware"]
        self.monitoring = False
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self, text="Cyber Threat Keyword Monitor", font=("Verdana", 24, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=20)
        
        # File selection button
        tk.Button(self, text="Select Log File", command=self.select_file, font=("Verdana", 14), bg="#3498db", fg="white", width=20).pack(pady=10)
        
        # Keyword management area
        tk.Label(self, text="Keywords to Monitor:", font=("Verdana", 14), bg="#f0f4f8").pack(pady=5)
        self.keyword_listbox = tk.Listbox(self, font=("Verdana", 12), height=5, width=50)
        self.keyword_listbox.pack(pady=5)
        self.update_keyword_list()
        
        keyword_button_frame = tk.Frame(self, bg="#f0f4f8")
        keyword_button_frame.pack(pady=5)
        tk.Button(keyword_button_frame, text="Add Keyword", command=self.add_keyword, font=("Verdana", 12), bg="#2ecc71", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(keyword_button_frame, text="Remove Selected", command=self.remove_keyword, font=("Verdana", 12), bg="#e74c3c", fg="white", width=15).grid(row=0, column=1, padx=5)
        
        # Start/Stop monitoring buttons
        self.monitor_button = tk.Button(self, text="Start Monitoring", command=self.start_monitoring, font=("Verdana", 14), bg="#f39c12", fg="white", width=20)
        self.monitor_button.pack(pady=20)
        
        # Log display area
        self.log_text = tk.Text(self, font=("Verdana", 12), height=10, width=80, state=tk.DISABLED, wrap=tk.WORD)
        self.log_text.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(title="Select a Log File")
        if self.file_path:
            messagebox.showinfo("File Selected", f"Monitoring file: {self.file_path}")

    def update_keyword_list(self):
        self.keyword_listbox.delete(0, tk.END)
        for keyword in self.keywords:
            self.keyword_listbox.insert(tk.END, keyword)

    def add_keyword(self):
        new_keyword = simpledialog.askstring("Add Keyword", "Enter a new keyword:")
        if new_keyword and new_keyword not in self.keywords:
            self.keywords.append(new_keyword)
            self.update_keyword_list()
            messagebox.showinfo("Success", f"Keyword '{new_keyword}' added.")
        elif new_keyword in self.keywords:
            messagebox.showwarning("Duplicate Keyword", "This keyword already exists.")

    def remove_keyword(self):
        selected_index = self.keyword_listbox.curselection()
        if selected_index:
            keyword = self.keyword_listbox.get(selected_index)
            self.keywords.remove(keyword)
            self.update_keyword_list()
            messagebox.showinfo("Success", f"Keyword '{keyword}' removed.")
        else:
            messagebox.showwarning("No Selection", "Please select a keyword to remove.")

    def start_monitoring(self):
        if not hasattr(self, "file_path") or not self.file_path:
            messagebox.showwarning("No File Selected", "Please select a log file to monitor.")
            return
        if not self.monitoring:
            self.monitoring = True
            self.monitor_button.config(text="Stop Monitoring", bg="#e74c3c")
            threading.Thread(target=self.monitor_file, daemon=True).start()
        else:
            self.monitoring = False
            self.monitor_button.config(text="Start Monitoring", bg="#f39c12")

    def monitor_file(self):
        with open(self.file_path, "r") as file:
            file.seek(0, os.SEEK_END)  # Move to the end of the file
            while self.monitoring:
                line = file.readline()
                if not line:
                    time.sleep(1)
                    continue
                for keyword in self.keywords:
                    if keyword.lower() in line.lower():
                        self.log_alert(line, keyword)

    def log_alert(self, line, keyword):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"Keyword '{keyword}' detected: {line}")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        messagebox.showinfo("Alert", f"Keyword '{keyword}' detected in the log file.")

if __name__ == "__main__":
    app = CyberThreatKeywordMonitor()
    app.mainloop()
