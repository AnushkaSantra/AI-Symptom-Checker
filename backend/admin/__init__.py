from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)
from appointment_database import get_appointments, mark_appointment_done
from prediction_database import (
    get_predictions,
    get_prediction_by_id,
    update_prediction,
    delete_prediction,
    clear_predictions
)

# =====================================================
# ADMIN BLUEPRINT - FIXED WITH STATIC FOLDER
# =====================================================

admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin",
    template_folder="templates",
    static_folder="static",  # <-- FIX: ADDED THIS
    static_url_path="/static"  # <-- FIX: ADDED THIS
)

# =====================================================
# ADMIN LOGIN - NOW WORKS ON /admin/ AND /admin/login
# =====================================================

@admin.route("/", methods=["GET", "POST"])
@admin.route("/login", methods=["GET", "POST"])  # <-- FIX: ADDED THIS
def login():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","").strip()
        ADMIN_USERNAME = "admin"
        ADMIN_PASSWORD = "admin123"
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        return render_template("login.html", error="Invalid username or password.")

    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    return render_template("login.html")

# =====================================================
# ADMIN DASHBOARD
# =====================================================

@admin.route("/dashboard", methods=["GET"])
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    try:
        all_appointments = get_appointments()
        # Show only Booked - Done will be removed automatically
        appointments = [a for a in all_appointments if a.get("status","Booked")!= "Done"]
    except Exception as error:
        print("Appointment database error:", error)
        appointments = []

    try:
        predictions = get_predictions()
    except Exception as error:
        print("Prediction database error:", error)
        predictions = []

    return render_template(
        "dashboard.html",
        appointments=appointments,
        predictions=predictions
    )

# =====================================================
# EDIT PREDICTION
# =====================================================

@admin.route("/prediction/<prediction_id>/edit", methods=["GET", "POST"])
def edit_prediction(prediction_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))

    prediction = get_prediction_by_id(prediction_id)
    if prediction is None:
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        updated_data = {
            "patientName": request.form.get("patientName","").strip(),
            "patientAge": request.form.get("patientAge","").strip(),
            "patientGender": request.form.get("patientGender","").strip(),
            "disease": request.form.get("disease","").strip(),
            "confidence": request.form.get("confidence","").strip(),
            "severity": request.form.get("severity","").strip(),
            "doctor": request.form.get("doctor","").strip()
        }
        try:
            update_prediction(prediction_id, updated_data)
        except Exception as error:
            print("Prediction update error:", error)
        return redirect(url_for("admin.dashboard"))

    return render_template("edit_prediction.html", prediction=prediction, prediction_id=prediction_id)

# =====================================================
# DELETE PREDICTION
# =====================================================

@admin.route("/prediction/<prediction_id>/delete", methods=["POST"])
def delete_prediction_route(prediction_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))
    try:
        deleted = delete_prediction(prediction_id)
        print("DELETED PREDICTION:", deleted)
    except Exception as error:
        print("Prediction deletion error:", error)
    return redirect(url_for("admin.dashboard"))

@admin.route("/predictions/clear", methods=["POST"])
def clear_all_predictions():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))
    try:
        clear_predictions()
    except Exception as error:
        print(error)
    return redirect(url_for("admin.dashboard"))

@admin.route("/appointment/<appointment_id>/done", methods=["POST"])
def complete_appointment(appointment_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))
    try:
        mark_appointment_done(appointment_id)
        print(f"Appointment {appointment_id} marked as Done")
    except Exception as error:
        print("Complete appointment error:", error)
    return redirect(url_for("admin.dashboard"))

# =====================================================
# ADMIN LOGOUT
# =====================================================

@admin.route("/logout", methods=["GET"])
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))