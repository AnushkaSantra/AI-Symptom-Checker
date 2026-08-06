# =====================================
# AI Health Assistant Chatbot
# =====================================

def get_reply(message):

    message = message.lower().strip()

    # =====================================
    # Greetings
    # =====================================

    if any(word in message for word in [
        "hi","hello","hey","good morning","good afternoon","good evening"
    ]):

        return (
            "Hello 👋\n\n"
            "Welcome to AI Health Assistant.\n\n"
            "I can help you with:\n"
            "• Diseases\n"
            "• Symptoms\n"
            "• Healthy Diet\n"
            "• Exercise\n"
            "• First Aid\n"
            "• Prevention Tips\n"
            "• Emergency Guidance\n\n"
            "How may I help you today?"
        )

    # =====================================
    # Emergency Detection
    # =====================================

    elif any(word in message for word in [

        "heart attack",
        "can't breathe",
        "cannot breathe",
        "difficulty breathing",
        "stroke",
        "unconscious",
        "heavy bleeding",
        "severe chest pain"

    ]):

        return (
            "⚠ EMERGENCY WARNING ⚠\n\n"
            "Your symptoms may indicate a medical emergency.\n\n"
            "Please call your local emergency services or go to the nearest hospital immediately.\n\n"
            "Do not rely only on this chatbot."
        )

    # =====================================
    # Fever
    # =====================================

    elif "fever" in message:

        return (
            "🌡 Fever\n\n"
            "Common causes:\n"
            "• Viral infection\n"
            "• Bacterial infection\n"
            "• Flu\n\n"
            "Take rest.\n"
            "Drink plenty of water.\n"
            "Monitor temperature.\n\n"
            "Consult a doctor if fever lasts more than 2 days or becomes very high."
        )

    # =====================================
    # Headache
    # =====================================

    elif "headache" in message:

        return (
            "🤕 Headache\n\n"
            "Possible causes:\n"
            "• Stress\n"
            "• Lack of sleep\n"
            "• Dehydration\n"
            "• Migraine\n\n"
            "Drink water.\n"
            "Take adequate rest.\n"
            "Avoid excessive screen time.\n\n"
            "Visit a doctor if headaches are severe or frequent."
        )

    # =====================================
    # Cough
    # =====================================

    elif "cough" in message:

        return (
            "😷 Cough\n\n"
            "Common causes:\n"
            "• Cold\n"
            "• Allergy\n"
            "• Viral infection\n"
            "• Asthma\n\n"
            "Drink warm fluids.\n"
            "Stay hydrated.\n\n"
            "Consult a doctor if cough lasts more than two weeks."
        )

    # =====================================
    # Cold
    # =====================================

    elif "cold" in message:

        return (
            "🤧 Common Cold\n\n"
            "Symptoms:\n"
            "• Sneezing\n"
            "• Runny nose\n"
            "• Mild fever\n"
            "• Sore throat\n\n"
            "Take rest.\n"
            "Drink warm water.\n"
            "Eat healthy food."
        )

    # =====================================
    # Sore Throat
    # =====================================

    elif "sore throat" in message:

        return (
            "🦠 Sore Throat\n\n"
            "Drink warm water.\n"
            "Avoid cold drinks.\n"
            "Rest your voice.\n\n"
            "Consult a doctor if symptoms persist."
        )

    # =====================================
    # Stomach Pain
    # =====================================

    elif "stomach" in message or "abdominal" in message:

        return (
            "🤢 Stomach Pain\n\n"
            "Possible causes:\n"
            "• Gastritis\n"
            "• Food poisoning\n"
            "• Indigestion\n"
            "• Infection\n\n"
            "Eat light food.\n"
            "Drink water.\n\n"
            "Consult a doctor if pain becomes severe."
        )

    # =====================================
    # Vomiting
    # =====================================

    elif "vomit" in message or "vomiting" in message:

        return (
            "🤮 Vomiting\n\n"
            "Drink ORS or water slowly.\n"
            "Avoid oily food.\n"
            "Take adequate rest.\n\n"
            "Consult a doctor if vomiting continues repeatedly."
        )

    # =====================================
    # Diarrhea
    # =====================================

    elif "diarrhea" in message or "loose motion" in message:

        return (
            "💧 Diarrhea\n\n"
            "Drink plenty of fluids.\n"
            "Take ORS solution.\n"
            "Eat light food.\n\n"
            "Consult a doctor if symptoms continue."
        )

    # =====================================
    # Constipation
    # =====================================

    elif "constipation" in message:

        return (
            "🥗 Constipation\n\n"
            "Eat fibre-rich foods.\n"
            "Drink more water.\n"
            "Exercise regularly.\n\n"
            "Consult a doctor if constipation lasts several days."
        )

    # =====================================
    # Dizziness
    # =====================================

    elif "dizzy" in message or "dizziness" in message:

        return (
            "😵 Dizziness\n\n"
            "Sit down immediately.\n"
            "Drink water.\n"
            "Avoid sudden movements.\n\n"
            "Consult a doctor if dizziness is frequent."
        )

    # =====================================
    # Weakness
    # =====================================

    elif "weakness" in message or "fatigue" in message:

        return (
            "😴 Weakness / Fatigue\n\n"
            "Possible causes:\n"
            "• Lack of sleep\n"
            "• Poor diet\n"
            "• Stress\n"
            "• Illness\n\n"
            "Take proper rest.\n"
            "Eat healthy food.\n"
            "Stay hydrated."
        )

    # =====================================
    # Water
    # =====================================

    elif "water" in message:

        return (
            "💧 Adults should generally drink around 2–3 litres of water daily, unless a doctor has advised otherwise."
        )

    # =====================================
    # Sleep
    # =====================================

    elif "sleep" in message:

        return (
            "😴 Adults should sleep 7–9 hours every night for good physical and mental health."
        )

    # =====================================
    # Exercise
    # =====================================

    elif "exercise" in message:

        return (
            "🏃 Exercise at least 30 minutes daily.\n\n"
            "Walking, cycling, yoga and light workouts improve overall health."
        )

    # =====================================
    # Diet
    # =====================================

    elif "diet" in message or "food" in message:

        return (
            "🥗 Healthy Diet\n\n"
            "Eat:\n"
            "• Fruits\n"
            "• Vegetables\n"
            "• Whole grains\n"
            "• Protein-rich food\n\n"
            "Avoid excessive sugary and processed foods."
        )
        # =====================================
    # Allergy
    # =====================================

    elif "allergy" in message:

        return (
            "🤧 Allergy\n\n"
            "An allergy is an immune system reaction to substances like dust, pollen, food or medicines.\n\n"
            "Common symptoms:\n"
            "• Sneezing\n"
            "• Itching\n"
            "• Skin rash\n"
            "• Watery eyes\n\n"
            "Avoid the allergen and consult a doctor if symptoms become severe."
        )

    # =====================================
    # Diabetes
    # =====================================

    elif "diabetes" in message:

        return (
            "🩸 Diabetes\n\n"
            "Diabetes occurs when blood sugar becomes too high.\n\n"
            "Symptoms:\n"
            "• Frequent urination\n"
            "• Increased thirst\n"
            "• Fatigue\n"
            "• Weight loss\n\n"
            "Maintain a healthy diet, exercise regularly and monitor blood sugar."
        )

    # =====================================
    # Dengue
    # =====================================

    elif "dengue" in message:

        return (
            "🦟 Dengue\n\n"
            "Dengue spreads through mosquito bites.\n\n"
            "Symptoms:\n"
            "• High fever\n"
            "• Severe headache\n"
            "• Joint pain\n"
            "• Skin rash\n\n"
            "Drink plenty of fluids and seek medical care if symptoms worsen."
        )

    # =====================================
    # Malaria
    # =====================================

    elif "malaria" in message:

        return (
            "🦟 Malaria\n\n"
            "Malaria is caused by parasites spread by mosquitoes.\n\n"
            "Symptoms:\n"
            "• Fever\n"
            "• Chills\n"
            "• Sweating\n"
            "• Weakness\n\n"
            "Early diagnosis and proper treatment are important."
        )

    # =====================================
    # COVID
    # =====================================

    elif "covid" in message or "coronavirus" in message:

        return (
            "🦠 COVID-19\n\n"
            "COVID-19 is a viral infection.\n\n"
            "Symptoms:\n"
            "• Fever\n"
            "• Cough\n"
            "• Sore throat\n"
            "• Difficulty breathing\n\n"
            "Isolate if infected and consult a doctor if symptoms become severe."
        )

    # =====================================
    # Asthma
    # =====================================

    elif "asthma" in message:

        return (
            "🫁 Asthma\n\n"
            "Asthma narrows the airways causing breathing difficulty.\n\n"
            "Symptoms:\n"
            "• Wheezing\n"
            "• Cough\n"
            "• Chest tightness\n"
            "• Shortness of breath\n\n"
            "Avoid smoke and dust and consult a doctor."
        )

    # =====================================
    # Pneumonia
    # =====================================

    elif "pneumonia" in message:

        return (
            "🫁 Pneumonia\n\n"
            "Pneumonia is an infection of the lungs.\n\n"
            "Symptoms:\n"
            "• Fever\n"
            "• Chest pain\n"
            "• Cough\n"
            "• Difficulty breathing\n\n"
            "Medical treatment is important."
        )

    # =====================================
    # Tuberculosis
    # =====================================

    elif "tuberculosis" in message or "tb" in message:

        return (
            "🫁 Tuberculosis (TB)\n\n"
            "TB mainly affects the lungs.\n\n"
            "Symptoms:\n"
            "• Long-lasting cough\n"
            "• Weight loss\n"
            "• Fever\n"
            "• Night sweats\n\n"
            "Consult a doctor for diagnosis and complete treatment."
        )

    # =====================================
    # Heart Attack
    # =====================================

    elif "heart attack" in message:

        return (
            "❤️ Heart Attack\n\n"
            "Symptoms include:\n"
            "• Chest pain\n"
            "• Sweating\n"
            "• Pain in left arm\n"
            "• Shortness of breath\n\n"
            "⚠ Seek emergency medical help immediately."
        )

    # =====================================
    # Hypertension
    # =====================================

    elif "hypertension" in message or "high blood pressure" in message:

        return (
            "🩺 High Blood Pressure\n\n"
            "Often there are no symptoms.\n\n"
            "Reduce salt intake.\n"
            "Exercise regularly.\n"
            "Maintain healthy weight.\n"
            "Monitor blood pressure."
        )

    # =====================================
    # Hypothyroidism
    # =====================================

    elif "hypothyroidism" in message:

        return (
            "🦋 Hypothyroidism\n\n"
            "Symptoms:\n"
            "• Fatigue\n"
            "• Weight gain\n"
            "• Dry skin\n"
            "• Feeling cold\n\n"
            "Consult an endocrinologist."
        )

    # =====================================
    # Hyperthyroidism
    # =====================================

    elif "hyperthyroidism" in message:

        return (
            "🦋 Hyperthyroidism\n\n"
            "Symptoms:\n"
            "• Weight loss\n"
            "• Fast heartbeat\n"
            "• Sweating\n"
            "• Anxiety\n\n"
            "Consult an endocrinologist."
        )

    # =====================================
    # Arthritis
    # =====================================

    elif "arthritis" in message:

        return (
            "🦴 Arthritis\n\n"
            "Symptoms:\n"
            "• Joint pain\n"
            "• Swelling\n"
            "• Stiffness\n\n"
            "Exercise regularly and consult an orthopedic doctor."
        )

    # =====================================
    # Osteoarthritis
    # =====================================

    elif "osteoarthritis" in message:

        return (
            "🦴 Osteoarthritis\n\n"
            "A wear-and-tear disease affecting joints.\n\n"
            "Maintain healthy weight and perform regular physiotherapy."
        )

    # =====================================
    # Cervical Spondylosis
    # =====================================

    elif "cervical" in message or "spondylosis" in message:

        return (
            "💺 Cervical Spondylosis\n\n"
            "Symptoms:\n"
            "• Neck pain\n"
            "• Shoulder pain\n"
            "• Stiffness\n\n"
            "Maintain good posture and consult an orthopedic specialist."
        )

    # =====================================
    # Migraine
    # =====================================

    elif "migraine" in message:

        return (
            "🤕 Migraine\n\n"
            "Migraine causes severe headaches with sensitivity to light or sound.\n\n"
            "Rest in a quiet room and consult a neurologist if attacks are frequent."
        )
        # =====================================
    # Psoriasis
    # =====================================

    elif "psoriasis" in message:

        return (
            "🩹 Psoriasis\n\n"
            "Psoriasis is a long-term skin condition causing red, itchy and scaly patches.\n\n"
            "Keep your skin moisturized.\n"
            "Avoid scratching.\n"
            "Consult a dermatologist."
        )

    # =====================================
    # Acne
    # =====================================

    elif "acne" in message or "pimple" in message:

        return (
            "🙂 Acne\n\n"
            "Acne occurs when skin pores become blocked.\n\n"
            "Wash your face twice daily.\n"
            "Avoid squeezing pimples.\n"
            "Consult a dermatologist if severe."
        )

    # =====================================
    # Chickenpox
    # =====================================

    elif "chickenpox" in message or "chicken pox" in message:

        return (
            "🐔 Chickenpox\n\n"
            "Chickenpox is a contagious viral disease.\n\n"
            "Symptoms:\n"
            "• Fever\n"
            "• Itchy blisters\n"
            "• Weakness\n\n"
            "Rest well and avoid scratching the blisters."
        )

    # =====================================
    # Typhoid
    # =====================================

    elif "typhoid" in message:

        return (
            "🌡 Typhoid\n\n"
            "Typhoid spreads through contaminated food and water.\n\n"
            "Drink clean water.\n"
            "Eat hygienic food.\n"
            "Consult a doctor for treatment."
        )

    # =====================================
    # Jaundice
    # =====================================

    elif "jaundice" in message:

        return (
            "💛 Jaundice\n\n"
            "Jaundice causes yellowing of the eyes and skin due to liver problems.\n\n"
            "Drink enough fluids.\n"
            "Avoid alcohol.\n"
            "Consult a doctor."
        )

    # =====================================
    # UTI
    # =====================================

    elif "uti" in message or "urinary" in message:

        return (
            "🚻 Urinary Tract Infection\n\n"
            "Symptoms:\n"
            "• Burning while urinating\n"
            "• Frequent urination\n"
            "• Lower abdominal pain\n\n"
            "Drink plenty of water and consult a doctor."
        )

    # =====================================
    # GERD
    # =====================================

    elif "gerd" in message or "acid reflux" in message or "heartburn" in message:

        return (
            "🔥 GERD (Acid Reflux)\n\n"
            "Avoid spicy foods.\n"
            "Eat smaller meals.\n"
            "Avoid lying down immediately after eating.\n"
            "Consult a gastroenterologist if symptoms continue."
        )

    # =====================================
    # Hepatitis
    # =====================================

    elif "hepatitis" in message:

        return (
            "🧬 Hepatitis\n\n"
            "Hepatitis is inflammation of the liver.\n\n"
            "Common symptoms:\n"
            "• Fatigue\n"
            "• Jaundice\n"
            "• Loss of appetite\n\n"
            "Consult a doctor for diagnosis."
        )

    # =====================================
    # Skin Rash
    # =====================================

    elif "rash" in message:

        return (
            "🩹 Skin Rash\n\n"
            "A skin rash may occur because of allergy, infection or irritation.\n\n"
            "Avoid scratching.\n"
            "Keep the area clean.\n"
            "Consult a dermatologist if the rash spreads."
        )

    # =====================================
    # Itching
    # =====================================

    elif "itch" in message or "itching" in message:

        return (
            "🖐 Itching\n\n"
            "Possible causes:\n"
            "• Allergy\n"
            "• Dry skin\n"
            "• Infection\n\n"
            "Avoid scratching and consult a doctor if persistent."
        )

    # =====================================
    # Eye Pain / Red Eyes
    # =====================================

    elif "eye" in message:

        return (
            "👁 Eye Problems\n\n"
            "If you have eye pain, redness or blurred vision:\n\n"
            "Do not rub your eyes.\n"
            "Wash with clean water.\n"
            "Consult an eye specialist."
        )

    # =====================================
    # Ear Pain
    # =====================================

    elif "ear" in message:

        return (
            "👂 Ear Pain\n\n"
            "Ear pain may be caused by infection or wax buildup.\n\n"
            "Do not insert sharp objects into the ear.\n"
            "Consult an ENT specialist."
        )

    # =====================================
    # Tooth Pain
    # =====================================

    elif "tooth" in message or "teeth" in message:

        return (
            "🦷 Tooth Pain\n\n"
            "Brush twice daily.\n"
            "Avoid excessive sweets.\n"
            "Visit a dentist if pain continues."
        )

    # =====================================
    # Stress
    # =====================================

    elif "stress" in message:

        return (
            "🧘 Stress\n\n"
            "Reduce stress by:\n"
            "• Deep breathing\n"
            "• Exercise\n"
            "• Meditation\n"
            "• Adequate sleep\n\n"
            "Seek professional help if stress becomes overwhelming."
        )

    # =====================================
    # Anxiety
    # =====================================

    elif "anxiety" in message:

        return (
            "💙 Anxiety\n\n"
            "Anxiety may cause nervousness, fast heartbeat and excessive worry.\n\n"
            "Practice relaxation techniques and consult a mental health professional if symptoms persist."
        )

    # =====================================
    # Depression
    # =====================================

    elif "depression" in message:

        return (
            "💚 Depression\n\n"
            "Depression is a serious mental health condition.\n\n"
            "Talk to someone you trust and consult a qualified mental health professional."
        )

    # =====================================
    # Pregnancy
    # =====================================

    elif "pregnancy" in message or "pregnant" in message:

        return (
            "🤰 Pregnancy\n\n"
            "Eat a balanced diet.\n"
            "Take regular prenatal checkups.\n"
            "Avoid smoking and alcohol.\n"
            "Consult your gynecologist regularly."
        )

    # =====================================
    # Child Health
    # =====================================

    elif "baby" in message or "child" in message:

        return (
            "👶 Child Health\n\n"
            "Children with high fever, breathing difficulty or persistent vomiting should be examined by a pediatrician as soon as possible."
        )
        # =====================================
    # Burn
    # =====================================

    elif "burn" in message:

        return (
            "🔥 Burn First Aid\n\n"
            "• Cool the burn under cool running water for 10–20 minutes.\n"
            "• Do not apply ice, toothpaste or butter.\n"
            "• Cover with a clean cloth.\n"
            "• Seek medical care for severe burns."
        )

    # =====================================
    # Cut
    # =====================================

    elif "cut" in message or "bleeding" in message:

        return (
            "🩹 Minor Cut\n\n"
            "• Wash the wound with clean water.\n"
            "• Apply gentle pressure to stop bleeding.\n"
            "• Cover with a clean bandage.\n"
            "• Consult a doctor if bleeding does not stop."
        )

    # =====================================
    # Dog Bite
    # =====================================

    elif "dog bite" in message:

        return (
            "🐶 Dog Bite\n\n"
            "Wash the wound immediately with soap and water for at least 15 minutes.\n"
            "Visit a hospital immediately for proper medical evaluation."
        )

    # =====================================
    # Snake Bite
    # =====================================

    elif "snake bite" in message:

        return (
            "🐍 Snake Bite\n\n"
            "Keep the person calm.\n"
            "Do NOT cut the wound or suck the venom.\n"
            "Go to the nearest hospital immediately."
        )

    # =====================================
    # Choking
    # =====================================

    elif "choking" in message:

        return (
            "😨 Choking\n\n"
            "If the person cannot breathe or speak, seek emergency help immediately.\n"
            "Perform first aid only if you are trained."
        )

    # =====================================
    # Fracture
    # =====================================

    elif "fracture" in message or "broken bone" in message:

        return (
            "🦴 Fracture\n\n"
            "Keep the injured part still.\n"
            "Do not try to straighten the bone.\n"
            "Seek medical care immediately."
        )

    # =====================================
    # Nose Bleed
    # =====================================

    elif "nose bleed" in message or "nosebleed" in message:

        return (
            "🩸 Nose Bleed\n\n"
            "Sit upright.\n"
            "Lean slightly forward.\n"
            "Pinch your nose for 10–15 minutes.\n"
            "Consult a doctor if bleeding continues."
        )

    # =====================================
    # Protein
    # =====================================

    elif "protein" in message:

        return (
            "🥚 Protein-rich foods include:\n\n"
            "• Eggs\n"
            "• Fish\n"
            "• Chicken\n"
            "• Milk\n"
            "• Lentils\n"
            "• Soybeans\n"
            "• Nuts"
        )

    # =====================================
    # Calcium
    # =====================================

    elif "calcium" in message:

        return (
            "🥛 Calcium-rich foods:\n\n"
            "• Milk\n"
            "• Cheese\n"
            "• Yogurt\n"
            "• Green leafy vegetables\n"
            "• Almonds"
        )

    # =====================================
    # Iron
    # =====================================

    elif "iron" in message:

        return (
            "🥬 Iron-rich foods:\n\n"
            "• Spinach\n"
            "• Beans\n"
            "• Lentils\n"
            "• Red meat\n"
            "• Dates"
        )

    # =====================================
    # Vitamin C
    # =====================================

    elif "vitamin c" in message:

        return (
            "🍊 Vitamin C sources:\n\n"
            "• Orange\n"
            "• Lemon\n"
            "• Guava\n"
            "• Kiwi\n"
            "• Amla"
        )

    # =====================================
    # Weight Loss
    # =====================================

    elif "weight loss" in message:

        return (
            "⚖ Healthy Weight Loss\n\n"
            "• Eat balanced meals.\n"
            "• Exercise regularly.\n"
            "• Avoid sugary drinks.\n"
            "• Sleep well."
        )

    # =====================================
    # Weight Gain
    # =====================================

    elif "weight gain" in message:

        return (
            "💪 Healthy Weight Gain\n\n"
            "• Eat nutritious meals.\n"
            "• Increase protein intake.\n"
            "• Strength training exercises.\n"
            "• Consult a dietitian if needed."
        )

    # =====================================
    # BMI
    # =====================================

    elif "bmi" in message:

        return (
            "📊 BMI (Body Mass Index)\n\n"
            "Formula:\n"
            "BMI = Weight (kg) ÷ Height² (m²)\n\n"
            "18.5–24.9 is generally considered a healthy range."
        )

    # =====================================
    # Vaccination
    # =====================================

    elif "vaccine" in message or "vaccination" in message:

        return (
            "💉 Vaccination helps protect against many serious diseases.\n\n"
            "Follow the recommended vaccination schedule and consult your healthcare provider."
        )

    # =====================================
    # Immunity
    # =====================================

    elif "immunity" in message:

        return (
            "🛡 Improve Immunity\n\n"
            "• Eat fruits and vegetables.\n"
            "• Sleep well.\n"
            "• Exercise regularly.\n"
            "• Stay hydrated.\n"
            "• Reduce stress."
        )

    # =====================================
    # Hygiene
    # =====================================

    elif "hygiene" in message:

        return (
            "🧼 Good Hygiene Tips\n\n"
            "• Wash hands regularly.\n"
            "• Drink clean water.\n"
            "• Keep food covered.\n"
            "• Maintain personal cleanliness."
        )

    # =====================================
    # Doctor Recommendation
    # =====================================

    elif "doctor" in message:

        return (
            "👨‍⚕ Doctor Guide\n\n"
            "• Heart → Cardiologist\n"
            "• Skin → Dermatologist\n"
            "• Bones → Orthopedic\n"
            "• Eyes → Ophthalmologist\n"
            "• Ear/Nose/Throat → ENT Specialist\n"
            "• Diabetes → Endocrinologist\n"
            "• Children → Pediatrician\n"
            "• Women's Health → Gynecologist\n"
            "• General illness → General Physician"
        )

    # =====================================
    # Medicine
    # =====================================

    elif "medicine" in message or "tablet" in message or "drug" in message:

        return (
            "💊 I cannot recommend or prescribe medicines.\n\n"
            "Please consult a qualified healthcare professional for medication advice."
        )

    # =====================================
    # Thank You
    # =====================================

    elif "thank" in message:

        return (
            "😊 You're welcome!\n\n"
            "Stay healthy and take care. If you have more health-related questions, I'm here to help."
        )

    # =====================================
    # Goodbye
    # =====================================

    elif "bye" in message or "goodbye" in message:

        return (
            "👋 Goodbye!\n\n"
            "Take care of your health. Have a wonderful day!"
        )

    # =====================================
    # Default Response
    # =====================================

    else:

        return (
            "🤖 I couldn't understand your question.\n\n"
            "You can ask me about:\n\n"
            "• Diseases\n"
            "• Symptoms\n"
            "• Allergy\n"
            "• Diabetes\n"
            "• Dengue\n"
            "• Malaria\n"
            "• Fever\n"
            "• Headache\n"
            "• Diet\n"
            "• Exercise\n"
            "• BMI\n"
            "• First Aid\n"
            "• Vaccination\n"
            "• Hygiene\n"
            "• Doctors\n\n"
            "Please ask your question in a different way."
        )