import os
import requests
from passlib.hash import sha256_crypt
import csv
import random
import matplotlib.pyplot as plt 
#permitir ingreso usuario y demas

def validar_usuario(usuario:str)->bool:
    if usuario in ("a","b"):
        return True
    else: return False

def validar_mail(mail:str,ids:list)->bool:
    if mail not in ids:
        return True
    else: return False

def user_registration(id_usuarios:list)->str:
    #PRECONDICIONES: UN NUEVO USER QUIERE GENERAR UNA CUENTA 
    #POSTCONDICIONES: MAIL QUE DEBE SER UNICO
    #pido datos al user
    print("Ingrese los siguientes datos, como se detalle a continucion: ")
    mail = input("Correo electronico: ")
    while(validar_mail(mail,id_usuarios)==False):
        print("El correo electronico ingresado ya se encuentra en uso.")
        print("Ingrese otro.")
        mail = input("Correo electronico: ")
    name = input("Nombre Usuario: ")
    password = sha256_crypt.hash(input("Contraseña: "))
    money = float(input("Dinero inicial que desea ingresar: "))

    #por ultimo se agrega este nuevo user al archivo, con esta funcion se consigue guardar lo que ya estaba en el archivo y reescribirlo + el nuevo usuario
    archivo_csv_r_w_data_users(mail,name,password,money)
    print(f"El usuario {name} ligado al correo electronico {mail} se ha registrado con exito.")

    return mail


def archivo_csv_r_w_data_users(new_mail:str,new_name:str,new_password:str,new_money:float)->None:

    users = {} #dict donde se va a guardar la data del archivo
    archivo_csv_users = 'data_users.csv'

    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users

       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'name':row[1],'password':row[2],'bets':row[3],'date':row[4],'money': row[5]}

    users[new_mail]={'name':new_name,'password':new_password,'bets':0,'date':None,'money':new_money}

    with open('data_users.csv', 'w', newline='', encoding='UTF-8') as archivo_csv: #aclaro con un 'w' que es un archivo de escritura

        csv_writer = csv.writer(archivo_csv, delimiter=',', quotechar='"',quoting=csv.QUOTE_NONNUMERIC)
        csv_writer.writerow(['name','password','bets','money'])
        for mail, data in users.items():
            csv_writer.writerow([mail,data['name'],data['password'],data['bets'],data['date'],data['money']])



def imprimir_opciones()->None:

    print("Bienvenido a la mejor plataforma de apuestas futboleras")
    print ("Seleccione una opcion: ")
    print ("1. Mostrar el plantel completo de un equipo de la Liga Profesional 2023")
    print ("2. Mostrar la tabla de posiciones de la Liga profesional")
    print ("3. Estadios y escudos de los equipos ")
    print ("4. Grafico goles equipo determinado")
    print ("5. Cargar dinero en cuenta ")
    print ("6. Usuario que más dinero apostó")
    print ("7. Usuario que más veces ganó")
    print ("8. Apuestas")
    print ("9. SALIR")

def opcion_seleccionada (opcion_elegida:int, equipos_2023:dict, jugadores_2023:dict):   #"complletar resto datos de la API"
    if opcion_elegida == 1: 
        print("--- Equipos de la Liga Profesional Temporada 2023---")
        equipos_2023 = equipos_liga_2023()
        listar_equipos_2023 (equipos_2023)
        equipo_usuario = input("Seleccione equipo: ")
        while equipo_usuario not in equipos_liga_2023:
            print("Equipo inválido")
        jugadores_2023 = jugadores_equipos ()
        id_equipo_usuario = id_equipo(equipos_2023, equipo_usuario)
        plantel_2023(id_equipo_usuario, jugadores_2023)


    elif opcion_elegida == 2:
        print("--- Tabla posiciones de la Liga Profesional Temporada 2023---")
        equipos_2023  = equipos_liga_2023 ()
        listar_equipos_2023 (equipos_2023)
       

    elif opcion_elegida == 3:
        print ("--- Escudos y Estadios ---")
        equipo_seleccionado=input("Seleccione equipo dentro del listado:")
        #escudos_estadios() --> daros apii

    elif opcion_elegida == 4:
        print ("--- Grafico goles y minutos ---")
        equipo_seleccionado=input("Seleccione equipo dentro del listado:")
        #datos de la api 

    elif opcion_elegida == 5:
        print ("--- Cargar dinero a cuenta ---")
        id_usuario = input ("MAIL: ")
        cargar_dinero_cuenta_usuario (id_usuario, "","")
    
    elif opcion_elegida == 6:
        print ("--- Usuario que más dinero apostó ---")
        #usuario_mas_aposto () 
        #basarme transacciones.csv

    elif opcion_elegida == 7:
        print ("--- Usuario que más veces gano ---")
        #usuario_ganador ()
        #registo en transacciones.csv / data_users.csv

    elif opcion_elegida == 8:
        print("--- APUESTAS ---")
        #apuestas_usuarios ()
        #registro si gana/deposita (+), si pierde (-) en transacciones
        #voy al data.csv al final para sumar o restar el dinero, ya con resultado de la apuesta

    else:
        print("Intente seleccionar una opcion del menu.")
        opcion_seleccionada(opcion_elegida,equipos_2023, jugadores_2023 )
    

