# from os import symlink
from tkinter import *
from tkinter import ttk
# from ttkthemes.themed_tk import ThemedTk
from colour import Color
# from ttkwidgets import ScaleEntry
from PIL import Image, ImageTk



class clickableScale(ttk.Scale):
    """a type of Scale where the left click is hijacked to work like a right click"""
    def __init__(self, master=None, **kwargs):
        ttk.Scale.__init__(self, master, **kwargs)
        self.bind('<Button-1>', self.set_value)

    def set_value(self, event):
        self.event_generate('<Button-3>', x=event.x, y=event.y)
        return 'break'




class Lightshow:
    shows = []
    GUImaster = None
    active = False
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
            show.button.config(style="off.TButton")
            if show.active and show != self:
                show.destroy_ui()
                show.active = False
        self.button.config(style="on.TButton")
        self.GUImaster.focus()
        self.build_ui()

    
    def build_ui(self):
        if self.active: return
        self.active = True
        print("ui build not configured")
    
    def destroy_ui(self):
        print("ui destruction not configured")




class Mono_LS(Lightshow):
    """
    A single-color lightshow wherein the color is controlable through a slider
    """
    active = False
    def build_ui(self):
        if self.active: return
        

        crange = [a.get_hex() for a in Color("blue").range_to(Color("red"), 1134)] 
        def set_colorbar_slider_bg(idx):
            self.GUImaster.style.configure("colorbar.Horizontal.TScale", troughcolor=crange[int(round(float(idx)))])
        
        
        self.color_scale = clickableScale(self.GUImaster.bottom_frame, from_=0, to=1133,orient="horizontal", command=set_colorbar_slider_bg, style="colorbar.Horizontal.TScale")
        self.color_scale.pack(fill="both", side="bottom",anchor="s")
        self.active = True 
    

    def destroy_ui(self):
        self.color_scale.pack_forget()
        self.GUImaster.style.configure("colorbar.Horizontal.TScale", troughcolor="blue")


# class GUI(ThemedTk):
class GUI(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        #self.set_theme("black")
        self.title("Laplace Lightshows")
        # self.config(cursor="none") # enable this to hide cursor on touch display
        self.attributes("-fullscreen", True) # enable this to go fullscreen on touch display
        self.style = ttk.Style()
        self.geometry("1280x400")
        self.resizable(False, False)

        self.style.configure("colorbar.Horizontal.TScale", troughcolor="blue", sliderthickness=40)
        
        self.button_frame = Frame(self, bg="grey")
        self.preview_frame = Frame(self, bg="grey")
        self.bottom_frame = Frame(self, bg = "grey")
        self.right_frame = Frame(self, bg = "grey")
        
        self.button_frame.grid(row = 0, column = 0,  sticky = "NSEW")
        self.preview_frame.grid(row = 1, column = 0,  sticky = "NSEW")
        self.bottom_frame.grid(row = 2, column = 0, columnspan = 1, sticky = "NSEW")
        self.right_frame.grid(row = 0, column = 1, rowspan= 3, columnspan=3, sticky = "NSEW")


        for i in range(4):
            self.columnconfigure(i,weight=1)
        self.rowconfigure(1,weight=1)

        self.fill_right_frame()
        

    
    def add_buttons(self):
        self.style.configure("on.TButton", background="grey", relief="flat", foreground="red")
        self.style.configure("off.TButton", background="#6b6b6b", relief="sunken", foreground="grey")
        self.style.map("on.TButton", 
            foreground = [("active", "grey")],
            background = [("active", "grey")]
                )
        for show in Lightshow.shows:
            show_button = ttk.Button(self.button_frame, image = show.icon, style="off.TButton")
            show.button = show_button
            show_button.config(command=show)
           
            show_button.pack(side="left", anchor="nw")
        Lightshow.shows[0].button.config(style="on.TButton")
    
    def fill_right_frame(self):
        # fills right frame with a brightness slider and power button
        def adjust_brightness(arg):
            print(arg)
        
    
        self.power_icon =ImageTk.PhotoImage(Image.open("off.png"))
        self.style.configure("power.TButton", background="grey")
        self.power_button = ttk.Button(self.right_frame, command= self.destroy, image = self.power_icon, style="power.TButton")
        self.power_button.image= self.power_icon
        self.power_button.pack(side="top", anchor="nw", fill="x")

        self.style.configure("brightness.Vertical.TScale", troughcolor="grey")
        self.brightness_scale = clickableScale(self.right_frame, from_=100, to=0, orient="vertical", command = adjust_brightness, style="brightness.Vertical.TScale")
        self.brightness_scale.pack(fill = "y", side="right", expand=True)






if __name__ == "__main__":
    gui = GUI()
    Lightshow.GUImaster = gui # set the standard parent for all lighshow gui objects
    LS_mono = Mono_LS("mono", "icon.png")
    LS_wheel = Lightshow("wheel", "icon.png")
    LS_dots = Lightshow("dots", "icon.png")
    LS_dots1 = Lightshow("dots1", "icon.png")
    LS_dots2 = Lightshow("dots2", "icon.png")
    LS_dots3 = Lightshow("dots3", "icon.png")
    LS_dots4 = Lightshow("dots4", "icon.png")
    LS_dots5 = Lightshow("dots5", "icon.png")
    LS_mono.build_ui()
    gui.add_buttons()
    gui.bind_all("<Control-c>", lambda event: gui.destroy() )
    gui.mainloop()

# #root = Tk()
# #root.geometry("1280x400")


# # img_render = ImageTk.PhotoImage(Image.open("colorbar2.png") )
# # img = Label(root, image=img_render)
# # img.pack(side="bottom",anchor="sw")


# crange = [a.get_hex() for a in Color("blue").range_to(Color("red"), 1001)]
# def set_colorbar_slider_bg(idx):
#     idx = int(idx.replace(".",""))
#     color_slider.config(troughcolor=crange[idx])
# color_slider = Scale(root, troughcolor=crange[0], from_=0, to=100, orient="horizontal", command=set_colorbar_slider_bg, showvalue=0,width=35, resolution=0.1)
# color_slider.pack(side="bottom", fill="x",pady=0)


# brightness_slider = Scale(root, from_=100, to=0, width=40)
# brightness_slider.pack(side="right", fill="y")

# # add permanent lightshows

# show_buttons = []
# for show in Lightshow.shows:
#     show_button = Button(root, image = show.icon, relief="raised",activebackground="red", bg="blue")
#     show.button = show_button
#     show_button.config(command=show)
#     show_button.pack(side="left", anchor="nw")
#     show_buttons.append(show_button)
# show_buttons[0].config(relief="sunken")


# root.mainloop()

