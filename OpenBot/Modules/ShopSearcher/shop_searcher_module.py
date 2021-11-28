from OpenBot.Modules import OpenLib
from OpenBot.Modules import OpenLog
import eXLib
import ui
import chr
import shop
import chat
import net


STATES = {
    'WAITING': 'WAITING',
    'SCANNING_AREA': 'SCANNING_AREA',
    'SCANNING_SHOPS': 'SCANNING_SHOPS',
}


class ShopSearcherModule(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.enabled = True
        self.current_state = STATES['WAITING']

        self.open_shop_attempts = 0
        self.current_scanning_name = ''
        self.player_names_to_scan = []
        self.scanned_player_names = []

        self.last_time = 0
        self.last_waiting_time = 0

    @staticmethod
    def get_player_vid_by_name(player_name):
        for vid in eXLib.InstancesList:
            chr.SelectInstance(vid)
            if chr.GetNameByVID(vid) == player_name:
                return vid
        return 0

    def scan_shop(self):
        slot_count = 40
        items = []
        for item_slot in range(slot_count * shop.GetTabCount()):
            item_id = shop.GetItemID(item_slot)
            if not item_id:
                continue
            price = shop.GetItemPrice(item_slot)
            item_bonuses = self.scan_item_bonuses(item_slot)
            count = shop.GetItemCount(item_slot)
            items.append({item_id: {'price': price,
                                    'item_bonuses': item_bonuses,
                                    'count': count,
                                    'item_slot': shop.GetItemCheque(item_slot),
                                    }})

        return items

    def scan_item_bonuses(self, item_slot):
        item_bonuses = []
        for x in range(10):
            metin_socket = shop.GetItemMetinSocket(item_slot, x)
            if not metin_socket:
                continue
            item_bonuses.append(metin_socket)

        return item_bonuses

    def OnUpdate(self):
        if not self.enabled:
            return

        val, self.last_time = OpenLib.timeSleep(self.last_time, 0.1)
        if not val:
            return

        if self.current_state == STATES['WAITING']:
            chat.AppendChat(3, 'WAITING')
            val, self.last_waiting_time = OpenLib.timeSleep(self.last_waiting_time, 1)
            if not val:
                return
            self.current_state = STATES['SCANNING_AREA']

        if self.current_state == STATES['SCANNING_AREA']:
            chat.AppendChat(3, 'SCANNING AREA')
            for vid in eXLib.InstancesList:
                chr.SelectInstance(vid)
                name = chr.GetNameByVID(vid)
                if OpenLib.MIN_RACE_SHOP <= chr.GetRace() <= OpenLib.MAX_RACE_SHOP \
                        and name not in self.scanned_player_names:
                    self.player_names_to_scan.append(name)
            self.current_state = STATES['SCANNING_SHOPS']

        if self.current_state == STATES['SCANNING_SHOPS']:
            chat.AppendChat(3, 'SCANNING SHOPS')
            if not self.player_names_to_scan:
                self.current_state = STATES['SCANNING_AREA']
                return

            if not self.current_scanning_name:
                self.current_scanning_name = self.player_names_to_scan.pop()

            shop_vid = self.get_player_vid_by_name(self.current_scanning_name)
            if not shop_vid:
                return
            chat.AppendChat(3, str(self.current_scanning_name))
            net.SendOnClickPacket(shop_vid)
            if shop.IsOpen():
                self.open_shop_attempts = 0
                self.scanned_player_names.append(self.current_scanning_name)
                self.current_scanning_name = ''
                items = self.scan_shop()
                net.SendShopEndPacket()
                OpenLog.DebugPrint(str(items))
                self.current_state = STATES['WAITING']

            self.open_shop_attempts += 1
            if self.open_shop_attempts > 2:
                self.open_shop_attempts = 0
                self.scanned_player_names.append(self.current_scanning_name)
                self.current_scanning_name = ''


shop_searcher_module = ShopSearcherModule()
shop_searcher_module.Show()