def plantel_2023(id_equipo:int, jugadores_2023:dict):
    jugadores_2023 = jugadores_equipos()
    for jugador in jugadores_2023:
        if (jugador['statistics'][0]['team']['id'] == id_equipo):
            print(jugador['player']['name'])
            equipos_2023 = equipos_liga_2023()
            for equipo in equipos_2023:
                id_equipo = equipo['team']['id']
                print(f"\nPlantel de {equipo['team']['name']}:")


def equipos_liga_2023 () -> dict:
    url = "https://v3.football.api-sports.io/teams"
    params = {"league": "128", "season": 2023, "country": "Argentina"}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", 
               "x-rapidapi-key": "407726f0daca539a383c3c8ca8e4ca93" }

    respuesta = requests.get(url, params = params, headers = headers)
    equipos_2023 = {}

    if respuesta.status_code == 200:
        data = respuesta.json()
        equipos_2023 = data ["response"]

    #procesa la data y devuelve un dict
    else:
        print("Err", respuesta.status_code )
    return equipos_2023

def jugadores_equipos ()-> dict:
    url = "https://v3.football.api-sports.io/teams"
    params ={"league": "128", "season": 2023}
    headers = {"x-rapidapi-host": "v3.football.api-sports.io", 
               "x-rapidapi-key": "407726f0daca539a383c3c8ca8e4ca93"}
    respuesta = requests.get (url, params = params, headers = headers)
    jugadores_2023 = {}
    if respuesta.status_code == 200:
        data = respuesta.json ()
        jugadores_2023 = data ["response"]
    else:
        print("Err", respuesta.status_code)

    return jugadores_2023


def listar_equipos_2023 (equipos_2023:dict) -> None:
    equipos_2023 = equipos_liga_2023 ()
    for i, equipo in enumerate (equipos_2023, start = 1):
        nombre_equipo = equipo["team"]["name"]
        id_equipo = equipo ["team"]["id"]
        print(f"{i}. {nombre_equipo} (id : {id_equipo})")


def id_equipo(equipos_2023:dict, equipo_usuario:str) -> None:
    equipos_2023 = equipos_liga_2023 ()
    for equipo in equipos_2023:
        if equipo_usuario == equipo["team"]["name"]:
            id_equipo_usuario = equipo["team"]["id"]
            print(equipo["team"])
    return id_equipo_usuario 

def cargar_dinero_cuenta_usuario(id_usuario, dinero, fecha): 
    
    users = {} #dict donde se va a guardar la data del archivo
    archivo_csv_users = 'data_users.csv'
   
    if os.path.isfile(archivo_csv_users):#verifica que exista el archivo de la data de los users

       with open(archivo_csv_users, newline='',encoding="UTF-8") as archivo_csv:
           csv_reader = csv.reader(archivo_csv, delimiter=',') 
           next(csv_reader)#evita la primera linea, o sea el header
           for row in csv_reader:
               mail = row[0]
               users[mail] = {'money': row[5]}

    if id_usuario  in users[mail]:
        dinero = input ("Dinero a cargar: ")
        dinero = float(dinero)
        dinero_en_cuenta = users[mail]['money'] 
        users[mail]["money"] = dinero_en_cuenta + dinero
    else:
        print("Mail invalido")

    print (f"Ahora posee {users[mail]['money']} disponible en su cuenta. ")
    
    # actualizar_dinero_en_cuenta() #actauliza csv usuarios con deposito (carga de dinero)
    # registrar_nueva_transaccion() #en desarollo



# def equipos_liga_2023 () -> dict:
#     url = "https://v3.football.api-sports.io/teams"
#     parameters = {"league": "128", "season": 2023, "country": "Argentina"}

