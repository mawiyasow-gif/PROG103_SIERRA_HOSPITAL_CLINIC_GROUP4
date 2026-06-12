import tkinter as tk
from gui import *

from utils import *

CLINIC_NAME = "Sierra Health Hospital Clinic"

TAGLINE = {
    "Your health is Our Priority, "
    "manage appointments, monitor and "
    "receive quality health services with Ease"
}


def main():
    root = tk.Tk()
    root.withdraw()

    def after_login(role):
        if role == "Doctor":
            open_doctor_dashboard(root)
        else:
            open_receptionist_dashboard(root)

    login_window(root, after_login)

    root.mainloop()

if __name__ == "__main__":
    main()



