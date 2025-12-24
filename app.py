from flask import Flask, render_template, request, send_file
from transformers import pipeline
from pypdf import PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import torch
torch.set_num_threads(2)


app = Flask(__name__)

# Load summarizer
summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)


# ---------------- HELPERS ----------------

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "
    return text

def chunk_text(text, max_words=400):
    words = text.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def summarize_text(text):
    summaries = []
    for chunk in chunk_text(text, max_words=300):
        if len(chunk.split()) > 80:
            result = summarizer(
                chunk,
                max_length=110,
                min_length=40,
                do_sample=False
            )
            summaries.append(result[0]["summary_text"])
    return " ".join(summaries)

def generate_bullets(text):
    sentences = text.split(". ")
    return [s.strip() for s in sentences if len(s.strip()) > 20][:6]

def generate_questions(summary):
    sentences = [s.strip() for s in summary.split(".") if len(s.strip()) > 30]

    questions = []

    for s in sentences[:4]:
        # Extract first meaningful phrase
        words = s.split()
        keyword = " ".join(words[:4])

        questions.append(f"Explain the concept of {keyword}.")
        questions.append(f"Why is {keyword} important?")
        questions.append(f"Write a short note on {keyword}.")
        questions.append(f"Discuss the applications of {keyword}.")

    # Remove duplicates and limit
    unique_questions = list(dict.fromkeys(questions))
    return unique_questions[:6]

# ---------------- ROUTES ----------------

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    bullets = []
    questions = []
    original_text = ""

    if request.method == "POST":

        if "pdf" in request.files and request.files["pdf"].filename != "":
            original_text = extract_text_from_pdf(request.files["pdf"])
        else:
            original_text = request.form.get("text", "")

        if len(original_text.split()) > 80:

            summary = summarize_text(original_text)
            bullets = generate_bullets(summary)
            questions = generate_questions(summary)
        else:
            summary = "Please upload a PDF or enter more text."

    return render_template(
        "index.html",
        summary=summary,
        bullets=bullets,
        questions=questions,
        original_text=original_text
    )

# ---------------- DOWNLOAD TXT ----------------

@app.route("/download/txt", methods=["POST"])
def download_txt():
    summary = request.form["summary"]
    bullets = request.form.getlist("bullets")
    questions = request.form.getlist("questions")

    content = "SUMMARY:\n\n" + summary + "\n\nBULLET NOTES:\n"
    for b in bullets:
        content += f"- {b}\n"

    content += "\nQUESTIONS:\n"
    for q in questions:
        content += f"- {q}\n"

    file = io.BytesIO()
    file.write(content.encode("utf-8"))
    file.seek(0)

    return send_file(file, as_attachment=True, download_name="ai_notes.txt")

# ---------------- DOWNLOAD PDF ----------------

@app.route("/download/pdf", methods=["POST"])
def download_pdf():
    summary = request.form["summary"]
    bullets = request.form.getlist("bullets")
    questions = request.form.getlist("questions")

    file = io.BytesIO()
    pdf = canvas.Canvas(file, pagesize=letter)
    text = pdf.beginText(40, 750)
    text.setFont("Helvetica", 11)

    text.textLine("AI GENERATED NOTES")
    text.textLine("")
    text.textLine("SUMMARY:")
    text.textLine(summary)
    text.textLine("")
    text.textLine("BULLET NOTES:")
    for b in bullets:
        text.textLine(f"- {b}")

    text.textLine("")
    text.textLine("QUESTIONS:")
    for q in questions:
        text.textLine(f"- {q}")

    pdf.drawText(text)
    pdf.showPage()
    pdf.save()
    file.seek(0)

    return send_file(file, as_attachment=True, download_name="ai_notes.pdf")

if __name__ == "__main__":
    app.run(debug=True)
