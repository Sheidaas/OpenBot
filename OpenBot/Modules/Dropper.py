from OpenBot.Modules import OpenLib, OpenLog
import ui
import player
import net
import shop



class Dropper(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.items_slots_to_drop = []
        self.items_slots_to_sell = []
        self.items_slots_to_use = []

        self.lastTime = 0

    def add_new_item_to_drop(self, item_slot):
        if item_slot not in self.items_slots_to_drop:
            self.items_slots_to_drop.append(item_slot)

    def add_new_item_to_sell(self, item_slot):
        if item_slot not in self.items_slots_to_sell:
            self.items_slots_to_sell.append(item_slot)

    def add_new_item_to_use(self, item_slot):
        if item_slot not in self.items_slots_to_use:
            self.items_slots_to_use.append(item_slot)

    @staticmethod
    def is_item_slot_in_chosen_items_list(items_id, items_list):
        excluded_items = []
        for slots in items_id.values():
            for slot in slots:
                if slot not in items_list:
                    excluded_items.append(slots)

        return excluded_items or False


    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 2)
        if val:
            if self.items_slots_to_drop:
                item_to_drop = self.items_slots_to_drop.pop()
                if player.GetItemCount(item_to_drop):
                    net.SendItemDropPacketNew(item_to_drop, player.GetItemCount(item_to_drop))

            if self.items_slots_to_sell:
                if shop.IsOpen():
                    item_to_sell = self.items_slots_to_sell.pop()
                    net.SendShopSellPacketNew(item_to_sell, player.GetItemCount(item_to_sell), 1)
                else:
                    self.items_slots_to_sell = []

            if self.items_slots_to_use:
                item_to_use = self.items_slots_to_use.pop()
                net.SendItemUsePacket(item_to_use)


dropper = Dropper()
dropper.Show()
