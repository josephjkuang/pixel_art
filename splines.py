import networkx as nx
import numpy as np


def evalBSpline(x1, x2, x3, t):
    return x1 + x2*t + x3 * t**2

# Takes in a list of 3 points


def getSpline(points):
    Base = np.array([[1, 1, 0], [-2, 2, 0], [1, -2, 1]])
    A = np.zeros((3, 2))

    for i in range(3):
        for j in range(2):
            for k in range(3):
                if j == 0:
                    A[i][j] += .5 * Base[i][k] * points[k][0]
                else:
                    A[i][j] += .5 * Base[i][k] * points[k][1]
    splinePointsX = []
    splinePointsY = []
    for t in np.arange(.1, 1.1, .1):
        splinePointsX.append(evalBSpline(A[0][0], A[1][0], A[2][0], t))
        splinePointsY.append(evalBSpline(A[0][1], A[1][1], A[2][1], t))
    return splinePointsX, splinePointsY


def generate_splines(graph):
    components = list(nx.connected_components(graph))

    spline_componentsX = []
    spline_componentsY = []

    for component in components:
        splinesX = []
        splinesY = []
        visited = set()
        component = list(component)
        if len(component) > 2:
            start = None
            line = True
            for point in component:
                if graph.degree(point) == 1:
                    start = point
                    break
            if start == None:
                start = component[0]
                line = False

            traversal = list(nx.dfs_preorder_nodes(
                graph, source=start, depth_limit=2))
            if not line:
                traversal = traversal[:3]
            start = traversal[2]

            for each in traversal:
                visited.add(each)

            while graph.degree(start) != 1 and len(visited) != len(component):
                for each in list(graph.neighbors(start)):
                    if each not in visited:
                        traversal.append(each)
                        visited.add(each)
                for i in range(1, 3):
                    for each in list(graph.neighbors(traversal[i])):
                        if each not in visited:
                            traversal.append(each)
                            visited.add(each)
                start = traversal[-1]
            for i in range(len(traversal) - 2):

                x, y = getSpline(
                    [traversal[i], traversal[i+1], traversal[i+2]])
                splinesX += x
                splinesY += y
            if not line:
                x, y = getSpline([traversal[-2], traversal[-1], traversal[0]])
                splinesX += x
                splinesY += y

                x, y = getSpline([traversal[-1], traversal[0], traversal[1]])
                splinesX += x
                splinesY += y

            spline_componentsX.append(splinesX)
            spline_componentsY.append(splinesY)

    return spline_componentsX, spline_componentsY
