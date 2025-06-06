import os
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language_map import get_text
from bot.utils.pdf_tools import create_pdf_from_text
from bot.utils.cleanup import cleanup_user_temp

async def start_text_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "en")
    context.user_data["text_mode"] = True
    await query.edit_message_text(get_text(lang, "send_text"))

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not context.user_data.get("text_mode"):
        return  # Ignore if not in text-to-pdf mode

    text = update.message.text.strip()
    user_id = update.effective_user.id

    os.makedirs(f"/tmp/{user_id}", exist_ok=True)
    output_path = f"/tmp/{user_id}/text_output.pdf"

    try:
        create_pdf_from_text(text, output_path)

        with open(output_path, "rb") as f:
            await update.message.reply_document(document=f, filename="text_output.pdf")

        await update.message.reply_text(get_text(lang, "pdf_ready"))
    except Exception:
        await update.message.reply_text("❌ Failed to convert text.")
    finally:
        context.user_data["text_mode"] = False
        cleanup_user_temp(user_id)
