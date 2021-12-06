import eXLib, ui, net, chr, player, skill, chat
from OpenBot.Modules import OpenLib, Movement

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

        self.instance_type_to_attack = []
        self.attack_bosses = False
        self.use_cloud_exploit = False
        self.is_wall_between = False
        self.attack_blocked_monsters = False

    def __del__(self):
        ui.Window.__del__(self)

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
                vid_hits += 1

        return vid_hits

    def OnUpdate(self):
        val, self.lastTime = OpenLib.timeSleep(self.lastTime, self.speed)
        if not val or not self.enabled or eXLib.IsDead(net.GetMainActorVID()):
            return

        main_vid = net.GetMainActorVID()
        isArch = OpenLib.IsWeaponArch()
        x, y, z = chr.GetPixelPosition(main_vid)
        self.lastPos = (x, y)
        mobs_to_attack = []

        for vid in eXLib.InstancesList:
            if vid == main_vid:
                continue
            if player.GetCharacterDistance(vid) > self.range:
                continue
            chr.SelectInstance(vid)
            if eXLib.IsDead(vid):
                continue

            type = chr.GetInstanceType(vid)

            if type not in self.instance_type_to_attack:

                if self.attack_bosses and type == OpenLib.MONSTER_TYPE and chr.GetRace(vid) in OpenLib.BOSS_IDS.keys():
                    pass
                else:
                    continue

            mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)
            if not self.attack_blocked_monsters:
                if eXLib.IsPositionBlocked(mob_x, mob_y):
                    continue

            if self.is_wall_between:
                if eXLib.IsPathBlocked(x, y, mob_x, mob_y):
                    continue

            mobs_to_attack.append(vid)

            if len(mobs_to_attack) > self.maxMonster:
                break

        hit_counter = 0
        chat.AppendChat(3, str(mobs_to_attack))
        for vid in mobs_to_attack:
            mob_x, mob_y, mob_z = chr.GetPixelPosition(vid)

            if self.use_cloud_exploit and OpenLib.GetClass() == OpenLib.SKILL_SET_DAGGER_NINJA:
                hit_counter += self.AttackCloud(mobs_to_attack, mob_x, mob_y)
            elif isArch:
                hit_counter += self.AttackArch(mobs_to_attack, mob_x, mob_y)
            else:
                hit_counter += self.TeleportAttack(mobs_to_attack, mob_x, mob_y)

            if hit_counter > self.maxMonster:
                break

        if (OpenLib.dist(x, y, self.lastPos[0], self.lastPos[1]) >= 50):
            Movement.TeleportStraightLine(self.lastPos[0], self.lastPos[1], x, y)


instance = Waithack()
instance.Show()
