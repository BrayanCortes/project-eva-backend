import socketio
import json
from Conexion_traductor import traductor_textos
from Conexion_IBM_NLU import ibm_analize_text
from Conexion_bd_Eva import guardar_datos
from Email_manager import email_sender
from Personalized_response import Respues_personalizada

sio = socketio.Server(cors_allowed_origins='*')

app = socketio.WSGIApp(sio)


#Conexion con el servidor
@sio.event
def connect(sid, environ):
    print('SERVER CONNECTION', sid)

#Desconexion con el servidor
@sio.event
def disconnect(sid):
    print('SERVER DISCONNECTION ', sid)

#Llegada de la data y response.S
@sio.event
def message(sid, data):
    json_data = json.loads(data)
    if data != "" and json_data['Response'] == False:
        try:
            json_data = json.loads(data)
            
            #Llamado a funciones de backend
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
            

            #RESPONSE AL FRONTEND
            #Devuelvo el response de gpt al front
            sio.emit('response', RespuestaGPT, room=sid)
        except json.JSONDecodeError:
            sio.emit('response', "Failed to decode JSON", room=sid)
    else:
        print("Empty Json")

if __name__ == '__main__':
    import eventlet
    import eventlet.wsgi
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)