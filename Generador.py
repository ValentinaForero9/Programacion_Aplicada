def PWM(x: int, f: float, a: float, duty: float)-> int:
    
     t = x / 512
     T = 1 / f
     ti = (T * duty / (100 * f))

    if (t % T) <= ti:
        
        voltaje = a / 2
    else:
        voltaje = -a / 2
        
    
    valor = int((-6.4 * voltaje) + 64)  
    return valor

print(PWM(128, 2, 4, 30))
