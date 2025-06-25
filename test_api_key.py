import requests
import tkinter as tk
from tkinter import simpledialog, messagebox

def get_api_key():
    root = tk.Tk()
    root.withdraw()
    api_key = simpledialog.askstring("Google Gemini API Key", "Paste your Google Gemini API key:")
    root.destroy()
    return api_key

def test_gemini_api_key(api_key):
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": api_key}
        data = {
            "contents": [{"parts": [{"text": "Hello"}]}]
        }
        response = requests.post(url, headers=headers, params=params, json=data, timeout=10)
        if response.status_code == 200 and 'candidates' in response.json():
            return True
        else:
            print(f"Gemini API key test failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Gemini API key test failed: {e}")
        return False

if __name__ == "__main__":
    api_key = get_api_key()
    if not api_key:
        print("No API key entered.")
        exit(1)
    if test_gemini_api_key(api_key):
        print("API key is valid!")
        tk.Tk().withdraw()
        messagebox.showinfo("Success", "API key is valid!")
    else:
        print("API key is invalid.")
        tk.Tk().withdraw()
        messagebox.showerror("Error", "API key is invalid.")