# -*- coding: utf-8 -*-


# Cálculo de la serie de Taylor para la exponencial
def taylor_exp(x: float, max_t: int) -> float:
    acc = 0
    p = x 
    fre = 1  

    for i in range (1, max_t):
        d = p / fre  
        if d < 0.0001:  
            break
        acc += d 
        p *= x  
        fre *= (i + 1)  

    return acc


# Cálculo de la serie de Taylor para el coseno
def taylor_cos (x: float, max_t: int) -> float:
    acc = 1
    p = x*x
    fre = 2  
    sign = -1  
    for i in range (1, max_t):
        d= p / fre 
        if d < 0.0001:  
            break
        acc += sign * d 
        fre *= 2 * i  
        sign *= -1  

    return acc


# Cálculo de la serie de Taylor para el logaritmo natural
def taylor_ln(x: float, max_t: int) -> float:
    acc = 0
    d = x - 1  
    sign = 1 

    for i in range(1, max_t):
        if 1 / i < 0.0001:  
            break
        acc += sign * (d / i) 
        sign *= -1  
        d *= (x - 1)  

    return acc

print(taylor_exp(3, 100))
print(taylor_cos(1, 100))
print(taylor_ln(2, 100))
