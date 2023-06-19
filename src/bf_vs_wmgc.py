import argparse
import time

import numpy as np

import utilities.utilities as utils
from brute.brute import BruteColoringAlgorithm
from parametrized.parametrized_algorithm import ParametrizedColoringAlgorithm
from utilities.generator import GraphGenerator
import pandas as pd

def random_graph(desired_vertex_count=10, desired_arc_count=10, desired_edge_count=1):
    G = GraphGenerator().generate_random_alt(vertex_count=desired_vertex_count, desired_edge_count=desired_edge_count,
                                             desired_arc_count=desired_arc_count)
    utils.add_source_and_sink(G)
    return G


def run_and_measure_brute(G):
    print("Starting brute")
    start_time = time.perf_counter()
    BruteColoringAlgorithm().run(G)
    end_time = time.perf_counter()
    print(f"Brute time: {end_time - start_time};")
    return end_time - start_time


def run_and_measure_parametrized(G):
    print("Starting parametrized")
    start_time = time.perf_counter()
    ParametrizedColoringAlgorithm().run(G)
    end_time = time.perf_counter()
    print(f"Parametrized time: {end_time - start_time};")
    return end_time - start_time


parser = argparse.ArgumentParser(description='Program przeprowadza testy porównawcze BF i WMGC.')

parser.add_argument('--vertex-count',
                    help='Liczba wierzchołków jaką powinny mieć losowe grafy')
parser.add_argument(
    '--number-of-edges',
    type=int,
    default=[1, 2, 1],
    nargs=3,
    help='Liczba krawędzi jaką powinny mieć losowe grafy'
)
parser.add_argument(
    '--number-of-arcs',
    type=int,
    default=[1, 2, 1],
    nargs=3,
    help='Liczba łuków jaką powinny mieć losowe grafy'
)
parser.add_argument('--iterations', dest='iterations',
                    help='Liczba losowych grafów dla każdej kombinacji l. krawędzi i l. łuków')
args = parser.parse_args()

vertex_count = int(args.vertex_count)
arc_count_test_cases = range(args.number_of_arcs[0], args.number_of_arcs[1], args.number_of_arcs[2])
edge_count_test_cases = range(args.number_of_edges[0], args.number_of_edges[1], args.number_of_edges[2])
iterations = int(args.iterations)

vertices = []
edge_tests = []
arc_tests = []

bf_p25 = []
bf_averages = []
bf_p75 = []
bf_p90 = []
bf_p99 = []

wmgc_p25 = []
wmgc_averages = []
wmgc_p75 = []
wmgc_p90 = []
wmgc_p99 = []

for edges in edge_count_test_cases:
    result_dict = dict()
    result_dict_parametrized = dict()

    for arcs in arc_count_test_cases:
        results1 = []
        results2 = []
        for i in range(iterations):
            G = random_graph(desired_vertex_count=vertex_count, desired_arc_count=arcs, desired_edge_count=edges)
            t1 = run_and_measure_brute(G)
            chromatic_brute = G.tags_to_vertices['t'].get_color()
            t2 = run_and_measure_parametrized(G)
            chromatic_para = G.tags_to_vertices['t'].get_color()

            results1.append(t1)
            results2.append(t2)
        vertices.append(vertex_count)
        edge_tests.append(edges)
        arc_tests.append(arcs)
        bf_p25.append(np.percentile(results1, 25))
        bf_averages.append(np.average(results1))
        bf_p75.append(np.percentile(results1, 75))
        bf_p90.append(np.percentile(results1, 90))
        bf_p99.append(np.percentile(results1, 99))

        wmgc_p25.append(np.percentile(results2, 25))
        wmgc_averages.append(np.average(results2))
        wmgc_p75.append(np.percentile(results2, 75))
        wmgc_p90.append(np.percentile(results2, 90))
        wmgc_p99.append(np.percentile(results2, 99))


d = {
    "vertices": vertices,
    "edges": edge_tests,
    "arcs": arc_tests,
    "bf_p25": bf_p25,
    "bf_avg": bf_averages,
    "bf_p75": bf_p75,
    "bf_p90": bf_p90,
    "bf_p99": bf_p99,
    "wmgc_p25": wmgc_p25,
    "wmgc_avg": wmgc_averages,
    "wmgc_p75": wmgc_p75,
    "wmgc_p90": wmgc_p90,
    "wmgc_p99": wmgc_p99,
}

df = pd.DataFrame(d)
print(df.to_csv(index=False, sep='\t'))