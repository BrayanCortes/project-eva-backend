import smtplib

def email_sender(sadness_mesurement,student_name,student_code, email, personal_data):
    # Configura el servidor SMTP y la cuenta de correo electrónico


    Lista_auth = []
    with open("E:/Universidad/Tesis-programacion-back-unicamente/Proyecto-eva-Back/src/Secrets-Emanger.txt") as file_object:
        for line in file_object:
            Lista_auth.append(line.rstrip())

    servidor_smtp = 'smtp.gmail.com'
    puerto_smtp = 587
    cuenta_correo = f'{Lista_auth[0]}'
    contraseña_correo = f'{Lista_auth[1]}' #Esto ira en un secretkeys, junto con el correo,

    # Crea el objeto del servidor SMTP y haz login en la cuenta de correo electrónico
    servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
    servidor.starttls()
    servidor.login(cuenta_correo,contraseña_correo)

    correo_bienestar = 'PruebasProyectoEvaBienestar@gmail.com'
    if personal_data == True:
        ##Se van a poner mas ifs, para tener cubiertos los porcentajes,
        if sadness_mesurement >= 31 and sadness_mesurement <=100:
            # Crea el mensaje de correo electrónico
            para = {correo_bienestar}
            asunto = f'Remision del estudiante {student_name} '
            cuerpo = f'Buenos dias, este es un correo automatico del Chatbot Eva para informar a la plantilla de psicologia de la universidad del valle que el estudiante {student_name} identificado con el codigo {student_code} y con correo electronico {email} presenta un nivel de tristeza del {sadness_mesurement}% por lo que se necesita que tomen cartas en el asunto.'
            mensaje = f'Subject: {asunto}\n\n{cuerpo}'
        elif sadness_mesurement >= 0  and sadness_mesurement <= 30.99:
            # Crea el mensaje de correo electrónico
            para = 'SoyUnEstudianteDePrueba@gmail.com'
            asunto = f'Hola {student_name} '
            cuerpo = f'Hola, esta es una respuesta automatica del Chatbot Eva, veo que tus niveles de tristeza son de {sadness_mesurement}%, si lo deseas intenta comunicarte con bienestar universitario usando el correo {correo_bienestar} y cuentales de tus resultados o acercate a la sede victoria de la universidad del valle.'
            mensaje = f'Subject: {asunto}\n\n{cuerpo}'
        # Envía el correo electrónico
    else:
        para = 'SoyUnEstudianteDePrueba@gmail.com'
        asunto = f'Hola {student_name} '
        cuerpo = f'Hola, esta es una respuesta automatica del Chatbot Eva, veo que tus niveles de tristeza son de {sadness_mesurement}%, si lo deseas intenta comunicarte con bienestar universitario usando el correo {correo_bienestar} y cuentales de tus resultados o acercate a la sede victoria de la universidad del valle.'
        mensaje = f'Subject: {asunto}\n\n{cuerpo}'
    #Envía el correo electrónico
    servidor.sendmail(cuenta_correo, para, mensaje)
    print("Correo enviado")

    # Cierra la conexión con el servidor SMTP
    servidor.quit()
