import matplotlib.pyplot as plt


def plot_linegraph(iters, plots, labels, title, xlabel, ylabel, yscale='linear'):
    for (label,plot) in zip(labels,plots):
        plt.plot(iters,plot, label=label)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    plt.yscale(yscale)
    plt.legend()
    plt.show()


def test_monoobjetivo():
    # Single Objective Test
    nodes = [10, 50, 100, 500, 1000, 5000, 10000]

    moa_time = [0.058593, 0.216415, 0.4468, 3.23875, 9.729239, 681.857582, 3019.211465]
    namoa_time = [0.016782, 0.039624, 0.073621, 0.189005, 0.402786, 3.267946, 1.664206]
    astar_time = [0.024021, 0.080235, 0.152528, 0.495049, 1.678004, 8.973901, 8.59563]
    dijkstra_time = [0.016957, 0.047886, 0.113705, 0.467796, 0.829749, 6.75428, 10.368193]

    moa_nodes = [12, 52, 102, 502, 1001, 5002, 9965]
    namoa_nodes = [8, 10, 37, 55, 163, 419, 347]
    astar_nodes = [8, 8, 50, 150, 340, 870, 5000]
    dijkstra_nodes = [8, 7, 55, 249, 430, 1619, 6066]

    title = "Comparativa del tiempo de ejecución (monoobjetivo)"
    xlabel = "Número de vértices del grafo"
    ylabel = "Tiempo de ejecución del algoritmo (segundos)"
    plot_linegraph(nodes, [moa_time,namoa_time,astar_time,dijkstra_time], ['MOA', 'NAMOA', 'A*', 'Dijkstra'], title, xlabel, ylabel, yscale='log')

    title = "Comparativa de vértices explorados (monoobjetivo)"
    ylabel = "Cantidad de vértices explorados"
    plot_linegraph(nodes, [moa_nodes,namoa_nodes,astar_nodes,dijkstra_nodes], ['MOA', 'NAMOA', 'A*', 'Dijkstra'], title, xlabel, ylabel, yscale='log')

def test_biobjetivo():
    # Single Objective Test
    nodes = [10, 50, 100, 500, 1000, 5000, 10000]

    moa_time = [0.025138, 0.228754, 0.198988, 3.116837,  5.414401, 299.066357, 2498.160209]
    namoa_time = [0.017026, 0.051, 0.076313, 0.181018, 0.392842, 1.727393, 1.75664]
    pulse_time = [0.016106, 0.030003, 0.045066, 0.045506, 0.136212, 0.33868, 0.325766]
    bdijkstra_time = [0.024769, 0.08851, 0.162084, 0.7971, 1.562354, 7.730177, 16.33514]

    moa_nodes = [12, 52, 102, 502, 1001, 5002, 9965]
    namoa_nodes = [8, 36, 49, 54, 166, 418, 347]
    pulse_nodes = [13, 46, 68, 73, 228, 597, 523]
    bdijkstra_nodes = [10, 50, 100, 500, 1000, 5000, 9963]

    title = "Comparativa del tiempo de ejecución (biobjetivo)"
    xlabel = "Número de vértices del grafo"
    ylabel = "Tiempo de ejecución del algoritmo (segundos)"
    plot_linegraph(nodes, [moa_time,namoa_time,pulse_time,bdijkstra_time], ['MOA', 'NAMOA', 'PULSE', 'BDijkstra'], title, xlabel, ylabel, yscale='log')

    title = "Comparativa de vértices explorados (biobjetivo)"
    ylabel = "Cantidad de vértices explorados"
    plot_linegraph(nodes, [moa_nodes,namoa_nodes,pulse_nodes,bdijkstra_nodes], ['MOA', 'NAMOA', 'PULSE', 'BDijkstra'], title, xlabel, ylabel, yscale='log')


def test_multiobjetivo():
    # Biobjective Test
    nodes = [10, 50, 100, 500, 1000, 5000, 10000]

    moa_time = [0.05651, 0.207406, 0.45079, 3.065849, 8.500368, 303.61994, 2394.548075]
    namoa_time = [0.016, 0.04852, 0.073467, 0.183431, 0.37153, 1.673997, 3.369756]

    moa_nodes = [12, 52, 102, 502, 1001, 5002, 9965]
    namoa_nodes = [8, 36, 49, 54, 166, 418, 347]

    title = "Comparativa del tiempo de ejecución (multiobjetivo)"
    xlabel = "Número de vértices del grafo"
    ylabel = "Tiempo de ejecución del algoritmo (segundos)"
    plot_linegraph(nodes, [moa_time, namoa_time], ['MOA', 'NAMOA'], title, xlabel, ylabel, yscale='log')

    title = "Comparativa de vértices explorados (multiobjetivo)"
    ylabel = "Cantidad de vértices explorados"
    plot_linegraph(nodes, [moa_nodes, namoa_nodes], ['MOA', 'NAMOA'], title, xlabel, ylabel, yscale='log')

def test_2objetivo():
    # Single Objective Test
    nodes = [10, 50, 100, 500, 1000, 5000, 10000]

    moa_time = [0.025138, 0.228754, 0.198988, 3.116837,  5.414401, 299.066357, 2498.160209]
    namoa_time = [0.017026, 0.051, 0.076313, 0.181018, 0.392842, 1.727393, 1.75664]
    pulse_time = [0.016106, 0.030003, 0.045066, 0.045506, 0.136212, 0.33868, 0.325766]
    bdijkstra_time = [0.024769, 0.08851, 0.162084, 0.7971, 1.562354, 7.730177, 16.33514]

    moa_nodes = [12, 52, 102, 502, 1001, 5002, 9965]
    namoa_nodes = [8, 36, 49, 54, 166, 418, 347]
    pulse_nodes = [13, 46, 68, 73, 228, 597, 523]
    bdijkstra_nodes = [10, 50, 100, 500, 1000, 5000, 9963]

    title = "Comparativa del tiempo de ejecución (biobjetivo)"
    xlabel = "Número de vértices del grafo"
    ylabel = "Tiempo de ejecución del algoritmo (segundos)"
    plot_linegraph(nodes, [moa_time,namoa_time,pulse_time,bdijkstra_time], ['MOA', 'NAMOA', 'PULSE', 'BDijkstra'], title, xlabel, ylabel, yscale='log')

    title = "Comparativa de vértices explorados (biobjetivo)"
    ylabel = "Cantidad de vértices explorados"
    plot_linegraph(nodes, [moa_nodes,namoa_nodes,pulse_nodes,bdijkstra_nodes], ['MOA', 'NAMOA', 'PULSE', 'BDijkstra'], title, xlabel, ylabel, yscale='log')
