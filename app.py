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

os.makedirs(TEMP_FOLDER, exist_ok=True)

translator = Translator()


# ============================================================
# IDIOMAS
# ============================================================

# Nombre mostrado:
#   bandera + idioma
#
# translation = código utilizado por Google Translate
#
# tesseract = código utilizado por Tesseract OCR

LANGUAGES = {
    "🇺🇸 English": {
        "translation": "en",
        "tesseract": "eng"
    },

    "🇪🇸 Español": {
        "translation": "es",
        "tesseract": "spa"
    },

    "🇫🇷 Français": {
        "translation": "fr",
        "tesseract": "fra"
    },

    "🇩🇪 Deutsch": {
        "translation": "de",
        "tesseract": "deu"
    },

    "🇮🇹 Italiano": {
        "translation": "it",
        "tesseract": "ita"
    },

    "🇵🇹 Português": {
        "translation": "pt",
        "tesseract": "por"
    },

    "🇧🇷 Português (Brasil)": {
        "translation": "pt",
        "tesseract": "por"
    },

    "🇳🇱 Nederlands": {
        "translation": "nl",
        "tesseract": "nld"
    },

    "🇷🇺 Русский": {
        "translation": "ru",
        "tesseract": "rus"
    },

    "🇺🇦 Українська": {
        "translation": "uk",
        "tesseract": "ukr"
    },

    "🇵🇱 Polski": {
        "translation": "pl",
        "tesseract": "pol"
    },

    "🇨🇿 Čeština": {
        "translation": "cs",
        "tesseract": "ces"
    },

    "🇸🇰 Slovenčina": {
        "translation": "sk",
        "tesseract": "slk"
    },

    "🇭🇺 Magyar": {
        "translation": "hu",
        "tesseract": "hun"
    },

    "🇷🇴 Română": {
        "translation": "ro",
        "tesseract": "ron"
    },

    "🇹🇷 Türkçe": {
        "translation": "tr",
        "tesseract": "tur"
    },

    "🇬🇷 Ελληνικά": {
        "translation": "el",
        "tesseract": "ell"
    },

    "🇸🇪 Svenska": {
        "translation": "sv",
        "tesseract": "swe"
    },

    "🇩🇰 Dansk": {
        "translation": "da",
        "tesseract": "dan"
    },

    "🇫🇮 Suomi": {
        "translation": "fi",
        "tesseract": "fin"
    },

    "🇳🇴 Norsk": {
        "translation": "no",
        "tesseract": "nor"
    },

    "🇮🇳 हिन्दी": {
        "translation": "hi",
        "tesseract": "hin"
    },

    "🇧🇩 বাংলা": {
        "translation": "bn",
        "tesseract": "ben"
    },

    "🇮🇩 Bahasa Indonesia": {
        "translation": "id",
        "tesseract": "ind"
    },

    "🇻🇳 Tiếng Việt": {
        "translation": "vi",
        "tesseract": "vie"
    },

    "🇹🇭 ไทย": {
        "translation": "th",
        "tesseract": "tha"
    },

    "🇰🇷 한국어": {
        "translation": "ko",
        "tesseract": "kor"
    },

    "🇯🇵 日本語": {
        "translation": "ja",
        "tesseract": "jpn"
    },

    "🇨🇳 简体中文": {
        "translation": "zh-cn",
        "tesseract": "chi_sim"
    },

    "🇹🇼 繁體中文": {
        "translation": "zh-tw",
        "tesseract": "chi_tra"
    },

    "🇸🇦 العربية": {
        "translation": "ar",
        "tesseract": "ara"
    },

    "🇮🇱 עברית": {
        "translation": "iw",
        "tesseract": "heb"
    }
}


LANGUAGE_NAMES = list(LANGUAGES.keys())


# ============================================================
# ACENTOS
# ============================================================

