class VerticalBeam:
    length=0
    thickness=0
    centerX=0

# parameterized constructor 
    def __init__(self, length, thickness, centerX): 
        self.length = length
        self.thickness = thickness
        self.centerX = centerX
      
    def display(self): 
        print("____________________________________")
        print("VerticalBeam")
        print("Length = " + str(self.length)) 
        print("Thickness = " + str(self.thickness)) 
        print("CenterX = " + str(self.centerX)) 
  
    def calculate(self): 
        self.centerX = self.length + self.thickness 


verticalBeam=VerticalBeam(30,30,30)
verticalBeam.display()

class HorizontalBeam:
    length=0
    thickness=0
    centerY=0

# parameterized constructor 
    def __init__(self, length, thickness, centerX): 
        self.length = length
        self.thickness = thickness
        self.centerY = centerX
      
    def display(self):
        print("____________________________________")
        print("HorizontalBeam")
        print("Length = " + str(self.length)) 
        print("Thickness = " + str(self.thickness)) 
        print("CenterY = " + str(self.centerY)) 
  
    def calculate(self): 
        self.centerX = self.length + self.thickness 


horizontalBeam1=HorizontalBeam(30,30,30)
horizontalBeam1.display()

horizontalBeam2=HorizontalBeam(30,30,30)
horizontalBeam2.display()


print(verticalBeam.length*horizontalBeam1.length) 



