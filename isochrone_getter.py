from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import mechanize
from astropy.table import Table

def isochrone_getter(link, filters, extinction, one_age, log_age, log_age_low, log_age_high, lin_age_low, lin_age_high, age_step):
    
    viable_filters = ['YBC_tab_mag_odfnew/tab_mag_ubvrijhk.dat', 'YBC_tab_mag_odfnew/tab_mag_2mass.dat']
    
    br = mechanize.Browser()
    br.open(link)
    br.select_form(nr = 0)
    br['photsys_file'] = [viable_filters[filters]]
    br['extinction_av'] = f'{extinction}'
    
    if log_age == True:
        
        br['isoc_isagelog'] = ['1',]
        
        if one_age == True:
            br['isoc_lagelow'] = f'{log_age_low}'
            br['isoc_dlage'] = '0.0'
            br.submit()
        
        if one_age == False:
            br['isoc_lagelow'] = f'{log_age_low}'
            br['isoc_lageupp'] = f'{log_age_high}'
            br['isoc_dlage'] = f'{age_step}'
            br.submit()
            
    if log_age == False:
        
        br['isoc_isagelog'] = ['0',]
        
        if one_age == True:
            br['isoc_agelow'] = f'{lin_age_low}'
            br['isoc_dage'] = '0.0'
            br.submit()
        
        if one_age == False:
            br['isoc_agelow'] = f'{lin_age_low}'
            br['isoc_ageupp'] = f'{lin_age_high}'
            br['isoc_dage'] = f'{age_step}'
            br.submit()
    
    response1 = br.follow_link(text_regex = 'output')
    html = urlopen(response1.geturl()).read()
    soup = BeautifulSoup(html, features = 'html.parser')
    text = soup.get_text()
    
    iso_table = Table.read(text, format = 'ascii')
    
    if filters == 0:
        old_names = ('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14', 'col15', 'col16', 'col17', 'col18', 'col19', 'col20', 'col21', 
                     'col22', 'col23', 'col24', 'col25', 'col26', 'col27', 'col28', 'col29', 'col30', 'col31', 'col32', 'col33', 'col34', 'col35', 'col36')

        col_names = ('Zini', 'MH', 'logAge', 'Mini', 'int_IMF', 'Mass', 'logL', 'logTe', 'logg', 'label', 'McoreTP', 'C_O', 'period0', 'period1', 'period2', 
                     'period3', 'period4', 'pmode', 'Mloss', 'tau1m', 'X', 'Y', 'Xc', 'Xn', 'Xo', 'Cexcess', 'Z', 'mbolmag', 'Umag', 'Bmag', 'Vmag', 'Rmag', 'Imag', 'Jmag', 'Hmag', 'Kmag')
        
        iso_table.rename_columns(old_names, col_names)
        
    if filters == 1:
        old_names = ('col1', 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11', 'col12', 'col13', 'col14', 'col15', 'col16', 'col17', 'col18', 'col19', 'col20', 'col21', 
                     'col22', 'col23', 'col24', 'col25', 'col26', 'col27', 'col28', 'col29', 'col30', 'col31')

        col_names = ('Zini', 'MH', 'logAge', 'Mini', 'int_IMF', 'Mass', 'logL', 'logTe', 'logg', 'label', 'McoreTP', 'C_O', 'period0', 'period1', 'period2', 
                     'period3', 'period4', 'pmode', 'Mloss', 'tau1m', 'X', 'Y', 'Xc', 'Xn', 'Xo', 'Cexcess', 'Z', 'mbolmag', 'Jmag', 'Hmag', 'Kmag')
        
        iso_table.rename_columns(old_names, col_names)

    return iso_table
