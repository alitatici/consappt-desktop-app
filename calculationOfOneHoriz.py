from beam import *
import math

class GeneralCalculator:
    verticalHatil = None
    HorizontalHatil = None
    concrete = None
    steel = None
    wall = None
    plaster = None
    earthquake = None
    reinforcedConcreteDensity = None
    concreteCover = None
    calculatedValues = None
    

    def __init__(self):
        print("Calculator Initialized")
        self.calculatedValues = CalculatedValues()
    def calculateOneHorizontal(self, VerticalHatil, HorizontalHatil, concrete, steel, wall,
     plaster, earthquake, reinforcedConcreteDensity, concreteCover):
        self.verticalHatil = verticalHatil
        self.HorizontalHatil = HorizontalHatil
        self.concrete = concrete
        self.steel = steel
        self.wall = wall,
        self.plaster = plaster,
        self.earthquake = earthquake
        self.reinforcedConcreteDensity = reinforcedConcreteDensity
        self.concreteCover = concreteCover

        self.calculateWallWeightPerUnitArea()
        self.calculateWallWeightPerMeter()
        #self.calculateWallLinearWeight()
        #self.calculateLinearEquivalentEarthquakeLoad()
        #self.calculateMomentAndShearForce()
        #self.calculateDeflection()
        #self.calculateNecessaryReinforcementArea()
        #self.calculateShearStirrups()

#weight per unit area of wall; plaster multiple with 2 beacuse of plaster uses both sides of wall. Result unit: t/m^2
    def calculateWallWeightPerUnitArea(self):
        self.calculatedValues.wallWeightPerUnitArea = (wall.thickness/100) * wall.density + 2*(plaster.thickness/100) * plaster.density
        print(self.calculatedValues.wallWeightPerUnitArea)

#Weight per meter of wall. Result unit: t/m. 
#This value must be lower than 0.7 t/m.
    def calculateWallWeightPerMeter(self):
        load = (wall.width - verticalHatil.thickness/100) * (verticalHatil.length - HorizontalHatil.thickness/100) * self.calculatedValues.wallWeightPerUnitArea
        load += verticalHatil.thickness/100 * wall.thickness/100 * verticalHatil.length * reinforcedConcreteDensity.reinforcedConcreteDensity
        load += HorizontalHatil.thickness/100 * wall.thickness/100 * (wall.width - verticalHatil.thickness/100) * reinforcedConcreteDensity.reinforcedConcreteDensity
        if load / wall.width > 0.7:
            print("need support to bottom of wall. (>700kg/m)")
        else:
            print("ok. (<700 kg/m")

#Calculation of We. Horizontal hatil's loads from wall and itself. Result unit: t/m
    #def calculateWallLinearWeight(self):
        #temp = (verticalHatil.thickness/100)
        #temp *= (wall.thickness/100)
        #temp *= reinforcedConcreteDensity.reinforcedConcreteDensity
        #temp += ((wall.width - verticalHatil.thickness/100)/2) * self.calculatedValues.wallWeightPerUnitArea
        #self.calculatedValues.wallLinearWeight = temp
        #print(self.calculatedValues.wallLinearWeight)


verticalHatil = VerticalHatil(20, 4, 5)
HorizontalHatil = HorizontalHatil(20, 2.2)
concrete = Concrete("C25")
steel = ReinforcementSteel("S420")
wall = Wall(20, 0.8, 8)
plaster = Plaster(2, 1.8)
earthquake = Earthquake(0.4, 1)
reinforcedConcreteDensity = ReinforcedConcreteDensity()
concreteCover = ConcreteCover(3)
heightParameter = HeightParameter(-5, 10)


calculator = GeneralCalculator()
calculator.calculateOneHorizontal(verticalHatil, HorizontalHatil, concrete, steel, wall, plaster,
 earthquake, reinforcedConcreteDensity, concreteCover)