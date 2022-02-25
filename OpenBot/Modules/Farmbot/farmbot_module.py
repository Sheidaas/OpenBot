from OpenBot.Modules.Actions import Action, ActionFunctions, ActionRequirementsCheckers
from OpenBot.Modules.Actions.ActionBotInterface import action_bot_interface
from OpenBot.Modules.Protector.protector_module import protector_module
from OpenBot.Modules.ChannelSwitcher.channel_switcher_interface import channel_switcher_interface
from OpenBot.Modules import OpenLog, OpenLib, Movement, Hooks
from OpenBot.Modules.OpenLog import DebugPrint
import ui, chat, chr, net, player, background
import eXLib

# STATES
WAITING_STATE = 'WAITING_STATE'
WALKING_STATE = 'WALKING_STATE'
MINING_STATE = 'MINING_STATE'
FARMING_STATE = 'FARMING_STATE'
SWITCHING_CHANNEL = 'SWITCHING_CHANNEL'
GOING_TO_SHOP = 'GOING_TO_SHOP'
BUY_POTIONS = 'BUY_POTIONS'
GOING_TO_DEATH_POINT = 'GOING_TO_DEATH_POINT'
WAITING_UNTIL_HP_IS_NOT_REGENERATED = 'WAITING_UNTIL_HP_IS_NOT_REGENERATED'
PICKING_ITEM = 'PICKING_ITEM'
BOSS_STATE = 'BOSS_STATE'
MOB_STATE = 'MOB_STATE'
EXCHANGING_ITEMS_TO_ENERGY = 'EXCHANGING_ITEMS_TO_ENERGY'

ENABLE_STATES = {
	'ENABLED': 'ENABLED',
	'PAUSED': 'PAUSED',
	'STOPPED': 'STOPPED',
}


RED_POTIONS_IDS = [27001, 27002, 27003, 27007, 27051, 27201, 27202, 27203]
BLUE_POTIONS_IDS = [27004, 27005, 27006, 27008, 27052, 27204, 27205, 27206, 63018]

def OnLoginPhase(phase, phaseWnd):
	global farm
	if OpenLib.IsInGamePhase():
		farm.discard_current_action()
		farm.mobs_vid_list = []
		farm.CURRENT_STATE = WALKING_STATE

def OnDigMotionCallback(main_vid,target_ore,n):
	global farm
	#DebugPrint(str(main_vid) + ' ' + str(net.GetMainActorVID()))
	if(main_vid != net.GetMainActorVID()):
		return
	if farm.enabled and farm.look_for_ore:
		DebugPrint('Digging is starting')
		farm.is_currently_digging = True
		slash_time = n * farm.MINING_SLASH_TIME
		action_bot_interface.AddWaiter(slash_time, farm.IsCurrentlyDiggingDone)

def returnFuncWithArgs(func, args):
	def x():
		func(args)
	
	return x

