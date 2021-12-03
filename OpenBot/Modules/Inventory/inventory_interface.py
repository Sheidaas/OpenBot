from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules import OpenLib
from OpenBot.Modules.Dropper import dropper
import player, item, net, chat, skill

STATUS = {
    'FREE_SLOTS': 'FreeSlots',
    'MAX_INVENTORY_SIZE': 'MaxInventorySize',
    'INVENTORY': 'Inventory',
    'EQUIPMENT': 'Equipment'
}
STATUS_ACTIONS = {
    'UPGRADE_ITEMS': 'upgrade_items',
    'SELL_ALL_ITEMS': 'sell_all_items',
    'DROP_ALL_ITEMS': 'drop_all_items',
    'USE_ALL_ITEMS': 'use_all_items',
    'USE_ITEM_ON_EQUIPMENT': 'use_item_on_equipment'
}
EQUIPMENT_NAMES = {
    'WEAPON': 'Weapon',
    'BODY': 'Body',
    'HEAD': 'Head',
    'NECK': 'Neck',
    'GLOVE': 'Glove',
    'EAR': 'Ear',
    'SHOES': 'Shoes',
    'PENDANT': 'Pendant',
    'UNIQUE1': 'Unique1',
    'UNIQUE2': 'Unique2',
    'COUNT': 'Count',
    'BELT': 'Belt',
    'ARROW': 'Arrow',
    'WRIST': 'Wrist',
    'SHIELD': 'Shield',
}
EQUIPMENT_SLOTS = {
    EQUIPMENT_NAMES['WEAPON']: item.EQUIPMENT_WEAPON,
    EQUIPMENT_NAMES['BODY']: item.EQUIPMENT_BODY,
    EQUIPMENT_NAMES['HEAD']: item.EQUIPMENT_HEAD,
    EQUIPMENT_NAMES['NECK']: item.EQUIPMENT_NECK,
    EQUIPMENT_NAMES['GLOVE']: item.EQUIPMENT_GLOVE,
    EQUIPMENT_NAMES['EAR']: item.EQUIPMENT_EAR,
    EQUIPMENT_NAMES['SHOES']: item.EQUIPMENT_SHOES,
    EQUIPMENT_NAMES['PENDANT']: item.EQUIPMENT_PENDANT,
    EQUIPMENT_NAMES['UNIQUE1']: item.EQUIPMENT_UNIQUE1,
    EQUIPMENT_NAMES['UNIQUE2']: item.EQUIPMENT_UNIQUE2,
    EQUIPMENT_NAMES['COUNT']: item.EQUIPMENT_COUNT,
    EQUIPMENT_NAMES['BELT']: item.EQUIPMENT_BELT,
    EQUIPMENT_NAMES['ARROW']: item.EQUIPMENT_ARROW,
    EQUIPMENT_NAMES['WRIST']: item.EQUIPMENT_WRIST,
    EQUIPMENT_NAMES['SHIELD']: 10,
}

class InventoryInterface:

    def SetStatus(self, status):
        DebugPrint(str(status))
        if status['action'] == STATUS_ACTIONS['UPGRADE_ITEMS']:
            self.UpgradeListOfItems(status['items_list'], status['number_to_upgrade'], mode=status['mode'])
        
        elif status['action'] == STATUS_ACTIONS['SELL_ALL_ITEMS']:
            self.SellListOfItems(status['items_list'])
        
        elif status['action'] == STATUS_ACTIONS['DROP_ALL_ITEMS']:
            self.DropAllItems(status['items_list'])

        elif status['action'] == STATUS_ACTIONS['USE_ALL_ITEMS']:
            self.UseAllItems(status['items_list'])

        elif status['action'] == STATUS_ACTIONS['USE_ITEM_ON_EQUIPMENT']:
            self.UseItemOnEquipment(*status['items_list'])

    def GetStatus(self):
        return {
            STATUS['FREE_SLOTS']: OpenLib.GetNumberOfFreeSlots(),
            STATUS['MAX_INVENTORY_SIZE']: OpenLib.MAX_INVENTORY_SIZE,
            STATUS['INVENTORY']: self.GetInventory(),
            STATUS['EQUIPMENT']: self.GetWearedItems(),
        }

    def GetInventory(self):
        items = []
        for i in range(OpenLib.MAX_INVENTORY_SIZE):
            ItemIndex = player.GetItemIndex(i)
            if not ItemIndex:
                return
            ItemName = item.GetItemName(item.SelectItem(int(ItemIndex)))
            if ItemIndex in [50300, 70037, 70055, 70104, 71093]:
                slot = player.GetItemMetinSocket(player.INVENTORY, i, 0)
            else:
                slot = False
            if slot:
                book_name = slot
            else:
                book_name = 'none'
            items.append({
            'name': ItemName,
            'book_name': book_name,
            'id': player.GetItemIndex(i),
            'count': player.GetItemCount(i),
            'type':
            'slot': i,

            })


            items.append({
            'icon': item.GetIconImageFileName(ItemIndex).replace("icon\item\\", '').replace('.tga', '')
            })



            items
        return items
    
    def GetWearedItems(self):
        eq = {}
        for key in EQUIPMENT_NAMES.keys():
            itemIndex = player.GetItemIndex(player.EQUIPMENT, EQUIPMENT_SLOTS[EQUIPMENT_NAMES[key]])
            item.SelectItem(int(itemIndex))
            eq[EQUIPMENT_NAMES[key]] = {'id': itemIndex,
                                        'icon': item.GetIconImageFileName(int(itemIndex)).replace("icon\item\\", '').replace('.tga', '')
                                        }
        return eq

    def UpgradeListOfItems(self, items_list, number_to_upgrade, mode=0):
        for item_slot in items_list:
            for x in range(number_to_upgrade):
                net.SendRefinePacket(item_slot, mode)

    def UseItemOnEquipment(self, key):
        net.SendItemUsePacket(player.EQUIPMENT, EQUIPMENT_SLOTS[EQUIPMENT_NAMES[key.upper()]])

    def SellListOfItems(self, items_list):
        for slot in items_list:
            dropper.add_new_item_to_sell(slot)

    def DropAllItems(self, items_list):
        for slot in items_list:
            dropper.add_new_item_to_drop(slot)

    def UseAllItems(self, items_list):
        for slot in items_list:
            dropper.add_new_item_to_use(slot)

inventory_interface = InventoryInterface()