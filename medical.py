import streamlit as st


# Load Patient Data (Simulated EHR Data)
def load_patient_data():
    try:
        return pd.DataFrame(columns=["Patient ID", "Name", "Age", "Diagnosis", "Medications", "Notes"])
    except Exception as e:
        st.error(f"Error loading patient data: {e}")
        return pd.DataFrame(columns=["Patient ID", "Name", "Age", "Diagnosis", "Medications", "Notes"])

patient_data = load_patient_data()

st.set_page_config(page_title="Doctor Assist Dashboard", layout="wide")
st.title("Doctor Assist Dashboard")

# Search Patient History
st.sidebar.header("Search Patient")
search_id = st.sidebar.text_input("Enter Patient ID")
if st.sidebar.button("Search"):
    patient = patient_data[patient_data["Patient ID"] == search_id]
    if not patient.empty:
        st.write(patient)
    else:
        st.warning("Patient not found")

# Voice-to-Text Notes
st.header("Voice Notes")
def record_voice_note():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Recording... Speak now!")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success("Transcription:")
        st.write(text)
    except sr.UnknownValueError:
        st.error("Could not understand audio")
    except sr.RequestError:
        st.error("Speech Recognition service unavailable")

if st.button("Record Voice Note"):
    record_voice_note()

# AI-Powered Patient History Summarizer
st.header("Patient History Summarizer")
def generate_summary(patient_id):
    patient = patient_data[patient_data["Patient ID"] == patient_id]
    if not patient.empty:
        history = f"Patient: {patient['Name'].values[0]}, Age: {patient['Age'].values[0]}, Diagnosis: {patient['Diagnosis'].values[0]}, Medications: {patient['Medications'].values[0]}, Notes: {patient['Notes'].values[0]}"
        return f"Summary: {history}"
    else:
        return "Patient data not found"

summary_id = st.text_input("Enter Patient ID for Summary")
if st.button("Generate Summary"):
    summary = generate_summary(summary_id)
    st.write(summary)

# Apply Theme
st.markdown("""
    <style>
        body { background-color: black; color: white; }
        .stTextInput, .stButton { color: black !important; }
    </style>
    """, unsafe_allow_html=True)
