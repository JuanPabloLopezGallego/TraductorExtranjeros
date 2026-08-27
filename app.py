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
# CONFIGURACIÓN
# ============================================================

TEMP_FOLDER = "temp"

if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)

translator = Translator()


# ============================================================
# IDIOMAS
# ============================================================

# translation = código utilizado por Google Translate / gTTS
#
# tesseract = código utilizado por Tesseract OCR
#
# Si un idioma de Tesseract no está instalado en el equipo,
# el programa utilizará inglés como respaldo.

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


LANGUAGE_LIST = list(LANGUAGES.keys())


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
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GENERAL
       ====================================================== */

    .stApp {
        background: linear-gradient(
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

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5eaf2;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #173b6c;
    }

    /* ======================================================
       TITULOS
       ====================================================== */

    h1 {
        color: #173b6c !important;
        font-weight: 800 !important;
    }

    h2 {
        color: #173b6c !important;
        font-weight: 750 !important;
    }

    h3 {
        color: #173b6c !important;
        font-weight: 700 !important;
    }

    /* ======================================================
       BOTONES
       ====================================================== */

    .stButton > button {
        width: 100%;
        min-height: 48px;

        border-radius: 14px;

        border: none;

        background: linear-gradient(
            90deg,
            #2563eb,
            #3b82f6
        );

        color: white;

        font-weight: 700;

        font-size: 15px;

        box-shadow:
            0 6px 18px rgba(37, 99, 235, 0.20);

        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #1d4ed8,
            #2563eb
        );

        transform: translateY(-2px);

        box-shadow:
            0 10px 25px rgba(37, 99, 235, 0.28);
    }

    /* ======================================================
       FILE UPLOADER
       ====================================================== */

    [data-testid="stFileUploader"] {
        background-color: white;
        border-radius: 15px;
    }

    /* ======================================================
       TEXT AREA
       ====================================================== */

    textarea {
        border-radius: 14px !important;
    }

    /* ======================================================
       SELECTBOX
       ====================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 12px;
    }

    /* ======================================================
       AUDIO
       ====================================================== */

    audio {
        width: 100%;
    }

    /* ======================================================
       INFO / SUCCESS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer-text {
        text-align: center;
        color: #8a97aa;
        font-size: 13px;
        padding-top: 30px;
        padding-bottom: 15px;
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
        character
        for character in filename
        if character.isalnum()
        or character in (" ", "_", "-")
    )

    filename = filename.replace(" ", "_")

    if not filename:
        filename = "translation"

    return filename


def remove_old_files(days=7):

    files = glob.glob(
        os.path.join(
            TEMP_FOLDER,
            "*.mp3"
        )
    )

    current_time = time.time()

    maximum_age = days * 86400

    for file in files:

        try:

            file_time = os.stat(file).st_mtime

            if file_time < current_time - maximum_age:
                os.remove(file)

        except Exception:
            pass


def extract_text_from_image(
    image_bytes,
    tesseract_language,
    use_filter=False
):

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

    original_image = image.copy()

    if use_filter:

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

    # --------------------------------------------------------
    # INTENTAR CON EL IDIOMA SELECCIONADO
    # --------------------------------------------------------

    try:

        detected_text = pytesseract.image_to_string(
            image,
            lang=tesseract_language
        )

    except Exception:

        # ----------------------------------------------------
        # FALLBACK A INGLÉS
        # ----------------------------------------------------

        try:

            detected_text = pytesseract.image_to_string(
                image,
                lang="eng"
            )

        except Exception:

            detected_text = ""

    return detected_text.strip(), original_image


def translate_and_create_audio(
    source_language,
    destination_language,
    text,
    tld
):

    translation = translator.translate(
        text,
        src=source_language,
        dest=destination_language
    )

    translated_text = translation.text

    filename = clean_filename(
        translated_text
    )

    audio_path = os.path.join(
        TEMP_FOLDER,
        filename + ".mp3"
    )

    speech = gTTS(
        text=translated_text,
        lang=destination_language,
        tld=tld,
        slow=False
    )

    speech.save(audio_path)

    return audio_path, translated_text


# ============================================================
# LIMPIAR AUDIOS ANTIGUOS
# ============================================================

remove_old_files(7)


# ============================================================
# HEADER
# ============================================================

st.title("🌎 EasyTranslate")

st.markdown(
    "### Understand the world around you"
)

st.write(
    "📷 Take a photo or upload an image, "
    "detect the text, translate it and listen to the result."
)


st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Settings")

    st.divider()

    # --------------------------------------------------------
    # IDIOMA DE ORIGEN
    # --------------------------------------------------------

    st.subheader("🌐 Image language")

    input_language_name = st.selectbox(
        "What language is in the image?",
        LANGUAGE_LIST,
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

    st.subheader("🔄 Translation language")

    output_language_name = st.selectbox(
        "Translate to:",
        LANGUAGE_LIST,
        index=0
    )

    output_language = LANGUAGES[
        output_language_name
    ]["translation"]


    # --------------------------------------------------------
    # INTERCAMBIAR IDIOMAS
    # --------------------------------------------------------

    if st.button("⇄ Swap languages"):

        current_input = input_language_name
        current_output = output_language_name

        # Guardamos los valores en session state
        st.session_state["input_language"] = current_output
        st.session_state["output_language"] = current_input

        st.rerun()


    # --------------------------------------------------------
    # ACENTO
    # --------------------------------------------------------

    st.subheader("🔊 Voice")

    accent_name = st.selectbox(
        "Voice accent:",
        list(ACCENTS.keys())
    )

    tld = ACCENTS[accent_name]


    # --------------------------------------------------------
    # PROCESAMIENTO
    # --------------------------------------------------------

    st.subheader("✨ Image processing")

    use_filter = st.checkbox(
        "Improve image before reading",
        value=False
    )


    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    st.subheader("📄 Result")

    show_translation = st.checkbox(
        "Show translated text",
        value=True
    )


    st.divider()

    st.info(
        "💡 Tip: Use a clear photo with good lighting "
        "for better text recognition."
    )


# ============================================================
# SECCIÓN DE PASOS
# ============================================================

st.header("✨ How does it work?")

step1, step2, step3 = st.columns(3)


with step1:

    st.info(
        "📷 **1. Take a photo**\n\n"
        "Photograph a menu, sign, document or any text."
    )


with step2:

    st.info(
        "🔍 **2. Detect the text**\n\n"
        "The application automatically reads the image."
    )


with step3:

    st.info(
        "🔊 **3. Listen**\n\n"
        "Translate the text and listen to the pronunciation."
    )


st.divider()


# ============================================================
# SECCIÓN DE IMAGEN
# ============================================================

st.header("📸 Choose an image")

st.write(
    "You can use your camera or upload an existing image."
)


camera_column, upload_column = st.columns(2)


camera_image = None
uploaded_image = None


# ============================================================
# CÁMARA
# ============================================================

with camera_column:

    st.subheader("📷 Camera")

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

    st.subheader("📁 Upload image")

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
# VARIABLES
# ============================================================

detected_text = ""

image_bytes = None


# ============================================================
# PROCESAR IMAGEN SUBIDA
# ============================================================

if uploaded_image is not None:

    image_bytes = uploaded_image.getvalue()

    st.divider()

    st.subheader("🖼️ Selected image")

    try:

        image = Image.open(
            uploaded_image
        )

        st.image(
            image,
            use_container_width=True
        )

    except Exception as error:

        st.error(
            "Unable to open the image."
        )


# ============================================================
# PROCESAR CÁMARA
# ============================================================

elif camera_image is not None:

    image_bytes = camera_image.getvalue()

    st.divider()

    st.subheader("🖼️ Your photo")

    st.image(
        image_bytes,
        use_container_width=True
    )


# ============================================================
# OCR
# ============================================================

if image_bytes is not None:

    with st.spinner(
        "🔍 Reading text from the image..."
    ):

        detected_text, original_image = (
            extract_text_from_image(
                image_bytes,
                tesseract_language,
                use_filter
            )
        )


# ============================================================
# TEXTO DETECTADO
# ============================================================

if detected_text:

    st.divider()

    st.header("📝 Detected text")

    st.write(
        "Review the detected text. "
        "You can edit it before translating."
    )

    edited_text = st.text_area(
        "Detected text",
        value=detected_text,
        height=180,
        label_visibility="collapsed"
    )


elif image_bytes is not None:

    st.warning(
        "⚠️ No text was detected in this image. "
        "Try a clearer photo or activate image processing."
    )

    edited_text = ""


else:

    edited_text = ""

    st.divider()

    st.info(
        "👋 **Ready to translate?**\n\n"
        "Take a photo or upload an image containing text."
    )


# ============================================================
# TRADUCCIÓN
# ============================================================

if edited_text.strip():

    st.divider()

    st.header("🌎 Translation")

    st.write(
        f"**{input_language_name} → {output_language_name}**"
    )

    translate_button = st.button(
        "🌎 Translate & Listen"
    )

    if translate_button:

        try:

            with st.spinner(
                "✨ Translating..."
            ):

                audio_path, translated_text = (
                    translate_and_create_audio(
                        input_language,
                        output_language,
                        edited_text,
                        tld
                    )
                )


            # ------------------------------------------------
            # TEXTO TRADUCIDO
            # ------------------------------------------------

            if show_translation:

                st.subheader("💬 Translated text")

                st.success(
                    translated_text
                )


            # ------------------------------------------------
            # AUDIO
            # ------------------------------------------------

            st.subheader("🔊 Listen")

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
                "✅ Translation completed!"
            )


        except Exception as error:

            st.error(
                "❌ There was a problem while translating."
            )

            st.caption(
                f"Technical information: {error}"
            )


# ============================================================
# IDIOMAS
# ============================================================

st.divider()

st.header("🌍 Supported languages")

st.write(
    f"**{len(LANGUAGE_LIST)} languages available:**"
)

language_columns = st.columns(4)

for index, language in enumerate(LANGUAGE_LIST):

    with language_columns[index % 4]:

        st.write(language)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌎 EasyTranslate · Simple translation for travelers, "
    "students and foreigners."
)
