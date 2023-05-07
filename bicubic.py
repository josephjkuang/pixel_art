import numpy as np
import cv2
import math
import matplotlib.pyplot as plt
from PIL import Image

# Bicubic convolution algorithm
# For best results: a = -0.5 or a = -0.75
def kernel(a, x):
    if abs(x) <= 1:
        return (a + 2) * abs(x) ** 3 - (a + 3) * abs(x) ** 2 + 1
    elif 1 < abs(x) and abs(x) < 2:
        return a * abs(x) ** 3 - 5 * a * abs(x) ** 2 + 8 * a * abs(x) - 4 * a
    else:
        return 0

# Bicupic Interpolation
def bicubicUpsample(image, scaleFactor, a):
    H, W, C = image.shape
    scaledH = int(np.floor(scaleFactor * H))
    scaledW = int(np.floor(scaleFactor * W))
    upsampledImage = np.zeros((scaledH, scaledW, C))
    paddedImage = cv2.makeBorder(image, 2, 2, 2, 2, cv2.BORDER_REFLECT)
    inverseScaleFactor = 1 / scaleFactor
    for i in range(scaledH):
        for j in range(scaledW):
            for k in range(C):
                xSource = i * inverseScaleFactor
                ySource = j * inverseScaleFactor
                print(xSource)
                print(ySource)
                # Sample the 4x4 region around pixel in souce image
                # Should give 16 pixels in total
                # Store pixel values in 4 x 4 coefficient matrix
                coefficientMatrix = np.zeros((4, 4))
                for n in range(-1, 3, 1):
                    for m in range(-1, 3, 1):
                        coefficientMatrix[n + 1, m + 1] = paddedImage[xSource + n, ySource + m, k]
                # Compute x intepolation vector
                xInterpolationVec = np.zeros((4, 1))
                for n in range(-1, 3, 1):
                    xInterpolationVec[n + 1] = NotImplemented
                # Compute y interpolation vector
                yInterpolationVec = np.zeros((4, 1))
                for n in range(-1, 3, 1):
                    yInterpolationVec[n + 1] = NotImplemented
                # Compute interpolated pixel
                interpolatedPixel = np.dot(
                    np.dot(xInterpolationVec, coefficientMatrix), yInterpolationVec)
                upsampledImage[i, j, k] = interpolatedPixel
    return upsampledImage

mario = Image.open('../inputs/mario.png')
upscaledBowser = mario.resize((mario.width * 5, mario.height * 5), resample=Image.BICUBIC)
upscaledBowser.save('./bicubicMario.png')
