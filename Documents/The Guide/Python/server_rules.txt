# emacs-mode: -*- python-*-
import random
import traceback
import obj
import missionvalidate as mv
import combatvalidate as cv
import followvalidate as fv
import stringtable_client as ST
import ltfxmap as FX

def Get(possible, default):
    if (possible is None):
        return default
    return possible



def outputToAll(msg):
    discovery.outputDebugString(msg)
    discovery.serverPrint(msg)
    discovery.errorPrint(msg)



def exceptionCB(obj, data, tb):
    try:
        outputToAll('****************************************')
        outputToAll('Rule Exception')
        outputToAll(`obj`)
        outputToAll(`data`)
        outputToAll('** traceback **')
        if tb:
            stackTrace = traceback.extract_tb(tb)
            stackTrace.reverse()
            for tuple in stackTrace:
                outputToAll(('File: %s (%d) Function: %s' % tuple[:3]))
                outputToAll(tuple[3])

        outputToAll('****************************************')
    except:
        pass



def evalContest(A, aMod, D, dMod):
    "\n    This is the basic contest of ability check\n\n    Attacker's Value: A+aMod+d100\n    Defender's Value: D+dMod+50\n\n    Attacker wins if his value is higher.    \n    "
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



def contestDbgFeedback(client_loc, string, abil, aMod, diff, roll):
    if (consolevar.AbilityDebugPrint > 1):
        actualRoll = (((-(abil + aMod) + diff) + 50) + roll)
        discovery.clientConsolePrint(client_loc, ('%s dbg: abil(%d) + tool(%d) + roll(%d) =  (%d) v.s diff(%d) ' % (string,
         abil,
         aMod,
         actualRoll,
         ((abil + aMod) + actualRoll),
         diff)))



def GetToolAbility(sentence):
    type = sentence.indirectObject.type
    type_info = discovery.getTypeInfo(type)
    if type_info.has_key('ReqAbilityID'):
        return type_info['ReqAbilityID']
    else:
        discovery.serverPrint('Tool used with no ability.')
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_ABILITY_TOOL_FAIL, constants.Chat.CT_SYS_IMPORTANT)
        return None



def HasToolForAbility(sentence, ability):
    """ checks if there is a tool appropriate for ability in inventory, returns True or False"""
    if (sentence.subject.AI is not None):
        return SUCCESS
    tool = sentence.subject.Inventory.findToolForAbility(ability)
    if (tool is not None):
        return SUCCESS
    else:
        return FAILURE



def GetItemsMatchingType(sentence, type):
    return sentence.subject.Inventory.getBackpackItems(type)



def GetMissionItems(sentence):
    return sentence.subject.Inventory.getMissionItems(sentence.subject.MissionKey)



def HasMissionKeyItem(sentence, type = 0):
    if (type != 0):
        item_list = GetItemsMatchingType(sentence, type)
    else:
        item_list = GetMissionItems(sentence)
    if (len(item_list) == 0):
        return FAILURE
    for eachItem in item_list:
        if mv.ValidMissionKeyMatch(eachItem.MissionKey, sentence.directObject.MissionKey):
            return SUCCESS

    discovery.clientConsolePrint('The key is not for this mission.')
    return FAILURE


HasMissionKeyItem.depAttr = '\ndirectObject.MissionKey\n'

def GeneralSuccess(sentence):
    '\n    This rule is just a pass-thru success!\n    '
    sentence.result = SUCCESS


GeneralSuccess.ID = 1000
GeneralSuccess.depAttr = '\n'

def GeneralSuccessBreakStealth(sentence):
    '\n    This rule is just a pass-thru success!\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


GeneralSuccessBreakStealth.ID = 1007
GeneralSuccessBreakStealth.depAttr = '\n'

def GeneralFailure(sentence):
    '\n    This rule is just a pass-thru failure!\n    '
    sentence.result = FAILURE


GeneralFailure.ID = 1001
GeneralFailure.depAttr = '\n'

def BreakExclusiveAbility(subject):
    if (subject.AbilityInv.CurExclusiveAbility != InvalidAbility):
        subject.AbilityInv.deactivateAbility(subject.AbilityInv.CurExclusiveAbility)



def BreakShadowObject(subject):
    if subject.AbilityInv.hasTempMod(MasterShadowActiveAbility):
        subject.AbilityInv.deactivateAbility(MasterShadowActiveAbility)



def ContainerOpen(sentence):
    NotExclusive = 0
    TeamExclusive = 1
    IndividualExclusive = 2
    OwnTeamExclusive = 3
    PermanentIndividualExclusive = 4
    TrapTriggered = 2
    Exclusive = 3
    BreakShadowObject(sentence.subject)
    if (sentence.directObject.ExclusiveType == TeamExclusive):
        if (sentence.directObject.ExclusiveLocator != sentence.subject.MissionTeamObjectLocator):
            discovery.clientSystemMessage(sentence.subject.locator, ST.ID_CONTAINER_SEARCH_EXCLUSIVE, constants.Chat.CT_SYS_INVENTORY_MANAGEMENT_FAILURE)
            sentence.result = Exclusive
            return 
    elif (sentence.directObject.ExclusiveType == IndividualExclusive):
        if (sentence.directObject.ExclusiveLocator != sentence.subject.locator):
            discovery.clientSystemMessage(sentence.subject.locator, ST.ID_CONTAINER_SEARCH_EXCLUSIVE, constants.Chat.CT_SYS_INVENTORY_MANAGEMENT_FAILURE)
            sentence.result = Exclusive
            return 
    elif (sentence.directObject.ExclusiveType == OwnTeamExclusive):
        if (not mv.ValidMissionKeyBaseMatch(sentence.directObject.MissionKey, sentence.subject.MissionKey)):
            discovery.clientSystemMessage(sentence.subject.locator, ST.ID_CONTAINER_SEARCH_EXCLUSIVE, constants.Chat.CT_SYS_INVENTORY_MANAGEMENT_FAILURE)
            sentence.result = Exclusive
            return 
    elif (sentence.directObject.ExclusiveType == PermanentIndividualExclusive):
        if (sentence.directObject.ExclusiveLocator != sentence.subject.locator):
            discovery.clientSystemMessage(sentence.subject.locator, ST.ID_CONTAINER_SEARCH_EXCLUSIVE, constants.Chat.CT_SYS_INVENTORY_MANAGEMENT_FAILURE)
            sentence.result = Exclusive
            return 
    BreakExclusiveAbility(sentence.subject)
    if (sentence.directObject.TrapArmed == 1):
        sentence.result = TrapTriggered
        return 
    sentence.result = SUCCESS


ContainerOpen.ID = 1010
ContainerOpen.depAttr = '\ndirectObject.MissionKey\ndirectObject.ExclusiveLocator\ndirectObject.ExclusiveType\ndirectObject.TrapArmed\n'

def ContainerClose(sentence):
    '\n    for now, this rule is just a pass-thru success!\n    '
    sentence.result = SUCCESS


ContainerClose.ID = 1011
ContainerClose.depAttr = '\n'

