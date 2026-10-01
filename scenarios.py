# scenarios.py
# Escenarios 1 y 2 del WP1 (llegadas simultáneas y secuenciación a 2 min en el IAF)
import numpy as np
from getCDO import getCDO
from star_data import (arrivals, star_distance_nm, T_ENTRY_S1, SEPARATION_S2,
                       USAR_DISTANCIAS_DEMO)

NM_TO_M = 1852.0
M_TO_FT = 1 / 0.3048


def fmt_time(t_s):
    """Segundos desde las 00:00:00 -> 'HH:MM:SS'."""
    t_s = int(round(t_s))
    return f"{t_s // 3600:02d}:{(t_s % 3600) // 60:02d}:{t_s % 60:02d}"


def fmt_delta(dt_s):
    """Diferencia en segundos -> '+mm:ss' / '-mm:ss'."""
    sign = '+' if dt_s >= 0 else '-'
    dt_s = int(round(abs(dt_s)))
    return f"{sign}{dt_s // 60:02d}:{dt_s % 60:02d}"


def entry_point_data(x, h, t, distance_m):
    """
    A partir de la trayectoria (x [m], h [m], t [s]) de getCDO, devuelve la altitud
    [ft] y el tiempo de vuelo [s] hasta el IAF en el punto situado a distance_m del IAF.
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
    Escenario 1: todos los aviones están en el primer WP de su STAR a las 11:45:00.
    Devuelve una lista de dicts (uno por llegada) con altitud en el STAR entry,
    tiempo de vuelo hasta el IAF y hora de llegada al IAF.
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
    Escenario 2: separación exacta de SEPARATION_S2 en el IAF, mismo orden de llegada
    que el escenario 1 y sin ajustar el primer avión.
    Devuelve una lista (en orden de llegada al IAF) con la nueva hora en el STAR entry,
    el ajuste respecto al escenario 1 y la hora en el IAF.
    """
    order = sorted(res1, key=lambda r: r['t_iaf_s'])  # orden de llegada al IAF (esc. 1)
    t_iaf_first = order[0]['t_iaf_s']

    results = []
    for k, r in enumerate(order):
        t_iaf_new = t_iaf_first + k * SEPARATION_S2
        t_entry_new = t_iaf_new - r['t_flight_s']  # el tiempo de vuelo no cambia
        results.append({
            **r,
            'pos': k + 1,
            't_iaf_new_s': t_iaf_new,
            't_entry_new_s': t_entry_new,
            'adjust_s': t_entry_new - T_ENTRY_S1,  # >0 retraso, <0 adelanto
        })
    return results


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
    if USAR_DISTANCIAS_DEMO:
        print("*** AVISO: se usan distancias de STAR DE EJEMPLO (star_data.py). "
              "Los resultados NO son válidos hasta poner las distancias reales. ***")
    res1 = compute_scenario1()
    res2 = compute_scenario2(res1)
    print_scenario1(res1)
    print_scenario2(res2)
    return res1, res2