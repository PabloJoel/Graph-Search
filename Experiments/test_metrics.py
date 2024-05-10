import os.path
import os
import pandas as pd
import random
from pathlib import Path

from Algorithms.AStar import AStar
from Algorithms.Dijkstra import Dijkstra
from Algorithms.MOA import MOA
from Algorithms.NAMOA import NAMOA
from Algorithms.BDijkstra import BDijkstra
from Algorithms.PULSE import PULSE
from Graphs.PandasGraph import PandasGraph
from Tests.heuristics import MockedHeuristicMOA, MockedHeuristicNAMOA, MockedHeuristicAutomatic


def tournament(start, objectives, graph, heuristic):
    moa = MOA(graph, heuristic=heuristic)
    moa.run(start_vertex=start, end_vertices=objectives)
    moa_sol = moa.solution.get_min_solution_cost(start)

    namoa = NAMOA(graph, heuristic=heuristic)
    namoa.run(start_vertex=start, end_vertices=objectives)
    namoa_sol = namoa.solution.get_min_solution_cost(start)

    bdijkstra = BDijkstra(graph)
    bdijkstra.run(start_vertex=start)
    bdijkstra_sol = bdijkstra.solution.get_min_solution_cost(start)

    pulse = PULSE(graph)
    pulse_sol = list()
    for objective in objectives:
        pulse.run(start_vertex=start, end_vertex=objective)
        pulse_sol.append(pulse.solution.get_min_solution_cost(start))

    pulse_sol = min(pulse_sol)

    all_sols = [moa_sol, namoa_sol, pulse_sol, bdijkstra_sol]
    result = {'MOA_Sol': str(moa_sol), 'NAMOA_Sol': str(namoa_sol), 'PULSE_Sol': str(pulse_sol), 'BDijkstra_Sol': str(bdijkstra_sol),
              'MOA_DOM': namoa.is_dominated(moa_sol, all_sols), 'NAMOA_DOM': namoa.is_dominated(namoa_sol, all_sols), 'PULSE_DOM': namoa.is_dominated(pulse_sol, all_sols), 'BDijkstra_DOM': namoa.is_dominated(bdijkstra_sol, all_sols),
              'MOA_Time': moa.metrics.execution_time, 'NAMOA_Time': namoa.metrics.execution_time, 'PULSE_Time': pulse.metrics.execution_time, 'BDijkstra_Time': bdijkstra.metrics.execution_time,
              'MOA_Nodes': moa.metrics.nodes_explored, 'NAMOA_Nodes': namoa.metrics.nodes_explored, 'PULSE_Nodes': pulse.metrics.nodes_explored, 'BDijkstra_Nodes': bdijkstra.metrics.nodes_explored}

    return result

def multitournament(start, objectives, graph, heuristic):
    moa = MOA(graph, heuristic=heuristic)
    moa.run(start_vertex=start, end_vertices=objectives)
    moa_sol = moa.solution.get_min_solution_cost(start)

    namoa = NAMOA(graph, heuristic=heuristic)
    namoa.run(start_vertex=start, end_vertices=objectives)
    namoa_sol = namoa.solution.get_min_solution_cost(start)

    all_sols = [moa_sol, namoa_sol]
    result = {'MOA_Sol': str(moa_sol), 'NAMOA_Sol': str(namoa_sol),
              'MOA_DOM': namoa.is_dominated(moa_sol, all_sols), 'NAMOA_DOM': namoa.is_dominated(namoa_sol, all_sols),
              'MOA_Time': moa.metrics.execution_time, 'NAMOA_Time': namoa.metrics.execution_time,
              'MOA_Nodes': moa.metrics.nodes_explored, 'NAMOA_Nodes': namoa.metrics.nodes_explored}

    return result

