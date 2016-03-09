# emacs-mode: -*- python-*-
import random
import traceback
import obj
from ability.defines import *
from combatvalidate import CanFight
import stringtable_client as StringTable
import math

def InterlockTurns(value):
    """ability mgr considers negative time values are interlock turns."""
    return -value



def d100():
    return random.range(100)



def outputToAll(msg):
    discovery.outputDebugString(msg)
    discovery.serverPrint(msg)
    discovery.clientSystemMessage(null, msg, constants.Chat.CT_SYS_IMPORTANT) #add



def outputAbilityDebug(msg):
    #if (consolevar.AbilityDebugPrint > 1):
    discovery.outputDebugString(msg)
    discovery.serverPrint(msg)
    discovery.clientSystemMessage(null, msg, constants.Chat.CT_SYS_IMPORTANT) #add



def setAbilityCombatID(sentence, combatID):
    combatIDMasked = (combatID & 255)
    sentence.result_data |= combatIDMasked



def setAbilityDataValue(sentence, value):
    result_data = sentence.result_data
    combatID = (result_data & 255)
    result_data = value
    result_data <<= 8
    result_data |= combatID
    sentence.result_data = result_data



def getAbilityName(abil):
    return abilitylib.getAbilityName(abil)



def evalContest(A, aMod, D, dMod):
    "\n    This is the basic contest of ability check. This covers combat\n    (attacker versus defender) as well as non-combat (ability versus\n    difficulty) situations.\n\n    Attacker's Value: A+aMod+d100\n    Defender's Value: D+dMod+50\n\n    Attacker wins if his value is higher.    \n    "
    discovery.serverPrint(((((((('A ' + `A`) + '  aMod ') + `aMod`) + '  D ') + `D`) + '  dMod ') + `dMod`))
    roll = random.randrange(100)
    discovery.serverPrint(('roll ' + `roll`))
    av = ((A + aMod) + roll)
    dv = ((D + dMod) + 50)
    discovery.serverPrint(("Attacker's Value: (A+aMod+roll) " + `av`))
    discovery.serverPrint(("Defender's Value: (D+dMod+50  ) " + `dv`))
    delta = (av - dv)
    discovery.serverPrint(('delta ' + `delta`))
    return delta



def flat_distance_within(pos1, pos2, test_dist):
    x_diff = (pos1.x - pos2.x)
    z_diff = (pos1.z - pos2.z)
    return (((x_diff * x_diff) + (z_diff * z_diff)) < (test_dist * test_dist))



def SafeVal(value):
    if (value is None):
        return 0
    return value



def GetAbilityLevel(player, ability):
    if player.hasAbility[ability]:
        return SafeVal(player.abilities[ability])
    else:
        return -10000



def GetHPAL(player):
    if player.hasAbility[AwakenedAbility]:
        return (AwakenedAbility,
         GetAbilityLevel(player, AwakenedAbility))
    return (AwakenedAbility,
     0)



def Get_HPAL_Level(player):
    (ability, level,) = GetHPAL(player)
    return level



def GetToolAbility(sentence):
    type = sentence.indirectObject.type
    type_info = discovery.getTypeInfo(type)
    if type_info.has_key('ReqAbilityID'):
        return type_info['ReqAbilityID']
    else:
        discovery.serverPrint('Tool used with no ability.')
        discovery.clientSystemMessage(sentence.subject.locator, StringTable.ID_ABILITY_TOOL_FAIL, constants.Chat.CT_SYS_IMPORTANT)
        return None



def HasToolForAbility(sentence, ability):
    """ checks if there is a tool appropriate for ability in inventory, returns True or False"""
    if (sentence.subject.AI is not None):
        return SUCCESS
    tool = sentence.subject.Inventory.findToolForAbility(ability)
    if (tool is not None):
        outputToAll('Tool found in inventory with required ability')
        return SUCCESS
    else:
        outputToAll('No tool found in inventory with required ability')
        return FAILURE



def IsProgramLauncherEquipped(subject):
    if IsAnNPC(subject):
        return SUCCESS
    if subject.Inventory.hasEquippedHackerItem():
        return SUCCESS
    else:
        discovery.serverPrint('   Program Launcher is not equipped!')
        discovery.clientSystemMessage(subject.locator, StringTable.ID_ABILITY_TOOL_FAIL, constants.Chat.CT_SYS_IMPORTANT)
        return FAILURE



def GetRandomListEntry(list):
    return list[GetRandomListSlot(list)]



