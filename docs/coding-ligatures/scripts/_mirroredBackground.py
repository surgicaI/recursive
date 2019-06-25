from mymisc import *
from vanilla import *
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from mojo.drawingTools import *
from AppKit import  NSSegmentStyleRoundRect

def dPoint(scale,p,s=6):
    s = s*scale
    r = s/2
    x, y = p
    rect(x-r,y-r,s,s)



class Win(object):
    globalKey = "com.rafalbuchner.mirroringDrawingGlobal"
    localkey = "com.rafalbuchner.mirroringDrawingLocal"
    mirroringOptions = ["none","hor", "ver", "both"]
    mirroringOptionsDict = [dict(title=option) for option in mirroringOptions]
    showOptions = ["fill", "nodes", "stroke"]
    showOptionsDict = [dict(title=option) for option in showOptions]

    def __init__(self):
        self.drawFill = False
        self.drawNodes = False
        self.drawStroke = False
        self.colorFill = (0,0,1)
        self.colorStroke = (0,0,1)


        btnH = 20
        txtH = 15
        x,y,p = 10,10,10
        self.view = Group((0,0,-0,-0))
        self.view.drawChBox = CheckBox((x,y,-p,btnH), "draw mirrored glyph", callback=self.drawChBoxCallback,sizeStyle="mini")
        y += btnH + p/2
        self.view.mirroringOptionsTxt = TextBox((x,y,-p,txtH), "mirroring options",sizeStyle="small")
        y += txtH + p/2
        self.view.mirroringOptions = SegmentedButton((x,y,-p,btnH), self.mirroringOptionsDict, sizeStyle="mini", callback=self.mirroringOptionsCallback)
        nsObj = self.view.mirroringOptions.getNSSegmentedButton()
        nsObj.setSegmentStyle_(NSSegmentStyleRoundRect)
        y += p + btnH
        self.view.showOptionsTxt = TextBox((x,y,-p,txtH), "show",sizeStyle="small")
        y += txtH + p/2
        self.view.showOptions = SegmentedButton((x,y,-p,btnH), self.showOptionsDict, sizeStyle="mini",callback=self.showOptionsCallback,selectionStyle="any")
        nsObj = self.view.showOptions.getNSSegmentedButton()
        nsObj.setSegmentStyle_(NSSegmentStyleRoundRect)
        y += p + btnH
        self.view.offsetTxt = TextBox((x,y,-p,txtH), "offset",sizeStyle="small")
        y += txtH + p/2
        self.view.offsetX = RBEditText((x,y,50,txtH), 0, sizeStyle="mini",placeholder="x value",callback=self.txtXCallback)
        self.view.offsetY = RBEditText((x+50,y,50,txtH), 0, sizeStyle="mini",placeholder="y value",callback=self.txtYCallback)
        y += btnH + p/2
        self.view.fillTxt = TextBox((x,y,-p,txtH), "fill",sizeStyle="small")
        self.view.fillColor = ColorWell((x+50, y, 50, txtH),
                                    callback=self.colorFillEdit, color=rgb2NSColor(self.colorFill))
        y += txtH + p/2
        self.view.strokeTxt = TextBox((x,y,-p,txtH), "stroke",sizeStyle="small")
        self.view.strokeColor = ColorWell((x+50, y, 50, txtH),
                                    callback=self.colorStrokeEdit, color=rgb2NSColor(self.colorStroke))
        self.loadSettings()
        self.w = FloatingWindow((0,0,200,300))
        self.w.view = self.view
        self.initCallbacksUI()
        self.loadGlyph()
        self.intiCallbackRadios()
        self.w.open()
        self.w.bind("close", self.closeWin)
        self.addObservers()
    # dcode
    def determineMirroringOption(self):
        if self.mirroringType == "none":
            self.reflectionMatrix = [1,0,0,1,0,0]
        if self.mirroringType == "both":
            self.reflectionMatrix = [-1,0,0,-1,0,0]
        if self.mirroringType == "ver":
            self.reflectionMatrix = [1,0,0,-1,0,0]
        if self.mirroringType == "hor":
            self.reflectionMatrix = [-1,0,0,1,0,0]

    def closeWin(self, sender):
        self.removeObservers()
        UpdateCurrentGlyphView()

    def addObservers(self):
        addObserver(self, "currentGlyphChangedCallback", "currentGlyphChanged")
        addObserver(self, "drawBackgroundCallback", "drawBackground")

    def removeObservers(self):
        removeObserver(self, "currentGlyphChanged")
        removeObserver(self, "drawBackground")

    def initCallbacksUI(self):
        self.txtXCallback(self.view.offsetX)
        self.txtYCallback(self.view.offsetY)
        self.colorFillEdit(self.view.fillColor)
        self.colorStrokeEdit(self.view.strokeColor)
        self.drawChBoxCallback(self.view.drawChBox)

    def intiCallbackRadios(self):
        self.mirroringType = "none"
        self.determineMirroringOption()

    def drawAction(self, scale):
        def _drawGlyph():
            if self.drawNodes:
                fill( *self.colorStroke )
                stroke(None)
                for c in self.glyph:
                    for p in c.points:
                        dPoint(scale,p.position)

            strokeWidth(1 * scale)
            if self.drawStroke: stroke( *self.colorStroke )
            else:               stroke( None )
            if self.drawFill:   fill  ( *self.colorFill )
            else:               fill  ( None )
            drawGlyph(self.glyph)

        # self.determineMirroringOption()

        x, y = self.drawingMeasurements

        translate(x+self.offsetX,y+self.offsetY)
        transform(self.reflectionMatrix)
        translate(-x,-y)


        _drawGlyph()


    def loadGlyph(self):
        self.glyph = CurrentGlyph()

    def loadSettings(self):
        # code
        pass



    # UI callbacks
    def colorFillEdit(self,sender):
        self.colorFill = nsColor2RGB(sender.get())
        UpdateCurrentGlyphView()

    def colorStrokeEdit(self, sender):
        self.colorStroke = nsColor2RGB(sender.get())
        UpdateCurrentGlyphView()

    def txtXCallback(self, sender):
        self.offsetX = float(sender.get())
        print(self.offsetX)
        UpdateCurrentGlyphView()

    def txtYCallback(self, sender):
        self.offsetY = float(sender.get())
        print(self.offsetY)
        UpdateCurrentGlyphView()

    def showOptionsCallback(self, sender):
        if len(sender.get()) == 0:
            sender.set([0])
        if 0 in sender.get():
            self.drawFill = True
        else:
            self.drawFill = False
        if 1 in sender.get():
            self.drawNodes = True
        else:
            self.drawNodes = False

        if 2 in sender.get():
            self.drawStroke = True
        else:
            self.drawStroke = False
        UpdateCurrentGlyphView()

    def mirroringOptionsCallback(self, sender):
        self.mirroringType = self.mirroringOptions[sender.get()]
        self.determineMirroringOption()

        UpdateCurrentGlyphView()

    def drawChBoxCallback(self, sender):
        self.drawGlyph = False
        if sender.get() == 1:
            self.drawGlyph = True
        UpdateCurrentGlyphView()

    # observer events
    def currentGlyphChangedCallback(self, info):
        self.loadGlyph()

    def drawBackgroundCallback(self, info):
        if self.glyph is not None and self.drawGlyph:
            scale = info['scale']
            save()
            self.drawAction(scale)
            restore()

    # dynamic properties
    # @offsetX.setter
    # def offsetX(self, value):
    #     self.__offsetX = value
    #
    # @offsetY.setter
    # def offsetY(self, value):
    #     self.__offsetY = value

    @property
    def drawingMeasurements(self):
        _x,_y,x_,y_ = self.glyph.bounds
        self.__drawingMeasurements = ((x_-_x)/2+_x,(y_-_y)/2+_y)
        return self.__drawingMeasurements

Win()
