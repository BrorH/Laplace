import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from utils import add_subplot_axes, AxBorder
import numpy as np
import sys


class ColorSelector:
    def __init__(self, Maker, ax):
        self.Maker = Maker
        self.Maker.CS = self
        self.ax = ax

        self.rgba = np.zeros(4, dtype=int)

        brightAx = add_subplot_axes(self.ax, [0.7, 0.1, 0.25, 0.05])
        brightAx.add_artist(AxBorder())
        self.bright = Slider(brightAx, "Brightness", 0, 1, valinit=1, initcolor='none', valstep=0.05, fc="k")

        self.R, self.Vr = rgbSlider(self, "R", 0)
        self.G, self.Vg = rgbSlider(self, "G", 1)
        self.B, self.Vb = rgbSlider(self, "B", 2)

        currAx = add_subplot_axes(self.ax, [0.5, 0.5, 0.5, 0.45])
        self.CurrCol = AxBorder(fill=True, fc=self.rgba/255)
        currAx.add_artist(self.CurrCol)
        self.CurrButt = Button(currAx, "")

    def get_set_single(self, c, val=None, me=False):
        if val is None:
            return self.rgba[c]
        else:
            self.rgba[c] = val
            if c == 0:
                if not me:
                    self.R.set_val(val)
                self.Vr.set_val(val)
            elif c == 1:
                if not me:
                    self.G.set_val(val)
                self.Vg.set_val(val)
            elif c == 2:
                if not me:
                    self.B.set_val(val)
                self.Vb.set_val(val)
            elif c == 3:
                if  not me:
                    self.bright.set_val(val)
                self.Vbright.set_val(val)
            self.CurrCol.set_fc(self.rgba / 255)


    def get_set_all(self, val=None):
        if val is None:
            return self.rgba
        else:
            self.rgba[:3] = val
            for i in range(3):
                self.get_set_single(i, val[i])


class NumberButton(Button):
    def __init__(self, ax, func, c, arg):
        self.func = func
        self.get = lambda: self.func(arg)
        self.set = lambda x: self.func(arg, x)
        self.c = c

        super().__init__(ax, str(self.get()))

        self.label.set_fontsize(20)
        self.label.set_fontweight("heavy")

        self.on_clicked(self.click)

    def set_val(self, val):
        self.label.set_text(str(val))

    def click(self, event):
        self.inp.set_visible(True)
        self.connect_me()
        plt.draw()

    def get_num(self, event):
        pass



def rgbSlider(Maker, c, n):
    I = np.identity(3)
    x0 = 0.05 + n * 0.15

    ax = add_subplot_axes(Maker.ax, [x0, 0.2, 0.1, 0.7])
    ax.add_artist(AxBorder(rect=[0.01, 0.01, 0.99, 255]))
    slid = Slider(ax, c, 0, 255, valinit=0, initcolor="none", valstep=1, orientation="vertical", fc=I[n])
    slid.label.set_fontweight("heavy")
    slid.label.set_fontsize(20)
    slid.valtext.set_visible(False)
    slid.on_changed(lambda x: Maker.get_set_single(n, x, True))

    valAx = add_subplot_axes(Maker.ax, [x0, 0.05, 0.1, 0.1])
    valAx.add_artist(AxBorder())
    val = NumberButton(valAx, Maker.get_set_single, c, n)
    return slid, val
