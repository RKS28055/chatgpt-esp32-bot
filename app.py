from flask import Flask, request, send_file
from gtts import gTTS
import openai
import os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/process', methods=['POST'])
def process():
    prompt = "Who are you?"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a smart voice assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response['choices'][0]['message']['content']

        tts = gTTS(reply)
        tts.save("reply.mp3")

        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.route('/audio')
def audio():
    return send_file("reply.mp3", mimetype="audio/mpeg")

if __name__ == '__main__':
    app.run()
