from .emotion_detection import emotion_detector

import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock",
        "Content-Type": "application/json"
    }
    input_json = {
        "raw_document": {
            "text": text_to_analyze
        }
    }

    response = requests.post(url, headers=headers, json=input_json)
    if response.status_code == 200:
        response_dict = response.json()

        # Debug print (optional)
        print("API response:", json.dumps(response_dict, indent=2))

        # Correct extraction of emotions from response
        emotions = {}
        if 'emotionPredictions' in response_dict and len(response_dict['emotionPredictions']) > 0:
            emotions = response_dict['emotionPredictions'][0].get('emotion', {})

        anger_score = emotions.get('anger', 0)
        disgust_score = emotions.get('disgust', 0)
        fear_score = emotions.get('fear', 0)
        joy_score = emotions.get('joy', 0)
        sadness_score = emotions.get('sadness', 0)

        scores = {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score
        }

        if all(score == 0 for score in scores.values()):
            dominant_emotion = None
        else:
            dominant_emotion = max(scores, key=scores.get)

        return {
            'anger': anger_score,
            'disgust': disgust_score,
            'fear': fear_score,
            'joy': joy_score,
            'sadness': sadness_score,
            'dominant_emotion': dominant_emotion
        }
    else:
        return {"error": f"Request failed with status code {response.status_code}"}
