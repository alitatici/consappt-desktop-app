from beam import *
import math

class GeneralCalculator:
    verticalHatil = None
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
    def calculateNonHorizontal(self, verticalHatil, concrete, steel, wall,
     plaster, earthquake, reinforcedConcreteDensity, concreteCover):
        self.verticalHatil = verticalHatil
        self.concrete = concrete
        self.steel = steel
        self.wall = wall,
        self.plaster = plaster,
        self.earthquake = earthquake
        self.reinforcedConcreteDensity = reinforcedConcreteDensity
        self.concreteCover = concreteCover

        self.calculateWallWeightPerUnitArea()
        self.calculateWallLinearWeight()
        self.calculateLinearEquivalentEarthquakeLoad()
        self.calculateMoment()
        self.calculateNecessaryReinforcementArea()

    def calculateWallWeightPerUnitArea(self):
        self.calculatedValues.wallWeightPerUnitArea = (wall.thickness/100) * wall.density + 2*(plaster.thickness/100) * plaster.density
        print(self.calculatedValues.wallWeightPerUnitArea)

    def calculateWallLinearWeight(self):
        temp = (verticalHatil.thickness/100)
        temp *= (wall.thickness/100)
        temp *= reinforcedConcreteDensity.reinforcedConcreteDensity
        temp += ((wall.width - verticalHatil.thickness/100)/2) * self.calculatedValues.wallWeightPerUnitArea
        self.calculatedValues.wallLinearWeight = temp
        print(self.calculatedValues.wallLinearWeight)

    def calculateLinearEquivalentEarthquakeLoad(self):
        print(earthquake.A0,earthquake.I, heightParameter.heightRatio)
        temp = 0.5 * self.calculatedValues.wallLinearWeight * earthquake.A0 * earthquake.I * (1+2*heightParameter.heightRatio)
        self.verticalHatil.linearEquivalentEarthquakeLoad = temp
        print(self.verticalHatil.linearEquivalentEarthquakeLoad)

    def calculateMoment(self):
        temp = verticalHatil.linearEquivalentEarthquakeLoad * verticalHatil.length* verticalHatil.length / 8
        # Convert kN
        self.verticalHatil.maximumMoment = temp * 9.81
        print(self.verticalHatil.maximumMoment)

    def calculateNecessaryReinforcementArea(self):
        a = 0.5 * concrete.k1 * concrete.fcd * verticalHatil.thickness * 10 
        b = - (verticalHatil.thickness - concreteCover.coverThickness) * 10 * concrete.k1 * concrete.fcd * verticalHatil.thickness * 10
        c = verticalHatil.maximumMoment * 1000000
        discriminant = (b*b) - (4*a*c) 

        root = 0

        if discriminant > 0:
            x1 = (- b + math.sqrt(discriminant)) / (2 * a)
            x2 = (- b - math.sqrt(discriminant)) / (2 * a)
        if x1 < x2:
            if x1 > 0:
                print("Root is ", x1)
                root = x1
        elif x2 < x1:
            if x2 > 0:
                print("Root is ", x2)
                root = x2
        else:
            print("Root not found")
            root = None


        temp = concrete.k1 * concrete.fcd *  verticalHatil.thickness * 10 * root / steel.fyd
        self.verticalHatil.necessaryReinforcementArea = temp
        print(self.verticalHatil.necessaryReinforcementArea)


verticalHatil = VerticalHatil(20, 4.1, 4)
concrete = Concrete("C25")
steel = ReinforcementSteel("S420")
wall = Wall(22.5, 0.5, 8.2)
plaster = Plaster(2, 1.8)
earthquake = Earthquake(0.4, 1)
reinforcedConcreteDensity = ReinforcedConcreteDensity()
concreteCover = ConcreteCover(3)
heightParameter = HeightParameter(-5, 10)


calculator = GeneralCalculator()
calculator.calculateNonHorizontal(verticalHatil, concrete, steel, wall, plaster,
 earthquake, reinforcedConcreteDensity, concreteCover)

