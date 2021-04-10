import matplotlib.pyplot as plt
from BrushMode import BrushMode as BM
from ColorSelector import ColorSelector as CS
from FrameController import FrameController as FM
from utils import add_subplot_axes


class LLS_Maker:
    pass


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.01,
                    bottom=0.01,
                    right=0.99,
                    top=0.99,
                    wspace=0.1,
                    hspace=0.1)

maker = LLS_Maker()
modeAx = add_subplot_axes(ax, [0.66, 0.5, 0.35, 0.5])
colorAx = add_subplot_axes(ax, [0.33, 0.5, 0.35, 0.5])
frameAx = add_subplot_axes(ax, [0, 0.5, 0.3, 0.5])
mirrorAx = add_subplot_axes(ax, [0, 0, 1, 0.5])

mode = BM(maker, modeAx)
color = CS(maker, colorAx)
frame = FM(maker, frameAx)




plt.show()