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
        tk.Label(frm, text=text, font=FONT_BOLD, bg=BG,).grid(row=row, column=0, sticky="e", pady=9)

    def ent(row, var, show=""):
        e = tk.Entry(frm, textvariable=var, width=30, font=FONT_BODY, show=show, relief="solid", bd=1)
        e.grid(row=row, column=1, pady=9, padx=(12,0)); return e

    role_var = tk.StringVar(value="Receptionist"); pw_var = tk.StringVar(); cf_var = tk.StringVar()

    lbl(0, "Role:")
    role_box = ttk.Combobox(frm, textvariable=role_var, width=28, state="readonly", font=FONT_BODY, values=["Doctor","Receptionist"])
    role_box.grid(row=0, column=1, pady=9, padx=(12,0))

    lbl(1, "Password:")
    pw_ent = ent(1, pw_var, show="*")

    cf_lbl_widget = tk.Label(frm, text="Confirm:", font=FONT_BOLD, bg=BG,)
    cf_ent_widget = tk.Entry(frm, textvariable=cf_var, width=30, font=FONT_BODY, show="*", relief="solid", bd=1)

    hint = tk.Label(frm, text="", font=FONT_SMALL, bg=BG, fg=BLUE_MID, wraplength=340)
    hint.grid(row=3, column=0, columnspan=2, pady=2)
    err = tk.Label(frm, text="", font=FONT_SMALL, bg=BG, fg=RED_DARK, wraplength=340)
    err.grid(row=4, column=0, columnspan=2, pady=2)

    def refresh_form(*_):
        role = role_var.get(); err.config(text=""); pw_var.set(""); cf_var.set("")
        if passwords[role] is None:
            hint.config(text=f"No password set for {role}. Create one now (min 4 chars).")
            cf_lbl_widget.grid(row=2, column=0, sticky="e", pady=9); cf_ent_widget.grid(row=2, column=1, pady=9, padx=(12,0))
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

# DOCTOR  PRESCRIBE MEDICATION
def open_prescriptions(parent):
    win = std_window(parent, "Prescribe Medication", "760x560", "Prescribe Medication", "Prescribe Medication", div_pad=6, grab=True)

    tk.Label(win, text="Select a served patient from the list below:", font=FONT_BODY, bg=BG, fg=GREY_BTN).pack(anchor="w", padx=16)

    list_frame = tk.Frame(win, bg=BG, padx=16); list_frame.pack(fill="x")
    lb = tk.Listbox(list_frame, height=6, font=FONT_BODY, selectmode="single", bg=CARD, relief="solid", bd=1,
        activestyle="dotbox", selectbackground=BLUE_MID, selectforeground="white")
    lb.pack(fill="x", pady=6)

    detail = tk.Frame(win, bg=BG, padx=16); detail.pack(fill="x")
    tk.Label(detail, text="Prescription Notes:", font=FONT_BOLD, bg=BG).pack(anchor="w", pady=(6,2))
    rx_box = tk.Text(detail, height=7, font=FONT_BODY, relief="solid", bd=1, wrap="word", bg=CARD, fg="#1a1a1a")
    rx_box.pack(fill="x")

    err_lbl = tk.Label(win, text="", font=FONT_SMALL, bg=BG, fg=RED_DARK); err_lbl.pack()

    def populate():
        lb.delete(0, "end")
        if not served:
            lb.insert("end", "  (No patients have been served yet)")
        else:
            for p in served:
                rx_flag = "  [Prescribed]" if p.get("prescription") else "  [Pending]"
                lb.insert("end", f"  {p['id']}   {p['name']}   ({p['category']}){rx_flag}")

    def on_select(event=None):
        sel = lb.curselection()
        if not sel or not served: return
        p = served[sel[0]]; rx_box.delete("1.0", "end"); rx_box.insert("end", p.get("prescription","")); err_lbl.config(text="")

    def save():
        sel = lb.curselection()
        if not sel or not served:
            err_lbl.config(text="Please select a patient first."); return
        rx = rx_box.get("1.0", "end").strip()
        if not rx:
            err_lbl.config(text="Prescription notes cannot be empty."); return
        served[sel[0]]["prescription"] = rx
        messagebox.showinfo("Saved", f"Prescription saved for {served[sel[0]]['name']}.")
        err_lbl.config(text=""); populate()

    lb.bind("<<ListboxSelect>>", on_select); populate()

    btn_row = tk.Frame(win, bg=BG); btn_row.pack(pady=10)
    flat_btn(btn_row, "Save Prescription", TEAL, save, 22).pack(side="left", padx=6)
    flat_btn(btn_row, "Refresh List", BLUE_MID, populate, 14).pack(side="left", padx=6)
    flat_btn(btn_row, "Close", GREY_BTN, win.destroy, 10).pack(side="left", padx=6)


