import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class AxBorder(mpatches.Rectangle):
    def __init__(self, rect=[0.01, 0.01, 0.98, 0.98], lw=5, ec="black", fill=False, **kwargs):
        super().__init__(rect[:2], rect[2], rect[3], lw=lw, fill=fill, ec=ec, **kwargs)


def add_subplot_axes(ax, rect):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]
    subax = fig.add_axes([x, y, width, height])
    subax.axis("off")
    return subax
