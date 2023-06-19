import argparse
import time

import numpy as np
import pandas as pd

import utilities.utilities as utils
from genetic.GeneticColoring import GeneticColoring, CrossoverType, ParentSelectionType
from parametrized.parametrized_algorithm import ParametrizedColoringAlgorithm
from utilities.generator import GraphGenerator


def random_job(number_of_jobs=2, number_of_machines=100):
    G = GraphGenerator().generate_scheduling_problem(number_of_jobs=number_of_jobs,
                                                     number_of_operations_per_job=number_of_machines,
                                                     number_of_machines=number_of_machines)
    utils.add_scheduling_source_and_sink(G, number_of_machines)
    return G


def run_and_measure_genetic_coloring(G):
    print("Starting genetic coloring")
    start_time = time.perf_counter()
    GeneticColoring(G).run(CrossoverType.TWO_POINTS.name, ParentSelectionType.RANK.name, 0.2)
    end_time = time.perf_counter()
    print(f"Genetic coloring time: {end_time - start_time};")
    return end_time - start_time


def run_and_measure_parametrized(G):
    print("Starting parametrized")
    start_time = time.perf_counter()
    ParametrizedColoringAlgorithm().run(G)
    end_time = time.perf_counter()
    print(f"Parametrized time: {end_time - start_time};")
    return end_time - start_time


parser = argparse.ArgumentParser(description='Program przeprowadza testy porównawcze WMGC i GC.')
parser.add_argument(
    '--number-of-machines',
    type=int,
    default=[1, 2, 1],
    nargs=3,
    help='Liczba maszyn jaką będą miały wygenerowane instancje problemu szeregowania zadań'
)
parser.add_argument('--iterations', dest='iterations',
                    help='Liczba losowych grafów do przetestowania dla każdej l. maszyn')
args = parser.parse_args()


genetic_times = []
wmgc_times = []
js_color = []
genetic_color = []

res_dict = {}

test_cases = range(args.number_of_machines[0], args.number_of_machines[1], args.number_of_machines[2])

res_dict = {"ops_per_job": test_cases}
gc_avg_times = []
gc_mean_color = []
wmgc_avg_times = []
wmgc_mean_color = []
max_errors = []
error_percentage = []
for case in test_cases:

    gc_times = []
    gc_colors = []
    wmgc_times = []
    wmgc_colors = []
    error_inner = []
    for i in range(int(args.iterations)):
        print(f"Test case {case}, it {i}")
        G = random_job(number_of_jobs=3, number_of_machines=case)
        wmgc_time = run_and_measure_parametrized(G)
        wmgc_chromatic_num = G.tags_to_vertices['t'].get_color()

        gc_time = run_and_measure_genetic_coloring(G)
        gc_chromatic_num = G.tags_to_vertices['t'].get_color()

        gc_times.append(gc_time)
        gc_colors.append(gc_chromatic_num)
        wmgc_times.append(wmgc_time)
        wmgc_colors.append(wmgc_chromatic_num)
        error_inner.append(gc_chromatic_num - wmgc_chromatic_num)

    gc_avg_times.append(np.average(gc_times))
    gc_mean_color.append(np.average(gc_colors))
    wmgc_avg_times.append(np.average(wmgc_times))
    wmgc_mean_color.append(np.average(wmgc_colors))
    max_errors.append(np.max(error_inner))
    error_percentage.append(np.count_nonzero(error_inner) / len(error_inner))

res_dict["gc_avg_time"] = gc_avg_times
res_dict["wmgc_avg_times"] = wmgc_avg_times
res_dict["max_error"] = max_errors
res_dict["error_percentage"] = error_percentage
df = pd.DataFrame(res_dict)
print(df.to_csv(index=False, sep='\t'))