def SecurityPBXDisable(sentence):
    "\n    This rule checks the attempt to disable a security device. The quality\n    of the tool used to disable the device is taken into account\n    rule :\n    Disable - Security = Outcome\n    DisableDC = Disable Security Devices\n    Ability Lvl + Disable Mods + (1 to 100) roll\n    Security = Security System's Difficulty Lvl + Security Mods + 50\n    \n    If Outcome < -15 then\n      ALARM TRIGGERED, CONTROL BOX DEACTIVATED\n    If Outcome >= 0 then\n      SYSTEM ACCESS GRANTED\n    else NOTHING (Access Denied)\n    "
    DSD_ACCESS_GRANTED = 1
    DSD_ALARMTRIGGERED = 2
    if (not sentence.subject.abilities[DisableSecurityDevicesAbility]):
        sentence.subject.AbilityInv.sendChat('SecurityPBX', 'Operation failed! Make sure you have the Disable Security Devices ability loaded.')
        sentence.result = 0
        return 
    my_abil = sentence.subject.abilities[SecuritySystemsAbility]
    if (not HasToolForAbility(sentence, DisableSecurityDevicesAbility)):
        sentence.subject.AbilityInv.sendChat('SecurityPBX', 'Operation failed! Make sure you have a disable device tool in your inventory.')
        sentence.result = 0
        return 
    if (sentence.directObject.Difficulty == None):
        print 'Target is not a security Device '
    BreakExclusiveAbility(sentence.subject)
    diff = sentence.directObject.Difficulty
    sentence.result = evalContest(my_abil, 0, diff, 0)
    out = ('Contest : %d v.s %d = %d ' % (my_abil,
     diff,
     sentence.result))
    contestDbgFeedback(sentence.subject.locator, 'SecurityPBX', my_abil, 0, diff, sentence.result)
    if (consolevar.AbilityDebugPrint > 1):
        sentence.subject.AbilityInv.sendChat('SecurityPBX', out)
    if (sentence.result < -15):
        sentence.result = DSD_ALARMTRIGGERED
        sentence.subject.AbilityInv.sendChat('SecurityPBX', 'ALARM TRIGGERED')
    else:
        sentence.result = DSD_ACCESS_GRANTED
        sentence.subject.AbilityInv.sendChat('SecurityPBX', 'ACCESS GRANTED')
    level = sentence.subject.PlayerCharacter.getLevel()
    if (level != 1):
        level = (level - 1)
        multiplier = consolevar.WeaklingKillMultiplier
    experience = int((multiplier + (consolevar.XPKnob * (((level * multiplier) * consolevar.XPConstantMultiplier) - multiplier))))
    sentence.subject.PlayerCharacter.addExperience(experience, constants.RST.DISABLEDEVICE)


SecurityPBXDisable.ID = 1012
SecurityPBXDisable.depAttr = '\nindirectObject.type\nindirectObject.Quality\ndirectObject.Difficulty\n'

