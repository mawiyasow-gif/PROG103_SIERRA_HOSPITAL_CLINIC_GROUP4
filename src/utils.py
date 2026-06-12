from datetime import datetime
import tkinter as tk
from tkinter import ttk
from logic import *

# DESIGN TOKENS
BLUE_DARK="#0d3b6e"; BLUE_MID="#1a6eab"; TEAL="#0e7c7b"; AMBER="#d4860a"; RED_DARK="#b5281c"; GREY_BTN="#5a6878"
BG="#eef2f7"; CARD="#ffffff"; SEP="#c3cdd8"
ROW_ODD="#f4f8fe"; ROW_EVEN="#dde9f7"; TAG_EMERG="#fce4e4"; TAG_PREG="#daeaf9"; TAG_NEXT="#d6f5e3"
FONT_TITLE=("Helvetica",17,"bold"); FONT_HEAD=("Helvetica",13,"bold"); FONT_BODY=("Helvetica",10)
FONT_SMALL=("Helvetica",9); FONT_BOLD=("Helvetica",10,"bold")
CLINIC_NAME = "Sierra Health Hospital Clinic"
TAGLINE = "Your health is Our Priority  manage appointments,\nmonitor and receive quality health services with Ease"
QUEUE_COLS = ("#","ID","Name","Age","Gender","Category","Arrived","Complaint")
QUEUE_WIDTHS = [45,80,160,50,75,110,80,160]
SEARCH_COLS = ("ID","Name","Age","Gender","Phone","Category","Arrived","Complaint","Status")
SEARCH_WIDTHS = [75,145,50,70,105,105,78,145,70]

# REUSABLE WIDGET BUILDERS
def flat_btn(parent, text, bg, command, width=22, pady=6):
    b = tk.Button(parent, text=text, bg=bg, fg="#070A0B", font=FONT_BOLD, relief="flat", bd=0,
        cursor="hand2", activebackground=bg, activeforeground="#ffffff", width=width, pady=pady, command=command)
    darker = _darken(bg)
    b.bind("<Enter>", lambda e: b.config(bg=darker)); b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b

def _darken(hex_color, amount=20):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r, g, b = max(0, r-amount), max(0, g-amount), max(0, b-amount)
    return f"#{r:02x}{g:02x}{b:02x}"

def divider(parent, padx=10, pady=4):
    tk.Frame(parent, bg=SEP, height=1).pack(fill="x", padx=padx, pady=pady)

def build_treeview(parent, cols, widths, height=12, tag="T"):
    style = ttk.Style(); style.theme_use("clam")
    sname = f"{tag}.Treeview"
    style.configure(f"{sname}.Heading", background=BLUE_DARK, foreground="white", font=FONT_BOLD, relief="flat", padding=4)
    style.map(f"{sname}.Heading", background=[("active", BLUE_MID)])
    style.configure(sname, rowheight=27, font=FONT_BODY, background=CARD, fieldbackground=CARD, foreground="#1a1a1a")
    style.map(sname, background=[("selected", BLUE_MID)], foreground=[("selected", "white")])
    outer = tk.Frame(parent, bg=BG)
    tree = ttk.Treeview(outer, columns=cols, show="headings", height=height, style=sname)
    for col, w in zip(cols, widths):
        tree.heading(col, text=col); tree.column(col, width=w, anchor="center", minwidth=45, stretch=True)
    sb = ttk.Scrollbar(outer, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=sb.set); tree.pack(side="left", fill="both", expand=True); sb.pack(side="left", fill="y")
    return outer, tree

def build_search_view(win, tag, prompt, empty_text, unit):
    """Shared live-search table (used by Patient Info and Search Patient)."""
    bar = tk.Frame(win, bg=BG); bar.pack(fill="x", padx=12)
    tk.Label(bar, text=prompt, font=FONT_BOLD, bg=BG).pack(side="left", padx=(0, 8))
    sv = tk.StringVar()
    tk.Entry(bar, textvariable=sv, width=36, font=FONT_BODY, relief="solid", bd=1).pack(side="left")
    fr, tree = build_treeview(win, SEARCH_COLS, SEARCH_WIDTHS, height=13, tag=tag)
    fr.pack(fill="both", expand=True, padx=10, pady=8)
    tree.column("Name", anchor="w", stretch=True); tree.column("Complaint", anchor="w", stretch=True)
    info_lbl = tk.Label(win, text=empty_text, font=FONT_SMALL, bg=BG, fg=GREY_BTN)
    info_lbl.pack(anchor="w", padx=14)

    def do_search(*_):
        term = sv.get().strip(); tree.delete(*tree.get_children())
        if not term:
            info_lbl.config(text=empty_text); return
        res = search_all(term)
        for p in res:
            status = "Waiting" if p in patients else "Served"
            tree.insert("", "end", values=(p["id"],p["name"],p["age"],p["gender"],p["phone"],p["category"],p["arrived"],p["complaint"],status))
        info_lbl.config(text=(f"{len(res)} {unit}(s) found." if res else f"No records matched '{term}'."))

    sv.trace_add("write", do_search)
    return tree

def build_queue_table(win, tag):
    """Shared waiting-queue table (used by Attend-to-Patients and Live Queue)."""
    fr, tree = build_treeview(win, QUEUE_COLS, QUEUE_WIDTHS, height=14, tag=tag)
    fr.pack(fill="both", expand=True, padx=10, pady=8)
    tree.column("Name", anchor="w", stretch=True); tree.column("Complaint", anchor="w", stretch=True)
    tree.tag_configure("next", background=TAG_NEXT, foreground="#0a4020")
    tree.tag_configure("emerg", background=TAG_EMERG, foreground="#6b1212")
    tree.tag_configure("preg", background=TAG_PREG, foreground="#0d3060")
    tk.Label(win, text="Legend:   Green = Next in line     Red = Emergency     Blue = Pregnant",
             font=FONT_SMALL, bg=BG, fg=GREY_BTN).pack(anchor="w", padx=12)
    return tree

def refresh_queue(tree):
    tree.delete(*tree.get_children())
    if not patients:
        tree.insert("", "end", values=("","","  No patients waiting","","","","","")); return
    for i, p in enumerate(patients, 1):
        tag = "next" if i==1 else "emerg" if p["category"]=="Emergency" else "preg" if p["category"]=="Pregnant" else ""
        tree.insert("", "end", values=(i,p["id"],p["name"],p["age"],p["gender"],p["category"],p["arrived"],p["complaint"]), tags=(tag,))
