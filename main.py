from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from googlesearch import search

app = Flask(__name__)

@app.route("/scan", methods=["GET"])
def scan_keyword():
    keyword = request.args.get("keyword")
    if not keyword:
        return jsonify({"error": "No keyword provided"}), 400

    results = []
    urls = list(search(keyword + " site:.hu", num_results=5))

    for url in urls:
        try:
            r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(r.text, "html.parser")

            for tag in soup(["script", "style", "noscript"]):
                tag.decompose()

            text = soup.get_text(separator=' ')
            clean_text = ' '.join(text.split())
            char_count = len(clean_text)

            results.append({
                "url": url,
                "character_count": char_count
            })

        except Exception as e:
            results.append({
                "url": url,
                "error": str(e)
            })

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)