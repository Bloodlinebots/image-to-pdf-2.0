# 📦 Telegram PDF Converter Bot

A multilingual Telegram bot to convert PDFs: images, text, DOCX to PDF, extract PDF pages as images, and lock/unlock PDFs.

## 🌍 Supported Languages
- English
- हिन्दी (Hindi)
- العربية (Arabic)
- Русский (Russian)

---

## ⚙️ Features

- 🖼️ Convert Images to PDF
- 📝 Text to PDF
- 📄 DOCX to PDF
- 📸 PDF to Images
- 🔐 Lock PDF (password protect)
- 🔓 Unlock PDF (remove password)
- 🧹 Auto-cleanup temp files
- 🌐 Multi-language support

---

## 🧰 Requirements

- Python 3.11+
- Telegram Bot Token
- Heroku (or any server)
- poppler-utils (for PDF to image)

---

## 🚀 Deployment

### ✅ Local Setup

```bash
git clone https://github.com/your-username/pdf-bot.git
cd pdf-bot

# Create virtual env (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt
