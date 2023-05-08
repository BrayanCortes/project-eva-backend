import socketio
import json
from Conexion_traductor import traductor_textos
from Conexion_IBM_NLU import ibm_analize_text
from Conexion_bd_Eva import guardar_datos
from Email_manager import email_sender
from Personalized_response import Respues_personalizada
import asyncio

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


"""
Poner mensaje de que si se quiere volver a interactuar, refrescar al final,

Pedir mas detalles en la pregunta abierta.
"""

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

@sio.event
def message(sid, data):
    print(sid)
    print(data)
    json_data = json.loads(data)
    print(json_data['Response'])
    if data != "" and json_data['Response'] == False:
        try:
            json_data = json.loads(data)
            print(f"Hola my friend soy la: {type(json_data)}")
            print(f"Hola my friend soy la: {(json_data)}")
            
            #Backend functions
            print("###################")
            print("")

            #Analisis de NLU
            Resultados_analisis = ibm_analize_text(traductor_textos(json_data['Openpregunta']))

            #Saco el resultado numerico de las tristeza que me da el analisis para mas adelante
            Porcentaje_tristeza = Resultados_analisis['sadness']

            #Respuesta personalizada de chatgpt
            RespuestaGPT = Respues_personalizada(json_data['nombre'],Porcentaje_tristeza)

            #Resultado de ibm en formato string para almacenarlo en la bd
            Resultados_analisis_STR = str(Resultados_analisis)

            #Envio de email
            email_sender(Porcentaje_tristeza,json_data['nombre'],json_data['codigoEstudent'],json_data['emailEstudent'],json_data['Usodatos'])
            
            #guardado de datos o update
            guardar_datos(json_data['nombre'],json_data['codigoEstudent'],json_data['emailEstudent'],json_data['pregunta1'], json_data['pregunta2'], json_data['pregunta3'], Resultados_analisis_STR ,json_data['Usodatos'])
            
            print("")
            print("###################")

            #Devuelvo el response de gpt al front
            sio.emit('response', RespuestaGPT, room=sid)
        except json.JSONDecodeError:
            print("Error al decodificar JSON")
            sio.emit('response', "Error al decodificar JSON", room=sid)
    else:
        print("###################")
        print("No viene data")

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)