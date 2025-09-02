from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Serve the frontend
@app.route("/")
def home():
    return render_template("multimodal-ai-search.html")


# Text search using DuckDuckGo API
@app.route("/search", methods=["GET"])
def text_search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&no_html=1"
    resp = requests.get(url)
    data = resp.json()

    results = []
    if "RelatedTopics" in data:
        for item in data["RelatedTopics"][:5]:  # Top 5 results
            if "Text" in item and "FirstURL" in item:
                results.append({
                    "title": item["Text"].split("–")[0][:50],
                    "description": item["Text"],
                    "type": "article",
                    "relevance": 90,
                    "source": item["FirstURL"]
                })

    return jsonify(results)


# Image search placeholder (can replace with real API later)
@app.route("/image-search", methods=["POST"])
def image_search():
    return jsonify([
        {
            "title": "Sample Image Match",
            "description": "Found similar images using placeholder AI.",
            "type": "image",
            "relevance": 92,
            "source": "https://picsum.photos/300"
        },
        {
            "title": "Visual AI Match",
            "description": "Detected similar features in other images.",
            "type": "image",
            "relevance": 88,
            "source": "https://picsum.photos/400"
        }
    ])


if __name__ == "__main__":
    app.run(debug=True)