# RECEPTIONIST  REGISTER PATIENT
def open_register(parent, on_done):
    win = std_window(parent, "Register Patient", "500x580", "Register Patient", "New Patient Registration", div_pad=8, grab=True)

    frm = tk.Frame(win, bg=BG, padx=24); frm.pack(fill="both", expand=True)

    nv = tk.StringVar(); av = tk.StringVar(); gv = tk.StringVar(value="Male"); pv = tk.StringVar()
    cv = tk.StringVar(); tv = tk.StringVar(value=datetime.now().strftime("%H:%M")); kv = tk.StringVar(value="Normal")

    row = 0
    def label(text):
        nonlocal row
        tk.Label(frm, text=text, font=FONT_BOLD, bg=BG, anchor="w").grid(row=row, column=0, sticky="w", pady=7)

    def entry(var):
        nonlocal row
        e = tk.Entry(frm, textvariable=var, width=30, font=FONT_BODY, relief="solid", bd=1)
        e.grid(row=row, column=1, pady=7, padx=(10,0)); row += 1; return e

    label("Full Name:"); entry(nv)
    label("Age:"); entry(av)

    label("Gender:")
    gf = tk.Frame(frm, bg=BG); gf.grid(row=row, column=1, pady=7, padx=(10,0), sticky="w")
    for g in ["Male","Female","Other"]:
        tk.Radiobutton(gf, text=g, variable=gv, value=g, bg=BG, font=FONT_BODY, activebackground=BG).pack(side="left", padx=5)
    row += 1

    label("Phone Number:"); entry(pv)
    label("Complaint:"); entry(cv)
    label("Arrived (HH:MM):"); entry(tv)

    label("Category:")
    ttk.Combobox(frm, textvariable=kv, width=28, state="readonly", font=FONT_BODY,
                 values=["Emergency","Pregnant","Normal"]).grid(row=row, column=1, pady=7, padx=(10,0))
    row += 1

    err = tk.Label(frm, text="", font=FONT_SMALL, bg=BG, fg=RED_DARK)
    err.grid(row=row, column=0, columnspan=2, pady=4); row += 1

    def submit():
        n=nv.get().strip(); a=av.get().strip(); g=gv.get(); p=pv.get().strip(); c=cv.get().strip(); t=tv.get().strip(); k=kv.get()
        checks = [(ok_name(n),"Name must contain letters only (no numbers)."),
                  (ok_age(a),"Age must be a number between 0 and 120."),
                  (ok_phone(p),"Phone must be 7 to 15 digits."),
                  (ok_note(c),"Please enter a valid complaint (not just numbers)."),
                  (ok_time(t),"Arrival time must be in HH:MM format (e.g. 09:30).")]
        for ok, msg in checks:
            if not ok:
                err.config(text=f"  {msg}"); return
        pid = register_patient(n, int(a), g, p, c, t, k)
        pos = next((i+1 for i, pt in enumerate(patients) if pt["id"]==pid), "?")
        messagebox.showinfo("Patient Registered",
            f"Registration successful!\n\nName       : {n.title()}\nPatient ID : {pid}\nGender     : {g}\n"
            f"Phone      : {p}\nCategory   : {k}\nQueue Pos  : {pos} of {len(patients)}")
        on_done(); win.destroy()

    flat_btn(frm, "Register Patient", TEAL, submit, 24).grid(row=row, column=0, columnspan=2, pady=10)

