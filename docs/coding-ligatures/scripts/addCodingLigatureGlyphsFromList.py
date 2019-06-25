from vanilla import *

class Win:
    def __init__(self):
        self.w = FloatingWindow((0,0,200,200),minSize=(200,200))
        self.w.list = List((0,0,-0,-44),[],columnDescriptions=[{"title":"glyph sources","editable":True,}],allowsEmptySelection=True)#,selectionCallback=self.selectionCallback)
        self.w.addBtn = SquareButton((0,-22,100,22),"create",callback=self.btnCb)
        self.w.addItemBtn = SquareButton((100,-22,22,22),"+",callback=self.addCb)
        self.w.deleteItems = SquareButton((122,-22,22,22),"-",callback=self.deleteCb)
        self.w.suffixTxt = TextBox((10,-44,100,22),"suffix")
        self.w.suffix = EditText((54,-44,0,22),"code")
        self.w.open()

    def deleteCb(self, sender):
        items = self.w.list.get()
        selection = self.w.list.getSelection()
        newItems = []
        for i, item in enumerate(items):
            if i in selection:
                continue
            newItems += [item]
        self.w.list.set(newItems)
            
    def addCb(self, sender):
        items = self.w.list.get()
        if len(CurrentFont().selectedGlyphNames) == 0:
            items += [{"glyph sources":"…"}]
        else:
                
            items += [{"glyph sources":" ".join(CurrentFont().selectedGlyphNames)}]
        self.w.list.set(items)
        
    def btnCb(self, sender):
        font = CurrentFont()
        items = self.w.list.get()
        suffix = self.w.suffix.get()
        for namedict in items:
            name = list(namedict.values())[0].replace(" ","_")
            name += ".%s" % suffix
            font.newGlyph(name)
            names = list(namedict.values())[0].split(" ")
            color = (0,0,1,1)
            offset = 0
            for _name in names:
                if _name not in font.keys():
                    color = (1,0,0,1)
                    continue
                component = font[_name]
                font[name].appendComponent(_name,offset=(offset,0))
                font[name].width += component.width
                offset += component.width
            font[name].markColor = color
        font.changed()
                
            
def main():
    Win()
    
    
if "__main__" == __name__:
    main()