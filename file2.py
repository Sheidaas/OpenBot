
from OpenBot.Modules import AutoDungeon, OpenLog
from OpenBot.Modules.Radar import Radar
from OpenBot.Modules import ChannelSwitcher
from OpenBot.Modules import DmgHacks, Hooks, MapManager
import chat, eXLib, player, chr,net,skill,app, background,event
from OpenBot.Modules import Radar,FarmingBot, Movement, Settings, OpenLib, Skillbot,ChannelSwitcher,Movement, FishingBot
from OpenBot.Modules.Actions import ActionFunctions


#orig_select_answer = event.SelectAnswer



#event.SelectAnswer = printFunc


#reload(FishingBot)
#x,y,z = player.GetMainCharacterPosition()
#vid,itemX,itemY = eXLib.GetCloseItemGround(x,y)
#if(vid!=0):
#    eXLib.SendPickupItem(vid)
#    chr.SetPixelPosition(itemX,itemY)
#    #eXLib.ClearOutput()


#Movement.GoToPositionAvoidingObjects(141700,146500,mapName="map_a2")
#Movement.GoToPositionAvoidingObjects(141700,146500,mapName="metin2_map_n_desert_01")

#Hooks._debugHookFunctionArgs(event.SelectAnswer)
#vid = player.GetTargetVID()

#eXLib.SendStartFishing(10)

#    #app.SetFrameSkip(1)
#    chat.AppendChat(3,str(eXLib.GetItemGrndID(vid)))
#

#vid = player.GetTargetVID()
#x,y,z = eXLib.GetPixelPosition(vid)
#chr.SelectInstance(vid)
#race = chr.GetRace()
#
#val = ActionFunctions.TalkWithNPC([race,(x,y),[5]])
#OpenLib.skipAnswers([3])
#eXLib.GetRequest("www.google.com",OpenLog.handleRequest)
#OpenLib.showAnswers()

#chat.AppendChat(3,str(background.GetCurrentMapName()))


val = eXLib.SendWebsocket(2,"frontend_client")
chat.AppendChat(3,str(val))