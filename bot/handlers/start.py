from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils.language_map import get_text

def main_menu(lang_code):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📷 Image ➡️ PDF", callback_data="image2pdf")],
        [InlineKeyboardButton("📝 Text ➡️ PDF", callback_data="text2pdf")],
        [InlineKeyboardButton("📄 DOCX ➡️ PDF", callback_data="docx2pdf")],
        [InlineKeyboardButton("📂 PDF ➡️ Images", callback_data="pdf2images")],
        [InlineKeyboardButton("🔐 Lock PDF", callback_data="lockpdf")],
        [InlineKeyboardButton("🔓 Unlock PDF", callback_data="unlockpdf")],
        [InlineKeyboardButton("🌐 Language / भाषा / язык / اللغة", callback_data="lang_menu")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang_code = context.user_data.get("lang", "en")
    text = get_text(lang_code, "start")

    await update.message.reply_text(
        text,
        reply_markup=main_menu(lang_code)
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = context.user_data.get("lang", "en")
    text = get_text(lang_code, "help")

    await update.message.reply_text(text)
