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
    admitted INTEGER DEFAULT 0,  -- 0 for Outpatient, 1 for Inpatient
    status TEXT DEFAULT 'Active', -- General account status
    admission_date TEXT,
    discharge_date TEXT,
    last_admission TEXT, 
    assigned_doctor TEXT
);
"""

STAFF_TABLE = """
CREATE TABLE IF NOT EXISTS staff (
    staff_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT,
    role TEXT, -- 'Doctor', 'Admin', 'Nurse'
    specialty TEXT,
    license_number TEXT,
    department TEXT,
    permissions TEXT,
    phone TEXT,
    email TEXT,
    address TEXT,
    status TEXT DEFAULT 'Active', -- Changed from 'Admitted' to 'Active'
    fee REAL DEFAULT 0.0
);
"""

# Kept empty as you are using the STAFF_TABLE for all roles
DOCTOR_TABLE = "" 
ADMIN_TABLE = ""

APPOINTMENT_TABLE = """
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    doctor_id TEXT NOT NULL,
    date TEXT,
    time TEXT,
    reason TEXT,
    status TEXT DEFAULT 'Scheduled', -- 'Scheduled', 'Completed', 'Cancelled', 'No Show'
    notes TEXT,
    outcome TEXT,
    outcome_type INTEGER,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
    FOREIGN KEY (doctor_id) REFERENCES staff (staff_id)
);
"""

BILL_TABLE = """
CREATE TABLE IF NOT EXISTS bills (
    bill_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    patient_name TEXT,
    amount REAL,
    service_description TEXT,
    payment_status TEXT, -- 'Pending', 'Paid'
    payment_date TEXT,
    payment_method TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);
"""