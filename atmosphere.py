import math

def get_isa_atmosphere(h_ft):
    """
    Función que calcula la temperatura [K], presión [Pa] y densidad [kg/(m^3)] según el modelo atmosférico ISA, tomando h_ft de input
    h_ft: altitud en pies

    Usa dos capas:
    - Troposfera (hasta 11 km): la temperatura baja linealmente con la altura.
    - Estratosfera baja (>= 11 km): temperatura constante y presión que aumenta de forma exponencial

    La densidad sale de la ley de los gases ideales rho = P / (R * T)

    Esta función se llama en cada paso de getCDO, debido a que la densidad cambia con la altitud y afecta a la resistencia aerodinámica.
    """

    h_m = h_ft * 0.3048  # Convertimos la altitud a metros para los cálculos

    T0 = 288.15  # K
    P0 = 101325  # Pa
    a = -0.0065  # Gradiente térmico (K/m)
    g = 9.80665  # m/s^2
    R = 287.05  # J/(kg*K)

    if h_m < 11000:  # Troposfera
        T = T0 + a * h_m
        P = P0 * (T / T0) ** (-g / (a * R))
    else:  # Estratosfera baja (hasta ~20km)
        T = T0 + a * 11000
        P11 = P0 * (T / T0) ** (-g / (a * R))
        P = P11 * math.exp(-g / (R * T) * (h_m - 11000))

    rho = P / (R * T)
    return T, P, rho