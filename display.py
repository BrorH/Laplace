import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from PIL import Image


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
    return subax


def click(event):
    if colorpicker.contains(event)[0]:
        x = event.xdata
        y = event.ydata
        if x is not None and y is not None:
            x = round(x)
            y = round(y)
            xc = x / 150 - 1
            yc = y / 150 - 1
            r = np.sqrt(xc ** 2 + yc ** 2)
            if r < 0.99:
                color = img[y, x, :]
                C.set_color(color / 255)
    elif mirror.contains(event)[0]:
        for pixel in mirror.get_children():
            if isinstance(pixel, Pixel):
                if pixel.contains(event)[0]:
                    pixel.set_color(C.get_ec())
                    break
    plt.draw()


class Pixel(mpatches.Rectangle):
    def __init__(self, x, y, xlen, ylen):
        super().__init__((x, y), xlen, ylen, fill=True)
        self.set_color((0, 0, 0))


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.01,
                    bottom=0.01,
                    right=0.99,
                    top=0.99,
                    wspace=0.1,
                    hspace=0.1)



Ps = [Pixel(i * 0.01, 0.7, 0.01, 0.3) for i in range(100)]
mirror = add_subplot_axes(ax, [0.01, 0.01, 0.98, 0.49])
for P in Ps:
    mirror.add_artist(P)

img = Image.open("ColorWheel.png")
img = np.asarray(img.convert("RGB"))
colorpicker = add_subplot_axes(ax, [0, 0.51, 0.48, 0.48])
colorpicker.imshow(img)
colorpicker.axis("off")

C = Pixel(-0.5, -0.5, 1, 1)
current = add_subplot_axes(ax, [0.5, 0.7, 0.2, 0.2])
current.axis("equal")
current.axis("off")
current.add_artist(C)

fig.canvas.mpl_connect("button_press_event", click)
ax.axis("off")

# print(ax.get_children())

plt.show()