ACCENTS = {
    "🌎 Default": "com",
    "🇺🇸 United States": "com",
    "🇬🇧 United Kingdom": "co.uk",
    "🇨🇦 Canada": "ca",
    "🇦🇺 Australia": "com.au",
    "🇮🇳 India": "co.in",
    "🇮🇪 Ireland": "ie",
    "🇿🇦 South Africa": "co.za"
}


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
"""
<style>

/* =========================================================
   GENERAL
   ========================================================= */

.stApp {
    background:
        radial-gradient(
            circle at top right,
            rgba(74, 144, 226, 0.12),
            transparent 30%
        ),
        linear-gradient(
            135deg,
            #f5f8ff 0%,
            #eef4ff 50%,
            #f9fbff 100%
        );
}

.main {
    padding-top: 1rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    background: linear-gradient(
        135deg,
        #2563eb 0%,
        #4f8df7 50%,
        #60a5fa 100%
    );

    border-radius: 28px;

    padding: 45px 30px;

    margin-bottom: 30px;

    text-align: center;

    color: white;

    box-shadow:
        0 20px 45px rgba(37, 99, 235, 0.25);
}

.hero-icon {
    font-size: 55px;
    margin-bottom: 5px;
}

.hero-title {
    font-size: 44px;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 18px;
    opacity: 0.92;
    margin-top: 8px;
}


/* =========================================================
   TARJETAS
   ========================================================= */

.card {
    background: rgba(255,255,255,0.96);

    border: 1px solid #e6edf7;

    border-radius: 20px;

    padding: 24px;

    margin-bottom: 20px;

    box-shadow:
        0 8px 30px rgba(31, 65, 114, 0.07);
}

.card-title {
    color: #173b6c;

    font-size: 21px;

    font-weight: 750;

    margin-bottom: 5px;
}

.card-description {
    color: #718096;

    font-size: 14px;

    line-height: 1.6;
}


/* =========================================================
   PASOS
   ========================================================= */

.step-card {
    background: white;

    border-radius: 18px;

    border: 1px solid #e6edf7;

    padding: 22px 15px;

    text-align: center;

    height: 145px;

    box-shadow:
        0 7px 22px rgba(31, 65, 114, 0.06);

    transition: all 0.2s ease;
}

.step-card:hover {
    transform: translateY(-3px);

    box-shadow:
        0 12px 28px rgba(31, 65, 114, 0.11);
}

.step-icon {
    font-size: 35px;
}

.step-title {
    color: #173b6c;

    font-weight: 700;

    margin-top: 7px;
}

.step-description {
    color: #7b8799;

    font-size: 12px;

    margin-top: 4px;
}


/* =========================================================
   SECCIÓN
   ========================================================= */

.section-title {
    color: #173b6c;

    font-size: 25px;

    font-weight: 800;

    margin-top: 25px;

    margin-bottom: 12px;
}


/* =========================================================
   RESULTADOS
   ========================================================= */

.detected-box {
    background: #f8fbff;

    border: 2px solid #dbeafe;

    border-radius: 18px;

    padding: 18px;

    margin-top: 10px;
}

.translation-box {
    background: linear-gradient(
        135deg,
        #eff6ff,
        #f5f9ff
    );

    border: 2px solid #bfdbfe;

    border-radius: 18px;

    padding: 22px;

    margin-top: 15px;
}


/* =========================================================
   BOTONES
   ========================================================= */

.stButton > button {
    width: 100%;

    min-height: 48px;

    border: none;

    border-radius: 13px;

    background: linear-gradient(
        90deg,
        #2563eb,
        #3b82f6
    );

    color: white;

    font-weight: 750;

    font-size: 15px;

    transition: all 0.2s ease;

    box-shadow:
        0 5px 15px rgba(37, 99, 235, 0.18);
}

.stButton > button:hover {
    transform: translateY(-2px);

    background: linear-gradient(
        90deg,
        #1d4ed8,
        #2563eb
    );

    box-shadow:
        0 8px 20px rgba(37, 99, 235, 0.25);
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background: #ffffff;

    border-right: 1px solid #e4ebf5;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #173b6c;
}

.sidebar-title {
    color: #173b6c;

    font-size: 22px;

    font-weight: 800;

    margin-bottom: 10px;
}

.sidebar-section {
    color: #2563eb;

    font-size: 14px;

    font-weight: 750;

    margin-top: 20px;

    margin-bottom: 5px;
}


/* =========================================================
   UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {
    background: white;

    border-radius: 15px;
}


/* =========================================================
   TEXT AREA
   ========================================================= */

textarea {
    border-radius: 13px !important;
}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {
    text-align: center;

    color: #8a97aa;

    font-size: 12px;

    padding: 35px 0 10px 0;
}

</style>
""",
unsafe_allow_html=True
)


