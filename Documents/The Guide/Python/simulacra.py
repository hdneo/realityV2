# emacs-mode: -*- python-*-
import random
import traceback
import obj
import missionvalidate as mv
import combatvalidate as cv
import stringtable_client as StringTable
import ability.utility as Utility
from ability.defines import *
import ltfxmap as FX
from time import ctime
print 'simulacra reloaded ',
print ctime()
ACOUSTICDECOYS1_DURATION = 60
ACOUSTICDECOYS2_DURATION = 120
ACOUSTICDECOYS3_DURATION = 60
ACOUSTICDECOYS1_RADIUS = 1000
ACOUSTICDECOYS2_RADIUS = 1000
ACOUSTICDECOYS3_RADIUS = 1000

def AcousticDecoy1_GetRange(level, selectionRangeDebuff):
    r = (5000.0 * selectionRangeDebuff)
    return (r,
     r)



def VecToStr(vec):
    val = ('%f %f %f' % (vec.x,
     vec.y,
     vec.z))
    return val



def AcousticDecoy2_Test(sentence):
    Utility.outputAbilityDebug('AcousticDecoy2_Test')
    if ((sentence.directObject.OwnerCharacterID is None) or (sentence.subject.CharacterID != sentence.directObject.OwnerCharacterID)):
        sentence.result = FAILURE
    else:
        sentence.result = SUCCESS


AcousticDecoy2_Test.depAttr = '\ndirectObject.OwnerCharacterID\n'

def Decoy1_Test(sentence):
    Utility.outputAbilityDebug('Decoy1_Test')
    if ((sentence.directObject.OwnerCharacterID is None) or (sentence.subject.CharacterID != sentence.directObject.OwnerCharacterID)):
        sentence.result = FAILURE
    else:
        sentence.result = SUCCESS


Decoy1_Test.depAttr = '\ndirectObject.OwnerCharacterID\n'

def StopProxy1_Test(sentence):
    Utility.outputAbilityDebug('StopProxy1_Test')
    if ((sentence.directObject.OwnerCharacterID is None) or (sentence.subject.CharacterID != sentence.directObject.OwnerCharacterID)):
        sentence.result = FAILURE
    else:
        sentence.result = SUCCESS


StopProxy1_Test.depAttr = '\ndirectObject.OwnerCharacterID\n'

def sim_clamp(min, max, lvl):
    if (lvl < min):
        return min
    elif (lvl > max):
        return max
    return lvl



def LogicDaemon1_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 4
    maxLevel = 7
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    subject.AbilityInv.createSimulacrum(('Simulacra.Nuker',
     lvl,
     gender), 'SimulacraInit()', LogicDaemon1Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, LogicDaemon1Ability, msg)



def LogicDaemon1_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def LogicDaemon2_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 8
    maxLevel = 17
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    subject.AbilityInv.createSimulacrum(('Simulacra.Nuker',
     lvl,
     gender), 'SimulacraInit()', LogicDaemon2Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, LogicDaemon2Ability, msg)



def LogicDaemon2_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def LogicDaemon3_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 18
    maxLevel = 34
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    subject.AbilityInv.createSimulacrum(('Simulacra.Nuker',
     lvl,
     gender), 'SimulacraInit()', LogicDaemon3Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, LogicDaemon3Ability, msg)



def LogicDaemon3_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def LogicDaemon4_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 35
    maxLevel = 50
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    subject.AbilityInv.createSimulacrum(('Simulacra.Nuker',
     lvl,
     gender), 'SimulacraInit()', LogicDaemon4Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, LogicDaemon4Ability, msg)



def LogicDaemon4_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def PatchDaemon1_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 12
    maxLevel = 22
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    subject.AbilityInv.createSimulacrum(('Simulacra.Healer',
     lvl,
     gender), 'SimulacraInit()', PatchDaemon1Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, PatchDaemon1Ability, msg)



