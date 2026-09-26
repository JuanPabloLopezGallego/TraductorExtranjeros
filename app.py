import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract

from PIL import Image
from gTTS import gTTS
from googletrans import Translator


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="EasyTranslate",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

TEMP_FOLDER = "temp"

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

translator = Translator()


# ============================================================
# IDIOMAS
# ============================================================

LANGUAGES = {
    "🇪🇸 Español": {"translation": "es", "tesseract": "spa"},
    "🇺🇸 English": {"translation": "en", "tesseract": "eng"},
    "🇫🇷 Français": {"translation": "fr", "tesseract": "fra"},
    "🇩🇪 Deutsch": {"translation": "de", "tesseract": "deu"},
    "🇮🇹 Italiano": {"translation": "it", "tesseract": "ita"},
    "🇵🇹 Português": {"translation": "pt", "tesseract": "por"},
    "🇳🇱 Nederlands": {"translation": "nl", "tesseract": "nld"},
    "🇷🇺 Русский": {"translation": "ru", "tesseract": "rus"},
    "🇺🇦 Українська": {"translation": "uk", "tesseract": "ukr"},
    "🇵🇱 Polski": {"translation": "pl", "tesseract": "pol"},
    "🇨🇿 Čeština": {"translation": "cs", "tesseract": "ces"},
    "🇸🇰 Slovenčina": {"translation": "sk", "tesseract": "slk"},
    "🇭🇺 Magyar": {"translation": "hu", "tesseract": "hun"},
    "🇷🇴 Română": {"translation": "ro", "tesseract": "ron"},
    "🇹🇷 Türkçe": {"translation": "tr", "tesseract": "tur"},
    "🇬🇷 Ελληνικά": {"translation": "el", "tesseract": "ell"},
    "🇸🇪 Svenska": {"translation": "sv", "tesseract": "swe"},
    "🇩🇰 Dansk": {"translation": "da", "tesseract": "dan"},
    "🇫🇮 Suomi": {"translation": "fi", "tesseract": "fin"},
    "🇳🇴 Norsk": {"translation": "no", "tesseract": "nor"},
    "🇮🇳 हिन्दी": {"translation": "hi", "tesseract": "hin"},
    "🇧🇩 বাংলা": {"translation": "bn", "tesseract": "ben"},
    "🇮🇩 Bahasa Indonesia": {"translation": "id", "tesseract": "ind"},
    "🇻🇳 Tiếng Việt": {"translation": "vi", "tesseract": "vie"},
    "🇹🇭 ไทย": {"translation": "th", "tesseract": "tha"},
    "🇰🇷 한국어": {"translation": "ko", "tesseract": "kor"},
    "🇯🇵 日本語": {"translation": "ja", "tesseract": "jpn"},
    "🇨🇳 简体中文": {"translation": "zh-cn", "tesseract": "chi_sim"},
    "🇹🇼 繁體中文": {"translation": "zh-tw", "tesseract": "chi_tra"},
    "🇸🇦 العربية": {"translation": "ar", "tesseract": "ara"},
    "🇮🇱 עברית": {"translation": "iw", "tesseract": "heb"}
}

LANGUAGE_LIST = list(LANGUAGES.keys())


# ============================================================
# ACENTOS
# ============================================================

ACCENTS = {
    "🌎 Predeterminado": "com",
    "🇺🇸 Estados Unidos": "com",
    "🇬🇧 Reino Unido": "co.uk",
    "🇨🇦 Canadá": "ca",
    "🇦🇺 Australia": "com.au",
    "🇮🇳 India": "co.in",
    "🇮🇪 Irlanda": "ie",
    "🇿🇦 Sudáfrica": "co.za"
}


