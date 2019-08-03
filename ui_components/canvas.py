from tkinter import *
from tkinter import ttk

class CanvasWall(ttk.Frame):

    def __init__(self, isapp=True, name='canvaswall'):
        ttk.Frame.__init__(self, name=name)
        self.master.title('Consappt - Hatıl Calculation Program')
        self.isapp = isapp

        self.canvas = Canvas(width=800, height=600, relief=SUNKEN)
        self.canvas.configure(background="#414141", highlightbackground="#383838", borderwidth=2)
        self.canvas.grid(row=0, column =1, rowspan = 60, columnspan=2)

        self.drawingFactor = 2
        self.H1State = False
        self.H2State = False

        self._define_wall()    # setup wall dimensions and appearance
        self._define_vertical_hatil()  # setup vertical hatil dimensions and appearance
        self._define_horizontal_hatil_1()  # setup horizontal hatil 1 dimensions and appearance
        self._define_horizontal_hatil_2()  # setup horizontal hatil 2 dimensions and appearance
        self._wall_setup(None)  # draw the wall and descriptions
        self._add_bindings()    # bind the reshape rectangles

    def _define_wall(self):
        # wall feature definitions
        # (a,b,c) define the wallhead's shape
        # 'motion' - method to use during drag
        #            of the active reshape rectangle
        # 'x1' - used to position descriptive text
        # 'x2' - used to position wallhead
        # 'y' - used to position wallhead
        # 'width' - width of wallhead shaft
        # 'box', 'active' - reshape rectangle styles
        # value are used/re-defined during wall edits
        wall = {
            'motion': None,
            'x1': 100,
            'x2': 250,
            'y': 440,
            'wallHeight': 2,
            'wallWidth': 2,
            'box': {'fill': ''},
            'active': {'fill': 'red'}}

        self.canvas.wallInfo = wall



    def _define_vertical_hatil(self):
        verticalHatil = {
            'motion': None,
            'x': 1,
            'thickness': 0.8,
            'box': {'fill': 'white'},
            'active': {'fill': 'red'}
        }
        self.canvas.verticalHatilInfo = verticalHatil

    def _define_horizontal_hatil_1(self):
        horizontalHatil = {
            'motion': None,
            'z': 0.8,
            'thickness': 0.3,
            'box': {'fill': 'white'},
            'active': {'fill': 'red'}
        }
        self.canvas.horizontalHatil1Info = horizontalHatil

    def _define_horizontal_hatil_2(self):
        horizontalHatil = {
            'motion': None,
            'z': 1.6,
            'thickness': 0.3,
            'box': {'fill': 'white'},
            'active': {'fill': 'red'}
        }
        self.canvas.horizontalHatil2Info = horizontalHatil

    def setH1Active(self):
        self.H1State = True

    def setH1Passive(self):
        self.H1State = False

    def setH2Active(self):
        self.H2State = True

    def setH2Passive(self):
        self.H2State = False

    # ================================================================================
    # Canvas bindings
    # ================================================================================
    def _add_bindings(self):
        # apply reshape rectangle fill colours on mouse enter/leave
        self.canvas.tag_bind('box', '<Enter>', self._box_enter)
        self.canvas.tag_bind('box', '<Leave>', self._box_leave)

        # ignore reshape rectangle enter/leave while rect is dragged
        self.canvas.tag_bind('box', '<B1-Enter>', ' ')
        self.canvas.tag_bind('box', '<B1-Leave>', ' ')

        # capture selection of reshaping rectangles
        self.canvas.tag_bind('wallHeight', '<1>', self._set_motion)
        self.canvas.tag_bind('wallWidth', '<1>', self._set_motion)
        self.canvas.tag_bind('verticalHatil', '<1>', self._set_motion)

        # handle reshape rectangle dragging
        self.canvas.bind(
            '<B1-Motion>', lambda evt: self.canvas.wallInfo['motion'](evt))
        self.canvas.bind('<Button1-ButtonRelease>', self._wall_setup)

    # ================================================================================
    # Bound methods - handle the wall reshaping edits
    # ================================================================================
    def _set_motion(self, evt):
        tags = self.canvas.gettags('current')
        if 'box' not in tags:
            return

        # use Python's ability to reference a function through a variable to
        # assign the appropriate motion method to the wallInfo 'motion'
        # dictionary key; the assigned method will be called when
        # <B1-Motion> is detected
        for t in tags:
            if t == 'wallHeight':
                self.canvas.wallInfo['motion'] = self._move_wallHeight
            elif t == 'wallWidth':
                self.canvas.wallInfo['motion'] = self._move_wallWidth
            elif t == 'verticalHatil':
                self.canvas.wallInfo['motion'] = self._move_verticalHatil

    def _move_wallHeight(self, evt):
        # handle drag of height reshape wall
        # limited to vertical motion
        v = self.canvas.wallInfo
        df = self.drawingFactor
        newHeight = (v['y'] + 2 - self.canvas.canvasy(evt.y))/10/df
        newHeight = newHeight * df
        if newHeight < 2*df:
            newHeight = 2*df
        if newHeight > 20*df:
            newHeight = 20*df

        if newHeight != v['wallHeight']:
            self.canvas.move('wallHeight', 0, (10*df*(v['wallHeight'] - newHeight/df)))
            v['wallHeight'] = newHeight/df

    def set_wallHeight(self, height):
        v = self.canvas.wallInfo
        if height < 2:
            v['wallHeight'] = 2
        elif height > 20:
            v['wallHeight'] = 20
        else:
            v['wallHeight'] = height
        self._wall_setup(None)

    def set_verticalHatilThickness(self, thickness):
        vH = self.canvas.verticalHatilInfo
        if thickness < 0.1:
            vH['thickness'] = 0.1
        elif thickness > 2:
            vH['thickness'] = 2
        else:
            vH['thickness'] = thickness
        self._wall_setup(None)
        

    def _move_wallWidth(self, evt):
        # handle drag of width reshape wall
        # limited to horizontal motion
        v = self.canvas.wallInfo
        vH = self.canvas.verticalHatilInfo
        df = self.drawingFactor
        newWidth = -(v['x1'] - self.canvas.canvasx(evt.x))/10/df
        newWidth = newWidth * df
        if newWidth < 2*df:
            newWidth = 2*df
        if newWidth > 20*df:
            newWidth = 20*df
        if newWidth != v['wallWidth']:
            self.canvas.move('wallWidth', -(v['wallWidth'] - newWidth/df)*df*10, 0)
            v['wallWidth'] = newWidth/df
            if v['wallWidth'] < vH['x']:
                vH['x'] = v['wallWidth']

    def set_wallWidth(self, width):
        v = self.canvas.wallInfo
        if width < 2:
            v['wallWidth'] = 2
        elif width > 20:
            v['wallWidth'] = 20
        else:
            v['wallWidth'] = width
        self._wall_setup(None)

    def _move_verticalHatil(self, evt):
        # handle drag of width reshape wall
        # limited to horizontal motion
        v = self.canvas.wallInfo
        vH = self.canvas.verticalHatilInfo
        df = self.drawingFactor
        newPos = -(v['x1'] - self.canvas.canvasx(evt.x))/10/df
        newPos = newPos * df
        if newPos < 0:
            newPos = 0
        if newPos > v['wallWidth'] * df:
            newPos = v['wallWidth'] * df

        if newPos != vH['x']:
            self.canvas.move('verticalHatil', -10*df*(vH['x'] - newPos/df), 0)
            vH['x'] = newPos/df

    def set_verticalHatilPos(self, pos):
        vH = self.canvas.verticalHatilInfo
        v = self.canvas.wallInfo
        vH['x'] = pos
        if pos < 0:
            vH['x'] = 0
        elif pos > v['wallWidth']:
            vH['x'] = 20
        else:
            vH['x'] = pos
        self._wall_setup(None)

    def set_zoom(self, zoomFactor):
        self.drawingFactor = zoomFactor
        self._wall_setup(None)


    def _box_enter(self, evt):
        # set fill colour to 'active' style
        self.canvas.itemconfigure('current', self.canvas.wallInfo['active'])

    def _box_leave(self, evt):
        # set fill colour to 'normal' style
        self.canvas.itemconfigure('current', self.canvas.wallInfo['box'])

    def _wall_setup(self, evt):
        # this method is called when the canvas is created and
        # whenever the wall is edited; all objects are deleted
        # and redrawn with each edit

        # assign canvas and wallInfo to temp variables for
        # easier reading
        c = self.canvas
        v = self.canvas.wallInfo
        vH = self.canvas.verticalHatilInfo
        hh1 = self.canvas.horizontalHatil1Info
        hh2 = self.canvas.horizontalHatil2Info
        df = self.drawingFactor
        

        tags = c.gettags('current')  # save existing tags, if any
        c.delete(ALL)      # remove all objects

        # WALL SECTION
        # Create the wall
        c.create_rectangle(v['x1'], v['y'], v['x1']+df*(v['wallWidth']*10), v['y']-df*(10*v['wallHeight']),
                           fill='SkyBlue1')

        c.create_rectangle(v['x1']-5, v['y']-df*(10 * v['wallHeight'])-5,
                           v['x1']+5, v['y']-df*(10 * v['wallHeight'])+5,
                           outline='black', width=1,
                           tags=('wallHeight', 'box'))

        c.create_rectangle(v['x1']+(df*v['wallWidth']*10)-5, v['y']-5,
                           v['x1']+(df*v['wallWidth']*10)+5, v['y']+5,
                           outline='black', width=1,
                           tags=('wallWidth', 'box'))

        # create small descriptive walls with text
        arrowShape = (5, 5, 2)

        # height of shaft (changes when 'height' box is dragged)
        start = v['x1'] - 10
        c.create_line(start, v['y'], start, v['y']-10*v['wallHeight']*df,
                      arrow=BOTH, arrowshape=arrowShape, fill="red")
        c.create_text(v['x1']-15, v['y']-(10*v['wallHeight']*df/2), text=v['wallHeight'], anchor=E, fill="red")

        c.create_line(v['x1'], v['y']+10, v['x1']+(10*v['wallWidth']*df), v['y']+10,
                      arrow=BOTH, arrowshape=arrowShape)
        c.create_text((v['x1']+(10*v['wallWidth']*df)/2),
                      v['y']+20, text=v['wallWidth'], anchor=E)

        # create text describing current values of wallInfo keys: a, b, c, height
        c.create_text(v['x1'], 480, text='Wall Height: {}'.format(v['wallHeight']),
                      anchor=W, font=('Helv', 18))
        c.create_text(v['x1'], 510, text='Wall Width: {}'.format(v['wallWidth']),
                      anchor=W, font=('Helv', 18))

        # VERTICAL HATIL SECTION
        c.create_line(v['x1'] + vH['x']*10*df, v['y'], v['x1'] + vH['x']*10*df, v['y']-10*df*v['wallHeight'],
                      fill='#333', width=10*df*vH['thickness'])
        c.create_text(v['x1'], 540, text='Vertical Hatil Pos: {}'.format(vH['x']),
                      anchor=W, font=('Helv', 18))

        c.create_rectangle(v['x1'] + vH['x']*df*10 - 5, v['y']-v['wallHeight']*df*5-5,
                           v['x1'] + vH['x']*df*10 + 5, v['y']-v['wallHeight']*df*5+5,
                           outline='black', width=1, fill='white',
                           tags=('verticalHatil', 'box'))


        # HORIZONTAL HATIL 1 SECTION
        if(self.H1State):
            c.create_line(v['x1'], v['y']-10*df*hh1['z'], v['x1'] + v['wallWidth']*10*df, v['y']-10*df*hh1['z'],
                        fill='#333', width=10*df*hh1['thickness'])

        # HORIZONTAL HATIL 2 SECTION
        if(self.H2State):
            c.create_line(v['x1'], v['y']-10*df*hh2['z'], v['x1'] + v['wallWidth']*10*df, v['y']-10*df*hh2['z'],
                        fill='#333', width=10*df*hh1['thickness'])

        # THICKNESS
        c.create_line(v['x1']+ (vH['x']-vH['thickness']/2)*df*10, v['y']-v['wallHeight']*df*10+10, v['x1'] + (vH['x']+vH['thickness']/2)*df*10, v['y']-v['wallHeight']*df*10+10,
                      arrow=BOTH, arrowshape=arrowShape, fill='white')

        c.create_text(v['x1'] + vH['x']*df*10+5,
                      v['y']-v['wallHeight']*df*10+25, text=vH['thickness'], anchor=E, fill='white')

        # FROM LEFT
        c.create_line(v['x1'], v['y']-v['wallHeight']*df*10-10, v['x1'] + vH['x']*df*10, v['y']-v['wallHeight']*df*10-10,
                      arrow=BOTH, arrowshape=arrowShape)
        c.create_text((v['x1']+(10*vH['x']*df)/2),
                      v['y']-v['wallHeight']*df*10-25, text="{0:.3f}".format(vH['x']), anchor=E)

        # FROM RIGHT
        c.create_line(v['x1'] + vH['x']*df*10, v['y']-v['wallHeight']*df*10-10, v['x1'] + v['wallWidth']*df*10, v['y']-v['wallHeight']*df*10-10,
                      arrow=BOTH, arrowshape=arrowShape)

        length = ((v['wallWidth']-vH['x'])*df*10) /2
        c.create_text(v['x1'] + vH['x']*df*10 + length,
                      v['y']-v['wallHeight']*df*10-25, text="{0:.3f}".format(v['wallWidth'] - vH['x']), anchor=E)

        # if a reshape box is selected, set it to 'active' style
        for t in tags:
            if t in ('wallHeight'):
                c.itemconfigure('current', v['active'])
            elif t in ('wallWidth'):
                c.itemconfigure('current', v['active'])
            elif t in ('verticalHatil'):
                c.itemconfigure('current', v['active'])