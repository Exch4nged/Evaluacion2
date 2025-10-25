import requests  # Para hacer peticiones HTTP a APIs
import urllib.parse  # Para codificar parámetros en URLs

route_url = "https://graphhopper.com/api/1/route?"  # URL del servicio de rutas
key = "dfe6d06e-6619-4130-b86c-5c0ed411a9c1"  # Tu clave de API

# Diccionario para traducir las instrucciones al español
traducciones_instrucciones = {
    "Continue": "Continúe",
    "Turn right": "Gire a la derecha", 
    "Turn left": "Gire a la izquierda",
    "Turn sharp right": "Gire fuertemente a la derecha",
    "Turn sharp left": "Gire fuertemente a la izquierda",
    "Turn slight right": "Gire ligeramente a la derecha",
    "Turn slight left": "Gire ligeramente a la izquierda",
    "Keep right": "Manténgase a la derecha",
    "Keep left": "Manténgase a la izquierda",
    "Enter roundabout": "Entre a la rotonda",
    "Leave roundabout": "Salga de la rotonda",
    "Arrive at destination": "Llegue a su destino",
    "onto": "hacia",
    "and drive toward": "y conduzca hacia"
}

def traducir_instruccion(instruccion):
    """Función para traducir las instrucciones al español"""
    instruccion_traducida = instruccion
    for eng, esp in traducciones_instrucciones.items():
        instruccion_traducida = instruccion_traducida.replace(eng, esp)
    return instruccion_traducida

def geocoding(location, key):  # Función que convierte direcciones en coordenadas
    # Validar entrada vacía
    while location == "":
        location = input("Ingrese la ubicación nuevamente: ")
    
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})
    
    replydata = requests.get(url)  # Hace la petición a la API
    json_data = replydata.json()  # Convierte respuesta a JSON
    json_status = replydata.status_code  # Obtiene código de estado
    
    if json_status == 200 and len(json_data["hits"]) != 0:  # Si la petición fue exitosa
        lat = json_data["hits"][0]["point"]["lat"]  # Extrae la latitud
        lng = json_data["hits"][0]["point"]["lng"]  # Extrae la longitud
        name = json_data["hits"][0]["name"]  # Extrae el nombre del lugar
        value = json_data["hits"][0]["osm_value"]  # Extrae el tipo de lugar
        
        # Traducir tipo de lugar
        tipos_lugar = {
            "city": "ciudad",
            "town": "pueblo",
            "state": "estado/provincia",
            "country": "país",
            "suburb": "suburbio"
        }
        value_es = tipos_lugar.get(value, value)
        
        if "country" in json_data["hits"][0]:  # Verifica si existe el campo país
            country = json_data["hits"][0]["country"]
        else:
            country = ""
        
        if "state" in json_data["hits"][0]:  # Verifica si existe el campo estado
            state = json_data["hits"][0]["state"]
        else:
            state = ""
        
        if len(state) != 0 and len(country) != 0:  # Si hay estado y país
            new_loc = name + ", " + state + ", " + country
        elif len(state) != 0:  # Si solo hay estado
            new_loc = name + ", " + country
        else:  # Si no hay ninguno
            new_loc = name
        
        print("URL de API de Geocodificación para " + new_loc + " (Tipo de Ubicación: " + value_es + ")\n" + url)
    else:  # Si hubo un error
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de API de Geocodificación: " + str(json_status) + "\nMensaje de error: " + json_data["message"])
    
    return json_status, lat, lng, new_loc  # Retorna código, coordenadas y ubicación


# BUCLE PRINCIPAL CON SELECCIÓN DE VEHÍCULO 
print("=================================================")
print("   APLICACIÓN DE RUTAS GRAPHHOPPER EN ESPAÑOL   ")
print("=================================================")
print("Integrantes del grupo:")
print("- Axl Urrutia, 21245254-8, ax.urrutia@duocuc.cl")
print("- Thomas Henriquez, 21650602-2, tho.henriquez@duocuc.cl")
print("- Maikol Mamani, 25530035-0, mai.mamani@duocuc.cl")
print("=================================================\n")

