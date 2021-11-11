from OpenBot.Modules.InstanceInteractions.shopper_module import shopper_module
import shop

SHOPPER_INTERFACE_ACTIONS = {
    'OPEN_SHOP': 'OPEN_SHOP',
    'CLOSE_SHOP': 'CLOSE_SHOP',
    'BUY_ITEMS': 'BUY_ITEMS',
}

class ShopperInterface:

    def SetStatus(self, status):
        for key in status.keys():
            if key == SHOPPER_INTERFACE_ACTIONS['OPEN_SHOP']:
                shopper_module.npc_id_to_open = status[key]['NpcIdToOpen']

            elif key == SHOPPER_INTERFACE_ACTIONS['CLOSE_SHOP']:
                shopper_module.npc_id_to_open = 0
                shopper_module.items_to_buy = []
                shopper_module.shop_items = []

            elif key == SHOPPER_INTERFACE_ACTIONS['BUY_ITEMS']:
                shopper_module.items_to_buy = [item['slot'] for item in status[key]['ItemsToBuy']]


    def GetStatus(self):
        return {
            'SelectedNPC': shopper_module.npc_id_to_open,
            'ItemsInShop': shopper_module.shop_items,
            'IsShopOpen': shop.IsOpen(),
        }



shopper_interface = ShopperInterface()