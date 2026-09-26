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
# ESTILOS CSS AVANZADOS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --primary: #2563eb;
        --primary-gradient: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        --accent-gradient: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        --text: #0f172a;
        --muted: #64748b;
        --bg-main: #f8fafc;
        --card-bg: #ffffff;
        --border: #e2e8f0;
    }

    /* Fondo de la app */
    .stApp {
        background-color: var(--bg-main);
        font-family: 'Inter', sans-serif;
    }

    /* Ocultar elementos por defecto de Streamlit */
    #MainMenu, footer { visibility: hidden; }

    /* Ajuste de contenedor */
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Hero Banner */
    .hero-container {
        background: #ffffff;
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.03);
        margin-bottom: 2rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: var(--muted);
        font-weight: 500;
        margin-bottom: 1rem;
    }

    .author-badge {
        display: inline-block;
        background: #eff6ff;
        color: #1d4ed8;
        padding: 0.35rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        border: 1px solid #bfdbfe;
    }

    /* Tarjetas de "Cómo funciona" */
    .step-card {
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 1.5rem;
        height: 100%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .step-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(37, 99, 235, 0.08);
        border-color: #cbd5e1;
    }

    .step-icon {
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }

    .step-title {
        font-weight: 700;
        color: #1e293b;
        font-size: 1.05rem;
        margin-bottom: 0.3rem;
    }

    .step-desc {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.4;
    }

    /* Estilos de Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid var(--border);
    }

    /* Botones primarios */
    .stButton > button {
        border-radius: 12px;
        background: var(--primary-gradient);
        color: white !important;
        font-weight: 600;
        border: none;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
    }

    /* Pestañas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        color: var(--muted);
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: var(--primary) !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: var(--muted);
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1rem;
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
            if os.stat(file).st_mtime < current_time - maximum_age:
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
    translation = translator.translate(text, src=source_language, dest=destination_language)
    translated_text = translation.text
    filename = clean_filename(translated_text)
    audio_path = os.path.join(TEMP_FOLDER, filename + ".mp3")

    speech = gTTS(text=translated_text, lang=destination_language, tld=tld, slow=False)
    speech.save(audio_path)

    return audio_path, translated_text


# ============================================================
# LIMPIEZA INICIAL
# ============================================================

remove_old_files(7)


# ============================================================
# HEADER PRINCIPAL (HERO SECTION)
# ============================================================

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🌎 EasyTranslate</div>
        <div class="hero-subtitle">Traduce al instante el texto contenido en tus imágenes y escúchalo</div>
        <div class="author-badge">Desarrollado por Juan Pablo López Gallego</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.title("⚙️ Configuración")
    
    st.markdown("### 🌐 Idiomas")
    
    input_language_name = st.selectbox(
        "Idioma origen (imagen):",
        LANGUAGE_LIST,
        index=st.session_state.get("input_index", 0),
        key="input_language_select"
    )

    output_language_name = st.selectbox(
        "Idioma destino (traducción):",
        LANGUAGE_LIST,
        index=st.session_state.get("output_index", 1),
        key="output_language_select"
    )

    if st.button("⇄ Intercambiar idiomas", use_container_width=True):
        input_index = LANGUAGE_LIST.index(input_language_name)
        output_index = LANGUAGE_LIST.index(output_language_name)
        st.session_state["input_index"] = output_index
        st.session_state["output_index"] = input_index
        st.rerun()

    input_language = LANGUAGES[input_language_name]["translation"]
    tesseract_language = LANGUAGES[input_language_name]["tesseract"]
    output_language = LANGUAGES[output_language_name]["translation"]

    st.markdown("---")
    st.markdown("### 🎙️ Voz & Opciones")

    accent_name = st.selectbox("Acento de audio:", list(ACCENTS.keys()))
    tld = ACCENTS[accent_name]

    use_filter = st.checkbox("Mejorar contraste de imagen (OCR)", value=False)
    show_translation = st.checkbox("Mostrar bloque de traducción", value=True)

    st.markdown("---")
    st.caption("💡 **Consejo:** Para un mejor reconocimiento, asegúrate de que la imagen tenga buena iluminación y un texto claro.")


# ============================================================
# CÓMO FUNCIONA
# ============================================================

st.markdown("### ✨ ¿Cómo funciona?")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">📸</div>
            <div class="step-title">1. Carga una imagen</div>
            <div class="step-desc">Toma una foto en tiempo real o sube una imagen desde tu dispositivo.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">🔍</div>
            <div class="step-title">2. Detección automática</div>
            <div class="step-desc">Extraemos el texto mediante reconocimiento óptico de caracteres (OCR).</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="step-card">
            <div class="step-icon">🔊</div>
            <div class="step-title">3. Traduce y escucha</div>
            <div class="step-desc">Obtén la traducción inmediata y escucha su pronunciación correcta.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")
st.write("")


# ============================================================
# SELECCIÓN DE IMAGEN (PESTAÑAS)
# ============================================================

st.markdown("### 📸 Captura o selecciona una imagen")

tab_upload, tab_camera = st.tabs(["📁 Subir archivo", "📷 Usar Cámara"])

uploaded_image = None
camera_image = None

with tab_upload:
    uploaded_image = st.file_uploader(
        "Arrastra o selecciona una imagen",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )

with tab_camera:
    camera_image = st.camera_input(
        "Toma una fotografía",
        label_visibility="collapsed"
    )


# ============================================================
# PROCESAMIENTO Y RESULTADOS
# ============================================================

image_bytes = None

if uploaded_image is not None:
    image_bytes = uploaded_image.getvalue()
elif camera_image is not None:
    image_bytes = camera_image.getvalue()

detected_text = ""

if image_bytes is not None:
    col_img, col_txt = st.columns([1, 1], gap="medium")
    
    with col_img:
        st.markdown("#### 🖼️ Vista previa")
        st.image(image_bytes, use_container_width=True)

    with st.spinner("🔍 Reconociendo texto en la imagen..."):
        detected_text, _ = extract_text_from_image(
            image_bytes,
            tesseract_language,
            use_filter
        )

    with col_txt:
        st.markdown("#### 📝 Texto detectado")
        if detected_text:
            edited_text = st.text_area(
                "Puedes corregir el texto si es necesario:",
                value=detected_text,
                height=180
            )
        else:
            st.warning("⚠️ No se detectó texto en la imagen. Prueba activando 'Mejorar contraste' en el panel lateral o usa otra imagen.")
            edited_text = ""
else:
    edited_text = ""


# ============================================================
# TRADUCCIÓN Y AUDIO
# ============================================================

if edited_text.strip():
    st.markdown("---")
    st.markdown(f"### 🌎 Traducción (`{input_language_name}` → `{output_language_name}`)")

    if st.button("✨ Traducir y Generar Audio", use_container_width=True):
        try:
            with st.spinner("Traduciendo y generando voz..."):
                audio_path, translated_text = translate_and_create_audio(
                    input_language,
                    output_language,
                    edited_text,
                    tld
                )

            res_col1, res_col2 = st.columns([2, 1], gap="medium")

            with res_col1:
                if show_translation:
                    st.success(translated_text)

            with res_col2:
                st.markdown("##### 🔊 Escuchar pronunciación")
                with open(audio_path, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")

        except Exception as error:
            st.error("❌ Ocurrió un error al procesar la traducción.")
            st.caption(f"Detalle técnico: {error}")


# ============================================================
# IDIOMAS DISPONIBLES
# ============================================================

with st.expander(f"🌍 Ver los {len(LANGUAGE_LIST)} idiomas compatibles"):
    lang_cols = st.columns(4)
    for idx, lang in enumerate(LANGUAGE_LIST):
        with lang_cols[idx % 4]:
            st.write(lang)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    """
    <div class="footer-text">
        <strong>EasyTranslate</strong> — Aplicación Web de Reconocimiento y Traducción de Texto<br>
        Creado por <strong>Juan Pablo López Gallego</strong>
    </div>
    """,
    unsafe_allow_html=True
)
