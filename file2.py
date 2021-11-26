import chat
from OpenBot.Modules.Protector.protector_interface import protector_interface
from OpenBot.Modules.Protector.protector_module import protector_module
from OpenBot.Modules import radar_module
#reload(radar_module)
#reload(protector_module)

#chat.AppendChat(3, str(protector_interface.GetStatus()))
protector_interface.switch_change_channel()