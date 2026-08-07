from flask import Flask, jsonify, request, send_from_directory, send_file, current_app
from flask_cors import CORS
from flask_mail import Mail, Message
import joblib, pandas as pd, os, json, traceback, socket, base64, requests
from threading import Thread
from dotenv import load_dotenv
load_dotenv()

orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    res = orig_getaddrinfo(host, port, family, type, proto, flags)
    return [r for r in res if r[0] == socket.AF_INET] or res
socket.getaddrinfo = getaddrinfo_ipv4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
if not os.path.exists(FRONTEND_DIR):
    FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))
os.makedirs(os.path.join(BASE_DIR, "reports"), exist_ok=True)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
app.secret_key = "secret"

from admin import admin
app.register_blueprint(admin)

app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=int(os.environ.get("MAIL_PORT", 465))
app.config["MAIL_USE_TLS"]=os.environ.get("MAIL_USE_TLS","false").lower()=="true"
app.config["MAIL_USE_SSL"]=os.environ.get("MAIL_USE_SSL","true").lower()=="true"
app.config["MAIL_USERNAME"]=os.environ.get("MAIL_USERNAME","").strip()
app.config["MAIL_PASSWORD"]=os.environ.get("MAIL_PASSWORD","").replace(" ","").strip()
app.config["MAIL_DEFAULT_SENDER"]=app.config["MAIL_USERNAME"]
app.config["MAIL_TIMEOUT"]=20
mail=Mail(app)
CORS(app)

model_path = os.path.join(BASE_DIR, "models/disease_model.pkl")
if not os.path.exists(model_path):
    model_path = os.path.join(BASE_DIR, "..", "models/disease_model.pkl")
model = joblib.load(model_path)

dataset_path = os.path.join(BASE_DIR, "dataset/Training.csv")
if not os.path.exists(dataset_path):
    dataset_path = os.path.join(BASE_DIR, "..", "dataset/Training.csv")
df = pd.read_csv(dataset_path)
if "Unnamed: 133" in df.columns:
    df = df.drop(columns=["Unnamed: 133"])
symptoms = list(df.columns[:-1])

from services.chatbot_service import get_reply
from services.disease_info import disease_information
from utils.pdf_generator import generate_pdf
from medicine_info import medicine_database
from appointment_database import add_appointment
from prediction_database import add_prediction
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

def send_async_email(app_obj, recipient, subject, body, pdf_path):
    with app_obj.app_context():
        # TRY RESEND HTTP FIRST - WORKS ON RENDER FREE
        resend_key = os.environ.get("RESEND_API_KEY","").strip()
        if resend_key:
            try:
                with open(pdf_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                payload = {
                    "from": os.environ.get("RESEND_FROM","onboarding@resend.dev"),
                    "to": [recipient],
                    "subject": subject,
                    "text": body,
                    "attachments": [{"filename": "Health_Report.pdf", "content": b64}]
                }
                r = requests.post("https://api.resend.com/emails",
                    json=payload,
                    headers={"Authorization": f"Bearer {resend_key}","Content-Type":"application/json"},
                    timeout=30)
                print(f"RESEND API {r.status_code}: {r.text}")
                if r.status_code in [200,201]:
                    print(f"EMAIL OK VIA RESEND to {recipient}")
                    return
                else:
                    print(f"RESEND FAILED, trying SMTP fallback")
            except Exception as e:
                print(f"RESEND ERROR {e}, trying SMTP")
                traceback.print_exc()

        # FALLBACK TO GMAIL SMTP
        try:
            msg = Message(subject=subject, recipients=[recipient], body=body)
            with open(pdf_path, "rb") as fp:
                msg.attach("Health_Report.pdf", "application/pdf", fp.read())
            mail.send(msg)
            print(f"EMAIL OK VIA SMTP to {recipient}")
        except Exception as e:
            print(f"EMAIL FAIL both methods: {e}")
            traceback.print_exc()

@app.route('/')
def home():
    base = find_file("login.html")
    return send_from_directory(base, "login.html")

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
    try:
        data=request.get_json() or {}
        fn=generate_pdf({"patientName":data.get("patientName","Unknown"),"patientAge":data.get("patientAge","Unknown"),"patientGender":data.get("patientGender","Unknown"),"disease":data.get("disease","Unknown"),"confidence":data.get("confidence",0),"description":data.get("description",""),"severity":data.get("severity","Unknown"),"doctor":data.get("doctor","General Physician"),"precautions":data.get("precautions",[])})
        if not os.path.isabs(fn):
            fn = os.path.join(BASE_DIR, fn)
        return send_file(fn, as_attachment=True)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error":str(e)}),500

@app.route("/send-report-email", methods=["POST"])
def send_report_email():
    try:
        data = request.get_json() or {}
        recipient = str(data.get("email","")).strip()
        if not recipient or "@" not in recipient:
            return jsonify({"success":False,"message":"Invalid email"}),400

        pdf_path = generate_pdf({
            "patientName": data.get("patientName","Unknown"),
            "patientAge": data.get("patientAge","Unknown"),
            "patientGender": data.get("patientGender","Unknown"),
            "disease": data.get("disease","Unknown"),
            "confidence": data.get("confidence",0),
            "description": data.get("description",""),
            "severity": data.get("severity","Unknown"),
            "doctor": data.get("doctor","General Physician"),
            "precautions": data.get("precautions",[])
        })
        if not os.path.isabs(pdf_path):
            pdf_path = os.path.join(BASE_DIR, pdf_path)

        subject = f"AI Health Report - {data.get('disease','Report')}"
        body = f"Hello {data.get('patientName','Patient')},\n\nYour AI Symptom Report is attached.\nDisease: {data.get('disease')}\nConfidence: {data.get('confidence')}%\nDoctor: {data.get('doctor')}\n\nTake care."

        Thread(target=send_async_email, args=(current_app._get_current_object(), recipient, subject, body, pdf_path), daemon=True).start()

        return jsonify({"success":True,"message":f"✅ Email queued to {recipient} - Will arrive in 10 sec, check inbox/spam"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success":False,"message":f"Email Failed: {str(e)}"}),500

@app.route("/chatbot", methods=["POST"])
def chatbot():
    data=request.get_json()
    try:
        reply=get_reply(data.get("message",""))
    except:
        reply="Sorry, chatbot offline"
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

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    if os.path.exists(os.path.join(FRONTEND_DIR, "patient", path)):
        return send_from_directory(os.path.join(FRONTEND_DIR, "patient"), path)
    return send_from_directory(FRONTEND_DIR, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)