#     headers = {"x-rapidapi-host": "v3.football.api-sports.io", 
#                "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

#     respuesta = requests.get(url, params = parameters, headers = headers)
#     equipos_2023 = {}
#     dict_equipos = {}

#     if respuesta.status_code == 200:
#         data = respuesta.json()
#         equipos_2023 = data ["response"]

#         for equipo in range (28):
#             dict_equipos[equipos_2023[equipo]["team"]["name"]] = equipos_2023[equipo]["team"]["id"]

    #procesa la data y devuelve un dict
     
    # else:
    #     print("Err", respuesta.status_code )

    # return dict_equipos


def fechas_teams(id_team:int)->dict:
    
    url = "https://v3.football.api-sports.io/fixtures?"

    parameters = {"league": "128","season": 2023,"team":id_team}

    headers = {"x-rapidapi-host": "v3.football.api-sports.io", "x-rapidapi-key": "6560a6c96c1a8e1c14463129104c7c84" }

    respuesta = requests.get(url, params = parameters, headers = headers)
    fechas = {}
    locales = {}
    visitantes = {}
    if respuesta.status_code == 200:
        data = respuesta.json()
        fechas = data['response']
        print(f"Fechas de Temporada 2023:")

        for fecha in range(len(fechas[0]['fixture'])):
            locales[fechas[0]['fixture']['teams']['home']['name']]= fechas[0]['fixture']['teams']['home']['id']
            visitantes[fechas[0]['fixture']['teams']['away']['name']] = fechas[0]['fixture']['teams']['away']['id'] 
            fechas[fecha] = [locales[fechas[0]['fixture']['teams']['home']['name']],visitantes[fechas[0]['fixture']['teams']['away']['name']]]           
        
        for i in (fechas):
            print(f"Fecha {i+1}: {fechas[i][0]} vs {fechas[i][1]}")

    else: print("Error al traer los datos")

    return fechas,locales,visitantes

def apuesta()->None:
    
    print("Estos son los equipos que estan participando del torneo 2023")

    equipos_dict = equipos_liga_2023()

    equipo_op = input("Elija por cual equipo desea apostar: ")
    while(equipo_op not in equipos_dict.values()):
        print("Opcion incorrecta, intente de nuevo")
        equipo_op = input("Elija por cual equipo desea apostar(ingrese el numero): ")

    id_equipo = equipos_dict[equipo_op]

    #funcion de buscar fechas
    dict_fechas,dict_locales,dict_visitantes = fechas_teams(id_equipo)

    fecha_elegida = input("Ingrese el num de fecha por el que desea apostar: ")





    
def main()->None:

    #falta agregar la parte del menu 
    
    print("Bienvenido a la mejor plataforma de apuestas futboleras")
    ids_ingresados = []
    
    op = input("Desea acceder a la plataforma? y/n:")
    while(op.lower() not in ("y","n")):
        print("La opcion ingresada no se enuentra dentro de las posibles.")
        print("Ingrese de nuevo.")
        op = input("Desea acceder a la plataforma? y/n:")
    
    while(op.lower()!="n"):

        print("Jugatela: plataforma de apuestas.\nEsta plataforma requiere tener un usuario, elija segun el caso:")
        usuario = input("a-Iniciar sesion:\n b-Crearse una cuenta:\n")
        while(validar_usuario(usuario)==False):
            print("La opcion ingresada no se enuentra dentro de las posibles.")
            print("Ingrese de nuevo.")
            usuario = input("a-Iniciar sesion:\n b-Crearse una cuenta:\n")

        if usuario.lower()=="b":
            
            id_usario = user_registration(ids_ingresados)
            ids_ingresados.append(id_usario)

        elif usuario.lower()=="a":
            pass

        op = input("Desea acceder de nuevo a la plataforma? y/n:")

        fin = False
        
        equipos_2023 = equipos_liga_2023()
        jugadores_2023 = jugadores_equipos ()
        while not fin :
            imprimir_opciones()
            opcion_elegida = input ("Seleccione una opcion del menu: ")
            opcion_elegida = int(opcion_elegida)
            if opcion_elegida != 9  or  opcion_elegida != 0:
                opcion_seleccionada(opcion_elegida, equipos_2023, jugadores_2023)
                
                
               
            else:
                    fin = True
                    print("¡Gracias por su vista! Dejanos una opinion: ")
                    opinion = input ()


main()