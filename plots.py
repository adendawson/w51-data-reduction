import matplotlib.pyplot as pl
import numpy as np

def make_cmd(size, table, xaxis, yaxis, label, xlim, ylim, legend, save, ext_vec = 5, markersize = 2, color = 'black'):
    
    a_v = ext_vec
    a_k = a_v * 0.112
    a_h = a_k * 1.56
    a_j = a_k * 2.51

    J = 13
    H = 12
    K = 11

    HK = (H + a_h) - (K + a_k)
    JK = (J + a_j) - (K + a_k)
    JH = (J + a_j) - (H + a_h)
    
    fig = pl.figure(figsize = (size,size))
    ax = pl.subplot()
    if xaxis == 'J-H' and yaxis == 'J':
        ax.scatter(table['mag_j_cal'] - table['mag_h_cal'], table['mag_j_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, JH - 1, a_j])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
    if xaxis == 'J-H' and yaxis == 'H':
        ax.scatter(table['mag_j_cal'] - table['mag_h_cal'], table['mag_h_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, JH - 1, a_h])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
    if xaxis == 'J-H' and yaxis == 'K':
        ax.scatter(table['mag_j_cal'] - table['mag_h_cal'], table['mag_k_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, JH - 1, a_k])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
        
    if xaxis == 'J-K' and yaxis == 'J':
        ax.scatter(table['mag_j_cal'] - table['mag_k_cal'], table['mag_j_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, JK - 2, a_j])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
    if xaxis == 'J-K' and yaxis == 'H':
        ax.scatter(table['mag_j_cal'] - table['mag_k_cal'], table['mag_h_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, JK - 2, a_h])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
    if xaxis == 'J-K' and yaxis == 'K':
        ax.scatter(table['mag_j_cal'] - table['mag_k_cal'], table['mag_k_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, JK - 2, a_k])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
        
    if xaxis == 'H-K' and yaxis == 'J':
        ax.scatter(table['mag_h_cal'] - table['mag_k_cal'], table['mag_j_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, HK - 1, a_j])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
    if xaxis == 'H-K' and yaxis == 'H':
        ax.scatter(table['mag_h_cal'] - table['mag_k_cal'], table['mag_h_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, HK - 1, a_h])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
    if xaxis == 'H-K' and yaxis == 'K':
        ax.scatter(table['mag_h_cal'] - table['mag_k_cal'], table['mag_k_cal'], s = markersize, color = color, label = label)
        vec = np.array([1.0, 9, HK - 1, a_k])
        X, Y, U, V = vec
        ax.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale = 1, label = f'Av = {ext_vec} mag')
        
    pl.xlabel(f'{xaxis}'); pl.ylabel(f'{yaxis}')
    pl.xlim(xlim); pl.ylim(ylim)
    if legend == True:
        pl.legend()
    ax.invert_yaxis()
    if save == True:
        fig.savefig(f'{xaxis}vs{yaxis}_CMD.png')
    
    return fig

def make_ccd(size, table, label, xlim, ylim, legend, save, ext_vec = 5, markersize = 2, color = 'black'):
    a_v = ext_vec
    a_k = a_v * 0.112
    a_h = a_k * 1.56
    a_j = a_k * 2.51

    J = 13
    H = 12
    K = 11

    HK = (H + a_h) - (K + a_k)
    JK = (J + a_j) - (K + a_k)
    JH = (J + a_j) - (H + a_h)
    
    fig = pl.figure(figsize = (size,size))
    ax = pl.subplot()
    ax.scatter(table['mag_h_cal'] - table['mag_k_cal'], table['mag_j_cal'] - table['mag_h_cal'], s = markersize, color = color, label = label)
    pl.xlabel('H-K'); pl.ylabel('J-H')
    pl.xlim(xlim); pl.ylim(ylim)
    if legend == True:
        pl.legend()
    if save == True:
        fig.savefig('ccd.png')
    
    return fig
