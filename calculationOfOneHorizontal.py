from beam import *
import math
	
class GeneralCalculatorForOneHorizontal:
    verticalHatil = None
    horizontalHatil = None
    concrete = None
    steel = None
    wall = None
    plaster = None
    earthquake = None
    reinforcedConcreteDensity = None
    concreteCover = None
    calculatedValues = None
    report = ""

    def __init__(self):
        print("calculatorOneHorizontal Initialized")
        self.calculatedValues = CalculatedValues()
    def calculateOneHorizontal(self, verticalHatil, horizontalHatil, concrete, steel, wall,
    plaster, earthquake, reinforcedConcreteDensity, concreteCover):
        self.verticalHatil = verticalHatil
        self.horizontalHatil = horizontalHatil
        self.concrete = concrete
        self.steel = steel
        self.wall = wall,
        self.plaster = plaster,
        self.earthquake = earthquake
        self.reinforcedConcreteDensity = reinforcedConcreteDensity
        self.concreteCover = concreteCover
        
        self.calculateWallWeightPerUnitArea()
        self.calculateWallWeightPerMeter()
        self.calculateWallLinearWeight()
        self.calculateLinearEquivalentEarthquakeLoad()
        self.calculateMomentAndShearForce()
        # self.calculateDeflection()
        #self.calculateNecessaryReinforcementArea()
        #self.calculateShearStirrups()
        print(self.report)

    #weight per unit area of wall; plaster multiple with 2 beacuse of plaster uses both sides of wall. Result unit: t/m^2
    def calculateWallWeightPerUnitArea(self):
        self.calculatedValues.wallWeightPerUnitArea = round((wall.thickness/100) * wall.density + 2*(plaster.thickness/100) * plaster.density, 3)
        #print(self.calculatedValues.wallWeightPerUnitArea)
        self.report += "Weight per unit area of wall: "+ str(self.calculatedValues.wallWeightPerUnitArea) + " t/m^2.\n"

    #Weight per meter of wall. Result unit: t/m.
    #This value must be lower than 0.7 t/m.
    def calculateWallWeightPerMeter(self):
        load = (wall.width - verticalHatil.thickness/100) * (verticalHatil.length - HorizontalHatil.thickness/100) * self.calculatedValues.wallWeightPerUnitArea
        load += verticalHatil.thickness/100 * wall.thickness/100 * verticalHatil.length * reinforcedConcreteDensity.reinforcedConcreteDensity
        load += horizontalHatil.thickness/100 * wall.thickness/100 * (wall.width - verticalHatil.thickness/100) * reinforcedConcreteDensity.reinforcedConcreteDensity
        load /= wall.width
        load = round(load, 3)
        if load / wall.width > 0.7:
            #print("need support to bottom of wall. (>700kg/m)")
            self.report += "Weight per meter of wall: "+str(load) + " t/m. Need support to bottom of wall. (>700kg/m)\n"
        else:
            #print(load, "ok. (<700 kg/m)")
            self.report += "Weight per meter of wall: "+str(load) + " t/m. Ok. (<700 kg/m)\n"

    #Calculation of We. Horizontal hatil's loads from wall and itself. Result unit: t/m
    def calculateWallLinearWeight(self):
        temp = (self.horizontalHatil.thickness/100)
        temp *= (wall.thickness/100)
        temp *= reinforcedConcreteDensity.reinforcedConcreteDensity
        temp += self.calculatedValues.wallWeightPerUnitArea * ((self.horizontalHatil.location - self.horizontalHatil.thickness/200) + self.verticalHatil.length - (self.horizontalHatil.location + self.horizontalHatil.thickness/200)) / 2
        self.calculatedValues.wallLinearWeight = round(temp, 3)
        #print(self.calculatedValues.wallLinearWeight)
        self.report += "The load which comes to hatil: " + str(self.calculatedValues.wallLinearWeight) + " t/m.\n"
        
    #Equivalent earthquake load which use in the calculations internal forces. Result unit: t/m
    def calculateLinearEquivalentEarthquakeLoad(self):
        #print(earthquake.A0,earthquake.I, heightParameter.heightRatio)
        temp = 0.5 * self.calculatedValues.wallLinearWeight * earthquake.A0 * earthquake.I * (1+2*heightParameter.heightRatio)
        self.horizontalHatil.linearEquivalentEarthquakeLoad = round(temp, 3)
        #print(self.horizontalHatil.linearEquivalentEarthquakeLoad)
        self.report += "Equivalent earthquake load: " + str(self.horizontalHatil.linearEquivalentEarthquakeLoad) + " t/m.\n"

    #Calculations of maximum moment and shear force. Result unit: tm and t
    def calculateMomentAndShearForce(self):
        tempa = (self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (wall.width - verticalHatil.location)**2) / 8
        tempa2 = self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (wall.width - verticalHatil.location) / 2
        tempo = (self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (verticalHatil.location)**2) / 8
        tempo2 = self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (verticalHatil.location) / 2

        if tempa > tempo:
            temp = tempa
        else:
            temp = tempo

        if tempa2 > tempo2:
            temp2 = tempa2
        else:
            temp2 = tempo2

        self.horizontalHatil.maximumMoment = round(temp, 3)
        self.horizontalHatil.maximumShearForce = round(temp2, 3)
        self.report += "Maximum moment of horizontal hatil: " + str(self.horizontalHatil.maximumMoment) + " kNm.\n"
        self.report += "Maximum shear force for horizontal hatil: " + str(self.horizontalHatil.maximumShearForce) + " kN.\n"

        #vertical hatil's point load from horizontal hatil
        temp3 = self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (wall.width) / 2
        #linear load from itself
        temp4 = (self.verticalHatil.thickness / 100) * (wall.thickness / 100) * reinforcedConcreteDensity.reinforcedConcreteDensity
        temp4 *= (0.5 * earthquake.A0 * earthquake.I * (1+2*heightParameter.heightRatio))
        temp4 *= 9.81

        self.verticalHatil.pointLoadFromHorizontalHatils = round(temp3, 3)
        self.verticalHatil.linearEquivalentEarthquakeLoad = round(temp4, 3)
        self.report += str(self.verticalHatil.linearEquivalentEarthquakeLoad) + "\n"

        #Maximum moment of vertical hatil.
        temp5 = (temp3 * (self.verticalHatil.length - self.horizontalHatil.location) * self.horizontalHatil.location / self.verticalHatil.length)
        temp5 += (temp4 * self.verticalHatil.length **2 / 8)
        temp6_1 = temp3 * (self.verticalHatil.length - self.horizontalHatil.location) / self.verticalHatil.length
        temp6_2 = temp3 * self.horizontalHatil.location / self.verticalHatil.length

        if temp6_1 > temp6_2:
            temp6 = temp6_1
        else:
            temp6 = temp6_2

        temp6 += temp4 * self.verticalHatil.length / 2

        self.verticalHatil.maximumMoment = round(temp5, 3)
        self.verticalHatil.maximumShearForce = round(temp6, 3)
        self.report += "Maximum moment of vertical hatil: " + str(self.verticalHatil.maximumMoment) + " kNm.\n"
        self.report += "Maximum shear force for vertical hatil: " + str(self.verticalHatil.maximumShearForce) + " kN.\n"

        #Calculated like the point load always on the middle of the vertical hatil.
        #Because, it is most unfavorable position for structure.

        print(self.horizontalHatil.maximumMoment)
        print(self.horizontalHatil.maximumShearForce)
        print(self.verticalHatil.pointLoadFromHorizontalHatils)
        print(self.verticalHatil.maximumMoment)
        print(self.verticalHatil.maximumShearForce)

    # #Deflection of horizontal hatil. Result unit: mm
    # def calculateDeflection(self):
    #     temp = (5 * self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * pow((self.verticalHatil.location * 1000),4) * 12)
    #     temp /= (384 * self.concrete.concreteElasticityModulus * self.horizontalHatil.thickness * 10 * pow((wall.thickness * 10),3))

    #     temp2 = (5 * self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * pow((wall.width - self.verticalHatil.location * 1000),4) * 12)
    #     temp2 /= (384 * self.concrete.concreteElasticityModulus * self.horizontalHatil.thickness * 10 * pow((wall.thickness * 10),3))

    #     if temp > temp2:
    #         self.horizontalHatil.deflection = temp
    #         print(self.horizontalHatil.deflection)

    #         if self.horizontalHatil.deflection > self.verticalHatil.location * 1000 / 300:
    #             print("Deflection is too much, hatil's sizes must be extend!")
    #         else:
    #             print("Within the deflection limit.")
    #     else:
    #         self.horizontalHatil.deflection = temp2
    #         print(self.horizontalHatil.deflection)

    #         if self.horizontalHatil.deflection > (wall.width - self.verticalHatil.location) * 1000 / 300:
    #             print("Deflection is too much, hatil's sizes must be extend!")
    #         else:
    #             print("Within the deflection limit.")

    #Deflection of vertical hatil. Result unit: mm
    #This calculation is not accurrate for every location of horizontal hatil.
    #That's only for horizontal hatil located on the middle of vertical hatil.



verticalHatil = VerticalHatil(20, 4, 5)
horizontalHatil = HorizontalHatil(20, 2.5)
concrete = Concrete("C25")
steel = ReinforcementSteel("S420", "ø10", "ø8", 10)
wall = Wall(20, 0.8, 8)
plaster = Plaster(2, 1.8)
earthquake = Earthquake(0.4, 1)
reinforcedConcreteDensity = ReinforcedConcreteDensity()
concreteCover = ConcreteCover(3)
heightParameter = HeightParameter(-5, 10)


calculatorOneHorizontal = GeneralCalculatorForOneHorizontal()
calculatorOneHorizontal.calculateOneHorizontal(verticalHatil, horizontalHatil, concrete, steel, wall, plaster,
earthquake, reinforcedConcreteDensity, concreteCover)