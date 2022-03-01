import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table, Column, unique, vstack, TableColumns
from astropy import table

def catalog_cross_matcher(main_cat, other_cat_table, other_cat_name, ra_column_name, dec_column_name, add_cols):
    
    main_cat[ra_column_name].fill_value = -99
    main_cat[dec_column_name].fill_value = -99
    
    def column_converter(column):
        ting = [column[i]*u.deg for i in range(len(column))]
    
        return ting
    
    ra_main = column_converter(main_cat.filled()[ra_column_name])
    dec_main = column_converter(main_cat.filled()[dec_column_name])
    
    main = SkyCoord(ra = ra_main, dec = dec_main)
    other = SkyCoord(ra = other_cat_table['ra']*u.deg, dec = other_cat_table['dec']*u.deg)

    index, d2d, d3d = main.match_to_catalog_sky(other)
    
    main_cat.add_column(col = np.zeros(len(main_cat), dtype = 'int'), name = f"{other_cat_name}_match_number")
    main_cat.add_column(col = np.zeros(len(main_cat), dtype = 'float'), name = f"{other_cat_name}_match_separation")
    
    for i in range(len(main_cat)):
        main_cat[f"{other_cat_name}_match_number"][i] = index[i]
        main_cat[f"{other_cat_name}_match_separation"][i] = (d2d[i].to(u.arcsec)) / u.arcsec
    
    indices = main_cat[f'{other_cat_name}_match_number']

    for i in range(len(add_cols)):
        main_cat.add_column(col = other_cat_table[add_cols[i]][indices], name = add_cols[i])
    
    match_numbers = np.unique(main_cat[f'{other_cat_name}_match_number'])

    main_cat.add_column(col=np.ones(len(main_cat), dtype='bool'), name=f'{other_cat_name}_matched')
    
    for idnumber in match_numbers:
        selection = main_cat[f'{other_cat_name}_match_number'] == idnumber
        separations = main_cat[f'{other_cat_name}_match_separation'][selection]
        closest = np.where(selection)[0][np.argmin(separations)]
        selection[closest] = False
        for col in add_cols:
            main_cat[col][selection] = np.nan
        main_cat[f'{other_cat_name}_matched'][selection] = False
        
    return main_cat