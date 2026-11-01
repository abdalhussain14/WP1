APP_ALT_FT = 6000 # Altitud [ft] que separa la configuración limpia de la configuración de aproximación
def calculate_thrust(h_ft, aircraft_data):
    """
    Calcula el empuje [N] del motor en descenso (a ralentí) a la altitud h_ft.

    Pasos que sigue:
    1. Elige el factor CT_desc según la altitud (modelo BADA de 3 tramos):
       - h >= hp_desc -> CT_desc_high
       - APP_ALT_FT <= h < hp_desc -> CT_desc_low
       - h < APP_ALT_FT -> CT_desc_app
    2. Calcula el empuje máximo T_max
    3. Calcula y devuelve T_desc
    """
    CT1 = aircraft_data['CT1']
    CT2 = aircraft_data['CT2']
    CT3 = aircraft_data['CT3']

    # 3 Fases del régimen de empuje BADA
    if h_ft >= aircraft_data['hp_desc']:
        CT_desc = aircraft_data['CT_desc_high']
    elif h_ft >= APP_ALT_FT:
        CT_desc = aircraft_data['CT_desc_low']
    else:
        CT_desc = aircraft_data['CT_desc_app']

    # Ecuación de empuje máximo
    T_max = CT1 * (1 - (h_ft / CT2) + CT3 * h_ft ** 2)

    # Empuje de descenso (en idle)
    T_desc = CT_desc * T_max
    return T_desc


def calculate_drag(rho, v_tas, S, m, h_ft, aircraft_data):
    """
    Calcula la resistencia aerodinámica [N] en vuelo estacionario.

    rho: Densidad [kg/(m^3)]            v_tas: true airspeed [m/s]
    S: Superfície alar [m^2]   m: masa [kg]     h_ft: altitud [ft]

    Por encima de APP_ALT_FT usa los coeficientes clean, y por debajo los de aproximación (app).
    Supone L = W, así que CL = 2W/(rho*S*V^2).
    Después CD = CD0 + CD2*CL^2 y finalmente D = (1/2)*rho*S*V^2*CD.
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

def calculate_fuel_flow(v_tas, thrust, aircraft_data):
    """
    Función que calcula el fuel flow [kg/s] según el modelo BADA.
    De inputs pilla v_tas [m/s], thrust [N] y aircraft_data [dict]

    Primero calcula el consumo específico (TSFC), con V en nudos:
    - tsfc = CF1 * (1 + V/CF2) [kg/(min*kN)]
    Después FF = tsfc * T, con T en kN, lo que da kg/min. Se divide entre 60 para devolver kg/s,
    que es lo que necesita la iteración de 1 s de getCDO.
    """
    MS_TO_KT = 3600 / 1852
    tsfc = aircraft_data['CF1'] * (1 + (v_tas * MS_TO_KT) / aircraft_data['CF2'])
    FF = tsfc * (thrust / 1000)
    return FF / 60