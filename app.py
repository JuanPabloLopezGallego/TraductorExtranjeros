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
# ESTILOS MEJORADOS (CSS)
# ============================================================

st.markdown(
    """
    <style>

    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --text: #0f172a;
        --muted: #64748b;
        --heading: #1e293b;
        --border: #e2e8f0;
    }

    .stApp {
        background: #f8fafc;
        color: var(--text);
    }

    /* Ocultar elementos predeterminados */
    #MainMenu, footer { visibility: hidden; }

    .block-container {
        max-width: 1100px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Sidebar elegante */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid var(--border);
    }

    /* Pestañas estilizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e2e8f0;
        padding: 6px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        border-radius: 8px;
        font-weight: 600;
        color: #475569;
        border: none !important;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: var(--primary) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    /* Botones principales */
    .stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: #ffffff !important;
        font-weight: 700;
        font-size: 16px;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
    }

    /* Tarjeta de título / Hero */
    .hero-container {
        background: #ffffff;
        padding: 2.5rem 1.5rem;
        border-radius: 20px;
        border: 1px solid var(--border);
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 0.25rem;
    }

    .hero-subtitle {
        font-size: 1.15rem;
        color: #64748b;
        margin-bottom: 0.8rem;
    }

    .author-badge {
        display: inline-block;
        background: #eff6ff;
        color: #2563eb;
        padding: 0.3rem 0.9rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Ajuste de contenedores */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px !important;
        background-color: #ffffff;
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


# Limpieza de archivos antiguos
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
    st.title("⚙️ Configuración")
    st.write("---")

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

    if st.button("⇄ Intercambiar idiomas"):
        input_index = LANGUAGE_LIST.index(input_language_name)
        output_index = LANGUAGE_LIST.index(output_language_name)
        st.session_state["input_index"] = output_index
        st.session_state["output_index"] = input_index
        st.rerun()

    st.write("---")
    st.subheader("🔊 Audio y Voz")

    accent_name = st.selectbox("Selecciona la acentuación:", list(ACCENTS.keys()))
    tld = ACCENTS[accent_name]

    st.write("---")
    st.subheader("✨ Opciones adicionales")

    use_filter = st.checkbox("Mejorar contraste de la imagen (OCR)", value=False)
    show_translation = st.checkbox("Mostrar texto traducido", value=True)

    st.info("💡 **Consejo:** Para mejores resultados, usa imágenes con texto claro y buena iluminación.")


# ============================================================
# ¿CÓMO FUNCIONA? (TARJETAS MODULARES)
# ============================================================

st.subheader("✨ ¿Cómo funciona?")
step1, step2, step3 = st.columns(3)

with step1:
    with st.container(border=True):
        st.markdown("##### 📷 1. Selecciona la imagen")
        st.caption("Sube un archivo o toma una foto a un menú, cartel o documento.")

with step2:
    with st.container(border=True):
        st.markdown("##### 🔍 2. Detección automática")
        st.caption("Reconocemos el texto en la imagen y te dejamos editarlo si lo necesitas.")

with step3:
    with st.container(border=True):
        st.markdown("##### 🔊 3. Traducción y Audio")
        st.caption("Obtén el texto traducido al instante y escucha su pronunciación.")

st.write("")


# ============================================================
# SELECCIONAR IMAGEN (PESTAÑAS)
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
        st.image(image_bytes, use_container_width=True, caption="Imagen cargada")

with tab_camera:
    camera_image = st.camera_input("Toma una fotografía", label_visibility="collapsed")
    if camera_image is not None:
        image_bytes = camera_image.getvalue()


# ============================================================
# PROCESAMIENTO OCR Y RESULTADOS
# ============================================================

detected_text = ""

if image_bytes is not None:
    with st.spinner("🔍 Analizando imagen con OCR..."):
        detected_text, _ = extract_text_from_image(
            image_bytes,
            tesseract_language,
            use_filter
        )

if detected_text:
    st.subheader("📝 Texto detectado")
    st.caption("Puedes corregir el texto detectado a continuación antes de traducirlo:")
    edited_text = st.text_area(
        "Texto a traducir", 
        value=detected_text, 
        height=140, 
        label_visibility="collapsed"
    )

elif image_bytes is not None:
    st.warning("⚠️ No se pudo reconocer texto en la imagen. Intenta activar la mejora de imagen en la barra lateral o subir una foto más clara.")
    edited_text = ""

else:
    edited_text = ""


# ============================================================
# TRADUCCIÓN Y AUDIO
# ============================================================

if edited_text.strip():
    st.write("---")
    st.subheader("🌎 Resultado de la traducción")
    st.write(f"Traducción de **{input_language_name}** a **{output_language_name}**:")

    if st.button("✨ Traducir y Generar Audio"):
        try:
            with st.spinner("Traduciendo y generando voz..."):
                audio_path, translated_text = translate_and_create_audio(
                    input_language,
                    output_language,
                    edited_text,
                    tld
                )

            if show_translation:
                st.success(translated_text)

            st.markdown("##### 🔊 Escuchar pronunciación:")
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

        except Exception as error:
            st.error("❌ Ocurrió un error al procesar la traducción.")
            st.caption(f"Detalle técnico: {error}")


# ============================================================
# IDIOMAS DISPONIBLES (EXPANDER LIMPIO)
# ============================================================

st.write("---")
with st.expander("🌍 Ver los 31 idiomas compatibles"):
    lang_cols = st.columns(4)
    for idx, lang in enumerate(LANGUAGE_LIST):
        with lang_cols[idx % 4]:
            st.write(f"• {lang}")


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="text-align: center; color: #94a3b8; font-size: 0.85rem; padding-top: 2rem;">
        EasyTranslate &bull; Desarrollado por <strong>Juan Pablo López Gallego</strong>
    </div>
    """,
    unsafe_allow_html=True
)
