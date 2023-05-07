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
    point_to_color = {node : graph.nodes[node]['color']  for node in graph.nodes()}
    
    for edge in graph.edges():
        midpoint = ((edge[0][0] + edge[1][0]) / 2, (edge[0][1] + edge[1][1]) / 2)
        nodes.append(midpoint)

        point_to_color[midpoint] = graph.nodes[edge[1]]['color']

    return np.array(nodes), point_to_color

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
def get_segments(width, height, vor, point_to_region, point_to_color):    
    # Create the figure base for image
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim([0.0, width - 1])
    ax.set_ylim([0.0, height - 1])
    ax.invert_yaxis()
    ax.set_aspect('equal')

    # Loop through all original input points to get segments
    segments = set()
    for index, point in enumerate(vor.filtered_points):
        # Matching the point to the region
        region = vor.filtered_regions[point_to_region[index]]
        vertices = vor.vertices[region + [region[0]], :]

        # Filling the region with color
        c = tuple(point_to_color[tuple(point)])
        ax.fill([vertex[0] for vertex in vertices], [vertex[1] for vertex in vertices], color=(c[2]/255.0, c[1]/255.0, c[0]/255.0))

        # Get the line segments that aren't just boundary points
        prev_on_boundary = on_boundary(vertices[0], width, height)
        prev_on_boundary = (vertices[0] in vor.filtered_points)
        for i in range(1, len(vertices)):
            curr_on_boundary = on_boundary(vertices[i], width, height)
            curr_on_boundary = (vertices[i] in vor.filtered_points)
            if (not prev_on_boundary) ^ (not curr_on_boundary):
                point1 = (vertices[i - 1][0], vertices[i - 1][1])
                point2 = (vertices[i][0], vertices[i][1])
                if (point2, point1) not in segments:
                    segments.add((point1, point2))
            prev_on_boundary = curr_on_boundary

    segments = np.array([np.array([np.array([x, y]) for x, y in tup]) for tup in segments])    
    return segments
