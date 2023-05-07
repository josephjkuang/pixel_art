import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from similarityGraph import *
import sys
from utils import * 

# Adding the voronoi midpoints and finding associative color for it
def get_voronoi_nodes(graph):
    nodes = [node for node in graph.nodes()]
    point_to_color = {node : graph.nodes[node]['color'] for node in graph.nodes()}
    
    for edge in graph.edges():
        midpoint = ((edge[0][0] + edge[1][0]) / 2, (edge[0][1] + edge[1][1]) / 2)
        nodes.append(midpoint)

        point_to_color[midpoint] = graph.nodes[edge[1]]['color']

    return np.array(nodes), point_to_color

# Add the midpoints to the valence-2 edges
def add_midpoints(graph):
    old_graph = graph.copy()

    for edge in old_graph.edges():
        node1, node2 = edge[0], edge[1]
        midpoint = ((node1[0] + node2[0]) / 2, (node1[1] + node2[1]) / 2)

        graph.add_node(midpoint, color=graph.nodes[node1]['color'], corner=None)
        graph.remove_edges_from((node1, node2))
        graph.add_edge(midpoint, node1)
        graph.add_edge(midpoint, node2)  

    return graph

# Determines if point is inbound
def in_box(points, bounding_box):
    return np.logical_and(np.logical_and(bounding_box[0] <= points[:, 0],
                                         points[:, 0] <= bounding_box[1]),
                          np.logical_and(bounding_box[2] <= points[:, 1],
                                         points[:, 1] <= bounding_box[3]))

# Determines if a point is on the boundary
def on_boundary(point, width, height):
    return point[0] == 0 or point[1] == 0 or point[0] == width or point[1] == height

# Creates the bounded voronoi graph 
def voronoi(points, bounding_box):
    eps = sys.float_info.epsilon

    # Select points inside the bounding box
    i = in_box(points, bounding_box)

    # Mirror the points
    points_center = points[i, :]
    points_left = np.copy(points_center)
    points_left[:, 0] = bounding_box[0] - (points_left[:, 0] - bounding_box[0])
    points_right = np.copy(points_center)
    points_right[:, 0] = bounding_box[1] + (bounding_box[1] - points_right[:, 0])
    points_down = np.copy(points_center)
    points_down[:, 1] = bounding_box[2] - (points_down[:, 1] - bounding_box[2])
    points_up = np.copy(points_center)
    points_up[:, 1] = bounding_box[3] + (bounding_box[3] - points_up[:, 1])
    points = np.append(points_center, np.append(np.append(points_left, points_right, axis=0), np.append(points_down, points_up, axis=0), axis=0), axis=0)
    
    vor = sp.spatial.Voronoi(points) # Compute Voronoi

    # Filter regions
    regions = []
    for region in vor.regions:
        flag = True
        for index in region:
            if index == -1:
                flag = False
                break
            else:
                x, y = vor.vertices[index, 0], vor.vertices[index, 1]
                if not(bounding_box[0] - eps <= x and x <= bounding_box[1] + eps and
                       bounding_box[2] - eps <= y and y <= bounding_box[3] + eps):
                    flag = False
                    break

        if region != [] and flag:
            regions.append(region)

    vor.filtered_points = points_center
    vor.filtered_regions = regions
    return vor

# Find the original input point corresponding to a polygon region
def get_region_point_indices(vor):
    regions = vor.filtered_regions
    points = vor.filtered_points

    pt_to_region = {} # Index of voronoi point to the corresponding index of filtered region

    visited = set()
    for i, pt in enumerate(points):
        point = Point(pt[0], pt[1])
        for j, region in enumerate(regions):
            if j in visited:
                continue

            vertices = vor.vertices[region + [region[0]], :]
            polygon = Polygon([tuple(vertex) for vertex in vertices])

            if polygon.contains(point):
                visited.add(j)
                pt_to_region[i] = j
                break

    return pt_to_region

# Graph the voronoi and find the segments that create the polygons
def graph_voronoi(width, height, vor, graph, point_to_region):    
    # Create the figure base for image
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim([0.0, width - 1])
    ax.set_ylim([0.0, height - 1])
    ax.invert_yaxis()
    ax.set_aspect('equal')

    # Loop through all original input points and filling the region with color
    segments = set()
    for index, point in enumerate(vor.filtered_points):
        # Matching the point to the region
        region = vor.filtered_regions[point_to_region[index]]
        vertices = vor.vertices[region + [region[0]], :]

        # Filling the region with color
        c = tuple(graph.nodes[tuple(point)]['color'])
        ax.fill([vertex[0] for vertex in vertices], [vertex[1] for vertex in vertices], color=(c[2]/255.0, c[1]/255.0, c[0]/255.0))
