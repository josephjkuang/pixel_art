import numpy as np
import math
import cv2

def bilinearInterpolation(image, scale):
    # Upscaling only
    if scale < 1:
        return image
    
    # Init variables
    H, W, C = image.shape
    scaledH = math.floor(H * scale)
    scaledW = math.floor(W * scale)
    outputImage = np.zeros((scaledH, scaledW, C), dtype=np.uint8)
    invScale = 1 / scale
    paddedImage = cv2.copyMakeBorder(image, 1, 1, 1, 1, borderType=cv2.BORDER_REPLICATE)

    # Fill output image
    for i in range(scaledH):
        for j in range(scaledW):
            for k in range(C):
                x = j * invScale
                y = i * invScale
                # Find four nearest points
                p1 = (math.floor(x - 1), math.floor(y))
                p2 = (math.floor(x + 1), math.floor(y))
                p3 = (math.floor(x), math.floor(y - 1))
                p4 = (math.floor(x), math.floor(y + 1))
                # Compute distances
                d1 = (p1[0] - x) ** 2 + (p1[1] - y) ** 2 
                d2 = (p2[0] - x) ** 2 + (p2[1] - y) ** 2 
                d3 = (p3[0] - x) ** 2 + (p3[1] - y) ** 2 
                d4 = (p4[0] - x) ** 2 + (p4[1] - y) ** 2 
                # Compute weights
                total = d1 + d2 + d3 + d4
                average = total / 4
                w1 = d1 / average
                w2 = d2 / average
                w3 = d3 / average
                w4 = d4 / average
                # Compute interpolation
                interpolatedPixel = (paddedImage[p1[1], p1[0], k] * w1 + \
                    paddedImage[p2[1], p2[0], k] * w2 + \
                    paddedImage[p3[1], p3[0], k] * w3 + \
                    paddedImage[p4[1], p4[0], k] * w4) / total
                outputImage[i, j, k] = interpolatedPixel
    
    return outputImage

mario = cv2.imread('../inputs/mario.png')
upscaledMario = bilinearInterpolation(mario, 5)
cv2.imwrite('./bilinearMario.png', upscaledMario)