class Concrete:
    concreteType=0
    fck=0
    fcd=0
    fctd=0
    concreteElasticityModulus=0
    k1=0

# parameterized constructor 
    def __init__(self, concreteType): 
        self.concreteType = concreteType
        if concreteType == "C20":
            self.fck=20
            self.fcd=13.3
            self.fctd=1.04
            self.concreteElasticityModulus=28000
            self.k1=0.85
        elif concreteType == "C25":
            self.fck=25
            self.fcd=16.7
            self.fctd=1.17
            self.concreteElasticityModulus=30000
            self.k1=0.85
        elif concreteType == "C30":
            self.fck=30
            self.fcd=20
            self.fctd=1.28
            self.concreteElasticityModulus=32000
            self.k1=0.82
        elif concreteType == "C35":
            self.fck=35
            self.fcd=23.3
            self.fctd=1.38
            self.concreteElasticityModulus=33000
            self.k1=0.79
        elif concreteType == "C40":
            self.fck=40
            self.fcd=26.7
            self.fctd=1.48
            self.concreteElasticityModulus=34000
            self.k1=0.76
        elif concreteType == "C45":
            self.fck=45
            self.fcd=30
            self.fctd=1.57
            self.concreteElasticityModulus=36000
            self.k1=0.73
        elif concreteType == "C50":
            self.fck=50
            self.fcd=33.3
            self.fctd=1.65
            self.concreteElasticityModulus=37000
            self.k1=0.70

class ReinforcementSteel:
    reinforcementSteelType=0
    fyd=0

# parameterized constructor 
    def __init__(self, reinforcementSteelType): 
        self.reinforcementSteelType = reinforcementSteelType
        if reinforcementSteelType == "S220":
            self.fyd=191
        elif reinforcementSteelType == "S420":
            self.fyd=365
        elif reinforcementSteelType == "S500":
            self.fyd=435

class Hatil:
    thickness=0
    location=0
    linearEquivalentEarthquakeLoad=0
    maximumMoment=0
    necessaryReinforcementArea=0
    maximumReinforcementArea=0
    minimumReinforcementArea=0
    maximumShearForce=0
    necessaryStirrup=0
    deflection=0
    def __init__(self, thickness, location): 
        self.thickness = thickness
        self.location = location

class VerticalHatil(Hatil):
    length=0
    pointLoadFromHorizontalHatils=0
    def __init__(self, thickness, location, length): 
        self.thickness = thickness
        self.location = location
        self.length = length


class HorizontalHatil(Hatil):
    leftLength=0
    rightLength=0
    linearLoadFromWall=0
    def setLength(self, leftLength, rightLength):
        self.leftLength = leftLength
        self.rightLength = rightLength

class Wall:
    density=0
    thickness=0
    width=0
    def __init__(self, thickness, density, width): 
        self.thickness = thickness
        self.density = density
        self.width = width

class Plaster:
    density=0
    thickness=0
    def __init__(self, thickness, density): 
        self.thickness = thickness
        self.density = density

class ReinforcedConcreteDensity:
    reinforcedConcreteDensity=0
    def __init__(self): 
        self.reinforcedConcreteDensity = 2.5
    def setDensity(self, newDensity):
        self.reinforcedConcreteDensity = newDensity

class ConcreteCover:
    coverThickness=0
    def __init__(self, coverThickness):
        self.coverThickness = coverThickness

class HeightParameter:
    heightFromBasement=0
    heightMax=0
    heightRatio=0
    def __init__(self, heightFromBasement, heightMax):
        self.heightFromBasement=heightFromBasement
        self.heightMax=heightMax
        if heightFromBasement/heightMax < 0:
            self.heightRatio = 1
        else:
            self.heightRatio = heightFromBasement/heightMax

class Earthquake:
    A0=0
    I=0
    def __init__(self, A0, I):
        self.A0 = A0
        self.I = I

class CalculatedValues:
    wallLinearWeight = 0
    wallWeightPerUnitArea = 0 
    ratioOfSpans = 0
    reinforcementAmount=0


