import os
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

APP_NAME = "DPH kalkulačka v3.1 (12 % / 21 %)"
APP_VERSION = "3.1"
AUTHOR = "Dariusz Zabdyr (Darek)"

def parse_amount(text: str) -> float | None:
    t = text.strip()
    if not t:
        return None
    t = t.replace("\u00A0", "").replace(" ", "").replace(",", ".")
    return float(t)

def fmt_num(x: float) -> str:
    # Bez měny, ať se to dobře kopíruje
    return f"{x:.2f}".replace(".", ",")

def copy_to_clipboard(text: str):
    root.clipboard_clear()
    root.clipboard_append(text)

def set_readonly(var: tk.StringVar, value: str):
    var.set(value)

def vypocitej():
    try:
        sazba = float(var_sazba.get())  # 0.12 / 0.21
        zaklad = parse_amount(var_in_zaklad.get())
        celkem = parse_amount(var_in_celkem.get())

        if zaklad is None and celkem is None:
            messagebox.showinfo("Info", "Vyplň buď Základ bez DPH, nebo Celkem s DPH.")
            return

        if zaklad is not None and celkem is not None:
            messagebox.showwarning("Pozor", "Vyplň jen jedno pole, buď Základ nebo Celkem.")
            return

        if zaklad is not None:
            if zaklad < 0:
                raise ValueError
            dph = zaklad * sazba
            celkem = zaklad + dph
            mode = "Zadaný základ bez DPH"
        else:
            if celkem is None or celkem < 0:
                raise ValueError
            zaklad = celkem / (1.0 + sazba)
            dph = celkem - zaklad
            mode = "Zadané celkem s DPH"

        set_readonly(var_out_zaklad, fmt_num(zaklad))
        set_readonly(var_out_dph, fmt_num(dph))
        set_readonly(var_out_celkem, fmt_num(celkem))
        label_info.configure(text=f"{mode} | Sazba {int(sazba*100)} %")

    except ValueError:
        messagebox.showerror("Chyba", "Zadej prosím platné číslo, může být i s čárkou.")

def vycisti():
    var_in_zaklad.set("")
    var_in_celkem.set("")
    var_out_zaklad.set("")
    var_out_dph.set("")
    var_out_celkem.set("")
    label_info.configure(text="")
    entry_in_zaklad.focus_set()

def kopiruj(var: tk.StringVar, label: str):
    v = var.get().strip()
    if not v:
        messagebox.showinfo("Info", "Nejdřív něco vypočítej 🙂")
        return
    copy_to_clipboard(v)
    if show_copy_popup.get():
        messagebox.showinfo("Zkopírováno", f"{label} je v schránce.")

def kopiruj_vse():
    z = var_out_zaklad.get().strip()
    d = var_out_dph.get().strip()
    c = var_out_celkem.get().strip()
    if not (z and d and c):
        messagebox.showinfo("Info", "Nejdřív něco vypočítej 🙂")
        return

    copy_to_clipboard(f"Základ {z} | DPH {d} | Celkem {c}")
    if show_copy_popup.get():
        messagebox.showinfo("Zkopírováno", "Celý výsledek je v schránce.")

def show_help():
    messagebox.showinfo(
        "Pomoc",
        "Vyplň buď Základ bez DPH nebo Celkem s DPH.\n"
        "Vyber sazbu 12 % nebo 21 % a klikni Vypočítat.\n\n"
        "Výsledky se objeví dole ve třech polích.\n"
        "Každé pole má vlastní tlačítko Kopírovat.\n"
        "Enter spustí výpočet."
    )

def about_app():
    messagebox.showinfo("O aplikaci", f"{APP_NAME}\nVerze: {APP_VERSION}")

def about_author():
    messagebox.showinfo("O autorovi", f"Autor: {AUTHOR}\nVytvořeno v Pythonu (ttk).")

APP_ID = "dph_kalkulacka"

def get_settings_path() -> Path:
    # Windows: %APPDATA%\dph_kalkulacka\settings.json
    # macOS/Linux: ~/.config/dph_kalkulacka/settings.json
    appdata = os.environ.get("APPDATA")
    if appdata:
        base = Path(appdata) / APP_ID
    else:
        base = Path.home() / ".config" / APP_ID
    base.mkdir(parents=True, exist_ok=True)
    return base / "settings.json"

def load_settings() -> dict:
    p = get_settings_path()
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_settings(data: dict) -> None:
    p = get_settings_path()
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def on_close():
    save_settings({
        "show_copy_popup": show_copy_popup.get()
    })
    root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)

