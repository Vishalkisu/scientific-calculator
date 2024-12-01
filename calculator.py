import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("500x750")
        self.root.configure(bg="#1a1a1a")  # Dark theme
        
        # Variables
        self.current_expression = ""
        self.memory = 0
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg="#1a1a1a")
        self.main_frame.pack(expand=True, fill="both", padx=15, pady=15)
        
        # Entry field for display
        display_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        display_frame.pack(fill="x", pady=(0, 15))
        
        self.display = tk.Entry(
            display_frame,
            font=("Segoe UI", 36),
            justify="right",
            bd=0,
            bg="#2d2d2d",
            fg="#ffffff",
            insertbackground="#ffffff"
        )
        self.display.pack(fill="x", ipady=15)
        
        # Memory display
        self.memory_label = tk.Label(
            display_frame,
            text="M: 0",
            font=("Segoe UI", 12),
            bg="#1a1a1a",
            fg="#666666"
        )
        self.memory_label.pack(anchor="e", pady=(5, 0))
        
        # Buttons frame
        buttons_frame = tk.Frame(self.main_frame, bg="#1a1a1a")
        buttons_frame.pack(expand=True, fill="both")
        
        # Configure grid
        for i in range(8):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Button style
        button_style = {
            "font": ("Segoe UI", 14),
            "borderwidth": 0,
            "relief": "flat",
            "pady": 10,
            "padx": 10
        }
        
        # Define buttons with their properties
        memory_buttons = [
            {"text": "MC", "bg": "#333333", "fg": "#ffffff", "cmd": self.memory_clear},
            {"text": "MR", "bg": "#333333", "fg": "#ffffff", "cmd": self.memory_recall},
            {"text": "M+", "bg": "#333333", "fg": "#ffffff", "cmd": self.memory_add},
            {"text": "M-", "bg": "#333333", "fg": "#ffffff", "cmd": self.memory_subtract},
            {"text": "MS", "bg": "#333333", "fg": "#ffffff", "cmd": self.memory_store},
        ]
        
        # Create memory buttons
        for i, btn in enumerate(memory_buttons):
            button = tk.Button(
                buttons_frame,
                text=btn["text"],
                command=btn["cmd"],
                bg=btn["bg"],
                fg=btn["fg"],
                activebackground="#404040",
                activeforeground="#ffffff",
                **button_style
            )
            button.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
        
        # Scientific functions
        scientific_buttons = [
            {"text": "sin", "cmd": lambda: self.scientific_function("math.sin")},
            {"text": "cos", "cmd": lambda: self.scientific_function("math.cos")},
            {"text": "tan", "cmd": lambda: self.scientific_function("math.tan")},
            {"text": "√", "cmd": lambda: self.scientific_function("math.sqrt")},
            {"text": "x²", "cmd": lambda: self.click("**2")},
        ]
        
        for i, btn in enumerate(scientific_buttons):
            button = tk.Button(
                buttons_frame,
                text=btn["text"],
                command=btn["cmd"],
                bg="#262626",
                fg="#00ff00",
                activebackground="#333333",
                activeforeground="#00ff00",
                **button_style
            )
            button.grid(row=1, column=i, padx=2, pady=2, sticky="nsew")
        
        # Main buttons layout
        main_buttons = [
            {"text": "(", "bg": "#262626", "fg": "#00ff00"},
            {"text": ")", "bg": "#262626", "fg": "#00ff00"},
            {"text": "%", "bg": "#262626", "fg": "#00ff00"},
            {"text": "⌫", "bg": "#ff4444", "fg": "white"},
            {"text": "C", "bg": "#ff4444", "fg": "white"},
            
            {"text": "7", "bg": "#404040", "fg": "white"},
            {"text": "8", "bg": "#404040", "fg": "white"},
            {"text": "9", "bg": "#404040", "fg": "white"},
            {"text": "÷", "bg": "#ff9500", "fg": "white", "cmd": lambda: self.click("/")},
            {"text": "π", "bg": "#262626", "fg": "#00ff00", "cmd": lambda: self.click("math.pi")},
            
            {"text": "4", "bg": "#404040", "fg": "white"},
            {"text": "5", "bg": "#404040", "fg": "white"},
            {"text": "6", "bg": "#404040", "fg": "white"},
            {"text": "×", "bg": "#ff9500", "fg": "white", "cmd": lambda: self.click("*")},
            {"text": "e", "bg": "#262626", "fg": "#00ff00", "cmd": lambda: self.click("math.e")},
            
            {"text": "1", "bg": "#404040", "fg": "white"},
            {"text": "2", "bg": "#404040", "fg": "white"},
            {"text": "3", "bg": "#404040", "fg": "white"},
            {"text": "-", "bg": "#ff9500", "fg": "white"},
            {"text": "ln", "bg": "#262626", "fg": "#00ff00", "cmd": lambda: self.scientific_function("math.log")},
            
            {"text": "0", "bg": "#404040", "fg": "white"},
            {"text": ".", "bg": "#404040", "fg": "white"},
            {"text": "±", "bg": "#404040", "fg": "white", "cmd": self.toggle_sign},
            {"text": "+", "bg": "#ff9500", "fg": "white"},
            {"text": "=", "bg": "#00aa00", "fg": "white"},
        ]
        
        row, col = 2, 0
        for btn in main_buttons:
            cmd = btn.get("cmd", lambda x=btn["text"]: self.click(x))
            button = tk.Button(
                buttons_frame,
                text=btn["text"],
                command=cmd,
                bg=btn["bg"],
                fg=btn["fg"],
                activebackground=btn["bg"],
                activeforeground=btn["fg"],
                **button_style
            )
            button.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 4:
                col = 0
                row += 1
        
        # Bind keyboard events
        self.root.bind('<Key>', self.key_press)
        
    def scientific_function(self, func):
        try:
            current = self.display.get()
            if current:
                result = eval(f"{func}({current})")
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
        except:
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, "Error")
    
    def toggle_sign(self):
        try:
            current = self.display.get()
            if current:
                if current.startswith('-'):
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, current[1:])
                else:
                    self.display.delete(0, tk.END)
                    self.display.insert(tk.END, '-' + current)
        except:
            pass
    
    def memory_clear(self):
        self.memory = 0
        self.memory_label.config(text="M: 0")
    
    def memory_recall(self):
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, str(self.memory))
    
    def memory_add(self):
        try:
            current = float(self.display.get())
            self.memory += current
            self.memory_label.config(text=f"M: {self.memory}")
        except:
            pass
    
    def memory_subtract(self):
        try:
            current = float(self.display.get())
            self.memory -= current
            self.memory_label.config(text=f"M: {self.memory}")
        except:
            pass
    
    def memory_store(self):
        try:
            self.memory = float(self.display.get())
            self.memory_label.config(text=f"M: {self.memory}")
        except:
            pass
            
    def click(self, key):
        if key == '=':
            try:
                result = eval(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif key == 'C':
            self.clear()
        elif key == '⌫':
            current = self.display.get()
            self.display.delete(0, tk.END)
            self.display.insert(0, current[:-1])
        else:
            self.display.insert(tk.END, key)
            
    def clear(self):
        self.display.delete(0, tk.END)
        
    def key_press(self, event):
        valid_chars = '0123456789+-*/().='
        if event.char in valid_chars:
            self.click(event.char)
        elif event.keysym == 'Return':
            self.click('=')
        elif event.keysym == 'BackSpace':
            self.click('⌫')
        elif event.keysym == 'Escape':
            self.clear()

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
