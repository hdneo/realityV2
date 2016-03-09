# emacs-mode: -*- python-*-
import obj
Cookbook = ((obj.CodeFragmentB,
  obj.CodeFragmentC,
  obj.TapDataNodeAbility),
 (obj.CodeFragmentB,
  obj.CodeFragmentC,
  obj.CodeFragmentC,
  obj.AnalyzeWeaknessTool))

def CraftRecipe(*ingredients):
    """ingredients is a tuple of Game Obj IDs.  Return value is new Game Obj ID (zero for failure)."""
    globs = globals()
    WriteOutCookbook()
    for recipe in Cookbook:
        if ((len(recipe) - 1) == len(ingredients)):
            discovery.serverPrint('SP: Crafting - Testing Recipe')
            if (ingredients == recipe[:len(ingredients)]):
                a_str = 'SP: Crafting - Recipe '
                for item in recipe:
                    type_info = discovery.getTypeInfo(item)
                    a_str = (a_str + type_info['localname'])
                    a_str = (a_str + '\n ')

                discovery.serverPrint(a_str)
                return recipe[(len(recipe) - 1)]

    discovery.serverPrint('SP: Crafting - No Matching Recipe Found')
    return 0



def GetRecipesForWriteCodeLevel(level):
    """ find the recipes for level """
    obj_list = []
    for recipe in Cookbook:
        item = recipe[(len(recipe) - 1)]
        type_info = discovery.getTypeInfo(item)
        if (type_info and type_info.has_key('Complexity')):
            if (level < type_info.Complexity):
                obj_list.append(item)

    return obj_list



def GetRecipesForObject(obj):
    """ find the recipe for the object """
    print 'getting recipe for ',
    print obj
    for recipe in Cookbook:
        if (obj == recipe[(len(recipe) - 1)]):
            foo = recipe[0:(len(recipe) - 1)]
            print 'Get recipe : ',
            print recipe[0:(len(recipe) - 1)],
            print ' type : ',
            print type(recipe[0:(len(recipe) - 1)])
            return foo

    return None



def debugTest():
    discovery.outputDebugString('-------------------------------------------------\n')
    discovery.outputDebugString('python- code fragment recipes loaded.\n')
    discovery.outputDebugString('-------------------------------------------------\n')
    discovery.serverPrint('SP: Code Fragment Recipes Functioning')



def WriteOutCookbook():
    file = open('c:/matrix/game/matrix/resource/Python/Monolith/clientcookbook.txt', 'w')
    for recipe in Cookbook:
        item = recipe[(len(recipe) - 1)]
        file.write(('%i ' % item))
        for i in range(0, (len(recipe) - 1)):
            file.write(('%i ' % recipe[i]))

        file.write('\n')

    file.close()



# local variables:
# tab-width: 4
