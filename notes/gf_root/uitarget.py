import app
import ui
import playerm2g2
import m2netm2g
import wndMgr
import messenger
import guild
import chr
import nonplayer
import localeInfo
import constInfo

if app.ENABLE_12ZI:
	import chrmgrm2g
	import background

if app.ENABLE_MESSENGER_BLOCK:
	import uiCommon

class TargetBoard(ui.ThinBoard):

	if app.ENABLE_MESSENGER_BLOCK:
			BUTTON_NAME_LIST = [ 
			localeInfo.TARGET_BUTTON_WHISPER, 
			localeInfo.TARGET_BUTTON_EXCHANGE, 
			localeInfo.TARGET_BUTTON_FIGHT, 
			localeInfo.TARGET_BUTTON_ACCEPT_FIGHT, 
			localeInfo.TARGET_BUTTON_AVENGE, 
			localeInfo.TARGET_BUTTON_FRIEND, 
			localeInfo.TARGET_BUTTON_INVITE_PARTY, 
			localeInfo.TARGET_BUTTON_LEAVE_PARTY, 
			localeInfo.TARGET_BUTTON_EXCLUDE, 
			localeInfo.TARGET_BUTTON_INVITE_GUILD,
			localeInfo.TARGET_BUTTON_DISMOUNT,
			localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
			localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
			localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
			localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
			localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
			localeInfo.TARGET_BUTTON_BLOCK,
			localeInfo.TARGET_BUTTON_BLOCK_REMOVE,
			"VOTE_BLOCK_CHAT",
		]
	else:
		BUTTON_NAME_LIST = [ 
			localeInfo.TARGET_BUTTON_WHISPER, 
			localeInfo.TARGET_BUTTON_EXCHANGE, 
			localeInfo.TARGET_BUTTON_FIGHT, 
			localeInfo.TARGET_BUTTON_ACCEPT_FIGHT, 
			localeInfo.TARGET_BUTTON_AVENGE, 
			localeInfo.TARGET_BUTTON_FRIEND, 
			localeInfo.TARGET_BUTTON_INVITE_PARTY, 
			localeInfo.TARGET_BUTTON_LEAVE_PARTY, 
			localeInfo.TARGET_BUTTON_EXCLUDE, 
			localeInfo.TARGET_BUTTON_INVITE_GUILD,
			localeInfo.TARGET_BUTTON_DISMOUNT,
			localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
			localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
			localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
			localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
			localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
			"VOTE_BLOCK_CHAT",
		]
		
	if app.ENABLE_12ZI:
		BUTTON_NAME_LIST.append(localeInfo.TARGET_BUTTON_REVIVE)

	GRADE_NAME =	{
						nonplayer.PAWN : localeInfo.TARGET_LEVEL_PAWN,
						nonplayer.S_PAWN : localeInfo.TARGET_LEVEL_S_PAWN,
						nonplayer.KNIGHT : localeInfo.TARGET_LEVEL_KNIGHT,
						nonplayer.S_KNIGHT : localeInfo.TARGET_LEVEL_S_KNIGHT,
						nonplayer.BOSS : localeInfo.TARGET_LEVEL_BOSS,
						nonplayer.KING : localeInfo.TARGET_LEVEL_KING,
					}
	EXCHANGE_LIMIT_RANGE = 3000
	
	if app.ENABLE_ELEMENT_ADD:
		ELEMENT_IMG_PATH = \
		{
			nonplayer.RACE_FLAG_ATT_ELEC	: "d:/ymir work/ui/game/12zi/element/elect.sub",
			nonplayer.RACE_FLAG_ATT_FIRE	: "d:/ymir work/ui/game/12zi/element/fire.sub",	
			nonplayer.RACE_FLAG_ATT_ICE		: "d:/ymir work/ui/game/12zi/element/ice.sub",
			nonplayer.RACE_FLAG_ATT_WIND	: "d:/ymir work/ui/game/12zi/element/wind.sub",
			nonplayer.RACE_FLAG_ATT_EARTH	: "d:/ymir work/ui/game/12zi/element/earth.sub",
			nonplayer.RACE_FLAG_ATT_DARK	: "d:/ymir work/ui/game/12zi/element/dark.sub",
		}

	def __init__(self):
		ui.ThinBoard.__init__(self)
		
		if app.ENABLE_MESSENGER_BLOCK:
			self.AddFlag("float")

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetOutline()
		name.Show()
		
		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			damage_display = ui.TextLine()
			damage_display.SetParent( name )
			damage_display.SetDefaultFontName()
			damage_display.SetOutline()
			damage_display.Show()
			self.damage_display = damage_display
			
		hpGauge = ui.Gauge()
		hpGauge.SetParent(self)
		hpGauge.MakeGauge(130, "red")
		hpGauge.Hide()

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		closeButton.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		closeButton.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		closeButton.SetPosition(30, 13)

		if localeInfo.IsARABIC():
			hpGauge.SetPosition(55, 17)
			hpGauge.SetWindowHorizontalAlignLeft()
			closeButton.SetWindowHorizontalAlignLeft()
		else:
			hpGauge.SetPosition(175, 17)
			hpGauge.SetWindowHorizontalAlignRight()
			closeButton.SetWindowHorizontalAlignRight()

		closeButton.SetEvent(ui.__mem_func__(self.OnPressedCloseButton))
		closeButton.Show()

		if app.ENABLE_ELEMENT_ADD:
			self.elementImgDict = {}
			for element, path in self.ELEMENT_IMG_PATH.items():
				elementImg = ui.ExpandedImageBox()
				elementImg.SetParent(self)
				elementImg.LoadImage( path )
				elementImg.SetPosition(0, 0)
				if localeInfo.IsARABIC():
					elementImg.SetWindowHorizontalAlignRight()
				else:
					elementImg.SetPosition(-40, 0)
					elementImg.SetWindowHorizontalAlignLeft()
				elementImg.Hide()
				self.elementImgDict[element] = elementImg
				
		self.buttonDict = {}
		self.showingButtonList = []
		for buttonName in self.BUTTON_NAME_LIST:
			button = ui.Button()
			button.SetParent(self)
		
			if localeInfo.IsARABIC():
				button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
			else:
				button.SetUpVisual("d:/ymir work/ui/public/small_thin_button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/small_thin_button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/small_thin_button_03.sub")
			
			button.SetWindowHorizontalAlignCenter()
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER].SetEvent(ui.__mem_func__(self.OnWhisper))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE].SetEvent(ui.__mem_func__(self.OnExchange))
		self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_AVENGE].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyInvite))
		self.buttonDict[localeInfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyExit))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCLUDE].SetEvent(ui.__mem_func__(self.OnPartyRemove))

		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_GUILD].SAFE_SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeInfo.TARGET_BUTTON_DISMOUNT].SAFE_SetEvent(self.__OnDismount)
		self.buttonDict[localeInfo.TARGET_BUTTON_EXIT_OBSERVER].SAFE_SetEvent(self.__OnExitObserver)
		self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT].SAFE_SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SAFE_SetEvent(self.__OnRequestParty)
		self.buttonDict[localeInfo.TARGET_BUTTON_BUILDING_DESTROY].SAFE_SetEvent(self.__OnDestroyBuilding)
		self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW].SAFE_SetEvent(self.__OnEmotionAllow)
		if app.ENABLE_12ZI:
			self.buttonDict[localeInfo.TARGET_BUTTON_REVIVE].SAFE_SetEvent(self.__OnReviveQustionDialog)
		
		if app.ENABLE_MESSENGER_BLOCK:
			self.buttonDict[localeInfo.TARGET_BUTTON_BLOCK].SAFE_SetEvent(self.__OnBlock)
			self.buttonDict[localeInfo.TARGET_BUTTON_BLOCK_REMOVE].SAFE_SetEvent(self.__OnBlockRemove)
		
		self.buttonDict["VOTE_BLOCK_CHAT"].SetEvent(ui.__mem_func__(self.__OnVoteBlockChat))

		self.name = name
		self.hpGauge = hpGauge
		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		self.eventWhisper = None
		self.isShowButton = False
		if app.ENABLE_12ZI:
			self.questionDialog = None

		self.__Initialize()
		self.ResetTargetBoard()

	def __del__(self):
		ui.ThinBoard.__del__(self)

		print "===================================================== DESTROYED TARGET BOARD"

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		self.isShowButton = False

	def Destroy(self):
		self.eventWhisper = None
		self.closeButton = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		self.hpGauge = None

		if app.ENABLE_ELEMENT_ADD:
			self.elementImgDict = None
		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			self.damage_display = None

		self.__Initialize()

	def OnPressedCloseButton(self):
		playerm2g2.ClearTarget()
		self.Close()

	def Close(self):
		self.__Initialize()
		self.Hide()

	def Open(self, vid, name):
		if app.ENABLE_ELEMENT_ADD:
			self.__HideAllElementImg()
		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			self.damage_display.Hide()
			
		if vid:
			if not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not playerm2g2.IsSameEmpire(vid):
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)
			
			if app.ENABLE_ELEMENT_ADD and app.ENABLE_PENDANT:
				element = playerm2g2.GetElementByVID(vid)
				if element:
					self.__ShowElementImg(element)
					
			if playerm2g2.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()		
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			self.__ShowButton(localeInfo.TARGET_BUTTON_WHISPER)
			self.__ShowButton("VOTE_BLOCK_CHAT")
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()
			
	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():			
				self.RefreshButton()		

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():			
			self.Refresh()
			
	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __ShowMainCharacterMenu(self):
		canShow=0

		self.HideAllButton()

		if playerm2g2.IsMountingHorse():
			self.__ShowButton(localeInfo.TARGET_BUTTON_DISMOUNT)
			canShow=1

		if playerm2g2.IsObserverMode():
			self.__ShowButton(localeInfo.TARGET_BUTTON_EXIT_OBSERVER)
			canShow=1

		if canShow:
			self.__ArrangeButtonPosition()
			self.Show()
		else:
			self.Hide()
			
	def __ShowNameOnlyMenu(self):
		self.HideAllButton()

	def SetWhisperEvent(self, event):
		self.eventWhisper = event

	def UpdatePosition(self):
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, 10)

	def ResetTargetBoard(self):

		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()

		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()
		
		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			self.damage_display.SetPosition(0, 30)
			self.damage_display.SetHorizontalAlignLeft()
			self.damage_display.SetWindowHorizontalAlignCenter()

		self.hpGauge.Hide()
		self.SetSize(250, 40)

	def SetTargetVID(self, vid):
		self.vid = vid

	def SetEnemyVID(self, vid):
		self.SetTargetVID(vid)

		name = chr.GetNameByVID(vid)
		level = nonplayer.GetLevelByVID(vid)
		grade = nonplayer.GetGradeByVID(vid)

		nameFront = ""
		if -1 != level:
			nameFront += "Lv." + str(level) + " "
		if self.GRADE_NAME.has_key(grade):
			nameFront += "(" + self.GRADE_NAME[grade] + ") "

		self.SetTargetName(nameFront + name)

		if app.ENABLE_ELEMENT_ADD:
			self.__HideAllElementImg()
			element = nonplayer.GetAttElementFlagByVID(vid)
			if element:
				self.__ShowElementImg(element)
				
		if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
			accumulate_count = playerm2g2.GetAccumulateDamageByVID(vid)
			if accumulate_count:
				self.damage_display.SetText( localeInfo.TARGET_TOOLTIP_ATTACK_COUNT % accumulate_count )
				self.damage_display.Show()
			else:
				self.damage_display.Hide()
			

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)
		self.name.SetText(name)

	def SetHP(self, hpPercentage):
		if not self.hpGauge.IsShow():

			self.SetSize(200 + 7*self.nameLength, self.GetHeight())

			if localeInfo.IsARABIC():
				self.name.SetPosition( self.GetWidth()-23, 13)
			else:
				self.name.SetPosition(23, 13)

			self.name.SetWindowHorizontalAlignLeft()
			self.name.SetHorizontalAlignLeft()
			self.hpGauge.Show()
			self.UpdatePosition()

		self.hpGauge.SetPercentage(hpPercentage, 100)

	def ShowDefaultButton(self):

		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW])
		for button in self.showingButtonList:
			button.Show()

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []

	def __ShowButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		m2netm2g.SendExchangeStartPacket(self.vid)

	def OnPVP(self):
		m2netm2g.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		m2netm2g.SendMessengerAddByVIDPacket(self.vid)

	def OnPartyInvite(self):
		m2netm2g.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		m2netm2g.SendPartyExitPacket()

	def OnPartyRemove(self):
		pid = playerm2g2.PartyMemberVIDToPID(self.vid)
		if pid:
			m2netm2g.SendPartyRemovePacket(pid)

	def __OnGuildAddMember(self):
		m2netm2g.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		m2netm2g.SendChatPacket("/unmount")

	def __OnExitObserver(self):
		m2netm2g.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		m2netm2g.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		m2netm2g.SendChatPacket("/party_request " + str(self.vid))

	def __OnDestroyBuilding(self):
		m2netm2g.SendChatPacket("/build d %d" % (self.vid))

	def __OnEmotionAllow(self):
		m2netm2g.SendChatPacket("/emotion_allow %d" % (self.vid))
		
	def __OnVoteBlockChat(self):
		cmd = "/vote_block_chat %s" % (self.nameString)
		m2netm2g.SendChatPacket(cmd)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):

		self.HideAllButton()
		
		if app.ENABLE_12ZI:
			if chrmgrm2g.IsDead(self.vid):
				if background.IsReviveTargetMap():
					self.__ShowButton(localeInfo.TARGET_BUTTON_REVIVE)
					self.__ArrangeButtonPosition()
				return

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			#self.__ShowButton(localeInfo.TARGET_BUTTON_BUILDING_DESTROY)
			#self.__ArrangeButtonPosition()
			return
		
		if playerm2g2.IsPVPInstance(self.vid) or playerm2g2.IsObserverMode():
			# PVP_INFO_SIZE_BUG_FIX
			self.SetSize(200 + 7*self.nameLength, 40)
			self.UpdatePosition()
			# END_OF_PVP_INFO_SIZE_BUG_FIX			
			return	

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_GUILD)

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeInfo.TARGET_BUTTON_FRIEND)
			
		if app.ENABLE_MESSENGER_BLOCK:
			if not messenger.IsBlockFriendByName(self.nameString):
				self.__ShowButton(localeInfo.TARGET_BUTTON_BLOCK)
			else:
				self.__ShowButton(localeInfo.TARGET_BUTTON_BLOCK_REMOVE)
			
		if playerm2g2.IsPartyMember(self.vid):

			self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if playerm2g2.IsPartyLeader(self.vid):
				self.__ShowButton(localeInfo.TARGET_BUTTON_LEAVE_PARTY)
			elif playerm2g2.IsPartyLeader(playerm2g2.GetMainCharacterIndex()):
				self.__ShowButton(localeInfo.TARGET_BUTTON_EXCLUDE)

		else:
			if playerm2g2.IsPartyMember(playerm2g2.GetMainCharacterIndex()):
				if playerm2g2.IsPartyLeader(playerm2g2.GetMainCharacterIndex()):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)

			if playerm2g2.IsRevengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_AVENGE)
			elif playerm2g2.IsChallengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif playerm2g2.IsCantFightInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if not playerm2g2.IsSameEmpire(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

		distance = playerm2g2.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeInfo.TARGET_BUTTON_EXCHANGE)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self):
		showingButtonCount = len(self.showingButtonList)

		pos = -(showingButtonCount / 2) * 68
		if 0 == showingButtonCount % 2:
			pos += 34

		for button in self.showingButtonList:
			button.SetPosition(pos, 33)
			pos += 68

		self.SetSize(max(150, showingButtonCount * 75), 65)
		self.UpdatePosition()

	def OnUpdate(self):
		if self.isShowButton:

			exchangeButton = self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE]
			distance = playerm2g2.GetCharacterDistance(self.vid)

			if distance < 0:
				if app.WJ_NEW_USER_CARE:
					playerm2g2.ClearTarget()
					self.Close()
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()
	
	if app.ENABLE_MESSENGER_BLOCK:
		def __OnBlock(self):
			m2netm2g.SendMessengerBlockAddByVIDPacket(self.vid)
			
		def __OnBlockRemove(self):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.MESSENGER_DO_YOU_DELETE)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnBlockRemove))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnBlockRemoveClose))
			self.questionDialog.Open()
				
		def OnBlockRemove(self):
			m2netm2g.SendMessengerBlockRemoveByVIDPacket(self.vid)
			self.OnBlockRemoveClose()
			
		def OnBlockRemoveClose(self):
			self.questionDialog.Close()
			self.questionDialog = None
			return True
			
	
	if app.ENABLE_ELEMENT_ADD:
		def __HideAllElementImg(self):
			
			for elementImg in self.elementImgDict.values():
				elementImg.Hide()
				
		def __ShowElementImg(self, key):
			if not key in self.elementImgDict:
				return False
				
			self.elementImgDict[key].Show()
			return True
			
			
	if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
		def RefreshAccumulateCount(self, vid):
			accumulate_count = playerm2g2.GetAccumulateDamageByVID(vid)
			if accumulate_count:
				self.damage_display.SetText( localeInfo.TARGET_TOOLTIP_ATTACK_COUNT % accumulate_count )
				self.damage_display.Show()
			else:
				self.damage_display.Hide()
			
	if app.ENABLE_12ZI:
		def __OnReviveQustionDialog(self):
			m2netm2g.SendChatPacket("/revivedialog %d" % (self.vid))
			
		def OpenReviveDialog(self, vid, itemcount):				
			self.questionDialog = uiCommon.QuestionDialog()
			if playerm2g2.IsMainCharacterIndex(vid):
				self.questionDialog.SetText(localeInfo.REVIVE_SELF_QUESTION % (itemcount))
			else:
				self.questionDialog.SetText(localeInfo.REVIVE_QUESTION % (chr.GetNameByVID(vid), itemcount))
				
			self.questionDialog.SetAcceptEvent(lambda arg=vid: self.OnRivive(arg))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnQuestionDialogClose))
			self.questionDialog.Open()
			
		def OnRivive(self, virId):
			m2netm2g.SendChatPacket("/revive %d" % (virId))
			self.OnQuestionDialogClose()
			
		def OnQuestionDialogClose(self):
			self.questionDialog.Close()
			self.questionDialog = None
			return True