PATIENT_TABLE = """
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    blood_type TEXT,
    allergies TEXT,
    medical_history TEXT,
    medical_notes TEXT,
    admitted INTEGER DEFAULT 0,
    admission_date TEXT,
    discharge_date TEXT,
    assigned_doctor TEXT
);
"""

STAFF_TABLE = """
CREATE TABLE IF NOT EXISTS staff (
    staff_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    role TEXT,
    specialty TEXT,
    license_number TEXT,
    department TEXT,
    permissions TEXT
);
"""

DOCTOR_TABLE = """
CREATE TABLE IF NOT EXISTS staff (
    staff_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    role TEXT,
    specialty TEXT,
    license_number TEXT,
    department TEXT,
    permissions TEXT
);
"""

ADMIN_TABLE = """
CREATE TABLE IF NOT EXISTS staff (
    staff_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    role TEXT,
    specialty TEXT,
    license_number TEXT,
    department TEXT,
    permissions TEXT
);
"""

APPOINTMENT_TABLE = """
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    date TEXT,
    time TEXT,
    reason TEXT,
    status TEXT,
    notes TEXT,
    outcome TEXT,
    outcome_type INTEGER
);
"""

BILL_TABLE = """
CREATE TABLE IF NOT EXISTS bills (
    bill_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    patient_name TEXT,
    amount REAL,
    service_description TEXT,
    payment_status TEXT,
    payment_date TEXT,
    payment_method TEXT
);
"""
