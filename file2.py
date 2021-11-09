#import chat
import eXLib
#from OpenBot.Modules.Inventory import inventory_interface
#from OpenBot.Modules import OpenLib
#from OpenBot.Modules.Settings import settings_interface
#from OpenBot.Modules.Networking import NetworkingWebsockets
#reload(settings_interface)
#reload(OpenLib)
#reload(inventory_interface)
#eXLib.SkipRenderer()
#import player, item, chat,

#for x in range(300):
    #ItemIndex = player.GetItemIndex(player.EQUIPMENT, x)
    #if ItemIndex != 0:
    #    ItemName = item.GetItemName(item.SelectItem(int(ItemIndex)))
    #    chat.AppendChat(3, str(int(ItemIndex)) + ' ' + ItemName)

#chat.AppendChat(3, str(inventory_interface.GetWearedItems()))

#_interface = FileHandlerInterface.FileHandlerInterface()
#chat.AppendChat(3, str(_interface.pickup_lists) + str(_interface.other_settings) + str(_interface.farmbot_paths))
#_interface.load_pickup_list('pickup_filter')
#_interface.dump_pickup_list()
#_interface.load_other_settings('new_settings')

#OpenLib.GetCurrentMetinLanguage())


#from OpenBot.Modules.Fishbot import fishbot_interface
#from OpenBot.Modules.Fishbot import fishbot_module

#reload(fishbot_module)
#reload(fishbot_interface)

#fishbot_interface.fishbot_interface.start()

#from OpenBot.Modules import Hooks
#import uiPrivateShopSearch, playerm2g2
#def x (x):
    #return True
#hook = Hooks.Hook(lambda: True, playerm2g2.GetItemCountByVnum)
#hook.HookFunction()

#new_ui = uiPrivateShopSearch.PrivateShopSeachWindow()
#new_ui.Open(True)

#import player, chat, net, m2netm2g
#chat.AppendChat(3, 'Current points: ')
#chat.AppendChat(3,  str(player.GetStatus(player.SKILL_ACTIVE)))


#OpenLib.GetAllBonusesOfItemBySlot(0)
#chat.AppendChat(3, 'dafs')

import shop, chat

if shop.IsOpen():
    for slot in range(shop.SHOP_SLOT_COUNT):
        chat.AppendChat(3, str(shop.GetItemID(slot)))

shop.Close()




