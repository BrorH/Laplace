from tkinter import *
from colour import Color
from PIL import Image, ImageTk

class Lightshow:
    shows = []
    def __init__(self, name, icon):
        self.name = name 
        self.icon =ImageTk.PhotoImage(Image.open(icon))
        if self not in Lightshow.shows:
            Lightshow.shows.append(self)
        self.button = None

    def __hash__(self):
        return hash(self.name)
    
    def __call__(self):
        for show in Lightshow.shows:
            show.button.config(relief="raised", bg="blue")
        self.button.config(relief="raised", bg="red")

root = Tk()
root.geometry("1280x400")


# img_render = ImageTk.PhotoImage(Image.open("colorbar2.png") )
# img = Label(root, image=img_render)
# img.pack(side="bottom",anchor="sw")


crange = [a.get_hex() for a in Color("blue").range_to(Color("red"), 1001)]
def set_colorbar_slider_bg(idx):
    idx = int(idx.replace(".",""))
    color_slider.config(troughcolor=crange[idx])
color_slider = Scale(root, troughcolor=crange[0], from_=0, to=100, orient="horizontal", command=set_colorbar_slider_bg, showvalue=0,width=35, resolution=0.1)
color_slider.pack(side="bottom", fill="x",pady=0)


brightness_slider = Scale(root, from_=100, to=0, width=40)
brightness_slider.pack(side="right", fill="y")

# add permanent lightshows
LS_static = Lightshow("static", "icon.png")
LS_wheel = Lightshow("wheel", "icon.png")
LS_dots = Lightshow("dots", "icon.png")
LS_dots1 = Lightshow("dots1", "icon.png")
LS_dots2 = Lightshow("dots2", "icon.png")
LS_dots3 = Lightshow("dots3", "icon.png")
LS_dots4 = Lightshow("dots4", "icon.png")
LS_dots5 = Lightshow("dots5", "icon.png")
LS_dots6 = Lightshow("dots6", "icon.png")
show_buttons = []
for show in Lightshow.shows:
    show_button = Button(root, image = show.icon, relief="raised",activebackground="red", bg="blue")
    show.button = show_button
    show_button.config(command=show)
    show_button.pack(side="left", anchor="nw")
    show_buttons.append(show_button)
# show_buttons[0].config(relief="sunken")


root.mainloop()

