import streamlit as st
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import img_to_array

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="EcoCare Waste Classifier", layout="wide", initial_sidebar_state="collapsed")

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;500;600;700&display=swap');

/* Force Dancing Script for every element */
*,
*::before,
*::after,
html,
body,
[data-testid="stAppViewContainer"],
.stButton button,
.stText,
.stMarkdown,
.stTextInput input,
.stNumberInput input,
.stSelectbox select,
.stRadio label,
.stCheckbox label,
.stSlider > div,
.stExpander > div,
.stTabs button,
.stTextArea textarea {
    font-family: 'Dancing Script', cursive !important;
}

/* Hide Streamlit header and footer for a clean embed */
header, footer {
    visibility: hidden;
}

/* App background and padding */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #d4f1dd 0%, #a8e6cf 50%, #c8e6c9 100%);
    padding: 2rem !important;
}

/* Titles, cards, and buttons (optional styling) */
.title { text-align: center; font-size: 36px; font-weight: 700; color: #2d5f3f; margin-bottom: 10px; }
.subtitle { text-align: center; font-size: 18px; color: #3d7050; margin-bottom: 30px; }
.image-box { background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
.result-card { background: linear-gradient(135deg, #5fa777 0%, #4a8f60 100%); border-radius: 15px; padding: 25px; text-align: center; box-shadow: 0 4px 15px rgba(95, 167, 119, 0.4); margin-bottom: 15px; color: white; }
.confidence-card { background: rgba(255,255,255,0.9); border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); font-weight: 700; color: #2d5f3f; }
.stButton button { background: linear-gradient(135deg, #5fa777 0%, #4a8f60 100%) !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 12px 30px !important; font-size: 17px !important; font-weight: 600 !important; width: 100% !important; }
.stButton button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(95, 167, 119, 0.5) !important; }
</style>
""", unsafe_allow_html=True)


# =========================
# MODEL SETUP
# =========================
MODEL_PATH = "waste_classifier_robust.h5"
IMG_SIZE = (224, 224)

@st.cache_resource
def build_model():
    base_model = MobileNetV2(weights=None, include_top=False, input_shape=(224,224,3))
    base_model.trainable = False
    inputs = tf.keras.Input(shape=(224,224,3))
    x = base_model(inputs, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(1, activation="sigmoid")(x)
    model = models.Model(inputs, outputs)
    return model

model = build_model()
model.load_weights(MODEL_PATH)

CLASS_MAP = {0: "Biodegradable", 1: "Non-Biodegradable"}

# =========================
# HEADER
# =========================
st.markdown('<h1 class="title">EcoCare Waste Classifier</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload an image to classify your waste</p>', unsafe_allow_html=True)

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1,1], gap="large")

with col1:
    uploaded_file = st.file_uploader("Choose an image", type=["jpg","png","jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.markdown('<div class="image-box">', unsafe_allow_html=True)
        st.image(image, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if uploaded_file:
        if st.button("Analyze Waste"):
            with st.spinner("Analyzing..."):
                try:
                    img = image.convert("RGB").resize(IMG_SIZE)
                    img_array = img_to_array(img)/255.0
                    img_array = np.expand_dims(img_array, axis=0)
                    prob = model.predict(img_array, verbose=0)[0][0]

                    if prob >= 0.5:
                        label = CLASS_MAP[1]
                        confidence = prob
                    else:
                        label = CLASS_MAP[0]
                        confidence = 1 - prob

                    st.markdown(f"""
                    <div class="result-card">
                        <p>Classification</p>
                        <h2>{label}</h2>
                    </div>
                    <div class="confidence-card">
                        Confidence: {round(float(confidence)*100, 2)}%
                    </div>
                    """, unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
    else:
        st.info("Upload an image to get started")
