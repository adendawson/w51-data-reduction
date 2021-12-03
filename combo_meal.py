import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table, Column, unique, vstack, TableColumns
from astropy import table

def column_converter(column):
    ting = [column[i]*u.deg for i in range(len(column))]
    
    return ting

def catalog_cross_matcher(main_cat, other_cat):
    
    main_cat['RAJ2000'].fill_value = -99
    main_cat['DEJ2000'].fill_value = -99
    
    ra_main = column_converter(main_cat.filled()['RAJ2000'])
    dec_main = column_converter(main_cat.filled()['DEJ2000'])
    
    main = SkyCoord(ra = ra_main, dec = dec_main)
    other = SkyCoord(ra = other_cat['ra']*u.deg, dec = other_cat['dec']*u.deg)

    index, d2d, d3d = main.match_to_catalog_sky(other)
    
    main_cat.add_column(col = np.zeros(len(main_cat), dtype = 'int'), name = "new_cat_match_number")
    main_cat.add_column(col = np.zeros(len(main_cat), dtype = 'float'), name = "new_cat_match_separation")
    
    for i in range(len(main_cat)):
        main_cat["new_cat_match_number"][i] = index[i]
        main_cat["new_cat_match_separation"][i] = (d2d[i].to(u.arcsec)) / u.arcsec
    
    indices = main_cat['new_cat_match_number']

    main_cat.add_column(col=other_cat['mag_j_cal'][indices], name='j_mag_new_cal')
    main_cat.add_column(col=other_cat['mag_h_cal'][indices], name='h_mag_new_cal')
    main_cat.add_column(col=other_cat['mag_k_cal'][indices], name='k_mag_new_cal')
    
    match_numbers = np.unique(main_cat['new_cat_match_number'])

    main_cat.add_column(col=np.ones(len(main_cat), dtype='bool'), name='new_cat_matched')
    
    for idnumber in match_numbers:
        selection = main_cat['new_cat_match_number'] == idnumber
        separations = main_cat['new_cat_match_separation'][selection]
        closest = np.where(selection)[0][np.argmin(separations)]
        selection[closest] = False
        for col in ('j_mag_new_cal', 'h_mag_new_cal', 'k_mag_new_cal'):
            main_cat[col][selection] = np.nan
        main_cat['new_cat_matched'][selection] = False
        
    return main_cat