# --- UI ---
root = tk.Tk()
settings = load_settings()
show_copy_popup = tk.BooleanVar(value=bool(settings.get("show_copy_popup", True)))
root.title(APP_NAME)
root.resizable(False, False)

# ttk theme (na Windows často působí líp "vista"; fallback je OK)
try:
    style = ttk.Style()
    if "vista" in style.theme_names():
        style.theme_use("vista")
except Exception:
    pass

# Menu
menubar = tk.Menu(root)
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Konec", command=on_close)
menubar.add_cascade(label="Soubor", menu=file_menu)

settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_checkbutton(
    label="Zobrazovat potvrzení po kopírování",
    variable=show_copy_popup
)
menubar.add_cascade(label="Nastavení", menu=settings_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Pomoc", command=show_help)
help_menu.add_separator()
help_menu.add_command(label="O aplikaci", command=about_app)
help_menu.add_command(label="O autorovi", command=about_author)
menubar.add_cascade(label="Nápověda", menu=help_menu)
root.config(menu=menubar)


# Hlavní kontejner
main = ttk.Frame(root, padding=14)
main.grid(row=0, column=0, sticky="nsew")

# Vstupy (2 sloupce)
inputs = ttk.LabelFrame(main, text="Vstup", padding=12)
inputs.grid(row=0, column=0, sticky="ew")
inputs.columnconfigure(0, weight=1)
inputs.columnconfigure(1, weight=1)

ttk.Label(inputs, text="Základ bez DPH").grid(row=0, column=0, sticky="w")
ttk.Label(inputs, text="Celkem s DPH").grid(row=0, column=1, sticky="w", padx=(12, 0))

var_in_zaklad = tk.StringVar()
var_in_celkem = tk.StringVar()

entry_in_zaklad = ttk.Entry(inputs, textvariable=var_in_zaklad, width=24)
entry_in_celkem = ttk.Entry(inputs, textvariable=var_in_celkem, width=24)
entry_in_zaklad.grid(row=1, column=0, sticky="w", pady=(6, 10))
entry_in_celkem.grid(row=1, column=1, sticky="w", padx=(12, 0), pady=(6, 10))

# Sazba + tlačítka
controls = ttk.Frame(inputs)
controls.grid(row=2, column=0, columnspan=2, sticky="ew")
controls.columnconfigure(0, weight=1)

ttk.Label(controls, text="Sazba DPH").grid(row=0, column=0, sticky="w")

var_sazba = tk.StringVar(value="0.21")
radios = ttk.Frame(controls)
radios.grid(row=1, column=0, sticky="w", pady=(6, 8))

ttk.Radiobutton(radios, text="12 %", variable=var_sazba, value="0.12").grid(row=0, column=0, sticky="w")
ttk.Radiobutton(radios, text="21 %", variable=var_sazba, value="0.21").grid(row=0, column=1, sticky="w", padx=(14, 0))

btns = ttk.Frame(controls)
btns.grid(row=1, column=1, sticky="e")
ttk.Button(btns, text="Vypočítat", command=vypocitej).grid(row=0, column=0, padx=(0, 8))
ttk.Button(btns, text="Vyčistit", command=vycisti).grid(row=0, column=1)

label_info = ttk.Label(inputs, text="")
label_info.grid(row=3, column=0, columnspan=2, sticky="w", pady=(6, 0))

# Výstupy
outputs = ttk.LabelFrame(main, text="Výsledek", padding=12)
outputs.grid(row=1, column=0, sticky="ew", pady=(12, 0))
outputs.columnconfigure(0, weight=1)

var_out_zaklad = tk.StringVar()
var_out_dph = tk.StringVar()
var_out_celkem = tk.StringVar()

def out_row(parent, r, label, var, copy_label):
    ttk.Label(parent, text=label).grid(row=r, column=0, sticky="w")
    e = ttk.Entry(parent, textvariable=var, width=22, state="readonly")
    e.grid(row=r, column=1, sticky="w", padx=(10, 0))
    ttk.Button(parent, text="Kopírovat", command=lambda: kopiruj(var, copy_label)).grid(row=r, column=2, padx=(10, 0))
    return e

out_row(outputs, 0, "Základ", var_out_zaklad, "Základ")
out_row(outputs, 1, "DPH", var_out_dph, "DPH")
out_row(outputs, 2, "Celkem", var_out_celkem, "Celkem")

ttk.Button(outputs, text="Kopírovat vše", command=kopiruj_vse).grid(row=3, column=0, columnspan=3, sticky="w", pady=(10, 0))

# Enter spustí výpočet
root.bind("<Return>", lambda e: vypocitej())
entry_in_zaklad.focus_set()

# Auto velikost + minsize, aby se neřezalo
root.update_idletasks()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()