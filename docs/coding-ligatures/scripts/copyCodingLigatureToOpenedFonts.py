af = AllFonts()
cf = CurrentFont()
for name in cf.selectedGlyphNames:
    if name.split(".")[1] == "code":
        baseNames = name.split(".")[0].split("_")
        for f in af:
            if f == cf:
                continue
            f.newGlyph(name)
            color = (0,0,1,1)
            offset = 0
            for baseName in baseNames:
                if baseName not in f.keys():
                    color = (1,0,0,1)
                    continue
                component = f[baseName]
                f[name].appendComponent(baseName,offset=(offset,0))
                f[name].width += component.width
                offset += component.width
            f[name].markColor = color
        