# ============================================================
# FUNCIONES
# ============================================================

def clean_filename(text):
    """
    Crea un nombre de archivo seguro para el audio.
    """

    name = text[:30].strip()

    if not name:
        name = "translation"

    name = "".join(
        character
        for character in name
        if character.isalnum()
        or character in (" ", "_", "-")
    )

    name = name.replace(" ", "_")

    if not name:
        name = "translation"

    return name


def text_to_speech(
    input_language,
    output_language,
    text,
    tld
):
    """
    Traduce el texto y genera el audio.
    """

    translation = translator.translate(
        text,
        src=input_language,
        dest=output_language
    )

    translated_text = translation.text

    filename = clean_filename(translated_text)

    audio_path = os.path.join(
        TEMP_FOLDER,
        f"{filename}.mp3"
    )

    tts = gTTS(
        text=translated_text,
        lang=output_language,
        tld=tld,
        slow=False
    )

    tts.save(audio_path)

    return audio_path, translated_text


def remove_old_files(days=7):
    """
    Elimina archivos MP3 antiguos.
    """

    files = glob.glob(
        os.path.join(TEMP_FOLDER, "*.mp3")
    )

    now = time.time()

    max_age = days * 86400

    for file in files:

        try:

            if os.stat(file).st_mtime < now - max_age:
                os.remove(file)

        except Exception:
            pass


def extract_text_from_image(
    image_bytes,
    tesseract_language,
    apply_filter=False
):
    """
    Extrae texto de una imagen utilizando Tesseract.
    """

    image_array = np.frombuffer(
        image_bytes,
        dtype=np.uint8
    )

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return "", None

    if apply_filter:

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.GaussianBlur(
            gray,
            (3, 3),
            0
        )

        image = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )[1]

    else:

        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

    try:

        text = pytesseract.image_to_string(
            image,
            lang=tesseract_language
        )

    except pytesseract.TesseractError:

        # Si el idioma de Tesseract no está instalado,
        # intentamos utilizar inglés como alternativa.

        try:

            text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

        except Exception:

            text = ""

    return text.strip(), image


# ============================================================
# LIMPIEZA
# ============================================================

remove_old_files(7)


# ============================================================
# HEADER
# ============================================================

