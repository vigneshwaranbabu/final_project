import requests
import json

def emotion_detector(text_to_analyse):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    header = {
        "Content-Type": "application/json",
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    myobj = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    try:
        # Make the request
        response = requests.post(url, json=myobj, headers=header, timeout=10)
        
        # Handle blank entry with 400 response
        if response.status_code == 400:
            return {
                "anger": None,
                "disgust": None,
                "fear": None,
                "joy": None,
                "sadness": None,
                "dominant_emotion": None
            }

        response.raise_for_status()

        # Convert response text into a dictionary
        response_json = json.loads(response.text)

        # Extract emotion scores
        emotions = response_json["emotionPredictions"][0]["emotion"]
        anger_score = emotions.get("anger", 0)
        disgust_score = emotions.get("disgust", 0)
        fear_score = emotions.get("fear", 0)
        joy_score = emotions.get("joy", 0)
        sadness_score = emotions.get("sadness", 0)

        # Determine dominant emotion
        emotion_scores = {
            "anger": anger_score,
            "disgust": disgust_score,
            "fear": fear_score,
            "joy": joy_score,
            "sadness": sadness_score
        }
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)

        # Return the output in the required format
        result = {
            "anger": anger_score,
            "disgust": disgust_score,
            "fear": fear_score,
            "joy": joy_score,
            "sadness": sadness_score,
            "dominant_emotion": dominant_emotion
        }
        return result

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
