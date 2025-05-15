import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import tkinter as tk
from tkinter import ttk

class AutoClicker:
    def __init__(self):
        self.clicking = False
        self.mouse = Controller()
        self.click_interval = 0.1  
        self.toggle_key = KeyCode(char="c")
        
        self.root = tk.Tk()
        self.root.title("AutoClicker")
        self.root.geometry("300x200")
        
        self.status_label = ttk.Label(self.root, text="Status: Stopped")
        self.status_label.pack(pady=10)
        
        ttk.Label(self.root, text="Click interval (per second):").pack()
        self.interval_entry = ttk.Entry(self.root)
        self.interval_entry.insert(0, str(self.click_interval))
        self.interval_entry.pack(pady=5)
        
        ttk.Label(self.root, text="Press 'c' button to start/stop").pack(pady=10)
        
        self.click_thread = threading.Thread(target=self.clicker, daemon=True)
        self.click_thread.start()
        
        self.listener = Listener(on_press=self.toggle_event)
        self.listener.start()
        
    def clicker(self):
        while True:
            if self.clicking:
                try:
                    self.mouse.click(Button.left, 1)
                    time.sleep(self.click_interval)
                except Exception as e:
                    print(f"Wrong key: {e}")
            time.sleep(0.01)
    
    def toggle_event(self, key):
        if key == self.toggle_key:
            self.clicking = not self.clicking
            status = "Executing" if self.clicking else "Stopped"
            self.status_label.config(text=f"Status: {status}")
            
            try:
                new_interval = float(self.interval_entry.get())
                if new_interval > 0:
                    self.click_interval = new_interval
            except ValueError:
                pass
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    auto_clicker = AutoClicker()
    auto_clicker.run() 