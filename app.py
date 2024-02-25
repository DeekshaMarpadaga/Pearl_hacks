from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
import requests
from datetime import datetime, timedelta
import random


app = Flask(__name__)

api_key = '949863bc9c5f481d93eb90f8ab6a3274'

past_reflection = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET'])
def analyze():
    reflection = request.args.get('reflectionText')
    sentiment = sentiment_analysis(reflection)

    # Save the reflection along with sentiment to past_reflections
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    past_reflection.append({
        'timestamp': timestamp,
        'reflection': reflection,
        'sentiment_score': sentiment['sentiment_score'],
        'sentiment_label': sentiment['sentiment_label']
    })

    return render_template('result.html', sentiment_score=sentiment['sentiment_score'], sentiment_label=sentiment['sentiment_label'])

@app.route('/past_reflections', methods=['GET'])
def past_reflections():
    # Render a page to display past reflections
    return render_template('past_reflections.html', past_reflections=past_reflection)


def sentiment_analysis(text):

    print(text)
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    if sentiment_score > 0.5:
        sentiment = "Positive"
    elif sentiment_score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    if sentiment =='Negative' or sentiment =='Neutral':
        articles = recommend_resources()
        
    return {"sentiment_score": sentiment_score,
        "sentiment_label":sentiment}

@app.template_global()
def recommend_resources():
    start_date = datetime.now() - timedelta(days=random.randint(1, 30))
    from_date = start_date.strftime('%Y-%m-%d')

    url = 'https://newsapi.org/v2/everything'
    params = {
        'apiKey': api_key,
        'q': 'comedy', 
        'pageSize': 5,
        'from': from_date
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles', [])
        print(articles)
        return articles
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return []
    

if __name__ == '__main__':
    app.run(debug=True, port=5001)