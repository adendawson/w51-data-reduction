from astropy.io import fits
import numpy as np
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.table import Table, Column, unique
from astropy import table
from astropy.io import ascii

def catalog_constructor(main_catalog, other_catalog, main_catalog_fh, other_catalog_fh, main_filter, other_filter):
    #main_catalog : catalog with highest population
    #other_catalog : catalog you want to add to main
    #main_catalog_wcs : filehandle of main filter image (main_catalog_fh = fits.open(your_file_path_here))
    #other_catalog_wcs : filehandle of other catalog image
    #main_filter (str) : one letter name of filter
    #other_filter (str) : one letter name of filter
    
    main_catalog_wcs = WCS(main_catalog_fh[0].header)
    other_catalog_wcs = WCS(other_catalog_fh[0].header)
    
    ra_main, dec_main = main_catalog_wcs.all_pix2world(main_catalog['x_0'], main_catalog['y_0'], 0)*u.deg
    ra_add, dec_add = other_catalog_wcs.all_pix2world(other_catalog['x_0'], other_catalog['y_0'], 0)*u.deg
    
    main_cat = SkyCoord(ra = ra_main, dec = dec_main)
    other_cat = SkyCoord(ra = ra_add, dec = dec_add)
    
    index, d2d, d3d = main_cat.match_to_catalog_sky(other_cat)
    
    main_catalog.add_column(col = np.zeros(len(main_catalog), dtype = 'int'), name = f"{other_filter}band_match_number")
    main_catalog.add_column(col = np.zeros(len(main_catalog), dtype = 'float'), name = f"{other_filter}band_match_separation")
    
    for i in range(len(main_catalog)):
        main_catalog[f"{other_filter}band_match_number"][i] = index[i]
        main_catalog[f"{other_filter}band_match_separation"][i] = d3d[i]
        
    #main_catalog.rename_column('peak', f'peak_{main_filter}')
    #main_catalog.rename_column('flux_0', f'flux_{main_filter}')
    #main_catalog.rename_column('mag', f'mag_{main_filter}')
    
    indices = main_catalog[f'{other_filter}band_match_number']
    
    main_catalog.add_column(col=other_catalog['peak'][indices], name=f'peak_{other_filter}')
    main_catalog.add_column(col=other_catalog['mag'][indices], name=f'mag_{other_filter}')
    main_catalog.add_column(col=other_catalog['flux_0'][indices], name=f'flux_{other_filter}')
    
    match_numbers = np.unique(main_catalog[f'{other_filter}band_match_number'])

    main_catalog.add_column(col=np.ones(len(main_catalog), dtype='bool'), name=f'{other_filter}band_matched')
    
    for idnumber in match_numbers:
        selection = main_catalog[f'{other_filter}band_match_number'] == idnumber
        separations = main_catalog[f'{other_filter}band_match_separation'][selection]
        closest = np.where(selection)[0][np.argmin(separations)]
        selection[closest] = False
        for col in (f'peak_{other_filter}', f'mag_{other_filter}', f'flux_{other_filter}'):
            main_catalog[col][selection] = np.nan
        main_catalog[f'{other_filter}band_matched'][selection] = False
    
    return main_catalog