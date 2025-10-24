# Evaluacion2 - Aplicación de Rutas GraphHopper

## Descripción
Aplicación en Python que utiliza la API de GraphHopper para calcular rutas entre ubicaciones, mostrando distancias, tiempos de viaje e instrucciones paso a paso en español.

## Integrantes
- Axl Urrutia, 21245254-8, ax.urrutia@duocuc.cl
- Thomas Henriquez, 21650602-2, tho.henriquez@duocuc.cl
- Maikol Mamani, 25530035-0, mai.mamani@duocuc.cl

## Requisitos
- Python 3.x
- Módulo requests (`pip install requests`)
- Clave API de GraphHopper

## Instalación
1. Descargar el archivo `graphhopper_parse-json_7.py`
2. Instalar dependencias: `pip install requests`
3. Obtener una clave API gratuita en https://www.graphhopper.com/

## Uso
Ejecutar el script:
```bash
python graphhopper_parse-json_7.py

1. Seleccionar modo de transporte:
automóvil / car
bicicleta / bike
a pie / foot
2. Ingresar ubicación de inicio y destino
3. Para salir, escribir 's' o 'salir'
