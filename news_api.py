from flask import Flask,jsonify,request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)
@app.route("/")
def news():

    category = request.args.get("category","world")
    
    if(category == "world"):
        url = "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNRE55YXpBU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen"
    elif(category == "entertainment"):
        url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNREpxYW5RU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
    elif(category == "sports"):
        url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp1ZEdvU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
    elif(category == "science"):
        url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFp0Y1RjU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
    elif(category == "technology"):
        url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGRqTVhZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
    elif(category  == "health"):
        url = "https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JXVnVMVWRDS0FBUAE?hl=en-IN&gl=IN&ceid=IN%3Aen"
    elif(category == "business"):
        url = "https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRGx6TVdZU0JXVnVMVWRDR2dKSlRpZ0FQAQ?hl=en-IN&gl=IN&ceid=IN%3Aen"
    
   

    # step1  : Get the HTML

    r = requests.get(url)
    htmlContent = r.content

    articles = []
    soup = BeautifulSoup(htmlContent,'html.parser')
    data = soup.find_all("article",class_="IBr9hb")
    results = 0
    for id,value in enumerate(data):
        results += 1
        title = value.find("a",class_="gPFEn").text
        link = value.find("a",class_="gPFEn").get("href")
        im = soup.find("img",class_="Quavad vwBmvb").get('src')
        au = value.find("div",class_="bInasb")
        if value.find("div",class_="bInasb") != None:
            author = au.find("span").text
        else :
            author = "null"
        
        article = {
            "id":id,
            "author":author,
            "title":title,
            "link":"https://news.google.com"+link[1:],
            "img":"https://news.google.com"+im
        }
        articles.append(article)
        
    return jsonify({"articles":articles,"totalResults":results})
            
def handler(event, context):
    return app(event, context)

if __name__ == "__main__":
    app.run(debug=True)










