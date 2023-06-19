import random
import time

import numpy
import numpy as np
import pygad

from genetic.GeneticConstants import ParentSelectionType


class GeneticJobShop:
    def __init__(self, graph):
        self.graph = graph
        self.function_inputs = range(0, len(graph.get_vertices()))

        self.number_of_jobs = graph.get_number_of_jobs()
        self.operations_per_job = graph.get_number_of_operations_per_job()
        self.gene_lower_bound = 0
        self.gene_upper_bound = self.number_of_jobs - 1

        self.mean_fitness = 0

    def on_generation_func(self, ga_instance):
        # unique_rows = numpy.unique(ga_instance.population, axis=0)
        # self.population_health.append(unique_rows.shape[0])

        stop = False
        # print(f"\rGenerations completed {ga_instance.generations_completed}", end='')
        # print()
        if len(ga_instance.best_solutions_fitness) > 10:
            stop = True
            ten_last = ga_instance.best_solutions_fitness[-10:]
            for previous, current in zip(ten_last, ten_last[1:]):
                if previous != current:
                    stop = False
                    break

        if stop:
            print("Stop condition reached")
            return "stop"

    def on_fitness(self, ga_instance, population_fitness):
        self.mean_fitness = np.mean(population_fitness)

    def place_at_free_slot(self, time_row, operation):
        later_than = 0
        if operation.get_incoming_directed_edges():
            previous_operation = operation.get_incoming_directed_edges()[0]
            if previous_operation.get_tag() != 's':
                later_than = previous_operation.get_color()

        if not time_row:
            time_row.append(operation)
            return

        # only one taken timeslot, so we can place either before or after
        if len(time_row) == 1:
            existing_operation = time_row[0]
            time_slot = existing_operation.get_color()

            if time_slot >= 2 and later_than < time_slot:
                time_slot.insert(0, operation)
            else:
                time_row.append(operation)

        for current, next in zip(time_row, time_row[1:]):
            if current.get_color() == next.get_color() - 1:  # no free slot
                continue
            if current.get_color() <= later_than:  # place after this element
                idx = time_row.index(current)
                time_row.insert(idx + 1, operation)
                return

        time_row.append(operation)
        return

    def fitness_func2(self, ga_instance, solution, solution_idx):
        # initialize empty timetable
        timetable = []
        for i in range(self.graph.get_number_of_machines()):
            timetable.append([])

        # job iterators
        jobs = [item[0] for item in self.graph.get_job_dict().values()]

        for gene in solution:
            current_operation = jobs[int(gene)]
            desired_machine = current_operation.get_assigned_machine()
            timetable_row = timetable[int(desired_machine)]

            self.place_at_free_slot(timetable_row, current_operation)

            if current_operation.get_outgoing_directed_edges():
                jobs[int(gene)] = current_operation.get_outgoing_directed_edges()[0]

    def find_next_free_index(self, list, later_than=0):
        if not list:
            return later_than

        if later_than < list[0].get_color():
            return later_than
        if len(list) is 1:
            if list[0].get_color() != later_than:
                return later_than
            else:
                return later_than + 1
        if later_than > list[-1].get_color():
            return later_than
        free_index = later_than
        for previous, current in zip(list, list[1:]):
            if previous.get_color() < free_index and current.get_color() > free_index:
                return free_index
            else:
                free_index = current.get_color() + 1

        return max(free_index, later_than)

    def find_op_at_timeslot(self, list, slot):
        """
        Find element in [slot, slot+1]
        :param list:
        :param slot:
        :return:
        """
        for el in list:
            if el.get_color() == slot:
                return el

        return None

    def has_conflicts(self, operation, timetable, index):
        conflicting_nodes = []
        for row in timetable:
            conflicting_op = self.find_op_at_timeslot(row, index)
            if conflicting_op and conflicting_op is not operation:
                conflicting_nodes.append(self.find_op_at_timeslot(row, index))

        for op2 in conflicting_nodes:
            if self.graph.are_connected_by_an_edge(operation.get_tag(), op2.get_tag()):
                return True

        return False

    def fitness_func2(self, ga_instance, solution, solution_idx):
        # TODO reset colors

        timetable = []
        for i in range(self.graph.get_number_of_machines()):
            timetable.append([])

        job_iterators = dict()
        for key, jobs in self.graph.get_job_dict().items():
            job_iterators[key] = iter(jobs)

        for gene in solution:
            job_tag = str(gene)
            operation = next(job_iterators[job_tag])
            desired_machine = int(operation.get_assigned_machine())

            potential_index = 0
            while True:
                incoming = operation.get_incoming_directed_edges()
                prev_op_index = -1
                if incoming:
                    prev_op_index = incoming[0].from_vertex.get_color() + 1
                minimum_index = max(potential_index, prev_op_index)

                while True:
                    potential_index = self.find_next_free_index(timetable[int(desired_machine)],
                                                                later_than=minimum_index)
                    if not self.has_conflicts(operation, timetable, potential_index):
                        operation.set_color(potential_index)
                        timetable[int(desired_machine)].insert(potential_index, operation)
                        break
                    minimum_index += 1
                break

        makespan = -1
        for row in timetable:
            if row[-1].get_color() + 1 > makespan:
                makespan = row[-1].get_color() + 1
        # print(solution)
        return 1 / makespan

    def crossover_func(self, parents, offspring_size, ga_instance):
        offspring = []
        idx = 0
        while len(offspring) != offspring_size[0]:
            parent1 = parents[idx % parents.shape[0], :].copy()
            parent2 = parents[(idx + 1) % parents.shape[0], :].copy()

            job_pool = range(self.gene_lower_bound, self.gene_upper_bound)
            random_sample_number = random.randint(1, self.number_of_jobs - 1)
            subset = random.sample(job_pool, random_sample_number)

            parent2_index = 0
            for gene in range(len(parent1)):
                if parent1[gene] not in subset:
                    while parent2_index < len(parent1) and parent2[parent2_index] in subset:
                        parent2_index += 1
                    parent1[gene] = parent2[parent2_index]
                    parent2_index += 1

            offspring.append(parent1)

            idx += 1

        return numpy.array(offspring)

    def mutation_func7(self, offspring, ga_instance):
        for chromosome in offspring:
            fitness = self.fitness_func2(None, chromosome, None)
            mutation_probability = 0.7
            if fitness > self.mean_fitness:
                mutation_probability = 0.01

            if random.random() < mutation_probability:
                ix1, ix2 = random.sample(range(1, len(chromosome)), 2)
                chromosome[[ix1, ix2]] = chromosome[[ix2, ix1]]
        return offspring

    def run(self):
        num_generations = 100
        num_parents_mating = 30

        sol_per_pop = 30
        num_genes = self.number_of_jobs

        chromosome_template = []
        for i in range(0, self.number_of_jobs):
            chromosome_template += ([i] * self.operations_per_job)

        start = time.perf_counter()
        initial_population = []
        for i in range(0, sol_per_pop):
            new_chromosome = chromosome_template.copy()
            random.shuffle(new_chromosome)
            initial_population.append(new_chromosome)
        print(f"Random population generated in: {time.perf_counter() - start}")

        ga_instance = pygad.GA(num_generations=num_generations,
                               num_parents_mating=num_parents_mating,
                               fitness_func=self.fitness_func2,
                               sol_per_pop=sol_per_pop,
                               num_genes=num_genes,
                               parent_selection_type=ParentSelectionType.TOURNAMENT.name,
                               keep_elitism=4,
                               crossover_type=self.crossover_func,
                               mutation_type=self.mutation_func7,
                               mutation_probability=0.0,
                               gene_type=int,
                               initial_population=initial_population,
                               on_generation=self.on_generation_func)

        ga_instance.run()

        # print(f"Upper bound: {self.upper_bound}")

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        print(f"Parameters of the best solution : {solution}")
        print(f"Fitness value of the best solution = {solution_fitness}")

        self.fitness_func2(None, solution, None)
        for from_vertex, to_vertex in self.graph.tags_to_vertices['t'].get_incoming_directed_edges():
            if not to_vertex.get_color():
                to_vertex.set_color(from_vertex.get_color() + 1)
            elif from_vertex.get_color() + 1 > to_vertex.get_color():
                to_vertex.set_color(from_vertex.get_color() + 1)

        max_color = self.graph.tags_to_vertices['t'].get_color()
        print(f"Max color: {max_color}")

        # fig, ax = plt.subplots()
        # ax.plot(ga_instance.best_solutions_fitness[1:])
        # plt.show()
        print(f"GeneticJobShop solutions: {ga_instance.best_solutions_fitness}")

        # ga_instance.plot_result()
        # ga_instance.plot_new_solution_rate()

        # utils.draw(self.graph, colors_as_labels=True)
