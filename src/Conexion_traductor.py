from googletrans import Translator

translations = Translator()

def traductor_textos(texto):

    traslador_list_json = translations.translate(texto,dest='en',src='es')
    return(traslador_list_json.text)

