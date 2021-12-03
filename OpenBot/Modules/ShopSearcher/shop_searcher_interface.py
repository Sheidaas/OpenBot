from OpenBot.Modules.ShopSearcher.shop_searcher_module import shop_searcher_module

STATUS = {
    'ENABLED': 'Enabled',
    'BUY_ITEM': 'BuyItem',
}


class ShopSearcherInterface:

    def SetStatus(self, status):
        for key in status.keys():

            if STATUS['ENABLED'] == key:
                self.switch_enabled(status[key])

            if STATUS['BUY_ITEM'] == key:
                pass

    def GetStatus(self):
        return {
            STATUS['ENABLED']: shop_searcher_module.enabled,
        }

    @staticmethod
    def switch_enabled(running_state):
        shop_searcher_module.change_running_state(running_state)

    def buy_item(self, buy_dict):
        chat.AppendChat(3, str(buy_dict))
        pass

shop_searcher_interface = ShopSearcherInterface()