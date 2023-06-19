class PermutationSignatureApplier:
    """
    Takes in an undirected H graph, directs its edges according to the signature
    """

    def __init__(self, base_h, permutation_signature, undirected_edges):
        self.base_h = base_h
        self.permutation_signature = permutation_signature
        self.undirected_edges = undirected_edges
        self.to_remove = []

    def __enter__(self):
        for (k, v), bit in zip(self.undirected_edges, self.permutation_signature):
            if bit == '0':
                # print(f'{k} {v} {bit}')
                self.base_h.add_arc_by_tag((k, v), weight=1)
                self.to_remove.append((k, v))
            else:
                # print(f'{v} {k} {bit}')
                self.base_h.add_arc_by_tag((v, k), weight=1)
                self.to_remove.append((v, k))

        return self.base_h

    def __exit__(self, exc_type, exc_value, traceback):
        for arc_tags in self.to_remove:
            self.base_h.remove_arc_by_tag(arc_tags)