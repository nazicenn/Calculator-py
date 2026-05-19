import tkinter as tk
from app.config.settings import AppConfig, Colors
from app.config.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from app.core.standard import StandardMode

class CalculatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(AppConfig.APP_NAME)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        self.themes = {
            "🌸": Colors.PASTEL, "💜": Colors.PURPLE,
            "🌊": Colors.OCEAN, "🌿": Colors.FOREST, "⚡": Colors.NEON
        }
        self.current_theme = "🌸"
        self.colors = self.themes[self.current_theme]
        
        self._setup_ui()
        self._setup_theme_buttons()
        self.calculator = StandardMode(self.main_frame, self.colors)
        self.calculator.pack(fill=tk.BOTH, expand=True)
    
    def _setup_ui(self):
        self.root.configure(bg=self.colors["bg"])
        
        self.theme_frame = tk.Frame(self.root, bg=self.colors["menu_bg"], height=50)
        self.theme_frame.pack(fill=tk.X)
        self.theme_frame.pack_propagate(False)
        
        tk.Label(self.theme_frame, text="🧮", font=("Segoe UI", 20),
                bg=self.colors["menu_bg"], fg=self.colors["equal"]).pack(side=tk.LEFT, padx=10)
        
        tk.Label(self.theme_frame, text="Hesap Makinesi", font=("Segoe UI", 12, "bold"),
                bg=self.colors["menu_bg"], fg=self.colors["text"]).pack(side=tk.LEFT)
        
        self.main_frame = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def _setup_theme_buttons(self):
        for theme_name in self.themes.keys():
            btn = tk.Button(self.theme_frame, text=theme_name, font=("Segoe UI", 11),
                          bg=self.colors["menu_bg"], fg=self.colors["equal"],
                          bd=0, padx=8, pady=5, cursor="hand2",
                          command=lambda t=theme_name: self.change_theme(t))
            btn.pack(side=tk.RIGHT, padx=2)
    
    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.colors = self.themes[theme_name]
        self.root.configure(bg=self.colors["bg"])
        self.theme_frame.configure(bg=self.colors["menu_bg"])
        self.main_frame.configure(bg=self.colors["bg"])
        
        for child in self.theme_frame.winfo_children():
            if isinstance(child, tk.Button) and child.cget("text") in self.themes:
                child.configure(bg=self.colors["menu_bg"], fg=self.colors["equal"])
            elif isinstance(child, tk.Label):
                child.configure(bg=self.colors["menu_bg"], fg=self.colors["text"])
        
        self.calculator.destroy()
        self.calculator = StandardMode(self.main_frame, self.colors)
        self.calculator.pack(fill=tk.BOTH, expand=True)
    
    def run(self):
        self.root.mainloop()