def DoorPickLock(sentence):
    '\n    This rule implements the attempt to pick a lock. Lock picks always succeed\n    after the progress bar has finished.\n    '
    if (not sentence.subject.hasAbility[OpenLocksAbility]):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_PICK_LOCK_ABILITY_FAILED, OpenLocksAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE
        return 
    if (not HasToolForAbility(sentence, OpenLocksAbility)):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_PICK_LOCK_TOOL_FAILED, OpenLocksAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE
        return 
    BreakExclusiveAbility(sentence.subject)
    sentence.subject.CharMvt.playNamedScriptWithTarget(Stance_Stand, 'stand_emote_pickupdesk', sentence.directObject.locator, 0)
    discovery.abilityMessageToCaster(ST.ID_CLIENT_PICK_LOCK_SUCCESS, OpenLocksAbility, sentence.subject.locator, sentence.directObject.locator, 0)
    sentence.result = SUCCESS
    level = sentence.subject.PlayerCharacter.getLevel()
    if (level != 1):
        level = (level - 1)
        multiplier = consolevar.WeaklingKillMultiplier
    experience = int((multiplier + (consolevar.XPKnob * (((level * multiplier) * consolevar.XPConstantMultiplier) - multiplier))))
    sentence.subject.PlayerCharacter.addExperience(experience, constants.RST.LOCKPICK)
    return 
    if HasToolForAbility(sentence, OpenLocksAbility):
        tool = sentence.subject.Inventory.findToolForAbility(OpenLocksAbility)
        aMod = tool.Quality
        if (aMod == None):
            aMod = 0
    else:
        discovery.abilityMessageToCaster(ST.ID_CLIENT_PICK_LOCK_TOOL_FAILED, OpenLocksAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE
        return 
    aMod = 0
    abil = 0
    if sentence.subject.hasAbility[LockPickingAbility]:
        abil += sentence.subject.abilities[LockPickingAbility]
    diff = (Get(sentence.directObject.Difficulty, 0) * 4)
    dMod = 0
    discovery.serverPrint('ab, am, diff, dm')
    discovery.serverPrint(`abil`)
    discovery.serverPrint(`aMod`)
    discovery.serverPrint(`diff`)
    discovery.serverPrint(`dMod`)
    roll = evalContest(abil, aMod, diff, dMod)
    contestDbgFeedback(sentence.subject.locator, 'OpenLock', abil, aMod, diff, roll)
    if (roll > 0):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_PICK_LOCK_SUCCESS, OpenLocksAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = SUCCESS
    else:
        discovery.abilityMessageToCaster(ST.ID_CLIENT_PICK_LOCK_FAILED, OpenLocksAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE


DoorPickLock.ID = 4000
DoorPickLock.depAttr = '\nindirectObject.Quality\nindirectObject.ReqAbilityID\ndirectObject.Difficulty\ndirectObject.locator\n'

def Repair(sentence):
    '\n    Just pass SUCCESS\n    '
    sentence.result = SUCCESS
    BreakExclusiveAbility(sentence.subject)


Repair.ID = 1337
Repair.depAttr = '\n'

def GenericOpen(sentence):
    '\n    Just pass SUCCESS\n    '
    NeedsRepairs = 2
    if ((sentence.directObject.Broken == 1) and (sentence.directObject.Repaired == 0)):
        sentence.result = NeedsRepairs
        return 
    sentence.result = SUCCESS
    BreakShadowObject(sentence.subject)


GenericOpen.ID = 1338
GenericOpen.depAttr = '\ndirectObject.Broken\ndirectObject.Repaired\n'

def GenericClose(sentence):
    '\n    Just pass SUCCESS\n    '
    BreakShadowObject(sentence.subject)
    sentence.result = SUCCESS


GenericClose.ID = 1339
GenericClose.depAttr = '\n'

def DoorOpenGeneric(sentence):
    '\n    This rule enforces that a door that has been locked to a specific\n    mission team may only be opened by them.\n    '
    BreakShadowObject(sentence.subject)
    DoorAlreadyOpen = 3
    if (sentence.directObject.IsOpen == True):
        sentence.result = DoorAlreadyOpen
        return 
    playerkey = sentence.subject.MissionKey
    if ((playerkey != mv.NON_ASSIGNABLE_MISSIONKEY) and (not mv.ValidMissionKeyBaseMatch(sentence.directObject.MissionKey, playerkey))):
        return 
    TrapTriggered = 2
    if (sentence.directObject.TrapArmed == 1):
        sentence.result = TrapTriggered
        BreakExclusiveAbility(sentence.subject)
        return 
    sentence.result = SUCCESS


DoorOpenGeneric.ID = 4004
DoorOpenGeneric.depAttr = '\ndirectObject.MissionKey\ndirectObject.TrapArmed\ndirectObject.IsOpen\n'

def DoorCloseTest(sentence):
    '\n    This rule simply returns success\n    '
    BreakShadowObject(sentence.subject)
    sentence.result = SUCCESS


DoorCloseTest.ID = 4002
DoorCloseTest.depAttr = '\n'

def DoorLockTest(sentence):
    '\n    This rule returns success if the proper key is in inventory\n    '
    TrapTriggered = 2
    if (sentence.directObject.TrapArmed == 1):
        sentence.result = TrapTriggered
        BreakExclusiveAbility(sentence.subject)
        return 
    if HasMissionKeyItem(sentence):
        sentence.result = SUCCESS
        BreakExclusiveAbility(sentence.subject)
        return 
    discovery.abilityMessageToCaster(ST.ID_CLIENT_UNLOCK_FAILED, AwakenedAbility, sentence.subject.locator, sentence.directObject.locator, 0)


DoorLockTest.ID = 4003
DoorLockTest.depAttr = HasMissionKeyItem.depAttr
DoorLockTest.depAttr += '\ndirectObject.TrapArmed\n'

def CardKeyTest(sentence):
    '\n    This rule simply returns success if the player has the correct cardkey\n    old function?\n    '
    if HasMissionKeyItem(sentence, obj.CardKey):
        sentence.result = SUCCESS
        BreakExclusiveAbility(sentence.subject)
        return 


CardKeyTest.ID = 4005
CardKeyTest.depAttr = HasMissionKeyItem.depAttr

def GenericKeyTest(sentence):
    '\n    This rule returns success if the proper key is in inventory\n    '
    if HasMissionKeyItem(sentence):
        sentence.result = SUCCESS
        BreakExclusiveAbility(sentence.subject)
        return 
    discovery.abilityMessageToCaster(ST.ID_CLIENT_UNLOCK_FAILED, AwakenedAbility, sentence.subject.locator, sentence.directObject.locator, 0)


GenericKeyTest.ID = 4006
GenericKeyTest.depAttr = HasMissionKeyItem.depAttr

def TrapDisarm(sentence):
    '\n    This rule implements the attempt to disarm a trap.\n    '
    DisarmFailure = 2
    DisarmFailureAndTrigger = 3
    abil = (4 * sentence.subject.abilities[DisarmTrapsAbility])
    if (abil < 1):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, "You need the 'Disarm Traps' ability.")
        discovery.clientConsolePrint(sentence.subject.locator, 'Hint: in the console, type \'AddAbility "DisarmTrapsAbility"\'')
        sentence.result = FAILURE
        return 
    diff = (Get(sentence.directObject.Difficulty, 0) * 4)
    dMod = 0
    aMod = 0
    discovery.serverPrint('ab, am, diff, dm')
    discovery.serverPrint(`abil`)
    discovery.serverPrint(`aMod`)
    discovery.serverPrint(`diff`)
    discovery.serverPrint(`dMod`)
    roll = evalContest(abil, aMod, diff, dMod)
    contestDbgFeedback(sentence.subject.locator, 'DisarmTraps', abil, aMod, diff, roll)
    discovery.clientConsolePrint(sentence.subject.locator, ('Attempted to disarm a trap, rolled ' + str(roll)))
    BreakExclusiveAbility(sentence.subject)
    if (roll > 0):
        discovery.clientConsolePrint(sentence.subject.locator, 'Trap Disarmed Successfully!')
        sentence.result = SUCCESS
    else:
        trigger_roll = random.randrange(100)
        if (abil > trigger_roll):
            discovery.clientConsolePrint(sentence.subject.locator, 'Trap Disarm unsuccessful')
            sentence.result = DisarmFailure
        else:
            discovery.clientConsolePrint(sentence.subject.locator, 'Trap Disarm unsuccessful and Trap went off!')
            sentence.result = DisarmFailureAndTrigger


TrapDisarm.ID = 4010
TrapDisarm.depAttr = '\ndirectObject.Difficulty\n'

def ComputerHack(sentence):
    '\n    Hacking a computer always succeeds (after the progress bar completes) as long\n    as the player has the Hacker ability loaded\n    '
    baseAbil = Get(sentence.subject.abilities[HackerAbility], 0)
    if (baseAbil < 1):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_HACK_COMPUTER_ABILITY_FAILED, HackerAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE
        return 
    discovery.abilityMessageToCaster(ST.ID_CLIENT_HACK_COMPUTER_SUCCESS, HackerAbility, sentence.subject.locator, sentence.directObject.locator, 0)
    sentence.result = SUCCESS
    level = sentence.subject.PlayerCharacter.getLevel()
    if (level != 1):
        level = (level - 1)
    multiplier = consolevar.WeaklingKillMultiplier
    experience = int((multiplier + (consolevar.XPKnob * (((level * multiplier) * consolevar.XPConstantMultiplier) - multiplier))))
    sentence.subject.PlayerCharacter.addExperience(experience, constants.RST.HACKCOMPUTER)
    BreakExclusiveAbility(sentence.subject)
    return 
    computerDiff = (Get(sentence.directObject.Difficulty, 0) * 4)
    playerAbil = (Get(sentence.subject.abilities[ComputerHackingAbility], 0) * 4)
    baseAbil = (Get(sentence.subject.abilities[HackerAbility], 0) * 4)
    if ((playerAbil < 1) or (baseAbil < 1)):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_HACK_COMPUTER_ABILITY_FAILED, HackerAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE
        return 
    roll = evalContest(playerAbil, 0, computerDiff, 0)
    contestDbgFeedback(sentence.subject.locator, 'HackComputer', playerAbil, 0, computerDiff, roll)
    if (roll > 0):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_HACK_COMPUTER_SUCCESS, HackerAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = SUCCESS
    else:
        discovery.abilityMessageToCaster(ST.ID_CLIENT_HACK_COMPUTER_FAILED, HackerAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE


ComputerHack.ID = 1002
ComputerHack.depAttr = '\ndirectObject.Difficulty\ndirectObject.locator\ndirectObject.Exclusive\n'

def ComputerInfect(sentence):
    '\n    Succeed if we have a computer virus which\n    matches our mission key.\n    '
    if HasMissionKeyItem(sentence, obj.ComputerVirus):
        sentence.result = SUCCESS
        BreakExclusiveAbility(sentence.subject)
        return 


ComputerInfect.ID = 1003
ComputerInfect.depAttr = HasMissionKeyItem.depAttr

def FileDestroyRecords(sentence):
    '\n    Always succeed.\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


FileDestroyRecords.ID = 1004
FileDestroyRecords.depAttr = '\n'

def SendMissionText(sentence):
    '\n    Called when an object should disgorge its mission specific text\n    '
    sentence.result = SUCCESS


SendMissionText.ID = 1005
SendMissionText.depAttr = '\n'

def SendMissionTextBreakStealth(sentence):
    '\n    Called when an object should disgorge its mission specific text\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


SendMissionTextBreakStealth.ID = 1006
SendMissionTextBreakStealth.depAttr = '\n'

def TestInvPickup(sentence):
    "\n    Return SUCCESS if the item can be picked up and put into the player's inventory.\n    Currently just always returns success.\n    "
    type = sentence.directObject.type
    singleton = discovery.getGameObjectPropValue(type, 'Singleton')
    if ((singleton is not None) and ((singleton != 0) and sentence.subject.Inventory.hasItem(type))):
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_INVENTORY_SINGLETON_DUPE)
        sentence.result = FAILURE
        return 
    if mv.ValidMissionKeyBaseMatch(sentence.directObject.MissionKey, sentence.subject.MissionKey):
        sentence.result = SUCCESS
        BreakExclusiveAbility(sentence.subject)
    else:
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_SYSTEM_MESSAGE_MISSION_KEY_MISMATCH)
        sentence.result = FAILURE


