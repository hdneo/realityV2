# emacs-mode: -*- python-*-

def GetImportObjects():
    importList = []
    importList.append('ability.general')
    importList.append('ability.effects')
    importList.append('ability.spy.sneaks')
    importList.append('ability.spy.misc')
    importList.append('ability.hacker.virii')
    importList.append('ability.hacker.health')
    importList.append('ability.hacker.misc')
    importList.append('ability.hacker.simulacra')
    importList.append('ability.hacker.crafting')
    importList.append('ability.soldier.misc')
    importList.append('ability.npc.specialmoves')
    importList.append('generic_free_attacks')
    return importList



def abilitiesSuccess():
    discovery.outputDebugString('-------------------------------------------------\n')
    discovery.outputDebugString('python- abilities system loaded.\n')
    discovery.outputDebugString('-------------------------------------------------\n')
    discovery.serverPrint('SP: Abilities System Functioning')



# local variables:
# tab-width: 4
