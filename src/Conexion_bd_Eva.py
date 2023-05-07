import mysql.connector
from decouple import config

def guardar_datos(name,code_student,email, Question1, Question2, Question3, analisis, personal_data):
    status_code = {'status': 0}
    if personal_data == True:
        Lista_auth = []

        with open("E:/Universidad/Tesis-programacion-back-unicamente/Proyecto-eva-Back/Secrets-bd.txt") as file_object:
            for line in file_object:
                Lista_auth.append(line.rstrip())
        
        # Crea la conexión a la base de datos
        conexion = mysql.connector.connect(
            host=f'{config('MYSQL_HOST')}',
            user=f'{Lista_auth[1]}',
            password=f'{Lista_auth[2]}',
            database=f'{Lista_auth[3]}'
        )
        # Crea un cursor para ejecutar consultas SQL en la base de datos
        cursor = conexion.cursor()

        # Ejecuta una consulta SQL SELECT para verificar si el registro ya existe
        consulta = "SELECT * FROM Data_Test2 WHERE codigo = %s AND nombre =%s"
        valores = (code_student, name)
        cursor.execute(consulta, valores)

        # Recupera los datos del registro si ya existe
        registro = cursor.fetchone()
        """fetchone() busca en la base de datos si existe el usuario con esas caracteristicas, imagino que se le puede pasar el userID"""
        print(registro)
        if registro:
            # Si el registro ya existe, muestra los datos en la aplicación Tkinter
            consulta = "UPDATE Data_Test2 SET Email = %s, respuesta1 = %s, respuesta2 = %s, respuesta3 = %s WHERE codigo = %s"
            valores = (email,Question1, Question2, Question3, code_student)
            cursor.execute(consulta, valores)
            #print(cursor)
            print("Esta consulta ya existe y fue actualizada")
        else:
            # Si el registro no existe, ejecuta una consulta SQL INSERT para insertar los datos en la tabla correspondiente
            consulta = "INSERT INTO Data_Test2(nombre, codigo, Email, respuesta1, respuesta2, respuesta3, resultados) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            valores = (name, code_student,email, Question1, Question2, Question3,analisis)
            cursor.execute(consulta, valores)
            #print(cursor)
            print("sORRY BRO ESE USER NO EXISTE Y POR ENDE NO HAY UPDATE, pero si creacion mi socio, revise la bd y veras que lo cree")

        # Confirma los cambios en la base de datos
        conexion.commit()

        status_code['status'] = 200
        print(status_code)

        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        conexion.close()
    else:
        print(f"No hay autorizacion para el uso de datos personales {personal_data}")
        status_code['status'] = 200
        print(status_code)
    
    #return status_code