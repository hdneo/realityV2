# emacs-mode: -*- python-*-
import random
import traceback
import missionvalidate as mv
import combatvalidate as cv
import followvalidate as fv
import stringtable_client as ST

def exceptionCB(obj, data, tb):
    try:
        discovery.errorPrint('****************************************')
        discovery.errorPrint('Rule Exception')
        discovery.errorPrint(`obj`)
        discovery.errorPrint(`data`)
        discovery.errorPrint('** traceback **')
        if tb:
            stackTrace = traceback.extract_tb(tb)
            stackTrace.reverse()
            for tuple in stackTrace:
                discovery.errorPrint(('File: %s (%d) Function: %s' % tuple[:3]))
                discovery.errorPrint(tuple[3])

        discovery.errorPrint('****************************************')
    except:
        pass



def debugTest():
    discovery.outputDebugString('ODS: Rules System Functioning')
    discovery.consolePrint('CS: Rules System Functioning')



def Get(possible, default):
    if (possible is None):
        return default
    return possible



def Success(sentence):
    '\n    You can use this for any always-successful verification\n    '
    sentence.result = SUCCESS


Success.ID = 1
Success.depAttr = ''

def Failure(sentence):
    '\n    You can use this for any always-failed verification\n    '
    sentence.result = FAILURE


Failure.ID = 0
Failure.depAttr = ''

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

def DecompileAbilityTest(sentence):
    '\n    This rule checks for the presence of the decompile ability.\n    '
    abil = (sentence.subject.abilities[DecompileAbility] * 4)
    if (abil > 0):
        sentence.result = SUCCESS
    else:
        sentence.result = FAILURE


DecompileAbilityTest.ID = 6000
DecompileAbilityTest.depAttr = ''

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

    discovery.consolePrint('The key is not for this mission.')
    return FAILURE


HasMissionKeyItem.depAttr = '\ndirectObject.MissionKey\n'

def HasToolForAbility(sentence, ability):
    """ checks if there is a tool appropriate for ability in inventory, returns True or False"""
    return SUCCESS



def ComputerInfect(sentence):
    '\n    Succeed if we have a computer virus which\n    matches our mission key.\n    '
    if (not mv.ValidMissionKeyBaseMatch(sentence.subject.MissionKey, sentence.directObject.MissionKey)):
        return 
    if HasMissionKeyItem(sentence, discovery.getGameObjectType('Computer Virus')):
        sentence.result = SUCCESS
        return 


ComputerInfect.ID = 1003
ComputerInfect.depAttr = HasMissionKeyItem.depAttr
ComputerInfect.depAttr += '\nindirectObject.instData\nindirectObject.type\n'

def ComputerHack(sentence):
    "\n    Hack client rule always succeeds if this is the player's mission;\n    server rule does more validation.\n    "
    sentence.result = FAILURE
    if (not mv.ValidMissionKeyBaseMatch(sentence.subject.MissionKey, sentence.directObject.MissionKey)):
        return 
    sentence.result = SUCCESS
    return 
    if sentence.subject.abilities[HackerAbility]:
        sentence.result = SUCCESS
        return 


ComputerHack.ID = 1002
ComputerHack.depAttr = HasMissionKeyItem.depAttr
ComputerHack.depAttr += '\nindirectObject.instData\nindirectObject.type\n'

def TrapDisarm(sentence):
    '\n    This rule checks for the presence of the DisarmTraps ability.\n    '
    TrapIsArmed = sentence.directObject.TrapArmed
    TrapIsVisible = sentence.directObject.TrapVisible
    abil = (4 * sentence.subject.abilities[DisarmTrapsAbility])
    sentence.result = FAILURE
    if TrapIsVisible:
        if TrapIsArmed:
            if (abil > 0):
                sentence.result = SUCCESS


TrapDisarm.ID = 4010
TrapDisarm.depAttr = '\ndirectObject.TrapArmed\ndirectObject.TrapVisible\n'

