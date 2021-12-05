from OpenBot.Modules import OpenLib
from OpenBot.Modules.Actions import ActionFunctions
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
import ui, shop, background, net

STATES = {
    'WAITING': 'WAITING',
    'RUNNING': 'RUNNING'
}

NPC_EVENT_ANSWERS = {
    9009: [1],
    9001: [0, 0],
    9002: [0, 0],
    9003: [0],
}

class ShopperModule(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.npc_id_to_open = 0
        self.current_state = STATES['WAITING']
        self.shop_items = []
        self.items_to_buy = []

        self.is_shop_scanned = False
        self.current_action_done = True
        self.lastTime = 0

    def on_current_action_done(self):
        self.current_action_done = True

    def _scan_shop_for_items(self):
        self.is_shop_scanned = True
        self.shop_items = [{'id': shop.GetItemID(slot),
                            'slot': slot,
                            'price': shop.GetItemPrice(slot),
                            'count': shop.GetItemCount(slot)}
                           for slot in range(shop.SHOP_SLOT_COUNT) if shop.GetItemID(slot)]

    def OnUpdate(self):
        if OpenLib.IsInGamePhase() and self.current_state == STATES['WAITING']:
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 3)
            if val:
                self.current_state = STATES['RUNNING']

        elif OpenLib.IsInGamePhase() and self.current_state == STATES['RUNNING'] and self.current_action_done:
            val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.5)
            if val:
                if self.npc_id_to_open and not shop.IsOpen():
                    action_dict = {
                        'function_args': [self.npc_id_to_open, NPC_EVENT_ANSWERS[self.npc_id_to_open], background.GetCurrentMapName()],
                        'function': ActionFunctions.TalkWithNPC,
                        'callback': self.on_current_action_done
                    }
                    self.current_action_done = False
                    action_bot_interface.AddAction(action_dict)
                    return

                elif self.npc_id_to_open and shop.IsOpen():

                    if not self.shop_items:
                        self._scan_shop_for_items()

                    if self.items_to_buy:
                        item_to_buy = self.items_to_buy.pop()
                        net.SendShopBuyPacket(item_to_buy)


shopper_module = ShopperModule()
shopper_module.Show()

