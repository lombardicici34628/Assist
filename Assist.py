import threading
import speech_recognition as sr
import requests
import queue
import tkinter as tk
from tkinter import simpledialog, messagebox
import ctypes, ctypes.wintypes as wintypes
import keyboard

# Constants
WDA_EXCLUDEFROMCAPTURE = 0x00000011

# Helper to hide from screen capture (Windows)
def hide_from_capture(hwnd):
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    SetWindowDisplayAffinity = user32.SetWindowDisplayAffinity
    SetWindowDisplayAffinity.argtypes = (wintypes.HWND, wintypes.DWORD)
    SetWindowDisplayAffinity.restype = wintypes.BOOL
    SetWindowDisplayAffinity(hwnd, WDA_EXCLUDEFROMCAPTURE)

# API Key Dialog
class APIKeyDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="API Key:").pack()
        self.entry = tk.Entry(master, show="*", width=40)
        self.entry.pack()
        return self.entry
    def apply(self):
        self.result = self.entry.get().strip()

# Q&A logic (runs in background)
def listen_and_qa(stop_event, qa_queue, api_key):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as src:
        while not stop_event.is_set():
            try:
                audio = recognizer.listen(src, timeout=2, phrase_time_limit=5)
                q = recognizer.recognize_google(audio)
            except Exception:
                continue
            qa_queue.put((q, "..."))
            try:
                resp = requests.post(
                    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent",
                    params={"key": api_key},
                    json={"contents":[{"parts":[{"text":q}]}]},
                    timeout=20
                )
                data = resp.json()
                ans = data['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                ans = f"(No response: {e})"
            qa_queue.put((q, ans))

# Main UI Window
class QAWindow:
    def __init__(self, root, qa_queue, stop_event):
        self.root = root
        self.qa_queue = qa_queue
        self.stop_event = stop_event
        # --- Professional overlay styling ---
        root.title('AI Interview Helper')
        root.attributes('-topmost', True)
        root.overrideredirect(True)  # Borderless
        root.attributes('-alpha', 0.92)  # Semi-transparent
        root.configure(bg='#222222')
        root.geometry('600x260+100+100')  # Larger window for easier reading
        root.attributes('-toolwindow', True)  # Hide from taskbar
        # Hide from screen capture (Windows 10+)
        root.after(200, lambda: hide_from_capture(root.winfo_id()))
        # --- End professional overlay styling ---

        # Close button
        self.close_btn = tk.Button(root, text='×', font=('Segoe UI', 14, 'bold'), fg='#fff', bg='#444', bd=0, command=self.quit, activebackground='#c00', activeforeground='#fff')
        self.close_btn.place(x=570, y=0, width=30, height=30)
        root.bind('<Escape>', lambda e: self.quit())
        # Make window draggable
        self.offset = (0,0)
        root.bind('<Button-1>', self.start_move)
        root.bind('<B1-Motion>', self.on_move)
        # --- Q&A content with copy support ---
        self.qtext = tk.Text(root, height=3, font=('Segoe UI', 13, 'bold'), fg='#00eaff', bg='#222222', wrap='word', bd=0, highlightthickness=0)
        self.qtext.pack(fill="x", padx=16, pady=(16,0))
        self.qtext.insert('1.0', 'Waiting for question...')
        self.qtext.config(state='normal')  # Enable selection/copy
        self.atext = tk.Text(root, height=7, font=('Segoe UI', 13), fg='#ffffff', bg='#222222', wrap='word', bd=0, highlightthickness=0)
        self.atext.pack(fill="x", padx=16, pady=(10,16))
        self.atext.config(state='normal')  # Enable selection/copy
        # Enable right-click copy
        self.qtext.bind('<Button-3>', self._show_context_menu)
        self.atext.bind('<Button-3>', self._show_context_menu)
        self._create_context_menu()
        # --- End Q&A content ---
        root.after(100, self.process_queue)
        keyboard.add_hotkey('ctrl+shift+h', self.toggle)

    def _create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label='Copy', command=self._copy_selection)
    def _show_context_menu(self, event):
        widget = event.widget
        widget.focus_set()
        self.context_menu.tk_popup(event.x_root, event.y_root)
    def _copy_selection(self):
        try:
            widget = self.root.focus_get()
            selection = widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selection)
        except Exception:
            pass

    def start_move(self, e):
        self.offset = (e.x, e.y)
    def on_move(self, e):
        x, y = e.x_root - self.offset[0], e.y_root - self.offset[1]
        self.root.geometry(f"+{x}+{y}")

    def process_queue(self):
        while not self.qa_queue.empty():
            q, a = self.qa_queue.get_nowait()
            self.qtext.config(state='normal'); self.qtext.delete('1.0','end'); self.qtext.insert('1.0', f"Q: {q}")
            self.qtext.config(state='normal')  # Keep enabled for selection/copy
            self.atext.config(state='normal'); self.atext.delete('1.0','end'); self.atext.insert('1.0', f"A: {a}")
            self.atext.config(state='normal')  # Keep enabled for selection/copy
        if not self.stop_event.is_set():
            self.root.after(200, self.process_queue)

    def toggle(self):
        if self.root.state()=='withdrawn':
            self.root.deiconify()
        else:
            self.root.withdraw()

    def quit(self):
        self.stop_event.set()
        self.root.destroy()

# Main
def main():
    root = tk.Tk()
    root.withdraw()
    dialog = APIKeyDialog(root)
    api_key = getattr(dialog, 'result', None)
    if not api_key:
        messagebox.showerror("No key", "API key is required.")
        return

    qa_queue = queue.Queue()
    stop_event = threading.Event()
    window = QAWindow(tk.Toplevel(root), qa_queue, stop_event)

    # Start Q&A thread *after* UI is running
    window.root.after(100, lambda: threading.Thread(
        target=listen_and_qa, args=(stop_event, qa_queue, api_key), daemon=True
    ).start())

    window.root.mainloop()

if __name__ == "__main__":
    main()
