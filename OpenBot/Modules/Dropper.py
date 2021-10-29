from OpenBot.Modules import OpenLib, OpenLog
import ui
import player
import net


class Dropper(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.items_slots_to_drop = []
        self.lastTime = 0

    def add_new_item_to_drop(self, item_slot):
        if item_slot not in self.items_slots_to_drop:
            self.items_slots_to_drop.append(item_slot)

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.2)
        if val and self.items_slots_to_drop:
            item_to_drop = self.items_slots_to_drop.pop()
            if player.GetItemCount(item_to_drop):
                net.SendItemDropPacketNew(item_to_drop, player.GetItemCount(item_to_drop))
                if player.GetItemCount(item_to_drop):
                    self.add_new_item_to_drop(item_to_drop)

dropper = Dropper()
dropper.Show()
