import tkinter as tk
from tkinter import messagebox
# import ttkbootstrap as ttk

from logic import *
from utils import *

def std_window(parent, title, geom, subtitle, heading=None, head_color=BLUE_DARK, div_pad=4, grab=False):
    """Common Toplevel + header bar + optional heading + divider, used by every sub-window."""
    win = tk.Toplevel(parent); win.title(title); win.geometry(geom); win.configure(bg=BG)
    if grab: win.grab_set()
    header_bar(win, subtitle)
    if heading:
        tk.Label(win, text=heading, font=FONT_HEAD, bg=BG, fg=head_color).pack(pady=(12, 2))
    divider(win, pady=(0, div_pad))
    return win


def login_window(root, on_success):
    win = tk.Toplevel(root); win.title("Staff Login"); win.geometry("520x560")
    win.configure(bg=BG); win.grab_set(); win.resizable(False, False)

    tk.Frame(win, bg=BLUE_DARK, height=6).pack(fill="x")
    tk.Label(win, text="Sierra Health", font=("Helvetica",36,"bold"), bg=BG, fg=BLUE_DARK).pack(pady=(22,2))
    tk.Label(win, text=CLINIC_NAME, font=("Helvetica",13,"bold"), bg=BG, fg=BLUE_DARK).pack()
    tk.Label(win, text="Staff Login", font=("Helvetica",11), bg=BG, fg=GREY_BTN).pack(pady=(4,6))
    divider(win, padx=30, pady=10)

    frm = tk.Frame(win, bg=BG, padx=44); frm.pack(fill="both", expand=True)

    def lbl(row, text):
        tk.Label(frm, text=text, font=FONT_BOLD, bg=BG, anchor="w").grid(row=row, column=0, sticky="w", pady=9)

    def ent(row, var, show=""):
        e = tk.Entry(frm, textvariable=var, width=30, font=FONT_BODY, show=show, relief="solid", bd=1)
        e.grid(row=row, column=1, pady=9, padx=(12,0)); return e

    role_var = tk.StringVar(value="Receptionist"); pw_var = tk.StringVar(); cf_var = tk.StringVar()

    lbl(0, "Role:")
    role_box = ttk.Combobox(frm, textvariable=role_var, width=28, state="readonly", font=FONT_BODY, values=["Doctor","Receptionist"])
    role_box.grid(row=0, column=1, pady=9, padx=(12,0))

    lbl(1, "Password:")
    pw_ent = ent(1, pw_var, show="*")

    cf_lbl_widget = tk.Label(frm, text="Confirm:", font=FONT_BOLD, bg=BG, anchor="w")
    cf_ent_widget = tk.Entry(frm, textvariable=cf_var, width=30, font=FONT_BODY, show="*", relief="solid", bd=1)

    hint = tk.Label(frm, text="", font=FONT_SMALL, bg=BG, fg=BLUE_MID, wraplength=340)
    hint.grid(row=3, column=0, columnspan=2, pady=2)
    err = tk.Label(frm, text="", font=FONT_SMALL, bg=BG, fg=RED_DARK, wraplength=340)
    err.grid(row=4, column=0, columnspan=2, pady=2)

    def refresh_form(*_):
        role = role_var.get(); err.config(text=""); pw_var.set(""); cf_var.set("")
        if passwords[role] is None:
            hint.config(text=f"No password set for {role}. Create one now (min 4 chars).")
            cf_lbl_widget.grid(row=2, column=0, sticky="w", pady=9); cf_ent_widget.grid(row=2, column=1, pady=9, padx=(12,0))
        else:
            hint.config(text=f"Enter your {role} password to continue.")
            cf_lbl_widget.grid_remove(); cf_ent_widget.grid_remove()

    role_var.trace_add("write", refresh_form); refresh_form()

    def attempt():
        role = role_var.get(); pw = pw_var.get(); err.config(text="")
        if not pw:
            err.config(text="Password cannot be empty."); return
        if passwords[role] is None:
            if len(pw) < 4:
                err.config(text="Password must be at least 4 characters."); return
            if pw != cf_var.get():
                err.config(text="Passwords do not match."); return
            passwords[role] = pw
            messagebox.showinfo("Password Created", f"Password for {role} has been set.\nRemember it as it cannot be recovered.")
            win.destroy(); on_success(role)
        else:
            if pw == passwords[role]:
                win.destroy(); on_success(role)
            else:
                err.config(text="Incorrect password. Please try again."); pw_var.set("")

    flat_btn(frm, "Login", BLUE_DARK, attempt, width=28, pady=10).grid(row=5, column=0, columnspan=2, pady=16)
    pw_ent.bind("<Return>", lambda e: attempt()); cf_ent_widget.bind("<Return>", lambda e: attempt())
def header_bar(win, subtitle=""):
    bar = tk.Frame(win, bg=BLUE_DARK); bar.pack(fill="x")
    tk.Label(bar, text=CLINIC_NAME, font=("Helvetica",12,"bold"), bg=BLUE_DARK, fg="#ffffff").pack(side="left", padx=14, pady=9)
    if subtitle:
        tk.Label(bar, text=f"|  {subtitle}", font=FONT_BODY, bg=BLUE_DARK, fg="#90bce8").pack(side="left")
    clk = tk.Label(bar, text="", font=FONT_BODY, bg=BLUE_DARK, fg="#90bce8"); clk.pack(side="right", padx=14)
    def _tick():
        clk.config(text=datetime.now().strftime("%A  %H:%M:%S")); win.after(1000, _tick)
    _tick(); return bar


# DOCTOR  ATTEND TO PATIENTS
def open_attend(parent):
    win = std_window(parent, "Attend to Patients", "1150x660", "Attend to Patients", "Waiting Queue")
    tree = build_queue_table(win, "Attend")

    def refresh(): refresh_queue(tree)

    def do_call_next():
        if not patients:
            messagebox.showinfo("Queue Empty", "There are no patients waiting."); return
        p = patients[0]
        if not messagebox.askyesno("Confirm", f"Attend to this patient?\n\nName      : {p['name']}\nCategory  : {p['category']}\nComplaint : {p['complaint']}"): return
        called = call_next()
        nxt = f"Next up: {patients[0]['name']}  ({patients[0]['category']})" if patients else "Queue is now empty."
        messagebox.showinfo("Now Attending",
            f"NOW ATTENDING\nPatient   : {called['name'].upper()}\nTicket    : {called['queue_no']}\n"
            f"Category  : {called['category']}\nComplaint : {called['complaint']}\n\n{nxt}")
        refresh()

    btn_row = tk.Frame(win, bg=BG); btn_row.pack(pady=10)
    flat_btn(btn_row, "Call Next Patient", TEAL, do_call_next, 22).pack(side="left", padx=6)
    flat_btn(btn_row, "Refresh", BLUE_MID, refresh, 14).pack(side="left", padx=6)
    flat_btn(btn_row, "Close", GREY_BTN, win.destroy, 10).pack(side="left", padx=6)
    refresh()
# DOCTOR  VIEW PATIENT INFO
def open_patient_info(parent):
    win = std_window(parent, "Patient Information", "1150x640", "View Patient Info", "Patient Information", div_pad=8)
    build_search_view(win, "Info", "Search (Name / ID / Phone):", "Type a name, patient ID, or phone number to search", "result")
    flat_btn(win, "Close", GREY_BTN, win.destroy, 10).pack(pady=8)

"""ALIMU CODE"""

"""KAI CODE"""
