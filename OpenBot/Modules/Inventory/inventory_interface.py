from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Dropper import dropper
import player, item, net, shop


class InventoryInterface:

    def SetStatus(self, status):
        DebugPrint(str(status))
        if status['action'] == 'upgrade_items':
            self.UpgradeListOfItems(status['items_list'], status['number_to_upgrade'], mode=status['mode'])
        
        elif status['action'] == 'sell_all_items':
            self.SellListOfItems(status['items_list'])
        
        elif status['action'] == 'drop_all_items':
            self.DropAllItems(status['items_list'])

        elif status['action'] == 'use_all_items':
            self.UseAllItems(status['items_list'])

    def GetStatus(self):
        return {
             'Inventory': self.GetInventory(),
             'Equipment': self.GetWearedItems(),
        }

    def GetInventory(self):
        items = []
        for i in range(100):
            ItemIndex = player.GetItemIndex(i)
            if ItemIndex != 0:
                ItemName = item.GetItemName(item.SelectItem(int(ItemIndex)))
                items.append({
                    'id': player.GetItemIndex(i),
                    'count': player.GetItemCount(i),
                    'slot': i,
                })
        return items
    
    def GetWearedItems(self):
        return {
            'Weapon': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_WEAPON) },
            'Body': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_BODY) },
            'Head': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_HEAD) },
            'Neck': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_NECK) },
            'Glove': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_GLOVE) },
            'Ear': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_EAR) },
            'Shoes': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_SHOES) },
            'Pendant': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_PENDANT) },
            'Unique1': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_UNIQUE1) },
            'Unique2': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_UNIQUE2) },
            'Count': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_COUNT) },
            'Belt': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_BELT) },
            'Arrow': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_ARROW) },
            'Wrist': { 'id': player.GetItemIndex(player.EQUIPMENT, item.EQUIPMENT_WRIST) },
        }

    def UpgradeListOfItems(self, items_list, number_to_upgrade, mode=0):
        for item_slot in items_list:
            for x in range(number_to_upgrade):
                net.SendRefinePacket(item_slot, mode)

    def SellListOfItems(self, items_list):
        from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
        time = 0.3
        if shop.IsOpen():
            for slot in items_list:
                action_bot_interface.AddWaiter(time, lambda: net.SendShopSellPacketNew(slot,player.GetItemCount(slot),1))
                time += 0.3
                

    def DropAllItems(self, items_list):
        for slot in items_list:
            dropper.add_new_item_to_drop(slot)

    def UseAllItems(self, items_list):
        from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
        time = 0.3
        for slot in items_list:
            action_bot_interface.AddWaiter(time, lambda: net.SendItemUsePacket(slot))
            time += 0.3

inventory_interface = InventoryInterface()