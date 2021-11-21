import ui,app,chat,chr,net,player,wndMgr,uiCommon,eXLib
from OpenBot.Modules.WaitHack.waithack_module import instance
from OpenBot.Modules.Farmbot.farmbot_module import farm
from OpenBot.Modules.Fishbot.fishbot_module import fishbot_module
from OpenBot.Modules.Settings.settings_module import instance as sett_instance
from OpenBot.Modules.Skillbot.skillbot_module import instance as skillbot_instance
from OpenBot.Modules import PythonManager, Hooks, UIComponents
from OpenBot.Modules.Networking import NetworkingWebsockets


class OpenBotHackbarDialog(ui.ScriptWindow): 				

    Hackbar = 0
    Teleport = 0
    ShortCuts = 0
    comp = UIComponents.Component()
    python_manager = PythonManager.PythonManagerDialog()

    

    def __init__(self):
        self.OpenBotBoard = ui.ThinBoard(layer="TOP_MOST")
        self.OpenBotBoard.SetPosition(0, 40)
        self.OpenBotBoard.SetSize(51, 75)
        self.OpenBotBoard.AddFlag("float")
        self.OpenBotBoard.AddFlag("movable")
        self.OpenBotBoard.Hide()


        self.ShowHackbarButton = self.comp.Button(None, '', 'Show Hackbar', wndMgr.GetScreenWidth()-99, 260, self.OpenHackbar, eXLib.PATH + 'OpenBot/Images/Shortcuts/show_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/show_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/show_0.tga')
        self.HideHackbarButton = self.comp.HideButton(None, '', 'Hide Hackbar', wndMgr.GetScreenWidth()-99, 260, self.OpenHackbar, eXLib.PATH + 'OpenBot/Images/Shortcuts/hide_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/hide_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/hide_0.tga')
        self.ShortCutButton = self.comp.Button(None, '', 'ShortCuts', wndMgr.GetScreenWidth()-62, 260, self.OpenShortCuts, eXLib.PATH + 'OpenBot/Images/Shortcuts/shortcut_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/shortcut_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/shortcut_0.tga')
        self.CrashButton = self.comp.HideButton(None, '', 'Exit', wndMgr.GetScreenWidth()-45, 310, self.CloseRequest, eXLib.PATH + 'OpenBot/Images/Shortcuts/close_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/close_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/close_0.tga')

        self.RunPythonButton = self.comp.Button(self.OpenBotBoard, '', 'Run-Python', 10, 10, self.RunPython, eXLib.PATH + 'OpenBot/Images/Shortcuts/loadpy_0.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/loadpy_1.tga', eXLib.PATH + 'OpenBot/Images/Shortcuts/loadpy_0.tga')
        self.networkButton = self.comp.Button(self.OpenBotBoard, '', 'Reconnect server', 8, 45, self.OnNetworkButton, eXLib.PATH + 'OpenBot/Images/Hackbar/action_0.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/action_1.tga', eXLib.PATH + 'OpenBot/Images/Hackbar/action_0.tga')

    def OpenHackbar(self):
        if self.Hackbar:
            self.Hackbar = 0
            self.ShowHackbarButton.Show()
            self.HideHackbarButton.Hide()
            self.OpenBotBoard.Hide()
        else:
            self.Hackbar = 1
            self.ShowHackbarButton.Hide()
            self.HideHackbarButton.Show()
            self.OpenBotBoard.Show()

    def OpenShortCuts(self):
        if player.GetName() == "":
            #return
            pass
        if self.ShortCuts:
            self.ShortCuts = 0
            self.CrashButton.Hide()
        else:
            self.ShortCuts = 1
            self.CrashButton.Show()

    def OnNetworkButton(self):
        reload(NetworkingWebsockets)

    def RunPython(self):
        self.python_manager.switch_state()

    def CloseRequest(self):
        self.QuestionDialog = uiCommon.QuestionDialog()
        self.QuestionDialog.SetText("Do You want to quit Metin2 immediately?")
        self.QuestionDialog.SetAcceptEvent(ui.__mem_func__(self.Close))
        self.QuestionDialog.SetCancelEvent(ui.__mem_func__(self.CancelQuestionDialog))
        self.QuestionDialog.Open()
        
    def Close(self):
        app.Abort()

    def CancelQuestionDialog(self):
        self.QuestionDialog.Close()
        self.QuestionDialog = None


try:
    app.Shop.Close()
except:
    pass

settings_loaded = False
def __PhaseChangeLoadSettingsCallback(phase, phaseWnd):
    global settings_loaded
    from OpenBot.Modules.FileHandler.FileHandlerInterface import file_handler_interface
    from OpenBot.Modules import OpenLib
    if phase == OpenLib.PHASE_GAME and not settings_loaded:
        def load():
            file_handler_interface.load_last_other_settings()
            file_handler_interface.load_last_farmbot_paths()
            file_handler_interface.load_last_pickup_list()
        OpenLib.SetTimerFunction(2, load)
        settings_loaded = True


Hooks.registerPhaseCallback("loadingCallback", __PhaseChangeLoadSettingsCallback)

app.Shop = OpenBotHackbarDialog()