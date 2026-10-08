# performance.py
APP_ALT_FT = 6000
def calculate_thrust(h_ft, aircraft_data):
    """
    Calcula el empuje máximo y el empuje de descenso asumiendo idle thrust
    """
    CT1 = aircraft_data['CT1']
    CT2 = aircraft_data['CT2']
    CT3 = aircraft_data['CT3']

    # 3 Fases del régimen de empuje BADA:
    if h_ft >= aircraft_data['hp_desc']:
        CT_desc = aircraft_data['CT_desc_high']
    elif h_ft >= APP_ALT_FT:
        CT_desc = aircraft_data['CT_desc_low']
    else:
        CT_desc = aircraft_data['CT_desc_app']

    # Ecuación de empuje máximo
    T_max = CT1 * (1 - (h_ft / CT2) + CT3 * h_ft ** 2)

    # Empuje de descenso en idle
    T_desc = CT_desc * T_max
    return T_desc


def calculate_drag(rho, v_tas, S, m, h_ft, aircraft_data):
    """
    Calcula la resistencia aerodinámica (Drag)
    """
    if h_ft < APP_ALT_FT:
        CD0 = aircraft_data['CD0_app']
        CD2 = aircraft_data['CD2_app']
    else:
        CD0 = aircraft_data['CD0_clean']
        CD2 = aircraft_data['CD2_clean']

    g = 9.81
    W = m * g
    L = W
    CL = (2 * L) / (rho * S * v_tas ** 2)

    # Ecuación de resistencia
    CD = CD0 + CD2 * CL ** 2
    Drag = 0.5 * rho * v_tas ** 2 * S * CD
    return Drag