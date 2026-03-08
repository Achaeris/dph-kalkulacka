# DPH kalkulačka

Malá desktopová aplikace v Pythonu, kterou jsem vytvořil jako praktickou pomůcku a zároveň jako trénink programování.  
Počítá DPH pro sazby **12 %** a **21 %**. Umí pracovat se **základem bez DPH** s **částkou celkem s DPH**.

**EN (short):** VAT calculator (CZ rates 12%/21%) built with Python Tkinter/ttk.
A small desktop app written in Python. Built as a practical tool and as a learning project.  
Calculates VAT using Czech rates **12%** and **21%**. Supports calculation from **net amount** or **gross amount**.

## Funkce
- Sazby: 12 %/21 %
- Výpočet ze základu bez DPH nebo z částky celkem s DPH
- Výstupy zvlášť: **Základ**, **DPH**, **Celkem**
- Kopírování do schránky (každé pole zvlášť+ Kopírovat vše)
- Nastavení: možnost vypnout potvrzovací hlášky po kopírování (uloží se)

## Spuštění (Windows/macOS/Linux)
Požadavky: Python 3.12+ (testováno na 3.14)

### Windows
```bash
python dph_kalkulacka_v3_xx.pyw
```

### macOS / Linux
```bash
python3 dph_kalkulacka_v3_xx.pyw
```

**Poznámka pro Linux:** pokud chybí Tkinter, doinstaluj balík `python3-tk`  
- Debian/Ubuntu: `sudo apt install python3-tk`  
- Fedora: `sudo dnf install python3-tk`

## Build do EXE (Windows)
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole dph_kalkulacka_v3_xx.pyw
```

Výstup je ve složce `dist/`.

## Licence
MIT License
