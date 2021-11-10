import numpy as np

def saturated_mask(array):
    
    bad1 = (array['x_h'] > 0) & (array['x_h'] < np.max(array['x_h'])) & (array['y_h'] > 0) & (array['y_h'] < 15)
    good_rows1 = ~bad1

    bad2 = (array['x_h'] > 325) & (array['x_h'] < 370) & (array['y_h'] > 320) & (array['y_h'] < 360)
    good_rows2 = ~bad2

    bad3 = (array['x_h'] > 1980) & (array['x_h'] < 2025) & (array['y_h'] > 1900) & (array['y_h'] < 1950)
    good_rows3 = ~bad3

    bad4 = (array['x_h'] > 1480) & (array['x_h'] < 1525) & (array['y_h'] > 2225) & (array['y_h'] < 2255)
    good_rows4 = ~bad4

    bad5 = (array['x_h'] > 1070) & (array['x_h'] < 1120) & (array['y_h'] > 2170) & (array['y_h'] < 2210)
    good_rows5 = ~bad5
    
    masked_catalog = array[good_rows1 & good_rows2 & good_rows3 & good_rows4 & good_rows5]
    
    return masked_catalog
