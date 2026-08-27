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

    "🇪🇸 Español": {
        "translation": "es",
        "tesseract": "spa"
    },

    "🇺🇸 English": {
        "translation": "en",
        "tesseract": "eng"
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
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       FONDO GENERAL
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
       TÍTULOS
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
       UPLOADER
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
       ALERTAS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }


    /* ======================================================
       FOOTER
       ====================================================== */

    .footer-text {
        text-align: center;

        color: #718096;

        font-size: 13px;

        padding-top: 25px;

        padding-bottom: 10px;
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

    try:

        detected_text = pytesseract.image_to_string(
            image,
            lang=tesseract_language
        )

    except Exception:

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
# LIMPIEZA
# ============================================================

remove_old_files(7)


# ============================================================
# HEADER PRINCIPAL
# ============================================================

st.title("🌎 EasyTranslate")

st.subheader(
    "Traduce el mundo que te rodea"
)
st.subheader(
    "Hecho por Juan Pablo López Gallego"
)
st.write(
    "📷 Toma una foto o sube una imagen, "
    "detecta el texto, tradúcelo y escucha el resultado."
)


st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Configuración")

    st.divider()


    # --------------------------------------------------------
    # IDIOMA DE LA IMAGEN
    # --------------------------------------------------------

    st.subheader("🌐 Idioma de la imagen")

    input_language_name = st.selectbox(
        "¿En qué idioma está el texto?",
        LANGUAGE_LIST,
        index=0
    )

    input_language = LANGUAGES[
        input_language_name
    ]["translation"]

    tesseract_language = LANGUAGES[
        input_language_name
    ]["tesseract"]


    # --------------------------------------------------------
    # IDIOMA DE TRADUCCIÓN
    # --------------------------------------------------------

    st.subheader("🔄 Idioma de traducción")

    output_language_name = st.selectbox(
        "¿A qué idioma quieres traducir?",
        LANGUAGE_LIST,
        index=1
    )

    output_language = LANGUAGES[
        output_language_name
    ]["translation"]


    # --------------------------------------------------------
    # INTERCAMBIAR IDIOMAS
    # --------------------------------------------------------

    if st.button("⇄ Intercambiar idiomas"):

        input_index = LANGUAGE_LIST.index(
            input_language_name
        )

        output_index = LANGUAGE_LIST.index(
            output_language_name
        )

        st.session_state["input_index"] = output_index
        st.session_state["output_index"] = input_index

        st.rerun()


    # --------------------------------------------------------
    # ACENTO
    # --------------------------------------------------------

    st.subheader("🔊 Voz")

    accent_name = st.selectbox(
        "Selecciona el acento:",
        list(ACCENTS.keys())
    )

    tld = ACCENTS[accent_name]


    # --------------------------------------------------------
    # PROCESAMIENTO
    # --------------------------------------------------------

    st.subheader("✨ Procesamiento de imagen")

    use_filter = st.checkbox(
        "Mejorar imagen antes de leerla",
        value=False
    )


    # --------------------------------------------------------
    # RESULTADO
    # --------------------------------------------------------

    st.subheader("📄 Resultado")

    show_translation = st.checkbox(
        "Mostrar texto traducido",
        value=True
    )


    st.divider()


    st.info(
        "💡 Consejo: utiliza una imagen clara y con "
        "buena iluminación para obtener mejores resultados."
    )


# ============================================================
# PASOS
# ============================================================

st.header("✨ ¿Cómo funciona?")

step1, step2, step3 = st.columns(3)


with step1:

    st.info(
        "📷 **1. Toma una foto**\n\n"
        "Fotografía un menú, señal, documento o cualquier texto."
    )


with step2:

    st.info(
        "🔍 **2. Detectamos el texto**\n\n"
        "La aplicación reconoce automáticamente las palabras."
    )


with step3:

    st.info(
        "🔊 **3. Escucha la traducción**\n\n"
        "Traduce el texto y escucha cómo se pronuncia."
    )


st.divider()


# ============================================================
# SELECCIONAR IMAGEN
# ============================================================

st.header("📸 Selecciona una imagen")

st.write(
    "Puedes utilizar la cámara o subir una imagen "
    "que ya tengas en tu dispositivo."
)


camera_column, upload_column = st.columns(2)


camera_image = None
uploaded_image = None


# ============================================================
# CÁMARA
# ============================================================

with camera_column:

    st.subheader("📷 Cámara")

    use_camera = st.checkbox(
        "Usar cámara"
    )

    if use_camera:

        camera_image = st.camera_input(
            "Toma una foto"
        )


# ============================================================
# SUBIR IMAGEN
# ============================================================

with upload_column:

    st.subheader("📁 Subir imagen")

    uploaded_image = st.file_uploader(
        "Selecciona una imagen",
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
# IMAGEN SUBIDA
# ============================================================

if uploaded_image is not None:

    image_bytes = uploaded_image.getvalue()

    st.divider()

    st.subheader("🖼️ Imagen seleccionada")

    try:

        image = Image.open(
            uploaded_image
        )

        st.image(
            image,
            use_container_width=True
        )

    except Exception:

        st.error(
            "No se ha podido abrir la imagen."
        )


# ============================================================
# IMAGEN DE CÁMARA
# ============================================================

elif camera_image is not None:

    image_bytes = camera_image.getvalue()

    st.divider()

    st.subheader("🖼️ Fotografía")

    st.image(
        image_bytes,
        use_container_width=True
    )


# ============================================================
# OCR
# ============================================================

if image_bytes is not None:

    with st.spinner(
        "🔍 Analizando la imagen..."
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

    st.header("📝 Texto detectado")

    st.write(
        "Revisa el texto antes de traducirlo. "
        "También puedes modificarlo manualmente."
    )

    edited_text = st.text_area(
        "Texto detectado",
        value=detected_text,
        height=180,
        label_visibility="collapsed"
    )


# ============================================================
# IMAGEN SIN TEXTO
# ============================================================

elif image_bytes is not None:

    st.warning(
        "⚠️ No se ha detectado ningún texto. "
        "Prueba con una imagen más clara o activa "
        "el procesamiento de imagen."
    )

    edited_text = ""


# ============================================================
# SIN IMAGEN
# ============================================================

else:

    edited_text = ""

    st.divider()

    st.info(
        "👋 **¡Listo para comenzar!**\n\n"
        "Toma una fotografía o sube una imagen que contenga texto."
    )


# ============================================================
# TRADUCCIÓN
# ============================================================

if edited_text.strip():

    st.divider()

    st.header("🌎 Traducción")

    st.write(
        f"**{input_language_name} → {output_language_name}**"
    )

    translate_button = st.button(
        "🌎 Traducir y escuchar"
    )


    if translate_button:

        try:

            with st.spinner(
                "✨ Traduciendo..."
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

                st.subheader(
                    "💬 Texto traducido"
                )

                st.success(
                    translated_text
                )


            # ------------------------------------------------
            # AUDIO
            # ------------------------------------------------

            st.subheader(
                "🔊 Escuchar"
            )

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
                "✅ ¡Traducción completada!"
            )


        except Exception as error:

            st.error(
                "❌ Ha ocurrido un problema al realizar "
                "la traducción."
            )

            st.caption(
                f"Información técnica: {error}"
            )


# ============================================================
# IDIOMAS DISPONIBLES
# ============================================================

st.divider()

st.header("🌍 Idiomas disponibles")

st.write(
    f"Actualmente puedes utilizar **{len(LANGUAGE_LIST)} idiomas:**"
)


language_columns = st.columns(4)


for index, language in enumerate(LANGUAGE_LIST):

    with language_columns[index % 4]:

        st.write(language)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    "<div class='footer-text'>"
    "🌎 EasyTranslate<br>"
    "Hecho por <strong>Juan Pablo López Gallego</strong>"
    "</div>",
    unsafe_allow_html=True
)
