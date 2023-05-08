from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from decouple import config

Ibm_key = config('IBM_KEY')
Ibm_url = config('IBM_URL')

#Consumo los secrets
####Advertencia se debe entrar a ibm a diario a cambiar credenciales porque se actualizan
def ibm_analize_text(translate_text):
    Lista_auth = []
    dict_response = {}
    Lista_response = []

    with open("E:/Universidad/Tesis-programacion-back-unicamente/Proyecto-eva-Back/src/Secrets.txt") as file_object:
        for line in file_object:
            Lista_auth.append(line.rstrip())

    #print(Lista_auth[0])
    #print(Lista_auth[1])

    # CREDENCIALES DE IBM NLU
    authenticator = IAMAuthenticator(f'{Ibm_key}')
    nlu = NaturalLanguageUnderstandingV1(
        version='2021-09-01',
        authenticator=authenticator
    )

    nlu.set_service_url(f'{Ibm_url}')

    # Main function.
    print(translate_text)
    text = translate_text
    response = nlu.analyze(
        text=text,
        features=Features(emotion=EmotionOptions(document=True))
    ).get_result()

    # Imprime los resultados de emociones
    print(response['emotion']['document']['emotion'])

    emotions = response['emotion']['document']['emotion']
    total_score = sum(emotions.values())

    for emotion, score in emotions.items():
        percent_score = round(score / total_score * 100, 2)
        print(f'{emotion}: {percent_score}%')
        Lista_response.append(f"{emotion}:{percent_score}")
        dict_response[f'{emotion}'] = percent_score
        #Lista_response_percets.append(percent_score)

    #return emotions
    return dict_response
    #return response['emotion']['document']['emotion']



