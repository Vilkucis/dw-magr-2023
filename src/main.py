import argparse

parser = argparse.ArgumentParser(description='Test description.')

parser.add_argument('--vertex-count', dest='vertex_count',
                    help='The number of vertices the random graphs should have')
parser.add_argument('--arc-count', dest='arc_count',
                    help='The number of arcs the random graphs should have')
parser.add_argument('--edge-count', dest='edge_count',
                    help='The number of edges the random graphs should have')
parser.add_argument('--iterations', dest='iterations',
                    help='The number of iterations to perform')
parser.add_argument(
    '--degree',
    type=int,
    default=[1, 2, 1],
    nargs=3,
)

args = parser.parse_args()
print(args.degree)