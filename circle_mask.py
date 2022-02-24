import numpy as np

def circle_mask(array_shape, x0, y0, radius):

    y, x = np.ogrid[:array_shape[0], :array_shape[1]]
    d = np.sqrt((x - x0)**2 + (y - y0)**2)

    mask = d <= radius
    
    return mask
