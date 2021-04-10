import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from utils import add_subplot_axes, AxBorder


class BrushMode:
    """
    Packaging class to hold right-most column of buttons;
    the ones that determine brush-mode
    """
    def __init__(self, Maker, ax):
        self.Maker = Maker  # Packaging class holding all of the Maker-display
        self.Maker.BM = self
        self.ax = ax
        self.mode = "Single"  # current mode
        self.fevry = 1
        self.brush_size = 1

        # Initialising the 4 mode-buttons
        singAx = add_subplot_axes(self.ax, [0.1, 0.75, 0.8, 0.2])
        fallAx = add_subplot_axes(self.ax, [0.1, 0.5, 0.8, 0.2])
        fevAx = add_subplot_axes(self.ax, [0.1, 0.25, 0.8, 0.2])
        brushAx = add_subplot_axes(self.ax, [0.1, 0, 0.8, 0.2])
        self.single = Coupled_Button(self, singAx, "Single", group="Mode", select=True)
        self.f_all = Coupled_Button(self, fallAx, "Fill all", group="Mode")
        self.f_every = Coupled_Button(self, fevAx, "Fill every", group="Mode")
        self.brush = Coupled_Button(self, brushAx, "Brush size", group="Mode")

        # Initialising the 2 number buttons
        numevAx = add_subplot_axes(fevAx, [0.7, 0, 0.3, 1])
        numbsAx = add_subplot_axes(brushAx, [0.75, 0, 0.25, 1])
        self.num_every = NumberButton(self.f_every, numevAx, self.get_set_fevry)
        self.num_brushsize = NumberButton(self.brush, numbsAx, self.get_set_brush_size)

    def get_set_fevry(self, val=None):
        if val is None:
            return self.fevry
        else:
            self.fevry = val

    def get_set_brush_size(self, val=None):
        if val is None:
            return self.brush_size
        else:
            self.brush_size = val


class Coupled_Button(Button):
    """
    Class to couple mpl.widgets.Button()s
    Only one button in each group can be active at a time
    When one is clicked, the others are un-clicked
    """
    Register = {}

    def __init__(self, window, ax, *args, group=None, select=False, **kwargs):
        super().__init__(ax, *args, **kwargs)
        self.window = window  # Mode
        self.group = group
        self.border = AxBorder()
        ax.add_artist(self.border)

        # Text properties
        self.label.set_fontsize(30)
        self.label.set_fontweight("heavy")
        self.label.set_x(0.1)
        self.label.set_horizontalalignment("left")

        # initialize group copuling
        if self.group is not None:
            if self.group in Coupled_Button.Register:
                Coupled_Button.Register[self.group].append(self)
            else:
                Coupled_Button.Register[self.group] = [self]

        self.on_clicked(self.click)
        self.set_selected(select)

    def set_selected(self, val):
        if not val:
            self.border.set_color("black")
        else:
            self.border.set_color("red")
            self.window.mode = self.label.get_text()
        self.selected = val

    def click(self, event):
        if self.group is not None:
            if not self.selected:
                for other in Coupled_Button.Register[self.group]:
                    other.set_selected(False)
                self.set_selected(True)
        plt.draw()


class NumberButton(Button):
    """
    Number selector buttons

    When clicked, will open a window to prompt user for number
    Disables all other input methods while this window is open
    """
    def __init__(self, parent, ax, func, text=None):
        self.parent = parent  # relating brush-mode button
        self.func = func  # callable in Mode to change value
        self.border = AxBorder()
        ax.add_artist(self.border)
        super().__init__(ax, str(self.func()))

        self.label.set_fontsize(30)
        self.label.set_fontweight("heavy")

        # Initialise overlay window which fills screen until new number selected
        if text is None:
            txt = "Hit a number on keyboard. Use Esc to go back"
        inpAx = plt.axes([0.15, 0.3, 0.7, 0.4])
        inpAx.axis("off")
        inpAx.add_artist(AxBorder(fill=True, fc="white"))
        inpAx.label = inpAx.text(0.5, 0.5,
                                 txt,
                                 fontsize=30,
                                 fontweight="bold",
                                 verticalalignment="center",
                                 horizontalalignment="center",
                                 transform=inpAx.transAxes,
                                 )
        inpAx.set_visible(False)
        self.inp = inpAx

        self.on_clicked(self.click)

    def click(self, event):
        self.inp.set_visible(True)
        self.connect_me()
        plt.draw()

    def get_num(self, event):
        if event.key in [str(i + 1) for i in range(9)]:
            self.func(event.key)  # change value in Mode
            self.label.set_text(str(event.key))  # update text
            self.disconnect_me()  # reactivate normal callbacks
            self.inp.set_visible(False)  # hide prompting window
        elif event.key == "escape":
            self.disconnect_me()
            self.inp.set_visible(False)
        plt.draw()

    def connect_me(self):
        # Disables all active callbackmethods, sets get_num as only callback
        self.default_callbacks = self.canvas.callbacks.callbacks  # save for reactivation
        plt.gcf().canvas.callbacks.callbacks = {}  # remove all
        self.cid = plt.gcf().canvas.mpl_connect("key_press_event", self.get_num)

    def disconnect_me(self):
        # Removes get_num for callbacks, reactivates all other callbacks
        plt.gcf().canvas.mpl_disconnect(self.cid)
        plt.gcf().canvas.callbacks.callbacks = self.default_callbacks
        self.parent.click(None)  # auto-select relevant brush-mode
