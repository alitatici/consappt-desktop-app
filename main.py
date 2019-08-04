from tkinter import *
from tkinter import ttk
from ui_components.canvas import CanvasWall
from beam import *
from ttkthemes import themed_tk as tk
from calculations import *
from calculationOfOneHorizontal import *
from calculationOfTwoHorizontal import *
import math

class Window:

    def donothing(self):
        filewin = Toplevel(self.root)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    def controlH1EntryState(self):
        if self.hh1Active.get() == 1:
            self.hh1Thickness.config(state="enabled")
            self.hh1Location.config(state="enabled")
            self.hh2State.configure(state="normal")
            self.designFrame.setH1Active()
        else:
            self.hh1Thickness.config(state="disabled")
            self.hh1Location.config(state="disabled")
            self.hh2State.configure(state="disabled")
            self.designFrame.setH1Passive()
            self.designFrame.setH2Passive()

    def controlH2EntryState(self):
        if self.hh2Active.get() == 1:
            self.hh2Thickness.config(state="enabled")
            self.hh2Location.config(state="enabled")
            self.designFrame.setH2Active()
        else:
            self.hh2Thickness.config(state="disabled")
            self.hh2Location.config(state="disabled")
            self.designFrame.setH2Passive()


    def func(self, evt):
        self.designFrame.set_verticalHatilPos(float(self.vhLocation.get()))
        self.designFrame.set_verticalHatilThickness(float(self.vhThickness.get())/100)
        if self.hh1Active.get() == 1:
            self.designFrame.set_hh1Pos(float(self.hh1Location.get()))
            self.designFrame.set_hh1Thickness(float(self.hh1Thickness.get())/100)
        if self.hh2Active.get() == 1:
            self.designFrame.set_hh2Pos(float(self.hh2Location.get()))
            self.designFrame.set_hh2Thickness(float(self.hh2Thickness.get())/100)            
        self.designFrame.set_wallHeight(float(self.vhLength.get()))
        self.designFrame.set_wallWidth(float(self.wallWidth.get()))
        cdX = float(self.wallWidth.get())/float(self.vhLength.get())
        if cdX > 1.5:
            self.designFrame.set_zoom(8/float(self.wallWidth.get())*8)
            self.var.set((8/float(self.wallWidth.get())*8)*10)

        else:
            self.designFrame.set_zoom(4.5/float(self.vhLength.get())*8)
            self.var.set((4/float(self.vhLength.get())*8)*10)


    def zoom(self, evt):
        self.designFrame.set_zoom(self.var.get()/10)

    def calculateProblem(self):
        self.wall = Wall(float(self.wallThickness.get()), float(self.wallDensity.get()), float(self.wallWidth.get()))
        self.verticalHatil = VerticalHatil(float(self.vhThickness.get()), float(self.vhLocation.get()), float(self.vhLength.get()))
        self.concrete = Concrete(self.concreteVariable.get())
        self.steel = ReinforcementSteel(self.steelVariable.get(), self.longitudinalVariable.get(), self.stirrupVariable.get(), int(self.distanceVariable.get()))
        self.plaster = Plaster(float(self.pThickness.get()), float(self.pDensity.get()))
        self.earthquake = Earthquake(float(self.eA0.get()), float(self.eI.get()))
        self.reinforcedConcreteDensity = ReinforcedConcreteDensity()
        self.concreteCover = ConcreteCover(float(self.ccT.get()))
        self.heightParameter = HeightParameter(float(self.hpFromBasement.get()), float(self.hpMax.get()))
        if self.hh2Active.get() == 1:
            self.horizontalHatil1 = HorizontalHatil(float(self.hh1Thickness.get()), float(self.hh1Location.get()))
            self.horizontalHatil2 = HorizontalHatil(float(self.hh2Thickness.get()), float(self.hh2Location.get()))
            calculator3 = GeneralCalculatorForTwoHorizontal()
            string = calculator3.calculateTwoHorizontal(self.verticalHatil, self.horizontalHatil1, self.horizontalHatil2, self.concrete, self.steel, self.wall, self.plaster,
            self.earthquake, self.reinforcedConcreteDensity, self.concreteCover, self.heightParameter)
        elif self.hh1Active.get() == 1:
            self.horizontalHatil1 = HorizontalHatil(float(self.hh1Thickness.get()), float(self.hh1Location.get()))
            calculator2 = GeneralCalculatorForOneHorizontal()
            string = calculator2.calculateOneHorizontal(self.verticalHatil, self.horizontalHatil1, self.concrete, self.steel, self.wall, self.plaster,
            self.earthquake, self.reinforcedConcreteDensity, self.concreteCover, self.heightParameter)
        else:
            calculator = GeneralCalculator()
            string = calculator.calculateNonHorizontal(self.verticalHatil, self.concrete, self.steel, self.wall, self.plaster,
            self.earthquake, self.reinforcedConcreteDensity, self.concreteCover, self.heightParameter)
        self.resultBox.delete(0, END)
        self.resultBox.insert(INSERT, string[0])
        self.T.delete("1.0", END)
        self.T.insert(END, string[1])



    def __init__(self):
            self.root = tk.ThemedTk()
            self.root.get_themes()
            self.root.set_theme("equilux")
            self.root.configure(bg="#383838")
            self.root.iconbitmap('consappt.ico')

            self.toolbar = ttk.Frame(self.root, borderwidth=1, relief=RAISED)

            self.reportDocButton = ttk.Button(self.toolbar, text="Create Report Document",
            command=self.root.quit)
            self.reportDocButton.grid(row= 0, column=0, sticky=(W,E,S,N))

            self.drawCADButton = ttk.Button(self.toolbar, text="Create AutoCAD Sketch",
            command=self.root.quit)
            self.drawCADButton.grid(row= 0, column=1, sticky=(W,E,S,N))

            self.toolbar.grid(row=0, column=0)

            self.designFrame = CanvasWall()


            # SETTINGS ENTRY

            self.settingsEntry = ttk.Frame(self.root)
            self.settingsEntry.grid(row =0, column = 1, sticky=E)

            ttk.Label(self.settingsEntry, text=" Zoom:").grid(row =1, column = 0, columnspan=2, sticky=(W,E))

            self.var = DoubleVar()
            self.var.set(50)
            self.settingsZoom = ttk.Scale(self.settingsEntry, variable = self.var, orient=HORIZONTAL, length=200, from_=1.0, to=100.0)
            self.root.bind("<ButtonRelease-1>", self.zoom)
 

            self.settingsZoom.grid(row=1, column=2, columnspan=2)

            # EARTHQUAKE ENTRY

            self.earthquakeEntry = ttk.LabelFrame(self.root, text="Earthquake")
            self.earthquakeEntry.grid(row =1, column =0, sticky=(W,E))

            ttk.Label(self.earthquakeEntry, text=" A0:").grid(row =1, column = 0, columnspan=2,  sticky=W)
            ttk.Label(self.earthquakeEntry, text=" I:").grid(row =1, column = 4, columnspan=2, sticky=W)

            self.eA0 = ttk.Entry(self.earthquakeEntry)
            self.eA0.insert(END, "0.4")
            self.eI = ttk.Entry(self.earthquakeEntry)
            self.eI.insert(END, "1")

            self.eA0.grid(row=1, column=2, columnspan=2)
            self.eI.grid(row=1, column=6, columnspan=2)

            # HEIGHT PARAMETER ENTRY

            self.heightParameterEntry = ttk.LabelFrame(self.root, text="Height Parameter")
            self.heightParameterEntry.grid(row =2, column = 0, sticky=(W,E))

            ttk.Label(self.heightParameterEntry, text=" From Basement(m):").grid(row = 0, column = 0,  sticky=W)
            ttk.Label(self.heightParameterEntry, text=" Max(m):").grid(row =0, column = 4, sticky=W)

            self.hpFromBasement = ttk.Entry(self.heightParameterEntry)
            self.hpFromBasement.insert(END, "-5")
            self.hpMax = ttk.Entry(self.heightParameterEntry)
            self.hpMax.insert(END, "10")

            self.hpFromBasement.grid(row=0, column=2, sticky=W)
            self.hpMax.grid(row=0, column=6, sticky=W)

            self.tripleFrameContainer = ttk.Frame(self.root)
            self.tripleFrameContainer.grid(row =3, column = 0, sticky=(W,E))


            # CONCRETE ENTRY

            self.concreteEntry = ttk.LabelFrame(self.tripleFrameContainer, text="Concrete")
            self.concreteEntry.grid(row =0, column = 0, sticky=(W,E))

            OPTIONS_FOR_CONCRETE = [
                "C20",
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
            ttk.Label(self.concreteEntry, text=" Type:").grid(row =1, column = 0, columnspan=2,  sticky=(W,E))

            self.concreteMenu = ttk.OptionMenu(self.concreteEntry, self.concreteVariable, *OPTIONS_FOR_CONCRETE)

            self.concreteMenu.grid(row=1, column=2, columnspan=2)


            # STEEL ENTRY

            self.steelEntry = ttk.LabelFrame(self.tripleFrameContainer, text="Steel")
            self.steelEntry.grid(row =0, column = 1, sticky=(W,E))

            OPTIONS_FOR_STEEL = [
                "S220",
                "S220",
                "S420",
                "S500"
                ]

            self.steelVariable = StringVar(self.root)
            self.steelVariable.set(OPTIONS_FOR_STEEL[0])
            ttk.Label(self.steelEntry, text=" Type:").grid(row =1, column = 0,  sticky=(W,E))

            self.steelMenu = ttk.OptionMenu(self.steelEntry, self.steelVariable, *OPTIONS_FOR_STEEL)

            self.steelMenu.grid(row=1, column=1)


            # CONCRETE COVER ENTRY

            self.concreteCoverEntry = ttk.LabelFrame(self.tripleFrameContainer, text="Concrete Cover")
            self.concreteCoverEntry.grid(row =0, column = 2, sticky=(W,E))

            ttk.Label(self.concreteCoverEntry, text=" Cover Thickness(cm):").grid(row =1, column = 0, columnspan=2,  sticky=W)

            self.ccT = ttk.Entry(self.concreteCoverEntry)
            self.ccT.insert(END, "3")

            self.ccT.grid(row=1, column=2, columnspan=2)


            # WALL ENTRY

            self.wallEntry = ttk.LabelFrame(self.root, text="Wall")
            self.wallEntry.grid(row =4, column = 0, sticky=(W,E))

            ttk.Label(self.wallEntry, text=" Thickness(cm):").grid(row =1, column = 0, columnspan=2, sticky=(W,E))
            ttk.Label(self.wallEntry, text=" Density(t/m³):").grid(row =1, column = 4, columnspan=2, sticky=(W,E))
            ttk.Label(self.wallEntry, text=" Width(m):").grid(row =1, column = 8, columnspan=2, sticky=(W,E))
            ttk.Label(self.wallEntry, text=" Length(m):").grid(row =1, column = 12, columnspan=2, sticky=(W,E))

            self.wallThickness = ttk.Entry(self.wallEntry)
            self.wallThickness.insert(END, "22.5")
            self.wallDensity = ttk.Entry(self.wallEntry)
            self.wallDensity.insert(END, "0.5")
            self.wallWidth = ttk.Entry(self.wallEntry)
            self.wallWidth.insert(END, "8.2")
            self.vhLength = ttk.Entry(self.wallEntry)
            self.vhLength.insert(END, "4")

            self.wallThickness.grid(row=1, column=2, columnspan=2)
            self.wallDensity.grid(row=1, column=6, columnspan=2)
            self.wallWidth.grid(row=1, column=10, columnspan=2)
            self.vhLength.grid(row=1, column=14, columnspan=2)


            # PLASTER ENTRY

            self.plasterEntry = ttk.LabelFrame(self.root, text="Plaster")
            self.plasterEntry.grid(row =5, column = 0, sticky=(W,E))

            ttk.Label(self.plasterEntry, text=" Thickness(cm):").grid(row =1, column = 0, columnspan=2,  sticky=W)
            ttk.Label(self.plasterEntry, text=" Density(t/m³):").grid(row =1, column = 4, columnspan=2, sticky=W)

            self.pThickness = ttk.Entry(self.plasterEntry)
            self.pThickness.insert(END, "2")
            self.pDensity = ttk.Entry(self.plasterEntry)
            self.pDensity.insert(END, "1.8")

            self.pThickness.grid(row=1, column=2, columnspan=2)
            self.pDensity.grid(row=1, column=6, columnspan=2)


            # VERTICAL HATIL ENTRY

            self.verticalHatilEntry = ttk.LabelFrame(self.root, text="Vertical Hatıl")
            self.verticalHatilEntry.grid(row =6, column = 0, sticky=(W,E))

            ttk.Label(self.verticalHatilEntry, text=" Thickness(cm):").grid(row =1, column = 0, columnspan=2,  sticky=(W,E))
            ttk.Label(self.verticalHatilEntry, text=" Location(m):").grid(row =1, column = 4, columnspan=2, sticky=(W,E))
            

            self.vhThickness = ttk.Entry(self.verticalHatilEntry)
            self.vhThickness.insert(END, "20")
            self.vhLocation = ttk.Entry(self.verticalHatilEntry)
            self.vhLocation.insert(END, "4.1")


            self.vhThickness.grid(row=1, column=2, columnspan=2)
            self.vhLocation.grid(row=1, column=6, columnspan=2)


            # HORIZONTAL HATIL 1 ENTRY

            self.horizontalHatil1Entry = ttk.LabelFrame(self.root, text="Horizontal Hatıl I")
            self.horizontalHatil1Entry.grid(row =7, column = 0, sticky=(W,E))

            ttk.Label(self.horizontalHatil1Entry, text=" Thickness(cm):").grid(row =1, column = 1, columnspan=2,  sticky=(W,E))
            ttk.Label(self.horizontalHatil1Entry, text=" Location(m):").grid(row =1, column = 5, columnspan=2, sticky=(W,E))

            self.hh1Thickness = ttk.Entry(self.horizontalHatil1Entry, state="disabled")
            self.hh1Thickness.insert(END, "20")
            self.hh1Location = ttk.Entry(self.horizontalHatil1Entry, state="disabled")
            self.hh1Location.insert(END, "4.1")

            self.hh1Active = IntVar()
            self.hh1State= ttk.Checkbutton(self.horizontalHatil1Entry, text="Add",
             variable=self.hh1Active, command=self.controlH1EntryState).grid(row=1, column = 0, sticky=W)

            self.hh1Thickness.grid(row=1, column=3, columnspan=2)
            self.hh1Location.grid(row=1, column=7, columnspan=2)


            # HORIZONTAL HATIL 2 ENTRY

            self.horizontalHatil2Entry = ttk.LabelFrame(self.root, text="Horizontal Hatıl II")
            self.horizontalHatil2Entry.grid(row =8, column = 0, sticky=(W,E))

            ttk.Label(self.horizontalHatil2Entry, text=" Thickness(cm):").grid(row =1, column = 1, columnspan=2,  sticky=(W,E))
            ttk.Label(self.horizontalHatil2Entry, text=" Location(m):").grid(row =1, column = 5, columnspan=2, sticky=(W,E))


            self.hh2Thickness = ttk.Entry(self.horizontalHatil2Entry, state="disabled")
            self.hh2Thickness.insert(END, "20")
            self.hh2Location = ttk.Entry(self.horizontalHatil2Entry, state="disabled")
            self.hh2Location.insert(END, "4.1")

            self.hh2Active = IntVar()
            self.hh2State = ttk.Checkbutton(self.horizontalHatil2Entry, text="Add", variable=self.hh2Active,
             command=self.controlH2EntryState, state="disabled")

            self.hh2State.grid(row=1, column = 0, sticky=W)
            self.hh2Thickness.grid(row=1, column=3, columnspan=2)
            self.hh2Location.grid(row=1, column=7, columnspan=2)

            # MINIMUM VALUES OF REINFORCEMENTs
            self.minValReinforcementEntry = ttk.LabelFrame(self.root, text="Minimum Values of Reinforcement")
            self.minValReinforcementEntry.grid(row =9, column = 0, sticky=(W,E))

            OPTIONS_FOR_LONGITUDINAL = [
                "ø8",
                "ø8",
                "ø10",
                "ø12",
                "ø14",
                "ø16"
                ]

            OPTIONS_FOR_STIRRUP = [
                "ø8",
                "ø8",
                "ø10",
                "ø12",
                "ø14",
                "ø16"
                ]

            OPTIONS_FOR_DISTANCE = [
                "8",
                "8",
                "10",
                "12",
                "14",
                "16",
                "18",
                "20",
                "22",
                "24",
                ]

            self.longitudinalVariable = StringVar(self.root)
            self.longitudinalVariable.set(OPTIONS_FOR_LONGITUDINAL[0])
            ttk.Label(self.minValReinforcementEntry, text=" Longitudinal:").grid(row =1, column = 0,  sticky=(W,E))

            self.longitudinalMenu = ttk.OptionMenu(self.minValReinforcementEntry, self.longitudinalVariable, *OPTIONS_FOR_LONGITUDINAL)


            self.stirrupVariable = StringVar(self.root)
            self.stirrupVariable.set(OPTIONS_FOR_STIRRUP[0])
            ttk.Label(self.minValReinforcementEntry, text=" Stirrup:").grid(row =1, column = 2,  sticky=(W,E))

            self.stirrupMenu = ttk.OptionMenu(self.minValReinforcementEntry, self.stirrupVariable, *OPTIONS_FOR_STIRRUP)

            self.distanceVariable = StringVar(self.root)
            self.distanceVariable.set(OPTIONS_FOR_DISTANCE[0])
            ttk.Label(self.minValReinforcementEntry, text=" Distance Between Stirrups(cm):").grid(row =1, column = 4,  sticky=(W,E))

            self.distanceMenu = ttk.OptionMenu(self.minValReinforcementEntry, self.distanceVariable, *OPTIONS_FOR_DISTANCE)
            
            
            self.longitudinalMenu.grid(row=1, column=1)
            self.stirrupMenu.grid(row = 1, column=3)
            self.distanceMenu.grid(row = 1, column=5)

            # CALCULATE - RESULT AREA

            self.calculateResultFrame = ttk.LabelFrame(self.root, text="Calculation")
            self.calculateResultFrame.grid(row = 11, column = 0, sticky=(W,E))


            ttk.Button(self.calculateResultFrame, text="Calculate Problem", command = self.calculateProblem).grid(row =0, column = 0, columnspan=2,  sticky=W)

            self.resultAreaFrame =ttk.Frame(self.calculateResultFrame)
            self.resultAreaFrame.grid(row =1, column = 0, columnspan = 10, sticky=(W,E))
            self.S = ttk.Scrollbar(self.resultAreaFrame)
            self.T = Text(self.resultAreaFrame, height=8, width=90)
            self.T.tag_add("here", "1.0", "1.4")
            self.T.tag_config("here", background="black", foreground="green")
            self.S.pack(side=RIGHT, fill=Y)
            self.T.pack(side=LEFT, fill=Y)
            self.S.config(command=self.T.yview)
            self.T.config(yscrollcommand=self.S.set)
            self.T.configure(background="#414141", fg="white")
            self.T.insert(END, "result...")


            self.resultBox = ttk.Entry(self.calculateResultFrame)
            self.resultBox.insert(END, "result...")

            self.resultBox.grid(row=0, column=2, columnspan=2)
            self.hpMax.grid(row=0, column=6, columnspan=2)

            self.root.bind("<KeyRelease>", self.func)
            self.root.mainloop()

def main():
    w = Window()

if __name__ == '__main__':
    main()
