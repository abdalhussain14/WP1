# star_data.py
# Datos del escenario de llegadas a LEBL RWY 24L (WP1, apartado 3 del SoW)

# Llegadas planificadas (enunciado). El orden es el de la tabla del SoW.
arrivals = [
    {'id': 'ALBER1Z', 'aircraft': 'B767-300ER', 'mlw_percent': 80},
    {'id': 'PUMAL1Z', 'aircraft': 'B737', 'mlw_percent': 100},
    {'id': 'MARTA3Z', 'aircraft': 'B777-300', 'mlw_percent': 100},
    {'id': 'MATEX3Z', 'aircraft': 'B767-300ER', 'mlw_percent': 80},
    {'id': 'LOBAR2W', 'aircraft': 'A319-131', 'mlw_percent': 80},
    {'id': 'CASPE2W', 'aircraft': 'A320-212', 'mlw_percent': 100},
]

# Hora a la que todos llegan al primer WP de la STAR en el escenario 1
T_ENTRY_S1 = 11 * 3600 + 45 * 60  # 11:45:00 [s desde las 00:00:00]

# Separación exigida en el IAF en el escenario 2
SEPARATION_S2 = 120  # s

# Distancia a lo largo de la STAR, desde el primer WP hasta el IAF [NM].
# ATENCIÓN: estos valores son DE EJEMPLO (inventados) para poder ejecutar el código.
# Hay que sustituirlos por la longitud real de cada STAR (carta STAR de ENAIRE en el AIP)
# y poner USAR_DISTANCIAS_DEMO = False.
USAR_DISTANCIAS_DEMO = False
star_distance_nm = {
    'ALBER1Z': 49.5,
    'PUMAL1Z': 51.8,
    'MARTA3Z': 96.3,
    'MATEX3Z': 102.6,
    'LOBAR2W': 81.7,
    'CASPE2W': 88.6,
}