TestInvPickup.ID = 10001
TestInvPickup.depAttr = '\ndirectObject.MissionKey\ndirectObject.type\n'

def TestHeavyLuggablePickup(sentence):
    "\n    Return SUCCESS if the item can be picked up and put into the player's inventory.\n    Currently just always returns success.\n    "
    if (Get(sentence.subject.abilities[HyperStrengthAbility], 0) == 0):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_PICKUP_FAILED, HyperStrengthAbility, sentence.subject.locator, sentence.directObject.locator, 0)
        sentence.result = FAILURE
        return 
    sentence.result = SUCCESS
    BreakExclusiveAbility(sentence.subject)


TestHeavyLuggablePickup.ID = 10003
TestHeavyLuggablePickup.depAttr = '\ndirectObject.locator\n'

def TestLightLuggablePickup(sentence):
    "\n    Return SUCCESS if the item can be picked up and put into the player's inventory.\n    "
    type = sentence.directObject.type
    singleton = discovery.getGameObjectPropValue(type, 'Singleton')
    if (sentence.directObject.CurrentState == 2112):
        sentence.result = FAILURE
        return 
    if ((singleton is not None) and ((singleton != 0) and sentence.subject.Inventory.hasItem(type))):
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_INVENTORY_SINGLETON_DUPE)
        sentence.result = FAILURE
        return 
    if ((sentence.directObject.ReqCharLevel is not None) and (sentence.directObject.ReqCharLevel > sentence.subject.Level)):
        discovery.abilityMessageToCaster(ST.ID_CLIENT_PICKUP_LEVEL_FAILED, 0, sentence.subject.locator, sentence.directObject.locator, sentence.directObject.ReqCharLevel)
        sentence.result = FAILURE
        return 
    i = 1
    exclusiveID = discovery.getGameObjectPropValue(type, ('PickupExclusive%d' % i))
    while (exclusiveID is not None):
        if sentence.subject.Inventory.hasItem(exclusiveID):
            discovery.clientSystemMessage(sentence.subject.locator, ST.ID_INVENTORY_SINGLETON_DUPE)
            sentence.result = FAILURE
            return 
        i += 1
        exclusiveID = discovery.getGameObjectPropValue(type, ('PickupExclusive%d' % i))

    sentence.result = SUCCESS
    BreakExclusiveAbility(sentence.subject)


TestLightLuggablePickup.ID = 10004
TestLightLuggablePickup.depAttr = '\ndirectObject.locator\ndirectObject.ReqCharLevel\ndirectObject.type\n'

def TestLuggableRelease(sentence):
    "\n    Return SUCCESS if the item can be picked up and put into the player's inventory.\n    "
    type = sentence.directObject.type
    if (sentence.directObject.UniqueID == 0):
        sentence.result = FAILURE
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_OBJECT_LUGGABLE_RELEASE_NO_OWNER, type)
    else:
        sentence.result = SUCCESS
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_OBJECT_LUGGABLE_RELEASE_SUCCESS, type)


TestLuggableRelease.ID = 10007
TestLuggableRelease.depAttr = '\ndirectObject.type\ndirectObject.UniqueID\n'

def InfoPickup(sentence):
    '\n    Return SUCCESS if the info item can be picked up.\n    Currently just always returns success.\n    '
    sentence.result = SUCCESS


InfoPickup.ID = 10002
InfoPickup.depAttr = '\n'

def SwitchOn(sentence):
    '\n    This rule is just a pass-thru success!\n    '
    BreakShadowObject(sentence.subject)
    sentence.result = SUCCESS


SwitchOn.ID = 10005
SwitchOn.depAttr = '\n'

def SwitchOff(sentence):
    '\n    This rule is just a pass-thru success!\n    '
    BreakShadowObject(sentence.subject)
    sentence.result = SUCCESS


SwitchOff.ID = 10006
SwitchOff.depAttr = '\n'

def MissionTeam_RequestJoin(sentence):
    '\n    Another Player has asked me to join a mission team.\n    '
    discovery.serverPrint('Someone asked me to join a mission team!')
    sentence.result = SUCCESS


MissionTeam_RequestJoin.ID = 10010
MissionTeam_RequestJoin.depAttr = '\n'

def HardlineExit(sentence):
    '\n    Return SUCCESS if the player can exit via this hardline.\n    Currently just always returns success.\n    '
    sentence.result = SUCCESS


HardlineExit.ID = 10020
HardlineExit.depAttr = '\ndirectObject.locator\n'

def HardlineSync(sentence):
    '\n    Return SUCCESS if the player can upload via this hardline.\n    Currently just always returns success.\n    '
    BreakShadowObject(sentence.subject)
    discovery.addHardline(sentence.directObject.locator, sentence.subject.ObjectServerID, sentence.subject.CharacterID, 1)
    sentence.result = SUCCESS


HardlineSync.ID = 10040
HardlineSync.depAttr = '\ndirectObject.locator\n'

def HardlineUpload(sentence):
    '\n    Return SUCCESS if the player can upload via this hardline.\n    Currently just always returns success.\n    '
    BreakShadowObject(sentence.subject)
    sentence.result = SUCCESS


HardlineUpload.ID = 10021
HardlineUpload.depAttr = '\ndirectObject.locator\n'

def HardlineExitToLoadingArea(sentence):
    '\n    Return SUCCESS if the player can exit via this hardline.\n    Currently just always returns success.\n    '
    sentence.result = SUCCESS


HardlineExitToLoadingArea.ID = 10022
HardlineExitToLoadingArea.depAttr = '\ndirectObject.locator\n'

def HardlineEnterConstruct(sentence):
    '\n    Return SUCCESS if the player can enter constructs via this hardline.\n    '
    if (sentence.subject.FactionID == 0):
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_HARDLINE_ENTER_CONSTRUCT_FAIL)
        sentence.result = FAILURE
        return 
    sentence.result = SUCCESS


HardlineEnterConstruct.ID = 10023
HardlineEnterConstruct.depAttr = '\ndirectObject.locator\n'

def HardlineHackConstruct(sentence):
    '\n    Return SUCCESS if the player can hack via this hardline.\n    '
    if (sentence.subject.FactionFlags & 16):
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_HACK_CONSTRUCT_FAIL_INPROGRESS)
        sentence.result = FAILURE
        return 
    print 'Hardline Hack ability = ',
    print sentence.subject.abilities[HackConstructKeyAbility]
    if (Get(sentence.subject.abilities[HackConstructKeyAbility], 0) == 0):
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_HARDLINE_HACK_CONSTRUCT_ABILITY_FAIL, constants.Chat.CT_SYS_IMPORTANT)
        sentence.result = FAILURE
        return 
    if (sentence.subject.FactionID == 0):
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_HARDLINE_HACK_CONSTRUCT_FACTION_FAIL)
        sentence.result = FAILURE
        return 
    print 'infocost = ',
    print consolevar.HackConstructInfoCost,
    print 'info = ',
    print sentence.subject.Information
    if (consolevar.HackConstructInfoCost > sentence.subject.Information):
        discovery.clientSystemMessage(sentence.subject.locator, ST.ID_HARDLINE_HACK_CONSTRUCT_INFO_FAIL)
        sentence.result = FAILURE
        print 'Not enough information'
        return 
    sentence.result = SUCCESS


