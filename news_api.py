from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route("/")
def news():
    category = request.args.get("category", "world")

    categories = {
        "world": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen",
        "entertainment": "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen",
        "sports": "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen",
        "science": "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp0Y1RjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen",
        "technology": "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen",
        "health": "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen",
        "business": "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
    }

    url = categories.get(category, categories["world"])
    
    try:
        r = requests.get(url, timeout=10)  # Add timeout
        r.raise_for_status()  # Ensure response is 200 OK
        htmlContent = r.content
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Failed to fetch news", "details": str(e)}), 500

    soup = BeautifulSoup(htmlContent, 'html.parser')
    data = soup.find_all("article", class_="IBr9hb")

    articles = []
    for id, value in enumerate(data):
        title_tag = value.find("a", class_="gPFEn")
        link = title_tag.get("href") if title_tag else "#"
        im_tag = soup.find("img", class_="Quavad vwBmvb")
        im = im_tag.get('src') if im_tag else "#"
        author_tag = value.find("div", class_="bInasb")
        author = author_tag.find("span").text if author_tag else "Unknown"

        article = {
            "id": id,
            "author": author,
            "title": title_tag.text if title_tag else "No title",
            "link": f"https://news.google.com{link}" if link.startswith("/") else link,
            "img": f"https://news.google.com{im}" if im.startswith("/") else im
        }
        articles.append(article)

    return jsonify({"articles": articles, "totalResults": len(articles)})

# Required for Vercel serverless function
def handler(event, context):
    return app(event, context)
if __name__ == "__main__":
    app.run(debug=False)







