import requests
import json

def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        with requests.Session() as session:
            response = session.post(url, headers=headers, json=input_json, timeout=10)
            if response.status_code == 400:
                return {
                    'anger': None,
                    'disgust': None,
                    'fear': None,
                    'joy': None,
                    'sadness': None,
                    'dominant_emotion': None
                }
            response.raise_for_status()
            response_data = response.json()

            # Extraer las emociones requeridas
            emotions = response_data.get("emotion", {})
            anger_score = emotions.get("anger", 0)
            disgust_score = emotions.get("disgust", 0)
            fear_score = emotions.get("fear", 0)
            joy_score = emotions.get("joy", 0)
            sadness_score = emotions.get("sadness", 0)

            # Encontrar la emoción dominante
            emotion_scores = {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score
            }
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

            # Formatear la salida
            result = {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': dominant_emotion
            }
            return result

    except requests.exceptions.RequestException as e:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

if __name__ == "__main__":
    text = "Estoy tan feliz de estar haciendo esto."
    print(emotion_detector(text))
