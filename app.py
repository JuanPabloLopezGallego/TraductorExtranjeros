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
# IDIOMAS Y ACENTOS
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
# ESTILOS CSS REPARADOS (CORRECCIÓN DE CONTRASTE)
# ============================================================

st.markdown(
    """
    <style>

    /* Reset global de colores para evitar conflictos con Dark Mode */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* BARRA LATERAL (SIDEBAR) - Corrección de contraste */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #0f172a !important;
    }

    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] p {
        color: #334155 !important;
    }

    /* CAMPOS Y SELECTORES */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] * {
        color: #0f172a !important;
        background-color: transparent !important;
    }

    /* PESTAÑAS (TABS) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e2e8f0 !important;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        font-weight: 600;
        color: #475569 !important;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #2563eb !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    /* BOTONES */
    .stButton > button {
        width: 100%;
        min-height: 46px;
        border-radius: 10px;
        border: none;
        background: #2563eb !important;
        color: #ffffff !important;
        font-weight: 700;
        font-size: 15px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }

    .stButton > button * {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        background: #1d4ed8 !important;
    }

    /* HERO CARD */
    .hero-container {
        background: #ffffff;
        padding: 2.2rem 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f172a !important;
        margin-bottom: 0.2rem;
    }

    .hero-subtitle {
        font-size: 1.1rem;
        color: #64748b !important;
        margin-bottom: 0.8rem;
    }

    .author-badge {
        display: inline-block;
        background: #eff6ff;
        color: #2563eb !important;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* CARGADOR DE ARCHIVOS */
    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 1px dashed #cbd5e1 !important;
        border-radius: 12px;
    }

    [data-testid="stFileUploader"] * {
        color: #334155 !important;
    }

    /* CONTENEDORES DE PASOS */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 12px !important;
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] * {
        color: #0f172a !important;
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
    return filename or "translation"


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


remove_old_files(7)


# ============================================================
# ENCABEZADO PRINCIPAL (HERO)
# ============================================================

st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🌎 EasyTranslate</div>
        <div class="hero-subtitle">Traduce el mundo que te rodea en tiempo real</div>
        <div class="author-badge">Creado por Juan Pablo López Gallego</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR DE CONFIGURACIÓN
# ============================================================

with st.sidebar:
    st.subheader("⚙️ Configuración")
    st.write("---")

    st.markdown("##### 🌐 Idiomas")
    
    input_language_name = st.selectbox(
        "Idioma de la imagen:",
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

    if st.button("⇄ Intercambiar idiomas"):
        input_index = LANGUAGE_LIST.index(input_language_name)
        output_index = LANGUAGE_LIST.index(output_language_name)
        st.session_state["input_index"] = output_index
        st.session_state["output_index"] = input_index
        st.rerun()

    st.write("---")
    st.markdown("##### 🔊 Voz y Acento")

    accent_name = st.selectbox("Acentuación:", list(ACCENTS.keys()))
    tld = ACCENTS[accent_name]

    st.write("---")
    st.markdown("##### ✨ Procesamiento")

    use_filter = st.checkbox("Mejorar contraste imagen", value=False)
    show_translation = st.checkbox("Mostrar texto traducido", value=True)

    st.info("💡 Usa imágenes con buena iluminación para obtener mejores resultados.")


# ============================================================
# PASOS DE USO
# ============================================================

st.subheader("✨ ¿Cómo funciona?")
step1, step2, step3 = st.columns(3)

with step1:
    with st.container(border=True):
        st.markdown("**📷 1. Selecciona imagen**")
        st.caption("Sube un archivo o toma una foto directamente.")

with step2:
    with st.container(border=True):
        st.markdown("**🔍 2. Detección OCR**")
        st.caption("El texto se extrae y puedes corregirlo si lo necesitas.")

with step3:
    with st.container(border=True):
        st.markdown("**🔊 3. Traducción y Voz**")
        st.caption("Obtén el texto traducido y escucha su pronunciación.")

st.write("")


# ============================================================
# CARGAR IMAGEN (PESTAÑAS)
# ============================================================

st.subheader("📸 Captura o sube tu imagen")

tab_upload, tab_camera = st.tabs(["📁 Subir archivo", "📷 Usar Cámara"])

image_bytes = None

with tab_upload:
    uploaded_image = st.file_uploader(
        "Selecciona una imagen", 
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )
    if uploaded_image is not None:
        image_bytes = uploaded_image.getvalue()
        st.image(image_bytes, use_container_width=True, caption="Imagen seleccionada")

with tab_camera:
    camera_image = st.camera_input("Toma una fotografía", label_visibility="collapsed")
    if camera_image is not None:
        image_bytes = camera_image.getvalue()


# ============================================================
# PROCESAMIENTO Y TEXTO DETECTADO
# ============================================================

detected_text = ""

if image_bytes is not None:
    with st.spinner("🔍 Leyendo texto de la imagen..."):
        detected_text, _ = extract_text_from_image(
            image_bytes,
            tesseract_language,
            use_filter
        )

if detected_text:
    st.subheader("📝 Texto detectado")
    st.caption("Revisa o modifica el texto antes de traducir:")
    edited_text = st.text_area(
        "Texto a traducir", 
        value=detected_text, 
        height=140, 
        label_visibility="collapsed"
    )

elif image_bytes is not None:
    st.warning("⚠️ No se detectó texto. Intenta activar el filtro de mejora en la barra lateral o usa una imagen más clara.")
    edited_text = ""

else:
    edited_text = ""


# ============================================================
# TRADUCCIÓN
# ============================================================

if edited_text.strip():
    st.write("---")
    st.subheader("🌎 Traducción")
    st.write(f"Traduciendo de **{input_language_name}** a **{output_language_name}**")

    if st.button("✨ Traducir y Escuchar"):
        try:
            with st.spinner("Procesando traducción y voz..."):
                audio_path, translated_text = translate_and_create_audio(
                    input_language,
                    output_language,
                    edited_text,
                    tld
                )

            if show_translation:
                st.success(translated_text)

            st.markdown("##### 🔊 Pronunciación:")
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

        except Exception as error:
            st.error("❌ Ocurrió un error con la traducción.")
            st.caption(f"Detalle técnico: {error}")


# ============================================================
# IDIOMAS COMPATIBLES
# ============================================================

st.write("---")
with st.expander("🌍 Idiomas compatibles (31)"):
    lang_cols = st.columns(4)
    for idx, lang in enumerate(LANGUAGE_LIST):
        with lang_cols[idx % 4]:
            st.write(f"• {lang}")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding-top: 2rem;">
        EasyTranslate &bull; Desarrollado por <strong>Juan Pablo López Gallego</strong>
    </div>
    """,
    unsafe_allow_html=True
)
