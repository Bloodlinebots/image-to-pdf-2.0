from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.language_map import get_text

language_names = {
    "en": "🇬🇧 English",
    "hi": "🇮🇳 हिंदी",
    "ru": "🇷🇺 Русский",
    "ar": "🇸🇦 العربية"
}

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("lang_"):
        lang_code = query.data.split("_")[1]
        context.user_data["lang"] = lang_code
        msg = get_text(lang_code, "start")
        await query.edit_message_text(
            text=f"✅ {language_names[lang_code]} selected.\n\n{msg}"
        )
    elif query.data == "lang_menu":
        keyboard = [
            [InlineKeyboardButton(name, callback_data=f"lang_{code}")]
            for code, name in language_names.items()
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🌐 Select your language:", reply_markup=reply_markup)
