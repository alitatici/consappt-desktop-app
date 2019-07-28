from tkinter import *
from tkinter import ttk
from ui_components.canvas import CanvasWall
from beam import *
from calculations import *
import math




class Window:

    def donothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def func(self, evt):
        self.designFrame.set_verticalHatilPos(float(self.vhLocation.get()))
        self.designFrame.set_wallHeight(float(self.vhLength.get()))
        self.designFrame.set_wallWidth(float(self.wallWidth.get()))

    def zoom(self, evt):
        self.designFrame.set_zoom(self.var.get()/10)

    def calculateProblem(self):
        self.wall = Wall(float(self.wallThickness.get()), float(self.wallDensity.get()), float(self.wallWidth.get()))
        self.verticalHatil = VerticalHatil(float(self.vhThickness.get()), float(self.vhLocation.get()), float(self.vhLength.get()))
        self.concrete = Concrete(self.concreteVariable.get())
        self.steel = ReinforcementSteel(self.steelVariable.get())
        self.plaster = Plaster(float(self.pThickness.get()), float(self.pDensity.get()))
        self.earthquake = Earthquake(float(self.eA0.get()), float(self.eI.get()))
        self.reinforcedConcreteDensity = ReinforcedConcreteDensity()
        self.concreteCover = ConcreteCover(float(self.ccT.get()))
        self.heightParameter = HeightParameter(float(self.hpFromBasement.get()), float(self.hpMax.get()))
        calculator = GeneralCalculator()
        string = calculator.calculateNonHorizontal(self.verticalHatil, self.concrete, self.steel, self.wall, self.plaster,
        self.earthquake, self.reinforcedConcreteDensity, self.concreteCover)
        self.resultBox.delete(0, END)
        self.resultBox.insert(INSERT, string)



    def __init__(self):
            self.root = Tk()

            self.menubar = Menu(self.root)
            self.filemenu = Menu(self.menubar, tearoff=0)
            self.filemenu.add_command(label="New", command=self.donothing)
            self.filemenu.add_command(label="Open", command=self.donothing)
            self.filemenu.add_command(label="Save", command=self.donothing)
            self.filemenu.add_command(label="Save as...", command=self.donothing)
            self.filemenu.add_command(label="Close", command=self.donothing)

            self.filemenu.add_separator()

            self.filemenu.add_command(label="Exit", command=self.root.quit)
            self.menubar.add_cascade(label="File", menu=self.filemenu)
            self.editmenu = Menu(self.menubar, tearoff=0)
            self.editmenu.add_command(label="Undo", command=self.donothing)

            self.editmenu.add_separator()

            self.editmenu.add_command(label="Cut", command=self.donothing)
            self.editmenu.add_command(label="Copy", command=self.donothing)
            self.editmenu.add_command(label="Paste", command=self.donothing)
            self.editmenu.add_command(label="Delete", command=self.donothing)
            self.editmenu.add_command(label="Select All", command=self.donothing)

            self.menubar.add_cascade(label="Edit", menu=self.editmenu)
            self.helpmenu = Menu(self.menubar, tearoff=0)
            self.helpmenu.add_command(label="Help Index", command=self.donothing)
            self.helpmenu.add_command(label="About...", command=self.donothing)
            self.menubar.add_cascade(label="Help", menu=self.helpmenu)

            self.designFrame = CanvasWall()


            # SETTINGS ENTRY

            self.settingsEntry = LabelFrame(self.root, text="Settings")
            self.settingsEntry.grid(row =0, column = 3, sticky=W)

            Label(self.settingsEntry, text="Zoom").grid(row =1, column = 0, columnspan=2, sticky=W)

            self.var = DoubleVar()
            self.settingsZoom = Scale(self.settingsEntry, variable = self.var, orient=HORIZONTAL, length=200, from_=1.0, to=100.0)
            self.root.bind("<ButtonRelease-1>", self.zoom)
 

            self.settingsZoom.grid(row=1, column=2, columnspan=2)


            # WALL ENTRY

            self.wallEntry = LabelFrame(self.root, text="Wall")
            self.wallEntry.grid(row =1, column = 3, sticky=W)

            Label(self.wallEntry, text="Thickness").grid(row =1, column = 0, columnspan=2, sticky=W)
            Label(self.wallEntry, text="Density").grid(row =1, column = 4, columnspan=2, sticky=W)
            Label(self.wallEntry, text="Width").grid(row =1, column = 8, columnspan=2, sticky=W)

            self.wallThickness = Entry(self.wallEntry)
            self.wallThickness.insert(END, "22.5")
            self.wallDensity = Entry(self.wallEntry)
            self.wallDensity.insert(END, "0.5")
            self.wallWidth = Entry(self.wallEntry)
            self.wallWidth.insert(END, "8.2")

            self.wallThickness.grid(row=1, column=2, columnspan=2)
            self.wallDensity.grid(row=1, column=6, columnspan=2)
            self.wallWidth.grid(row=1, column=10, columnspan=2)

            # VERTICAL HATIL ENTRY

            self.verticalHatilEntry = LabelFrame(self.root, text="Vertical Hatıl")
            self.verticalHatilEntry.grid(row =2, column = 3, sticky=W)

            Label(self.verticalHatilEntry, text="Thickness").grid(row =1, column = 0, columnspan=2,  sticky=W)
            Label(self.verticalHatilEntry, text="Location").grid(row =1, column = 4, columnspan=2, sticky=W)
            Label(self.verticalHatilEntry, text="Length").grid(row =1, column = 8, columnspan=2, sticky=W)

            self.vhThickness = Entry(self.verticalHatilEntry)
            self.vhThickness.insert(END, "20")
            self.vhLocation = Entry(self.verticalHatilEntry)
            self.vhLocation.insert(END, "4.1")
            self.vhLength = Entry(self.verticalHatilEntry)
            self.vhLength.insert(END, "4")

            self.vhThickness.grid(row=1, column=2, columnspan=2)
            self.vhLocation.grid(row=1, column=6, columnspan=2)
            self.vhLength.grid(row=1, column=10, columnspan=2)

            # CONCRETE ENTRY

            self.concreteEntry = LabelFrame(self.root, text="Concrete")
            self.concreteEntry.grid(row =3, column = 3, sticky=W)

            OPTIONS_FOR_CONCRETE = [
                "C20",
                "C25",
                "C30",
                "C35",
                "C40",
                "C45",
                "C50",
                ]

            self.concreteVariable = StringVar(self.root)
            self.concreteVariable.set(OPTIONS_FOR_CONCRETE[0])
            Label(self.concreteEntry, text="Type").grid(row =1, column = 0, columnspan=2,  sticky=W)

            self.concreteMenu = OptionMenu(self.concreteEntry, self.concreteVariable, *OPTIONS_FOR_CONCRETE)

            self.concreteMenu.grid(row=1, column=2, columnspan=2)


            # STEEL ENTRY

            self.steelEntry = LabelFrame(self.root, text="Steel")
            self.steelEntry.grid(row =4, column = 3, sticky=W)

            OPTIONS_FOR_STEEL = [
                "S220",
                "S420",
                "S500"
                ]

            self.steelVariable = StringVar(self.root)
            self.steelVariable.set(OPTIONS_FOR_STEEL[0])
            Label(self.steelEntry, text="Type").grid(row =1, column = 0, columnspan=2,  sticky=W)

            self.steelMenu = OptionMenu(self.steelEntry, self.steelVariable, *OPTIONS_FOR_STEEL)

            self.steelMenu.grid(row=1, column=2, columnspan=2)

            # PLASTER ENTRY

            self.plasterEntry = LabelFrame(self.root, text="Plaster")
            self.plasterEntry.grid(row =5, column = 3, sticky=W)

            Label(self.plasterEntry, text="Thickness").grid(row =1, column = 0, columnspan=2,  sticky=W)
            Label(self.plasterEntry, text="Density").grid(row =1, column = 4, columnspan=2, sticky=W)

            self.pThickness = Entry(self.plasterEntry)
            self.pThickness.insert(END, "2")
            self.pDensity = Entry(self.plasterEntry)
            self.pDensity.insert(END, "1.8")

            self.pThickness.grid(row=1, column=2, columnspan=2)
            self.pDensity.grid(row=1, column=6, columnspan=2)


            # EARTHQUAKE ENTRY

            self.earthquakeEntry = LabelFrame(self.root, text="Earthquake")
            self.earthquakeEntry.grid(row =6, column = 3, sticky=W)

            Label(self.earthquakeEntry, text="A0").grid(row =1, column = 0, columnspan=2,  sticky=W)
            Label(self.earthquakeEntry, text="I").grid(row =1, column = 4, columnspan=2, sticky=W)

            self.eA0 = Entry(self.earthquakeEntry)
            self.eA0.insert(END, "0.4")
            self.eI = Entry(self.earthquakeEntry)
            self.eI.insert(END, "1")

            self.eA0.grid(row=1, column=2, columnspan=2)
            self.eI.grid(row=1, column=6, columnspan=2)

            # CONCRETE COVER ENTRY

            self.concreteCoverEntry = LabelFrame(self.root, text="Concrete Cover")
            self.concreteCoverEntry.grid(row =7, column = 3, sticky=W)

            Label(self.concreteCoverEntry, text="Cover Thickness").grid(row =1, column = 0, columnspan=2,  sticky=W)

            self.ccT = Entry(self.concreteCoverEntry)
            self.ccT.insert(END, "3")

            self.ccT.grid(row=1, column=2, columnspan=2)


            # HEIGHT PARAMETER ENTRY

            self.heightParameterEntry = LabelFrame(self.root, text="Height Parameter")
            self.heightParameterEntry.grid(row =8, column = 3, sticky=W)

            Label(self.heightParameterEntry, text="From Basement").grid(row =1, column = 0, columnspan=2,  sticky=W)
            Label(self.heightParameterEntry, text="Max").grid(row =1, column = 4, columnspan=2, sticky=W)

            self.hpFromBasement = Entry(self.heightParameterEntry)
            self.hpFromBasement.insert(END, "-5")
            self.hpMax = Entry(self.heightParameterEntry)
            self.hpMax.insert(END, "10")

            self.hpFromBasement.grid(row=1, column=2, columnspan=2)
            self.hpMax.grid(row=1, column=6, columnspan=2)

            # CALCULATE - RESULT AREA

            self.calculateResultFrame = LabelFrame(self.root, text="Calculation")
            self.calculateResultFrame.grid(row =9, column = 3, sticky=W)


            Button(self.calculateResultFrame, text="Calculate Problem", command = self.calculateProblem).grid(row =1, column = 0, columnspan=2,  sticky=W)


            self.resultBox = Entry(self.calculateResultFrame)
            self.resultBox.insert(END, "result...")

            self.resultBox.grid(row=1, column=2, columnspan=2)
            self.hpMax.grid(row=1, column=6, columnspan=2)

            self.root.bind("<KeyRelease>", self.func)
            self.root.config(menu=self.menubar)
            self.root.mainloop()

def main():
    w = Window()

if __name__ == '__main__':
    main()
