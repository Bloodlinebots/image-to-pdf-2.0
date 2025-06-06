import os
from telegram import Update
from telegram.ext import ContextTypes
from PyPDF2 import PdfReader, PdfWriter
from bot.utils.language_map import get_text
from bot.utils.cleanup import cleanup_user_temp

async def start_unlock_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "en")
    context.user_data["unlock_mode"] = True
    await query.edit_message_text(get_text(lang, "send_pdf_to_unlock"))

async def handle_pdf_to_unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not context.user_data.get("unlock_mode"):
        return

    document = update.message.document
    if not document.file_name.endswith(".pdf"):
        await update.message.reply_text("❌ Please send a valid PDF file.")
        return

    context.user_data["locked_pdf"] = await document.get_file()
    context.user_data["locked_filename"] = document.file_name

    await update.message.reply_text(get_text(lang, "ask_unlock_password"))

async def handle_unlock_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not context.user_data.get("unlock_mode") or "locked_pdf" not in context.user_data:
        return

    password = update.message.text.strip()
    user_id = update.effective_user.id
    os.makedirs(f"/tmp/{user_id}", exist_ok=True)

    input_path = f"/tmp/{user_id}/{context.user_data['locked_filename']}"
    output_path = f"/tmp/{user_id}/unlocked.pdf"

    await context.user_data["locked_pdf"].download_to_drive(input_path)

    try:
        reader = PdfReader(input_path)
        if not reader.is_encrypted:
            await update.message.reply_text("⚠️ This PDF is not locked.")
            return

        if not reader.decrypt(password):
            await update.message.reply_text(get_text(lang, "wrong_password"))
            return

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        with open(output_path, "rb") as f:
            await update.message.reply_document(f, filename="unlocked.pdf")

        await update.message.reply_text(get_text(lang, "pdf_unlocked_success"))
    except Exception:
        await update.message.reply_text("❌ Failed to unlock the PDF.")
    finally:
        context.user_data.clear()
        cleanup_user_temp(user_id)
