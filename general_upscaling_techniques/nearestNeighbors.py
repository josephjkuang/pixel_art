import numpy as np
import math
import cv2

def nearestNeighborsInterpolation(image, scale):
    # Upscaling only
    if scale < 1:
        return image
    
    # Init variables
    H, W, C = image.shape
    scaledH = math.floor(H * scale)
    scaledW = math.floor(W * scale)
    outputImage = np.zeros((scaledH, scaledW, C), dtype=np.uint8)
    invScale = 1 / scale

    # Fill output image
    for i in range(scaledH):
        for j in range(scaledW):
            for k in range(C):
                x = math.floor(j * invScale)
                y = math.floor(i * invScale)
                interpolatedPixel = image[y, x, k]
                outputImage[i, j, k] = interpolatedPixel
    
    return outputImage 


mario = cv2.imread('../inputs/mario.png')
upscaledMario = nearestNeighborsInterpolation(mario, 5)
cv2.imwrite('./nearestNeighborsMario.png', upscaledMario)