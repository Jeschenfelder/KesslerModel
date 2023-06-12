import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def convert_typearr(type_arr):
    ''' Convert Type array to numeric version for later plotting'''
    conversion_dict = {'b':0,'a': 1,'f':2,'s':3,'i':4,'v':1}
    viz_arr = type_arr.copy()
    for i in range(0,type_arr.shape[0]):
        for j in range(0,type_arr.shape[1]):
            viz_arr[i,j] = conversion_dict[type_arr[i,j]]
    viz_arr = viz_arr.astype('int')
    return viz_arr

def create_typecmap():
    ''' Function to create a colormap for the type array'''
    cmap = (colors.ListedColormap(['white','saddlebrown','dimgray','lightsteelblue'])
        .with_extremes(over='0', under='1'))

    bounds = [1,2,3,4]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    return cmap,bounds

def plot_typearr(viz_arr,cmap,bounds,title='Soil profile'):
    fig,ax = plt.subplots(1,1, figsize=(6,6))
    plot = ax.imshow(viz_arr,cmap=cmap,vmax=4)
    ax.set_title(title)
    cbar = fig.colorbar(plot,ax=ax,ticks=bounds)
    cbar.set_ticklabels(['air','fines','stones','ice'])
    return fig,ax