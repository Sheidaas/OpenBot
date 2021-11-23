import chr
import eXLib
import ui
import net
import chat
from OpenBot.Modules import OpenLib

STATES = {
    'WAITING': 'WAITING',
    'RUNNING': 'RUNNING'
}


class Radar(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.current_state = STATES['WAITING']
        self.check_for_players = True
        self.players = []
        self.check_for_ores = True
        self.ores = []
        self.check_for_metins = True
        self.metins = []

        self.last_time = 0

    def add_new_entity(self, entity):
        if chr.GetNameByVID(entity) == 'None':
            return

        if OpenLib.IsThisPlayer(entity):
            self.players.append(entity)
        elif OpenLib.IsThisOre(entity):
            self.ores.append(entity)
        elif OpenLib.IsThisMetin(entity):
            self.metins.append(entity)

    def OnUpdate(self):

        if self.current_state == STATES['WAITING'] and OpenLib.IsInGamePhase():
            val, self.last_time = OpenLib.timeSleep(self.last_time, 3)
            if val:
                self.current_state = STATES['RUNNING']

        elif self.current_state == STATES['RUNNING'] and OpenLib.IsInGamePhase():
            val, self.last_time = OpenLib.timeSleep(self.last_time, 0.1)
            if val:

                # Refreshing lists
                self.players = []
                self.metins = []
                self.ores = []
                # Adding new entities to selected lists
                for vid in eXLib.InstancesList:

                    if vid == net.GetMainActorVID():
                        continue

                    if chr.GetInstanceType(vid) == OpenLib.MONSTER_TYPE:
                        continue

                    if vid in self.players + self.ores + self.metins:
                        continue

                    self.add_new_entity(vid)

                #chat.AppendChat(3, str([(chr.GetNameByVID(player), chr.GetInstanceType(player)) for player in self.players]))


radar_module = Radar()
radar_module.Show()
