from OpenBot.Modules.Attacker.attacker_module import attacker_module
import chat

STATUS_KEYS = {
    'MINIMUM_HP_TO_ATTACK': 'MinimumHpToAttack',
    'CAN_USE_SKILLS': 'CanUseSkills',
    'MIN_MONSTERS_GRADE_TO_USE_SKILL': 'MinMonstersGradeToUseSkill',
    'TIME_BETWEEN_SKILLS': 'TimeBetweenSkills',
    'STOP': 'Stop',
    'ATTACK': 'Attack',
    'ADD_WHOLE_GROUP_TO_KILL': 'AddWholeGroupToKill',
}


class AttackerInterface:

    def SetStatus(self, status):
        chat.AppendChat(3, str(status))
        for key in status:

            if STATUS_KEYS['MINIMUM_HP_TO_ATTACK'] == key:
                attacker_module.minimum_hp_to_attack = status[key]

            elif STATUS_KEYS['CAN_USE_SKILLS'] == key:
                attacker_module.can_use_skills = status[key]

            elif STATUS_KEYS['MIN_MONSTERS_GRADE_TO_USE_SKILL'] == key:
                attacker_module.min_monsters_grade_to_use_skill = status[key]

            elif STATUS_KEYS['TIME_BETWEEN_SKILLS'] == key:
                attacker_module.time_between_skills = status[key]

            elif STATUS_KEYS['ADD_WHOLE_GROUP_TO_KILL'] == key:
                attacker_module.add_whole_group_to_kill = status[key]

            elif STATUS_KEYS['STOP'] == key:
                attacker_module.stop()

            elif STATUS_KEYS['ATTACK'] == key:
                attacker_module.select_mob_to_kill(status[key], lambda : 0, lock_vid=True)


    def GetStatus(self):
        return {
            STATUS_KEYS['MINIMUM_HP_TO_ATTACK']: attacker_module.minimum_hp_to_attack,
            STATUS_KEYS['CAN_USE_SKILLS']: attacker_module.can_use_skills,
            STATUS_KEYS['MIN_MONSTERS_GRADE_TO_USE_SKILL']: attacker_module.min_monsters_grade_to_use_skill,
            STATUS_KEYS['TIME_BETWEEN_SKILLS']: attacker_module.time_between_skills,
            STATUS_KEYS['ADD_WHOLE_GROUP_TO_KILL']: attacker_module.add_whole_group_to_kill,
        }

attacker_interface = AttackerInterface()
