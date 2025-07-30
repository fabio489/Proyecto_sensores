import serial
import requests
from datetime import datetime

# Cambia esto a tu puerto correcto
SERIAL_PORT = 'COM15'
BAUD_RATE = 115200
API_URL = 'http://localhost:8000/api/temperatura'  # Cambia si tu API está en otro host

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

while True:
    # Leer línea de la planta
    if ser.in_waiting:
        planta_line = ser.readline().decode('utf-8').strip()
        if planta_line.startswith("Planta:"):
            planta = planta_line.split(":", 1)[1].strip()

            # Leer línea de temperatura
            if ser.in_waiting:
                temp_line = ser.readline().decode('utf-8').strip()
                if temp_line.startswith("Temperatura:"):
                    try:
                        temperatura = float(temp_line.split(":", 1)[1].strip())
                    except ValueError:
                        print("Temperatura no válida:", temp_line)
                        continue

                    # Agregar fecha y hora actual en formato ISO 8601
                    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    payload = {
                        "planta": planta,
                        "temperatura": temperatura,
                        "timestamp": timestamp
                    }
                    print("Enviando JSON:", payload)
                    try:
                        response = requests.post(API_URL, json=payload)
                        print("Respuesta de la API:", response.status_code, response.text)
                    except Exception as e:
                        print("Error enviando a la API:", e)