from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from decouple import config

#Variables de entorno
Ibm_key = config('IBM_KEY')
Ibm_url = config('IBM_URL')

def ibm_analize_text(translate_text):
    
    dict_response = {}
    Lista_response = []


    # CREDENCIALES DE IBM NLU
    authenticator = IAMAuthenticator(f'{Ibm_key}')
    nlu = NaturalLanguageUnderstandingV1(
        version='2021-09-01',
        authenticator=authenticator
    )

    # URL del servicio que se Usa de IBM
    nlu.set_service_url(f'{Ibm_url}')

    # Main function.
    print(translate_text)
    text = translate_text
    response = nlu.analyze(
        text=text,
        features=Features(emotion=EmotionOptions(document=True))
    ).get_result()

    # Imprime los resultados de emociones
    #print(response['emotion']['document']['emotion'])

    emotions = response['emotion']['document']['emotion']
    total_score = sum(emotions.values())

    for emotion, score in emotions.items():
        percent_score = round(score / total_score * 100, 2)
        #print(f'{emotion}: {percent_score}%')
        Lista_response.append(f"{emotion}:{percent_score}")
        dict_response[f'{emotion}'] = percent_score

    return dict_response