# RECEPTIONIST  VIEW QUEUE
def open_queue(parent):
    win = std_window(parent, "Live Queue", "1150x660", "Live Queue", "Waiting Queue")
    tree = build_queue_table(win, "Queue")

    def refresh(): refresh_queue(tree)

    btn_row = tk.Frame(win, bg=BG); btn_row.pack(pady=10)
    flat_btn(btn_row, "Refresh", BLUE_MID, refresh, 14).pack(side="left", padx=6)
    flat_btn(btn_row, "Close", GREY_BTN, win.destroy, 10).pack(side="left", padx=6)
    refresh()

# RECEPTIONIST  SEARCH PATIENTS
def open_search(parent):
    win = std_window(parent, "Search Patient", "1150x640", "Search Patients", "Search Patients", div_pad=8)
    build_search_view(win, "Search", "Name / ID / Phone:", "Start typing to search all patients", "record")
    flat_btn(win, "Close", GREY_BTN, win.destroy, 10).pack(pady=8)

# RECEPTIONIST  SERVED PATIENTS
def open_served(parent):
    win = std_window(parent, "Served Patients", "1150x640", "Served Patients",
                      f"Served Today  {len(served)} patient(s)", head_color=TEAL, div_pad=8)
    cols = ("ID","Name","Age","Gender","Phone","Category","Arrived","Complaint")
    widths = [75,145,50,70,105,105,78,160]
    fr, tree = build_treeview(win, cols, widths, height=14, tag="Served"); fr.pack(fill="both", expand=True, padx=10)
    tree.column("Name", anchor="w", stretch=True); tree.column("Complaint", anchor="w", stretch=True)
    tree.tag_configure("odd", background=ROW_ODD, foreground="#1a1a1a")
    tree.tag_configure("even", background=ROW_EVEN, foreground="#1a1a1a")

    if not served:
        tree.insert("", "end", values=("","  No patients served yet","","","","","",""))
    else:
        for i, p in enumerate(served):
            tree.insert("", "end", values=(p["id"],p["name"],p["age"],p["gender"],p["phone"],p["category"],p["arrived"],p["complaint"]),
                         tags=("odd" if i % 2 == 0 else "even",))

    flat_btn(win, "Close", GREY_BTN, win.destroy, 10).pack(pady=10)

# RECEPTIONIST  SUMMARY
def open_summary(parent):
    win = std_window(parent, "Summary", "560x520", "Summary", "Today's Summary", div_pad=10)
    counts = queue_counts()
    fr, tree = build_treeview(win, ("Description","Count"), [330,120], height=10, tag="Summary"); fr.pack(fill="both", expand=True, padx=16)
    tree.column("Description", anchor="w"); tree.column("Count", anchor="center")

    tree.tag_configure("total", background="#e8eef8", foreground="#0d1b4b")
    tree.tag_configure("waiting", background="#fff5d6", foreground="#7d4e00")
    tree.tag_configure("served", background="#d6f5e3", foreground="#0a4020")
    tree.tag_configure("emerg", background=TAG_EMERG, foreground="#6b1212")
    tree.tag_configure("preg", background=TAG_PREG, foreground="#0d3060")
    tree.tag_configure("normal", background="#f0f0f2", foreground="#333")
    tree.tag_configure("next", background=TAG_NEXT, foreground="#0a4020")

    total = len(patients) + len(served)
    tree.insert("", "end", values=("Total Registered Today", total), tags=("total",))
    tree.insert("", "end", values=("Currently Waiting", len(patients)), tags=("waiting",))
    tree.insert("", "end", values=("Already Served", len(served)), tags=("served",))
    tree.insert("", "end", values=("", ""))
    tree.insert("", "end", values=("Emergency in Queue", counts["Emergency"]), tags=("emerg",))
    tree.insert("", "end", values=("Pregnant in Queue", counts["Pregnant"]), tags=("preg",))
    tree.insert("", "end", values=("Normal in Queue", counts["Normal"]), tags=("normal",))
    if patients:
        n = patients[0]
        tree.insert("", "end", values=("", ""))
        tree.insert("", "end", values=(f"Next Patient:   {n['name']}   |   {n['category']}", ""), tags=("next",))

    flat_btn(win, "Close", GREY_BTN, win.destroy, 10).pack(pady=12)

