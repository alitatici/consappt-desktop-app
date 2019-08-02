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
   #delete it later... #ReinforcementSteel = None
    report = ""
    

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
        self.calculateWallWeightPerMeter()
        self.calculateWallLinearWeight()
        self.calculateLinearEquivalentEarthquakeLoad()
        self.calculateDeflection()
        self.calculateMomentAndShearForce()
        result = self.calculateNecessaryReinforcementArea()
        self.calculateShearStirrups()
        print(self.report)
        return result

#weight per unit area of wall; plaster multiple with 2 beacuse of plaster uses both sides of wall. Result unit: t/m^2
    def calculateWallWeightPerUnitArea(self):
        self.calculatedValues.wallWeightPerUnitArea = round((wall.thickness/100) * wall.density + 2*(plaster.thickness/100) * plaster.density, 3)
        #print("Weight per unit area of wall: "+ str(self.calculatedValues.wallWeightPerUnitArea))
        self.report += "Weight per unit area of wall: "+ str(self.calculatedValues.wallWeightPerUnitArea) + " t/m^2.\n"

#Weight per meter of wall. Result unit: t/m. 
#This value must be lower than 0.7 t/m.
    def calculateWallWeightPerMeter(self):
        load = (wall.width - verticalHatil.thickness/100) * verticalHatil.length * self.calculatedValues.wallWeightPerUnitArea
        load += verticalHatil.thickness/100 * wall.thickness/100 * verticalHatil.length * reinforcedConcreteDensity.reinforcedConcreteDensity
        load /= wall.width
        load = round(load, 3)
        if load > 0.7:
            #print(str(load) + " t/m. Need support to bottom of wall. (>700kg/m)")
            self.report += "Weight per meter of wall: "+str(load) + " t/m. Need support to bottom of wall. (>700kg/m)\n"
        else:
            #print(load, "ok. (<700 kg/m)")
            self.report += "Weight per meter of wall: "+str(load) + " t/m. Ok. (<700 kg/m)\n"

#Calculation of We. Hatil's loads from wall and itself. Result unit: t/m
    def calculateWallLinearWeight(self):
        temp = (verticalHatil.thickness/100)
        temp *= (wall.thickness/100)
        temp *= reinforcedConcreteDensity.reinforcedConcreteDensity
        temp += ((wall.width - verticalHatil.thickness/100)/2) * self.calculatedValues.wallWeightPerUnitArea
        self.calculatedValues.wallLinearWeight = round(temp, 3)
        #print("The load which comes to hatil: " + str(self.calculatedValues.wallLinearWeight))
        self.report += "The load which comes to hatil: " + str(self.calculatedValues.wallLinearWeight) + " t/m.\n"

#Equivalent earthquake load which use in the calculations internal forces. Result unit: t/m
    def calculateLinearEquivalentEarthquakeLoad(self):
        temp = 0.5 * self.calculatedValues.wallLinearWeight * earthquake.A0 * earthquake.I * (1+2*heightParameter.heightRatio)
        self.verticalHatil.linearEquivalentEarthquakeLoad = round(temp, 3)
        #print("Equivalent earthquake load " + str(self.verticalHatil.linearEquivalentEarthquakeLoad))
        self.report += "Equivalent earthquake load: " + str(self.verticalHatil.linearEquivalentEarthquakeLoad) + " t/m.\n"

#Deflection. Result unit: mm
    def calculateDeflection(self):
        temp = (5 * self.verticalHatil.linearEquivalentEarthquakeLoad * 9.81 * pow((self.verticalHatil.length * 1000),4) * 12)
        temp /= (384 * self.concrete.concreteElasticityModulus * self.verticalHatil.thickness * 10 * pow((wall.thickness * 10),3))
        self.verticalHatil.deflection = round(temp,3)
        #print("Deflection of vertical hatil: " + str(self.verticalHatil.deflection))

        if self.verticalHatil.deflection > self.verticalHatil.length * 1000 / 300:
            #print("Deflection is too much, hatil's size must be extend!")
            self.report += "Deflection of vertical hatil: " + str(self.verticalHatil.deflection) + " mm. Deflection is too much, hatil's size must be extend!(>=L/300)" + "\n"
        else:
            #print("Within the deflection limit.")
            self.report += "Deflection of vertical hatil: " + str(self.verticalHatil.deflection) + " mm. Within the deflection limit.(<L/300)" + "\n"
        
#Calculations of maximum moment and shear force. Result unit: tm and t
    def calculateMomentAndShearForce(self):
        temp = verticalHatil.linearEquivalentEarthquakeLoad * 9.81 * verticalHatil.length* verticalHatil.length / 8
        temp2 = verticalHatil.linearEquivalentEarthquakeLoad * 9.81 * verticalHatil.length / 2
        self.verticalHatil.maximumMoment = round(temp, 3)
        self.verticalHatil.maximumShearForce = round(temp2, 3)

        #print(self.verticalHatil.maximumMoment)
        #print(self.verticalHatil.maximumShearForce)
        self.report += "Maximum moment: " + str(self.verticalHatil.maximumMoment) + " kNm.\n" + "Maximum shear force: " + str(self.verticalHatil.maximumShearForce) + " kN.\n"

