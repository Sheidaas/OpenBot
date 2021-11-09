from OpenBot.Modules import OpenLib, MapManager
import ui

STATES = {
    'WAITING': 'WAITING',
    'RUNNING': 'RUNNING'
}


class ShopperModule(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.npc_id_to_open = 0
        self.is_shop_open = False
        self.current_state = STATES['WAITING']
        self.shop_items = []
        self.items_to_buy = []

        self.current_action_done = None
        self.lastTime = 0


    def OnUpdate(self):
        if OpenLib.IsInGamePhase() and self.current_state == STATES['WAITING']:
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 3)
            if val:
                self.current_state = STATES['RUNNING']

        elif OpenLib.IsInGamePhase() and self.current_state == STATES['RUNNING']:
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.2)
            if val:
                if self.npc_id_to_open and not self.is_shop_open:
                    npc_position = MapManager.GetNpcFromMap(OpenLib.GetPlayerEmpireSecondMap(), self.npc_id_to_open)
                    if OpenLib.isPlayerCloseToPosition(*npc_position, max_dist=500):
                        
