from OpenBot.Modules.Fishbot.fishbot_module import fishbot_module

STATUS_KEYS = {
    'ENABLED': 'Enabled',
    'STARTING_POSITION': 'StartingPosition',
    'CHECK_REPETITIONS': 'CheckRepetitions',
    'MAX_REPETITIONS': 'MaxRepetitions',
    'REPETITIONS': 'Repetitions',
    'GRILL_FISH': 'GrillFish',
    'INSTANT_FISHING': 'InstantFishing',
    'MIN_TIME_BETWEEN_FISH': 'MinTimeBetweenFish',
    'MAX_TIME_BETWEEN_FISH': 'MaxTimeBetweenFish',
    'FISH_ID_TO_OPEN': 'FishIdToOpen',
    'DEAD_FISH_ID_TO_GRILL': 'DeadFishIdToGrill',
    'DEAD_FISH_ID_TO_DROP': 'DeadFishIdToDrop',
    'CATCHES_TO_DROP': 'CatchesToDrop',
    'CATCHES_TO_SELL': 'CatchesToSell',
}


class FishbotInterface:

    def SetStatus(self, status):

        if status[STATUS_KEYS['ENABLED']] and status[STATUS_KEYS['ENABLED']] != fishbot_module.enabled:
            self.start()
        elif not status[STATUS_KEYS['ENABLED']] and status[STATUS_KEYS['ENABLED']] != fishbot_module.enabled:
            self.stop()

        if status[STATUS_KEYS['GRILL_FISH']] != fishbot_module.grill_fish:
            self.switch_grill_fish()

        if status[STATUS_KEYS['INSTANT_FISHING']] != fishbot_module.instant_fishing:
            self.switch_instant_fishing()

        if status[STATUS_KEYS['CHECK_REPETITIONS']] != fishbot_module.check_repetitions:
            self.switch_repetitions()

        if status[STATUS_KEYS['MAX_REPETITIONS']] != fishbot_module.max_repetitions:
            self.set_max_repetitions(status[STATUS_KEYS['MAX_REPETITIONS']])

        if status[STATUS_KEYS['MIN_TIME_BETWEEN_FISH']] != fishbot_module.min_time_between_fish:
            self.set_min_time_between_fish(status[STATUS_KEYS['MIN_TIME_BETWEEN_FISH']])

        if status[STATUS_KEYS['MAX_TIME_BETWEEN_FISH']] != fishbot_module.max_time_between_fish:
            self.set_max_time_between_fish(status[STATUS_KEYS['MAX_TIME_BETWEEN_FISH']])

        if status[STATUS_KEYS['FISH_ID_TO_OPEN']] != fishbot_module.fish_id_to_open:
            fishbot_module.fish_id_to_open = status[STATUS_KEYS['FISH_ID_TO_OPEN']]

        if status[STATUS_KEYS['DEAD_FISH_ID_TO_GRILL']] != fishbot_module.dead_fish_id_to_grill:
            fishbot_module.dead_fish_id_to_grill = status[STATUS_KEYS['DEAD_FISH_ID_TO_GRILL']]

        if status[STATUS_KEYS['DEAD_FISH_ID_TO_DROP']] != fishbot_module.dead_fish_it_to_drop:
            fishbot_module.dead_fish_it_to_drop = status[STATUS_KEYS['DEAD_FISH_ID_TO_DROP']]

        if status[STATUS_KEYS['CATCHES_TO_SELL']] != fishbot_module.catches_to_sell:
            fishbot_module.catches_to_sell = status[STATUS_KEYS['CATCHES_TO_SELL']]

        if status[STATUS_KEYS['CATCHES_TO_DROP']] != fishbot_module.catches_to_drop:
            fishbot_module.catches_to_drop = status[STATUS_KEYS['CATCHES_TO_DROP']]

        return

    def GetStatus(self):
        return {
            STATUS_KEYS['ENABLED']: fishbot_module.enabled,
            STATUS_KEYS['STARTING_POSITION']: fishbot_module.starting_position,
            STATUS_KEYS['GRILL_FISH']: fishbot_module.grill_fish,
            STATUS_KEYS['INSTANT_FISHING']: fishbot_module.instant_fishing,
            STATUS_KEYS['CHECK_REPETITIONS']: fishbot_module.check_repetitions,
            STATUS_KEYS['MAX_REPETITIONS']: fishbot_module.max_repetitions,
            STATUS_KEYS['REPETITIONS']: fishbot_module.repetitions,
            STATUS_KEYS['MIN_TIME_BETWEEN_FISH']: fishbot_module.min_time_between_fish,
            STATUS_KEYS['MAX_TIME_BETWEEN_FISH']: fishbot_module.max_time_between_fish,
            STATUS_KEYS['FISH_ID_TO_OPEN']: fishbot_module.fish_id_to_open,
            STATUS_KEYS['DEAD_FISH_ID_TO_GRILL']: fishbot_module.dead_fish_id_to_grill,
            STATUS_KEYS['DEAD_FISH_ID_TO_DROP']: fishbot_module.dead_fish_it_to_drop,
            STATUS_KEYS['CATCHES_TO_SELL']: fishbot_module.catches_to_sell,
            STATUS_KEYS['CATCHES_TO_DROP']: fishbot_module.catches_to_drop,
        }

    def start(self):
        fishbot_module.start()

    def stop(self):
        fishbot_module.stop()

    def switch_grill_fish(self):
        if fishbot_module.grill_fish:
            fishbot_module.grill_fish = False
        else:
            fishbot_module.grill_fish = True

    def switch_repetitions(self):
        if fishbot_module.check_repetitions:
            fishbot_module.check_repetitions = False
        else:
            fishbot_module.check_repetitions = True

    def switch_instant_fishing(self):
        fishbot_module.switch_instant_fish()

    def set_max_repetitions(self, max_repetitions):
        fishbot_module.max_repetitions = max_repetitions

    def set_min_time_between_fish(self, time_to_set):
        if time_to_set > fishbot_module.max_time_between_fish:
            fishbot_module.min_time_between_fish = fishbot_module.max_time_between_fish
        elif time_to_set < 1:
            fishbot_module.min_time_between_fish = 1
        else:
            fishbot_module.min_time_between_fish = time_to_set

    def set_max_time_between_fish(self, time_to_set):
        if time_to_set < fishbot_module.min_time_between_fish:
            fishbot_module.max_time_between_fish = fishbot_module.min_time_between_fish
        elif time_to_set > 15:
            fishbot_module.max_time_between_fish = 15
        else:
            fishbot_module.max_time_between_fish = time_to_set

fishbot_interface = FishbotInterface()
