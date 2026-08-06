import sqlite3
import os

# ==========================================
# DATABASE LOCATION
# ==========================================

DATABASE = os.path.join(
    os.path.dirname(__file__),
    "appointments.db"
)

# ==========================================
# CREATE DATABASE
# ==========================================

def init_database():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            doctor TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'Booked'
        )
    """)

    # --- MIGRATION: Add status column if old DB exists without it ---
    try:
        cursor.execute("SELECT status FROM appointments LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE appointments ADD COLUMN status TEXT DEFAULT 'Booked'")
        cursor.execute("UPDATE appointments SET status='Booked' WHERE status IS NULL")

    connection.commit()
    connection.close()

# ==========================================
# ADD APPOINTMENT
# ==========================================

def add_appointment(appointment):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO appointments
        (name, email, phone, doctor, date, time, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Booked')
    """, (
        appointment.get("name", ""),
        appointment.get("email", ""),
        appointment.get("phone", ""),
        appointment.get("doctor", ""),
        appointment.get("date", ""),
        appointment.get("time", "")
    ))

    connection.commit()
    appointment_id = cursor.lastrowid
    connection.close()
    appointment["id"] = appointment_id
    return appointment

# ==========================================
# GET ALL APPOINTMENTS
# ==========================================

def get_appointments():

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM appointments
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return [
        dict(row)
        for row in rows
    ]

# ==========================================
# GET APPOINTMENTS BY EMAIL
# ==========================================

def get_appointment_by_email(email):

    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM appointments
        WHERE LOWER(email) = LOWER(?)
        ORDER BY id DESC
    """, (email,))

    rows = cursor.fetchall()
    connection.close()

    return [
        dict(row)
        for row in rows
    ]

# ==========================================
# CHECK SLOT AVAILABILITY
# ==========================================

def is_slot_available(doctor, date, time):

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id
        FROM appointments
        WHERE LOWER(doctor) = LOWER(?)
        AND date = ?
        AND time = ?
        AND status != 'Done'
        LIMIT 1
    """, (
        doctor.strip(),
        date.strip(),
        time.strip()
    ))

    result = cursor.fetchone()
    connection.close()
    return result is None

# ==========================================
# NEW: MARK AS DONE - ADDED FOR ADMIN
# ==========================================

def get_appointment_by_id(appointment_id):
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id=?", (appointment_id,))
    row = cursor.fetchone()
    connection.close()
    return dict(row) if row else None

def mark_appointment_done(appointment_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("UPDATE appointments SET status='Done' WHERE id=?", (appointment_id,))
    connection.commit()
    connection.close()
    return True

def delete_appointment(appointment_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
    connection.commit()
    connection.close()
    return True

# ==========================================
# INITIALIZE DATABASE
# ==========================================

init_database()