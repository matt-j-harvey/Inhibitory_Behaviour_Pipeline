import matplotlib.pyplot as plt


def forceAspect(ax,aspect=1):
    im = ax.get_images()
    extent =  im[0].get_extent()
    ax.set_aspect(abs((extent[1]-extent[0])/(extent[3]-extent[2]))/aspect)

def plot_lick_raster(lick_raster):

    figure_1 = plt.figure()
    axis_1 = figure_1.add_subplot(1,1,1)

    axis_1.imshow(lick_raster)
    forceAspect(axis_1, aspect=3)
    plt.show()