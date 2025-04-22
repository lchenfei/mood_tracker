from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

CSV_FILE = 'mood_log.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        mood = request.form.get('mood')
        note = request.form.get('note', '')
        date = datetime.now().strftime('%Y-%m-%d')

        new_entry = pd.DataFrame([[date, mood, note]], columns=["date", "mood", "note"])

        if os.path.exists(CSV_FILE):
            df = pd.read_csv(CSV_FILE)
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df = new_entry

        df.to_csv(CSV_FILE, index=False)
        message = f"Saved mood: {mood} with note: {note}"

    return render_template('index.html', message=message)

@app.route('/chart')
def chart():
    try:
        df = pd.read_csv(CSV_FILE)
        mood_counts = df['mood'].value_counts().to_dict()
    except Exception:
        mood_counts = {}
    return render_template('index.html', mood_data=mood_counts)

if __name__ == '__main__':
    app.run(debug=True)