def PatchDaemon1_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def PatchDaemon2_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 23
    maxLevel = 43
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    subject.AbilityInv.createSimulacrum(('Simulacra.Healer',
     lvl,
     gender), 'SimulacraInit()', PatchDaemon2Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, PatchDaemon2Ability, msg)



def PatchDaemon2_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def PatchDaemon3_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 44
    maxLevel = 50
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    subject.AbilityInv.createSimulacrum(('Simulacra.Healer',
     lvl,
     gender), 'SimulacraInit()', PatchDaemon3Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, PatchDaemon3Ability, msg)



def PatchDaemon3_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()


simulacra_choices = ('Simulacra.Aikido',
 'Simulacra.Karate',
 'Simulacra.KungFu',
 'Simulacra.Pistol',
 'Simulacra.Rifle',
 'Simulacra.SMG')

def RemoteProxy1_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 1
    maxLevel = 4
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    if (len(consolevar.RemoteProxySheet) > 2):
        subject.AbilityInv.createSimulacrum((consolevar.RemoteProxySheet,
         lvl,
         gender), 'SimulacraInit()', RemoteProxy1Ability)
    else:
        subject.AbilityInv.createSimulacrum((random.choice(simulacra_choices),
         lvl,
         gender), 'SimulacraInit()', RemoteProxy1Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, RemoteProxy1Ability, msg)



def RemoteProxy1_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def RemoteProxy2_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 4
    maxLevel = 7
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    if (len(consolevar.RemoteProxySheet) > 2):
        subject.AbilityInv.createSimulacrum((consolevar.RemoteProxySheet,
         lvl,
         gender), 'SimulacraInit()', RemoteProxy2Ability)
    else:
        subject.AbilityInv.createSimulacrum((random.choice(simulacra_choices),
         lvl,
         gender), 'SimulacraInit()', RemoteProxy2Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, RemoteProxy2Ability, msg)
    subject.AbilityInv.destroyCurrentSimulacrum()



def RemoteProxy2_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def RemoteProxy3_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 8
    maxLevel = 17
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    if (len(consolevar.RemoteProxySheet) > 2):
        subject.AbilityInv.createSimulacrum((consolevar.RemoteProxySheet,
         lvl,
         gender), 'SimulacraInit()', RemoteProxy3Ability)
    else:
        subject.AbilityInv.createSimulacrum((random.choice(simulacra_choices),
         lvl,
         gender), 'SimulacraInit()', RemoteProxy3Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, RemoteProxy3Ability, msg)



def RemoteProxy3_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def RemoteProxy4_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 18
    maxLevel = 34
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    if (len(consolevar.RemoteProxySheet) > 2):
        subject.AbilityInv.createSimulacrum((consolevar.RemoteProxySheet,
         lvl,
         gender), 'SimulacraInit()', RemoteProxy4Ability)
    else:
        subject.AbilityInv.createSimulacrum((random.choice(simulacra_choices),
         lvl,
         gender), 'SimulacraInit()', RemoteProxy4Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, RemoteProxy4Ability, msg)



def RemoteProxy4_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def RemoteProxy5_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    minLevel = 35
    maxLevel = 50
    lvl = sim_clamp(minLevel, maxLevel, subject.Level)
    if (len(consolevar.RemoteProxySheet) > 2):
        subject.AbilityInv.createSimulacrum((consolevar.RemoteProxySheet,
         lvl,
         gender), 'SimulacraInit()', RemoteProxy5Ability)
    else:
        subject.AbilityInv.createSimulacrum((random.choice(simulacra_choices),
         lvl,
         gender), 'SimulacraInit()', RemoteProxy5Ability)
    Utility.SendAbilityOutputToCasterMsg(StringTable.ID_CLIENT_ABILITY_CREATE_SIMULACRA_CASTER, RemoteProxy5Ability, msg)



