from OpenBot.Modules.ShopSearcher.shop_searcher_module import shop_searcher_module

STATUS = {
    'ENABLED': 'Enabled',
}


class ShopSearcherInterface:

    def SetStatus(self, status):
        for key in status.keys():

            if STATUS['ENABLED'] == key:
                self.switch_enabled()

    def GetStatus(self):
        return {
            STATUS['ENABLED']: shop_searcher_module.enabled,
        }

    @staticmethod
    def switch_enabled():
        shop_searcher_module.enabled = not shop_searcher_module.enabled

shop_searcher_interface = ShopSearcherInterface()