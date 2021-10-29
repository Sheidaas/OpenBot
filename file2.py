
#from OpenBot.Modules.Networking import NetworkingWebsockets
#reload(NetworkingWebsockets)

#from OpenBot.Modules import OpenLib, OpenLog
#OpenLog.DebugPrint(OpenLib.GetCurrentMetinLanguage())


#from OpenBot.Modules.Fishbot import fishbot_interface
#from OpenBot.Modules.Fishbot import fishbot_module

#reload(fishbot_module)
#reload(fishbot_interface)

#fishbot_interface.fishbot_interface.start()

from OpenBot.Modules import Hooks
import uiPrivateShopSearch, playerm2g2
def x (x):
    return True
hook = Hooks.Hook(lambda: True, playerm2g2.GetItemCountByVnum)
hook.HookFunction()

new_ui = uiPrivateShopSearch.PrivateShopSeachWindow()
new_ui.Open(True)