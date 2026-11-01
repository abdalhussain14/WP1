import math

from performance import calculate_drag, calculate_thrust, APP_ALT_FT


def get_minimum_rod_speed(rho, S, m, h_ft, aircraft_data):
    """
    Función que calcula la velocidad TAS que da el mínimo rate of descent (RoD) en ralentí.

    Se deriva RoD = (D - T)*V/W respecto de V y se iguala a 0 y se encuentra que la velocidad TAS
    para el RoD mínimo és: v = sqrt( (T + sqrt(T^2 + 12*CD0*CD2*W^2)) / (3*rho*S*CD0) ).

    La función devuelve tanto v_tas [m/s], como RoD mínimo [m/s]. Si el RoD no es positivo (osea
    que el avión no desciende), salta un error.
    """
    g = 9.81
    W = m * g
    T_desc = calculate_thrust(h_ft, aircraft_data)

    if h_ft < APP_ALT_FT:
        CD0 = aircraft_data['CD0_app']
        CD2 = aircraft_data['CD2_app']
    else:
        CD0 = aircraft_data['CD0_clean']
        CD2 = aircraft_data['CD2_clean']

    v_tas = math.sqrt((T_desc + math.sqrt(T_desc**2 + 12*CD0*CD2* W**2))/(3*rho*S*CD0))

    drag = calculate_drag(rho, v_tas, S, m, h_ft, aircraft_data)
    rod = (drag - T_desc)*v_tas/W

    if rod <= 0:
        raise ValueError(
            f"A {h_ft:.0f} ft el empuje en ralentí supera la resistencia: "
            f"el avión no puede descender (RoD = {rod:.2f} m/s)")
    return v_tas, rod