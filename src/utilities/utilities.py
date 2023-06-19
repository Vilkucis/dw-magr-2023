import networkx
from matplotlib import pyplot as plt


def draw(old_graph, colors_as_labels=False, draw_weights=False):
    graph = networkx.DiGraph()

    for vertex in old_graph.get_vertices():
        # TODO add undirected edges
        for edge in vertex.get_outgoing_directed_edges():
            from_edge, to_edge = edge
            graph.add_edge(from_edge.get_tag(), to_edge.get_tag(), color="r", weight=edge.get_weight())

    for from_edge, to_edge in old_graph.get_undirected_edges():
        graph.add_edge(from_edge.get_tag(), to_edge.get_tag(), color='b', weight=1)

    color_map = []
    for vertex in graph:
        old_vertex = old_graph.get_tags_to_vertices()[vertex]
        color = old_vertex.get_color() if old_vertex.get_color() else -1
        color_map.append(color)

    colors = networkx.get_edge_attributes(graph, 'color').values()
    edge_labels = networkx.get_edge_attributes(graph, "weight")

    labels = dict()
    for node in graph.nodes:
        if colors_as_labels:
            labels[node] = old_graph.get_tags_to_vertices()[node].get_color()
        else:
            labels[node] = node

    # pos = networkx.drawing.nx_pydot.graphviz_layout(graph, prog="dot")
    pos = networkx.circular_layout(sorted(graph))
    networkx.draw(graph, pos, labels=labels, node_color=color_map, with_labels=True, edge_color=colors)
    if draw_weights:
        networkx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()


def add_source_and_sink(graph):
    graph.add_vertex_by_tag("s")
    graph.add_vertex_by_tag("t")
    for vertex in graph.get_vertices():
        if vertex.get_tag() != "s" and vertex.get_tag() != "t":
            graph.add_arc_by_tag(("s", vertex.get_tag()))
            graph.add_arc_by_tag((vertex.get_tag(), "t"))


def add_scheduling_source_and_sink(graph, operations_per_job):
    graph.add_vertex_by_tag("s").set_color(0)
    graph.add_vertex_by_tag("t")

    first_op = []
    last_op = []

    for job, ops in graph.get_job_dict().items():
        first_op.append(ops[0])
        for op in ops:
            if not op.get_outgoing_directed_edges():
                last_op.append(op)

    for first, last in zip(first_op, last_op):
        graph.add_arc_by_tag(("s", first.get_tag()))
        graph.add_arc_by_tag((last.get_tag(), "t"))

    return None
