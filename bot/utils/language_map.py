from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Language codes mapped to their native names
LANGUAGE_NAMES = {
    "en": "English 🇬🇧",
    "hi": "हिन्दी 🇮🇳",
    "ar": "العربية 🇸🇦",
    "ru": "Русский 🇷🇺"
}

def get_language_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=name, callback_data=f"lang_{code}")
        for code, name in LANGUAGE_NAMES.items()
    ]
    keyboard.add(*buttons)
    return keyboard
