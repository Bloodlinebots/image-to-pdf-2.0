import json
import os

# Supported languages
LANGUAGES = ["en", "hi", "ru", "ar"]

# Load all language files into memory
language_data = {}

for lang in LANGUAGES:
    file_path = os.path.join(os.path.dirname(__file__), f"../../locales/{lang}.json")
    with open(file_path, "r", encoding="utf-8") as f:
        language_data[lang] = json.load(f)

def get_text(lang_code: str, key: str) -> str:
    lang = lang_code if lang_code in language_data else "en"
    return language_data[lang].get(key, f"[{key}]")