def SecurityPBXDisable(sentence):
    '\n    This rule always returns true. The server rule performs validation.\n    '
    sentence.result = SUCCESS


SecurityPBXDisable.ID = 1012
SecurityPBXDisable.depAttr = '\nindirectObject.type\n'

def DoorPickLock(sentence):
    '\n    Pick Lock will always appear, except in the tutorial\n    '
    if (clientshell.getTutorialState() != clientshell.eTutState_Invalid):
        sentence.result = FAILURE
        return 
    sentence.result = SUCCESS


DoorPickLock.ID = 4000
DoorPickLock.depAttr = '\nindirectObject.Quality\nindirectObject.ReqAbilityID\ndirectObject.Difficulty\ndirectObject.locator\n'

def GetOnLadder(sentence):
    '\n    This rule allows for checks before a player can get on a ladder.\n    '
    sentence.result = FAILURE
    if ((sentence.subject.Stance != Stance_Stand) and ((sentence.subject.Stance != Stance_Aggro) and ((sentence.subject.Stance != Stance_Sneak) and (sentence.subject.Stance != Stance_Invis)))):
        return 
    if (sentence.directObject.Ladder is None):
        return 
    heightdiff = (sentence.subject.Position.y - sentence.directObject.Position.y)
    if (heightdiff > 0):
        sentence.directObject.Ladder.checkNavMeshTop()
        if (not sentence.directObject.Ladder.HasValidTopPosition):
            discovery.consolePrint(('HasValidTopPosition = %d' % sentence.directObject.Ladder.HasValidTopPosition))
            return 
    else:
        sentence.directObject.Ladder.checkNavMeshBottom()
        if (not sentence.directObject.Ladder.HasValidBottomPosition):
            return 
    if (sentence.subject.CharMvt is None):
        return 
    if sentence.subject.CharMvt.isInside():
        return 
    sentence.result = SUCCESS


GetOnLadder.ID = 4100
GetOnLadder.depAttr = '\n'

def DoorLockTest(sentence):
    '\n    This rule returns success if the player has the key, otherwise failure\n    '
    sentence.result = SUCCESS
    return 


DoorLockTest.ID = 4003
DoorLockTest.depAttr = HasMissionKeyItem.depAttr
DoorLockTest.depAttr += '\nindirectObject.instData\ndirectObject.MissionKey\n'

def CardKeyTest(sentence):
    '\n    This rule simply returns success\n    '
    if (not mv.ValidMissionKeyBaseMatch(sentence.subject.MissionKey, sentence.directObject.MissionKey)):
        return 
    if HasMissionKeyItem(sentence, discovery.getGameObjectType('CardKey')):
        sentence.result = SUCCESS
        return 


CardKeyTest.ID = 4005
CardKeyTest.depAttr = HasMissionKeyItem.depAttr
CardKeyTest.depAttr += '\nindirectObject.instData\n'

def GenericKeyTest(sentence):
    '\n    This rule returns success if the player has the correct key\n    otherwise returns failure\n    '
    sentence.result = SUCCESS
    return 


GenericKeyTest.ID = 4006
GenericKeyTest.depAttr = HasMissionKeyItem.depAttr
GenericKeyTest.depAttr += '\nindirectObject.instData\ndirectObject.MissionKey\n'

def DoorOpenGeneric(sentence):
    '\n    This rule enforces that a door that has been locked to a specific\n    mission team may only be opened by them.\n    '
    playerkey = sentence.subject.MissionKey
    if ((playerkey != mv.NON_ASSIGNABLE_MISSIONKEY) and (not mv.ValidMissionKeyBaseMatch(sentence.directObject.MissionKey, playerkey))):
        return 
    sentence.result = SUCCESS


DoorOpenGeneric.ID = 4004
DoorOpenGeneric.depAttr = '\ndirectObject.MissionKey\n'

