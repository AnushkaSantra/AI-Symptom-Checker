# ============================================================
# AI HEALTH ASSISTANT
# doctor_recommendation.py
# ============================================================
#
# Maps predicted diseases to appropriate medical specialists.
#
# This system provides informational recommendations only.
# It does not replace professional medical advice.
# ============================================================


doctor_recommendations = {

    # General
    "Common Cold": "General Physician",
    "Gastroenteritis": "General Physician",
    "Dengue": "General Physician",
    "Malaria": "General Physician",
    "Typhoid": "General Physician",
    "Chicken pox": "General Physician",
    "Drug Reaction": "General Physician",
    "Urinary tract infection": "General Physician",

    # Skin
    "Acne": "Dermatologist",
    "Fungal infection": "Dermatologist",
    "Impetigo": "Dermatologist",
    "Psoriasis": "Dermatologist",

    # Respiratory
    "Bronchial Asthma": "Pulmonologist",
    "Pneumonia": "Pulmonologist",
    "Tuberculosis": "Pulmonologist",

    # Heart
    "Heart attack": "Cardiologist",
    "Hypertension": "Cardiologist",

    # Neurology
    "Migraine": "Neurologist",
    "Paralysis (brain hemorrhage)": "Neurologist",
    "(vertigo) Paroymsal Positional Vertigo": "ENT Specialist",

    # Endocrine
    "Diabetes": "Endocrinologist",
    "Diabetes ": "Endocrinologist",
    "Hyperthyroidism": "Endocrinologist",
    "Hypothyroidism": "Endocrinologist",
    "Hypoglycemia": "Endocrinologist",

    # Bones and joints
    "Arthritis": "Rheumatologist",
    "Osteoarthristis": "Orthopedic Specialist",
    "Cervical spondylosis": "Orthopedic Specialist",

    # Digestive / Liver
    "GERD": "Gastroenterologist",
    "Peptic ulcer diseae": "Gastroenterologist",
    "Chronic cholestasis": "Gastroenterologist",
    "Jaundice": "Gastroenterologist",
    "hepatitis A": "Gastroenterologist",
    "Hepatitis B": "Gastroenterologist",
    "Hepatitis C": "Gastroenterologist",
    "Hepatitis D": "Gastroenterologist",
    "Hepatitis E": "Gastroenterologist",
    "Alcoholic hepatitis": "Gastroenterologist",

    # Other
    "AIDS": "Infectious Disease Specialist",
    "Allergy": "Allergist",
    "Dimorphic hemmorhoids(piles)": "General Surgeon",
    "Varicose veins": "Vascular Specialist"
}


# ============================================================
# HELPER FUNCTION
# ============================================================

def get_recommended_doctor(disease):

    """
    Return the recommended medical specialist
    for the predicted disease.
    """

    disease = str(disease).strip()

    return doctor_recommendations.get(
        disease,
        "General Physician"
    )