def singletournament(start, objectives, graph, heuristic):
    moa = MOA(graph, heuristic=heuristic)
    moa.run(start_vertex=start, end_vertices=objectives)
    moa_sol = moa.solution.get_min_solution_cost(start)

    namoa = NAMOA(graph, heuristic=heuristic)
    namoa.run(start_vertex=start, end_vertices=objectives)
    namoa_sol = namoa.solution.get_min_solution_cost(start)

    astar = AStar(graph)
    astar.run(start_vertex=start, end_vertex=objectives[0])
    astar_sol = astar.solution.get_min_solution_cost(start)

    dijkstra = Dijkstra(graph)
    dijkstra.run(start_vertex=start, end_vertex=objectives[0])
    dijkstra_sol = dijkstra.solution.get_min_solution_cost(start)

    all_sols = [moa_sol, namoa_sol, astar_sol, dijkstra_sol]
    result = {'MOA_Sol': str(moa_sol), 'NAMOA_Sol': str(namoa_sol), 'A*_Sol': str(astar_sol), 'Dijkstra_Sol': str(dijkstra_sol),
              'MOA_DOM': namoa.is_dominated(moa_sol, all_sols), 'NAMOA_DOM': namoa.is_dominated(namoa_sol, all_sols), 'A*_DOM': namoa.is_dominated(astar_sol, all_sols), 'Dijkstra_DOM': namoa.is_dominated(dijkstra_sol, all_sols),
              'MOA_Time': moa.metrics.execution_time, 'NAMOA_Time': namoa.metrics.execution_time, 'A*_Time': astar.metrics.execution_time, 'Dijkstra_Time': dijkstra.metrics.execution_time,
              'MOA_Nodes': moa.metrics.nodes_explored, 'NAMOA_Nodes': namoa.metrics.nodes_explored, 'A*_Nodes': astar.metrics.nodes_explored, 'Dijkstra_Nodes': dijkstra.metrics.nodes_explored}

    return result


def test_moa_data():

    return None
    #{'MOA_Sol': '[4, 11]', 'NAMOA_Sol': '[4, 11]', 'PULSE_Sol': '[4, 11]', 'BDijkstra_Sol': '[4, 11]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 0.035137, 'NAMOA_Time': 0.030538, 'PULSE_Time': 0.328429, 'BDijkstra_Time': 0.309774, 'MOA_Nodes': 15, 'NAMOA_Nodes': 21, 'PULSE_Nodes': 54, 'BDijkstra_Nodes': 72}

    start = 's'
    objectives = ['y1', 'y2', 'y3']
    data = pd.read_csv('moa-data.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicMOA(graph))
    print(res)


def test_namoa_data():
    return None
    #{'MOA_Sol': '[4, 10]', 'NAMOA_Sol': '[4, 10]', 'PULSE_Sol': '[4, 10]', 'BDijkstra_Sol': '[4, 10]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 0.023049, 'NAMOA_Time': 0.019109, 'PULSE_Time': 0.022111, 'BDijkstra_Time': 0.032973, 'MOA_Nodes': 10, 'NAMOA_Nodes': 10, 'PULSE_Nodes': 10, 'BDijkstra_Nodes': 15}

    start = 's'
    objectives = ['y']
    data = pd.read_csv('namoa-data.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicNAMOA(graph))
    print(res)

# -----------------ONE WEIGTHS TESTS---------------------------------------

def test_big_data10_uniobj():
    return None
    #'MOA_Time': 0.058593, 'NAMOA_Time': 0.016782, 'A*_Time': 0.024021, 'Dijkstra_Time': 0.016957, 'MOA_Nodes': 12, 'NAMOA_Nodes': 8, 'A*_Nodes': 4, 'Dijkstra_Nodes': 8}

    start = 1
    objectives = [0]
    data = pd.read_csv('big_data_10_60%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1'])
    res = singletournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data50_uniobj():
    return None
    #'MOA_Time': 0.216415, 'NAMOA_Time': 0.039624, 'A*_Time': 0.080235, 'Dijkstra_Time': 0.047886, 'MOA_Nodes': 52, 'NAMOA_Nodes': 10, 'A*_Nodes': 3, 'Dijkstra_Nodes': 7}

    start = 10
    objectives = [20]
    data = pd.read_csv('big_data_50_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1'])
    res = singletournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data100_uniobj():
    return None
    #'MOA_Time': 0.4468, 'NAMOA_Time': 0.073621, 'A*_Time': 0.152528, 'Dijkstra_Time': 0.113705, 'MOA_Nodes': 102, 'NAMOA_Nodes': 37, 'A*_Nodes': 4, 'Dijkstra_Nodes': 55}

    start = 2
    objectives = [22]
    data = pd.read_csv('big_data_100_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1'])
    res = singletournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data500_uniobj():
    return None
    #'MOA_Time': 3.23875, 'NAMOA_Time': 0.189005, 'A*_Time': 0.495049, 'Dijkstra_Time': 0.467796, 'MOA_Nodes': 502, 'NAMOA_Nodes': 55, 'A*_Nodes': 4, 'Dijkstra_Nodes': 249}

    start = 377
    objectives = [126]
    data = pd.read_csv('big_data_500_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1'])
    res = singletournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data1000_uniobj():
    return None
    #'MOA_Time': 9.729239, 'NAMOA_Time': 0.402786, 'A*_Time': 1.678004, 'Dijkstra_Time': 0.829749, 'MOA_Nodes': 1001, 'NAMOA_Nodes': 163, 'A*_Nodes': 5, 'Dijkstra_Nodes': 430}

    start = 757
    objectives = [605]
    data = pd.read_csv('big_data_1000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1'])
    res = singletournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data5000_uniobj():
    return None
    #'MOA_Time': 681.857582, 'NAMOA_Time': 3.267946, 'A*_Time': 8.973901, 'Dijkstra_Time': 6.75428, 'MOA_Nodes': 5002, 'NAMOA_Nodes': 419, 'A*_Nodes': 4, 'Dijkstra_Nodes': 1619}

    start = 1049
    objectives = [3409]
    data = pd.read_csv('big_data_5000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1'])
    res = singletournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data10000_uniobj():
    #return None
    #'MOA_Time': 3019.211465, 'NAMOA_Time': 1.664206, 'A*_Time': 8.59563, 'Dijkstra_Time': 10.368193, 'MOA_Nodes': 9965, 'NAMOA_Nodes': 347, 'A*_Nodes': 4, 'Dijkstra_Nodes': 6066}

    start = 1416
    objectives = [2783]
    data = pd.read_csv('big_data_10000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1'])
    res = singletournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)