def StanceSiteEnter(sentence):
    '\n    This rule should be used as a general stance site rule.\n    '
    sentence.result = FAILURE
    if (not sentence.directObject.SiteInUse):
        if (sentence.subject.Stance == 0):
            sentence.result = SUCCESS


StanceSiteEnter.ID = 4110
StanceSiteEnter.depAttr = '\ndirectObject.SiteInUse\n'

def RequestCombat(sentence):
    '\n    This rule should become quite complex as it tries to figure\n    out if anyone can fight anything.\n    '
    if cv.CanFight(sentence.subject, sentence.directObject):
        sentence.result = SUCCESS


RequestCombat.ID = 2001
RequestCombat.depAttr = '\ndirectObject.IsDead\ndirectObject.FactionID\ndirectObject.NavPolyID\n'

def CanFollowClient(subject, directObject):
    if mv.ValidMissionKeyBaseMatch(subject.MissionTeam.MissionKey, directObject.MissionElement.MissionKey):
        return True
    return False



def CanStopFollowClient(directObject):
    if (consolevar.PlayerID == directObject.AI.MasterCharacterID):
        return True
    return False



def FollowMeNPC(sentence):
    '\n    This rule is called whenever an amenable NPC is told to follow\n    '
    if CanFollowClient(sentence.subject, sentence.directObject):
        sentence.result = SUCCESS


FollowMeNPC.ID = 9004
FollowMeNPC.depAttr = '\ndirectObject.SimulacraSlave.OwnerCharacterID\ndirectObject.MissionElement.MissionKey\n'

def StopFollowingMeNPC(sentence):
    '\n    This rule is called whenever an obsequious NPC is told to stop following\n    '
    if CanStopFollowClient(sentence.directObject):
        sentence.result = SUCCESS


StopFollowingMeNPC.ID = 9005
StopFollowingMeNPC.depAttr = '\ndirectObject.AI.MasterCharacterID\n'

def IsYourSimulacrum(sentence):
    '\n    This rule is called to check if a simulacrum is yours\n    '
    sentence.result = SUCCESS


IsYourSimulacrum.ID = 9006
IsYourSimulacrum.depAttr = '\ndirectObject.SimulacraSlave.OwnerCharacterID\n'

def MissionTeamInvite(sentence):
    sentence.result = SUCCESS


MissionTeamInvite.ID = 10010
MissionTeamInvite.depAttr = ''

def HardlineHackControlNodeStage1(sentence):
    '\n    Return SUCCESS if the player is an attacker and can attack this control node.\n    '
    sentence.result = SUCCESS


HardlineHackControlNodeStage1.ID = 10025
HardlineHackControlNodeStage1.depAttr = '\n'

