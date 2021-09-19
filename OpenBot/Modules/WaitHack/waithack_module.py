from OpenBot.Modules.OpenLog import DebugPrint
import eXLib, ui, net, chr, player, chat, item, skill
from OpenBot.Modules import OpenLib, FileManager, Movement
from OpenBot.Modules.FileManager import boolean

CLOUD_SKILL_STATE_WAITING = 0
CLOUD_SKILL_STATE_READY = 1
CLOUD_SKILL_STATE_USED = 2


class Waithack(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.lastTime = 0

        self.enabled = False
        self.range = 0
        self.speed = 0
        self.maxMonster = 0
        self.cloudSkillState = CLOUD_SKILL_STATE_READY

        self.attackPlayer = False
        self.avoidPlayers = False
        self.use_cloud_exploit = False
        self.is_wall_between = False
        self.attack_blocked_monsters = False

        self.LoadSettings()

    def __del__(self):
        ui.Window.__del__(self)

    def LoadSettings(self):
        self.maxMonster = float(FileManager.ReadConfig("WaitHack_MaxMonsters"))
        self.speed = float(FileManager.ReadConfig("WaitHack_Speed"))
        self.range = float(FileManager.ReadConfig("WaitHack_Range"))
        self.use_cloud_exploit = boolean(FileManager.ReadConfig("WaitHack_CloudExploit"))
        self.attackPlayer = boolean(FileManager.ReadConfig('WaitHack_attackPlayer'))
        self.avoidPlayers = boolean(FileManager.ReadConfig("WaitHack_PlayerClose"))
        self.is_wall_between = boolean(FileManager.ReadConfig("WaitHack_IsWallBetween"))
        self.attack_blocked_monsters = boolean(FileManager.ReadConfig("WaitHack_AttackBlocked"))

    def SaveSettings(self):
        FileManager.WriteConfig("WaitHack_MaxMonsters", str(self.maxMonster))
        FileManager.WriteConfig("WaitHack_Speed", str(self.speed))
        FileManager.WriteConfig("WaitHack_Range", str(self.range))
        FileManager.WriteConfig("WaitHack_PlayerClose", str(self.avoidPlayers))
        FileManager.WriteConfig("WaitHack_attackPlayer", str(self.attackPlayer))
        FileManager.WriteConfig("WaitHack_CloudExploit", str(self.use_cloud_exploit))
        FileManager.WriteConfig("WaitHack_IsWallBetween", str(self.is_wall_between))
        FileManager.WriteConfig("WaitHack_AttackBlocked", str(self.attack_blocked_monsters))
        FileManager.Save()

    def onEnableChange(self, val):
        if val:
            eXLib.BlockAttackPackets()
        else:
            eXLib.UnblockAttackPackets()

    def TeleportAttack(self, lst, x, y):
        Movement.TeleportStraightLine(self.lastPos[0], self.lastPos[1], x, y)
        self.lastPos = (x, y)
        # eXLib.SendStatePacket(x,y,0,eXLib.CHAR_STATE_STOP,0)
        vid_hits = 0
        for vid in lst:
            mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)
            if OpenLib.dist(x, y, mob_x, mob_y) < OpenLib.ATTACK_MAX_DIST_NO_TELEPORT:
                # chat.AppendChat(3,"Sent Attack, X:" + str(mob_x) + " Y:" + str(mob_y) + "VID: " +str(vid))
                eXLib.SendAttackPacket(vid, 0)
                lst.remove(vid)
                vid_hits += 1

        return vid_hits

    # chat.AppendChat(3,"After: " + str(len(lst)))

    def __sendUseSkill(self):
        instance.cloudSkillState = CLOUD_SKILL_STATE_READY

    def AttackArch(self, lst, x, y):
        vid_hits = 0
        # chat.AppendChat(3,"Attacking with arch")
        for enemy in lst:
            x, y, z = chr.GetPixelPosition(enemy)
            eXLib.SendAddFlyTarget(enemy, x, y)
            eXLib.SendShoot(eXLib.COMBO_SKILL_ARCH)
            lst.remove(enemy)
            vid_hits += 1
        return vid_hits

    def AttackCloud(self, lst, x, y):
        # chat.AppendChat(3,"Attacking with arch")
        Movement.TeleportStraightLine(self.lastPos[0], self.lastPos[1], x, y)
        self.lastPos = (x, y)
        # eXLib.SendStatePacket(x,y,0,eXLib.CHAR_STATE_STOP,0)
        vid_hits = 0
        for vid in lst:
            mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)
            if OpenLib.dist(x, y, mob_x, mob_y) < OpenLib.ATTACK_MAX_DIST_NO_TELEPORT:
                if not player.IsSkillCoolTime(5) and player.GetStatus(player.SP) > OpenLib.GetSkillManaNeed(35, 5):
                    if self.cloudSkillState == CLOUD_SKILL_STATE_READY:
                        eXLib.SendUseSkillPacketBySlot(5, vid)
                        self.cloudSkillState = CLOUD_SKILL_STATE_USED
                    elif self.cloudSkillState == CLOUD_SKILL_STATE_WAITING:
                        return 999999999
                    else:
                        OpenLib.SetTimerFunction(1, self.__sendUseSkill)
                        self.cloudSkillState = CLOUD_SKILL_STATE_WAITING
                        return 99999999
                x, y, z = chr.GetPixelPosition(vid)
                eXLib.SendAttackPacket(vid, 0)
                eXLib.SendAddFlyTarget(vid, x, y)
                eXLib.SendShoot(35)
                lst.remove(vid)
                vid_hits += 1

        return vid_hits

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, self.speed)
        if val and self.enabled and not eXLib.IsDead(net.GetMainActorVID()):
            if OpenLib.GetCurrentPhase() != OpenLib.PHASE_GAME:
                return
            isArch = OpenLib.IsWeaponArch()
            main_vid = net.GetMainActorVID()
            x, y, z = chr.GetPixelPosition(main_vid)
            self.lastPos = (x, y)
            lst = list()

            for vid in eXLib.InstancesList:
                if vid == main_vid:
                    continue

                if not chr.HasInstance(vid):
                    continue

                if self.avoidPlayers and OpenLib.IsThisPlayer(vid):
                    return

                if OpenLib.IsThisNPC(vid):
                    continue

                if self.attackPlayer and OpenLib.IsThisPlayer(vid):
                    continue

                if player.GetCharacterDistance(vid) <= self.range and not eXLib.IsDead(vid):
                    lst.append(vid)

            hit_counter = 0
            i = 0
            # chat.AppendChat(3,str(len(lst)))
            while len(lst) > 0 and hit_counter < self.maxMonster:
                vid = lst[0]
                mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)
                if not self.attack_blocked_monsters:
                    if eXLib.IsPositionBlocked(mob_x, mob_y):
                        lst.remove(vid)
                        continue
                if self.is_wall_between:
                    if eXLib.IsPathBlocked(x, y, mob_x, mob_y):
                        lst.remove(vid)
                        continue
                if self.use_cloud_exploit and OpenLib.GetClass() == OpenLib.SKILL_SET_DAGGER_NINJA:
                    hit_counter += self.AttackCloud(lst, mob_x, mob_y)
                elif isArch:
                    hit_counter += self.AttackArch(lst, mob_x, mob_y)
                else:
                    hit_counter += self.TeleportAttack(lst, mob_x, mob_y)
                i += 1
            if (OpenLib.dist(x, y, self.lastPos[0], self.lastPos[1]) >= 50):
                Movement.TeleportStraightLine(self.lastPos[0], self.lastPos[1], x, y)

instance = Waithack()
instance.Show()