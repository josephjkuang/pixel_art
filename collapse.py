from shapely.geometry.polygon import Polygon
from shapely.ops import unary_union
from similarityGraph import *
import matplotlib.pyplot as plt
import networkx as nx

def union_same_color_regions(graph, vor, point_to_region):
    point_to_index = {tuple(point) : i for i, point in enumerate(vor.filtered_points)}

    components = nx.connected_components(graph)
    color_regions = []

    for component in components:
        polygons = []
        for point in component:
            vertices = np.array(vor.vertices[vor.filtered_regions[point_to_region[point_to_index[tuple(point)]]]])
            vertices = np.where(vertices < 0, 0, vertices)
            
            polygon = Polygon([tuple(vertex) for vertex in vertices])
            polygons.append(polygon)
            
        color_regions.append(unary_union(polygons))

    return color_regions

def reduce_line_segments(vertices):
    new_vertices = vertices.copy()
    removals = 0

    for i in range(len(vertices) - 3):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]
        x3, y3 = vertices[i + 2]
        slope1 = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')
        slope2 = (y3 - y2) / (x3 - x2) if (x3 - x2) != 0 else float('inf')
        if slope1 == slope2:
            new_vertices.remove(new_vertices[i + 1 - removals])
            removals += 1
    
    return new_vertices

def get_collapsed_segments(graph, vor, point_to_region, width, height):
    color_regions = union_same_color_regions(graph, vor, point_to_region)

    # Create the figure base for image
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim([0.0, width - 1])
    ax.set_ylim([0.0, height - 1])
    ax.invert_yaxis()
    ax.set_aspect('equal')

    segments = []
    for vertices in color_regions:
        vertices = list(vertices.exterior.coords)
        vertices = reduce_line_segments(vertices)
        segments.append(vertices)

        ax.fill([vertex[0] for vertex in vertices], [vertex[1] for vertex in vertices])

    return segments
