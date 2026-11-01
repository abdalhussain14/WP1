from aircraft_data import get_aircraft_data
from atmosphere import get_isa_atmosphere
from optimum_speed import get_minimum_rod_speed
import math

from performance import calculate_fuel_flow, calculate_thrust


def getCDO(aircraft_model, MLW_percent, return_time=False):
    """
    Función que genera la trayectoria del descenso continuo (CDO) simulando hacia atrás desde el
    IAF (6000ft) hasta FL400.

    Toma de entradas el aircraft_model (string) y el peso final (en IAF) del avión como % del MLW (ej. 80 o 100)

    Devuelve (x, h) o, con return_time=True, (x, h, t):
    - x: posición horizontal [m], que es 0 en el IAF y negativa antes de él
    - h: altitud [m]
    - t: tiempo [s] que tarda en llegar al IAF desde ese punto

    A partir de las condiciones iniciales, cada iteración (con paso de 1 segundo):
    1. Calcula la atmósfera en la altitud actual
    2. Obtiene la velocidad de mínimo RoD y ese RoD
    3. Sube altitud (RoD*dt) y resta distancia horizontal (V*cos(gamma))
    4. Suma a la masa el consumo y 1 segundo al tiempo.
    """
    ac_data = get_aircraft_data(aircraft_model)
    if not ac_data:
        raise ValueError("Aircraft model not found")

    # Peso final de la aeronave
    m = ac_data['MLW'] * (MLW_percent / 100.0)
    S = ac_data['S']

    # Condiciones iniciales (simulamos hacia atrás desde el IAF)
    h_ft = 6000
    x_m = 0

    x_history = [x_m]
    h_history = [h_ft * 0.3048]  # guardamos altitud en metros para el gráfico
    t_history = [0]  # tiempo hasta el IAF [s]

    delta_t = 1

    while h_ft < 40000:
        # 1. Cálculo de atmosfera
        T, P, rho = get_isa_atmosphere(h_ft)

        # 2. Cálculo de velocidad óptima y Rate of Descent (RoD)
        v_tas, rod_ms = get_minimum_rod_speed(rho, S, m, h_ft, ac_data)
        thrust = calculate_thrust(h_ft, ac_data)
        fuel_flow_kg_s = calculate_fuel_flow(v_tas, thrust, ac_data)

        # 3. Subimos altitud y restamos distancia horizontal
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

        # 4. A la masa le sumamos el consumo (ya que la simulación es hacia atrás)
        m += fuel_flow_kg_s * delta_t

    if return_time:
        return x_history, h_history, t_history
    return x_history, h_history