st.markdown(
"""
<div class="hero">

    <div class="hero-icon">🌎</div>

    <div class="hero-title">
        EasyTranslate
    </div>

    <div class="hero-subtitle">
        Understand the world around you.
        Translate text from images and listen to the result.
    </div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">⚙️ Settings</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # --------------------------------------------------------
    # IDIOMA DE ORIGEN
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">🌐 IMAGE LANGUAGE</div>',
        unsafe_allow_html=True
    )

    input_language_name = st.selectbox(
        "What language is in the image?",
        LANGUAGE_NAMES,
        index=1
    )

    input_language = LANGUAGES[
        input_language_name
    ]["translation"]

    tesseract_language = LANGUAGES[
        input_language_name
    ]["tesseract"]


    # --------------------------------------------------------
    # IDIOMA DESTINO
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">🔄 TRANSLATION LANGUAGE</div>',
        unsafe_allow_html=True
    )

    default_output_index = (
        LANGUAGE_NAMES.index("🇺🇸 English")
    )

    output_language_name = st.selectbox(
        "Translate to:",
        LANGUAGE_NAMES,
        index=default_output_index
    )

    output_language = LANGUAGES[
        output_language_name
    ]["translation"]


    # --------------------------------------------------------
    # ACENTO
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">🔊 VOICE</div>',
        unsafe_allow_html=True
    )

    accent_name = st.selectbox(
        "Voice accent:",
        list(ACCENTS.keys())
    )

    tld = ACCENTS[accent_name]


    # --------------------------------------------------------
    # OCR
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">🔍 IMAGE PROCESSING</div>',
        unsafe_allow_html=True
    )

    apply_filter = st.checkbox(
        "✨ Improve image before reading",
        value=False
    )


    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-section">📄 RESULT</div>',
        unsafe_allow_html=True
    )

    display_output_text = st.checkbox(
        "Show translated text",
        value=True
    )


    # --------------------------------------------------------
    # INFORMACIÓN
    # --------------------------------------------------------

    st.markdown("---")

    st.info(
        "💡 For best results, use a clear image with "
        "good lighting and readable text."
    )


# ============================================================
# PASOS
# ============================================================

st.markdown(
    '<div class="section-title">✨ How does it work?</div>',
    unsafe_allow_html=True
)

step1, step2, step3 = st.columns(3)


with step1:

    st.markdown(
    """
    <div class="step-card">

        <div class="step-icon">📷</div>

        <div class="step-title">
            1. Take a photo
        </div>

        <div class="step-description">
            Photograph a menu, sign or document.
        </div>

    </div>
    """,
    unsafe_allow_html=True
    )


with step2:

    st.markdown(
    """
    <div class="step-card">

        <div class="step-icon">🔍</div>

        <div class="step-title">
            2. Detect text
        </div>

        <div class="step-description">
            We automatically recognize the words.
        </div>

    </div>
    """,
    unsafe_allow_html=True
    )


with step3:

    st.markdown(
    """
    <div class="step-card">

        <div class="step-icon">🔊</div>

        <div class="step-title">
            3. Listen
        </div>

        <div class="step-description">
            Hear the translation in your language.
        </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# ============================================================
# TÍTULO DE CAPTURA
# ============================================================

st.markdown(
    '<div class="section-title">📸 Choose an image</div>',
    unsafe_allow_html=True
)


st.markdown(
"""
<div class="card">

    <div class="card-title">
        📷 Camera or 📁 Upload
    </div>

    <div class="card-description">
        Take a picture with your camera or upload an
        existing image from your device.
    </div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# CÁMARA / UPLOAD
# ============================================================

camera_column, upload_column = st.columns(2)


camera_image = None
uploaded_image = None


# ============================================================
# CÁMARA
# ============================================================

with camera_column:

    st.markdown("### 📷 Camera")

    use_camera = st.checkbox(
        "Use camera"
    )

    if use_camera:

        camera_image = st.camera_input(
            "Take a photo"
        )


# ============================================================
# UPLOAD
# ============================================================

with upload_column:

    st.markdown("### 📁 Upload image")

    uploaded_image = st.file_uploader(
        "Choose an image",
        type=[
            "png",
            "jpg",
            "jpeg",
            "webp"
        ]
    )


# ============================================================
# VARIABLE DEL TEXTO
# ============================================================

detected_text = ""


# ============================================================
# PROCESAR IMAGEN SUBIDA
# ============================================================

if uploaded_image is not None:

    st.markdown(
        '<div class="section-title">🖼️ Your image</div>',
        unsafe_allow_html=True
    )

    image_bytes = uploaded_image.getvalue()

    pil_image = Image.open(
        uploaded_image
    )

    st.image(
        pil_image,
        use_container_width=True
    )

    detected_text, processed_image = extract_text_from_image(
        image_bytes,
        tesseract_language,
        apply_filter
    )


# ============================================================
# PROCESAR CÁMARA
# ============================================================

elif camera_image is not None:

    st.markdown(
        '<div class="section-title">🖼️ Your photo</div>',
        unsafe_allow_html=True
    )

    image_bytes = camera_image.getvalue()

    detected_text, processed_image = extract_text_from_image(
        image_bytes,
        tesseract_language,
        apply_filter
    )

    st.image(
        image_bytes,
        use_container_width=True
    )


# ============================================================
# TEXTO DETECTADO
# ============================================================

if detected_text:

    st.markdown(
        '<div class="section-title">📝 Detected text</div>',
        unsafe_allow_html=True
    )

    st.markdown(
    """
    <div class="detected-box">

        <div class="card-description">
            Review the detected text below.
            You can edit it before translating.
        </div>

    </div>
    """,
    unsafe_allow_html=True
    )

    edited_text = st.text_area(
        "Text detected:",
        value=detected_text,
        height=180,
        label_visibility="collapsed"
    )


# ============================================================
# NO TEXTO
# ============================================================

else:

    edited_text = ""

    st.markdown(
    """
    <div class="card">

        <div class="card-title">
            👋 Ready to translate?
        </div>

        <div class="card-description">
            Take a photo or upload an image containing text
            to get started.
        </div>

    </div>
    """,
    unsafe_allow_html=True
    )


# ============================================================
# TRADUCIR
# ============================================================

if edited_text.strip():

    st.markdown(
        '<div class="section-title">🌎 Translation</div>',
        unsafe_allow_html=True
    )

    translate_column, spacer = st.columns(
        [1, 2]
    )

    with translate_column:

        translate_button = st.button(
            "🌎 Translate & Listen",
            use_container_width=True
        )


    if translate_button:

        try:

            with st.spinner(
                "✨ Translating..."
            ):

                audio_path, translated_text = text_to_speech(
                    input_language,
                    output_language,
                    edited_text,
                    tld
                )


            # ------------------------------------------------
            # RESULTADO
            # ------------------------------------------------

            st.markdown(
            f"""
            <div class="translation-box">

                <div class="card-title">
                    💬 Translation
                </div>

                <div class="card-description">
                    {output_language_name}
                </div>

            </div>
            """,
            unsafe_allow_html=True
            )


            if display_output_text:

                st.text_area(
                    "Translated text:",
                    value=translated_text,
                    height=150,
                    label_visibility="collapsed"
                )


            # ------------------------------------------------
            # AUDIO
            # ------------------------------------------------

            st.markdown("### 🔊 Listen")

            with open(
                audio_path,
                "rb"
            ) as audio_file:

                audio_bytes = audio_file.read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )


            st.success(
                "✅ Translation completed successfully!"
            )


        except Exception as error:

            st.error(
                "❌ Something went wrong while translating."
            )

            st.caption(
                f"Technical information: {error}"
            )


# ============================================================
# INFORMACIÓN DE IDIOMAS
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">🌍 Supported languages</div>',
    unsafe_allow_html=True
)

st.markdown(
f"""
<div class="card">

    <div class="card-title">
        {len(LANGUAGE_NAMES)} languages available
    </div>

    <div class="card-description">
        English · Español · Français · Deutsch · Italiano ·
        Português · Nederlands · Русский · Українська · Polski ·
        Čeština · Slovenčina · Magyar · Română · Türkçe ·
        Ελληνικά · Svenska · Dansk · Suomi · Norsk · हिन्दी ·
        বাংলা · Bahasa Indonesia · Tiếng Việt · ไทย · 한국어 ·
        日本語 · 简体中文 · 繁體中文 · العربية · עברית
    </div>

</div>
""",
unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
"""
<div class="footer">

    🌎 EasyTranslate
    <br>
    Simple translation for travelers, students and foreigners.

</div>
""",
unsafe_allow_html=True
)
