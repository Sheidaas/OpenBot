import ui,net,player,eXLib
from OpenBot.Modules import FileManager, Movement, OpenLib
from OpenBot.Modules.FileManager import boolean


class SettingsDialog(ui.ScriptWindow):
    TIME_DEAD = 5
    TIME_POTS = 0.2
    RED_POTIONS_IDS = [27001,27002,27003,27007,27051,27201,27202,27203]
    BLUE_POTIONS_IDS = [27004,27005,27006,27008,27052,27204,27205,27206,63018]

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.restartHere = False
        self.restartInCity = False
        self.bluePotions = True
        self.redPotions = True
        self.speedHack = False
        self.antiExpTimerSleep = 0
        self.antiExp = False
        self.minMana = 95
        self.minHealth = 80
        self.speedMultiplier = 0.0
        self.lastTimeDead = OpenLib.GetTime()

        self.pickUp = False
        self.pickUpRange = 290.0
        self.pickUpSpeed = 0.5
        self.pickFilter = set()
        self.excludeInFilter = True
        self.useRangePickup = False
        self.doNotPickupIfPlayerHere = False
        self.checkIsWallBetweenPlayerAndItem = False

        self.useOnClickDmg = False
        self.onClickDmgSpeed = 0.0
        self.timerDmg = OpenLib.GetTime()

        self.wallHack = False
        self.sellItems = set()

        self.can_add_waiter = True
        self.timerPots = 0
        self.timerDead = 0
        self.pickUpTimer = 0
        self.LoadSettings()

    def LoadSettings(self):
        #OpenLog.DebugPrint("Loading Settings")
        self.autoLogin = boolean(FileManager.ReadConfig("AutoLogin"))
        self.restartHere = boolean(FileManager.ReadConfig("AutoRestart"))
        self.bluePotions = boolean(FileManager.ReadConfig("UseBluePots"))
        self.redPotions = boolean(FileManager.ReadConfig("UseRedPots"))
        self.speedHack = boolean(FileManager.ReadConfig("SpeedHack"))
        self.speedMultiplier = float(FileManager.ReadConfig("SpeedHackMultiplier"))
        self.minMana = int(FileManager.ReadConfig("MinMana"))
        self.minHealth = int(FileManager.ReadConfig("MinHealth"))
        self.pickUp = boolean(FileManager.ReadConfig("PickupUse"))
        self.pickUpRange = float(FileManager.ReadConfig("PickupRange"))
        self.pickUpSpeed = float(FileManager.ReadConfig("PickupSpeed"))
        self.excludeInFilter = boolean(FileManager.ReadConfig("FilterMode"))
        self.useRangePickup = boolean(FileManager.ReadConfig("UseRangePickup"))
        self.wallHack = boolean(FileManager.ReadConfig("WallHack"))
        self.onClickDmgSpeed  = boolean(FileManager.ReadConfig("OnClickDamageSpeed"))
        self.antiExp = boolean(FileManager.ReadConfig("antiExp"))
        self.doNotPickupIfPlayerHere = boolean(FileManager.ReadConfig("doNotPickupIfPlayerHere"))
        for i in FileManager.LoadListFile(FileManager.CONFIG_PICKUP_FILTER):
            self.addPickFilterItem(int(i))
        self.sellItems = {int(i) for i in FileManager.LoadListFile(FileManager.CONFIG_SELL_INVENTORY)}

    def SaveSettings(self):
        #OpenLog.DebugPrint("Saving Settings")
        FileManager.WriteConfig("AutoLogin", str(self.autoLogin))
        FileManager.WriteConfig("AutoRestart", str(self.restartHere))
        FileManager.WriteConfig("UseBluePots", str(self.bluePotions))
        FileManager.WriteConfig("UseRedPots", str(self.redPotions))
        FileManager.WriteConfig("SpeedHack", str(self.speedHack))
        FileManager.WriteConfig("SpeedHackMultiplier", str(self.speedMultiplier))
        FileManager.WriteConfig("MinMana", str(self.minMana))
        FileManager.WriteConfig("MinHealth", str(self.minHealth))
        FileManager.WriteConfig("PickupUse", str(self.pickUp))
        FileManager.WriteConfig("PickupRange", str(self.pickUpRange))
        FileManager.WriteConfig("PickupSpeed", str(self.pickUpSpeed))
        FileManager.WriteConfig("FilterMode", str(self.excludeInFilter))
        FileManager.WriteConfig("UseRangePickup", str(self.useRangePickup))
        FileManager.WriteConfig("WallHack", str(self.wallHack))
        FileManager.WriteConfig("OnClickDamageSpeed", str(self.onClickDmgSpeed))
        FileManager.WriteConfig("antiExp", str(self.antiExp))
        FileManager.WriteConfig("timeAfterDead", str(self.waitTimeDeadEditLine.GetText()))
        FileManager.WriteConfig("doNotPickupIfPlayerHere", str(self.doNotPickupIfPlayerHere))
        
        #chat.AppendChat(3,str(self.pickUp))
        FileManager.SaveListFile(FileManager.CONFIG_PICKUP_FILTER,self.pickFilter)
        FileManager.SaveListFile(FileManager.CONFIG_SELL_INVENTORY,self.sellItems)
        FileManager.Save()

    # General
    def CheckUsePotions(self):
        val, self.timerPots = OpenLib.timeSleep(self.timerPots,self.TIME_POTS)
        if val:
            if self.redPotions and (float(player.GetStatus(player.HP)) / (float(player.GetStatus(player.MAX_HP))) * 100) < int(self.minHealth):
                OpenLib.UseAnyItemByID(self.RED_POTIONS_IDS)

            if self.bluePotions and (float(player.GetStatus(player.SP)) / (float(player.GetStatus(player.MAX_SP))) * 100) < int(self.minMana):
                OpenLib.UseAnyItemByID(self.BLUE_POTIONS_IDS)

    def checkReviveAndLogin(self):
        val, self.timerDead = OpenLib.timeSleep(self.timerDead,self.TIME_DEAD)

        if not val:
            return

        if self.restartHere and player.GetStatus(player.HP) <= 0:
            self.lastTimeDead = OpenLib.GetTime()
            if not self.restartInCity:
                OpenLib.Revive()
            else:
                OpenLib.Revive(in_city=True)
        
        if self.autoLogin and OpenLib.GetCurrentPhase() == OpenLib.PHASE_LOGIN:
            net.DirectEnter(0,0)
            #ChannelSwitcher.instance.ConnectToChannel()
    
    def WallHackSwich(self,val):
        if bool(val):
            self.wallHack = True
            eXLib.DisableCollisions()
        else:
            self.wallHack = False
            eXLib.EnableCollisions()

    def antiExpFunc(self):
        from OpenBot.Modules.Actions import ActionBot
        def _anti_exp():
            self.can_add_waiter = True
            exp = player.GetEXP()
            if exp > 1000000:
                net.SendGuildOfferPacket(1000000)
            elif exp < 1000000 and exp > 0:
                net.SendGuildOfferPacket(exp)
            elif exp == 0:
                return
        
        if self.antiExp and self.can_add_waiter:
            ActionBot.instance.AddNewWaiter(3, _anti_exp)
            self.can_add_waiter = False

    def SetSpeedHackMultiplier(self, new_speed_multiplier):
        self.speedMultiplier = new_speed_multiplier
        if self.speedHack:
            eXLib.SetMoveSpeedMultiplier(self.speedMultiplier)

    def OnSpeedHackOnOff(self):
        if self.speedHack:
            self.speedHack = False
        else:
            self.speedHack = True
        if self.speedHack:
            eXLib.SetMoveSpeedMultiplier(self.speedMultiplier)
        else:
            eXLib.SetMoveSpeedMultiplier(0.0)

    #PICKUP
    def OnChangePickMode(self,val):
        self.excludeInFilter = val
        if not val:
            eXLib.ItemGrndOnFilter()
        else:
            eXLib.ItemGrndNotOnFilter()

    def delPickFilterItem(self,id):
        eXLib.ItemGrndDelFilter(id)
        self.pickFilter.remove(int(id))

    def addPickFilterItem(self,id):
        eXLib.ItemGrndAddFilter(id)
        self.pickFilter.add(int(id))
        
    def PickUp(self):
        if self.pickUp:

            if self.doNotPickupIfPlayerHere:
                if OpenLib.IsAnyPlayerHere():
                    return

            val, self.pickUpTimer = OpenLib.timeSleep(self.pickUpTimer,self.pickUpSpeed)
            if not val:
                return
            if OpenLib.GetCurrentPhase() != OpenLib.PHASE_GAME:
                return
            x,y,z = player.GetMainCharacterPosition()
            vid,itemX,itemY = eXLib.GetCloseItemGround(x,y)
            if vid == 0:
                return
            dst = OpenLib.dist(x,y,itemX,itemY)
            allowedRange = max(self.pickUpRange,float(OpenLib.MAX_PICKUP_DIST)) 
            if dst <= allowedRange:
                #Teleport to item
                if dst >= OpenLib.MAX_PICKUP_DIST:
                    #return
                    if not self.useRangePickup:
                        return
                    
                    #if self.checkIsWallBetweenPlayerAndItem:
                    #    if eXLib.IsPathBlocked(x, y, itemX, itemY):
                    #        return

                    Movement.TeleportStraightLine(x,y,itemX,itemY)
                    eXLib.SendPickupItem(vid)
                    Movement.TeleportStraightLine(itemX,itemY,x,y)
                else:
                    eXLib.SendPickupItem(vid)    

    def OnUpdate(self):
        self.CheckUsePotions()
        self.checkReviveAndLogin()
        self.PickUp()
        self.antiExpFunc()
     
def GetIDsItemsToSell():
    global instance
    """
    Returns a set with all items IDs which should be sold.
    Returns:
        [set]: Returns a set with all items which should be sold.
    """
    return instance.sellItems

def GetSlotItemsToSell():
    global instance
    """
    Returns a set with all items slots which should be sold.
    Returns:
        [set]: Returns a set with all slots which should be sold.
    """
    items = instance.sellItems
    slots = set()
    for i in range(0,OpenLib.MAX_INVENTORY_SIZE):
        item = player.GetItemIndex(i)
        if item != 0 and item in items:
            slots.add(i)
    return slots

def GetLastTimeDead():
    """
    Returns the last time the player was dead from OpenLib.GetTime and the amount of time to wait.
    Returns:
        tupple[float,float]: Returns the last time the player was dead and the time to wait.
    """
    global instance
    return (instance.lastTimeDead, instance.GetTimeAfterDead())
    

#SettingsDialog().Show()
instance = SettingsDialog()
instance.Show()
