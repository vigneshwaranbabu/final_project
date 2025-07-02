#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask server for emotion detection service.
"""

from flask import Flask, request, jsonify, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

HOST = "localhost"
PORT = 5000


@app.route("/", methods=["GET"])
def index():
    """
    Render the index.html template.
    """
    return render_template("index.html")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detector_route():
    """
    Handle emotion detection requests via GET or POST.
    """
    if request.method == "POST":
        data = request.get_json()
        if not data or "text" not in data:
            return (
                jsonify({
                    "error": "Invalid request. Please send JSON with a 'text' field."
                }),
                400,
            )
        statement = data["text"]
    else:
        statement = request.args.get("textToAnalyze")

    result = emotion_detector(statement)

    if "error" in result:
        return jsonify({"error": result["error"]}), 500

    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again!"

    response_text = (
        "For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return response_text


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