def GetRandomListSlot(list):
    return random.randrange(0, len(list))



def GetEquippedWeapon(subject):
    if IsAnNPC(subject):
        return None
    else:
        return subject.Inventory.getEquippedWeaponItem()



def GetEquippedHackerItem(subject):
    if IsAnNPC(subject):
        return None
    else:
        return subject.Inventory.getEquippedHackerItem()



def SetItem(subject, item, slot):
    if (IsAnNPC(subject) and (slot == 109)):
        subject.setWeapon(item.type)
        return None
    else:
        subject.Inventory.setItem(item, slot)



def GetRandEquipedItemFromInventory(subject):
    if subject.Inventory:
        validItemSlots = subject.Inventory.getEquippedItems()
        if (not validItemSlots):
            return validItemSlots
        return GetRandomListEntry(validItemSlots)
    else:
        outputAbilityDebug('GetRandEquipedItemFromInventory: No inventory on target.')
        return subject.Inventory



def IsACharacter(subject):
    if subject.CharMvt:
        return True
    else:
        return False



def IsAPlayer(subject):
    if IsACharacter(subject):
        if subject.Inventory:
            return True
    return False



def IsAnNPC(subject):
    if IsAPlayer(subject):
        return False
    return True



def IsAnItem(subject):
    return (IsACharacter(subject) == False)



def PerformSpecialMove(subject, defenderLocator, ability, success, level = 0, item = None):
    result = subject.Interlock.specialAttack(defenderLocator, ability, success, level, item)
    outputAbilityDebug(('Special Move Perf: %d ' % result))
    return result


BaseCombatSpecialMoveDepAttr = '\ndirectObject.locator\n'

def SendAbilityOutputToCaster(msgID, ability, caster, target, extraData = ()):
    discovery.abilityMessageToCaster(msgID, ability, caster, target, extraData)



def SendAbilityOutputToTarget(msgID, ability, caster, target, extraData = ()):
    discovery.abilityMessageToTarget(msgID, ability, caster, target, extraData)



def SendAbilityOutputToAll(msgID, ability, caster, target, extraData = ()):
    discovery.abilityMessageToAll(msgID, ability, caster, target, extraData)



def SendAbilityOutputToCasterSentence(msgID, ability, sentence, extraData = ()):
    discovery.abilityMessageToCaster(msgID, ability, sentence.subject.locator, sentence.directObject.locator, extraData)



def SendAbilityOutputToTargetSentence(msgID, ability, sentence, extraData = ()):
    discovery.abilityMessageToTarget(msgID, ability, sentence.subject.locator, sentence.directObject.locator, extraData)



def SendAbilityOutputToAllSentence(msgID, ability, sentence, extraData = ()):
    discovery.abilityMessageToAll(msgID, ability, sentence.subject.locator, sentence.directObject.locator, extraData)



def SendAbilityOutputToCasterMsg(msgID, ability, msg, extraData = ()):
    discovery.abilityMessageToCaster(msgID, ability, msg.subjectLocator, msg.directObjectLocator, extraData)



def SendAbilityOutputToTargetMsg(msgID, ability, msg, extraData = ()):
    discovery.abilityMessageToTarget(msgID, ability, msg.subjectLocator, msg.directObjectLocator, extraData)



def SendAbilityOutputToAllMsg(msgID, ability, msg, extraData = ()):
    discovery.abilityMessageToAll(msgID, ability, msg.subjectLocator, msg.directObjectLocator, extraData)



def SendDestoryItemOutputToAllMsg(abilityID, subject, directobject, itemID, send_message = True):
    if (send_message == False):
        return None
    SendAbilityOutputToAll(StringTable.ID_CLIENT_ABILITY_ITEM_DESTORY, abilityID, subject, directobject, itemID)



def SendGiveHealthResultToAll(abilityID, subject, directobject, value, send_message = True):
    if (send_message == False):
        return None
    SendAbilityOutputToAll(StringTable.ID_CLIENT_ABILITY_GIVE_HEALTH, abilityID, subject, directobject, value)



def SendTakeDamageResultToAll(result, abilityID, subject, directobject, value, send_message = True):
    if (send_message == False):
        return None
    if ((result == DEFLECTED) or (result == FAILURE)):
        SendAbilityOutputToAll(StringTable.ID_CLIENT_ABILITY_VIRUS_DEFLECTED, abilityID, subject, directobject, value)
    else:
        SendAbilityOutputToAll(StringTable.ID_CLIENT_ABILITY_TAKE_DAMAGE, abilityID, subject, directobject, value)