def RemoteProxy5_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def KungFuSimulacra1_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.KungFu',
     Level_1_Sim,
     gender), 'SimulacraInit()', KungFuSimulacra1Ability)



def KungFuSimulacra1_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def KungFuSimulacra2_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.KungFu',
     Level_2_Sim,
     gender), 'SimulacraInit()', KungFuSimulacra2Ability)



def KungFuSimulacra2_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def KungFuSimulacra3_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.KungFu',
     Level_3_Sim,
     gender), 'SimulacraInit()', KungFuSimulacra3Ability)



def KungFuSimulacra3_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def PistolSimulacra1_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.Pistol',
     Level_1_Sim,
     gender), 'SimulacraInit()', PistolSimulacra1Ability)



def PistolSimulacra1_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def PistolSimulacra2_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.Pistol',
     Level_2_Sim,
     gender), 'SimulacraInit()', PistolSimulacra2Ability)



def PistolSimulacra2_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def PistolSimulacra3_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.Pistol',
     Level_3_Sim,
     gender), 'SimulacraInit()', PistolSimulacra3Ability)



def PistolSimulacra3_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def RifleSimulacra1_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.Rifle',
     Level_1_Sim,
     gender), 'SimulacraInit()', RifleSimulacra1Ability)



def RifleSimulacra1_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def RifleSimulacra2_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.Rifle',
     Level_2_Sim,
     gender), 'SimulacraInit()', RifleSimulacra2Ability)



def RifleSimulacra2_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def RifleSimulacra3_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.Rifle',
     Level_3_Sim,
     gender), 'SimulacraInit()', RifleSimulacra3Ability)



def RifleSimulacra3_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def SMGSimulacra1_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.SMG',
     Level_1_Sim,
     gender), 'SimulacraInit()', SMGSimulacra1Ability)



def SMGSimulacra1_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def SMGSimulacra2_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.SMG',
     Level_2_Sim,
     gender), 'SimulacraInit()', SMGSimulacra2Ability)



def SMGSimulacra2_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def SMGSimulacra3_Subject(subject, msg):
    gender = random.choice(('f',
     'm'))
    subject.AbilityInv.createSimulacrum(('Simulacra.SMG',
     Level_3_Sim,
     gender), 'SimulacraInit()', SMGSimulacra3Ability)



def SMGSimulacra3_Deactivate(subject):
    subject.AbilityInv.destroyCurrentSimulacrum()



def MessageCloud_GetRange(level, selectionRangeDebuff):
    return ((3000.0 * selectionRangeDebuff),
     (3000.0 * selectionRangeDebuff))



def MessageCloud_DirectObject(subject, msg):
    Utility.outputAbilityDebug('MSG CLOUD DIRECT OBJECT ')
    percentage_decrease_in_range = 80
    duration = 4.0
    mem_cost = 0
    mc_procs = ('MessageCloudInit',
     'MessageCloudTerm',
     '',
     '',
     '')
    subject.AbilityInv.addTempModProcs(mc_procs, MessageCloudAbility, SelectionRangeAbility, duration, mem_cost, 0, percentage_decrease_in_range)



def MessageCloud_Subject(subject, msg):
    Utility.outputAbilityDebug('MSG CLOUD')
    objects = discovery.getAllObjects()
    msgcldid = objects['MessageCloud']
    print 'msg cld id : ',
    print msgcldid
    duration = 20.0
    msgcld = subject.AbilityInv.createStaticObject(msgcldid, {'Position': msg.location,
     'Orientation': subject.CharMvt.Orientation,
     'Duration': duration})
    procs = ('',
     '',
     'MessageCloudPulse',
     '',
     '')
    msgcld.Abilities.addTempModProcs(procs, duration, 0, 0)
    procs = ('MessageCloudInit',
     'MessageCloudTerm',
     '',
     '',
     '')
    msgcld.Abilities.addTempModProcs(procs, duration, 0, 0)



# local variables:
# tab-width: 4
