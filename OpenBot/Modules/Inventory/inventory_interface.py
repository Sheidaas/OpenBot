from OpenBot.Modules.OpenLog import DebugPrint
import player, item, net, shop


class InventoryInterface:

    def SetStatus(self, status):

        if status['action'] == 'upgrade_items':
            self.UpgradeListOfItems(status['items_list'], status['number_to_upgrade'], mode=status['mode'])
        
        if status['action'] == 'sell_all_items':
            self.SellListOfItems(status['items_list'])
        
        if status['action'] == 'drop_all_items':
            self.DropAllItems(status['items_list'])

    def GetStatus(self):
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

    def UpgradeListOfItems(self, items_list, number_to_upgrade, mode=0):
        for item_slot in items_list:
            for x in range(number_to_upgrade):
                net.SendRefinePacket(item_slot, mode)

    def SellListOfItems(self, items_list):
        if shop.IsOpen():
            for slot in items_list:
                net.SendShopSellPacketNew(slot,player.GetItemCount(slot),1)

    def DropAllItems(self, items_list):
        for slot in items_list:
            DebugPrint(slot)
            net.SendItemDropPacketNew(slot, player.GetItemCount(slot))

inventory_interface = InventoryInterface()