HardlineHackConstruct.ID = 10024
HardlineHackConstruct.depAttr = '\ndirectObject.locator\n'

def HardlineHackControlNodeStage1(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    sentence.result = SUCCESS


HardlineHackControlNodeStage1.ID = 10025
HardlineHackControlNodeStage1.depAttr = '\n'

def HardlineHackControlNodeStage2(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    sentence.result = SUCCESS


HardlineHackControlNodeStage2.ID = 10026
HardlineHackControlNodeStage2.depAttr = '\n'

def HardlineHackControlNodeStage3(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    sentence.result = SUCCESS


HardlineHackControlNodeStage3.ID = 10027
HardlineHackControlNodeStage3.depAttr = '\n'

def HardlineHackControlNodeClaimConstruct(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    print 'Claim Construct Rule succeeded'
    sentence.result = rs.claimConstruct(sentence.subject.FactionObjectLocator, sentence.subject.FactionName, sentence.subject.FactionID, sentence.directObject.locator)


HardlineHackControlNodeClaimConstruct.ID = 10028
HardlineHackControlNodeClaimConstruct.depAttr = '\ndirectObject.locator\n'

def HardlineEnableControlNodeStage1(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    sentence.result = SUCCESS


HardlineEnableControlNodeStage1.ID = 10029
HardlineEnableControlNodeStage1.depAttr = '\n'

def HardlineEnableControlNodeStage2(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    sentence.result = SUCCESS


HardlineEnableControlNodeStage2.ID = 10030
HardlineEnableControlNodeStage2.depAttr = '\n'

def HardlineEnableControlNodeStage3(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    sentence.result = SUCCESS


HardlineEnableControlNodeStage3.ID = 10031
HardlineEnableControlNodeStage3.depAttr = '\n'

def ConstructConfigure(sentence):
    '\n    Return SUCCESS if the player can configure constructs via control node.\n    '
    if (sentence.subject.FactionID == sentence.directObject.FactionID):
        sentence.result = SUCCESS


ConstructConfigure.ID = 10032
ConstructConfigure.depAttr = '\ndirectObject.FactionID\n'

def TagAccessNode(sentence):
    '\n    Return SUCCESS if the player can tag an Access Node.\n    '
    discovery.addAccessNode(sentence.directObject.locator, sentence.subject.ObjectServerID, sentence.subject.CharacterID, sentence.directObject.SoftBoundaryID)
    sentence.result = SUCCESS


TagAccessNode.ID = 10033
TagAccessNode.depAttr = '\ndirectObject.locator\ndirectObject.SoftBoundaryID\n'

def TutorialExitPtExit(sentence):
    "\n    This rule is just a pass-thru success!\n    For Tutorial Exit Point (needs two success pass-thrus,\n    so GeneralSuccess can't be used!)\n    "
    sentence.result = SUCCESS


TutorialExitPtExit.ID = 10034
TutorialExitPtExit.depAttr = '\n'

def TutorialExitPtExitToLoadingArea(sentence):
    "\n    This rule is just a pass-thru success!\n    For Tutorial Exit Point (needs two success pass-thrus,\n    so GeneralSuccess can't be used!)\n    "
    sentence.result = SUCCESS


TutorialExitPtExitToLoadingArea.ID = 10035
TutorialExitPtExitToLoadingArea.depAttr = '\n'

def TutorialExitPtJackIntoTheMatrix(sentence):
    "\n    This rule is just a pass-thru success!\n    For Tutorial Exit Point (needs two success pass-thrus,\n    so GeneralSuccess can't be used!)\n    "
    sentence.result = SUCCESS


TutorialExitPtJackIntoTheMatrix.ID = 10037
TutorialExitPtJackIntoTheMatrix.depAttr = '\n'

def TutorialExitPtUpload(sentence):
    '\n    Return SUCCESS if the player can upload via this Tutorial Exit Point.\n    Currently just always returns success.\n    '
    sentence.result = SUCCESS


TutorialExitPtUpload.ID = 10038
TutorialExitPtUpload.depAttr = '\ndirectObject.locator\n'

def TestContainerPut(sentence):
    "\n    This rule puts the player's equipped item into a container\n\n    S:  Player Character\n    IO: item\n    DO: container\n    "
    sentence.result = SUCCESS


TestContainerPut.ID = 7000
TestContainerPut.depAttr = '\n'

def TestContainerGet(sentence):
    '\n    This rule gets the selected item from a container\n\n    S:  Player Character\n    IO: item\n    DO: container\n    '
    discovery.serverPrint(`sentence.indirectObject`)
    if (not sentence.indirectObject):
        sentence.result = FAILURE
        discovery.clientConsolePrint(sentence.subject.locator, "You've got to select the thing you want to drop in the receptacle")
        return 
    sentence.result = SUCCESS


TestContainerGet.ID = 7001
TestContainerGet.depAttr = '\n'

def TestContainerGetAll(sentence):
    '\n    This rule gets all items from a container\n\n    S:  Player Character\n    IO: item\n    DO: container\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


TestContainerGetAll.ID = 7002
TestContainerGetAll.depAttr = '\n'

def TestMissionContainerPut(sentence):
    '\n    This rule confirms the mission keys match and then calls TestContainerPut\n\n    S:  Player Character\n    IO: item\n    DO: container\n    '
    if sentence.indirectObject:
        if sentence.directObject:
            if mv.ValidMissionKeyMatch(sentence.directObject.MissionKey, sentence.indirectObject.instData):
                BreakExclusiveAbility(sentence.subject)
                sentence.result = SUCCESS


TestMissionContainerPut.ID = 7003
TestMissionContainerPut.depAttr = '\nindirectObject.MissionKey\ndirectObject.MissionKey\n'

def TestMissionContainerPhoto(sentence):
    '\n    This rule confirms the mission keys match and then calls TestContainerPut\n\n    S:  Player Character\n    IO: item\n    DO: container\n    '
    if HasMissionKeyItem(sentence, obj.DigitalCamera):
        sentence.result = SUCCESS
        BreakExclusiveAbility(sentence.subject)
        return 


TestMissionContainerPhoto.ID = 7005
TestMissionContainerPhoto.depAttr = HasMissionKeyItem.depAttr

def ReceptacleDropTest(sentence):
    '\n    This rule checks to see if the item dropped in the receptacle\n    matches the item we\'re looking for.\n\n    Note: here\'s an exception to the intuitive mapping of English\n    sentences into our protocol.\n\n    S:  Player Character\n    IO: Secret Plans\n    DO: Receptacle\n\n    This doesn\'t match how you\'d put the sentence together. You\'d\n    probably say "I give the plans to the spy", but the contrived\n    expression that more matches our protocol is "I present the spy\n    with the plans". The reason we do this is because the thing in\n    your inventory is ALWAYS the IO.\n\n    '
    playerTeam = sentence.subject.MissionTeamObjectLocator
    discovery.serverPrint(`sentence.indirectObject`)
    if (not sentence.indirectObject):
        sentence.result = FAILURE
        discovery.clientConsolePrint(sentence.subject.locator, "You've got to enable the thing you want to drop in the receptacle")
        return 
    discovery.sendMissionResult(playerTeam, sentence.indirectObject)
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


ReceptacleDropTest.ID = 5999
ReceptacleDropTest.depAttr = '\n'

def CompileCode(sentence):
    '\n    This rule implements the attempt to compile code. The quality of\n    the decomp tool acts as a bonus to the character. The complexity\n    of the code is what the roll must beat.\n    '
    BreakShadowObject(sentence.subject)
    abil = (sentence.subject.abilities[CompileAbility] * 4)
    if (abil < 1):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, "You need the 'Compile' ability.")
        discovery.clientConsolePrint(sentence.subject.locator, 'Hint: in the console, type \'AddAbility "CompileAbility"\'')
        sentence.result = FAILURE
        return 
    if sentence.indirectObject:
        aMod = sentence.indirectObject.Quality
        aClass = sentence.indirectObject.Class
        discovery.serverPrint(('tool quality ' + `aMod`))
        discovery.serverPrint(('tool class ' + `aClass`))
    else:
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You need a Decomp Tool equipped to compile code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Decomp Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    if (not (aClass == 4001)):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You have equipped the wrong tool. You need a Decomp Tool equipped to compile code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Decomp Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    diff = Get(sentence.directObject.Difficulty, 0)
    dMod = 0
    discovery.serverPrint('ab, am, diff, dm')
    discovery.serverPrint(`abil`)
    discovery.serverPrint(`aMod`)
    discovery.serverPrint(`diff`)
    discovery.serverPrint(`dMod`)
    roll = evalContest(abil, aMod, diff, dMod)
    discovery.clientConsolePrint(sentence.subject.locator, ('Attempted to compile code, rolled ' + str(roll)))
    if (roll > 0):
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Compiled Successfully!')
        sentence.result = SUCCESS
    else:
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Compile unsuccessful')
        sentence.result = FAILURE


CompileCode.ID = 6001
CompileCode.depAttr = '\ndirectObject.Difficulty\n'

def DecompileCode(sentence):
    '\n    This rule implements the attempt to decompile code. The quality of\n    the decomp tool acts as a bonus to the character. The complexity\n    of the code is what the roll must beat.\n    '
    BreakShadowObject(sentence.subject)
    abil = (sentence.subject.abilities[DecompileAbility] * 4)
    if (abil < 1):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, "You need the 'Decompile' ability.")
        discovery.clientConsolePrint(sentence.subject.locator, 'Hint: in the console, type \'AddAbility "DecompileAbility"\'')
        sentence.result = FAILURE
        return 
    if sentence.indirectObject:
        aMod = sentence.indirectObject.Quality
        aClass = sentence.indirectObject.Class
        discovery.serverPrint(('tool quality ' + `aMod`))
        discovery.serverPrint(('tool class ' + `aClass`))
    else:
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You need a Decomp Tool equipped to compile code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Decomp Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    if (not (aClass == 4001)):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You have equipped the wrong tool. You need a Decomp Tool equipped to compile code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Decomp Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    diff = Get(sentence.directObject.Complexity, 0)
    dMod = 0
    discovery.serverPrint('ab, am, diff, dm')
    discovery.serverPrint(`abil`)
    discovery.serverPrint(`aMod`)
    discovery.serverPrint(`diff`)
    discovery.serverPrint(`dMod`)
    roll = evalContest(abil, aMod, diff, dMod)
    discovery.clientConsolePrint(sentence.subject.locator, ('Attempted to decompile code, rolled ' + str(roll)))
    if (roll > 0):
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Decompiled Successfully!')
        sentence.result = SUCCESS
    else:
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Decompile unsuccessful')
        sentence.result = FAILURE


DecompileCode.ID = 6000
DecompileCode.depAttr = '\ndirectObject.Complexity\n'

def CopyCode(sentence):
    '\n    This rule implements the attempt to copy code. The quality of\n    the copy tool acts as a bonus to the character. The complexity\n    of the code is what the roll must beat.\n    '
    BreakShadowObject(sentence.subject)
    abil = sentence.subject.abilities[CopyCodeAbility]
    if (abil < 1):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, "You need the 'Copy Code' ability.")
        discovery.clientConsolePrint(sentence.subject.locator, 'Hint: in the console, type \'AddAbility "CopyCodeAbility"\'')
        sentence.result = FAILURE
        return 
    if sentence.indirectObject:
        aMod = sentence.indirectObject.Quality
        aClass = sentence.indirectObject.Class
        discovery.serverPrint(('tool quality ' + `aMod`))
        discovery.serverPrint(('tool class ' + `aClass`))
    else:
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You need a Copy Tool equipped to compile code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Copy Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    if (not (aClass == 4000)):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You have equipped the wrong tool. You need a Copy Tool equipped to compile code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Copy Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    diff = Get(sentence.directObject.Difficulty, 0)
    dMod = 0
    discovery.serverPrint('ab, am, diff, dm')
    discovery.serverPrint(`abil`)
    discovery.serverPrint(`aMod`)
    discovery.serverPrint(`diff`)
    discovery.serverPrint(`dMod`)
    roll = evalContest(abil, aMod, diff, dMod)
    discovery.clientConsolePrint(sentence.subject.locator, ('Attempted to copy code, rolled ' + str(roll)))
    if (roll > 0):
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Copied Successfully!')
        sentence.result = SUCCESS
    else:
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Copy unsuccessful')
        sentence.result = FAILURE


CopyCode.ID = 6002
CopyCode.depAttr = '\ndirectObject.Difficulty\n'

def EncryptCode(sentence):
    '\n    This rule implements the attempt to encrypt code. The quality of\n    the cryptography tool acts as a bonus to the character. The complexity\n    of the encryption is what the roll must beat.\n    '
    BreakShadowObject(sentence.subject)
    abil = (sentence.subject.abilities[CryptographyAbility] * 4)
    if (abil < 1):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, "You need the 'Cryptography' ability.")
        discovery.clientConsolePrint(sentence.subject.locator, 'Hint: in the console, type \'AddAbility "CryptographyAbility"\'')
        sentence.result = FAILURE
        return 
    if sentence.indirectObject:
        aMod = sentence.indirectObject.Quality
        aClass = sentence.indirectObject.Class
        discovery.serverPrint(('tool quality ' + `aMod`))
        discovery.serverPrint(('tool class ' + `aClass`))
    else:
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You need a Cryptography Tool equipped to encrypt code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Cryptography Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    if (not (aClass == 4004)):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You have equipped the wrong tool. You need a Cryptography Tool equipped to encrypt code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Cryptography Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    diff = Get(sentence.directObject.EncryptDifficulty, 0)
    dMod = 0
    discovery.serverPrint('ab, am, diff, dm')
    discovery.serverPrint(`abil`)
    discovery.serverPrint(`aMod`)
    discovery.serverPrint(`diff`)
    discovery.serverPrint(`dMod`)
    roll = evalContest(abil, aMod, diff, dMod)
    discovery.clientConsolePrint(sentence.subject.locator, ('Attempted to encrypt code, rolled ' + str(roll)))
    if (roll > 0):
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Encrypted Successfully!')
        sentence.result = roll
    else:
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Encrypt unsuccessful')
        sentence.result = FAILURE


EncryptCode.ID = 6003
EncryptCode.depAttr = '\ndirectObject.EncryptDifficulty\n'

def DecryptCode(sentence):
    '\n    This rule implements the attempt to encrypt code. The quality of\n    the cryptography tool acts as a bonus to the character. The complexity\n    of the encryption is what the roll must beat.\n    '
    BreakShadowObject(sentence.subject)
    abil = (sentence.subject.abilities[CryptographyAbility] * 4)
    if (abil < 1):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, "You need the 'Cryptography' ability.")
        discovery.clientConsolePrint(sentence.subject.locator, 'Hint: in the console, type \'AddAbility "CryptographyAbility"\'')
        sentence.result = FAILURE
        return 
    if sentence.indirectObject:
        aMod = sentence.indirectObject.Quality
        aClass = sentence.indirectObject.Class
        discovery.serverPrint(('tool quality ' + `aMod`))
        discovery.serverPrint(('tool class ' + `aClass`))
    else:
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You need a Decomp Tool equipped to encrypt code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Decomp Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    if (not (aClass == 4001)):
        discovery.clientConsolePrint(sentence.subject.locator, '')
        discovery.clientConsolePrint(sentence.subject.locator, 'You have equipped the wrong tool. You need a Decomp Tool equipped to decrypt code!')
        discovery.clientConsolePrint(sentence.subject.locator, 'Find a Decomp Tool in the world and then go to the inventory tab (skull), and select, then equip the tool')
        sentence.result = FAILURE
        return 
    diff = Get(sentence.directObject.DecryptDifficulty, 0)
    dMod = 0
    discovery.serverPrint('ab, am, diff, dm')
    discovery.serverPrint(`abil`)
    discovery.serverPrint(`aMod`)
    discovery.serverPrint(`diff`)
    discovery.serverPrint(`dMod`)
    roll = evalContest(abil, aMod, diff, dMod)
    discovery.clientConsolePrint(sentence.subject.locator, ('Attempted to decrypt code, rolled ' + str(roll)))
    if (roll > 0):
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Decrypted Successfully!')
        sentence.result = SUCCESS
    else:
        discovery.clientConsolePrint(sentence.subject.locator, 'Code Decrypt unsuccessful')
        sentence.result = FAILURE


DecryptCode.ID = 6004
DecryptCode.depAttr = '\ndirectObject.DecryptDifficulty\n'

def MissionTeamCheck(sentence):
    "\n    This rule rejects any sentence where the subject's missionID\n    doesn't match the sentence's missionID. The sentence's mID is\n    inserted as if by magic based on who has 'ownership' of the Direct\n    Object.\n    "
    if (sentence.mission == sentence.subject.missionID):
        sentence.result = PASS
    else:
        sentence.result = FAILURE


MissionTeamCheck.ID = 20000
MissionTeamCheck.depAttr = '\n'

def GetOnLadder(sentence):
    '\n    This rule allows for checks before a player can get on a ladder.\n    '
    GetOnTop = 2
    GetOnBottom = 3
    sentence.result = FAILURE
    BreakExclusiveAbility(sentence.subject)
    if ((sentence.subject.Stance != Stance_Stand) and (sentence.subject.Stance != Stance_Aggro)):
        return 
    if (sentence.subject.CharMvt is None):
        return 
    if sentence.subject.CharMvt.isInside():
        return 
    heightdiff = (sentence.subject.Position.y - sentence.directObject.Position.y)
    if (heightdiff > 0):
        sentence.result = GetOnTop
    else:
        sentence.result = GetOnBottom


GetOnLadder.ID = 4100
GetOnLadder.depAttr = '\ndirectObject.Position\n'

def StanceSiteEnter(sentence):
    '\n    This rule should be used as a general stance site rule.\n    '
    sentence.result = FAILURE
    if (not sentence.directObject.SiteInUse):
        if (sentence.subject.Stance == Stance_Stand):
            sentence.result = SUCCESS


StanceSiteEnter.ID = 4110
StanceSiteEnter.depAttr = '\ndirectObject.SiteInUse\n'

def StanceSiteExit(sentence):
    '\n    This rule should be used as a general stance site exit rule.\n    It just assumes returns success.\n    '
    sentence.result = SUCCESS


StanceSiteExit.ID = 4111
StanceSiteExit.depAttr = '\n'

def ScriptingBuddyUse(sentence):
    '\n    This rule is to be used for scripting buddies.\n    '
    sentence.result = SUCCESS


ScriptingBuddyUse.ID = 4112
ScriptingBuddyUse.depAttr = '\n'

def ScriptingBuddyReset(sentence):
    '\n    This rule is to be used for scripting buddies.\n    '
    sentence.result = SUCCESS


ScriptingBuddyReset.ID = 4113
ScriptingBuddyReset.depAttr = '\n'

def TurnLightOn(sentence):
    '\n    This rule is called whenever a light switch is turned on\n    '
    sentence.result = SUCCESS


TurnLightOn.ID = 9000
TurnLightOn.depAttr = ''

def TurnLightOff(sentence):
    '\n    This rule is called whenever a light switch is turned off\n    '
    sentence.result = SUCCESS


TurnLightOff.ID = 9001
TurnLightOff.depAttr = ''

def ElevShowPanelUI(sentence):
    '\n    This rule is called whenever an elevator is used\n    '
    sentence.result = SUCCESS


ElevShowPanelUI.ID = 9002
ElevShowPanelUI.depAttr = ''

def TalkNPC(sentence):
    '\n    This rule is called whenever a garrulous NPC is told to talk\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


TalkNPC.ID = 9003
TalkNPC.depAttr = ''

def FollowMeNPC(sentence):
    '\n    This rule is called whenever an amenable NPC is told to follow\n    '
    BreakExclusiveAbility(sentence.subject)
    if fv.CanFollow(sentence.subject, sentence.directObject):
        sentence.result = SUCCESS


FollowMeNPC.ID = 9004
FollowMeNPC.depAttr = fv.CanFollow.depAttr

def StopFollowingMeNPC(sentence):
    '\n    This rule is called whenever an obsequious NPC is told to stop following\n    '
    BreakExclusiveAbility(sentence.subject)
    if fv.CanStopFollow(sentence.subject, sentence.directObject):
        sentence.result = SUCCESS


StopFollowingMeNPC.ID = 9005
StopFollowingMeNPC.depAttr = fv.CanStopFollow.depAttr

def SignalBoostUpload(sentence):
    '\n    this is called when a player wants to upload stuff through a signal booster\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


SignalBoostUpload.ID = 9008
SignalBoostUpload.depAttr = '\n'

def SignalBoostActivate(sentence):
    '\n    this is called when a player activates the signal booster\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


SignalBoostActivate.ID = 9009
SignalBoostActivate.depAttr = '\n'

def CollectorSuccess(sentence):
    '\n    This rule is called when a player has finished a collector quest\n    '
    if sentence.subject.Vendor.CollectorBeanCounterType:
        playerRep = GetReputationFromOrg(sentence.directObject, sentence.directObject.OrganizationID)
        InvalidCrewID = 0
        if ((sentence.subject.SignpostReqReputation == 0) or ((sentence.directObject.OrganizationID == sentence.subject.SignpostOrgID) and ((playerRep >= sentence.subject.SignpostReqReputation) or (sentence.directObject.CrewID != InvalidCrewID)))):
            sentence.subject.Vendor.sendBeanCounter(sentence.directObject.locator, sentence.subject.Vendor.CollectorBeanCounterPoints)
    sentence.result = SUCCESS


CollectorSuccess.ID = 10039
CollectorSuccess.depAttr = '\ndirectObject.locator\ndirectObject.OrganizationID\ndirectObject.ReputationMerovingian\ndirectObject.ReputationZionMilitary\ndirectObject.ReputationMachines\ndirectObject.ReputationCypherites\ndirectObject.ReputationNiobe\ndirectObject.ReputationPluribusNeo\ndirectObject.CrewID\n'

def InvokeVendor(sentence):
    '\n    This rule is called when a player interacts with a vendor (NPC)\n    '
    BreakExclusiveAbility(sentence.subject)
    if sentence.directObject.VendorWelcomeAnimID:
        sentence.subject.PlayerCharacter.sendTriggeredAnim(sentence.directObject.locator, sentence.directObject.VendorWelcomeAnimID)
    sentence.result = SUCCESS


InvokeVendor.ID = 10036
InvokeVendor.depAttr = '\ndirectObject.locator\ndirectObject.VendorWelcomeAnimID\n'

def IsYourSimulacrum(sentence):
    if (sentence.directObject.OwnerCharacterID == sentence.subject.PlayerCharacter.CharacterID):
        return True


IsYourSimulacrum.ID = 9006
IsYourSimulacrum.depAttr = '\ndirectObject.OwnerCharacterID\n'

def TeleporterOrgCheck(sentence):
    '\n    This rule is called whenever a player interacts with a PvP teleporter\n    '
    teleporterOrgID = sentence.directObject.ArchivistOrganization
    if (sentence.subject.OrganizationID == teleporterOrgID):
        sentence.result = SUCCESS
        return 
    discovery.clientSystemMessage(sentence.subject.locator, ST.ID_SYSTEM_MESSAGE_TELEPORTER_ORG_FAILURE)
    sentence.result = FAILURE


TeleporterOrgCheck.ID = 9007
TeleporterOrgCheck.depAttr = '\nTedirectObject.ArchivistOrganization\n'

def BombDefuseStep1(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 1.\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


BombDefuseStep1.ID = 3330
BombDefuseStep1.depAttr = '\n'

def BombDefuseStep2(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 2.\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


BombDefuseStep2.ID = 3331
BombDefuseStep2.depAttr = '\n'

def BombDefuseStep3(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 3.\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


BombDefuseStep3.ID = 3332
BombDefuseStep3.depAttr = '\n'

def BombDefuseStep4(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 4.\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


BombDefuseStep4.ID = 3333
BombDefuseStep4.depAttr = '\n'

def BombDefuseStep5(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 5.\n    '
    BreakExclusiveAbility(sentence.subject)
    sentence.result = SUCCESS


BombDefuseStep5.ID = 3334
BombDefuseStep5.depAttr = '\n'

def HalloweenJOLActivate(sentence):
    '\n    This rule is called when activating a Jack O Lantern for the Halloween event\n    '
    BreakExclusiveAbility(sentence.subject)
    components = (constants.Components.PlayerCharacter)
    objs = sentence.subject.PlayerCharacter.getObjectsInRadius(sentence.directObject.EffectRadius, components)
    for obj in objs:
        if obj.PlayerCharacter:
            discovery.clientSystemMessage(obj.locator, ST.ID_HALLOWEEN_JOL_SUCCESS, constants.Chat.CT_SYS_IMPORTANT)
            obj.PlayerCharacter.spawnSequence(sentence.directObject.SequenceID)

    sentence.result = SUCCESS


HalloweenJOLActivate.ID = 3335
HalloweenJOLActivate.depAttr = '\ndirectObject.EffectRadius\ndirectObject.SequenceID\n'

def IsAdmin(sentence):
    '\n    This rule can be used to verify that the subject is an Admin\n    '
    sentence.result = SUCCESS


IsAdmin.ID = 3336
IsAdmin.depAttr = '\n'

def SearchlightStep1(sentence):
    '\n    This rule is called when determining if a player can initiate searchlight step 1.\n    It always returns SUCCESS\n    '
    sentence.result = SUCCESS


SearchlightStep1.ID = 3337
SearchlightStep1.depAttr = '\n'

def SearchlightStep2(sentence):
    '\n    This rule is called when determining if a player can initiate searchlight step 2.\n    It always returns SUCCESS\n    '
    sentence.result = SUCCESS


SearchlightStep2.ID = 3338
SearchlightStep2.depAttr = '\n'

def SearchlightStep3(sentence):
    '\n    This rule is called when determining if a player can initiate searchlight step 3.\n    It always returns SUCCESS\n    '
    sentence.result = SUCCESS


SearchlightStep3.ID = 3339
SearchlightStep3.depAttr = '\n'

def SearchlightStep4(sentence):
    '\n    This rule is called when determining if a player can initiate searchlight step 4.\n    It always returns SUCCESS\n    '
    sentence.result = SUCCESS


SearchlightStep4.ID = 3340
SearchlightStep4.depAttr = '\n'

def SearchlightStep5(sentence):
    '\n    This rule is called when determining if a player can initiate searchlight step 5.\n    It always returns SUCCESS\n    '
    sentence.result = SUCCESS


SearchlightStep5.ID = 3341
SearchlightStep5.depAttr = '\n'

def SearchlightCleanup(sentence):
    '\n    This rule just verifies that the subject is an Admin\n    '
    if (sentence.subject.AdminPrivileges != 0):
        mods = sentence.directObject.AbilityInv.getTempMods(SpotlightTimerAbility, 0)
        if (mods is not None):
            sentence.subject.AbilityInv.sendChat('Spotlight', 'Found spotlight timers')
            for mod in mods:
                out = ('Time Left : %d ' % mod.TimeLeft)
                sentence.subject.AbilityInv.sendChat('Spotlight', mod.TimeLeft)

        else:
            sentence.subject.AbilityInv.sendChat('Spotlight', 'No spotlight timers found')
        sentence.result = SUCCESS
    else:
        sentence.result = FAILURE


SearchlightCleanup.ID = 3342
SearchlightCleanup.depAttr = '\n'

def SearchlightStep6(sentence):
    '\n    This rule is called when determining if a player can initiate searchlight step 6.\n    It always returns SUCCESS\n    '
    sentence.result = SUCCESS


SearchlightStep6.ID = 3343
SearchlightStep6.depAttr = '\n'

def GetReputationFromOrg(subject, org):
    rep = None
    if (org == constants.Organization.Zion):
        rep = subject.ReputationZionMilitary
    if (org == constants.Organization.Machines):
        rep = subject.ReputationMachines
    if (org == constants.Organization.Merovingian):
        rep = subject.ReputationMerovingian
    if (org == constants.Organization.Cypherites):
        rep = subject.ReputationCypherites
    if (org == constants.Organization.Niobe):
        rep = subject.ReputationNiobe
    if (org == constants.Organization.PluribusNeo):
        rep = subject.ReputationPluribusNeo
    if (rep is None):
        return 0
    return rep



def test2():
    zorp(blsera)



def test1():
    test2()



def levelCost(lvl):
    test1()
    xpArray = [0,
     1000,
     3000,
     6000,
     10000,
     15000,
     21000,
     28000,
     36000,
     45000,
     55000,
     66000,
     78000,
     91000,
     105000,
     120000,
     136000,
     153000,
     171000,
     190000,
     210000,
     231000,
     253000,
     276000,
     300000,
     325000,
     351000,
     378000,
     406000,
     435000,
     465000,
     496000,
     528000,
     561000,
     595000,
     630000,
     666000,
     703000,
     741000,
     780000,
     820000,
     861000,
     903000,
     946000,
     990000,
     1035000,
     1081000,
     1128000,
     1176000,
     1225000]
    lvl -= 1
    if ((lvl >= 0) and (lvl < len(xpArray))):
        return xpArray[lvl]
    return -1


levelCost.ID = 10
levelCost.tableDim = 1

def debugTest():
    discovery.outputDebugString('ODS: Rules System Functioning')
    discovery.serverPrint('SP: Rules System Functioning')



# local variables:
# tab-width: 4
