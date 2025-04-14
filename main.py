from flask import Flask, request, render_template
import os
import assemblyai as aai
import google.generativeai as genai

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# AssemblyAI setup
aai.settings.api_key = "4141b3a78ee74998b5e5c0dea795234f"
transcriber = aai.Transcriber()

# Gemini setup
genai.configure(api_key="AIzaSyD-m8SIS7HJLeLtPJzAiFhhdQEIscN9x68")
model = genai.GenerativeModel("models/gemini-2.0-flash")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            # Transcribe
            transcript = transcriber.transcribe(filepath)
            transcription_text = transcript.text

            # Summarize
            prompt = f"Summarize the following text in a clear, concise paragraph:\n\n{transcription_text}"
            summary = model.generate_content(prompt).text

            return render_template("result.html", 
                                   transcript=transcription_text, 
                                   summary=summary)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)