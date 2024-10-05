import board
import busio
import time
from digitalio import DigitalInOut
import adafruit_ssd1306
import math

i2c = busio.I2C(board.GP1, board.GP0)
reset_pin = DigitalInOut(board.GP5)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, reset=reset_pin)

oled.fill(0)
oled.show()

brazo_confg = {
    "pantalla": {"ancho": 128, "alto": 64},
    "base": {"ancho": 10, "alto": 10, "pos": [64, 64]},  
    "segmentos": [
        {"longitud": 30, "angulo": 0},  
        {"longitud": 20, "angulo": 0}   
    ]
}

def dibujar_base():
    base = brazo_confg["base"]
    oled.fill_rect(base["pos"][0] - base["ancho"] // 2, base["pos"][1] - base["alto"], base["ancho"], base["alto"], 1)

def calcular_segmento(x_inicial, y_inicial, longitud, angulo):
    x_final = x_inicial + longitud * math.cos(math.radians(angulo))
    y_final = y_inicial - longitud * math.sin(math.radians(angulo))
    return int(x_final), int(y_final)

def dibujar_brazo(angulos):
    oled.fill(0)
    dibujar_base()

    x, y = brazo_confg["base"]["pos"]
    y -= brazo_confg["base"]["alto"]

    for i, segmento in enumerate(brazo_confg["segmentos"]):
        longitud = segmento["longitud"]
        angulo = sum(angulos[:i+1]) 

        x_nuevo, y_nuevo = calcular_segmento(x, y, longitud, angulo)

        oled.line(x, y, x_nuevo, y_nuevo, 1)

        x, y = x_nuevo, y_nuevo

    oled.show()

while True:
    try:
        angulos = []
        angulos.append(float(input("Angulo primer segmento (de 0 a 180): ")))
        angulos.append(float(input("Angulo segundo segmento (de 0 a 90): ")))
      
        if not (0 <= angulos[0] <= 180):
            print("El angulo debe estar entre 0 y 180.")
            continue
        if not (0 <= angulos[1] <= 90):
            print("El angulo debe estar entre 0 y 90.")
            continue

        dibujar_brazo(angulos)

        time.sleep(1)

    except ValueError:
        print("Numero invalido.")
