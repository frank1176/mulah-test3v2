from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

app = Flask(__name__)

@app.route("/")
def index():
    headlines = get_headlines()
    return render_template('index.html', headlines=headlines)

def get_headlines():
    url = "https://www.theverge.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.select('h2 a')
    dates = soup.select('time')

    date_times = [date_element['datetime'] for date_element in dates if date_element.has_attr('datetime')]
    date_objects = [datetime.fromisoformat(date_time) for date_time in date_times]

    headlines = []

    date_threshold = datetime(2022, 1, 1, tzinfo=timezone.utc)

    for article, date_obj in zip(articles, date_objects):
        if date_obj >= date_threshold:
            title = article.text
            link = url + article['href'] if article['href'].startswith('/') else article['href']
            headlines.append({'title': title, 'link': link, 'date': date_obj.strftime('%b %d, %Y')})

    headlines = sorted(headlines, key=lambda x: x['date'], reverse=True)
    return headlines

if __name__ == "__main__":
    app.run(debug=True)
