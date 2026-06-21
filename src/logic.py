# IN-MEMORY DATA STORE
patients = []; served = []; counter = [1]
passwords = {"Doctor": None, "Receptionist": None}
PRIORITY = {"Emergency": 1, "Pregnant": 2, "Normal": 3}

# CORE BUSINESS LOGIC
def make_id():
    pid = f"P{counter[0]:03d}"; counter[0] += 1; return pid

def sort_queue():
    patients.sort(key=lambda p: (PRIORITY[p["category"]], p["arrived"]))

def register_patient(name, age, gender, phone, complaint, arrived, category):
    pid = make_id()
    patients.append({"id": pid, "name": name.title(), "age": age, "gender": gender, "phone": phone,
        "complaint": complaint.capitalize(), "arrived": arrived, "category": category,
        "queue_no": len(patients) + len(served) + 1, "prescription": "", "status": "Waiting"})
    sort_queue(); return pid

def call_next():
    if not patients: return None
    p = patients.pop(0); p["status"] = "Served"; served.append(p); return p

def search_all(term):
    t = term.lower()
    return [p for p in patients + served if t in p["id"].lower() or t in p["name"].lower() or t in p["phone"]]

def queue_counts():
    c = {"Emergency": 0, "Pregnant": 0, "Normal": 0}
    for p in patients: c[p["category"]] += 1
    return c

# VALIDATION HELPERS
def ok_name(t):  return bool(t.strip()) and t.replace(" ", "").isalpha()
def ok_age(t):   return t.isdigit() and 0 <= int(t) <= 120
def ok_phone(t): return t.isdigit() and 7 <= len(t) <= 15
def ok_note(t):  return bool(t.strip()) and not t.strip().isdigit()
def ok_time(t):
    return (len(t) == 5 and t[2] == ":" and t[:2].isdigit() and t[3:].isdigit()
            and 0 <= int(t[:2]) <= 23 and 0 <= int(t[3:]) <= 59)