while True:
    # MENÚ DE VEHÍCULOS 
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Perfiles de vehículo disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("automóvil, bicicleta, a pie")
    print("(también puede usar: car, bike, foot)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("Escriba 'salir' o 's' para terminar el programa")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    
    # Diccionario para mapear términos en español a inglés
    vehiculos_esp_ing = {
        "automóvil": "car",
        "automovil": "car",
        "auto": "car",
        "carro": "car",
        "coche": "car",
        "bicicleta": "bike",
        "bici": "bike",
        "a pie": "foot",
        "pie": "foot",
        "caminando": "foot",
        "caminar": "foot"
    }
    
    profile = ["car", "bike", "foot"]  # Lista de vehículos válidos en inglés
    vehicle_input = input("Ingrese un perfil de vehículo: ").lower()
    
    # Validar si el usuario quiere salir
    if vehicle_input == "salir" or vehicle_input == "s" or vehicle_input == "quit" or vehicle_input == "q":
        print("\n¡Gracias por usar la aplicación de rutas! Hasta luego.")
        break
    
    # Verificar si se ingresó en español y convertir a inglés
    if vehicle_input in vehiculos_esp_ing:
        vehicle = vehiculos_esp_ing[vehicle_input]
    elif vehicle_input in profile:
        vehicle = vehicle_input
    else: 
        vehicle = "car"  # Vehículo por defecto
        print("No se ingresó un perfil de vehículo válido. Usando el perfil de automóvil.")
    
    # Traducir el tipo de vehículo para mostrar
    vehiculos_es = {"car": "automóvil", "bike": "bicicleta", "foot": "a pie"}
    vehicle_es = vehiculos_es.get(vehicle, vehicle)
    print(f"Vehículo seleccionado: {vehicle_es}")
    
    # Solicitar ubicación de origen
    loc1 = input("\nUbicación de inicio: ")
    if loc1.lower() == "salir" or loc1.lower() == "s" or loc1 == "quit" or loc1 == "q":
        print("\n¡Gracias por usar la aplicación de rutas! Hasta luego.")
        break
    orig = geocoding(loc1, key)  # Obtiene coordenadas del origen
    
    # Solicitar ubicación de destino
    loc2 = input("\nDestino: ")
    if loc2.lower() == "salir" or loc2.lower() == "s" or loc2 == "quit" or loc2 == "q":
        print("\n¡Gracias por usar la aplicación de rutas! Hasta luego.")
        break
    dest = geocoding(loc2, key)  # Obtiene coordenadas del destino
    
    print("=================================================")
    
    # CALCULAR RUTA 
    if orig[0] == 200 and dest[0] == 200:  # Si ambas ubicaciones son válidas
        # Construir parámetros de la URL
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])  # Punto de origen (lat,lng)
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])  # Punto de destino (lat,lng)
        
        # Construir URL completa con el tipo de vehículo
        paths_url = route_url + urllib.parse.urlencode({"key":key, "vehicle":vehicle}) + op + dp
        
        # Hacer la petición a la API de rutas
        paths_status = requests.get(paths_url).status_code  # Código de estado
        paths_data = requests.get(paths_url).json()  # Datos JSON de la ruta
        
        print("Estado de API de Rutas: " + str(paths_status) + "\nURL de API de Rutas:\n" + paths_url)
        
        print("=================================================")
        print("Direcciones desde " + orig[3] + " hasta " + dest[3] + " en " + vehicle_es)
        print("=================================================")
        
        if paths_status == 200:  # Si la ruta se calculó correctamente
            # Calcular distancia en millas y kilómetros
            miles = (paths_data["paths"][0]["distance"]) / 1000 / 1.61  # Convertir metros a millas
            km = (paths_data["paths"][0]["distance"]) / 1000  # Convertir metros a kilómetros
            
            # Calcular duración del viaje (convertir milisegundos a hh:mm:ss)
            sec = int(paths_data["paths"][0]["time"] / 1000 % 60)  # Segundos
            min = int(paths_data["paths"][0]["time"] / 1000 / 60 % 60)  # Minutos
            hr = int(paths_data["paths"][0]["time"] / 1000 / 60 / 60)  # Horas
            
            # Mostrar resultados formateados con máximo 2 decimales
            print("Distancia recorrida: {0:.2f} millas / {1:.2f} km".format(miles, km))
            print("Duración del viaje: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
            print("=================================================")
            
            # ========== INSTRUCCIONES PASO A PASO EN ESPAÑOL ==========
            print("\nInstrucciones detalladas del viaje:")
            print("-------------------------------------------------")
            
            # Recorrer todas las instrucciones de la ruta
            for i, instruccion in enumerate(paths_data["paths"][0]["instructions"], 1):
                # Extraer el texto de la instrucción
                texto_instruccion = instruccion["text"]
                # Traducir la instrucción al español
                texto_instruccion_es = traducir_instruccion(texto_instruccion)
                # Extraer la distancia de este paso
                distancia = instruccion["distance"]
                # Mostrar la instrucción con su distancia (máximo 2 decimales)
                print("{0}. {1} ( {2:.2f} km / {3:.2f} millas )".format(
                    i, 
                    texto_instruccion_es, 
                    distancia/1000, 
                    distancia/1000/1.61
                ))
            
            print("=================================================")
        else:  # ========== MANEJO DE ERRORES ==========
            # Si la API no pudo calcular la ruta
            if "message" in paths_data:
                mensaje_error = paths_data["message"]
                # Traducir mensajes de error comunes
                if "Connection between locations not found" in mensaje_error:
                    mensaje_error = "No se encontró conexión entre las ubicaciones"
                elif "Wrong credentials" in mensaje_error:
                    mensaje_error = "Credenciales incorrectas. Verifique su clave API"
                elif "Cannot find point" in mensaje_error:
                    mensaje_error = "No se puede encontrar el punto especificado"
                elif "Vehicle profile" in mensaje_error:
                    mensaje_error = "Perfil de vehículo no válido"
                    
                print("Mensaje de error: " + mensaje_error)
            else:
                print("Error desconocido al calcular la ruta")
            print("*************************************************")
    else:  # Si alguna de las ubicaciones no fue válida
        print("\nNo se pudo calcular la ruta.")
        if orig[0] != 200:
            print("Error con la ubicación de origen: " + loc1)
        if dest[0] != 200:
            print("Error con la ubicación de destino: " + loc2)
        print("Por favor, verifique las ubicaciones ingresadas.")
        print("*************************************************")

print("\n=================================================")
print("        FIN DE LA APLICACIÓN                     ")
print("=================================================")