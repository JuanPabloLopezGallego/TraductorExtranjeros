import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from PIL import Image
from gtts import gTTS
from googletrans import Translator


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="EasyTranslate",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

translator = Translator()

# Crear carpeta temporal
os.makedirs("temp", exist_ok=True)


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

    /* ---------- FONDO GENERAL ---------- */

    .stApp {
        background: linear-gradient(135deg, #f5f9ff 0%, #eef4ff 50%, #f8fbff 100%);
    }

    .main {
        padding-top: 1rem;
    }

    /* ---------- OCULTAR ELEMENTOS DE STREAMLIT ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ---------- TITULO ---------- */

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #173B6C;
        margin-bottom: 0.2rem;
    }

    .main-subtitle {
        text-align: center;
        font-size: 1.15rem;
        color: #61708A;
        margin-bottom: 2rem;
    }

    /* ---------- TARJETAS ---------- */

    .card {
        background: white;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(31, 65, 114, 0.08);
        border: 1px solid #e7eef8;
        margin-bottom: 1.2rem;
    }

    .card-title {
        color: #173B6C;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }

    .card-description {
        color: #6B7890;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }

    /* ---------- HERO ---------- */

    .hero {
        background: linear-gradient(135deg, #1769E0, #4D9AFF);
        border-radius: 25px;
        padding: 2.2rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 12px 35px rgba(23, 105, 224, 0.22);
    }

    .hero h1 {
        font-size: 2.6rem;
        margin-bottom: 0.5rem;
    }

    .hero p {
        font-size: 1.1rem;
        opacity: 0.92;
    }

    /* ---------- BOTONES ---------- */

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: none;
        background: linear-gradient(90deg, #1769E0, #388BFF);
        color: white;
        font-weight: 700;
        padding: 0.65rem 1rem;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #0F57C5, #1769E0);
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(23, 105, 224, 0.25);
    }

    /* ---------- SIDEBAR ---------- */

    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e7eef8;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #173B6C;
    }

    /* ---------- RESULTADO ---------- */

    .result-box {
        background: #F0F7FF;
        border-left: 5px solid #1769E0;
        padding: 1.2rem;
        border-radius: 12px;
        margin-top: 1rem;
    }

    .result-title {
        color: #1769E0;
        font-size: 1.15rem;
        font-weight: 700;
    }

    /* ---------- PASOS ---------- */

    .step {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e7eef8;
        box-shadow: 0 5px 20px rgba(31, 65, 114, 0.05);
    }

    .step-icon {
        font-size: 2rem;
    }

    .step-title {
        color: #173B6C;
        font-weight: 700;
        margin-top: 0.4rem;
    }

    .step-text {
        color: #718096;
        font-size: 0.9rem;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        text-align: center;
        color: #8A97AA;
        padding: 2rem;
        font-size: 0.85rem;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# FUNCIONES
# ============================================================

def text_to_speech(input_language, output_language, text, tld):

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    trans_text = translation.text

    tts = gTTS(
        trans_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    clean_name = text[:20].strip()

    if not clean_name:
        clean_name = "audio"

    # Evitar caracteres problemáticos
    clean_name = "".join(
        c for c in clean_name
        if c.isalnum() or c in (" ", "_", "-")
    )

    file_path = f"temp/{clean_name}.mp3"

    tts.save(file_path)

    return clean_name, trans_text


def remove_files(n):

    mp3_files = glob.glob("temp/*mp3")

    if len(mp3_files) == 0:
        return

    now = time.time()
    n_days = n * 86400

    for f in mp3_files:

        if os.stat(f).st_mtime < now - n_days:
            os.remove(f)


remove_files(7)


# ============================================================
# HEADER / HERO
# ============================================================

st.markdown("""
<div class="hero">

    <h1>🌎 EasyTranslate</h1>

    <p>
        Traduce textos de imágenes fácilmente y escucha
        la traducción en el idioma que necesites.
    </p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# EXPLICACIÓN
# ============================================================

st.markdown("""
<div class="card">

<div class="card-title">✨ ¿Cómo funciona?</div>

<div class="card-description">
No necesitas escribir el texto manualmente. 
Simplemente carga una imagen o utiliza tu cámara.
</div>

</div>
""", unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="step">
        <div class="step-icon">📷</div>
        <div class="step-title">1. Toma una foto</div>
        <div class="step-text">
            Fotografía un menú, señal, documento o texto.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="step">
        <div class="step-icon">🔍</div>
        <div class="step-title">2. Detectamos el texto</div>
        <div class="step-text">
            Nuestro sistema reconoce automáticamente las palabras.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="step">
        <div class="step-icon">🔊</div>
        <div class="step-title">3. Escucha la traducción</div>
        <div class="step-text">
            Obtén la traducción y escucha cómo se pronuncia.
        </div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚙️ Configuración")

    st.markdown("---")

    # --------------------------------------------------------
    # IDIOMA DE ENTRADA
    # --------------------------------------------------------

    st.markdown("### 🌐 Idioma de la imagen")

    languages = {
        "🇺🇸 Inglés": "en",
        "🇪🇸 Español": "es",
        "🇧🇩 Bengalí": "bn",
        "🇰🇷 Coreano": "ko",
        "🇨🇳 Mandarín": "zh-cn",
        "🇯🇵 Japonés": "ja"
    }

    input_language_name = st.selectbox(
        "El texto de la imagen está en:",
        list(languages.keys())
    )

    input_language = languages[input_language_name]


    # --------------------------------------------------------
    # IDIOMA DE SALIDA
    # --------------------------------------------------------

    st.markdown("### 🔄 Idioma de traducción")

    output_language_name = st.selectbox(
        "Quiero traducirlo a:",
        list(languages.keys()),
        index=1
    )

    output_language = languages[output_language_name]


    # --------------------------------------------------------
    # ACENTO
    # --------------------------------------------------------

    st.markdown("### 🗣️ Acento")

    accents = {
        "🌎 Predeterminado": "com",
        "🇮🇳 India": "co.in",
        "🇬🇧 Reino Unido": "co.uk",
        "🇺🇸 Estados Unidos": "com",
        "🇨🇦 Canadá": "ca",
        "🇦🇺 Australia": "com.au",
        "🇮🇪 Irlanda": "ie",
        "🇿🇦 Sudáfrica": "co.za"
    }

    accent_name = st.selectbox(
        "Selecciona el acento:",
        list(accents.keys())
    )

    tld = accents[accent_name]


    # --------------------------------------------------------
    # TEXTO DE SALIDA
    # --------------------------------------------------------

    st.markdown("### 📄 Resultado")

    display_output_text = st.checkbox(
        "Mostrar el texto traducido",
        value=True
    )

    st.markdown("---")

    st.info(
        "💡 Consejo: utiliza imágenes claras y con buena iluminación "
        "para obtener mejores resultados."
    )


# ============================================================
# ÁREA PRINCIPAL
# ============================================================

st.markdown("""
<div class="card">

<div class="card-title">📸 Selecciona una imagen</div>

<div class="card-description">
Puedes utilizar la cámara de tu dispositivo o subir una imagen
desde tu ordenador o teléfono.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# CÁMARA / ARCHIVO
# ============================================================

camera_col, upload_col = st.columns(2)


with camera_col:

    st.markdown("### 📷 Cámara")

    use_camera = st.checkbox(
        "Usar cámara",
        value=False
    )

    if use_camera:

        filter_option = st.radio(
            "Mejorar imagen",
            ("Sí", "No"),
            horizontal=True
        )

        img_file_buffer = st.camera_input(
            "Toma una fotografía"
        )

    else:

        img_file_buffer = None
        filter_option = "No"


with upload_col:

    st.markdown("### 📁 Subir imagen")

    bg_image = st.file_uploader(
        "Selecciona una imagen",
        type=["png", "jpg", "jpeg"],
        help="Formatos compatibles: PNG, JPG y JPEG"
    )


# ============================================================
# TEXTO DETECTADO
# ============================================================

text = ""


# ------------------------------------------------------------
# IMAGEN SUBIDA
# ------------------------------------------------------------

if bg_image is not None:

    st.markdown("### 🖼️ Imagen seleccionada")

    uploaded_image = Image.open(bg_image)

    st.image(
        uploaded_image,
        caption="Imagen cargada",
        use_container_width=True
    )

    img_cv = cv2.imread(bg_image.name)

    # Si OpenCV no puede leer directamente el archivo,
    # usamos los bytes del uploader.
    if img_cv is None:

        file_bytes = np.asarray(
            bytearray(bg_image.read()),
            dtype=np.uint8
        )

        img_cv = cv2.imdecode(
            file_bytes,
            cv2.IMREAD_COLOR
        )

    img_rgb = cv2.cvtColor(
        img_cv,
        cv2.COLOR_BGR2RGB
    )

    text = pytesseract.image_to_string(
        img_rgb
    )


# ------------------------------------------------------------
# CÁMARA
# ------------------------------------------------------------

if img_file_buffer is not None:

    st.markdown("### 🔎 Texto detectado")

    bytes_data = img_file_buffer.getvalue()

    cv2_img = cv2.imdecode(
        np.frombuffer(bytes_data, np.uint8),
        cv2.IMREAD_COLOR
    )

    # Aplicar filtro
    if filter_option == "Sí":

        gray = cv2.cvtColor(
            cv2_img,
            cv2.COLOR_BGR2GRAY
        )

        cv2_img = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

    img_rgb = cv2.cvtColor(
        cv2_img,
        cv2.COLOR_BGR2RGB
    )

    text = pytesseract.image_to_string(
        img_rgb
    )


# ============================================================
# MOSTRAR TEXTO DETECTADO
# ============================================================

if text.strip():

    st.markdown("""
    <div class="result-box">

        <div class="result-title">
            📝 Texto detectado
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.text_area(
        "Puedes revisar el texto antes de traducirlo:",
        value=text,
        height=150
    )

else:

    st.markdown("""
    <div class="card">

        <div class="card-title">
            👋 ¡Comencemos!
        </div>

        <div class="card-description">
            Sube una imagen o activa la cámara para detectar
            automáticamente el texto.
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# TRADUCCIÓN
# ============================================================

if text.strip():

    st.markdown("")

    translate_col, empty_col = st.columns([1, 2])

    with translate_col:

        translate_button = st.button(
            "🌎 Traducir y escuchar",
            use_container_width=True
        )

    if translate_button:

        with st.spinner("✨ Traduciendo..."):

            try:

                result, output_text = text_to_speech(
                    input_language,
                    output_language,
                    text,
                    tld
                )

                audio_file = open(
                    f"temp/{result}.mp3",
                    "rb"
                )

                audio_bytes = audio_file.read()

                st.markdown("""
                <div class="result-box">

                    <div class="result-title">
                        🔊 Traducción lista
                    </div>

                </div>
                """, unsafe_allow_html=True)

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

                if display_output_text:

                    st.markdown("### 💬 Texto traducido")

                    st.success(output_text)

            except Exception as e:

                st.error(
                    f"❌ No fue posible realizar la traducción: {e}"
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    🌎 EasyTranslate · Traducción sencilla para viajeros y extranjeros

</div>
""", unsafe_allow_html=True)
