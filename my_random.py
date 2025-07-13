import tkinter as tk
from tkinter import messagebox
import random
import threading
import keyboard
import pystray
from PIL import Image, ImageDraw

class StealthRandomizerApp:
    def __init__(self):
        self.secret_number = None
        self.range_min = 1
        self.range_max = 100

        self.root = tk.Tk()
        self.root.title("Stealth Randomizer")
        self.root.geometry("320x180")

        # Ввод диапазона прямо в интерфейсе
        tk.Label(self.root, text="Min:").pack()
        self.min_entry = tk.Entry(self.root)
        self.min_entry.insert(0, "1")
        self.min_entry.pack()

        tk.Label(self.root, text="Max:").pack()
        self.max_entry = tk.Entry(self.root)
        self.max_entry.insert(0, "100")
        self.max_entry.pack()

        self.set_button = tk.Button(self.root, text="Set Range", command=self.set_range)
        self.set_button.pack(pady=5)

        self.label = tk.Label(self.root, text="Waiting for input...", font=("Arial", 14))
        self.label.pack(pady=10)

        self.icon = pystray.Icon("stealth_randomizer", self.create_image(), "Stealth Randomizer", menu=pystray.Menu(
            pystray.MenuItem("Exit", self.exit_app)
        ))

        threading.Thread(target=self.icon.run, daemon=True).start()

        # Секретный ввод по Ctrl+Alt+S
        keyboard.add_hotkey('ctrl+alt+s', self.set_secret_number)

    def create_image(self):
        image = Image.new('RGB', (64, 64), "black")
        d = ImageDraw.Draw(image)
        d.rectangle([16, 16, 48, 48], fill="white")
        return image

    def set_range(self):
        try:
            min_val = int(self.min_entry.get())
            max_val = int(self.max_entry.get())

            if min_val >= max_val:
                messagebox.showerror("Invalid range", "Minimum must be less than maximum.")
                return

            self.range_min = min_val
            self.range_max = max_val
            self.label.config(text=f"Range set: {self.range_min}–{self.range_max}")

            self.update_random_number()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")

    def update_random_number(self):
        if self.secret_number is not None:
            display_number = self.secret_number
        else:
            display_number = random.randint(self.range_min, self.range_max)

        self.label.config(text=f"Number: {display_number}")
        self.root.after(1000, self.update_random_number)

    def set_secret_number(self):
        # Секретный режим — появляется диалог только по горячей клавише
        def ask():
            from tkinter import simpledialog
            result = simpledialog.askstring("Secret", "Enter secret number (hidden):", show="*", parent=self.root)
            if result and result.isdigit():
                self.secret_number = int(result)
                self.label.config(text="Secret number activated.")
                self.root.after(3000, self.update_label)
            else:
                self.secret_number = None
                self.label.config(text="Invalid or cancelled.")

        self.root.after(0, ask)

    def update_label(self):
        self.label.config(text=f"Range set: {self.range_min}–{self.range_max}")

    def exit_app(self, icon, item):
        self.icon.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = StealthRandomizerApp()
    app.run()
