class WeighedColoring():

    def run(self, sorted_graph):
        for vertex in sorted_graph:
            max_color = 0
            parent_edges = vertex.get_incoming_directed_edges()
            if parent_edges:
                for incoming in vertex.get_incoming_directed_edges():
                    incoming_color = incoming.get_from_vertex().get_color()

                    if incoming_color is not None and incoming_color + incoming.get_weight() > max_color:
                        max_color = incoming_color + incoming.get_weight()
                    vertex.set_color(max_color)
            else:
                vertex.set_color(0)