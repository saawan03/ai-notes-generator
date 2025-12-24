# 🤖 AI Notes Generator & Summarizer

An AI-powered web application that converts long text or PDF documents into **concise summaries, bullet-point notes, and exam-oriented questions**.  
Built to help students study smarter and faster.

---

## ✨ Features

- 🧠 **AI Text Summarization**
- 📄 **PDF Upload & Processing**
- 📝 **Bullet-Point Notes Generation**
- ❓ **Exam-Oriented Question Generation**
- 📥 **Download Notes as TXT or PDF**
- 🌙 **Modern Dark Mode UI**
- ⚡ **Optimized & Stable AI Model**

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask

### AI / NLP
- Hugging Face Transformers
- DistilBART (`sshleifer/distilbart-cnn-12-6`)

### Frontend
- HTML5
- Bootstrap 5
- Custom Dark UI (Glassmorphism style)

### Utilities
- PyPDF (PDF text extraction)
- ReportLab (PDF generation)

---

## 🚀 How It Works

1. User pastes text **or uploads a PDF**
2. Long content is **split into chunks** to handle AI token limits
3. Each chunk is summarized using a **distilled transformer model**
4. Summaries are merged into:
   - 📌 Clean paragraph summary
   - 📝 Bullet-point notes
   - ❓ Exam-style questions
5. Notes can be downloaded as **TXT or PDF**

---

## 📂 Project Structure

