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
        self.calculateWallWeightPerMeter()
        self.calculateWallLinearWeight()
        self.calculateLinearEquivalentEarthquakeLoad()
        self.calculateMomentAndShearForce()
        self.calculateDeflectionOfHorizontalHatil()
        self.calculateDeflectionOfVerticalHatil()
        self.calculateNecessaryReinforcementAreaHorizontalHatil()
        self.calculateNecessaryReinforcementAreaVerticalHatil()
        self.calculateShearStirrupsOfHorizontalHatil()
        self.calculateShearStirrupsOfVerticalHatil()
        print(self.report)

        return (self.report, self.report)

    #weight per unit area of wall; plaster multiple with 2 beacuse of plaster uses both sides of wall. Result unit: t/m^2
    def calculateWallWeightPerUnitArea(self):
        self.calculatedValues.wallWeightPerUnitArea = round(((self.wall.thickness/100) * self.wall.density + 2*(self.plaster.thickness/100) * self.plaster.density), 3)
        #print(self.calculatedValues.wallWeightPerUnitArea)
        self.report += "Weight per unit area of wall: "+ str(self.calculatedValues.wallWeightPerUnitArea) + " t/m^2.\n"

    #Weight per meter of wall. Result unit: t/m.
    #This value must be lower than 0.7 t/m.
    def calculateWallWeightPerMeter(self):
        load = (self.wall.width - self.verticalHatil.thickness/100) * (self.verticalHatil.length - self.horizontalHatil.thickness/100) * self.calculatedValues.wallWeightPerUnitArea
        load += self.verticalHatil.thickness/100 * self.wall.thickness/100 * self.verticalHatil.length * self.reinforcedConcreteDensity.reinforcedConcreteDensity
        load += self.horizontalHatil.thickness/100 * self.wall.thickness/100 * (self.wall.width - self.verticalHatil.thickness/100) * self.reinforcedConcreteDensity.reinforcedConcreteDensity
        load /= self.wall.width
        load = round(load, 3)
        if (load / self.wall.width) > 0.7:
            #print("need support to bottom of wall. (>700kg/m)")
            self.report += "Weight per meter of wall: "+ str(load) + " t/m. Need support to bottom of wall. (>700kg/m)\n"
        else:
            #print(load, "ok. (<700 kg/m)")
            self.report += "Weight per meter of wall: "+ str(load) + " t/m. Ok. (<700 kg/m)\n"

    #Calculation of We. Horizontal hatil's loads from wall and itself. Result unit: t/m
    def calculateWallLinearWeight(self):
        temp = (self.horizontalHatil.thickness/100)
        temp *= (self.wall.thickness/100)
        temp *= self.reinforcedConcreteDensity.reinforcedConcreteDensity
        temp += self.calculatedValues.wallWeightPerUnitArea * ((self.horizontalHatil.location - self.horizontalHatil.thickness/200) + self.verticalHatil.length - (self.horizontalHatil.location + self.horizontalHatil.thickness/200)) / 2
        self.calculatedValues.wallLinearWeight = round(temp, 3)
        #print(self.calculatedValues.wallLinearWeight)
        self.report += "The load which comes to hatil: " + str(self.calculatedValues.wallLinearWeight) + " t/m.\n"
        
    #Equivalent earthquake load which use in the calculations internal forces. Result unit: t/m
    def calculateLinearEquivalentEarthquakeLoad(self):
        #print(earthquake.A0,earthquake.I, heightParameter.heightRatio)
        temp = 0.5 * self.calculatedValues.wallLinearWeight * self.earthquake.A0 * self.earthquake.I * (1+2*self.heightParameter.heightRatio)
        self.horizontalHatil.linearEquivalentEarthquakeLoad = round(temp, 3)
        #print(self.horizontalHatil.linearEquivalentEarthquakeLoad)
        self.report += "Equivalent earthquake load: " + str(self.horizontalHatil.linearEquivalentEarthquakeLoad) + " t/m.\n"

    #Calculations of maximum moment and shear force. Result unit: tm and t
    def calculateMomentAndShearForce(self):
        tempa = (self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (self.wall.width - self.verticalHatil.location)**2) / 8
        tempa2 = self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (self.wall.width - self.verticalHatil.location) / 2
        tempo = (self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (self.verticalHatil.location)**2) / 8
        tempo2 = self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (self.verticalHatil.location) / 2

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
        temp3 = self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * (self.wall.width) / 2
        #linear load from itself
        temp4 = (self.verticalHatil.thickness / 100) * (self.wall.thickness / 100) * self.reinforcedConcreteDensity.reinforcedConcreteDensity
        temp4 *= (0.5 * self.earthquake.A0 * self.earthquake.I * (1+2*self.heightParameter.heightRatio))
        temp4 *= 9.81

        self.verticalHatil.pointLoadFromHorizontalHatils = round(temp3, 3)
        self.verticalHatil.linearEquivalentEarthquakeLoad = round(temp4, 3)
        #self.report += str(self.verticalHatil.linearEquivalentEarthquakeLoad) + "\n"

        #Maximum moment of vertical hatil.
        #Calculated like the point load always on the middle of the vertical hatil.
        #Because, it is most unfavorable position for structure.
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

    #Deflection of horizontal hatil. Result unit: mm
    def calculateDeflectionOfHorizontalHatil(self):
        temp = (5 * self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * pow((self.verticalHatil.location * 1000),4) * 12)
        temp /= (384 * self.concrete.concreteElasticityModulus * self.horizontalHatil.thickness * 10 * pow((self.wall.thickness * 10),3))

        temp2 = (5 * self.horizontalHatil.linearEquivalentEarthquakeLoad * 9.81 * pow((self.wall.width - self.verticalHatil.location * 1000),4) * 12)
        temp2 /= (384 * self.concrete.concreteElasticityModulus * self.horizontalHatil.thickness * 10 * pow((self.wall.thickness * 10),3))

        temp3 = round(((self.wall.width - self.verticalHatil.location) * 1000 / 300), 3)

        if temp > temp2:
            self.horizontalHatil.deflection = round(temp, 3)
            #print(self.horizontalHatil.deflection)

            if self.horizontalHatil.deflection > self.verticalHatil.location * 1000 / 300:
                self.report += "Deflection of horizontal hatil: " + str(self.horizontalHatil.deflection) + " mm. Deflection is too much, hatil's sizes must be extend! (L/300 =" +str(temp3) + ")\n"
                #print("Deflection is too much, hatil's sizes must be extend!")
            else:
                self.report += "Deflection of horizontal hatil: " + str(self.horizontalHatil.deflection) + " mm. Within the deflection limit. (L/300 =" +str(temp3) + ")\n"
                #print("Within the deflection limit.")
        else:
            self.horizontalHatil.deflection = round(temp2, 3)
            #print(self.horizontalHatil.deflection)

            if self.horizontalHatil.deflection > (self.wall.width - self.verticalHatil.location) * 1000 / 300:
                self.report += "Deflection of horizontal hatil: " + str(self.horizontalHatil.deflection) + " mm. Deflection is too much, hatil's sizes must be extend! (L/300 =" +str(temp3) + ")\n"
                #print("Deflection is too much, hatil's sizes must be extend!")
            else:
                self.report += "Deflection of horizontal hatil: " + str(self.horizontalHatil.deflection) + " mm. Within the deflection limit. (L/300 =" +str(temp3) + ")\n"
                #print("Within the deflection limit.")

    # Deflection of vertical hatil. Result unit: mm
    # This calculation is not accurrate for every location of horizontal hatil.
    # That's only for horizontal hatil located on the middle of vertical hatil.

    #Deflection of vertical hatil. Result unit: mm
    def calculateDeflectionOfVerticalHatil(self):
        temp = (5 * self.verticalHatil.linearEquivalentEarthquakeLoad * pow((self.verticalHatil.length * 1000),4) * 12)
        temp /= (384 * self.concrete.concreteElasticityModulus * self.verticalHatil.thickness * 10 * pow((self.wall.thickness * 10),3))

        temp2 = (self.verticalHatil.pointLoadFromHorizontalHatils * 1000 * pow((self.verticalHatil.length * 1000), 3) * 12)
        temp2 /= (48 * self.concrete.concreteElasticityModulus * self.verticalHatil.thickness * 10 * pow((self.wall.thickness * 10),3))

        temp3 = round((self.verticalHatil.length * 1000 / 300), 3)

        self.verticalHatil.deflection = round((temp + temp2), 3)

        if self.verticalHatil.deflection > self.verticalHatil.location * 1000 / 300:
            self.report += "Deflection of horizontal hatil: " + str(self.verticalHatil.deflection) + " mm. Deflection is too much, hatil's sizes must be extend! (L/300 =" +str(temp3) + ")\n"
            #print("Deflection is too much, hatil's sizes must be extend!")
        else:
            self.report += "Deflection of horizontal hatil: " + str(self.verticalHatil.deflection) + " mm. Within the deflection limit. (L/300 =" +str(temp3) + ")\n"
            #print("Within the deflection limit.")


    #Calculation of necessary reinforcement area for horizontal hatil. Result unit cm^2
    def calculateNecessaryReinforcementAreaHorizontalHatil(self):
        a = 0.5 * self.concrete.k1 * self.concrete.fcd * self.horizontalHatil.thickness * 10 
        b = - (self.wall.thickness * 10 - self.concreteCover.coverThickness * 10) * self.concrete.k1 * self.concrete.fcd * self.horizontalHatil.thickness * 10
        c = self.horizontalHatil.maximumMoment * 1000000
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


        temp = self.concrete.k1 * self.concrete.fcd *  self.horizontalHatil.thickness * 10 * root / (self.steel.fyd*100)
        self.horizontalHatil.necessaryReinforcementArea = round(temp, 3)
        #print(self.horizontalHatil.necessaryReinforcementArea)
        self.report += "Necessary reinforcement area of horizontal hatil: " + str(self.horizontalHatil.necessaryReinforcementArea) + " cm^2.\n"

        if self.steel.minimumLongitudinalReinforcementDiameter == "ø8" or self.steel.minimumLongitudinalReinforcementDiameter == "ø10":
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

        elif self.steel.minimumLongitudinalReinforcementDiameter == "ø12":
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

        elif self.steel.minimumLongitudinalReinforcementDiameter == "ø14":
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
        
        elif self.steel.minimumLongitudinalReinforcementDiameter == "ø16":
            if temp < 4.02:
	            self.calculatedValues.reinforcementAmount = "2ø16"
            elif temp >= 4.02 and temp < 6.03:
	            self.calculatedValues.reinforcementAmount = "3ø16"
            elif temp >= 6.03 and temp < 8.04:
	            self.calculatedValues.reinforcementAmount = "4ø16"
            else:
	            self.calculatedValues.reinforcementAmount = "not found for "+str(temp)+" cm^2"

        #print(self.calculatedValues.reinforcementAmount)
        self.report += "Necessary reinforcement amount of horizontal hatil: " + str(self.calculatedValues.reinforcementAmount) + "\n"
        return self.calculatedValues.reinforcementAmount

    #Calculation of necessary reinforcement area for vertical hatil. Result unit cm^2
    def calculateNecessaryReinforcementAreaVerticalHatil(self):
        a = 0.5 * self.concrete.k1 * self.concrete.fcd * self.verticalHatil.thickness * 10 
        b = - (self.wall.thickness * 10 - self.concreteCover.coverThickness * 10) * self.concrete.k1 * self.concrete.fcd * self.verticalHatil.thickness * 10
        c = self.verticalHatil.maximumMoment * 1000000
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


        temp = self.concrete.k1 * self.concrete.fcd *  self.verticalHatil.thickness * 10 * root / (self.steel.fyd*100)
        self.verticalHatil.necessaryReinforcementArea = round(temp, 3)
        #print(self.verticalHatil.necessaryReinforcementArea)
        self.report += "Necessary reinforcement area of vertical hatil: " + str(self.verticalHatil.necessaryReinforcementArea) + " cm^2.\n"

        if self.steel.minimumLongitudinalReinforcementDiameter == "ø8" or self.steel.minimumLongitudinalReinforcementDiameter == "ø10":
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

        elif self.steel.minimumLongitudinalReinforcementDiameter == "ø12":
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

        elif self.steel.minimumLongitudinalReinforcementDiameter == "ø14":
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
        
        elif self.steel.minimumLongitudinalReinforcementDiameter == "ø16":
            if temp < 4.02:
	            self.calculatedValues.reinforcementAmount = "2ø16"
            elif temp >= 4.02 and temp < 6.03:
	            self.calculatedValues.reinforcementAmount = "3ø16"
            elif temp >= 6.03 and temp < 8.04:
	            self.calculatedValues.reinforcementAmount = "4ø16"
            else:
	            self.calculatedValues.reinforcementAmount = "not found for "+str(temp)+" cm^2"

        #print(self.calculatedValues.reinforcementAmount)
        self.report += "Necessary reinforcement amount of vertical hatil: " + str(self.calculatedValues.reinforcementAmount) + "\n"
        return self.calculatedValues.reinforcementAmount

    #Calculations of horizontal hatil's stirrups.
    def calculateShearStirrupsOfHorizontalHatil(self):
        Vcr = 0.65 * self.concrete.fctd * self.horizontalHatil.thickness * 10 * (self.wall.thickness * 10 - self.concreteCover.coverThickness * 10) / 1000 
        Vres = 0.22 * self.concrete.fcd * self.horizontalHatil.thickness * 10 * (self.wall.thickness * 10 - self.concreteCover.coverThickness*10) / 1000
        #Vc = 0.8 * Vcr 
        Vw = 2 * pow((self.steel.stirrupDiameter*10),2) * math.pi / 4
        Vw *= (self.wall.thickness * 10 - self.concreteCover.coverThickness * 10)
        Vw *= self.steel.fyd
        Vw /= (self.steel.minimumDistanceBetweenStirrups * 10000)
        #Vr = Vc + Vw
        #print(self.horizontalHatil.maximumShearForce, Vcr, Vw, Vres, Vr, steel.stirrupDiameter, steel.minimumDistanceBetweenStirrups)
        if self.horizontalHatil.maximumShearForce <= Vcr:
        #Minimum stirrups use.
            #print("Stirrup:"+str(steel.minimumStirrupReinforcementDiameter)+"/"+str(steel.minimumDistanceBetweenStirrups)+"cm")
            self.report += "Horizontal hatil stirrup:"+str(self.steel.minimumStirrupReinforcementDiameter)+"/"+str(self.steel.minimumDistanceBetweenStirrups)+" cm"+ "\n"
        else:
            if self.horizontalHatil.maximumShearForce > Vres:
                #print("Hatil's sizes must extend.")
                self.report += "Horizontal hatil's sizes must extend." + "\n"
            else:
                #print("Change the stirrup selections.")
                self.report += "Change the stirrup selection limits." + "\n"

    #Calculations of vertical hatil's stirrups.
    def calculateShearStirrupsOfVerticalHatil(self):
        Vcr = 0.65 * self.concrete.fctd * self.verticalHatil.thickness * 10 * (self.wall.thickness * 10 - self.concreteCover.coverThickness * 10) / 1000 
        Vres = 0.22 * self.concrete.fcd * self.verticalHatil.thickness * 10 * (self.wall.thickness * 10 - self.concreteCover.coverThickness*10) / 1000
        #Vc = 0.8 * Vcr 
        Vw = 2 * pow((self.steel.stirrupDiameter*10),2) * math.pi / 4
        Vw *= (self.wall.thickness * 10 - self.concreteCover.coverThickness * 10)
        Vw *= self.steel.fyd
        Vw /= (self.steel.minimumDistanceBetweenStirrups * 10000)
        #Vr = Vc + Vw
        #print(self.verticalHatil.maximumShearForce, Vcr, Vw, Vres, Vr, steel.stirrupDiameter, steel.minimumDistanceBetweenStirrups)
        if self.verticalHatil.maximumShearForce <= Vcr:
        #Minimum stirrups use.
            #print("Stirrup:"+str(steel.minimumStirrupReinforcementDiameter)+"/"+str(steel.minimumDistanceBetweenStirrups)+"cm")
            self.report += "Vertical hatil stirrup:"+str(self.steel.minimumStirrupReinforcementDiameter)+"/"+str(self.steel.minimumDistanceBetweenStirrups)+" cm"+ "\n"
        else:
            if self.verticalHatil.maximumShearForce > Vres:
                #print("Hatil's sizes must extend.")
                self.report += "Vertical hatil's sizes must extend." + "\n"
            else:
                #print("Change the stirrup selections.")
                self.report += "Change the stirrup selection limits." + "\n"


# verticalHatil = VerticalHatil(20, 4, 5)
# horizontalHatil = HorizontalHatil(20, 2.5)
# concrete = Concrete("C25")
# steel = ReinforcementSteel("S420", "ø10", "ø8", 20)
# wall = Wall(20, 0.5, 8)
# plaster = Plaster(2, 1.8)
# earthquake = Earthquake(0.4, 1)
# reinforcedConcreteDensity = ReinforcedConcreteDensity()
# concreteCover = ConcreteCover(3)
# heightParameter = HeightParameter(-5, 10)


# calculatorOneHorizontal = GeneralCalculatorForOneHorizontal()
# calculatorOneHorizontal.calculateOneHorizontal(verticalHatil, horizontalHatil, concrete, steel, wall, plaster,
# earthquake, reinforcedConcreteDensity, concreteCover, heightParameter)