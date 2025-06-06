import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

import os
BOT_TOKEN = os.environ["BOT_TOKEN"]
from bot.handlers import (
    start,
    language,
    image_to_pdf,
    text_to_pdf,
    docx_to_pdf,
    pdf_to_images,
    lock_pdf,
    unlock_pdf,
    done
)

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update.message:
        await update.message.reply_text("⚠️ An unexpected error occurred.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("help", start.help_command))
    app.add_handler(CommandHandler("done", done.done))

    # Language
    app.add_handler(CallbackQueryHandler(language.set_language, pattern="^lang_"))

    # Features (image → pdf, text → pdf, etc.)
    app.add_handler(CallbackQueryHandler(image_to_pdf.start_image_to_pdf, pattern="^image2pdf$"))
    app.add_handler(MessageHandler(filters.PHOTO, image_to_pdf.handle_image))

    app.add_handler(CallbackQueryHandler(text_to_pdf.start_text_to_pdf, pattern="^text2pdf$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_to_pdf.handle_text))

    app.add_handler(CallbackQueryHandler(docx_to_pdf.start_docx_to_pdf, pattern="^docx2pdf$"))
    app.add_handler(MessageHandler(filters.Document.MimeType("application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
                                   docx_to_pdf.handle_docx))

    app.add_handler(CallbackQueryHandler(pdf_to_images.start_pdf_to_images, pattern="^pdf2images$"))
    # ✅ FIXED LINE:
    app.add_handler(MessageHandler(filters.Document.PDF, pdf_to_images.handle_pdf_for_images))

    app.add_handler(CallbackQueryHandler(lock_pdf.start_lock_pdf, pattern="^lockpdf$"))
    app.add_handler(MessageHandler(filters.Document.PDF, lock_pdf.handle_lock_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lock_pdf.receive_password))

    app.add_handler(CallbackQueryHandler(unlock_pdf.start_unlock_pdf, pattern="^unlockpdf$"))
    app.add_handler(MessageHandler(filters.Document.PDF, unlock_pdf.handle_unlock_pdf))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unlock_pdf.receive_unlock_password))

    # Error handler
    app.add_error_handler(error_handler)

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
