import os
from telegram import Update
from telegram.ext import ContextTypes
from PyPDF2 import PdfReader, PdfWriter
from bot.utils.language_map import get_text
from bot.utils.cleanup import cleanup_user_temp

async def start_lock_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "en")
    context.user_data["lock_mode"] = True
    await query.edit_message_text(get_text(lang, "send_pdf_to_lock"))

async def handle_pdf_to_lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not context.user_data.get("lock_mode"):
        return

    document = update.message.document
    if not document.file_name.endswith(".pdf"):
        await update.message.reply_text("❌ Please send a valid PDF file.")
        return

    context.user_data["pdf_file"] = await document.get_file()
    context.user_data["pdf_filename"] = document.file_name

    await update.message.reply_text(get_text(lang, "ask_password"))

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")

    if not context.user_data.get("lock_mode") or "pdf_file" not in context.user_data:
        return

    password = update.message.text.strip()
    user_id = update.effective_user.id
    os.makedirs(f"/tmp/{user_id}", exist_ok=True)

    input_path = f"/tmp/{user_id}/{context.user_data['pdf_filename']}"
    output_path = f"/tmp/{user_id}/locked.pdf"

    await context.user_data["pdf_file"].download_to_drive(input_path)

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)
        writer.encrypt(password)

        with open(output_path, "wb") as f:
            writer.write(f)

        with open(output_path, "rb") as f:
            await update.message.reply_document(f, filename="locked.pdf")

        await update.message.reply_text(get_text(lang, "pdf_locked_success"))
    except Exception:
        await update.message.reply_text("❌ Failed to lock the PDF.")
    finally:
        context.user_data.clear()
        cleanup_user_temp(user_id)