#Calculation of necessary reinforcement area. Result unit cm^2
    def calculateNecessaryReinforcementArea(self):
        a = 0.5 * concrete.k1 * concrete.fcd * verticalHatil.thickness * 10 
        b = - (wall.thickness * 10 - concreteCover.coverThickness * 10) * concrete.k1 * concrete.fcd * verticalHatil.thickness * 10
        c = verticalHatil.maximumMoment * 1000000
        discriminant = (b*b) - (4*a*c) 

        root = 0

        if discriminant > 0:
            x1 = (- b + math.sqrt(discriminant)) / (2 * a)
            x2 = (- b - math.sqrt(discriminant)) / (2 * a)
        if x1 < x2:
            if x1 > 0:
                #print("Root is ", x1)
                root = x1
        elif x2 < x1:
            if x2 > 0:
                #print("Root is ", x2)
                root = x2
        else:
            print("Root not found\n")
            root = None


        temp = concrete.k1 * concrete.fcd *  verticalHatil.thickness * 10 * root / (steel.fyd*100)
        self.verticalHatil.necessaryReinforcementArea = round(temp, 3)
        #print(self.verticalHatil.necessaryReinforcementArea)
        self.report += "Necessary reinforcement area: " + str(self.verticalHatil.necessaryReinforcementArea) + " cm^2.\n"

        if steel.minimumLongitudinalReinforcementDiameter == "ø8" or steel.minimumLongitudinalReinforcementDiameter == "ø10":
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

        elif steel.minimumLongitudinalReinforcementDiameter == "ø12":
            if temp < 2.26:
	            self.calculatedValues.reinforcementAmount = "2ø12"
            elif temp >= 2.26 and temp < 3.08:
                self.calculatedValues.reinforcementAmount = "2ø14"
            elif temp >= 3.08 and temp < 3.39:
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

        elif steel.minimumLongitudinalReinforcementDiameter == "ø14":
            if temp < 3.08:
                self.calculatedValues.reinforcementAmount = "2ø14"
            elif temp >= 3.08 and temp < 4.02:
                self.calculatedValues.reinforcementAmount = "2ø16"
            elif temp >= 4.02 and temp < 4.62:
                self.calculatedValues.reinforcementAmount = "3ø14"
            elif temp >= 4.62 and temp < 6.03:
                self.calculatedValues.reinforcementAmount = "3ø16"
            elif temp >= 6.03 and temp < 6.16:
                self.calculatedValues.reinforcementAmount = "4ø14"
            elif temp >= 6.16 and temp < 8.04:
                self.calculatedValues.reinforcementAmount = "4ø16"
            else:
                self.calculatedValues.reinforcementAmount = "not found for "+str(temp)+" cm^2"
        
        elif steel.minimumLongitudinalReinforcementDiameter == "ø16":
            if temp < 4.02:
	            self.calculatedValues.reinforcementAmount = "2ø16"
            elif temp >= 4.02 and temp < 6.03:
	            self.calculatedValues.reinforcementAmount = "3ø16"
            elif temp >= 6.03 and temp < 8.04:
	            self.calculatedValues.reinforcementAmount = "4ø16"
            else:
	            self.calculatedValues.reinforcementAmount = "not found for "+str(temp)+" cm^2"

        #print(self.calculatedValues.reinforcementAmount)
        self.report += "Necessary reinforcement amount: " + str(self.calculatedValues.reinforcementAmount) + "\n"
        return self.calculatedValues.reinforcementAmount
                
#Calculations of stirrups.
    def calculateShearStirrups(self):
        Vcr = 0.65 * self.concrete.fctd * self.verticalHatil.thickness * 10 * (wall.thickness * 10 - concreteCover.coverThickness * 10) / 1000 
        Vres = 0.22 * concrete.fcd * self.verticalHatil.thickness * 10 * (wall.thickness * 10 - concreteCover.coverThickness*10) / 1000
        #Vc = 0.8 * Vcr 
        Vw = 2 * pow((steel.stirrupDiameter*10),2) * math.pi / 4
        Vw *= (wall.thickness * 10 - concreteCover.coverThickness * 10)
        Vw *= steel.fyd
        Vw /= (steel.minimumDistanceBetweenStirrups * 10000)
        #Vr = Vc + Vw
        #print(self.verticalHatil.maximumShearForce, Vcr, Vw, Vres, Vr, steel.stirrupDiameter, steel.minimumDistanceBetweenStirrups)
        if self.verticalHatil.maximumShearForce <= Vcr:
        #Minimum stirrups use.
            #print("Stirrup:"+str(steel.minimumStirrupReinforcementDiameter)+"/"+str(steel.minimumDistanceBetweenStirrups)+"cm")
            self.report += "Stirrup:"+str(steel.minimumStirrupReinforcementDiameter)+"/"+str(steel.minimumDistanceBetweenStirrups)+" cm"+ "\n"
        else:
            if self.verticalHatil.maximumShearForce > Vres:
                #print("Hatil's sizes must extend.")
                self.report += "Hatil's sizes must extend." + "\n"
            else:
                #print("Change the stirrup selections.")
                self.report += "Change the stirrup selections." + "\n"



verticalHatil = VerticalHatil(20, 4.1, 3)
concrete = Concrete("C25")
steel = ReinforcementSteel("S420", "ø12", "ø8", 20)
wall = Wall(15, 0.5, 8.2)
plaster = Plaster(2, 1.8)
earthquake = Earthquake(0.4, 1)
reinforcedConcreteDensity = ReinforcedConcreteDensity()
concreteCover = ConcreteCover(3)
heightParameter = HeightParameter(-5, 10)


# calculator = GeneralCalculator()
# calculator.calculateNonHorizontal(verticalHatil, concrete, steel, wall, plaster,
#  earthquake, reinforcedConcreteDensity, concreteCover)

