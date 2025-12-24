APP_TITLE = "Hospital Management System"
APP_VERSION = "1.0.0"

DB_NAME = "hospital.db"
DB_PATH = f"database/{DB_NAME}"

ROLE_ADMIN = "admin"
ROLE_DOCTOR = "doctor"
ROLE_PATIENT = "patient"
ROLE_STAFF = "staff"

ALL_ROLES = [
    ROLE_ADMIN,
    ROLE_DOCTOR,
    ROLE_PATIENT,
    ROLE_STAFF
]

MIN_PASSWORD_LENGTH = 8

THEME_PRIMARY_COLOR = "#2E86C1"
THEME_ACCENT_COLOR = "#AED6F1"

ERROR_INVALID_EMAIL = "Invalid email format."
ERROR_PASSWORD_TOO_SHORT = f"Password must be at least {MIN_PASSWORD_LENGTH} characters long."
ERROR_FIELDS_REQUIRED = "All fields are required."

TABLE_USERS = "users"
TABLE_PATIENTS = "patients"
TABLE_DOCTORS = "doctors"
TABLE_APPOINTMENTS = "appointments"
TABLE_BILLING = "billing"
