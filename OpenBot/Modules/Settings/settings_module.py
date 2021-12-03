from OpenBot.Modules.OpenLog import DebugPrint
import ui,net,player,eXLib, chat, background, chr
from OpenBot.Modules import Movement, OpenLib, Hooks


class SettingsDialog(ui.ScriptWindow):
    TIME_DEAD = 10
    TIME_POTS = 0.2
    RED_POTIONS_IDS = [27001,27002,27003,27007,27051,27201,27202,27203]
    BLUE_POTIONS_IDS = [27004,27005,27006,27008,27052,27204,27205,27206,63018]

    def __init__(self):
        ui.ScriptWindow.__init__(self)
        self.renderTextures = True
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
        self.pickUpSpeed = 0.3
        self.pickFilter = []
        self.excludeInFilter = True
        self.useRangePickup = False
        self.doNotPickupIfPlayerHere = False
        self.checkIsWallBetweenPlayerAndItem = False
        self.pickItemsFirst = True
        self.pickItemsIgnorePath = False
        self.useOnClickDmg = False
        self.onClickDmgSpeed = 0.0
        self.timerDmg = OpenLib.GetTime()
        self.can_add_revive_action = True
        self.wallHack = False
        self.sellItems = set()
        self.autoLogin = False
        self.can_add_waiter = True
        self.timerPots = 0
        self.timerDead = 0
        self.pickUpTimer = 0
        self.autoLoginTimer = 0

    # General
    def CheckUsePotions(self):
        val, self.timerPots = OpenLib.timeSleep(self.timerPots,self.TIME_POTS)
        if val:
            if self.redPotions and (float(player.GetStatus(player.HP)) / (float(player.GetStatus(player.MAX_HP))) * 100) < int(self.minHealth):
                OpenLib.UseAnyItemByID(self.RED_POTIONS_IDS)

            if self.bluePotions and (float(player.GetStatus(player.SP)) / (float(player.GetStatus(player.MAX_SP))) * 100) < int(self.minMana):
                OpenLib.UseAnyItemByID(self.BLUE_POTIONS_IDS)

    def revive_callback(self):
        self.can_add_revive_action = True

    def switch_render_textures(self):
        if self.renderTextures:
            self.renderTextures = False
            eXLib.SkipRenderer()
        else:
            self.renderTextures = True
            #eXLib.UnskipRender()

    def checkReviveAndLogin(self):
        val, self.timerDead = OpenLib.timeSleep(self.timerDead, self.TIME_DEAD)

        if not val:
            return

        if player.GetStatus(player.HP) <= 0:
            chat.AppendChat(3, 'dead')
            x, y, z = chr.GetPixelPosition(net.GetMainActorVID())
            OpenLib.LAST_DEATH_POINT = [[int(x), int(y)], background.GetCurrentMapName()]

            if self.restartHere:
                if self.can_add_revive_action:
                    self.can_add_revive_action = False
                    from OpenBot.Modules.Actions import ActionBot, ActionFunctions, ActionRequirementsCheckers
                    chat.AppendChat(3, 'added recovering here ')
                    ActionBot.instance.NewActionReturned({
                        'name': 'Recovering',
                        'function_args': [0, ['waithack']],
                        'function': ActionFunctions.WaitFor,
                        'requirements': {ActionRequirementsCheckers.IS_HP_RECOVERED: []},
                        'callback': self.revive_callback,
                    })
                OpenLib.Revive()
            elif self.restartInCity:
                try:
                    if self.can_add_revive_action:
                        self.can_add_revive_action = False
                        from OpenBot.Modules.Actions import ActionBot, ActionFunctions, ActionRequirementsCheckers
                        chat.AppendChat(3, 'added recovering city')
                        ActionBot.instance.NewActionReturned({
                            'name': 'Recovering',
                            'function_args': [0, ['waithack']],
                            'function': ActionFunctions.WaitFor,
                            'requirements': {ActionRequirementsCheckers.IS_HP_RECOVERED: []},
                            'callback': self.revive_callback,
                        })
                    Hooks.GetGameWindow().interface.dlgRestart.RestartTown()
                except Exception as e:
                    DebugPrint('Error while recovering in city')
                    DebugPrint(str(e))

        if self.autoLogin and OpenLib.GetCurrentPhase() == OpenLib.PHASE_LOGIN:
            from OpenBot.Modules.Protector.protector_module import protector_module
            val, self.autoLoginTimer = OpenLib.timeSleep(self.autoLoginTimer,
                                                         protector_module.time_to_wait_in_login_phase)
            if not val: return
            net.DirectEnter(0, 0)
    
    def WallHackSwich(self, val):
        if bool(val):
            self.wallHack = True
            eXLib.DisableCollisions()
        else:
            self.wallHack = False
            eXLib.EnableCollisions()

    def antiExpFunc(self):
        from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface

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
            action_bot_interface.AddWaiter(0.5, _anti_exp)
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

    def SetPickupRange(self, value):
        self.pickUpRange = value
        eXLib.ItemGrndSelectRange(self.pickUpRange)

    #PICKUP
    def OnChangePickItemFirst(self,val):
        self.pickItemsFirst = val
        if(self.pickItemsFirst):
            eXLib.ItemGrndItemFirst()
        else:
            eXLib.ItemGrndNoItemFirst()

    def OnChangePickItemsIgnorePath(self,val):
        self.pickItemsIgnorePath = val
        if(self.pickItemsIgnorePath):
            eXLib.ItemGrndInBlockedPath()
        else:
            eXLib.ItemGrndNotInBlockedPath()

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
        self.pickFilter.append(int(id))
        
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