def GetPropertyFromAbility(ability_id, property_name):
    type_id = discovery.abilityIDToGameObjectID(ability_id)
    return discovery.getGameObjectPropValue(type_id, property_name)



def GetAbilityInfoID(ability_id):
    return GetPropertyFromAbility(ability_id, 'InfoID')



def AbilityRound(value):
    newValue = int((value + 0.5))
    if (newValue == 0):
        newValue = 1
    return newValue



def AbilityFourCCFix(val):
    return (val & 2147483647)



def ToFourCC(val):
    t = [0,
     0,
     0,
     0]
    t[0] = chr((val & 255))
    t[1] = chr(((val & 65280) >> 8))
    t[2] = chr(((val & 16711680) >> 16))
    t[3] = chr(((val & -16777216) >> 24))
    return t



def normalize(vec):
    vlen = math.sqrt((((vec.x ** 2) + (vec.y ** 2)) + (vec.z ** 2)))
    vec.x = (vec.x / vlen)
    vec.y = (vec.y / vlen)
    vec.z = (vec.z / vlen)
    return vlen



def lengthSquared(vec):
    vlen = (((vec.x ** 2) + (vec.y ** 2)) + (vec.z ** 2))
    return vlen



def length(vec):
    vlen = math.sqrt(lengthSquared(vect))
    return vlen



def dot(a, b):
    return (((a.x * b.x) + (a.y * b.y)) + (a.z * b.z))



def vec_sub(a, b):
    class temp_vec:
        __module__ = __name__

    temp = temp_vec()
    temp.x = (a.x - b.x)
    temp.y = (a.y - b.y)
    temp.z = (a.z - b.z)
    return temp



def isObjWithinFrust(basis_obj, target_obj, width):
    basis_pos = basis_obj.Position
    basis_dir = basis_obj.Orientation.BasisVector_Z
    target_pos = target_obj.Position
    vec_to_target = vec_sub(target_pos, basis_pos)
    len_to_target = normalize(vec_to_target)
    orientation_offset = dot(vec_to_target, basis_dir)
    if (orientation_offset < 0):
        return (False,
         len_to_target)
    else:
        frust_width = (width / 2)
        angle = (math.acos(orientation_offset) * (180 / math.pi))
        if (angle < width):
            return (True,
             len_to_target)
        else:
            return (False,
             len_to_target)



def GetSneakLevel(subject):
    sneak_lvl = subject.abilities[SneakGrantAbility]
    return sneak_lvl



def SneakTest(subject):
    angle = 60.0
    max_dist = 2000.0
    min_dist = 300.0
    max_sneak_lvl = 50.0
    subjectPos = subject.Position
    components = (constants.Components.PlayerCharacter)
    sneak_lvl = float(GetSneakLevel(subject))
    if (sneak_lvl > max_sneak_lvl):
        sneak_lvl = max_sneak_lvl
    dist = (min_dist + (max_dist - (max_dist * (sneak_lvl / max_sneak_lvl))))
    outputAbilityDebug(('Sneaker detection range %f meters ' % (dist / 100.0)))
    opponents = subject.PlayerCharacter.getEnemiesInRadius(dist)
    if (len(opponents) == 0):
        return 0
    noiseLevel = subject.CharMvt.NoiseLevel
    stealthLevel = subject.CharMvt.StealthLevel
    for opponent in opponents:
        if ((opponent.locator != subject.locator) and CanFight(subject, opponent)):
            (inFrust, dist,) = isObjWithinFrust(opponent, subject, angle)
            if inFrust:
                if physics.clearLine(opponent.Position, subject.Position):
                    stealthAwareness = opponent.CharMvt.StealthAwareness
                    outputAbilityDebug(('SA(%i) v.s SL(%i) NL(%i) ' % (stealthAwareness,
                     stealthLevel,
                     noiseLevel)))
                    if abilitylib.sneakTest(opponent.CharMvt.StealthAwareness, stealthLevel, noiseLevel, dist):
                        outputAbilityDebug('Sneaker Popped!')
                        SendAbilityOutputToCaster(StringTable.ID_CLIENT_ABILITY_REVEALER_SNEAKER_REVEALED, 0, opponent.locator, subject.locator, 0)
                        SendAbilityOutputToTarget(StringTable.ID_CLIENT_ABILITY_SNEAKER_SNEAKER_REVEALED, 0, opponent.locator, subject.locator, 0)
                        return 1

    return 0



