from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from flask_mail import Mail, Message
import joblib, pandas as pd, os, json
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# FIX: Prefer backend/frontend first (what Render uses)
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
if not os.path.exists(FRONTEND_DIR):
    FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

print("APP.PY IN:", BASE_DIR)
print("FRONTEND DIR:", FRONTEND_DIR, "EXISTS:", os.path.exists(FRONTEND_DIR))

os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)
os.makedirs("reports", exist_ok=True)

# App
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
app.secret_key = "secret"

from admin import admin
app.register_blueprint(admin)

app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=587
app.config["MAIL_USE_TLS"]=True
app.config["MAIL_USERNAME"]=os.environ.get("MAIL_USERNAME","")
app.config["MAIL_PASSWORD"]=os.environ.get("MAIL_PASSWORD","")
app.config["MAIL_DEFAULT_SENDER"]=app.config["MAIL_USERNAME"] or "demo@aihealth.local"
mail=Mail(app)
CORS(app)

# Model - auto find
model_path = "models/disease_model.pkl"
if not os.path.exists(os.path.join(BASE_DIR, model_path)):
    model_path = "../models/disease_model.pkl"
model = joblib.load(os.path.join(BASE_DIR, model_path))

dataset_path = "dataset/Training.csv"
if not os.path.exists(os.path.join(BASE_DIR, dataset_path)):
    dataset_path = "../dataset/Training.csv"
df = pd.read_csv(os.path.join(BASE_DIR, dataset_path))
if "Unnamed: 133" in df.columns:
    df = df.drop(columns=["Unnamed: 133"])
symptoms = list(df.columns[:-1])

from services.chatbot_service import get_reply
from services.disease_info import disease_information
from utils.pdf_generator import generate_pdf
from medicine_info import medicine_database
from appointment_database import add_appointment, get_appointments, is_slot_available
from prediction_database import add_prediction, get_predictions
from doctor_recommendation import get_recommended_doctor

USERS_FILE = os.path.join(BASE_DIR, "users.json")
users = []
if os.path.exists(USERS_FILE):
    try:
        with open(USERS_FILE) as f:
            users=json.load(f)
    except:
        pass

def find_file(filename):
    for base in [os.path.join(FRONTEND_DIR, "patient"), FRONTEND_DIR]:
        if os.path.exists(os.path.join(base, filename)):
            return base
    return FRONTEND_DIR

# -------- ROUTES --------
@app.route('/')
def home():
    base = find_file("login.html")
    return send_from_directory(base, "login.html")

@app.route("/patient/login")
def patient_login_page():
    base = find_file("login.html")
    return send_from_directory(base, "login.html")

@app.route("/patient/register")
def patient_register_page():
    base = find_file("register.html")
    return send_from_directory(base, "register.html")

@app.route("/symptoms")
def get_symptoms():
    return jsonify(symptoms)

@app.route("/predict", methods=["POST"])
def predict():
    data=request.get_json()
    sel=data.get("symptoms",[])
    input_data=[0 for _ in symptoms]
    for s in sel:
        if s in symptoms:
            input_data[symptoms.index(s)]=1
    input_df=pd.DataFrame([input_data], columns=symptoms)
    pred=model.predict(input_df)
    disease=str(pred[0]).strip()
    try:
        doctor=get_recommended_doctor(disease)
    except:
        doctor="General Physician"
    try:
        prob=model.predict_proba(input_df)[0]
        conf=round(max(prob)*100,2)
        top3=sorted(zip(model.classes_, prob), key=lambda x:x[1], reverse=True)[:3]
        top=[{"Disease":str(d).strip(),"Confidence":round(p*100,2)} for d,p in top3]
    except:
        conf=0; top=[]
    info=disease_information.get(disease,{"description":"No desc","precautions":["Consult doctor"],"doctor":doctor,"severity":"Unknown"})
    med=medicine_database.get(disease,{"otc":[],"prescription":[],"advice":[]})
    try:
        add_prediction({"patientName":data.get("patientName"),"patientAge":data.get("patientAge"),"patientGender":data.get("patientGender"),"disease":disease,"confidence":conf,"severity":info.get("severity"),"doctor":doctor})
    except:
        pass
    return jsonify({"Predicted Disease":disease,"Confidence":conf,"Top Predictions":top,"Description":info.get("description",""),"Severity":info.get("severity","Unknown"),"Doctor":doctor,"Precautions":info.get("precautions",[]),"OTC Medicines":med.get("otc",[])})

@app.route("/download-report", methods=["POST"])
def download_report():
    data=request.get_json()
    fn=generate_pdf({"patientName":data.get("patientName","Unknown"),"patientAge":data.get("patientAge","Unknown"),"patientGender":data.get("patientGender","Unknown"),"disease":data.get("disease","Unknown"),"confidence":data.get("confidence",0),"description":data.get("description",""),"severity":data.get("severity","Unknown"),"doctor":data.get("doctor","General Physician"),"precautions":data.get("precautions",[])})
    return send_file(fn, as_attachment=True)

@app.route("/send-report-email", methods=["POST"])
def send_email():
    return jsonify({"success":True,"message":"✅ Report generated! Please Download PDF."})

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data=request.get_json()
    try:
        reply=get_reply(data.get("message",""))
    except:
        reply="Sorry"
    return jsonify({"reply":reply})

@app.route("/book-appointment", methods=["POST"])
def book_app():
    data=request.get_json()
    add_appointment(data)
    return jsonify({"success":True}),201

@app.route("/patient/register", methods=["POST"])
def reg_api():
    data=request.get_json()
    email=str(data.get("email","")).lower().strip()
    if any(u["email"]==email for u in users):
        return jsonify({"success":False,"message":"Email exists"}),409
    users.append({"name":data.get("name"),"email":email,"password":data.get("password")})
    with open(USERS_FILE,"w") as f:
        json.dump(users,f)
    return jsonify({"success":True,"message":"Registered"})

@app.route("/patient/login", methods=["POST"])
def log_api():
    data=request.get_json()
    email=str(data.get("email","")).lower().strip()
    pwd=str(data.get("password",""))
    for u in users:
        if u["email"]==email and u["password"]==pwd:
            return jsonify({"success":True,"name":u["name"],"patient":{"name":u["name"],"email":u["email"]}})
    return jsonify({"success":False,"message":"Invalid Email or Password"}),401

# This MUST be last
@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    # also check patient subfolder
    if os.path.exists(os.path.join(FRONTEND_DIR, "patient", path)):
        return send_from_directory(os.path.join(FRONTEND_DIR, "patient"), path)
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)