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

"""KAI CODE"""
