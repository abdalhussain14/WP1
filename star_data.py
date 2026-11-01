# Datos del escenario de llegadas a LEBL RWY 24L (apartado 3 del SoW)

# lista con el id de cada STAR, el modelo de avión y su % de MLW en IAF
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

# Separación exigida en el IAF en el escenario 2 (en segundos)
SEPARATION_S2 = 120

# Distancia a lo largo de la STAR, desde el primer WP hasta el IAF [NM],
# con valores reales tomados de las cartas STAR de ENAIRE (AIP)
star_distance_nm = {
    'ALBER1Z': 49.5,
    'PUMAL1Z': 51.8,
    'MARTA3Z': 96.3,
    'MATEX3Z': 102.6,
    'LOBAR2W': 81.7,
    'CASPE2W': 88.6,
}