def HardlineHackControlNodeStage2(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    if (sentence.subject.FactionID != sentence.directObject.FactionID):
        sentence.result = SUCCESS


HardlineHackControlNodeStage2.ID = 10026
HardlineHackControlNodeStage2.depAttr = '\n'

def HardlineHackControlNodeStage3(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    if (sentence.subject.FactionID != sentence.directObject.FactionID):
        sentence.result = SUCCESS


HardlineHackControlNodeStage3.ID = 10027
HardlineHackControlNodeStage3.depAttr = '\n'

def HardlineHackControlNodeClaimConstruct(sentence):
    '\n    Return SUCCESS if the player can hack this control node.\n    '
    if (sentence.subject.FactionID != sentence.directObject.FactionID):
        sentence.result = SUCCESS


HardlineHackControlNodeClaimConstruct.ID = 10028
HardlineHackControlNodeClaimConstruct.depAttr = '\n'

def HardlineEnterConstruct(sentence):
    '\n    Return SUCCESS if the player can enter constructs via this hardline.\n    '
    sentence.result = SUCCESS


HardlineEnterConstruct.ID = 10023
HardlineEnterConstruct.depAttr = '\n'

def HardlineHackConstruct(sentence):
    '\n    Return SUCCESS if the player can hack via this hardline.\n    '
    sentence.result = SUCCESS


HardlineHackConstruct.ID = 10024
HardlineHackConstruct.depAttr = '\n'

def TutorialExitPtJackIntoTheMatrix(sentence):
    '\n    Return SUCCESS if the player can exit the tutorial\n    '
    if ((clientshell.getTutorialState() != clientshell.eTutState_PostStatus) and constants.Build.final):
        sentence.result = FAILURE
        return 
    sentence.result = SUCCESS


TutorialExitPtJackIntoTheMatrix.ID = 10037
TutorialExitPtJackIntoTheMatrix.depAttr = '\n'

def ConstructConfigure(sentence):
    '\n    Return SUCCESS if the player can configure constructs via control node.\n    '
    sentence.result = SUCCESS


ConstructConfigure.ID = 10032
ConstructConfigure.depAttr = '\n'

def TagAccessNode(sentence):
    '\n    Return SUCCESS if the player can tag an Access Node.\n    '
    if (accessnode.isValid(sentence.directObject.SoftBoundaryID) or (not accessnode.canTagNode(sentence.directObject.SoftBoundaryID))):
        sentence.result = FAILURE
        return 
    sentence.result = SUCCESS


TagAccessNode.ID = 10033
TagAccessNode.depAttr = '\n'

def HardlineExit(sentence):
    '\n    Return SUCCESS if the player can exit via this hardline.\n    Currently just always returns success.\n    '
    if hardlineMgr.isKnown(sentence.directObject.Hardline.getID()):
        sentence.result = SUCCESS
        return 
    sentence.result = FAILURE


HardlineExit.ID = 10020
HardlineExit.depAttr = '\ndirectObject.locator\n'

def HardlineUpload(sentence):
    '\n    Return SUCCESS if the player can upload via this hardline.\n    Currently just always returns success.\n    '
    if hardlineMgr.isKnown(sentence.directObject.Hardline.getID()):
        sentence.result = SUCCESS
        return 
    sentence.result = FAILURE


HardlineUpload.ID = 10021
HardlineUpload.depAttr = '\ndirectObject.locator\n'

def HardlineExitToLoadingArea(sentence):
    '\n    Return SUCCESS if the player can exit via this hardline.\n    Currently just always returns success.\n    '
    if hardlineMgr.isKnown(sentence.directObject.Hardline.getID()):
        sentence.result = SUCCESS
        return 
    sentence.result = FAILURE


HardlineExitToLoadingArea.ID = 10022
HardlineExitToLoadingArea.depAttr = '\ndirectObject.locator\n'

def HardlineSync(sentence):
    '\n    Return SUCCESS if the player does not know this hardline.\n    '
    if hardlineMgr.isKnown(sentence.directObject.Hardline.getID()):
        sentence.result = FAILURE
        return 
    sentence.result = SUCCESS


HardlineSync.ID = 10040
HardlineSync.depAttr = '\ndirectObject.locator\n'

def ContainerOpen(sentence):
    sentence.result = FAILURE
    if (((sentence.directObject.UseCount != 0) and ((sentence.directObject.AI is None) or sentence.directObject.Container.getLootState())) or (sentence.directObject.UseTaker and sentence.directObject.UseTaker.Enabled)):
        sentence.result = SUCCESS
    elif ((sentence.directObject.AI is None) and mv.IsNonReservedMatchingKey(sentence.directObject.MissionKey, sentence.subject.MissionKey)):
        sentence.result = SUCCESS


ContainerOpen.ID = 1010
ContainerOpen.depAttr = '\n'

def Repair(sentence):
    '\n    Just pass SUCCESS\n    '
    sentence.result = SUCCESS


Repair.ID = 1337
Repair.depAttr = '\n'

def GenericOpen(sentence):
    '\n    Just pass SUCCESS\n    '
    sentence.result = SUCCESS


GenericOpen.ID = 1338
GenericOpen.depAttr = '\n'

def GenericClose(sentence):
    '\n    Just pass SUCCESS\n    '
    sentence.result = SUCCESS


GenericClose.ID = 1339
GenericClose.depAttr = '\n'

def BombDefuseStep1(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 1.\n    '
    itemID = int(sentence.directObject.DefuseItemID1)
    if (len(GetItemsMatchingType(sentence, itemID)) > 0):
        sentence.directObject.DetailsStringID = 0
        sentence.result = SUCCESS
        return 
    sentence.directObject.DetailsStringID = ST.ID_OBJ_BOMB_NO_DEFUSE
    sentence.result = FAILURE


BombDefuseStep1.ID = 3330
BombDefuseStep1.depAttr = '\ndirectObject.DefuseItemID1\ndirectObject.DetailsStringID\n'

def BombDefuseStep2(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 2.\n    '
    itemID = int(sentence.directObject.DefuseItemID2)
    if (len(GetItemsMatchingType(sentence, itemID)) > 0):
        sentence.directObject.DetailsStringID = 0
        sentence.result = SUCCESS
        return 
    sentence.directObject.DetailsStringID = ST.ID_OBJ_BOMB_NO_DEFUSE
    sentence.result = FAILURE


BombDefuseStep2.ID = 3331
BombDefuseStep2.depAttr = '\ndirectObject.DefuseItemID2\ndirectObject.DetailsStringID\n'

def BombDefuseStep3(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 3.\n    '
    itemID = int(sentence.directObject.DefuseItemID3)
    if (len(GetItemsMatchingType(sentence, itemID)) > 0):
        sentence.directObject.DetailsStringID = 0
        sentence.result = SUCCESS
        return 
    sentence.directObject.DetailsStringID = ST.ID_OBJ_BOMB_NO_DEFUSE
    sentence.result = FAILURE


BombDefuseStep3.ID = 3332
BombDefuseStep3.depAttr = '\ndirectObject.DefuseItemID3\ndirectObject.DetailsStringID\n'

def BombDefuseStep4(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 4.\n    '
    itemID = int(sentence.directObject.DefuseItemID4)
    if (len(GetItemsMatchingType(sentence, itemID)) > 0):
        sentence.directObject.DetailsStringID = 0
        sentence.result = SUCCESS
        return 
    sentence.directObject.DetailsStringID = ST.ID_OBJ_BOMB_NO_DEFUSE
    sentence.result = FAILURE


BombDefuseStep4.ID = 3333
BombDefuseStep4.depAttr = '\ndirectObject.DefuseItemID4\ndirectObject.DetailsStringID\n'

def BombDefuseStep5(sentence):
    '\n    This rule is called when determining if a player can initiate defusal step 5.\n    '
    itemID = int(sentence.directObject.DefuseItemID5)
    if (len(GetItemsMatchingType(sentence, itemID)) > 0):
        sentence.directObject.DetailsStringID = 0
        sentence.result = SUCCESS
        return 
    sentence.directObject.DetailsStringID = ST.ID_OBJ_BOMB_NO_DEFUSE
    sentence.result = FAILURE


BombDefuseStep5.ID = 3334
BombDefuseStep5.depAttr = '\ndirectObject.DefuseItemID5\ndirectObject.DetailsStringID\n'

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
    sentence.result = SUCCESS


SearchlightCleanup.ID = 3342
SearchlightCleanup.depAttr = '\n'

def SearchlightStep6(sentence):
    '\n    This rule is called when determining if a player can initiate searchlight step 5.\n    It always returns SUCCESS\n    '
    sentence.result = SUCCESS


SearchlightStep6.ID = 3343
SearchlightStep6.depAttr = '\n'

# local variables:
# tab-width: 4