# ============================================================
# ESTILOS MEJORADOS (CSS)
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #f8fafc;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    /* Hero Banner */
    .hero-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #3b82f6 100%);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        color: white;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18);
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin: 0;
        color: #ffffff !important;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        color: #e0e7ff !important;
        font-weight: 500;
        margin-top: 0.4rem;
    }

    .author-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        backdrop-filter: blur(8px);
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #ffffff;
        font-weight: 600;
        border: 1px solid rgba(255, 255, 255, 0.25);
        margin-top: 0.8rem;
    }

    /* Cards 'Cómo Funciona' */
    .step-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.25rem 1.1rem;
        text-align: left;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03);
        height: 100%;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .step-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
    }

    .step-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    .step-title {
        font-weight: 700;
        color: #0f172a;
        font-size: 1.05rem;
        margin-bottom: 0.3rem;
    }

    .step-desc {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.45;
    }

    /* Sidebar Estilizada */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }

    section[data-testid="stSidebar"] .stSelectbox label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #334155;
    }

    /* Tabs para entradas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 44px;
        border-radius: 10px;
        font-weight: 600;
        color: #475569;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #2563eb !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    /* Botones */
    .stButton > button {
        border-radius: 12px;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        font-weight: 700;
        padding: 0.6rem 1.2rem;
        border: none;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 18px rgba(37, 99, 235, 0.35);
    }

    /* Badges de Idiomas */
    .lang-badge {
        display: inline-block;
        background: #f1f5f9;
        border: 1px solid #e2e8f0;
        color: #334155;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 3px;
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #94a3b8;
        font-size: 0.88rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FUNCIONES
# ============================================================

def clean_filename(text):
    filename = text[:30].strip()
    if not filename:
        filename = "translation"

    filename = "".join(
        character for character in filename
        if character.isalnum() or character in (" ", "_", "-")
    )

    filename = filename.replace(" ", "_")
    return filename if filename else "translation"


def remove_old_files(days=7):
    files = glob.glob(os.path.join(TEMP_FOLDER, "*.mp3"))
    current_time = time.time()
    maximum_age = days * 86400

    for file in files:
        try:
            file_time = os.stat(file).st_mtime
            if file_time < current_time - maximum_age:
                os.remove(file)
        except Exception:
            pass


def extract_text_from_image(image_bytes, tesseract_language, use_filter=False):
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        return "", None

    original_image = image.copy()

    if use_filter:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    try:
        detected_text = pytesseract.image_to_string(image, lang=tesseract_language)
    except Exception:
        try:
            detected_text = pytesseract.image_to_string(image, lang="eng")
        except Exception:
            detected_text = ""

    return detected_text.strip(), original_image


def translate_and_create_audio(source_language, destination_language, text, tld):
    translation = translator.translate(
        text,
        src=source_language,
        dest=destination_language
    )

    translated_text = translation.text
    filename = clean_filename(translated_text)
    audio_path = os.path.join(TEMP_FOLDER, filename + ".mp3")

    speech = gTTS(
        text=translated_text,
        lang=destination_language,
        tld=tld,
        slow=False
    )
    speech.save(audio_path)

    return audio_path, translated_text


# ============================================================
# LIMPIEZA
# ============================================================

remove_old_files(7)


# ============================================================
# HEADER / HERO BANNER
# ============================================================

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🌎 EasyTranslate</div>
        <div class="hero-subtitle">Traduce el mundo que te rodea en tiempo real</div>
        <div class="author-badge">✨ Desarrollado por Juan Pablo López Gallego</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR DE CONFIGURACIÓN
# ============================================================

with st.sidebar:
    st.title("⚙️ Configuración")
    st.caption("Ajusta las opciones de lectura y voz")

    st.markdown("---")

    st.subheader("🌐 Idiomas")

    input_language_name = st.selectbox(
        "Idioma del texto en la imagen:",
        LANGUAGE_LIST,
        index=st.session_state.get("input_index", 0),
        key="input_language_select"
    )

    input_language = LANGUAGES[input_language_name]["translation"]
    tesseract_language = LANGUAGES[input_language_name]["tesseract"]

    output_language_name = st.selectbox(
        "Traducir a:",
        LANGUAGE_LIST,
        index=st.session_state.get("output_index", 1),
        key="output_language_select"
    )

    output_language = LANGUAGES[output_language_name]["translation"]

    if st.button("⇄ Intercambiar idiomas", use_container_width=True):
        input_index = LANGUAGE_LIST.index(input_language_name)
        output_index = LANGUAGE_LIST.index(output_language_name)
        st.session_state["input_index"] = output_index
        st.session_state["output_index"] = input_index
        st.rerun()

    st.markdown("---")

    st.subheader("🔊 Opciones de Voz y Lectura")

    accent_name = st.selectbox(
        "Acento de la voz:",
        list(ACCENTS.keys())
    )
    tld = ACCENTS[accent_name]

    use_filter = st.checkbox("⚡ Mejorar contraste de imagen (OCR)", value=False)
    show_translation = st.checkbox("💬 Mostrar texto traducido", value=True)

    st.markdown("---")

    st.info("💡 **Consejo:** Asegúrate de tomar fotos nítidas con buena iluminación para mejorar el reconocimiento.")


# ============================================================
# PASOS - ¿CÓMO FUNCIONA?
# ============================================================

st.markdown("### ✨ ¿Cómo funciona?")

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">📷</div>
            <div class="step-title">1. Captura o Subida</div>
            <div class="step-desc">Toma una foto instantánea o carga un archivo con el texto que deseas traducir.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with step2:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">🔍</div>
            <div class="step-title">2. Extracción OCR</div>
            <div class="step-desc">Nuestro motor detecta e interpreta automáticamente los caracteres de la imagen.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with step3:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">🔊</div>
            <div class="step-title">3. Traducción y Audio</div>
            <div class="step-desc">Obtén el resultado escrito y escucha la pronunciación exacta con voz natural.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# SELECCIÓN DE IMAGEN (PESTAÑAS)
# ============================================================

st.markdown("### 📸 Selecciona o captura una imagen")

tab_upload, tab_camera = st.tabs(["📁 Subir Imagen", "📷 Tomar Foto"])

image_bytes = None

with tab_upload:
    uploaded_image = st.file_uploader(
        "Arrastra un archivo o haz clic para examinar",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )
    if uploaded_image is not None:
        image_bytes = uploaded_image.getvalue()

with tab_camera:
    camera_image = st.camera_input("Captura una fotografía", label_visibility="collapsed")
    if camera_image is not None and image_bytes is None:
        image_bytes = camera_image.getvalue()


# ============================================================
# PROCESAMIENTO Y OCR
# ============================================================

detected_text = ""

if image_bytes is not None:
    st.markdown("---")
    col_img, col_ocr = st.columns([1, 1], gap="medium")

    with col_img:
        st.subheader("🖼️ Imagen Cargada")
        st.image(image_bytes, use_container_width=True)

    with col_ocr:
        st.subheader("📝 Texto Detectado")
        with st.spinner("🔍 Analizando imagen con Tesseract OCR..."):
            detected_text, _ = extract_text_from_image(
                image_bytes,
                tesseract_language,
                use_filter
            )

        if detected_text:
            st.caption("Puedes corregir o editar el texto antes de traducirlo:")
            edited_text = st.text_area(
                "Texto editable",
                value=detected_text,
                height=200,
                label_visibility="collapsed"
            )
        else:
            st.warning("⚠️ No se reconoció texto en la imagen. Intenta con otra toma más clara o activa 'Mejorar contraste' en el panel lateral.")
            edited_text = ""
else:
    edited_text = ""


# ============================================================
# TRADUCCIÓN Y AUDIO
# ============================================================

if edited_text.strip():
    st.markdown("---")
    st.markdown("### 🌎 Resultado de Traducción")
    st.caption(f"Traduciendo de **{input_language_name}** a **{output_language_name}**")

    if st.button("🚀 Traducir y Generar Audio", use_container_width=True):
        try:
            with st.spinner("✨ Procesando traducción y audio..."):
                audio_path, translated_text = translate_and_create_audio(
                    input_language,
                    output_language,
                    edited_text,
                    tld
                )

            res_col1, res_col2 = st.columns(2)

            with res_col1:
                if show_translation:
                    st.subheader("💬 Texto Traducido")
                    st.success(translated_text)

            with res_col2:
                st.subheader("🔊 Audio Generado")
                with open(audio_path, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")

            st.toast("¡Traducción generada exitosamente!", icon="✅")

        except Exception as error:
            st.error("❌ Ocurrió un error al realizar la traducción.")
            st.caption(f"Detalle técnico: {error}")


# ============================================================
# IDIOMAS DISPONIBLES (EXPANDER LIMPIO)
# ============================================================

st.markdown("---")

with st.expander(f"🌍 Ver lista completa de idiomas soportados ({len(LANGUAGE_LIST)})"):
    badges_html = "".join([f'<span class="lang-badge">{lang}</span>' for lang in LANGUAGE_LIST])
    st.markdown(f"<div>{badges_html}</div>", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="custom-footer">
        🌎 <strong>EasyTranslate</strong> — Aplicación interactiva de OCR y traducción<br>
        Creado por <strong>Juan Pablo López Gallego</strong>
    </div>
    """,
    unsafe_allow_html=True
)
