import numpy as np

def epx_upsample(image):
    h, w, c = image.shape
    output = np.zeros((2 * h, 2 * w, c), dtype=np.uint8)
    
    for i in range(h):
        for j in range(w):
            # 'p' and its surrounding pixel
            p = image[i, j, :]
            
            a = image[i-1, j, :] if i != 0 else p
            b = image[i, j + 1, :] if j != w - 1 else p 
            c = image[i, j - 1, :] if j != 0 else p
            d = image[i + 1, j, :] if i != h - 1 else p
            
            # Default to corresponding pixel
            output[2 * i, 2 * j, :] = p
            output[2 * i + 1, 2 * j, :] = p
            output[2 * i, 2 * j + 1, :] = p
            output[2 * i + 1, 2 * j + 1, :] = p
            
            # Replacement of neighbors
            if np.array_equal(c, a) and not np.array_equal(c, d) and not np.array_equal(a, b):
                output[2 * i, 2 * j, :] = a
            if np.array_equal(a, b) and not np.array_equal(a, c) and not np.array_equal(b, d):
                output[2 * i, 2 * j + 1, :] = b
            if np.array_equal(d, c) and not np.array_equal(d, b) and not np.array_equal(c, a):
                output[2 * i + 1, 2 * j, :] = c
            if np.array_equal(b, d) and not np.array_equal(b, a) and not np.array_equal(d, c):
                output[2 * i + 1, 2 * j + 1, :] = d
    
    return output