import math
import csv
import matplotlib.pyplot as plt

# ==========================================
# 1. CONSTANTES FÍSICAS Y CARGA DE DATOS
# ==========================================
G = 9.80665  # Gravedad [m/s^2]
FT_TO_M = 0.3048  # Conversión de pies a metros


def load_and_convert_csv(filepath):
    """
    Lee el archivo CSV transpuesto (aviones en columnas, parámetros en filas)
    y lo convierte a unidades del Sistema Internacional (SI).
    """
    si_data = {}
    with open(filepath, mode='r', encoding='utf-8-sig') as file:
        # Detectar el separador leyendo la primera línea
        primera_linea = file.readline()
        separador = ';' if ';' in primera_linea else ','
        file.seek(0)

        reader = csv.reader(file, delimiter=separador)

        # 1. Leer las cabeceras (nombres de los aviones)
        headers = next(reader)
        aircraft_models = [h.strip() for h in headers[1:]]  # Evitamos la columna 'Parameter'

        for model in aircraft_models:
            si_data[model] = {}

        # 2. Leer fila por fila y asignar el valor al parámetro correspondiente
        for row in reader:
            if not row or len(row) < 2:
                continue

            param_name = row[0].strip()

            for i, model in enumerate(aircraft_models):
                try:
                    val = float(row[i + 1].strip())
                except ValueError:
                    continue  # Saltar si la celda está vacía o no es un número

                # Clasificar y aplicar factores de conversión al Sistema Internacional
                if "Landing Weight" in param_name:
                    si_data[model]["MLW"] = val * 1000.0
                elif param_name.startswith("S "):
                    si_data[model]["S"] = val
                elif "CD0_app" in param_name:
                    si_data[model]["CD0_app"] = val
                elif "CD2_app" in param_name:
                    si_data[model]["CD2_app"] = val
                elif "CD0_clean" in param_name:
                    si_data[model]["CD0_clean"] = val
                elif "CD2_clean" in param_name:
                    si_data[model]["CD2_clean"] = val
                elif "hp_desc" in param_name:
                    si_data[model]["hp_desc"] = val * FT_TO_M
                elif "CT_Desc_high" in param_name:
                    si_data[model]["CT_Desc_high"] = val
                elif "CT_Desc_low" in param_name:
                    si_data[model]["CT_Desc_low"] = val
                elif "CT_Desc_app" in param_name:
                    si_data[model]["CT_Desc_app"] = val
                elif "CT1" in param_name:
                    si_data[model]["C_T1"] = val
                elif "CT2" in param_name:
                    si_data[model]["C_T2"] = val * FT_TO_M
                elif "CT3" in param_name:
                    si_data[model]["C_T3"] = val / (FT_TO_M ** 2)
                elif "CF1" in param_name:
                    si_data[model]["C_F1"] = val / 60000.0
                elif "CF2" in param_name:
                    si_data[model]["C_F2"] = val * 0.514444

    return si_data


# ==========================================
# 2. MOTOR DEL SIMULADOR CDO
# ==========================================
def get_isa_density(h_m):
    """Calcula la densidad atmosférica (ISA)."""
    if h_m < 11000.0:
        T = 288.15 - 0.0065 * h_m
        rho = 1.225 * (T / 288.15) ** 4.256848
    else:
        T = 216.65
        rho = 0.36391 * math.exp(-G / (287.05287 * T) * (h_m - 11000.0))
    return rho


def getCDO(aircraft_model, MLW_percent, si_data):
    """Simula la trayectoria CDO hacia atrás operando en SI."""
    ac = si_data[aircraft_model]

    # Condiciones iniciales en el IAF: x=0 y altitud a 5.000 pies
    x = 0.0
    h_m = 5000.0 * FT_TO_M

    mass = ac["MLW"] * (MLW_percent / 100.0)
    weight = mass * G

    x_traj = [x]
    h_traj = [h_m]
    delta_t = 1.0

    # Bucle hasta alcanzar FL400 (12.192 m)
    while h_m <= 12192.0:
        rho = get_isa_density(h_m)

        # Empuje (Idle Thrust)
        T_max = ac["C_T1"] * (1.0 - h_m / ac["C_T2"] + ac["C_T3"] * h_m ** 2)
        if h_m > ac["hp_desc"]:
            T_desc = ac["CT_Desc_high"] * T_max
        else:
            T_desc = ac["CT_Desc_low"] * T_max

        CD0 = ac["CD0_clean"]
        CD2 = ac["CD2_clean"]

        # Velocidad de mínimo ROD
        term1 = 4.0 * CD2 * weight ** 2
        term2 = 3.0 * rho ** 2 * ac["S"] ** 2 * CD0
        V_minROD = (term1 / term2) ** 0.25

        # Resistencia (Drag)
        CL_opt = math.sqrt((3.0 * CD0) / CD2)
        D = 0.5 * rho * V_minROD ** 2 * ac["S"] * (CD0 + CD2 * CL_opt ** 2)

        # RoD y Ángulo
        RoD = V_minROD * ((D - T_desc) / weight)
        sin_gamma = max(-1.0, min(1.0, (D - T_desc) / weight))
        gamma = math.asin(sin_gamma)

        V_x = V_minROD * math.cos(gamma)

        # Cinemática inversa
        x -= V_x * delta_t
        h_m += RoD * delta_t

        # Consumo y recuperación de masa al simular hacia atrás
        eta = ac["C_F1"] * (1.0 + V_minROD / ac["C_F2"])
        FF = eta * T_desc

        mass += FF * delta_t
        weight = mass * G

        x_traj.append(x)
        h_traj.append(h_m)

    return x_traj, h_traj


# ==========================================
# 3. SCRIPT PRINCIPAL DE EJECUCIÓN
# ==========================================
def main():
    archivo_datos = 'aircraft_data.csv'
    try:
        aircraft_data_si = load_and_convert_csv(archivo_datos)
    except FileNotFoundError:
        print(f"Error: No se ha encontrado el archivo '{archivo_datos}'.")
        return

    aircraft_models = ["B767-300ER", "B777-300", "B737", "A320-212", "A319-131"]
    weight_conditions = [100, 80]

    plt.figure(figsize=(14, 7))

    for model in aircraft_models:
        for w_percent in weight_conditions:
            try:
                x_traj, h_traj = getCDO(model, w_percent, aircraft_data_si)
                label_name = f"{model} [{w_percent}% MLW]"
                plt.plot(x_traj, h_traj, label=label_name)
            except KeyError:
                print(f"El modelo {model} no se ha leído correctamente del CSV.")

    plt.title("Simulador de Trayectorias CDO (Hacia atrás desde IAF a 5000 ft)")
    plt.xlabel("Distancia al IAF [m] (x)")
    plt.ylabel("Altitud [m] (h)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='upper right', fontsize='small')
    plt.xlim(min(x_traj), 5000)
    plt.show()


if __name__ == "__main__":
    main()



