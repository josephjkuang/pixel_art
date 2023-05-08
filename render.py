from shapely.geometry.polygon import Polygon
import random
import numpy as np
import random
import matplotlib.pyplot as plt

# Render image using random samples of points along edge of regions to get a color estimate
def render_image(curves, width, height, graph):
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim([0.0, width - 1])
    ax.set_ylim([0.0, height - 1])
    ax.invert_yaxis()
    ax.set_aspect('equal')

    # Sort curves by area
    # Bigger areas are more likely to be in the background of image
    areas = []
    for i, vertices in enumerate(curves):
        poly = Polygon([tuple(vertex) for vertex in vertices])
        area = poly.area
        areas.append(area)
    ordering = np.argsort(areas)[::-1]

    # Plot final image
    for i, idx in enumerate(ordering):
        vertices = curves[idx]
        if len(vertices) < 25:
            sample = random.sample(list(vertices), len(vertices))
        else:
            sample = random.sample(list(vertices), 25)
        colors = []
        poly = Polygon([tuple(vertex) for vertex in vertices])
        centroid = list(poly.centroid.coords)[0]
        for point in sample:
            dx = point[0] - centroid[0]
            dy = point[1] - centroid[1]
            estimatedPoint = (round(point[0] - (0.1 * dx)), round(point[1] - (0.1 * dy)))
            colors.append(tuple(graph.nodes[tuple(estimatedPoint)]['color']))
        c = np.median(colors, axis=0)
        ax.fill([vertex[0] for vertex in vertices], [vertex[1] for vertex in vertices], color=(c[2]/255.0, c[1]/255.0, c[0]/255.0))