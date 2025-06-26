from flask import Flask, render_template, request, redirect, session, url_for
from utils.ai_helpers import granite_generate_response, analyze_sentiment
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client['citizenai']
chat_collection = db['chat_history']
sentiment_collection = db['sentiments']
concern_collection = db['concerns']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/chat')
def chat():
    chat_history = list(chat_collection.find().sort("timestamp", -1).limit(10))
    return render_template('chat.html', chat_history=chat_history)



@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form.get('question')
    if question:
        response = granite_generate_response(question)
        chat_collection.insert_one({
            "question": question,
            "response": response,
            "timestamp": datetime.utcnow()
        })
        history = list(chat_collection.find().sort("timestamp", -1).limit(10))
        return render_template('chat.html', question_response=response, chat_history=history)
    return redirect(url_for('chat'))

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    feedback = request.form.get('feedback')
    if feedback:
        sentiment = analyze_sentiment(feedback)
        sentiment_collection.insert_one({
            "feedback": feedback,
            "sentiment": sentiment,
            "timestamp": datetime.utcnow()
        })
    return redirect(url_for('chat'))


@app.route('/concern', methods=['POST'])
def submit_concern():
    concern = request.form.get('concern')
    if concern:
        concern_collection.insert_one({"concern": concern, "timestamp": datetime.utcnow()})
        return render_template('chat.html', question_response=None, sentiment=None, concern_submitted=True)
    return redirect(url_for('chat'))

@app.route('/dashboard')
def dashboard():
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for doc in sentiment_collection.find():
        if doc['sentiment'] in sentiments:
            sentiments[doc['sentiment']] += 1
    recent_issues = [doc['concern'] for doc in concern_collection.find().sort("timestamp", -1).limit(5)]
    feedback_list = list(sentiment_collection.find().sort("timestamp", -1).limit(10))
    return render_template('dashboard.html', sentiments=sentiments, recent_issues=recent_issues,feedback_list=feedback_list)

if __name__ == '__main__':
    app.run(debug=True)
