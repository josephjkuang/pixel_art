import numpy as np
import matplotlib.pyplot as plt

# Using Chaikin's Corner Cutting Algorithm, smooth polygon regions
def smooth_image(segments, width, height):
    def chaikins_corner_cutting(coords, refinements=5):
        coords = np.array(coords)

        for _ in range(refinements):
            L = coords.repeat(2, axis=0)
            R = np.empty_like(L)
            R[0] = L[0]
            R[2::2] = L[1:-1:2]
            R[1:-1:2] = L[2::2]
            R[-1] = L[-1]
            coords = L * 0.75 + R * 0.25

        return coords
    
    smoothed_curved = []
    for segment in segments:
        if (0.0, 0.0) not in segment and (width - 1, height - 1) not in segment and (width - 1, 0) not in segment and (0, height - 1) not in segment:
            smoothed_curved.append(chaikins_corner_cutting(segment))
        else:
            smoothed_curved.append(np.array([[0,0], [width - 1, 0], [width - 1, height - 1], [0, height - 1], [0, 0]]))

    plt.figure()
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal')
    for curve in smoothed_curved:
        xs = curve[:, 0]
        ys = curve[:, 1]
        plt.plot(xs, ys)

    return smoothed_curved