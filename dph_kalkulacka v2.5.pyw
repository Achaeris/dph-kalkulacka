import tkinter as tk
from tkinter import messagebox

APP_NAME = "DPH kalkulačka v2.5 (12 % / 21 %)"
APP_VERSION = "2.5"
AUTHOR = "Dariusz Zabdyr (Darek)"

def parse_amount(text: str) -> float | None:
    t = text.strip()
    if not t:
        return None
    t = t.replace("\u00A0", "").replace(" ", "").replace(",", ".")
    return float(t)

def fmt_num(x: float) -> str:
    # formát bez měny, ať se to dobře kopíruje do faktur a Excelu
    return f"{x:.2f}".replace(".", ",")

def set_readonly(entry: tk.Entry, value: str):
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, value)
    entry.config(state="readonly")

def copy_to_clipboard(text: str):
    root.clipboard_clear()
    root.clipboard_append(text)

def vypocitej():
    try:
        sazba = float(var_sazba.get())  # 0.12 nebo 0.21
        zaklad = parse_amount(entry_in_zaklad.get())
        celkem = parse_amount(entry_in_celkem.get())

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

        set_readonly(entry_out_zaklad, fmt_num(zaklad))
        set_readonly(entry_out_dph, fmt_num(dph))
        set_readonly(entry_out_celkem, fmt_num(celkem))

        label_info.config(text=f"{mode} | Sazba {int(sazba*100)} %")

    except ValueError:
        messagebox.showerror("Chyba", "Zadej prosím platné číslo, může být i s čárkou.")

def vycisti():
    entry_in_zaklad.delete(0, tk.END)
    entry_in_celkem.delete(0, tk.END)
    set_readonly(entry_out_zaklad, "")
    set_readonly(entry_out_dph, "")
    set_readonly(entry_out_celkem, "")
    label_info.config(text="")
    entry_in_zaklad.focus_set()

def kopiruj_zaklad():
    v = entry_out_zaklad.get().strip()
    if not v:
        messagebox.showinfo("Info", "Nejdřív něco vypočítej 🙂")
        return
    copy_to_clipboard(v)
    messagebox.showinfo("Zkopírováno", "Základ je v schránce.")

def kopiruj_dph():
    v = entry_out_dph.get().strip()
    if not v:
        messagebox.showinfo("Info", "Nejdřív něco vypočítej 🙂")
        return
    copy_to_clipboard(v)
    messagebox.showinfo("Zkopírováno", "DPH je v schránce.")

def kopiruj_celkem():
    v = entry_out_celkem.get().strip()
    if not v:
        messagebox.showinfo("Info", "Nejdřív něco vypočítej 🙂")
        return
    copy_to_clipboard(v)
    messagebox.showinfo("Zkopírováno", "Celkem je v schránce.")

def kopiruj_vse():
    z = entry_out_zaklad.get().strip()
    d = entry_out_dph.get().strip()
    c = entry_out_celkem.get().strip()
    if not (z and d and c):
        messagebox.showinfo("Info", "Nejdřív něco vypočítej 🙂")
        return
    text = f"Základ {z} | DPH {d} | Celkem {c}"
    copy_to_clipboard(text)
    messagebox.showinfo("Zkopírováno", "Celý výsledek je v schránce.")

def show_help():
    messagebox.showinfo(
        "Pomoc",
        "Vyplň buď Základ bez DPH nebo Celkem s DPH.\n"
        "Vyber sazbu 12 % nebo 21 % a klikni Vypočítat.\n\n"
        "Výsledky se objeví dole ve třech polích.\n"
        "Každé pole má vlastní tlačítko Kopírovat."
    )

def about_app():
    messagebox.showinfo("O aplikaci", f"{APP_NAME}\nVerze: {APP_VERSION}")

def about_author():
    messagebox.showinfo("O autorovi", f"Autor: {AUTHOR}\nVytvořeno v Pythonu (Tkinter).")

root = tk.Tk()
root.title(APP_NAME)
root.resizable(False, False)
root.geometry("700x360")

menubar = tk.Menu(root)
help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="Pomoc", command=show_help)
help_menu.add_separator()
help_menu.add_command(label="O aplikaci", command=about_app)
help_menu.add_command(label="O autorovi", command=about_author)
menubar.add_cascade(label="Nápověda", menu=help_menu)
root.config(menu=menubar)

frame = tk.Frame(root, padx=12, pady=12)
frame.pack(fill="both", expand=True)

tk.Label(frame, text="Základ bez DPH").grid(row=0, column=0, sticky="w")
entry_in_zaklad = tk.Entry(frame, width=26)
entry_in_zaklad.grid(row=1, column=0, sticky="w", pady=(4, 10))

tk.Label(frame, text="Celkem s DPH").grid(row=0, column=1, sticky="w", padx=(12, 0))
entry_in_celkem = tk.Entry(frame, width=26)
entry_in_celkem.grid(row=1, column=1, sticky="w", padx=(12, 0), pady=(4, 10))

tk.Label(frame, text="Sazba DPH").grid(row=2, column=0, sticky="w", pady=(6, 0))
var_sazba = tk.StringVar(value="0.21")
radios = tk.Frame(frame)
radios.grid(row=3, column=0, sticky="w", pady=(4, 10))
tk.Radiobutton(radios, text="12 %", variable=var_sazba, value="0.12").pack(side="left", padx=(0, 12))
tk.Radiobutton(radios, text="21 %", variable=var_sazba, value="0.21").pack(side="left")

btns = tk.Frame(frame)
btns.grid(row=3, column=1, sticky="e", padx=(12, 0), pady=(4, 10))
tk.Button(btns, text="Vypočítat", command=vypocitej, width=12).pack(side="left", padx=(0, 8))
tk.Button(btns, text="Vyčistit", command=vycisti, width=10).pack(side="left")

label_info = tk.Label(frame, text="", font=("Segoe UI", 9))
label_info.grid(row=4, column=0, columnspan=2, sticky="w", pady=(6, 8))

tk.Label(frame, text="Výsledky").grid(row=5, column=0, sticky="w")

out = tk.Frame(frame)
out.grid(row=6, column=0, columnspan=2, sticky="w")

tk.Label(out, text="Základ").grid(row=0, column=0, sticky="w")
entry_out_zaklad = tk.Entry(out, width=18, state="readonly")
entry_out_zaklad.grid(row=1, column=0, sticky="w", pady=(4, 10))
tk.Button(out, text="Kopírovat", command=kopiruj_zaklad, width=10).grid(row=1, column=1, padx=(8, 18), pady=(4, 10))

tk.Label(out, text="DPH").grid(row=0, column=2, sticky="w")
entry_out_dph = tk.Entry(out, width=18, state="readonly")
entry_out_dph.grid(row=1, column=2, sticky="w", pady=(4, 10))
tk.Button(out, text="Kopírovat", command=kopiruj_dph, width=10).grid(row=1, column=3, padx=(8, 18), pady=(4, 10))

tk.Label(out, text="Celkem").grid(row=0, column=4, sticky="w")
entry_out_celkem = tk.Entry(out, width=18, state="readonly")
entry_out_celkem.grid(row=1, column=4, sticky="w", pady=(4, 10))
tk.Button(out, text="Kopírovat", command=kopiruj_celkem, width=10).grid(row=1, column=5, padx=(8, 0), pady=(4, 10))

tk.Button(frame, text="Kopírovat vše", command=kopiruj_vse, width=14).grid(row=7, column=0, sticky="w", pady=(6, 0))

entry_in_zaklad.focus_set()
root.bind("<Return>", lambda e: vypocitej())
root.mainloop()