def InitialSneakTest(subject):
    angle = 60.0
    max_dist = 2000.0
    min_dist = 300.0
    max_sneak_lvl = 50.0
    subjectPos = subject.Position
    components = (constants.Components.PlayerCharacter)
    sneak_lvl = float(GetSneakLevel(subject))
    if (sneak_lvl > max_sneak_lvl):
        sneak_lvl = max_sneak_lvl
    dist = (min_dist + (max_dist - (max_dist * (sneak_lvl / max_sneak_lvl))))
    outputAbilityDebug(('Sneaker detection range %f meters ' % (dist / 100.0)))
    opponents = subject.PlayerCharacter.getEnemiesInRadius(dist)
    if (len(opponents) == 0):
        return 0
    for opponent in opponents:
        if ((opponent.locator != subject.locator) and CanFight(subject, opponent)):
            (inFrust, dist,) = isObjWithinFrust(opponent, subject, angle)
            if inFrust:
                if physics.clearLine(opponent.Position, subject.Position):
                    return 1

    return 0



def GetClosestCharacter(subject, distance):
    subjectPos = subject.Position
    components = (constants.Components.CharMovement)
    outputAbilityDebug(('Finding all characters in %f meters ' % distance))
    characters = physics.getObjectsInRadius(subjectPos.x, subjectPos.y, subjectPos.z, distance, components)
    if (len(characters) == 0):
        return 0
    validCharacters = []
    characterDists = []
    index = 0
    for character in characters:
        if ((character.locator != subject.locator) and CanFight(subject, character)):
            if physics.clearLine(character.Position, subject.Position):
                characterPos = character.Position
                vector = vec_sub(characterPos, subjectPos)
                distFrom = lengthSquared(vector)
                newEntry = (distFrom,
                 index)
                characterDists.append(newEntry)
        index += 1

    if (len(characterDists) == 0):
        return None
    characterDists.sort()
    clostestCharacter = characterDists[0]
    clostestCharacterIndex = clostestCharacter[1]
    return characters[clostestCharacterIndex]



def GetLOSFriendlies(subject, distance):
    subjectPos = subject.Position
    components = (constants.Components.CharMovement)
    outputAbilityDebug(('Finding all friendly characters in %f meters ' % distance))
    characters = physics.getObjectsInRadius(subjectPos.x, subjectPos.y, subjectPos.z, distance, components)
    if (len(characters) == 0):
        return 0
    validCharacters = []
    distSquared = (distance * distance)
    for character in characters:
        if ((character.locator != subject.locator) and CanFight(subject, character)):
            if physics.clearLine(character.Position, subject.Position):
                characterPos = character.Position
                vector = vec_sub(characterPos, subjectPos)
                distFrom = lengthSquared(vector)
                if (distFrom <= distSquared):
                    validCharacters.append(character)

    return validCharacters



def GetClosestEnemyInSight(subject, distance):
    subjectPos = subject.Position
    components = (constants.Components.CharMovement)
    enemies = physics.getObjectsInRadius(subjectPos.x, subjectPos.y, subjectPos.z, distance, components)
    if (len(enemies) == 0):
        return None
    nearestEnemy = None
    nearestDistance = (distance * distance)
    for enemy in enemies:
        if subject.CharMvt.isEnemy(enemy.locator):
            outputAbilityDebug('GetClosestEnemyInSight: found a valid enemy')
            enemyPos = enemy.Position
            if physics.clearLine(subjectPos, enemyPos):
                vector = vec_sub(enemyPos, subjectPos)
                distFrom = lengthSquared(vector)
                if (distFrom <= nearestDistance):
                    nearestEnemy = enemy
                    nearestDistance = distFrom

    return nearestEnemy



def turnOffAuras(subject):
    AuraAbilities = [CombatAura1Ability,
     CombatAura2Ability,
     DeflectBullets1Ability,
     DeflectVirus1Ability,
     Miasma1Ability,
     StaticField1Ability,
     CodeShaperAbility,
     DaemonBoostAbility,
     DaemonBoost2Ability,
     ProxyTechnicianAbility]
    for abil in AuraAbilities:
        if subject.hasAbility[abil]:
            subject.AbilityInv.deactivateAbility(abil)




def GetHitPointsForLevel(level):
    return (((level - 1) * 3) + 100)



# local variables:
# tab-width: 4
