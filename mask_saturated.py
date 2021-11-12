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
    
    bad6 = (array['x_h'] > 2190) & (array['x_h'] < 2260) & (array['y_h'] > 1350) & (array['y_h'] < 1395)
    good_rows6 = ~bad6
    
    bad7 = (array['x_h'] > 2075) & (array['x_h'] < 2085) & (array['y_h'] > 1415) & (array['y_h'] < 1425)
    good_rows7 = ~bad7
    
    bad8 = (array['x_h'] > 100) & (array['x_h'] < 200) & (array['y_h'] > 0) & (array['y_h'] < 100)
    good_rows8 = ~bad8
    
    bad9 = (array['x_h'] > 380) & (array['x_h'] < 390) & (array['y_h'] > 30) & (array['y_h'] < 95)
    good_rows9 = ~bad9
    
    masked_catalog = array[good_rows1 & good_rows2 & good_rows3 & good_rows4 & good_rows5 & good_rows6 & good_rows7 & good_rows8 & good_rows9]
    
    return masked_catalog