from googletrans import Translator

translations = Translator()

def traductor_textos(texto):

    traslador_list_json = translations.translate(texto,dest='en',src='es')
    #print(traslador_list_json.text)
    return(traslador_list_json.text)


#Open_Question_translate = traductor_textos(Open_Question)

#print(Open_Question_translate)