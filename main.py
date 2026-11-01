import matplotlib.pyplot as plt
from getCDO import getCDO
from scenarios import run_scenarios


def main():
    """
    Función principal del programa.

    Llama en primer lugar a la función run_scenarios() de scenarios.py, que calcula y muestra
    los resultados de cada escenario en consola.

    Después, para poder dibujar el gráfico para cada modelo y peso, se llama a la función getCDO()
    en cada caso para conseguir la trayectoria y graficarla.
    """
    run_scenarios()

    # Los modelos de aeronaves y pesos para el bucle
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

    # Formato de la gràfica y leyenda
    plt.title("Simulador de Operación de Descenso Continuo (CDO)")
    plt.xlabel("x [m]")
    plt.ylabel("h [m]")

    plt.legend(loc='upper right', fontsize=9)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()


if __name__ == "__main__":
    main()
