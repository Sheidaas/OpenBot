from OpenBot.Modules.OpenLog import DebugPrint
from OpenBot.Modules.Actions import ActionFunctions, ActionRequirementsCheckers, ActionBot
from BotBase import BotBase
import UIComponents
import ui

# Alchemist 20001 29200, 81200 c1
# Weapon Dealer 9001 43000 60700

#shonso weapon dealer 9001 59600 55700
#alchemist 20001 622 511

#chunjo weapon dealer 676 662
# 660 734
class EnergyBot(BotBase):

    def __init__(self):
        BotBase.__init__(self, 0.5)
        self.ItemSlotToBuy = 4
        self.ItemCountToBuy = 5
        self.BuildWindow()

    def BuildWindow(self):
        comp = UIComponents.Component()
        self.Board = ui.BoardWithTitleBar()
        self.Board.SetSize(235, 190)
        self.Board.SetPosition(52, 40)
        self.Board.AddFlag('movable')
        self.Board.SetTitleName('EnergyBot')
        self.Board.SetCloseEvent(self.switch_state)
        self.Board.Hide()


        self.slot_barItemCountToBuy, self.edit_lineItemCountToBuy = \
            comp.EditLine(self.Board, str(self.ItemCountToBuy), 20, 40, 20, 20, 25)
        self.text_lineItemCountToBuy = comp.TextLine(self.Board, 'how many items buy', 50, 47, comp.RGB(255, 255, 255))

        self.slot_barItemSlotToBuy, self.edit_lineItemSlotToBuy= \
            comp.EditLine(self.Board, str(self.ItemSlotToBuy), 20, 60, 20, 20, 25)
        self.text_lineItemSlotToBuy = comp.TextLine(self.Board, 'item slot to buy in Weapon shop dealer', 50, 67, comp.RGB(255, 255, 255))

        self.SwitchEnableExchangeEnergyToCrystal = comp.OnOffButton(self.Board, '\t\t\t\t\t\tExchange energy?', 'If check, character will try to exchange energy to crystals',
                                20, 100,  funcState=self.SwitchEnableExchangeEnergyToCrystal, defaultValue=False)

        self.enableEnergyBot = comp.OnOffButton(self.Board, '', '', 170, 140,
                                            OffUpVisual='OpenBot/Images/start_0.tga',
                                            OffOverVisual='OpenBot/Images/start_1.tga',
                                            OffDownVisual='OpenBot/Images/start_2.tga',
                                            OnUpVisual='OpenBot/Images/stop_0.tga',
                                            OnOverVisual='OpenBot/Images/stop_1.tga',
                                            OnDownVisual='OpenBot/Images/stop_2.tga',
                                            funcState=self.SwitchEnableEnergyBot, defaultValue=False)       


    def SwitchEnableExchangeEnergyToCrystal(self, val):
        pass
    
    def AddExchangeEnergyToCrystalToStage(self):
        actions_dict = {0: {'args': [20001, (62200, 51100), 'metin2_map_a1'],
              'function': ActionFunctions.ChangeEnergyToCrystal,
              'requirements': {},
              'callback': instance.SetIsCurrActionDoneTrue},
              1: {'args': [20001, (66000, 73400), 'metin2_map_b1'],
              'function': ActionFunctions.ChangeEnergyToCrystal,
              'requirements': {},
              'callback': instance.SetIsCurrActionDoneTrue},
              2: {'args': [20001, (29200, 81200), 'metin2_map_c1'],
              'function': ActionFunctions.ChangeEnergyToCrystal,
              'requirements': {},
              'callback': instance.SetIsCurrActionDoneTrue},
              }
        self.currSchema['stages'][self.currStage]['actions'].append(actions_dict[self.currStage])

    def SwitchEnableEnergyBot(self, val):
        if val:
            self.Start()
            self.currSchema = ENERGY_BOT_SCHEMA
            self.RecognizeStartStage()
            if self.SwitchEnableExchangeEnergyToCrystal.isOn:
                self.AddExchangeEnergyToCrystalToStage()
        else:
            self.Stop()
        
        DebugPrint(str(self.currSchema))

    def RecognizeStartStage(self):
        if ActionRequirementsCheckers.isInMaps(['metin2_map_a1']):
            self.currStage = 0
        elif ActionRequirementsCheckers.isInMaps(['metin2_map_b1']):
            self.currStage = 1
        elif ActionRequirementsCheckers.isInMaps(['metin2_map_c1']):
            self.currStage = 2
        else:
            self.Stop()
    
    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.Board.Show()

    def Frame(self):
        if self.isCurrActionDone:
            action_dict = self.currSchema['stages'][self.currStage]['actions'][self.currAction]
            self.isCurrActionDone = False
            if ActionFunctions.GoBuyItemsFromNPC.__name__ == self.currSchema['stages'][self.currStage]['actions'][self.currAction]['function'].__name__:
                item_count = int(self.edit_lineItemCountToBuy.GetText())
                item_slot = int(self.edit_lineItemSlotToBuy.GetText())
                self.currSchema['stages'][self.currStage]['actions'][self.currAction]['args'][0] = [item_slot for x in range(item_count)]
            ActionBot.instance.AddNewAction(action_dict)
            DebugPrint(str(action_dict))

instance = EnergyBot()

ENERGY_BOT_SCHEMA = {
    'requirements': {
        'maps': ['metin2_map_a1', 'metin2_map_b1', 'metin2_map_c1'],
        'lvl': 35},
    'options': {
        'SlotToBuy': 4,
        'CountItemToBuy': 10,},
    'stages': {
        0: {'options': [ActionBot.STAGE_REPEAT],
            'actions': [{'args': [[], 9001, (59600, 55700), instance.SetIsCurrActionDoneTrue], # position
                        'function': ActionFunctions.GoBuyItemsFromNPC,
                        'requirements': {}
                        },
                        {'args': [[1040], 20001, (62200, 51100)], # position
                        'function': ActionFunctions.GetEnergyFromAlchemist,
                        'requirements': {},
                        'callback': instance.SetIsCurrActionDoneTrue
                        },
                        ]},
        1: {'options': [ActionBot.STAGE_REPEAT],
            'actions': [{'args': [[], 9001, (67600, 66200), instance.SetIsCurrActionDoneTrue], # position
                        'function': ActionFunctions.GoBuyItemsFromNPC,
                        'requirements': {}
                        },
                        {'args': [[1040], 20001, (66000, 73400)], # position
                        'function': ActionFunctions.GetEnergyFromAlchemist,
                        'requirements': {},
                        'callback': instance.SetIsCurrActionDoneTrue
                        },
                        ]},
        2: {'options': [ActionBot.STAGE_REPEAT],
            'actions': [{'args': [[], 9001, (43000, 60700), instance.SetIsCurrActionDoneTrue], # position
                        'function': ActionFunctions.GoBuyItemsFromNPC,
                        'requirements': {}
                        },
                        {'args': [[1040], 20001, (29200, 81200)], # position
                        'function': ActionFunctions.GetEnergyFromAlchemist,
                        'requirements': {},
                        'callback': instance.SetIsCurrActionDoneTrue
                        },
                        ]}
    }
}