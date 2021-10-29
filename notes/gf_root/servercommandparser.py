import m2netm2g
import background
import stringCommander
import constInfo
import app
class ServerCommandParser(object):

	def __init__(self):
		m2netm2g.SetServerCommandParserWindow(self)
		self.__ServerCommand_Build()

	def __ServerCommand_Build(self):
		serverCommandList={
			"DayMode"				: self.__DayMode_Update, 
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"item_mall"				: self.__ItemMall_Open,
			
		}

		if app.ENABLE_NEW_HALLOWEEN_EVENT:
			serverCommandList["halloween_box"] = self.__Halloween_box_event
			
		serverCommandList["mini_game_okey"] = self.__MiniGameOkeyEvent
			
		if app.ENABLE_2016_VALENTINE:
			serverCommandList["valentine_drop"] = self.__ValentineEvent
			
		if app.ENABLE_MONSTER_BACK:
			if app.ENABLE_10TH_EVENT:
				serverCommandList["e_monsterback"] = self.__MonsterBack
			else:
				serverCommandList["e_easter_monsterback"] = self.__EasterMonsterBack
			
		if app.ENABLE_CARNIVAL2016:
			serverCommandList["carnival_event"] = self.__CarnivalEvent
			
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			serverCommandList["mini_game_okey_normal"] = self.__MiniGameOkeyNormalEvent
			
		if app.ENABLE_AUTO_SYSTEM:
			serverCommandList["auto_loginoff"] = self.__AutoOff	

		if app.ENABLE_SUMMER_EVENT:
			serverCommandList["e_summer_event"] = self.__SummerEvent
			
		if app.ENABLE_BATTLE_FIELD:	
			serverCommandList["battle_field"] = self.__BattleFieldInfo
			serverCommandList["battle_field_open"] = self.__BattleFieldOpen
			serverCommandList["battle_field_event"] = self.__BattleFieldEventInfo
			serverCommandList["battle_field_event_open"] = self.__BattleFieldEventOpen
			
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			serverCommandList["guild_war"] = self.Guild_War_Check
			serverCommandList["clear_guildranking"] = self.PassGuildCommand
			serverCommandList["clear_applicant"] = self.PassGuildCommand
			serverCommandList["clear_applicantguild"] = self.PassGuildCommand

		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			serverCommandList["clear_guild_reddragonlair_ranking"] = self.PassGuildDragonCommand
			serverCommandList["check_reddragonlairranking_board"] = self.PassGuildDragonCommand
			
		if app.ENABLE_FISH_EVENT:
			serverCommandList["fish_event"] = self.__FishEvent	
			
		if app.ENABLE_2017_RAMADAN:
			serverCommandList["e_2017_ramadan_event"] = self.__2017RamaDanEvent					
			
		if app.ENABLE_PARTY_MATCH:
			serverCommandList["party_match_off"] = self.__PartyMatchOff
			
		if app.ENABLE_MINI_GAME_YUTNORI:
			serverCommandList["mini_game_yutnori"] = self.__MiniGameYutnori
			
		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)
			
	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def Guild_War_Check(self, enable):
			self.__PreserveCommand("guild_war " + enable)

		def PassGuildCommand(self):
			pass


	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def PassGuildDragonCommand(self):
			pass
	
	if app.ENABLE_NEW_HALLOWEEN_EVENT:
		def __Halloween_box_event(self, enable):
			self.__PreserveCommand("halloween_box " + enable)
			
	def __MiniGameOkeyEvent(self, enable):
		self.__PreserveCommand("mini_game_okey " + enable)
			
	if app.ENABLE_2016_VALENTINE:
		def __ValentineEvent(self, enable):
			self.__PreserveCommand("valentine_drop " + enable)
			
	if app.ENABLE_MONSTER_BACK:
		if app.ENABLE_10TH_EVENT:
			def __MonsterBack(self, enable):
				self.__PreserveCommand("e_monsterback " + enable)
		else:
			def __EasterMonsterBack(self, enable):
				self.__PreserveCommand("e_easter_monsterback " + enable)
			
	if app.ENABLE_CARNIVAL2016:
		def __CarnivalEvent(self, enable):
			self.__PreserveCommand("carnival_event " + enable)
			
	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			def __MiniGameOkeyNormalEvent(self, enable):
				self.__PreserveCommand("mini_game_okey_normal " + enable)
	
	if app.ENABLE_AUTO_SYSTEM:
		def __AutoOff(self, enable):
			self.__PreserveCommand("auto_loginoff")
			
	if app.ENABLE_SUMMER_EVENT:
		def __SummerEvent(self, enable):
			self.__PreserveCommand("e_summer_event " + enable)

	if app.ENABLE_BATTLE_FIELD:
		def __BattleFieldInfo(self, enable):
			self.__PreserveCommand("battle_field %s" % (enable))
			
		def __BattleFieldOpen(self, open):
			self.__PreserveCommand("battle_field_open %s" % (open))
			
		def __BattleFieldEventInfo(self, enable, start, end):
			self.__PreserveCommand("battle_field_event %s %s %s" % (enable, start, end))
		
		def __BattleFieldEventOpen(self, open):
			self.__PreserveCommand("battle_field_event_open %s" % (open))
	
	if app.ENABLE_FISH_EVENT:
		def __FishEvent(self, enable):
			self.__PreserveCommand("fish_event " + enable)
			
	if app.ENABLE_2017_RAMADAN:
		def __2017RamaDanEvent(self, enable):
			self.__PreserveCommand("e_2017_ramadan_event " + enable)
			
	if app.ENABLE_PARTY_MATCH:
		def __PartyMatchOff(self, enable):
			self.__PreserveCommand("party_match_off " + enable)
		
	if app.ENABLE_MINI_GAME_YUTNORI:
		def __MiniGameYutnori(self, enable):
			self.__PreserveCommand("mini_game_yutnori " + enable)
						
	def BINARY_ServerCommand_Run(self, line):
		try:
			print " BINARY_ServerCommand_Reserve", line
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			import dbg
			dbg.TraceError(msg)
			return 0

	def __PreserveCommand(self, line):
		m2netm2g.PreserveServerCommand(line)	

	def __DayMode_Update(self, mode):
		self.__PreserveCommand("PRESERVE_DayMode " + mode)

	def __ItemMall_Open(self):
		self.__PreserveCommand("item_mall")

	## юс╫ц
	def __XMasBoom_Enable(self, mode):
		if "1"==mode:
			self.__PreserveCommand("PRESERVE_DayMode dark")
		else:
			self.__PreserveCommand("PRESERVE_DayMode light")
	def __XMasSnow_Enable(self, mode):
		self.__PreserveCommand("xmas_snow " + mode)
	def __XMasTree_Enable(self, grade):
		self.__PreserveCommand("xmas_tree " + grade)
		

parserWnd = ServerCommandParser()