class FarmingBot(ui.ScriptWindow):

	MINING_SLASH_TIME = 2.1

	def __init__(self):
		ui.Window.__init__(self)
		self.CURRENT_STATE = WALKING_STATE
		self.current_point = 0  # Current position index
		self.path = []  # list of tuples with coordinates [(0, 0, 'mapname'), (2, 2, 'map_name)] etc
		self.lastTime = 0
		self.enabled = ENABLE_STATES['STOPPED']
		eXLib.RegisterDigMotionCallback(OnDigMotionCallback)
		self.slash_timer = OpenLib.GetTime()
		self.hasRecivedSlash = False
		self.lastTimeMine = 0   
		self.ores_vid_list = []
		self.ores_to_mine = []
		self.boss_vid_list = []
		self.mobs_vid_list = []
		self.selectedOre = 0
		self.is_currently_digging = False
		self.metins_vid_list = []
		self.selectedMetin = 0
		self.selectedBoss = 0
		self.isCurrActionDone = True
		self.lastTimeWaitingState = 0
		self.timeForWaitingState = 5
		self.isReadyToSwitchChannel = False
		self.switch_channels = False
		self.look_for_metins = False
		self.metin_to_kill = []
		self.look_for_ore = False
		self.look_for_bosses = False
		self.look_for_mobs = True
		self.selectedMob = 0
		self.mobs_to_kill = []
		self.mobs_to_avoid = []
		self.exchange_items_to_energy = False
		self.potions_to_buy = []
		self.level_paths = {}
		self.current_level_path_key = 0
		self.can_go_sell_items = False
		self.skill_books_ids = []
		self.items_to_sell = []
		self.can_go_buy_potions = False
		self.potions_to_buy = []
		self.max_range_to_mob = 10000
		self.vid_skip_list = []
		self.items_to_pickup = []
		self.selectedItem = 0
		self.move_to_items = True
		self.last_death_point = []
		self.last_walking_is_player_near = False

	def __del__(self):
		ui.Window.__del__(self)

	def switch_move_to_items(self):
		if self.move_to_items:
			self.move_to_items = False
			self.items_to_pickup = []
		else:
			self.move_to_items = True

	def create_path(self, level):
		self.level_paths[level] = {'path': self.path, 'mobs_to_kill': self.mobs_to_kill}

	def set_path(self, key):
		if key not in self.level_paths.keys():
			return
		self.path = self.level_paths[key]['path']
		self.mobs_to_kill = self.level_paths[key]['mobs_to_kill']

	def delete_path(self, key):
		if key not in self.level_paths.keys():
			return
		del self.level_paths[key]

	def pop_path(self):
		for level in self.level_paths.keys():
			if level >= player.GetStatus(player.LEVEL):
				return level
		return self.current_level_path_key

	def onStart(self):
		if len(self.path) > 1:
			self.enabled = ENABLE_STATES['ENABLED']
			return True
		else:
			chat.AppendChat(3, '[Farmbot] - You need to add more than 1 waypoint!')
			self.onStop()
			return False

	def onStop(self):
		self.isCurrActionDone = True
		self.selectedMetin = 0
		self.selectedOre = 0
		self.current_point = 0
		self.selectedMob = 0
		self.selectedBoss = 0
		self.selectedItem = 0
		self.mobs_vid_list = []
		self.items_to_pickup = []
		self.is_currently_digging = False
		self.enabled = ENABLE_STATES['STOPPED']
		Movement.StopMovement()
		from OpenBot.Modules.Attacker.attacker_module import attacker_module
		attacker_module.discard_current_action()
		attacker_module.additional_vid_targets_to_kill = []
		attacker_module.target_vid_in_attack = 0
		attacker_module.target_vid = 0


	def DiscardingAction(self):
		self.isCurrActionDone = True

	def IsWalkingDone(self):
		self.isCurrActionDone = True
		self.CURRENT_STATE = WALKING_STATE
		self.next_point()

	def IsDestroyingMetinDone(self):
		self.isCurrActionDone = True
		self.selectedMetin = 0
		self.selectedBoss = 0
		self.selectedMob = 0
		self.CURRENT_STATE = WAITING_STATE
		self.lastTimeWaitingState = OpenLib.GetTime()

	def KilledMob(self):
		self.selectedMob = 0
		self.isCurrActionDone = True
		self.CURRENT_STATE = WALKING_STATE

	def GoingToDeathPointDone(self):
		self.isCurrActionDone = True
		self.CURRENT_STATE = WAITING_STATE
		OpenLib.LAST_DEATH_POINT = []

	def IsCurrentlyDiggingDone(self):
		self.is_currently_digging = False
		self.isCurrActionDone = True
		if self.selectedOre not in eXLib.InstancesList:
			self.selectedOre = 0

	def IsExchangingItemsToEnergyFragmentsDone(self):
		self.isCurrActionDone = True
		self.CURRENT_STATE = WALKING_STATE

	def IsCurrentlyDigging(self):
		return self.is_currently_digging

	def add_point(self, point_dict):
		self.path.append((point_dict['x'], point_dict['y'], point_dict['map_name']))

	def delete_point(self, point_dict):
		for point in self.path:
			if point[0] == point_dict['x'] and point[1] == point_dict['y'] and point[2] == point_dict['map_name']:
				self.path.remove(point)
				return True
		return False

	def next_point(self):
		Movement.StopMovement()
		if self.current_point + 1 < len(self.path):
			self.current_point += 1
			self.vid_skip_list = []
		else:
			self.vid_skip_list = []
			self.path.reverse()
			self.current_point = 0
			if self.switch_channels:
				self.CURRENT_STATE = SWITCHING_CHANNEL

	def which_state_should_play(self):
		can_pickup = True
		closest_vid = OpenLib.GetNearestVidFromList(eXLib.InstancesList)
		chr.SelectInstance(closest_vid)
		x1, y1, z = chr.GetPixelPosition(net.GetMainActorVID())
		x2, y2, z = chr.GetPixelPosition(closest_vid)
		if OpenLib.dist(x1, y1, x2, y2) < 500 \
				and self.CURRENT_STATE != WALKING_STATE \
				and chr.GetInstanceType(closest_vid) == OpenLib.MONSTER_TYPE:
			can_pickup = False
			if not self.isCurrActionDone and self.CURRENT_STATE == PICKING_ITEM:
				selected_item = [item for item in self.items_to_pickup if item['vid'] == self.selectedItem][0]
				if OpenLib.isPlayerCloseToPosition(selected_item['position'][0], selected_item['position'][1], 500) and self.look_for_mobs:
					self.discard_current_action()
					self.selectedMob = closest_vid
					return MOB_STATE

		if self.CURRENT_STATE == WAITING_STATE:
			return WAITING_STATE

		elif self.CURRENT_STATE == SWITCHING_CHANNEL:
			return SWITCHING_CHANNEL

		if not self.isCurrActionDone:
			return False

		elif OpenLib.isInventoryFull():
			is_any_item_to_sell = OpenLib.DoPlayerHasItems(OpenLib.GetItemsSlotsByID(self.items_to_sell))
			is_any_book_to_sell = OpenLib.DoPlayerHasBooksWithSkillsId(self.skill_books_ids)

			if (not is_any_book_to_sell and not is_any_item_to_sell) or not self.can_go_sell_items:
				#Add a callback about inventory is full and there is nothing to sell
				chat.AppendChat(3, 'Stopping Farmbot, inv is full')
				self.onStop()
				return WAITING_STATE
			chat.AppendChat(3, 'going sell items')
			return GOING_TO_SHOP



		elif self.can_go_buy_potions and (not OpenLib.DoPlayerHasItems(OpenLib.GetItemsSlotsByID(RED_POTIONS_IDS)) or
			not OpenLib.DoPlayerHasItems(OpenLib.GetItemsSlotsByID(BLUE_POTIONS_IDS))):
			chat.AppendChat(3, 'going buy potions')
			return BUY_POTIONS

		elif OpenLib.LAST_DEATH_POINT:
			return GOING_TO_DEATH_POINT

		elif self.move_to_items and self.items_to_pickup and can_pickup:
			items_to_check = [item for item in self.items_to_pickup
							  if (not item['owner'] or item['owner'] == player.GetName()) and item is not None]

			from OpenBot.Modules.Settings.settings_module import instance
			closest_item = None
			if instance.pickItemsFirst:
				items_only = [item for item in items_to_check if item['itemIndex'] != 1]
				if items_only:
					closest_item = OpenLib.getClosestItemFromList(items_only)

			if closest_item is None:
				closest_item = OpenLib.getClosestItemFromList(items_to_check)

			self.selectedItem = closest_item['vid']
			return PICKING_ITEM

		elif self.look_for_metins and self.metins_vid_list and not self.last_walking_is_player_near:
			self.selectedMetin = self.metins_vid_list.pop()
			return FARMING_STATE

		elif self.look_for_bosses and self.boss_vid_list and not self.last_walking_is_player_near:
			self.selectedBoss = self.boss_vid_list.pop()
			return BOSS_STATE

		elif self.look_for_ore and self.ores_vid_list:
			self.selectedOre = self.ores_vid_list.pop()
			return MINING_STATE

		elif self.look_for_mobs and self.mobs_vid_list:
			nearest_vid = OpenLib.GetNearestVidFromList(self.mobs_vid_list)
			self.selectedMob = nearest_vid
			return MOB_STATE

		return WALKING_STATE

	def check_is_selected_item_exist(self):
		if not self.selectedItem:
			return False

		for item in self.items_to_pickup:
			if item['vid'] == self.selectedItem:
				return True

		self.selectedItem = 0
		self.DiscardingAction()
		return False

	def SetIsCurrActionDoneTrue(self):
		self.isCurrActionDone = True
		self.selectedItem = 0
		self.CURRENT_STATE = WALKING_STATE

	def checkForMetinsAndOres(self):
		self.ores_vid_list = []
		self.boss_vid_list = []
		self.metins_vid_list = []
		self.mobs_vid_list = []
		my_x, my_y, my_z = chr.GetPixelPosition(net.GetMainActorVID())
		x1, y1 = self.path[self.current_point][0], self.path[self.current_point][1]
		for vid in eXLib.InstancesList:
			chr.SelectInstance(vid)
			if vid in self.vid_skip_list:
				continue
			if vid == net.GetMainActorVID():
				continue
			x2, y2, z = chr.GetPixelPosition(vid)
			if eXLib.IsPositionBlocked(x2, y2) or not eXLib.FindPath(my_x, my_y, x2, y2):
				continue

			if self.look_for_ore and OpenLib.IsThisOre(vid) and chr.GetRace() in self.ores_to_mine:
					self.ores_vid_list.append(vid)

			elif self.look_for_metins and OpenLib.IsThisMetin(vid) and not eXLib.IsDead(vid):
				if protector_module.is_unknown_player_close:
					self.vid_skip_list.append(vid)
				else:
					self.metins_vid_list.append(vid)

			elif self.look_for_bosses and OpenLib.IsThisBoss(vid) and not eXLib.IsDead(vid):
				if protector_module.is_unknown_player_close:
					self.vid_skip_list.append(vid)
				else:
					self.boss_vid_list.append(vid)

			elif self.look_for_mobs and not eXLib.IsDead(vid) and chr.GetInstanceType(vid) == OpenLib.MONSTER_TYPE:
				mob_race = chr.GetRace()
				if (not self.mobs_to_kill or mob_race in self.mobs_to_kill) and mob_race not in self.mobs_to_avoid:
					if OpenLib.dist(x1, y1, x2, y2) <= self.max_range_to_mob:
						for group_vids in OpenLib.getMobGroup(vid):
							chr.SelectInstance(group_vids)
							if chr.GetRace() in self.mobs_to_avoid:
								continue
						self.mobs_vid_list.append(vid)

	def check_item_list(self):
		items_to_remove = []
		my_x, my_y, my_z = chr.GetPixelPosition(net.GetMainActorVID())
		[items_to_remove.append(item) for item in self.items_to_pickup
		 if OpenLib.dist(my_x, my_y, item['position'][0], item['position'][1]) > 5000]
		[self.items_to_pickup.remove(item) for item in items_to_remove]

	def generate_walking_action(self, is_player_near):
		interrupt_function = None
		interruptors_args = []
		interruptors = []
		if self.look_for_metins:
			interruptors_args.append(self.vid_skip_list)
			interruptors.append(ActionRequirementsCheckers.isMetinNearly)

		if self.look_for_ore:
			interruptors_args.append([self.ores_to_mine, []])
			interruptors.append(ActionRequirementsCheckers.isRaceNearly)

		if self.look_for_bosses:
			interruptors_args.append([OpenLib.BOSS_IDS.keys(), self.vid_skip_list])
			interruptors.append(ActionRequirementsCheckers.isRaceNearly)

		if self.look_for_mobs and self.mobs_vid_list:
			interruptors_args.append([self.mobs_to_kill, []])
			interruptors.append(ActionRequirementsCheckers.isRaceNearly)

		if self.move_to_items:
			interruptors_args.append(self.items_to_pickup)
			interruptors.append(ActionRequirementsCheckers.areItemsNearly)

		if is_player_near:
			interruptors = []
			interruptors_args = []
			interrupt_function = None
		else:
			interrupt_function = lambda: Action.DISCARD


		action_dict = {
			'call_only_once': True,
			'name': '[Farmbot] - working',
			'function_args': [(self.path[self.current_point][0], self.path[self.current_point][1]),
							  self.path[self.current_point][2]],
			'function': ActionFunctions.MoveToPosition,
			'requirements': {ActionRequirementsCheckers.IS_ON_POSITION: [self.path[self.current_point][0],
																		 self.path[self.current_point][1], 300],
							 ActionRequirementsCheckers.IS_IN_MAP: [self.path[self.current_point][2]]},
			'callback': self.IsWalkingDone,
			'callback_on_failed': self.DiscardingAction,
			'interruptors_args': interruptors_args,
			'interruptors': interruptors,
			'interrupt_function': interrupt_function,
			'parent': 'farmbot'}

		return action_dict

	def generate_walk_to_death_point_action(self):
		return  {
			'call_only_once': True,
			'name': 'Retuning to death point',
			'function_args': [OpenLib.LAST_DEATH_POINT[0], OpenLib.LAST_DEATH_POINT[1]],
			'function': ActionFunctions.MoveToPosition,
			'requirements': {ActionRequirementsCheckers.IS_ON_POSITION:
								 [OpenLib.LAST_DEATH_POINT[0][0], OpenLib.LAST_DEATH_POINT[0][1], 300],
							 ActionRequirementsCheckers.IS_IN_MAP: [OpenLib.LAST_DEATH_POINT[1]]},
			'callback': self.GoingToDeathPointDone,
		}

	def generate_channel_switcher_action(self):
		action_dict = {
			'function_args': [channel_switcher_interface.GetNextChannel()],
			'function': ActionFunctions.ChangeChannel,
			'requirements': {ActionRequirementsCheckers.IS_IN_CHANNEL: [channel_switcher_interface.GetNextChannel()]},
			'callback': self.SetIsCurrActionDoneTrue,
			'parent': 'farmbot'
		}
		return action_dict

	def generate_mining_action(self):
		return {
			'function_args': [self.selectedOre, self.IsCurrentlyDigging],
			'requirements': {},
			'function': ActionFunctions.MineOre,
			'on_success': [Action.NEXT_ACTION],
			'on_failed': [Action.NEXT_ACTION],
			'parent': 'farmbot'
		}

	def generate_go_to_shop_action(self):

		slots_to_sell = []
		for slot in range(OpenLib.MAX_INVENTORY_SIZE):
			item_id = player.GetItemIndex(slot)
			if not item_id:
				continue

			if item_id in [50300, 70037, 70055, 70104, 71093]:
				skill = player.GetItemMetinSocket(player.INVENTORY, slot, 0)
				if skill in self.skill_books_ids:
					slots_to_sell.append(slot)
			elif item_id in self.items_to_sell:
				slots_to_sell.append(slot)

		return {
			'name': '[Farmbot] - Selling items',
			'function_args': [slots_to_sell, 9003, [0], self.IsExchangingItemsToEnergyFragmentsDone],
			'function': ActionFunctions.GoSellItemsToNPC,
			'parent': 'farmbot'

		}

	def generate_buy_potions_actions(self):
		items_slot_to_buy = [7, 7, 13]
		action = {
			'name': '[Farmbot] - going to buy potions',
			'function_args': [items_slot_to_buy, 9003, [0], self.IsExchangingItemsToEnergyFragmentsDone],
			'function': ActionFunctions.GoBuyItemsFromNPC,
		}
		return action

	def generate_walk_to_item_action(self):
		item_to_pick = None
		for item in self.items_to_pickup:
			if item['vid'] == self.selectedItem:
				item_to_pick = item
				break

		if item_to_pick is None:
			return False
		my_x, my_y, my_z = chr.GetPixelPosition(net.GetMainActorVID())

		if 220 >= OpenLib.dist(my_x, my_y, item_to_pick['position'][0], item_to_pick['position'][1]):
			return True

		return 	{
			'call_only_once': True,
			'name': 'Walk to item',
			'function_args': [(item_to_pick['position'][0], item_to_pick['position'][1]),
							  background.GetCurrentMapName()],
			'function': ActionFunctions.MoveToPosition,
			'requirements': {ActionRequirementsCheckers.IS_ON_POSITION: [item_to_pick['position'][0],
																		 item_to_pick['position'][1], 150]},
			'callback_on_failed': self.DiscardingAction,
			'parent': 'farmbot'}

	def discard_current_action(self):
		from OpenBot.Modules.Actions.ActionBot import instance
		instance.DiscardActionByParent('farmbot')
		self.selectedOre = 0
		self.selectedMetin = 0
		self.selectedBoss = 0
		self.selectedMob = 0
		self.selectedItem = 0
		self.isCurrActionDone = True
		self.is_currently_digging = False
		if self.CURRENT_STATE == FARMING_STATE:
			self.CURRENT_STATE = SWITCHING_CHANNEL
		else:
			self.CURRENT_STATE = self.which_state_should_play()
		player.SetAttackKeyState(False)

	def OnUpdate(self):
		val, self.lastTime = OpenLib.timeSleep(self.lastTime, 0.1)
		if not OpenLib.IsInGamePhase() or not val or self.enabled != ENABLE_STATES['ENABLED']:
			return

		new_path = self.pop_path()
		if new_path != self.current_level_path_key:
			self.current_level_path_key = new_path
			self.set_path(new_path)
			return

		self.check_is_selected_item_exist()

		self.CURRENT_STATE = self.which_state_should_play()

		if protector_module.is_unknown_player_close:
			if self.CURRENT_STATE == FARMING_STATE or self.CURRENT_STATE == BOSS_STATE:
				chat.AppendChat(3, 'there is a player')
				if not self.isCurrActionDone:
					self.discard_current_action()

			elif self.CURRENT_STATE == WALKING_STATE and not self.last_walking_is_player_near:
				if not self.isCurrActionDone:
					self.discard_current_action()
					self.isCurrActionDone = True
		else:
			if self.CURRENT_STATE == WALKING_STATE and self.last_walking_is_player_near:
				if not self.isCurrActionDone:
					self.discard_current_action()
					self.isCurrActionDone = True

		self.check_item_list()

		if not self.isCurrActionDone:
			return

		self.checkForMetinsAndOres()

		if self.CURRENT_STATE == WAITING_STATE:
			val, self.lastTimeWaitingState = OpenLib.timeSleep(self.lastTimeWaitingState, self.timeForWaitingState)
			if val:
				self.lastTimeWaitingState = 0
				self.CURRENT_STATE = WALKING_STATE

		elif self.CURRENT_STATE == WALKING_STATE:
			self.last_walking_is_player_near = protector_module.is_unknown_player_close
			action_bot_interface.AddActionAsLast(self.generate_walking_action(protector_module.is_unknown_player_close))
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == SWITCHING_CHANNEL:
			self.isCurrActionDone = False
			action_bot_interface.AddActionAsLast(self.generate_channel_switcher_action())
			return

		elif self.CURRENT_STATE == MINING_STATE:
			action_bot_interface.AddActionAsLast(self.generate_mining_action())
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == FARMING_STATE:
			from OpenBot.Modules.Attacker.attacker_module import attacker_module
			attacker_module.select_mob_to_kill(self.selectedMetin, self.IsDestroyingMetinDone, lock_vid=True)
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == EXCHANGING_ITEMS_TO_ENERGY:
			OpenLog.DebugPrint('[Farming-bot] EXCHANGING_STATE')
			action_dict = {'function_args': [],
							'function': ActionFunctions.ExchangeTrashItemsToEnergyFragments,
							'on_success': [Action.NEXT_ACTION],
							'callback': self.IsExchangingItemsToEnergyFragmentsDone}
			action_bot_interface.AddActionAsLast(action_dict)
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == BUY_POTIONS:
			action_bot_interface.AddActionAsLast(self.generate_buy_potions_actions())
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == GOING_TO_SHOP:
			action_bot_interface.AddActionAsLast(self.generate_go_to_shop_action())
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == BOSS_STATE:
			from OpenBot.Modules.Attacker.attacker_module import attacker_module
			attacker_module.select_mob_to_kill(self.selectedBoss, self.IsDestroyingMetinDone, lock_vid=True)
			self.isCurrActionDone = False
			return
		
		elif self.CURRENT_STATE == GOING_TO_DEATH_POINT:
			action_bot_interface.AddActionAsLast(self.generate_walk_to_death_point_action())
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == MOB_STATE:
			from OpenBot.Modules.Attacker.attacker_module import attacker_module
			attacker_module.select_mob_to_kill(self.selectedMob, self.KilledMob)
			if attacker_module.add_whole_group_to_kill:
				[attacker_module.additional_vid_targets_to_kill.append(mob) for mob in OpenLib.getMobGroup(self.selectedMob)]
			self.isCurrActionDone = False
			return

		elif self.CURRENT_STATE == PICKING_ITEM:
			player.SetAttackKeyState(False)

			action = self.generate_walk_to_item_action()
			if not action:
				return
			elif isinstance(action, dict):
				action_bot_interface.AddActionAsLast(action)
			self.isCurrActionDone = False

		elif self.CURRENT_STATE == WAITING_UNTIL_HP_IS_NOT_REGENERATED:
			self.CURRENT_STATE = WAITING_STATE

	def newItemAppears(self, vid, itemIndex, x, y, owner):
		from OpenBot.Modules.Settings.settings_module import instance
		if not self.move_to_items:
			return

		item_in_filter = itemIndex in instance.pickFilter

		if instance.excludeInFilter:
			if item_in_filter:
				return
		else:
			if not item_in_filter:
				return

		if eXLib.IsPositionBlocked(x, y):
			return

		self.items_to_pickup.append({'vid': vid, 'position': [x, y], 'itemIndex': itemIndex, 'owner': owner})

	def itemOwnerChange(self, vid, owner):
		for item in self.items_to_pickup:
			if item['vid'] == vid:
				item['owner'] = owner
				return

	def itemDissapear(self, vid):
		if vid == self.selectedItem:
			self.SetIsCurrActionDoneTrue()

		for item in self.items_to_pickup:
			if item['vid'] == vid:
				self.items_to_pickup.remove(item)
				return


farm = FarmingBot()
farm.Show()
eXLib.SetRecvAddGrndItemCallback(farm.newItemAppears)
eXLib.SetRecvChangeOwnershipGrndItemCallback(farm.itemOwnerChange)
eXLib.SetRecvDelGrndItemCallback(farm.itemDissapear)

Hooks.registerPhaseCallback('pauseFarmbot', OnLoginPhase)