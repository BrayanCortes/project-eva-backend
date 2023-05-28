import mysql.connector
from decouple import config
import asyncio

#Variables de entorno
Host = config('MYSQL_HOST')
User = config('MYSQL_USER')
Password = config('MYSQL_PASSWORD')
DataBase = config('MYSQL_DB')
Port = config('MYSQL_PORT')

def guardar_datos(name,code_student,email, Question1, Question2, Question3, analisis, personal_data):
    status_code = {'status': 0}
    if personal_data == True:
        
        # Crea la conexión a la base de datos
        conexion = mysql.connector.connect(
            host=f'{Host}',
            user=f'{User}',
            password=f'{Password}',
            database=f'{DataBase}',
            port = f'{Port}',
        )
        # Crea un cursor para ejecutar consultas SQL en la base de datos
        cursor = conexion.cursor()

        # Ejecuta una consulta SQL SELECT para verificar si el registro ya existe
        consulta = "SELECT * FROM Data_Test2 WHERE codigo = %s AND nombre =%s"
        valores = (code_student, name)
        cursor.execute(consulta, valores)
        # Recupera los datos del registro si ya existe
        registro = cursor.fetchone()
        print(registro)
        if registro:
            consulta = "UPDATE Data_Test2 SET Email = %s, nombre = %s, respuesta1 = %s, respuesta2 = %s, respuesta3 = %s, resultados = %s WHERE codigo = %s"
            valores = (email,name,Question1, Question2, Question3,analisis,code_student)
            cursor.execute(consulta, valores)
            print(f"Update Student with code:{code_student} and Name:{name}")
        else:
            # Si el registro no existe, ejecuta una consulta SQL INSERT para insertar los datos en la tabla correspondiente
            consulta = "INSERT INTO Data_Test2(nombre, codigo, Email, respuesta1, respuesta2, respuesta3, resultados) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (name, code_student,email, Question1, Question2, Question3,analisis)
            cursor.execute(consulta, valores)
            print(f"Insert Student with Name:{name} and Code:{code_student}")
        # Confirma los cambios en la base de datos
        conexion.commit()
        status_code['status'] = 200
        print(status_code)

        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        conexion.close()
    else:
        print(f"Data use authorization denied: {personal_data}")
        status_code['status'] = 200
        print(status_code)
    
    #return status_code