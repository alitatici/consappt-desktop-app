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
        self.calculateMomentAndShearForce()
        self.calculateDeflection()
        self.calculateNecessaryReinforcementArea()
        self.calculateShearStirrup()

#weight per unit area of wall; plaster multiple with 2 beacuse of plaster uses both sides of wall. Result unit: t/m^2
    def calculateWallWeightPerUnitArea(self):
        self.calculatedValues.wallWeightPerUnitArea = (wall.thickness/100) * wall.density + 2*(plaster.thickness/100) * plaster.density
        print(self.calculatedValues.wallWeightPerUnitArea)

#Calculation of We. Hatil's loads from wall and itself. Result unit: t/m
    def calculateWallLinearWeight(self):
        temp = (verticalHatil.thickness/100)
        temp *= (wall.thickness/100)
        temp *= reinforcedConcreteDensity.reinforcedConcreteDensity
        temp += ((wall.width - verticalHatil.thickness/100)/2) * self.calculatedValues.wallWeightPerUnitArea
        self.calculatedValues.wallLinearWeight = temp
        print(self.calculatedValues.wallLinearWeight)

#Equivalent earthquake load which use in the calculations internal forces. Result unit: t/m
    def calculateLinearEquivalentEarthquakeLoad(self):
        print(earthquake.A0,earthquake.I, heightParameter.heightRatio)
        temp = 0.5 * self.calculatedValues.wallLinearWeight * earthquake.A0 * earthquake.I * (1+2*heightParameter.heightRatio)
        self.verticalHatil.linearEquivalentEarthquakeLoad = temp
        print(self.verticalHatil.linearEquivalentEarthquakeLoad)

#Deflection. Result unit: mm
    def calculateDeflection(self):
        temp = (5 * self.verticalHatil.linearEquivalentEarthquakeLoad * 9.81 * pow((self.verticalHatil.length * 1000),4) * 12)
        temp /= (384 * self.concrete.concreteElasticityModulus * self.verticalHatil.thickness * 10 * pow((wall.thickness * 10),3))
        self.verticalHatil.deflection = temp
        print(self.verticalHatil.deflection)

        if self.verticalHatil.deflection > self.verticalHatil.length * 1000 / 300:
            print("Deflection is too much, hatil's size must be extend!")
        else:
            print("Within the deflection limit.")

#Calculations of maximum moment and shear force. Result unit: tm and t
    def calculateMomentAndShearForce(self):
        temp = verticalHatil.linearEquivalentEarthquakeLoad * 9.81 * verticalHatil.length* verticalHatil.length / 8
        temp2 = verticalHatil.linearEquivalentEarthquakeLoad * 9.81 * verticalHatil.length / 2
        self.verticalHatil.maximumMoment = temp
        self.verticalHatil.maximumShearForce = temp2
        print(self.verticalHatil.maximumMoment)
        print(self.verticalHatil.maximumShearForce)

#Calculation of necessary reinforcement area. Result unit cm^2
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


        temp = concrete.k1 * concrete.fcd *  verticalHatil.thickness * 10 * root / (steel.fyd*100)
        self.verticalHatil.necessaryReinforcementArea = temp
        print(self.verticalHatil.necessaryReinforcementArea)

        if temp < 1.57:
            self.calculatedValues.reinforcementAmount = "2ø10"
        elif temp >= 1.57 and temp < 2.26:
            self.calculatedValues.reinforcementAmount = "2ø12"
        elif temp >= 2.26 and temp < 2.36:
            self.calculatedValues.reinforcementAmount = "3ø10"
        elif temp >= 2.36 and temp < 3.08:
            self.calculatedValues.reinforcementAmount = "2ø14"
        elif temp >= 3.08 and temp < 3.14:
            self.calculatedValues.reinforcementAmount = "4ø10"
        elif temp >= 3.14 and temp < 3.39:
            self.calculatedValues.reinforcementAmount = "3ø12"
        elif temp >= 3.39 and temp < 4.02:
            self.calculatedValues.reinforcementAmount = "2ø16"
        elif temp >= 4.02 and temp < 4.52:
            self.calculatedValues.reinforcementAmount = "4ø12"
        elif temp >= 4.52 and temp < 4.62:
            self.calculatedValues.reinforcementAmount = "3ø14"
        elif temp >= 4.62 and temp < 6.03:
            self.calculatedValues.reinforcementAmount = "3ø16"
        elif temp >= 6.03 and temp < 6.16:
            self.calculatedValues.reinforcementAmount = "4ø14"
        elif temp >= 6.16 and temp < 8.04:
            self.calculatedValues.reinforcementAmount = "4ø16"
        else:
            self.calculatedValues.reinforcementAmount = "not found for "+str(temp)+" cm^2"

        print(self.calculatedValues.reinforcementAmount)
        
#Calculations of stirrups. 
    def calculateShearStirrup(self):
        Vcr = 0.65 * self.concrete.fctd * self.verticalHatil.thickness * 10 * (wall.thickness * 10 - concreteCover * 10)

        self.verticalHatil.necessaryStirrup = Vcr

        print(self.verticalHatil.necessaryStirrup)


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

