# atmosphere.py
import math


def get_isa_atmosphere(h_ft):
    """
    Calcula temperatura, presión y densidad según ISA
    h_ft: altitud en pies
    """
    h_m = h_ft * 0.3048  # Conversión a metros

    T0 = 288.15  # K
    P0 = 101325  # Pa
    rho0 = 1.225  # kg/m^3
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