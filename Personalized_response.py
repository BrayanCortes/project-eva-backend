import openai

def Respues_personalizada(nombre,sadness_mesurement):

    Lista_auth = []

    with open("E:/Universidad/Tesis-Programacion/Proyecto-eva-Back/Secrets-gpt.txt") as file_object:
        for line in file_object:
            Lista_auth.append(line.rstrip())
    
    openai.api_key = f'{Lista_auth[0]}'
    """
    La escala fue hecha usando la escala de tristeza o la escala de depresion de beck.
    La formula para sacar los porcentajes fue 9/60 * 100
    """

    nivel_tristeza = ""
    if sadness_mesurement <= 15.99:
        nivel_tristeza = "0"
    elif sadness_mesurement >= 16 and sadness_mesurement <= 30.99:
        nivel_tristeza = "medio-bajo"
    elif sadness_mesurement >= 31 and sadness_mesurement <= 49.99:
        nivel_tristeza = "moderado"
    elif sadness_mesurement >= 50 and sadness_mesurement <= 65.99:
        nivel_tristeza = "medio-alto"
    elif sadness_mesurement >= 66 and sadness_mesurement <= 100:
        nivel_tristeza = "alto"


    prompt = f"Dile unas palabas de aliento a una persona de nombre {nombre} que tiene un nivel {nivel_tristeza} de tristeza, dependiendo del nombre ten en cuenta si es femenino o masculino."
    print(f"Perzonalized para: {nivel_tristeza} y para mi panita: {nombre}")
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.8,
    )
    respuesta = completions.choices[0].text
    
    return respuesta

