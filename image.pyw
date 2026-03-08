from PIL import Image, ImageDraw, ImageFont
import os, math

# Create a clean app icon for "DPH Kalkulačka" (VAT calculator)
size = 1024
img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Colors (kept neutral; not using matplotlib style constraints here)
bg = (22, 24, 29, 255)          # dark slate
panel = (33, 36, 44, 255)       # slightly lighter
accent = (255, 255, 255, 255)   # white
accent2 = (180, 190, 205, 255)  # cool gray
green = (90, 210, 120, 255)     # subtle green for % / VAT vibe

# Rounded background
radius = 200
draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=bg)

# Calculator body
body_margin = 150
body = [body_margin, body_margin, size - body_margin, size - body_margin]
draw.rounded_rectangle(body, radius=140, fill=panel)

# Screen
screen = [body_margin + 90, body_margin + 90, size - body_margin - 90, body_margin + 290]
draw.rounded_rectangle(screen, radius=70, fill=(17, 19, 23, 255))
# Screen shine line
draw.rounded_rectangle([screen[0]+30, screen[1]+30, screen[2]-30, screen[1]+70], radius=25, fill=(40, 45, 55, 180))

# Buttons grid
grid_left = body_margin + 90
grid_top = body_margin + 360
grid_right = size - body_margin - 90
grid_bottom = size - body_margin - 90

cols, rows = 4, 4
gap = 28
btn_w = (grid_right - grid_left - gap*(cols-1)) // cols
btn_h = (grid_bottom - grid_top - gap*(rows-1)) // rows

buttons = []
for r in range(rows):
    for c in range(cols):
        x0 = grid_left + c*(btn_w+gap)
        y0 = grid_top + r*(btn_h+gap)
        x1 = x0 + btn_w
        y1 = y0 + btn_h
        buttons.append((x0, y0, x1, y1))

# Draw buttons with slight depth
for (x0, y0, x1, y1) in buttons:
    draw.rounded_rectangle([x0, y0, x1, y1], radius=45, fill=(24, 27, 33, 255))
    # highlight
    draw.rounded_rectangle([x0+12, y0+12, x1-12, y0+38], radius=18, fill=(50, 55, 66, 120))

# Make one accent button (like "=")
eq = buttons[-1]
draw.rounded_rectangle(eq, radius=45, fill=(18, 92, 62, 255))
draw.rounded_rectangle([eq[0]+12, eq[1]+12, eq[2]-12, eq[1]+38], radius=18, fill=(255, 255, 255, 70))

# Add "%" symbol in middle button area
# Choose a central button (row 1 col 2)
pct_btn = buttons[1*cols + 2]
draw.rounded_rectangle(pct_btn, radius=45, fill=(28, 31, 38, 255))
draw.rounded_rectangle([pct_btn[0]+12, pct_btn[1]+12, pct_btn[2]-12, pct_btn[1]+38], radius=18, fill=(70, 78, 92, 120))

# Load font
def load_font(sz):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(path):
            return ImageFont.truetype(path, sz)
    return ImageFont.load_default()

font_dph = load_font(120)
font_pct = load_font(140)

# Write "DPH" on screen
text = "DPH"
tw, th = draw.textbbox((0,0), text, font=font_dph)[2:]
sx = (screen[0] + screen[2] - tw)//2
sy = (screen[1] + screen[3] - th)//2 - 5
draw.text((sx, sy), text, font=font_dph, fill=accent)

# Write "%" on button
pct = "%"
ptw, pth = draw.textbbox((0,0), pct, font=font_pct)[2:]
px = (pct_btn[0] + pct_btn[2] - ptw)//2
py = (pct_btn[1] + pct_btn[3] - pth)//2 - 10
draw.text((px, py), pct, font=font_pct, fill=green)

# Draw "=" on eq button
font_eq = load_font(130)
eq_text = "="
etw, eth = draw.textbbox((0,0), eq_text, font=font_eq)[2:]
ex = (eq[0] + eq[2] - etw)//2
ey = (eq[1] + eq[3] - eth)//2 - 10
draw.text((ex, ey), eq_text, font=font_eq, fill=(240,255,245,255))

# Save PNG
png_path = "/mnt/data/dph_kalkulacka_icon.png"
img.save(png_path)

# Save ICO with multiple sizes
ico_path = "/mnt/data/dph_kalkulacka_icon.ico"
sizes = [(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)]
img.save(ico_path, format="ICO", sizes=sizes)

png_path, ico_path, os.path.getsize(ico_path)