# -----------------TWO WEIGTHS TESTS---------------------------------------

def test_big_data10():
    return None
    #{'MOA_Sol': '[18, 18]', 'NAMOA_Sol': '[18, 18]', 'PULSE_Sol': '[18, 18]', 'BDijkstra_Sol': '[18, 18]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 0.025138, 'NAMOA_Time': 0.017026, 'PULSE_Time': 0.016106, 'BDijkstra_Time': 0.024769, 'MOA_Nodes': 12, 'NAMOA_Nodes': 8, 'PULSE_Nodes': 13, 'BDijkstra_Nodes': 10}
    start = 1
    objectives = [0]
    data = pd.read_csv('big_data_10_60%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data50():
    return None
    #{'MOA_Sol': '[5, 13]', 'NAMOA_Sol': '[5, 13]', 'PULSE_Sol': '[5, 13]', 'BDijkstra_Sol': '[5, 13]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 0.228754, 'NAMOA_Time': 0.051, 'PULSE_Time': 0.030003, 'BDijkstra_Time': 0.08851, 'MOA_Nodes': 52, 'NAMOA_Nodes': 36, 'PULSE_Nodes': 46, 'BDijkstra_Nodes': 50}
    start = 10
    objectives = [20]
    data = pd.read_csv('big_data_50_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data100():
    return None
    #{'MOA_Sol': '[14, 17]', 'NAMOA_Sol': '[14, 17]', 'PULSE_Sol': '[14, 17]', 'BDijkstra_Sol': '[14, 17]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 0.198988, 'NAMOA_Time': 0.076313, 'PULSE_Time': 0.045066, 'BDijkstra_Time': 0.162084, 'MOA_Nodes': 102, 'NAMOA_Nodes': 49, 'PULSE_Nodes': 68, 'BDijkstra_Nodes': 100}
    start = 2
    objectives = [22]
    data = pd.read_csv('big_data_100_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data500():
    return None
    #{'MOA_Sol': '[19, 16]', 'NAMOA_Sol': '[19, 16]', 'PULSE_Sol': '[19, 16]', 'BDijkstra_Sol': '[19, 16]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 3.116837, 'NAMOA_Time': 0.181018, 'PULSE_Time': 0.045506, 'BDijkstra_Time': 0.7971, 'MOA_Nodes': 502, 'NAMOA_Nodes': 54, 'PULSE_Nodes': 73, 'BDijkstra_Nodes': 500}

    start = 377
    objectives = [126]
    data = pd.read_csv('big_data_500_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data1000():
    return None
    #{'MOA_Sol': '[20, 14]', 'NAMOA_Sol': '[20, 14]', 'PULSE_Sol': '[20, 14]', 'BDijkstra_Sol': '[20, 14]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 5.414401, 'NAMOA_Time': 0.392842, 'PULSE_Time': 0.136212, 'BDijkstra_Time': 1.562354, 'MOA_Nodes': 1001, 'NAMOA_Nodes': 166, 'PULSE_Nodes': 228, 'BDijkstra_Nodes': 1000}

    start = 757
    objectives = [605]
    data = pd.read_csv('big_data_1000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data5000():
    return None
    #{'MOA_Sol': '[13, 12]', 'NAMOA_Sol': '[13, 12]', 'PULSE_Sol': '[13, 12]', 'BDijkstra_Sol': '[13, 12]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 299.066357, 'NAMOA_Time': 1.727393, 'PULSE_Time': 0.33868, 'BDijkstra_Time': 7.730177, 'MOA_Nodes': 5002, 'NAMOA_Nodes': 418, 'PULSE_Nodes': 597, 'BDijkstra_Nodes': 5000}

    start = 1049
    objectives = [3409]
    data = pd.read_csv('big_data_5000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data10000():
    return None
    #{'MOA_Sol': '[26, 17]', 'NAMOA_Sol': '[26, 17]', 'PULSE_Sol': '[26, 17]', 'BDijkstra_Sol': '[26, 17]', 'MOA_DOM': False, 'NAMOA_DOM': False, 'PULSE_DOM': False, 'BDijkstra_DOM': False, 'MOA_Time': 2498.160209, 'NAMOA_Time': 1.75664, 'PULSE_Time': 0.325766, 'BDijkstra_Time': 16.33514, 'MOA_Nodes': 9965, 'NAMOA_Nodes': 347, 'PULSE_Nodes': 523, 'BDijkstra_Nodes': 9963}
    start = 1416
    objectives = [2783]
    data = pd.read_csv('big_data_10000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

# -----------------FOUR WEIGTHS TESTS---------------------------------------

def test_big_data10_multi():
    return None
    #'MOA_Time': 0.05651, 'NAMOA_Time': 0.016, 'MOA_Nodes': 12, 'NAMOA_Nodes': 8

    start = 1
    objectives = [0]
    data = pd.read_csv('big_data_10_60%_multiobjective.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = multitournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data50_multi():
    return None
    #'MOA_Time': 0.207406, 'NAMOA_Time': 0.04852, 'MOA_Nodes': 52, 'NAMOA_Nodes': 36

    start = 10
    objectives = [20]
    data = pd.read_csv('big_data_50_30%_multiobjective.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = multitournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data100_multi():
    return None
    #'MOA_Time': 0.45079, 'NAMOA_Time': 0.073467, 'MOA_Nodes': 102, 'NAMOA_Nodes': 49

    start = 2
    objectives = [22]
    data = pd.read_csv('big_data_100_30%_multiobjective.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = multitournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data500_multi():
    return None
    #'MOA_Time': 3.065849, 'NAMOA_Time': 0.183431, 'MOA_Nodes': 502, 'NAMOA_Nodes': 54}

    start = 377
    objectives = [126]
    data = pd.read_csv('big_data_500_30%_multiobjective.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = multitournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data1000_multi():
    return None
    #'MOA_Time': 8.500368, 'NAMOA_Time': 0.37153, 'MOA_Nodes': 1001, 'NAMOA_Nodes': 166}
    start = 757
    objectives = [605]
    data = pd.read_csv('big_data_1000_30%_multiobjective.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = multitournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data5000_multi():
    return None
    #'MOA_Time': 303.61994, 'NAMOA_Time': 1.673997, 'MOA_Nodes': 5002, 'NAMOA_Nodes': 418}

    start = 1049
    objectives = [3409]
    data = pd.read_csv('big_data_5000_30%_multiobjective.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = multitournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data10000_multi():
    return None
    #'MOA_Time': 2394.548075, 'NAMOA_Time': 3.369756, 'MOA_Nodes': 9965, 'NAMOA_Nodes': 347}

    start = 1416
    objectives = [2783]
    data = pd.read_csv('big_data_10000_30%_multiobjective.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = multitournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


# ---------------TWO OBJECTIVE TESTS-------------------------------------


def test_big_data10_biobjective():
    return None
    #'MOA_Sol': '[12, 15]', 'NAMOA_Sol': '[18, 18]', 'PULSE_Sol': '[12, 15]', 'BDijkstra_Sol': '[4, 6]',
    #'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False,
    #'MOA_Time': 0.060077, 'NAMOA_Time': 0.016912, 'PULSE_Time': 0.048771, 'BDijkstra_Time': 0.037501,
    #'MOA_Nodes': 12, 'NAMOA_Nodes': 8, 'PULSE_Nodes': 28, 'BDijkstra_Nodes': 10}

    start = 1
    objectives = [0,4]
    data = pd.read_csv('big_data_10_60%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data50_biobjective():
    return None
    #{'MOA_Sol': '[5, 13]', 'NAMOA_Sol': '[5, 13]', 'PULSE_Sol': '[5, 13]', 'BDijkstra_Sol': '[1, 2]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 0.215237, 'NAMOA_Time': 0.049202, 'PULSE_Time': 0.092354, 'BDijkstra_Time': 0.169693, 'MOA_Nodes': 52, 'NAMOA_Nodes': 36, 'PULSE_Nodes': 93, 'BDijkstra_Nodes': 50}

    start = 10
    objectives = [20, 47]
    data = pd.read_csv('big_data_50_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data100_biobjective():
    return None
    # {'MOA_Sol': '[14, 17]', 'NAMOA_Sol': '[14, 17]', 'PULSE_Sol': '[14, 17]', 'BDijkstra_Sol': '[1, 3]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 0.460109, 'NAMOA_Time': 0.08087, 'PULSE_Time': 0.120687, 'BDijkstra_Time': 0.35008, 'MOA_Nodes': 99, 'NAMOA_Nodes': 49, 'PULSE_Nodes': 134, 'BDijkstra_Nodes': 100}

    start = 2
    objectives = [22, 62]
    data = pd.read_csv('big_data_100_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data500_biobjective():
    return None
    # {'MOA_Sol': '[16, 20]', 'NAMOA_Sol': '[16, 20]', 'PULSE_Sol': '[16, 20]', 'BDijkstra_Sol': '[1, 6]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 3.284205, 'NAMOA_Time': 0.195681, 'PULSE_Time': 0.123263, 'BDijkstra_Time': 1.98532, 'MOA_Nodes': 502, 'NAMOA_Nodes': 54, 'PULSE_Nodes': 144, 'BDijkstra_Nodes': 500}

    start = 377
    objectives = [126, 262]
    data = pd.read_csv('big_data_500_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data1000_biobjective():
    return None
    #{'MOA_Sol': '[20, 14]', 'NAMOA_Sol': '[20, 14]', 'PULSE_Sol': '[20, 14]', 'BDijkstra_Sol': '[8, 2]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 8.945706, 'NAMOA_Time': 0.400292, 'PULSE_Time': 0.363292, 'BDijkstra_Time': 4.571932, 'MOA_Nodes': 1001, 'NAMOA_Nodes': 166, 'PULSE_Nodes': 453, 'BDijkstra_Nodes': 1000}

    start = 757
    objectives = [605, 588]
    data = pd.read_csv('big_data_1000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data5000_biobjective():
    return None
    #{'MOA_Sol': '[13, 12]', 'NAMOA_Sol': '[13, 12]', 'PULSE_Sol': '[13, 12]', 'BDijkstra_Sol': '[1, 1]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 312.07237, 'NAMOA_Time': 1.821786, 'PULSE_Time': 0.980798, 'BDijkstra_Time': 22.870614, 'MOA_Nodes': 5002, 'NAMOA_Nodes': 418, 'PULSE_Nodes': 1196, 'BDijkstra_Nodes': 5000}

    start = 1049
    objectives = [3409, 3338]
    data = pd.read_csv('big_data_5000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data10000_biobjective():
    #return None

    start = 1416
    objectives = [2783, 9698]
    data = pd.read_csv('big_data_10000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

# --------------FOUR OBJECTIVE TESTS--------------------------------------


def test_big_data10_multibjective():
    return None
    #{'MOA_Sol': '[12, 15]', 'NAMOA_Sol': '[18, 18]', 'PULSE_Sol': '[12, 15]', 'BDijkstra_Sol': '[4, 6]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 0.058745, 'NAMOA_Time': 0.017127, 'PULSE_Time': 0.13644, 'BDijkstra_Time': 0.038986, 'MOA_Nodes': 12, 'NAMOA_Nodes': 8, 'PULSE_Nodes': 59, 'BDijkstra_Nodes': 10}

    start = 1
    objectives = [0,4,6,7]
    data = pd.read_csv('big_data_10_60%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data50_multibjective():
    return None
    #{'MOA_Sol': '[5, 13]', 'NAMOA_Sol': '[5, 13]', 'PULSE_Sol': '[5, 13]', 'BDijkstra_Sol': '[1, 2]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 0.214769, 'NAMOA_Time': 0.047359, 'PULSE_Time': 0.219971, 'BDijkstra_Time': 0.164997, 'MOA_Nodes': 52, 'NAMOA_Nodes': 30, 'PULSE_Nodes': 189, 'BDijkstra_Nodes': 50}

    start = 10
    objectives = [20, 47, 3, 35]
    data = pd.read_csv('big_data_50_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data100_multibjective():
    return None
    #{'MOA_Sol': '[11, 9]', 'NAMOA_Sol': '[14, 17]', 'PULSE_Sol': '[11, 9]', 'BDijkstra_Sol': '[1, 3]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 0.439988, 'NAMOA_Time': 0.077169, 'PULSE_Time': 0.253934, 'BDijkstra_Time': 0.347185, 'MOA_Nodes': 90, 'NAMOA_Nodes': 49, 'PULSE_Nodes': 235, 'BDijkstra_Nodes': 100}

    start = 2
    objectives = [22, 62, 68, 1]
    data = pd.read_csv('big_data_100_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data500_multibjective():
    return None
    #{'MOA_Sol': '[16, 20]', 'NAMOA_Sol': '[16, 20]', 'PULSE_Sol': '[16, 20]', 'BDijkstra_Sol': '[1, 6]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 3.182511, 'NAMOA_Time': 0.192789, 'PULSE_Time': 0.492187, 'BDijkstra_Time': 1.940192, 'MOA_Nodes': 494, 'NAMOA_Nodes': 54, 'PULSE_Nodes': 490, 'BDijkstra_Nodes': 500}

    start = 377
    objectives = [126, 262, 157, 481]
    data = pd.read_csv('big_data_500_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data1000_multibjective():
    return None
    #{'MOA_Sol': '[20, 14]', 'NAMOA_Sol': '[16, 7]', 'PULSE_Sol': '[16, 7]', 'BDijkstra_Sol': '[8, 2]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 8.785644, 'NAMOA_Time': 0.389638, 'PULSE_Time': 0.773626, 'BDijkstra_Time': 4.53082, 'MOA_Nodes': 998, 'NAMOA_Nodes': 146, 'PULSE_Nodes': 902, 'BDijkstra_Nodes': 1000}

    start = 757
    objectives = [605, 588, 816, 978]
    data = pd.read_csv('big_data_1000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_big_data5000_multibjective():
    return None
    #{'MOA_Sol': '[13, 12]', 'NAMOA_Sol': '[13, 12]', 'PULSE_Sol': '[13, 12]', 'BDijkstra_Sol': '[1, 1]', 'MOA_DOM': True, 'NAMOA_DOM': True, 'PULSE_DOM': True, 'BDijkstra_DOM': False, 'MOA_Time': 314.191052, 'NAMOA_Time': 1.952976, 'PULSE_Time': 1.874154, 'BDijkstra_Time': 22.115835, 'MOA_Nodes': 5002, 'NAMOA_Nodes': 418, 'PULSE_Nodes': 2248, 'BDijkstra_Nodes': 5000}

    start = 1049
    objectives = [3409, 3338, 1035, 4416]
    data = pd.read_csv('big_data_5000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

def test_big_data10000_4vert():
    return None
    # 'MOA_Time': 2461.266393, 'NAMOA_Time': 3.446214, 'PULSE_Time': 4.18555, 'BDijkstra_Time': 90.426541,'MOA_Nodes': 9899, 'NAMOA_Nodes': 346, 'PULSE_Nodes': 2452, 'BDijkstra_Nodes': 9963}

    start = 1416
    objectives = [2783, 6397, 2625, 9698]
    data = pd.read_csv('big_data_10000_30%.csv')
    graph = PandasGraph(data, weight_cols=['weight_1','weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)

# ----------------------------------------------------

def test_G01_2obj():
    tests_path = str(Path(__file__).parent)
    g01_path = os.path.join(tests_path, 'MSPP_data\\grid\\2 objectives\\G01.txt')
    with open(g01_path, 'r') as file:
        data = file.readlines()[1:-2]
        data = [doc.replace('\n', '').split(' ') for doc in data]
        data_df = pd.DataFrame(data=data, columns=['source', 'target', 'weight_1', 'weight_2'])

    start = "1"
    #objectives = [823]
    objectives = ["3"]
    graph = PandasGraph(data_df, weight_cols=['weight_1', 'weight_2'])
    res = tournament(start, objectives, graph, MockedHeuristicAutomatic(graph, objectives[0]))
    print(res)


def test_create_dataset_biobjective():
    return None
    num_vertices = 50
    edge_prob = 30
    new_vertices = [i for i in range(num_vertices)]
    filename = f'big_data_{num_vertices}_{edge_prob}%.csv'

    added_vertices = list()
    data = list()
    while len(new_vertices) > 0:
        rand = random.randint(0, 100)
        if len(new_vertices) == num_vertices:
            source = new_vertices.pop(random.randint(0, len(new_vertices) - 1))
            target = new_vertices.pop(random.randint(0, len(new_vertices) - 1))
        elif rand > edge_prob:  # Create Node
            source = random.choice(added_vertices)
            target = new_vertices.pop(random.randint(0, len(new_vertices) - 1))
        elif rand <= edge_prob:  # Create Edge
            source = random.choice(added_vertices)
            target = None
            while target != source:
                target = random.choice(added_vertices)

        weight_1 = random.randint(1, 10)
        weight_2 = random.randint(1, 10)

        added_vertices.append(source)
        added_vertices.append(target)

        data.append({'source': source, 'target': target, 'weight_1': weight_1, 'weight_2': weight_2})

    data = pd.DataFrame(data)
    data.to_csv(filename, index=False)


def test_create_dataset_multiobjective():
    #return None
    num_vertices = 10000
    edge_prob = 30
    filename = f'big_data_{num_vertices}_{edge_prob}%.csv'
    new_filename = f'big_data_{num_vertices}_{edge_prob}%_multiobjective.csv'
    data = pd.read_csv(filename)

    data['weight_3'] = [random.randint(1, 10) for i in range(len(data))]
    data['weight_4'] = [random.randint(1, 10) for i in range(len(data))]

    data = pd.DataFrame(data)
    data.to_csv(new_filename, index=False)