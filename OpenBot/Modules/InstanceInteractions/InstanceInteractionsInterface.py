from OpenBot.Modules.InstanceInteractions.shopper_interface import SHOPPER_INTERFACE_ACTIONS
from OpenBot.Modules.InstanceInteractions.shopper_interface import shopper_interface
from OpenBot.Modules.InstanceInteractions.instance_interactions_module import instance_interactions_module

class InstanceInteractionsInterface:

    def SetStatus(self, status):
        for key in status.keys():

            if key in SHOPPER_INTERFACE_ACTIONS.keys():
                shopper_interface.SetStatus(status)

    def GetStatus(self):
        return {
            'Shopper': shopper_interface.GetStatus(),
        }

    def SetSelectedNPC(self, new_npc_id):
        instance_interactions_module.selected_npc = new_npc_id



instance_interactions_interface = InstanceInteractionsInterface()

