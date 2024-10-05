  import math

def PWM(x: int, f: float, a: float, dutty: float, offset: float) -> int:
    t = x / 512  
    T = 1 / f
    c_a = T * dutty / 100
    if t % T <= c_a:
        volj = (a / 2) + offset
    else:
        volj = (-a / 2) + offset
    return int(-6.4 * volj + 64)

def SIERRA(x: int, f: float, a: float, offset: float) -> int:
    t = x / 512  
    T = 1 / f
    ti = t % T
    pe = a / T
    volj = pe * ti - (a / 2) + offset
    return int(-6.4 * volj + 64)

def COSENO(x: int, f: float, a: float, offset: float) -> int:
    t = x / 512  
    volj = (a / 2) * math.cos(2 * math.pi * f * t) + offset
    return int(-6.4 * volj + 64)

def GENERADOR(x: int, f: float, a: float, duty: float, offset: float, señal: str) -> int:
    if señal == "PWM":
        return PWM(x, f, a, duty, offset)
    elif señal == "Sierra":
        return SIERRA(x, f, a, offset)
    elif señal == "Coseno":
        return COSENO(x, f, a, offset)
    else:
        raise ValueError("Tipo de señal no soportado")
        
print (GENERADOR(100, 50, 1, 50, 0, "PWM"))          
print (GENERADOR(100, 50, 1, 50, 0, "Sierra"))        
print (GENERADOR(100, 50, 1, 50, 0, "Coseno"))      
