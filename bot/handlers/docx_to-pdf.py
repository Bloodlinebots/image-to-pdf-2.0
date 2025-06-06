import os
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language_map import get_text
from bot.utils.docx_to_pdf_converter import convert_docx_to_pdf
from bot.utils.cleanup import cleanup_user_temp

async def start_docx_to_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    lang = context.user_data.get("lang", "en")
    await query.edit_message_text(get_text(lang, "send_docx"))

async def handle_docx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get("lang", "en")
    document = update.message.document

    if not document.file_name.endswith(".docx"):
        await update.message.reply_text("❌ Please send a valid .docx file.")
        return

    user_id = update.effective_user.id
    os.makedirs(f"/tmp/{user_id}", exist_ok=True)

    input_path = f"/tmp/{user_id}/{document.file_name}"
    output_path = f"/tmp/{user_id}/converted.pdf"

    file = await document.get_file()
    await file.download_to_drive(input_path)

    try:
        convert_docx_to_pdf(input_path, output_path)

        with open(output_path, "rb") as f:
            await update.message.reply_document(document=f, filename="converted.pdf")

        await update.message.reply_text(get_text(lang, "pdf_ready"))
    except Exception as e:
        await update.message.reply_text("❌ Failed to convert DOCX.")
    finally:
        cleanup_user_temp(user_id)
