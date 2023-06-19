import argparse
import time

import numpy as np

from genetic.GeneticColoring import GeneticColoring, CrossoverType, ParentSelectionType
from genetic.GeneticJobShop import GeneticJobShop

from utilities.generator import GraphGenerator
import utilities.utilities as utils
import pandas as pd

def random_job(number_of_jobs = 2, number_of_machines=100):
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

def run_and_measure_genetic_job_shop(G):
    print("Starting job shop")
    start_time = time.perf_counter()
    GeneticJobShop(G).run()
    end_time = time.perf_counter()
    print(f"Genetic job shop time: {end_time - start_time};")
    return end_time - start_time

parser = argparse.ArgumentParser(description='Program przeprowadza testy porównawcze GC i GJS.')
parser.add_argument(
    '--number-of-machines',
    type=int,
    default=[2, 3, 1],
    nargs=3,
    help='Liczba maszyn jaką będą miały wygenerowane instancje problemu szeregowania zadań'
)
parser.add_argument(
    '--number-of-jobs',
    type=int,
    default=[2, 3, 1],
    nargs=3,
    help='Liczba zadań jaką będą miały wygenerowane instancje problemu szeregowania zadań'
)
parser.add_argument('--iterations', dest='iterations',
                    help='Liczba losowych grafów do przetestowania dla każdej kombinacji l. zadań i l. maszyn')
args = parser.parse_args()

if args.number_of_jobs[0] < 2:
    raise Exception("Number of jobs must be > 1")
if args.number_of_machines[0] < 2:
    raise Exception("Number of machines must be > 1")

jobs_test_cases = range(args.number_of_jobs[0], args.number_of_jobs[1], args.number_of_jobs[2])
machines_test_cases = range(args.number_of_machines[0], args.number_of_machines[1], args.number_of_machines[2])

job_tests = []
op_tests = []
gc_avg_times = []
gc_average_color = []
js_avg_times = []
js_average_color = []

for jobs in jobs_test_cases:
    for machines in machines_test_cases:
        gc_times = []
        gc_colors = []
        js_times = []
        js_colors = []
        for i in range(int(args.iterations)):
            G = random_job(number_of_jobs=jobs, number_of_machines=machines)
            t1 = run_and_measure_genetic_job_shop(G)
            gjs_chromatin_n = G.tags_to_vertices['t'].get_color()

            t2 = run_and_measure_genetic_coloring(G)
            gc_chromatic_n = G.tags_to_vertices['t'].get_color()

            gc_times.append(t2)
            gc_colors.append(gc_chromatic_n)
            js_times.append(t1)
            js_colors.append(gjs_chromatin_n)

        job_tests.append(jobs)
        op_tests.append(machines)
        gc_avg_times.append(np.average(gc_times))
        gc_average_color.append(np.average(gc_colors))
        js_avg_times.append(np.average(js_times))
        js_average_color.append(np.average(js_colors))

d = {
    "jobs": job_tests,
    "machines": op_tests,
    "gc_avg_time": gc_avg_times,
    "gc_avg_color": gc_average_color,
    "js_avg_times": js_avg_times,
    "js_avg_color": js_average_color
}

df = pd.DataFrame(d)
print(df.to_csv(index=False, sep='\t'))

