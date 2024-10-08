from flask import Flask, request, render_template, jsonify, send_from_directory
import os
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
from docx import Document
import pdfplumber

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'output/'

# יצירת התיקיות במידה והן לא קיימות
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_audio', methods=['POST'])
def upload_audio_file():
    if 'fileInput' not in request.files:
        return jsonify({'text': 'לא נבחר קובץ'})

    file = request.files['fileInput']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # טיפול בקבצי אודיו לפי פורמט
    if filename.endswith('.ogg'):
        audio = AudioSegment.from_ogg(filepath)
        filepath_wav = os.path.splitext(filepath)[0] + ".wav"
        audio.export(filepath_wav, format="wav")
        filepath = filepath_wav
    elif filename.endswith('.mp3'):
        audio = AudioSegment.from_mp3(filepath)
        filepath_wav = os.path.splitext(filepath)[0] + ".wav"
        audio.export(filepath_wav, format="wav")
        filepath = filepath_wav
    elif filename.endswith('.wav'):
        # אם זה כבר קובץ WAV, אין צורך להמיר
        pass
    else:
        return jsonify({'text': 'פורמט קובץ לא נתמך'})

    # זיהוי דיבור מהאודיו
    recognizer = sr.Recognizer()
    with sr.AudioFile(filepath) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='he-IL')
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)
            with open(output_filepath, "w", encoding="utf-8") as text_file:
                text_file.write(text)
            return jsonify({'text': text, 'download_url': f'/download/{output_filename}'})
        except sr.UnknownValueError:
            return jsonify({'text': 'לא זוהה טקסט'})
        except sr.RequestError:
            return jsonify({'text': 'שגיאה בשירות זיהוי הדיבור'})

@app.route('/upload_text', methods=['POST'])
def upload_text_file():
    if 'fileInput' not in request.files:
        return jsonify({'text': 'לא נבחר קובץ'})

    file = request.files['fileInput']
    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    text = ""

    if filename.endswith('.txt'):
        # קריאת תוכן מקובץ טקסט
        with open(filepath, 'r', encoding="utf-8") as text_file:
            text = text_file.read()
    elif filename.endswith('.pdf'):
        # קריאת תוכן מקובץ PDF
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    elif filename.endswith('.docx'):
        # קריאת תוכן מקובץ DOCX
        doc = Document(filepath)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    elif filename.endswith('.doc'):
        # קריאת תוכן מקובץ DOC באמצעות pywin32 (מיועד לחלונות בלבד)
        return jsonify({'text': 'פורמט DOC לא נתמך בגרסה זו'})
    else:
        return jsonify({'text': 'פורמט קובץ לא נתמך'})

    if text:
        tts = gTTS(text, lang='iw')  # שימוש ב-gTTS לשפה העברית
        output_audio_path = os.path.join(OUTPUT_FOLDER, os.path.splitext(filename)[0] + ".mp3")
        tts.save(output_audio_path)

        return jsonify({'text': text, 'download_url': f'/download/{os.path.basename(output_audio_path)}'})
    else:
        return jsonify({'text': 'לא נמצא תוכן להמרה'})

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)