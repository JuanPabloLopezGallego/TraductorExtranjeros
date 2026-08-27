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
        "tesser
