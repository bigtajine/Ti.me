#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ti.me – Vista-style clock widget.
Shows analog clock + time and date. Uses your system’s local time.
Author: BigTajine
"""

from ctypes import windll
from datetime import datetime
import math
import tkinter as tk
from tkinter import font as tkFont

try:
    windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    pass

# Vista-style (dark glass)
BG_COLOR = "#1a2332"
BG_ALPHA = 0.92
FACE_BG = "#0d1117"
RIM_COLOR = "#3d4f5f"
TICK_COLOR = "#8b9cad"
HAND_HOUR = "#e8eaed"
HAND_MINUTE = "#e8eaed"
HAND_SECOND = "#c5221f"
TEXT_COLOR = "#e0e6ed"
TEXT_DIM = "#8b9cad"

app = tk.Tk()
ratio = app.winfo_screenwidth() / 2560
width = max(160, int(ratio * 180))
height = max(180, int(ratio * 200))

app.title("Ti.me")
app.attributes("-topmost", True)
app.attributes("-alpha", BG_ALPHA)
app.configure(bg=BG_COLOR)
app.resizable(False, False)
app.geometry(f"{width}x{height}")
try:
    app.iconbitmap("time.ico")
except Exception:
    pass

app.option_add("*Background", BG_COLOR)
app.option_add("*Foreground", TEXT_COLOR)


def set_rounded_region(widget, radius=12):
    try:
        hwnd = widget.winfo_id()
        r = min(radius, width // 2, height // 2)
        region = windll.gdi32.CreateRoundRectRgn(0, 0, width + 1, height + 1, r, r)
        windll.user32.SetWindowRgn(hwnd, region, 1)
    except Exception:
        pass


clock_center_x = width // 2
clock_center_y = 58
clock_radius = 44


def tick():
    canvas.delete("face")
    canvas.delete("ticks")
    canvas.delete("hands")
    cx, cy, r = clock_center_x, clock_center_y, clock_radius
    now = datetime.now()
    sec = now.second + now.microsecond / 1e6
    min_ = now.minute + sec / 60
    hour = (now.hour % 12) + min_ / 60

    canvas.create_oval(cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2, fill=FACE_BG, outline=RIM_COLOR, width=2, tags="face")
    for i in range(12):
        angle = (i * 30 - 90) * math.pi / 180
        inner_r = r - 12 if i % 3 == 0 else r - 8
        x1 = cx + inner_r * math.cos(angle)
        y1 = cy + inner_r * math.sin(angle)
        x2 = cx + (r - 2) * math.cos(angle)
        y2 = cy + (r - 2) * math.sin(angle)
        canvas.create_line(x1, y1, x2, y2, fill=TICK_COLOR, width=2 if i % 3 == 0 else 1, tags="ticks")
    for angle_deg, hand_r, color, w in [
        (sec * 6 - 90, r - 10, HAND_SECOND, 1),
        (min_ * 6 - 90, r - 14, HAND_MINUTE, 2),
        (hour * 30 - 90, r - 26, HAND_HOUR, 3),
    ]:
        rad = angle_deg * math.pi / 180
        canvas.create_line(cx, cy, cx + hand_r * math.cos(rad), cy + hand_r * math.sin(rad), fill=color, width=w, tags="hands")

    bottom_label.config(text=now.strftime("%H:%M  %a, %d %b"))
    app.after(200, tick)


# Analog clock
canvas = tk.Canvas(app, width=width, height=clock_center_y + clock_radius + 6, bg=BG_COLOR, highlightthickness=0)
canvas.pack(pady=(8, 4))

# One line: time + date
font_name = "Segoe UI" if "Segoe UI" in tkFont.families() else "TkDefaultFont"
bottom_label = tk.Label(app, text="--:--  ---, -- ---", font=(font_name, 10), fg=TEXT_DIM, bg=BG_COLOR)
bottom_label.pack(pady=(0, 10))

app.after(0, tick)
app.update_idletasks()
app.after(50, lambda: set_rounded_region(app))
app.mainloop()
