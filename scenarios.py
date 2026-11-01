# Escenarios 1 y 2 del WP1 (llegadas simultáneas y secuenciación a 2 min en el IAF)
import numpy as np
from getCDO import getCDO
from star_data import arrivals, star_distance_nm, T_ENTRY_S1, SEPARATION_S2

NM_TO_M = 1852.0
M_TO_FT = 1 / 0.3048


def fmt_time(t_s):
    """Pasa segundos desde las 00:00:00 a texto HH:MM:SS"""
    t_s = int(round(t_s))
    return f"{t_s // 3600:02d}:{(t_s % 3600) // 60:02d}:{t_s % 60:02d}"


def fmt_delta(dt_s):
    """Pasa de una diferencia de segundos a texto con signo -> '+mm:ss' / '-mm:ss'."""
    if dt_s >= 0:
        sign = '+'
    else:
        sign = '-'
    dt_s = int(round(abs(dt_s)))
    return f"{sign}{dt_s // 60:02d}:{dt_s % 60:02d}"


def entry_point_data(x, h, t, distance_m):
    """
    Función que, partiendo de la trayectoria (x, h, t) y la distancia de la STAR, calcula
    y devuelve tanto la altitud [ft] en el punto de entrada de la STAR como el tiempo de vuelo [s]
    entre el punto de entrada de la STAR y el IAF.

    Calcula estos valores mediante interpolaciones lineales.
    """
    d_traj = -np.array(x)  # distancia al IAF (positiva, creciente)
    if distance_m > d_traj[-1]:
        raise ValueError(
            f"La STAR ({distance_m / NM_TO_M:.1f} NM) es más larga que la trayectoria "
            f"simulada ({d_traj[-1] / NM_TO_M:.1f} NM hasta FL400)")
    h_entry_m = np.interp(distance_m, d_traj, h)
    t_flight = np.interp(distance_m, d_traj, t)
    return h_entry_m * M_TO_FT, t_flight


def compute_scenario1():
    """
    Escenario 1: todas las arrivals están en el primer WP de su STAR a las 11:45:00.

    Por cada arrival en star_data simula el CDO, calcula la altura de entrada a la STAR y
    el tiempo en el que llega a al IAF, sumando el tiempo de vuelo a 11:45:00.

    Devuelve una lista con los resultados para cada arrival de star_data.
    """
    results = []
    for arr in arrivals:
        x, h, t = getCDO(arr['aircraft'], arr['mlw_percent'], return_time=True)
        d_m = star_distance_nm[arr['id']] * NM_TO_M
        h_entry_ft, t_flight = entry_point_data(x, h, t, d_m)
        results.append({
            **arr,
            'dist_nm': star_distance_nm[arr['id']],
            'h_entry_ft': h_entry_ft,
            't_flight_s': t_flight,
            't_entry_s': T_ENTRY_S1,
            't_iaf_s': T_ENTRY_S1 + t_flight,
        })
    return results


def compute_scenario2(res1):
    """
    Escenario 2: separación exacta de SEPARATION_S2 en el IAF.

    Ordenamos en primer lugar las arrivals del escenario 1 por tiempo de llegada al IAF.
    A cada arrival (excepto la primera) le añadimos SEPARATION_S2 al tiempo en IAF y calculamos el nuevo tiempo en entry,
    sabiendo que ni el tiempo de vuelo ni la altura de entrada cambian.

    También al resultado obtenido le añadimos una propiedad adjust_s, que resta el tiempo real en el entry del previsto (11:45:00).
    """
    order = sorted(res1, key=lambda r: r['t_iaf_s'])  # Devuelve la lista de resultados del escenario 1 ordenada por t_iaf_s
    t_iaf_first = order[0]['t_iaf_s']

    results = []
    for k, r in enumerate(order):
        t_iaf_new = t_iaf_first + k * SEPARATION_S2 # Nuevo tiempo en IAF (para el primero es el mismo)
        t_entry_new = t_iaf_new - r['t_flight_s']  # el tiempo de vuelo no cambia
        results.append({
            **r,
            'pos': k + 1,
            't_iaf_new_s': t_iaf_new,
            't_entry_new_s': t_entry_new,
            'adjust_s': t_entry_new - T_ENTRY_S1,  # >0 retraso, <0 adelanto
        })
    return results


"""
Funciones para mostrar en consola los resultados de cada escenario
"""
def print_scenario1(res1):
    print("\n=== ESCENARIO 1: llegadas simultáneas al STAR entry (11:45:00) ===")
    print(f"{'STAR':<9}{'Avión':<12}{'%MLW':>5}{'Dist[NM]':>9}{'Alt entry[ft]':>15}"
          f"{'T vuelo':>10}{'Hora IAF':>11}")
    for r in sorted(res1, key=lambda r: r['t_iaf_s']):
        print(f"{r['id']:<9}{r['aircraft']:<12}{r['mlw_percent']:>5}{r['dist_nm']:>9.1f}"
              f"{r['h_entry_ft']:>15.0f}{fmt_time(r['t_flight_s']):>10}"
              f"{fmt_time(r['t_iaf_s']):>11}")

    order = sorted(res1, key=lambda r: r['t_iaf_s'])
    print("\nSeparaciones entre llegadas consecutivas al IAF:")
    for a, b in zip(order, order[1:]):
        print(f"  {a['id']} -> {b['id']}: {b['t_iaf_s'] - a['t_iaf_s']:.0f} s")


def print_scenario2(res2):
    print(f"\n=== ESCENARIO 2: separación de {SEPARATION_S2} s en el IAF ===")
    print(f"{'Pos':<4}{'STAR':<9}{'Avión':<12}{'Alt entry[ft]':>15}{'Hora entry':>12}"
          f"{'Ajuste':>9}{'Hora IAF':>11}")
    for r in res2:
        print(f"{r['pos']:<4}{r['id']:<9}{r['aircraft']:<12}{r['h_entry_ft']:>15.0f}"
              f"{fmt_time(r['t_entry_new_s']):>12}{fmt_delta(r['adjust_s']):>9}"
              f"{fmt_time(r['t_iaf_new_s']):>11}")


def run_scenarios():
    """
    Función que ejecuta cada escenario y escribe en consola los resultados.
    Se ejecuta en la función main del programa.
    """
    res1 = compute_scenario1()
    res2 = compute_scenario2(res1)
    print_scenario1(res1)
    print_scenario2(res2)
    return res1, res2