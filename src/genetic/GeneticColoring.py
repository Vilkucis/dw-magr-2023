import random

import numpy
import numpy as np
import pygad

from genetic.GeneticConstants import ParentSelectionType, CrossoverType
from graph.algorithms import IsAcyclic, CalculateLongestPaths


class GeneticColoring():
    def __init__(self, graph):
        self.graph = graph
        self.function_inputs = range(0, len(graph.get_vertices()))
        self.desired_output = 4

        self.topological_sort = IsAcyclic(graph).run_dfs()[1]  # TODO keep in Graph, make it lazy?
        self.distances = CalculateLongestPaths().run(self.topological_sort)
        self.upper_bound = self.distances[('s', 't')] + len(self.graph.vertex_tuples_to_edges)
        # print(f"Upper bound: {self.upper_bound}")

        self.population_health = []
        self.mean_fitness = 0
        self.previous_best_solution = None

    def on_generation_func(self, ga_instance):
        unique_rows = numpy.unique(ga_instance.population, axis=0)
        self.population_health.append(unique_rows.shape[0])

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

    def fitness_func3(self, ga_instance, solution, solution_idx):
        """
        The fitness function is equal to:
        - number of bad colorings, negated - if the coloring is incorrect
        - `1/chromatic number of solution` - if the coloring is correct
        """
        for color, vertex in zip(solution, self.topological_sort):
            vertex.set_color(color)
        number_of_bad_colorings = 0
        for vertex in self.topological_sort:
            for arc in vertex.get_outgoing_directed_edges():
                if arc.from_vertex.get_color() >= arc.to_vertex.get_color():
                    number_of_bad_colorings += 1
        for k, v in self.graph.vertex_tuples_to_edges.items():
            if v.from_vertex.get_color() == v.to_vertex.get_color():
                number_of_bad_colorings += 1
                pass

        if number_of_bad_colorings == 0:
            return 1 / self.graph.tags_to_vertices['t'].get_color()
        else:
            return 0 - number_of_bad_colorings

    def is_coloring_correct(self, vertex):
        is_coloring_correct = True
        for incoming_arc in vertex.get_incoming_directed_edges():
            if incoming_arc.from_vertex.get_color() >= vertex.get_color():
                is_coloring_correct = False
        # for outgoing_arc in vertex.get_outgoing_directed_edges():
        #     if outgoing_arc.from_vertex.get_color() <= vertex.get_color():
        #         is_coloring_correct = False
        for edge in vertex.get_undirected_edges():
            if edge.from_vertex.get_color() == edge.to_vertex.get_color():
                is_coloring_correct = False

        return is_coloring_correct

    def available_colors_for_vertex(self, vertex):
        """
        :param vertex:
        :return: a list of eligible colors for vertex in ascending order
        """
        available_colors = set(range(0, self.upper_bound))
        unavailable_colors = set()

        lower_bound = 0
        upper_bound = self.upper_bound

        for incoming_arc in vertex.get_incoming_directed_edges():
            if incoming_arc.from_vertex.get_color() > lower_bound:
                lower_bound = incoming_arc.from_vertex.get_color()
        for outgoing_arc in vertex.get_outgoing_directed_edges():
            if outgoing_arc.to_vertex.get_color() < upper_bound:
                upper_bound = outgoing_arc.to_vertex.get_color()
        for edge in vertex.get_undirected_edges():
            if edge.from_vertex == vertex:
                unavailable_colors.add(edge.to_vertex.get_color())
            else:
                unavailable_colors.add(edge.from_vertex.get_color())

        upper_bound -= 1
        lower_bound += 1

        if upper_bound <= lower_bound:
            return list()

        available_colors = set(range(lower_bound, upper_bound))
        diff = available_colors.difference(unavailable_colors)

        if not diff:
            return [upper_bound]

        return sorted(list(diff))

    def mutation_func7(self, offspring, ga_instance):
        for chromosome in offspring[0:]:
            if random.random() < ga_instance.mutation_probability:
                for chromosome_index, vertex in zip(range(0, len(chromosome)), self.topological_sort):
                    vertex.set_color(chromosome[chromosome_index])

                for from_vertex, to_vertex in self.graph.vertex_tuples_to_edges.values():
                    if not self.is_coloring_correct(from_vertex):
                        candidates = self.available_colors_for_vertex(from_vertex)
                        new_color = random.choice(candidates[:2])
                        from_vertex.set_color(new_color)
                        chromosome[self.topological_sort.index(from_vertex)] = new_color
                    if not self.is_coloring_correct(to_vertex):
                        candidates = self.available_colors_for_vertex(to_vertex)
                        new_color = random.choice(candidates[:2])
                        to_vertex.set_color(new_color)
                        chromosome[self.topological_sort.index(to_vertex)] = new_color

                for vertex in self.topological_sort:
                    if not self.is_coloring_correct(vertex):
                        candidates = self.available_colors_for_vertex(vertex)
                        new_color = random.choice(candidates[:2])
                        vertex.set_color(new_color)
                        chromosome[self.topological_sort.index(vertex)] = new_color

        return offspring

    def lower_bound(self, vertex):
        """
        :param vertex:
        :return: a list of eligible colors for vertex in ascending order
        """

        lower_bound = 0

        for incoming_arc in vertex.get_incoming_directed_edges():
            if incoming_arc.from_vertex.get_color() > lower_bound:
                lower_bound = incoming_arc.from_vertex.get_color()

        return lower_bound

    def mutation_func8(self, offspring, ga_instance):
        """
        for each vertex
            if adjacent to an edge, colors it with a random color selected from a list of viable colors sorted ascending,
            otherwise colors it with a color 1 bigger than the maximum color of a neighbour from an incoming arc
        """
        for chromosome in offspring:
            fitness = self.fitness_func3(None, chromosome, None)
            mutation_probability = 0.7
            if fitness > self.mean_fitness:
                mutation_probability = 0.01

            if random.random() < mutation_probability:
                for chromosome_index, vertex in zip(range(0, len(chromosome)), self.topological_sort):
                    vertex.set_color(chromosome[chromosome_index])

                for vertex in self.topological_sort[1:]:
                    candidates = self.available_colors_for_vertex(vertex)
                    lower_bound = self.lower_bound(vertex)
                    if not candidates:
                        new_color = lower_bound + 1
                        vertex.set_color(new_color)
                        chromosome[self.topological_sort.index(vertex)] = new_color
                        continue
                    if not vertex.get_undirected_edges():
                        new_color = lower_bound + 1
                        vertex.set_color(new_color)
                        chromosome[self.topological_sort.index(vertex)] = new_color
                    else:
                        new_color = random.choice(candidates[:10])
                        vertex.set_color(new_color)
                        chromosome[self.topological_sort.index(vertex)] = new_color

        return offspring

    def run(self, crossover_type, parent_selection_type, mutation_probability):

        fitness_function = self.fitness_func3

        num_generations = 1000
        num_parents_mating = 30

        sol_per_pop = 30
        num_genes = len(self.function_inputs)

        init_range_low = 0
        init_range_high = self.upper_bound

        mutation_type = self.mutation_func8

        gene_space = [[0]]
        ap = list(range(1, self.upper_bound))
        for i in range(1, len(self.function_inputs)):
            gene_space.append(ap)

        ga_instance = pygad.GA(num_generations=num_generations,
                               num_parents_mating=num_parents_mating,
                               fitness_func=fitness_function,
                               sol_per_pop=sol_per_pop,
                               num_genes=num_genes,
                               keep_elitism=4,
                               init_range_low=init_range_low,
                               init_range_high=init_range_high,
                               parent_selection_type=ParentSelectionType.TOURNAMENT.name,
                               crossover_type=CrossoverType.SINGLE_POINT.name,
                               mutation_type=mutation_type,
                               mutation_probability=0.7,
                               gene_type=int,
                               gene_space=gene_space,
                               on_generation=self.on_generation_func,
                               on_fitness=self.on_fitness)

        ga_instance.run()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()
        print(f"Parameters of the best solution : {solution}")
        print(f"Fitness value of the best solution = {solution_fitness}")

        # ga_instance.plot_result()
        #
        # fig, ax = plt.subplots()
        # ax.plot(self.population_health)
        # plt.show()
        #
        # fig, ax = plt.subplots()
        # ax.plot(ga_instance.best_solutions_fitness[1:])
        # plt.show()

        print(f"GeneticColoring solutions: {ga_instance.best_solutions_fitness}")

        self.fitness_func3(None, solution, None)
        max_color = self.graph.tags_to_vertices['t'].get_color()
        print(f"Max color: {max_color}")

        return len(numpy.unique(solution))
        # utils.draw(self.graph, colors_as_labels=True)
