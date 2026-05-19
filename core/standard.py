import tkinter as tk
from tkinter import messagebox
import math
import ast
import operator

# GÜVENLİ MATEMATİK PARSER
GUVENLI_OPERATORLER = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def guvenli_eval(expr):
    """eval() yerine güvenli matematik parser"""
    try:
        expr = expr.replace("×", "*").replace("÷", "/")
        tree = ast.parse(expr, mode='eval')
        
        def _eval(node):
            if isinstance(node, ast.Constant):
                return node.value
            elif isinstance(node, ast.BinOp):
                left = _eval(node.left)
                right = _eval(node.right)
                return GUVENLI_OPERATORLER[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = _eval(node.operand)
                return GUVENLI_OPERATORLER[type(node.op)](operand)
            else:
                raise ValueError(f"Desteklenmeyen işlem")
        
        return _eval(tree.body)
    except Exception as e:
        raise Exception(f"Hesaplama hatası")

# ANA SINIF
class StandardMode(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=colors["bg"])
        self.colors = colors
        self.ifade = ""
        self.gecmis = ""
        self.sayi1 = None
        self.islem = None
        self.yeni_sayi = True
        
        self._setup_ui()
        self._create_buttons()
        self._setup_keyboard()
    
    def _setup_ui(self):
        ekran_frame = tk.Frame(self, bg="white", bd=0, relief=tk.FLAT)
        ekran_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        self.gecmis_var = tk.StringVar()
        self.gecmis_label = tk.Label(ekran_frame, textvariable=self.gecmis_var,
            font=("Segoe UI", 11), justify="right", anchor="e",
            bg="white", fg="#888888", height=1)
        self.gecmis_label.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        self.ekran_var = tk.StringVar()
        self.ekran = tk.Entry(ekran_frame, textvariable=self.ekran_var,
            font=("Segoe UI", 32), justify="right", bd=0, relief=tk.FLAT,
            bg="white", fg="black", state="readonly", readonlybackground="white")
        self.ekran.pack(fill=tk.X, ipady=10)
        
        self.ekran.bind("<Configure>", self._ajusta_yazi_boyutu)
        
        self.button_frame = tk.Frame(self, bg=self.colors["bg"])
        self.button_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
    
    def _ajusta_yazi_boyutu(self, event=None):
        text = self.ekran_var.get()
        if not text:
            return
        for size in range(32, 14, -2):
            max_chars = self.ekran.winfo_width() // (size // 2)
            if len(text) <= max_chars or size <= 16:
                self.ekran.config(font=("Segoe UI", size))
                break
    
    def _format_number(self, sayi):
        try:
            num = float(sayi)
            if math.isinf(num) or math.isnan(num):
                return "Hata"
            if abs(num) >= 1e15 or (abs(num) < 1e-12 and num != 0):
                return f"{num:.12e}".rstrip("0").rstrip(".")
            else:
                if num.is_integer():
                    return str(int(num))
                else:
                    return f"{num:.12f}".rstrip("0").rstrip(".")
        except:
            return str(sayi)
    
    def _update_display(self):
        if self.ifade:
            self.ekran_var.set(self._format_number(self.ifade))
        else:
            self.ekran_var.set("0")
        if self.gecmis:
            self.gecmis_var.set(self.gecmis)
        else:
            self.gecmis_var.set("")
        self._ajusta_yazi_boyutu()
    
    def _create_buttons(self):
        for i in range(6):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.button_frame.grid_columnconfigure(i, weight=1)
        
        butonlar = [("%",0,0), ("CE",0,1), ("C",0,2), ("⌫",0,3),
            ("1/x",1,0), ("x²",1,1), ("√x",1,2), ("÷",1,3),
            ("7",2,0), ("8",2,1), ("9",2,2), ("×",2,3),
            ("4",3,0), ("5",3,1), ("6",3,2), ("-",3,3),
            ("1",4,0), ("2",4,1), ("3",4,2), ("+",4,3),
            ("±",5,0), ("0",5,1), (".",5,2), ("=",5,3)]
        
        for text, row, col in butonlar:
            if text == "=":
                bg = self.colors["equal"]
                hover = self.colors.get("equal_hover", "#106ebe")
            elif text in ("÷","×","-","+","%","1/x","x²","√x","±","CE","C","⌫"):
                bg = self.colors["operator"]
                hover = "#d0d0d0"
            else:
                bg = self.colors["button"]
                hover = "#e5e5e5"
            
            btn = tk.Button(self.button_frame, text=text, font=("Segoe UI", 12),
                bg=bg, fg=self.colors["text"], bd=0, padx=12, pady=14, cursor="hand2")
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            
            # HOVER EFEKTİ
            btn.bind("<Enter>", lambda e, b=btn, h=hover: b.config(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, orig=bg: b.config(bg=orig))
            
            btn.config(command=lambda t=text: self._click(t))
    
    def _hesapla(self):
        try:
            sayi2 = float(self.ifade) if self.ifade else 0
            
            if self.islem == "+":
                sonuc = self.sayi1 + sayi2
            elif self.islem == "-":
                sonuc = self.sayi1 - sayi2
            elif self.islem == "×":
                sonuc = self.sayi1 * sayi2
            elif self.islem == "÷":
                if sayi2 == 0:
                    messagebox.showerror("Hata", "Sıfıra bölünemez!")
                    self.ifade = ""
                    self.sayi1 = None
                    self.islem = None
                    self._update_display()
                    return
                sonuc = self.sayi1 / sayi2
            else:
                sonuc = sayi2
            
            if math.isinf(sonuc) or math.isnan(sonuc):
                messagebox.showerror("Hata", "Geçersiz işlem!")
                self.ifade = ""
                self.sayi1 = None
                self.islem = None
                self._update_display()
                return
            
            self.ifade = str(sonuc)
            self.sayi1 = sonuc
        except OverflowError:
            messagebox.showerror("Hata", "Sayı çok büyük!")
            self.ifade = ""
            self.sayi1 = None
            self.islem = None
        except Exception as e:
            messagebox.showerror("Hata", str(e))
            self.ifade = ""
            self.sayi1 = None
            self.islem = None
    
    def _click(self, tus):
        if tus == "C":
            self.ifade = ""
            self.gecmis = ""
            self.sayi1 = None
            self.islem = None
            self.yeni_sayi = True
        
        elif tus == "CE":
            self.ifade = ""
            self.yeni_sayi = True
        
        elif tus == "⌫":
            self.ifade = self.ifade[:-1]
            if not self.ifade:
                self.ifade = "0"
        
        elif tus in ("+", "-", "×", "÷"):
            if self.ifade:
                if self.sayi1 is not None and self.islem and not self.yeni_sayi:
                    self._hesapla()
                else:
                    self.sayi1 = float(self.ifade) if self.ifade else 0
                
                self.islem = tus
                self.yeni_sayi = True
                self.gecmis = f"{self._format_number(str(self.sayi1))} {self.islem}"
                self.ifade = ""
        
        elif tus == "=":
            if self.sayi1 is not None and self.islem:
                self.gecmis = f"{self._format_number(str(self.sayi1))} {self.islem} {self._format_number(self.ifade)} ="
                self._hesapla()
                self.islem = None
                self.yeni_sayi = True
        
        elif tus == "±":
            try:
                self.ifade = str(-float(self.ifade))
            except:
                pass
        
        elif tus == "%":
            try:
                self.ifade = str(float(self.ifade) / 100)
            except:
                pass
        
        elif tus == "1/x":
            try:
                val = float(self.ifade)
                if val == 0:
                    raise
                self.ifade = str(1 / val)
            except:
                messagebox.showerror("Hata", "Sıfırın tersi yok!")
        
        elif tus == "x²":
            try:
                self.ifade = str(float(self.ifade) ** 2)
            except:
                pass
        
        elif tus == "√x":
            try:
                val = float(self.ifade)
                if val < 0:
                    raise
                self.ifade = str(math.sqrt(val))
            except:
                messagebox.showerror("Hata", "Negatif sayının karekökü olmaz!")
        
        else:
            if self.yeni_sayi:
                self.ifade = ""
                self.yeni_sayi = False
            if len(self.ifade) < 25:
                self.ifade += tus
        
        self._update_display()
    
    def _setup_keyboard(self):
        self.master.bind_all("<Key>", self._key_press)
        self.master.bind_all("<Return>", lambda e: self._click("="))
        self.master.bind_all("<KP_Enter>", lambda e: self._click("="))
        self.master.bind_all("<BackSpace>", lambda e: self._click("⌫"))
        self.master.bind_all("<Escape>", lambda e: self._click("C"))
    
    def _key_press(self, event):
        key = event.char
        if key.isdigit():
            self._click(key)
        elif key in "+-*/.":
            if key == "*":
                self._click("×")
            elif key == "/":
                self._click("÷")
            else:
                self._click(key)
        elif key == "%":
            self._click("%")