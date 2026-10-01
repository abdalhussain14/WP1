# optimum_speed.py
from performance import calculate_drag, calculate_thrust


def get_minimum_rod_speed(rho, S, m, h_ft, aircraft_data):
    """
    Busca iterativamente la velocidad (TAS) que minimiza el Rate of Descent (RoD).
    """
    g = 9.81
    W = m * g
    T_desc = calculate_thrust(h_ft, aircraft_data)

    best_v = 0
    min_rod = float('inf')

    # Ampliamos el rango de búsqueda: de 50 m/s a 320 m/s (aprox. 100 kts a 620 kts TAS)
    for v_tas in range(50, 320):
        Drag = calculate_drag(rho, v_tas, S, m, h_ft, aircraft_data)

        # Ecuación de Rate of Descent
        rod = (Drag - T_desc) * v_tas / W

        # Buscamos el mínimo RoD positivo
        if 0 < rod < min_rod:
            min_rod = rod
            best_v = v_tas

    return best_v, min_rod