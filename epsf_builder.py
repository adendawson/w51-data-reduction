from astropy.visualization import simple_norm
import matplotlib.pyplot as pl
from astropy.table import Table
from astropy.stats import sigma_clipped_stats
from astropy.nddata import NDData
from photutils.psf import extract_stars
from photutils.psf import EPSFBuilder
import photutils as p
from photutils import DAOStarFinder
from astropy import stats

def epsf_builder(data):
    std = stats.mad_std(data)
    
    mask = p.make_source_mask(data = data, nsigma = 2, npixels = 5)
    mean, median, std = sigma_clipped_stats(data, sigma = 3, mask = mask)
    
    #can use std when calculating threshold but std value is small and threshold needs to be big ~3000
    daofind = DAOStarFinder(fwhm = 3.0, threshold = 3000.) 
    starcat = daofind(data - median)
    
    size = 25
    hsize = (size - 1) / 2
    x = starcat['xcentroid']  
    y = starcat['ycentroid']  
    mask = ((x > hsize) & (x < (data.shape[1] -1 - hsize)) & (y > hsize) & (y < (data.shape[0] -1 - hsize))) 
    
    starcat = Table()
    starcat['x'] = x[mask]  
    starcat['y'] = y[mask] 
    
    mean_val, median_val, std_val = sigma_clipped_stats(data, sigma=2.)  
    data -= median_val  
    
    nddata = NDData(data=data)  
    
    stars = extract_stars(nddata, starcat, size=25)
    
    #very basic EPSBuilder args (will add more) 
    epsf_builder = EPSFBuilder(oversampling=4, maxiters=10, progress_bar=False)  
    epsf, fitted_stars = epsf_builder(stars)
    
    return epsf, fitted_stars 