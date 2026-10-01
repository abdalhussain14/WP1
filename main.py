# main.py
import matplotlib.pyplot as plt
from getCDO import getCDO
from scenarios import run_scenarios


def main():
    # Escenarios 1 y 2 (apartado 3 del SoW): tiempos al IAF y secuenciación
    run_scenarios()

    # Incluimos todos los modelos de aeronaves para la iteración
    aircrafts = ['B767-300ER', 'B777-300', 'B737', 'A320-212', 'A319-131']
    weights = [100, 80]

    # Creamos el entorno de representación gráfica
    plt.figure(figsize=(12, 7))

    for model in aircrafts:
        for w in weights:
            try:
                print(f"Simulando {model} al {w}% MLW...")
                x, h = getCDO(model, w)
                plt.plot(x, h, label=f"{model} [{w}% MLW]")
            except Exception as e:
                print(f"No se pudo simular {model} al {w}%: {e}")

    # Damos el formato preciso a la gráfica
    plt.title("Simulador de Operación de Descenso Continuo (CDO)")
    plt.xlabel("x [m]")
    plt.ylabel("h [m]")

    # Movemos la leyenda y ajustamos los límites para mayor claridad visual
    plt.legend(loc='upper right', fontsize=9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


if __name__ == "__main__":
    main()
