# getCDO.py
from aircraft_data import get_aircraft_data
from atmosphere import get_isa_atmosphere
from optimum_speed import get_minimum_rod_speed
import math


def getCDO(aircraft_model, MLW_percent, return_time=False):
    """
    Genera una trayectoria 2D [x, h] simulada hacia atrás.

    Por defecto devuelve (x, h), igual que antes.
    Si return_time=True devuelve (x, h, t), donde t[i] es el tiempo [s]
    que tarda el avión en llegar al IAF desde el punto i de la trayectoria
    (t = 0 en el IAF; como se simula hacia atrás, t crece 1 s por iteración).
    """
    ac_data = get_aircraft_data(aircraft_model)
    if not ac_data:
        raise ValueError("Aircraft model not found")

    # Peso final de la aeronave
    m = ac_data['MLW'] * (MLW_percent / 100.0)
    S = ac_data['S']

    # Condiciones iniciales (simulación hacia atrás desde el IAF)
    h_ft = 6000  # ft
    x_m = 0  # m

    x_history = [x_m]
    h_history = [h_ft * 0.3048]  # guardamos altitud en metros para el gráfico
    t_history = [0]  # tiempo hasta el IAF [s]

    delta_t = 1  # iteración de 1 segundo

    # Hmax = FL400 (40,000 ft)
    while h_ft <= 40000:
        # 1. Calcular atmósfera
        T, P, rho = get_isa_atmosphere(h_ft)

        # 2. Calcular velocidad óptima y Rate of Descent (RoD)
        v_tas, rod_ms = get_minimum_rod_speed(rho, S, m, h_ft, ac_data)

        if rod_ms == float('inf'):
            break  # Evitar bucles infinitos si no converge

        # 3. Integración hacia atrás
        # Como vamos hacia atrás, SUMAMOS altitud y RESTAMOS distancia X
        h_m = h_ft * 0.3048
        h_m += rod_ms * delta_t
        h_ft = h_m / 0.3048

        # Cálculo de la distancia horizontal (aproximación v_tas aprox v_ground en calma)
        # Angulo de descenso gamma
        gamma = math.asin(rod_ms / v_tas)
        v_horizontal = v_tas * math.cos(gamma)

        x_m -= v_horizontal * delta_t

        # Guardar puntos
        x_history.append(x_m)
        h_history.append(h_m)
        t_history.append(t_history[-1] + delta_t)

    if return_time:
        return x_history, h_history, t_history
    return x_history, h_history