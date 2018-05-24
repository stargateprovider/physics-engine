from tkinter import *
from tkinter import ttk
from engine import *

from threading import Thread
from demos import *


class VectorEntry(Frame):
    def __init__(self, master, **attr):
        super().__init__(master, **attr)
        self.x = DoubleVar(master, 0)
        self.y = DoubleVar(master, 0)

        xEntry = Entry(self, textvariable=self.x)
        yEntry = Entry(self, textvariable=self.y)
        xEntry["width"] = int(xEntry["width"] *.5 - 1)
        yEntry["width"] = int(yEntry["width"] *.5 - 1)
        xEntry.grid(row=0, column=0, padx=(0,4))
        yEntry.grid(row=0, column=1, padx=(4,0))
    def get(self):
        return Vec2D(self.x.get(), self.y.get())
    def set(self, x, y):
        self.x.set(x)
        self.y.set(y)


class Simulator():
    defaults = {
        "step"      : 1,
        "width"     : 600,
        "height"    : 450,
        "vBoundary" : 0,
        "g"         : Vec2D(0,0),
        "coef_drag" : 0,
        "bgcolor"   : (0,0,0),
        "pathLimit" : 0
    }
    
    def __init__(self, master, engine):
        self.master = master
        self.engine = engine
        self.simThread = Thread(target=self.engine.start)
        self.bodyNames = {}

        topBar = Frame(master)
        self.img = [PhotoImage(file='play.png'), PhotoImage(file='pause.png')]
        self.toggle_btn = Button(topBar, text="start", command=self.toggle_running,
                                 image=self.img[0], compound="left", relief=GROOVE)
        self.debugBox = Checkbutton(topBar, text="debug", command=self.toggle_debug)
        book = ttk.Notebook(master)

        ### keskkonna sätted
        settingsFrame = Frame(book)
        for i, txt in enumerate(("Laius", "Kõrgus", "Ajasamm", "Minimaalne kiirus",
                                 "Õhutakistustegur", "Gravitatsioon", "Taustavärv (RGB)", "Saba")):
            Label(settingsFrame, text=txt).grid(row=i, column=0)
        self.entry_scrX = Entry(settingsFrame)
        self.entry_scrY = Entry(settingsFrame)
        self.entry_dt = Entry(settingsFrame)
        self.entry_minv = Entry(settingsFrame)
        self.entry_g = VectorEntry(settingsFrame)
        self.entry_drag = Entry(settingsFrame)
        self.bgFrame = Frame(settingsFrame)
        Spinbox(self.bgFrame, from_=0, to=255, width=4).grid(row=0, column=0, padx=2)
        Spinbox(self.bgFrame, from_=0, to=255, width=4).grid(row=0, column=1, padx=1)
        Spinbox(self.bgFrame, from_=0, to=255, width=4).grid(row=0, column=2, padx=2)
        self.entry_trail = Entry(settingsFrame)

        Button(settingsFrame, text="Muuda sätted", command=self.change_settings).grid(row=8)
        book.add(settingsFrame, text="Sätted", compound="left")


        ### Kehade lisamine
        ### Universaalsed keha omadused
        bodyFrame = Frame(book)
        for i, txt in enumerate(("Tüüp", "Nimi", "Värv (RGB)", "Elastsustegur",
                                "Liugehõrdetegur", "Seisuhõõrdetegur")):
            Label(bodyFrame, text=txt).grid(row=i, column=0)

        self.bodyType = ttk.Combobox(bodyFrame, values=["Circle", "Wall"], state="readonly")
        self.entry_name = Entry(bodyFrame)
        
        self.colorFrame = Frame(bodyFrame)
        Spinbox(self.colorFrame, from_=0, to=255, width=4).grid(row=0, column=0, padx=2)
        Spinbox(self.colorFrame, from_=0, to=255, width=4).grid(row=0, column=1, padx=1)
        Spinbox(self.colorFrame, from_=0, to=255, width=4).grid(row=0, column=2, padx=2)
        for widget in self.colorFrame.children.values():
            widget.delete(0,END)
            widget.insert(0,255)
        self.bodyFillBool = BooleanVar()
        Checkbutton(self.colorFrame, text="Täidetud", variable=self.bodyFillBool
                    ).grid(row=1, column=0, columnspan=3)
        
        self.entry_elasticity = Spinbox(bodyFrame, from_=0, to=1, increment=.1)
        self.entry_elasticity.delete(0,END)
        self.entry_elasticity.insert(0,1.0)
        self.entry_fric_kinetic = Spinbox(bodyFrame, from_=0, to=1, increment=.1)
        self.entry_fric_static = Spinbox(bodyFrame, from_=0, to=1, increment=.1)

        ### Ringide omadused
        self.circleAttr = LabelFrame(bodyFrame, text="Circle")
        for i, txt in enumerate(("Mass", "Raadius", "Kordinaadid",
                                "Kiirus", "Kiirendus", "Nurkkiirus")):
            Label(self.circleAttr, text=txt).grid(row=i, column=0)
        self.entry_m = Entry(self.circleAttr)
        self.entry_r = Entry(self.circleAttr)
        self.entry_pos = VectorEntry(self.circleAttr)
        self.entry_v = VectorEntry(self.circleAttr)
        self.entry_a = VectorEntry(self.circleAttr)
        self.entry_w = Entry(self.circleAttr)

        ### Seinte omadused
        self.wallAttr = LabelFrame(bodyFrame, text="Wall")
        Label(self.wallAttr, text="Alguspunkt").grid(row=1, column=0)
        Label(self.wallAttr, text="Lõpppunkt").grid(row=2, column=0)
        self.wallPosAttr = Frame(self.wallAttr)
        self.wallPosVar = StringVar()
        for i, value in enumerate(("N", "E", "S", "W", "muu")):
            Radiobutton(self.wallPosAttr, text=value, value=value, variable=self.wallPosVar,
                        command=self.toggle_wallPosVar).grid(row=0,column=i)
        self.entry_wallPos1 = VectorEntry(self.wallAttr)
        self.entry_wallPos2 = VectorEntry(self.wallAttr)

        Button(bodyFrame, text="Lisa keha", command=self.addBody).grid(row=8)
        book.add(bodyFrame, text="Lisa keha")


        ### Kehade eemaldamine
        bodyListFrame = Frame(book)
        self.treeHeaders = ("Tüüp", "Värv", "Mass", "Kiirus", "Kordinaadid")
        self.tree = ttk.Treeview(bodyListFrame, columns=self.treeHeaders)
        
        self.tree.heading("#0", text="Nimi")
        self.tree.column("#0", width=80)
        for name in self.treeHeaders:
            self.tree.heading(name, text=name)
            self.tree.column(name, width=100)

        Button(bodyListFrame, text="Eemalda keha", command=self.removeBody).grid(row=1, column=0)
        Button(bodyListFrame, text="Uuenda kordinaadid", command=self.updateBodyParameters).grid(row=1, column=1)
        book.add(bodyListFrame, text="Eemalda keha")


        ### Näidised
        examplesTab = Frame(book)
        demoKeys = tuple(demoSettings.keys())
        self.demoType = ttk.Combobox(examplesTab, values=demoKeys, state="readonly")
        Button(examplesTab, text="Vali", command=self.load_demo).grid(row=0, column=1, sticky="new", padx=3, pady=3)
        Button(examplesTab, text="Taasta algseis", command=self.reset).grid(row=0, column=2, sticky="new", padx=3, pady=3)
        book.add(examplesTab, text="Näited")


        ### Paigutamine:
        master.bind("<<ComboboxSelected>>", self.change_body)
        book.bind("<<NotebookTabChanged>>", self.updateBodyParameters)
        topBar.grid(row=0, column=0, sticky="w")
        self.toggle_btn.grid(row=0, column=0, sticky="w", padx=2, pady=2)
        self.debugBox.grid(row=0, column=1, sticky="w", padx=2, pady=2)
        #self.exampleMenu.grid(row=0, column=2, sticky="w", padx=2, pady=2)
        book.grid(row=1, column=0, sticky="new")

        master.columnconfigure(0, weight=1)
        bodyListFrame.columnconfigure(0, weight=1)

        for i, widget in enumerate((self.entry_scrX, self.entry_scrY, self.entry_dt, self.entry_minv,
                                    self.entry_drag, self.entry_g, self.bgFrame, self.entry_trail)):
            widget.grid(row=i, column=1)
        for i, widget in enumerate((self.bodyType, self.entry_name, self.colorFrame,
                                    self.entry_elasticity, self.entry_fric_kinetic, self.entry_fric_static)):
            widget.grid(row=i, column=1)
        for i, widget in enumerate((self.entry_m, self.entry_r, self.entry_pos,
                                   self.entry_v, self.entry_a, self.entry_w)):
            widget.grid(row=i, column=1)
        self.wallPosAttr.grid(row=0, column=0, columnspan=2)
        self.entry_wallPos1.grid(row=1, column=1)
        self.entry_wallPos2.grid(row=2, column=1)

        self.tree.grid(row=0, column=0, columnspan=2, sticky="nesw")
        self.demoType.grid(row=0, column=0, sticky="new", padx=5, pady=6)

        ### Algväärtused
        for widget in ((self.entry_dt, 1), (self.entry_scrX, 600), (self.entry_scrY, 450),
                       (self.entry_minv, 0), (self.entry_drag, 0), (self.entry_trail, 0),
                       (self.entry_m, 1), (self.entry_r, 10), (self.entry_w, 0)):
            widget[0].insert(0, self.defaults[widget[1]] if type(widget[1]) == str else widget[1])

    def change_settings(self):
        wasRunning = self.stopIfRunning()
        e = self.engine
        e.step      = float(self.entry_dt.get())
        e.width     = int(self.entry_scrX.get())
        e.height    = int(self.entry_scrY.get())
        e.velBoundary = float(self.entry_minv.get())
        e.g         = self.entry_g.get()
        e.coef_drag = float(self.entry_drag.get())
        e.bgcolor   = [int(w.get()) for w in self.bgFrame.children.values()]
        e.pathLimit = int(self.entry_trail.get())
        e.screen    = pygame.display.set_mode((e.width, e.height), RESIZABLE)
        if wasRunning:
            self.toggle_running()

    def reset(self):
        wasRunning = self.stopIfRunning()
        for attr, value in self.defaults.items():
            setattr(self.engine, attr, value)
        self.engine.screen = pygame.display.set_mode(
            (self.defaults["width"], self.defaults["height"]), RESIZABLE)
        self.engine.objects = set()
        self.engine.time = 0
        self.tree.delete(*self.tree.get_children())
        self.bodyNames = dict()

    def load_demo(self):
        self.reset()
        demo(self.engine, self.demoType.get())

    def change_body(self, event=None):
        if self.bodyType.get() == "Circle":
            self.wallAttr.grid_forget()
            self.circleAttr.grid(row=7, column=0, columnspan=2, ipadx=2, ipady=2, sticky="nesw")
        elif self.bodyType.get() == "Wall":
            self.circleAttr.grid_forget()
            self.wallAttr.grid(row=7, column=0, columnspan=2, ipadx=2, ipady=2, sticky="nesw")

    def stopIfRunning(self):
        if self.engine.running:
            self.toggle_running()
            return True
        return False

    def getCommonBodyAttributes(self):
        return {
            "name": self.entry_name.get(),
            "color": [int(w.get()) for w in self.colorFrame.children.values() if isinstance(w, Spinbox)],
            "fill": self.bodyFillBool.get(),
            "restitution": float(self.entry_elasticity.get()),
            "staticfriction": float(self.entry_fric_kinetic.get()),
            "dynamicfriction": float(self.entry_fric_static.get())
        }

    def addBody(self):
        bType = self.bodyType.get()
        if not bType:
            return False
        wasRunning = self.stopIfRunning()

        attributes = self.getCommonBodyAttributes()
        name = attributes["name"]
        if not name:
            name = "Nimetu"
        if self.bodyNames.get(name):
            self.bodyNames[name] += 1
            name = "{} ({})".format(name, self.bodyNames[name])
        self.bodyNames[name] = 1
        attributes["name"] = name

        if bType == "Circle":
            attributes.update({
                "m": float(self.entry_m.get()),
                "radius": int(self.entry_r.get()),
                "x": self.entry_pos.get()[0],
                "y": self.entry_pos.get()[1],
                "v": self.entry_v.get(),
                "const_a": self.entry_a.get()
            })
            self.engine.addCircle(**attributes)
        elif bType == "Wall":
            wallPos = self.wallPosVar.get()
            w, h = self.engine.width, self.engine.height
            coords = {"N": {"x1": 0, "y1": 0, "x2": w, "y2": 0},
                    "E": {"x1": w, "y1": 0, "x2": w, "y2": h},
                    "S": {"x1": w, "y1": h, "x2": 0, "y2": h},
                    "W": {"x1": 0, "y1": h, "x2": 0, "y2": 0},
                    "muu":
                    {"x1": self.entry_wallPos1.get()[0],
                    "y1": self.entry_wallPos1.get()[1],
                    "x2": self.entry_wallPos2.get()[0],
                    "y2": self.entry_wallPos2.get()[1]}}[wallPos]
            attributes.update(coords)
            self.engine.addWall(**attributes)

        self.tree.insert("", "end", name, text=name)
        if wasRunning:
            self.toggle_running()

    def removeBody(self):
        wasRunning = self.stopIfRunning()
        removeNames = list(self.tree.selection())
        toDiscard = set()
        for obj in self.engine.objects:
            if not removeNames:
                break
            if obj.name in removeNames:
                toDiscard.add(obj)
                removeNames.remove(obj.name)
                self.tree.delete(obj.name)
                del self.bodyNames[obj.name]
        self.engine.objects -= toDiscard
        if wasRunning:
            self.toggle_running()

    def updateBodyParameters(self, event=None):
        for b in self.engine.objects:
            color = str(b.color)[1:-1]
            if isinstance(b, Circle):
                pos = (int(b.x), int(b.y))
                v = "(%.1f, %.1f)" % b.v
            elif isinstance(b, Wall):
                pos = ((int(b.x1), int(b.y1)), (int(b.x2), int(b.y2)))
                v = " - "
            if not self.tree.exists(b.name):
                self.tree.insert("", "end", b.name, text=b.name)
                self.bodyNames[b.name] = 1
                
            for options in zip(self.treeHeaders, (type(b).__name__, color, b.m, v, pos)):
                self.tree.set(b.name, options[0], value=options[1])

    def toggle_wallPosVar(self):
        widgets = self.entry_wallPos1.children
        widgets.update(self.entry_wallPos2.children)
        newState = DISABLED
        if self.wallPosVar.get() == "muu":
            newState = NORMAL
        for w in widgets.values():
            w.config(state=newState)

    def toggle_running(self, event=None):
        if self.engine.running:
            self.engine.stop()
            self.simThread.join()
            del self.simThread
            self.toggle_btn.config(text="start", image=self.img[0])
        else:
            self.simThread = Thread(target=self.engine.start)
            self.master.after_idle(self.simThread.start)
            self.toggle_btn.config(text="stop", image=self.img[1])

##    def toggle_pause(self, event=None):
##        lbl = "pause" if self.engine.pause else "unpause"
##        self.engine.togglePause()
##        self.topmenu.entryconfigure(2, label=lbl)

    def toggle_debug(self):
        self.engine.debug = not self.engine.debug

root = Tk()
Simulator(root, Engine(width=300, height=220))
root.mainloop()
pygame.quit()
