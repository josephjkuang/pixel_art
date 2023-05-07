import cv2
import networkx as nx
import numpy as np

# Milestone 1: Reshaping the pixels using the heuristics to make sure that they are grouped with their neighbors
def create_similarity_graph(image):
    # Create a similarity graph from the input image using heuristics to group similar pixels together.
    graph = nx.Graph()
    height, width, _ = image.shape

    for y1 in range(height):
        for x1 in range(width):
            # Adding the nodes to the graph
            corners = [(x1, y1), (x1 + 1, y1), (x1, y1 + 1), (x1 + 1, y1 + 1)]
            color = image[y1][x1]
            graph.add_node((x1, y1), color=image[y1][x1], corners=corners)

            # Adding the neighbor nodes (8 / 2 = 4 neighbors to ignore repeats)
            neighbors = [(x1 + 1, y1), (x1, y1 + 1) , (x1 + 1, y1 + 1), (x1 + 1, y1 - 1)]
            for neighbor in neighbors:
                x2, y2 = neighbor
                if x2 < width and y2 < height and y2 >= 0 and color_equals(image, x1, y1, x2, y2):
                    # Only add neighbors that are in the same color range
                    graph.add_edge((x1, y1), (x2, y2))  

    return graph

# Check if the pixels are in equality range according to the Kopf-Lischinski algorithm 
def color_equals(image, x1, y1, x2, y2):
    yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    y, u, v = cv2.split(yuv.astype(np.int16))

    if 48.0 < abs(y[y1, x1] - y[y2, x2]):
        return False
    if 7.0 < abs(u[y1, x1] - u[y2, x2]):
        return False
    if 6.0 < abs(v[y1, x1] - v[y2, x2]):
        return False
    return True

# Remove diagonals if the square is fully connected
def remove_diagonals(graph, image): 
    height, width, _ = image.shape

    edges_to_remove = []
    for y in range(height - 1):
        for x in range(width - 1):
            corners = graph.nodes[(x, y)]['corners']
            connections = 0
            for i, node1 in enumerate(corners):
                for j, node2 in enumerate(corners[i + 1:]):
                    if graph.has_edge(node1, node2):
                        connections += 1

            if connections == 6:
                edges_to_remove.append(((x, y), (x + 1, y + 1)))
                edges_to_remove.append(((x + 1, y), (x, y + 1)))
            elif connections == 2 and graph.has_edge((x, y), (x + 1, y + 1)) and graph.has_edge(( x+ 1, y), (x, y + 1)):
                remove_diagonal_gestalt((x, y), graph)

    graph.remove_edges_from(edges_to_remove)
    return graph

# Remove a single diagonal if the square contains only diagonal connections
def remove_diagonal_gestalt(node, graph):
    # Weights for diagonals where weights[0] is the weight for (x, y) -> (x + 1, y + 1)
    # and weights[1] is the weight for (x + 1, y) -> (x, y + 1)
    x, y = node
    weights = np.array([0, 0])
    weights += getCurvesScore(node, graph)
    weights += getSparsePixelsScore(node, graph)
    weights += getIslandsScore(node, graph)

    if weights[0] > weights[1]:
        graph.remove_edge((x + 1, y), (x, y + 1))
    elif weights[0] < weights[1]:
        graph.remove_edge((x, y), (x + 1, y + 1))
    else:
        graph.remove_edges_from([((x, y), (x + 1, y + 1)), ((x + 1, y), (x, y + 1))])

def getCurvesScore(node, graph):
    x, y = node
    return np.array([findCurveLength((x, y), (x + 1, y + 1),  graph),\
                     findCurveLength((x + 1, y), (x - 1, y + 1), graph)])

def findCurveLength(node1, node2, graph):
    current = None
    queue = [node1]
    visited = set()
    count = 0

    # check for base case where both nodes have valence != 2
    node1Valence = graph.degree(node1)
    node2Valence = graph.degree(node2)

    if node1Valence != 2 and node2Valence != 2:
        return 1
    
    while len(queue) != 0:
        current = queue.pop(0)
        cur_edges = graph.edges(current)

        visited.add(current)

        for edge in cur_edges:
            neighbor = edge[1]
            neighbor_edges = graph.edges(neighbor)

            if len(neighbor_edges) == 2 and neighbor not in visited:
                queue.append(neighbor)
                count += 1
            elif len(neighbor_edges) == 1:
                count += 1

    return count

def getSparsePixelsScore(node, graph):
    x, y = node
    component1 = nx.ego_graph(graph, node, radius = 4).nodes()
    component2 = nx.ego_graph(graph, (x + 1, y), radius = 4).nodes()

    return np.array([len(component2), len(component1)])

def getIslandsScore(node, graph):
    x, y = node
    weight = np.array([0, 0])

    if len(graph.edges((x, y))) == 1 or len(graph.edges((x + 1, y + 1))) == 1:
        weight[0] += 5
    if len(graph.edges((x + 1, y))) == 1 or len(graph.edges((x, y + 1))) == 1:
        weight[1] += 5

    return weight
