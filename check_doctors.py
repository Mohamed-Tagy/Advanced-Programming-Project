import sqlite3

DB_FILE = "hospital.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# قائمة دكاترة إضافية
doctors_to_add = [
    ('D002', 'Dr. Mona', 35, 'Female', 'Neurology', 'LIC124'),
    ('D003', 'Dr. Karim', 50, 'Male', 'Orthopedics', 'LIC125'),
    ('D004', 'Dr. Sara', 42, 'Female', 'Pediatrics', 'LIC126')
]

for doc in doctors_to_add:
    staff_id, name, age, gender, specialty, license_number = doc
    cursor.execute("""
        INSERT OR IGNORE INTO staff
        (staff_id, name, age, gender, role, specialty, license_number, department, permissions, status, fee)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (staff_id, name, age, gender, 'Doctor', specialty, license_number, None, '', 'Admitted', 0.0))

conn.commit()
print("Additional doctors added.")
cursor.close()
conn.close()
