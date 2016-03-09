# emacs-mode: -*- python-*-
gObjectTypeInfo = {}

def Init():
    objnames = discovery.getAllObjects()
    globs = globals()
    for (name, id,) in objnames.iteritems():
        name = name.replace(' ', '')
        name = name.replace('-', '')
        globs[name] = id




def GetTypeInfo(id):
    if (id in gObjectTypeInfo):
        return gObjectTypeInfo[id]
    gObjectTypeInfo[id] = discovery.getTypeInfo(id)
    return gObjectTypeInfo[id]


Init()

# local variables:
# tab-width: 4
