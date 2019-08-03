from beam import *
import math
	
class GeneralCalculatorForOneHorizontal:

    def __init__(self):
        print("calculatorOneHorizontal Initialized")
        self.calculatedValues = CalculatedValues()
        self.verticalHatil = None
        self.horizontalHatil = None
        self.concrete = None
        self.steel = None
        self.wall = None
        self.plaster = None
        self.earthquake = None
        self.reinforcedConcreteDensity = None
        self.concreteCover = None
        self.calculatedValues = None
        self.heightParameter = None
        self.report = ""

    def calculateOneHorizontal(self, verticalHatil, horizontalHatil, concrete, steel, wall,
    plaster, earthquake, reinforcedConcreteDensity, concreteCover, heightParameter):
        self.verticalHatil = verticalHatil
        self.horizontalHatil = horizontalHatil
        self.concrete = concrete
        self.steel = steel
        self.wall = wall
        self.plaster = plaster
        self.earthquake = earthquake
        self.reinforcedConcreteDensity = reinforcedConcreteDensity
        self.concreteCover = concreteCover
        self.heightParameter = heightParameter
        
        self.calculateWallWeightPerUnitArea()
        # self.calculateWallWeightPerMeter()
        # self.calculateWallLinearWeight()
        # self.calculateLinearEquivalentEarthquakeLoad()
        # self.calculateMomentAndShearForce()
        # self.calculateDeflectionOfHorizontalHatil()
        # self.calculateDeflectionOfVerticalHatil()
        # self.calculateNecessaryReinforcementAreaHorizontalHatil()
        # self.calculateNecessaryReinforcementAreaVerticalHatil()
        # self.calculateShearStirrupsOfHorizontalHatil()
        # self.calculateShearStirrupsOfVerticalHatil()
        print(self.report)

    #weight per unit area of wall; plaster multiple with 2 beacuse of plaster uses both sides of wall. Result unit: t/m^2
    def calculateWallWeightPerUnitArea(self):
        self.calculatedValues.wallWeightPerUnitArea = round(((self.wall.thickness/100) * self.wall.density + 2*(self.plaster.thickness/100) * self.plaster.density), 3)
        #print(self.calculatedValues.wallWeightPerUnitArea)
        self.report += "Weight per unit area of wall: "+ str(self.calculatedValues.wallWeightPerUnitArea) + " t/m^2.\n"