# ROLE DASHBOARDS
def _base_dashboard(root, title, subtitle):
    win = tk.Toplevel(root); win.title(f"{title}  {CLINIC_NAME}"); win.configure(bg=BG)
    try: win.state("zoomed")
    except: win.attributes("-zoomed", True)
    win.minsize(820, 560); header_bar(win, subtitle); return win

def open_doctor_dashboard(root):
    win = _base_dashboard(root, "Doctor", "Doctor Portal"); divider(win)
    tk.Label(win, text="Doctor Dashboard", font=FONT_TITLE, bg=BG, fg=BLUE_DARK).pack(pady=(28,4))
    tk.Label(win, text=TAGLINE, font=("Helvetica",10,"italic"), bg=BG, fg=GREY_BTN, justify="center").pack(pady=(0,20))

    btns = [("Attend to Patients", TEAL, lambda: open_attend(win)),
            ("View Patient Info", BLUE_DARK, lambda: open_patient_info(win)),
            ("Prescribe Medication", BLUE_MID, lambda: open_prescriptions(win))]
    for label, color, cmd in btns:
        flat_btn(win, label, color, cmd, 32, pady=8).pack(pady=6)

    divider(win, pady=14)
    flat_btn(win, "Logout", RED_DARK, lambda: do_logout(win, root), 14).pack(pady=4)

def open_receptionist_dashboard(root):
    win = _base_dashboard(root, "Receptionist", "Receptionist Portal")

    stats = tk.Frame(win, bg=BG); stats.pack(fill="x", padx=16, pady=(6,0))
    w_lbl = tk.Label(stats, text="Waiting: 0", font=FONT_BOLD, bg=BG, fg=AMBER); w_lbl.pack(side="left", padx=(0,20))
    s_lbl = tk.Label(stats, text="Served: 0", font=FONT_BOLD, bg=BG, fg=TEAL); s_lbl.pack(side="left")

    def update_stats():
        w_lbl.config(text=f"Waiting: {len(patients)}"); s_lbl.config(text=f"Served:  {len(served)}")

    divider(win, pady=6)
    tk.Label(win, text="Receptionist Dashboard", font=FONT_TITLE, bg=BG, fg=BLUE_DARK).pack(pady=(10,4))
    tk.Label(win, text=TAGLINE, font=("Helvetica",10,"italic"), bg=BG, fg=GREY_BTN, justify="center").pack(pady=(0,16))

    def do_register(): open_register(win, update_stats)

    btns = [("Register Patient", TEAL, do_register),
            ("View Queue", BLUE_DARK, lambda: open_queue(win)),
            ("Search Patient", BLUE_MID, lambda: open_search(win)),
            ("Served Patients", "#1e8449", lambda: open_served(win)),
            ("Summary", GREY_BTN, lambda: open_summary(win))]
    for label, color, cmd in btns:
        flat_btn(win, label, color, cmd, 32, pady=8).pack(pady=6)

    divider(win, pady=14)
    flat_btn(win, "Logout", RED_DARK, lambda: do_logout(win, root), 14).pack(pady=4)

def do_logout(win, root):
    if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
        win.destroy()
        login_window(root, lambda role: (open_doctor_dashboard(root) if role == "Doctor" else open_receptionist_dashboard(root)))
