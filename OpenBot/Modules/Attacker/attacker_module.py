import ui
import chr
import player
import eXLib
import net
import nonplayer
import chat
from OpenBot.Modules import OpenLib, Hooks
from OpenBot.Modules.Actions import ActionFunctions, ActionRequirementsCheckers, Action
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface

STAGES = {
    'STOPPED': 'STOPPED',
    'RUNNING': 'RUNNING',
}

ATTACKING_STAGE = {
    'STARTING': 'STARTING',
    'MOVING': 'MOVING',
    'ESCAPING': 'ESCAPING',
    'ATTACKING': 'ATTACKING',
    'FINISHED': 'FINISHED',
}

def OnLoginPhase(phase, phaseWnd):
    global attacker_module
    if OpenLib.IsInGamePhase():
        attacker_module.discard_current_action()
        attacker_module.stop()


class Attacker(ui.ScriptWindow):

    def __init__(self):
        ui.Window.__init__(self)
        self.current_stage = STAGES['STOPPED']
        self.current_attacking_stage = ATTACKING_STAGE['STARTING']

        self.target_vid_in_attack = 0
        self.target_vid = 0
        self.distance_to_target = 0
        self.additional_vid_targets_to_kill = []
        self.current_action_done = True
        self.callback = None

        self.last_mob_position = ()
        self.was_engaged = False
        self.last_time = 0
        self.last_hp = 0

        self.minimum_hp_to_attack = 50
        self.lock_vid = False
        self.can_use_skills = True
        self.min_monsters_grade_to_use_skill = 4
        self.time_between_skills = 3
        self.add_whole_group_to_kill = True

        self.can_use_skill = True
        self.use_skill_timer = 0

    def select_mob_to_kill(self, new_vid_target, callback, lock_vid=False):
        self.lock_vid = lock_vid
        self.target_vid = new_vid_target
        self.target_vid_in_attack = new_vid_target
        self.current_stage = STAGES['RUNNING']
        self.callback = callback

    def stop(self):
        self.lock_vid = False
        self.was_engaged = False
        self.additional_vid_targets_to_kill = []
        self.target_vid_in_attack = 0
        self.target_vid = 0
        self.current_stage = STAGES['STOPPED']
        self.current_attacking_stage = ATTACKING_STAGE['STARTING']

    def return_dist_to_target(self, target):
        my_x, my_y, z = chr.GetPixelPosition(net.GetMainActorVID())
        target_x, target_y, z = chr.GetPixelPosition(target)
        return OpenLib.dist(my_x, my_y, target_x, target_y)

    def on_walking_callback(self):
        self.current_action_done = True
        self.was_engaged = True
        self.current_attacking_stage = ATTACKING_STAGE['ATTACKING']

    def on_attacking_callback(self):
        self.target_vid_in_attack = 0
        self.current_action_done = True

    def in_change_current_attacking_target(self):
        if not eXLib.IsDead(self.target_vid_in_attack) and self.lock_vid:
            return self.target_vid_in_attack

        self.lock_vid = False
        my_x, my_y, z = chr.GetPixelPosition(net.GetMainActorVID())
        curr_x, curr_y, z = chr.GetPixelPosition(self.target_vid_in_attack)
        distance_to_current_vid = OpenLib.dist(my_x, my_y, curr_x, curr_y)
        chosen_closed_vid = OpenLib.GetNearestVidFromList(self.additional_vid_targets_to_kill)
        chosen_closed_x, chosen_closed_y, z = chr.GetPixelPosition(chosen_closed_vid)

        vids_to_kill = [vid for vid in eXLib.InstancesList
                        if chr.GetInstanceType(vid) == OpenLib.MONSTER_TYPE
                        and 350 >= OpenLib.distance_to_vid(vid)]

        new_closed_vid = OpenLib.GetNearestVidFromList(vids_to_kill)
        new_closed_x, new_closed_y, z = chr.GetPixelPosition(new_closed_vid)

        distance_to_chosen = OpenLib.dist(my_x, my_y, chosen_closed_x, chosen_closed_y)
        distance_to_new_closed = OpenLib.dist(my_x, my_y, new_closed_x, new_closed_y)

        [self.additional_vid_targets_to_kill.append(vid) for vid in vids_to_kill]

        if distance_to_chosen >= distance_to_current_vid and distance_to_new_closed >= distance_to_current_vid:
            return self.target_vid_in_attack

        if 350 >= distance_to_current_vid:
            self.was_engaged = True
            self.discard_current_action()
            if distance_to_new_closed >= distance_to_chosen:
                return chosen_closed_vid
            self.additional_vid_targets_to_kill.append(new_closed_vid)
            return new_closed_vid
        return chosen_closed_vid

    def choose_target(self):
        if self.current_attacking_stage == ATTACKING_STAGE['ATTACKING']:
            self.target_vid_in_attack = self.in_change_current_attacking_target()

        if not self.target_vid_in_attack:
            if eXLib.IsDead(self.target_vid) and self.additional_vid_targets_to_kill:
                new_vid = OpenLib.GetNearestVidFromList(self.additional_vid_targets_to_kill)
                try:
                    self.additional_vid_targets_to_kill.remove(new_vid)
                except ValueError:
                    pass
                self.target_vid_in_attack = new_vid
            else:
                self.target_vid_in_attack = self.target_vid

    def discard_current_action(self):
        from OpenBot.Modules.Actions.ActionBot import instance
        instance.DiscardActionByParent('attacker')
        self.current_action_done = True

    def on_walking_interruptor_callback(self):
        self.current_action_done = True
        self.current_attacking_stage = ATTACKING_STAGE['STARTING']
        return Action.NEXT_ACTION

    def return_which_state_should_be_played(self):
        if (not self.target_vid_in_attack or eXLib.IsDead(self.target_vid_in_attack)) and not self.lock_vid:
            self.discard_current_action()
            return ATTACKING_STAGE['FINISHED']

        player.SetTarget(self.target_vid_in_attack)
        Hooks.GetGameWindow().targetBoard.Hide()

        if self.current_attacking_stage == ATTACKING_STAGE['MOVING']:
            return ATTACKING_STAGE['MOVING']

        if not self.was_engaged and self.minimum_hp_to_attack > float(player.GetStatus(player.HP)) / float(
                player.GetStatus(player.MAX_HP)) * 100:
            if self.last_hp > float(player.GetStatus(player.HP)):
                self.was_engaged = True
                return ATTACKING_STAGE['STARTING']
            self.last_hp = float(player.GetStatus(player.HP))
            self.was_engaged = False
            return ATTACKING_STAGE['STARTING']

        target_to_vid = self.return_dist_to_target(self.target_vid_in_attack)
        if 750 > target_to_vid:
            return ATTACKING_STAGE['ATTACKING']
        else:
            return ATTACKING_STAGE['MOVING']

    def interrupt_walking_function(self):
        self.current_action_done = True
        self.current_attacking_stage = ATTACKING_STAGE['STARTING']
        return Action.DISCARD

    def generate_walking_action(self):
        self.current_action_done = False
        enemy_x, enemy_y, z = chr.GetPixelPosition(self.target_vid_in_attack)
        action_dict = {
            'call_only_once': True,
            'name': '[Attacker] Moving to target',
            'function_args': [[enemy_x, enemy_y]],
            'function': ActionFunctions.MoveToPosition,
            'requirements': {ActionRequirementsCheckers.IS_ON_POSITION: [enemy_x, enemy_y]},
            'interrupt_function': self.interrupt_walking_function,
            'interruptors': [ActionRequirementsCheckers.isNearInstance],
            'interruptors_args': [self.target_vid_in_attack],
            'callback': self.on_walking_callback,
            'callback_on_failed': self.on_walking_interruptor_callback,
            'parent': 'attacker',
        }
        return action_dict

    def generate_attack_action(self):
        self.current_action_done = False
        return {'function_args': [self.target_vid_in_attack],
                'function': ActionFunctions.DestroyByVID,
                'callback': self.on_attacking_callback,
                'parent': 'attacker'
                }

    def use_skill(self):
        if not self.can_use_skill:
            val, self.use_skill_timer = OpenLib.timeSleep(self.use_skill_timer, self.time_between_skills)
            if not val:
                return
            self.can_use_skill = True

        current_skill_set = OpenLib.GetClassSkillIDs(OpenLib.GetClass())
        if current_skill_set == OpenLib.SKILL_SET_NONE:
            return

        vids_to_kill = [vid for vid in eXLib.InstancesList
                        if chr.GetInstanceType(vid) == OpenLib.MONSTER_TYPE
                        and 300 >= OpenLib.distance_to_vid(vid) and not eXLib.IsDead(vid)]

        monsters_grade = sum([nonplayer.GetGradeByVID(vid)+1 for vid in vids_to_kill]) + nonplayer.GetGradeByVID(self.target_vid_in_attack)
        #chat.AppendChat(3, str(monsters_grade))
        if self.min_monsters_grade_to_use_skill > monsters_grade:
            return

        from OpenBot.Modules.Skillbot.skillbot_module import instance
        # usable skill cant be active skill, it have at least has 1 lvl and cannot be on cd
        usable_skills = [skill for skill in current_skill_set if skill not in instance.ACTIVE_SKILL_IDS and
                         player.GetSkillLevel(current_skill_set.index(skill)+1) and
                         not player.IsSkillCoolTime(current_skill_set.index(skill) + 1)]
        if not usable_skills:
            return

        if not 300 >= OpenLib.distance_to_vid(self.target_vid_in_attack):
            return

        player.ClickSkillSlot(current_skill_set.index(usable_skills.pop()) + 1)
        self.can_use_skill = False

    def OnUpdate(self):
        val, self.last_time = OpenLib.timeSleep(self.last_time, 0.1)
        if not val:
            return

        if self.current_stage == STAGES['STOPPED']:
            return
        if self.current_stage == STAGES['RUNNING']:
            last_vid = self.target_vid_in_attack
            my_x, my_y, my_z = chr.GetPixelPosition(net.GetMainActorVID())
            self.choose_target()
            self.current_attacking_stage = self.return_which_state_should_be_played()

            if last_vid != self.target_vid_in_attack and not self.current_action_done:
                self.discard_current_action()

            x, y, z = chr.GetPixelPosition(self.target_vid_in_attack)
            if self.current_attacking_stage == ATTACKING_STAGE['MOVING'] and self.last_mob_position:
                if OpenLib.dist(x, y, self.last_mob_position[0], self.last_mob_position[1]) > 500:
                    self.discard_current_action()
            if self.current_attacking_stage == ATTACKING_STAGE['MOVING'] and self.last_mob_position and \
                    (eXLib.IsPositionBlocked(self.last_mob_position[0], self.last_mob_position[1])
                    or (not eXLib.FindPath(my_x, my_y, self.last_mob_position[0], self.last_mob_position[1]))):
                self.discard_current_action()
            if self.current_attacking_stage == ATTACKING_STAGE['ATTACKING'] and self.can_use_skills:
                self.use_skill()

            if not self.current_action_done:
                return

            if self.current_attacking_stage == ATTACKING_STAGE['MOVING']:
                player.SetAttackKeyState(False)
                dist_to_target = self.return_dist_to_target(self.target_vid_in_attack)
                self.last_mob_position = (x, y)
                if 750 >= dist_to_target:
                    self.on_walking_callback()
                    return

                action_bot_interface.AddActionAsLast(self.generate_walking_action())

            if self.current_attacking_stage == ATTACKING_STAGE['ATTACKING']:
                self.was_engaged = True
                action_bot_interface.AddActionAsLast(self.generate_attack_action())

            if self.current_attacking_stage == ATTACKING_STAGE['FINISHED']:
                self.discard_current_action()
                self.current_attacking_stage = ATTACKING_STAGE['STARTING']
                self.current_stage = STAGES['STOPPED']
                self.was_engaged = False
                player.SetAttackKeyState(False)
                self.callback()

attacker_module = Attacker()
attacker_module.Show()
Hooks.registerPhaseCallback('pauseAttacker', OnLoginPhase)