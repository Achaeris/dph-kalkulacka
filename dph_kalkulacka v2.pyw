import tkinter as tk
from tkinter import messagebox

APP_NAME = "DPH kalkulačka v2 (12 % / 21 %)"
APP_VERSION = "2.0"
AUTHOR = "Dariusz Zabdyr (Darek)"

def parse_amount(text: str) -> float | None:
    t = text.strip()
    if not t:
        return None
    t = t.replace(" ", "").replace("\u00A0", "").replace(",", ".")
    return float(t)

def fmt_kc(x: float) -> str:
    return f"{x:,.2f} Kč".replace(",", " ")

def vypocitej():
    try:
        sazba = float(var_sazba.get())  # 0.12 / 0.21
        zaklad = parse_amount(entry_zaklad.get())
        celkem = parse_amount(entry_celkem.get())

        if zaklad is None and celkem is None:
            messagebox.showinfo("Info", "Vyplň buď Základ bez DPH, nebo Celkem s DPH.")
            return

        if zaklad is not None and celkem is not None:
            messagebox.showwarning("Pozor", "Vyplň jen jedno pole (Základ nebo Celkem).")
            return

        if zaklad is not None:
            if zaklad < 0:
                raise ValueError
            dph = zaklad * sazba
            celkem = zaklad + dph
            mode = "Zadaný základ bez DPH"

        else:
            if celkem < 0:
                raise ValueError
            zaklad = celkem / (1.0 + sazba)
            dph = celkem - zaklad
            mode = "Zadané celkem s DPH"

        label_vysledek.config(
            text=(
                f"{mode}\n"
                f"Sazba: {int(sazba*100)} %\n"
                f"Základ: {fmt_kc(zaklad)}\n"
                f"DPH: {fmt_kc(dph)}\n"
                f"Celkem: {fmt_kc(celkem)}"
            )
        )

        root.clipboard_clear()
        root.clipboard_append(
            f"Sazba {int(sazba*100)}% | Základ {zaklad:.2f} | DPH {dph:.2f} | Celkem {celkem:.2f}"
        )

    except ValueError:
        messagebox.showerror("Chyba", "Zadej prosím platné číslo (může být i s čárkou).")

def vycisti():
    entry_zaklad.delete(0, tk.END)
    entry_celkem.delete(0, tk.END)
    label_vysledek.config(text="")
    entry_zaklad.focus_set()

def kopiruj():
    txt = label_vysledek.cget("text").strip()
    if not txt:
        messagebox.showinfo("Info", "Nejdřív něco vypočítej 🙂")
        return
    root.clipboard_clear()
    root.clipboard_append(txt.replace("\n", " | "))
    messagebox.showinfo("Zkopírováno", "Výsledek je v schránce.")

def show_help():
    messagebox.showinfo(
        "Pomoc",
        "Jak používat:\n"
        "Vyplň buď:\n"
        "• Základ bez DPH  → spočítá DPH a Celkem\n"
        "nebo\n"
        "• Celkem s DPH    → spočítá Základ a DPH\n\n"
        "Sazbu vyber 12 % nebo 21 %.\n"
        "Enter spustí výpočet."
    )

def about_app():
    messagebox.showinfo("O aplikaci", f"{APP_NAME}\nVerze: {APP_VERSION}")

def about_author():
    messagebox.showinfo("O autorovi", f"Autor: {AUTHOR}\nVytvořeno v Pythonu (Tkinter).")

root = tk.Tk()
root.title(APP_NAME)
root.resizable(False, False)
root.geometry("420x330")

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

tk.Label(frame, text="Základ bez DPH:").grid(row=0, column=0, sticky="w")
entry_zaklad = tk.Entry(frame, width=30)
entry_zaklad.grid(row=1, column=0, sticky="w", pady=(4, 10))

tk.Label(frame, text="Celkem s DPH:").grid(row=2, column=0, sticky="w")
entry_celkem = tk.Entry(frame, width=30)
entry_celkem.grid(row=3, column=0, sticky="w", pady=(4, 12))

tk.Label(frame, text="Sazba DPH:").grid(row=4, column=0, sticky="w")
var_sazba = tk.StringVar(value="0.21")
radios = tk.Frame(frame)
radios.grid(row=5, column=0, sticky="w", pady=(4, 12))
tk.Radiobutton(radios, text="12 %", variable=var_sazba, value="0.12").pack(side="left", padx=(0, 12))
tk.Radiobutton(radios, text="21 %", variable=var_sazba, value="0.21").pack(side="left")

btns = tk.Frame(frame)
btns.grid(row=6, column=0, sticky="w")
tk.Button(btns, text="Vypočítat", command=vypocitej, width=12).pack(side="left", padx=(0, 8))
tk.Button(btns, text="Vyčistit", command=vycisti, width=10).pack(side="left", padx=(0, 8))
tk.Button(btns, text="Kopírovat", command=kopiruj, width=10).pack(side="left")

label_vysledek = tk.Label(frame, text="", justify="left", font=("Segoe UI", 10))
label_vysledek.grid(row=7, column=0, sticky="w", pady=(14, 0))

entry_zaklad.focus_set()
root.bind("<Return>", lambda e: vypocitej())
root.mainloop()