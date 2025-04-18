import os
import re
import json
import customtkinter as ctk
from tkinter import filedialog

# Regex patterns
LOG_PATTERN = re.compile(r"URL: (.*?)\nUsername: (.*?)\nPassword: (.*?)\n")
INFO_PATTERN = re.compile(r"City: (.*?)\nIP: (.*?)\n")


def search_logs(folder, target_url=None, target_browser=None, target_city=None, target_ip=None, target_user=None, target_pass=None):
    found_logs = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        matches = LOG_PATTERN.findall(content)
                        for match in matches:
                            url, username, password = match
                            if ((target_url and target_url in url) or
                                (target_browser and target_browser in url) or
                                (target_user and target_user in username) or
                                (target_pass and target_pass in password)):
                                found_logs.append({"File": file_path, "URL": url, "Username": username, "Password": password})
                        if target_city or target_ip:
                            info_matches = INFO_PATTERN.findall(content)
                            for city, ip in info_matches:
                                if ((target_city and target_city in city) or
                                    (target_ip and target_ip in ip)):
                                    found_logs.append({"File": file_path, "City": city, "IP": ip})
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    return found_logs


def save_results(results, format_choice):
    save_path = filedialog.asksaveasfilename(defaultextension=f".{format_choice}", filetypes=[(f"{format_choice.upper()} Files", f"*.{format_choice}")])
    if save_path:
        if format_choice == "json":
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=4)
        elif format_choice == "html" or format_choice == "txt":
            with open(save_path, "w", encoding="utf-8") as f:
                for result in results:
                    f.write(json.dumps(result, indent=4) + "\n")
        print(f"Results saved to {save_path}")


def run_search():
    folder = filedialog.askdirectory(title="Select Log Folder")
    url = url_entry.get()
    browser = browser_entry.get()
    city = city_entry.get()
    ip = ip_entry.get()
    user = user_entry.get()
    password = pass_entry.get()
    format_choice = format_var.get()

    if folder:
        results = search_logs(folder, url, browser, city, ip, user, password)
        if results:
            save_results(results, format_choice)
        else:
            print("No matching logs found.")


ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.title("Redline Log Search")
root.geometry("500x600")

ctk.CTkLabel(root, text="Redline Log Search Tool", font=("Arial", 24)).pack(pady=10)

url_entry = ctk.CTkEntry(root, placeholder_text="URL")
url_entry.pack(pady=5)

browser_entry = ctk.CTkEntry(root, placeholder_text="Browser Type")
browser_entry.pack(pady=5)

city_entry = ctk.CTkEntry(root, placeholder_text="City")
city_entry.pack(pady=5)

ip_entry = ctk.CTkEntry(root, placeholder_text="IP")
ip_entry.pack(pady=5)

user_entry = ctk.CTkEntry(root, placeholder_text="Username")
user_entry.pack(pady=5)

pass_entry = ctk.CTkEntry(root, placeholder_text="Password")
pass_entry.pack(pady=5)

format_var = ctk.StringVar(value="txt")
ctk.CTkLabel(root, text="Result Format").pack(pady=5)
ctk.CTkOptionMenu(root, variable=format_var, values=["txt", "html", "json"]).pack(pady=5)

ctk.CTkButton(root, text="Search Logs", command=run_search).pack(pady=20)

root.mainloop()
