import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgrm2g
import playerm2g2
import snd
import chatm2g
import textTail
import snd
import m2netm2g
import effect
import wndMgr
#import fly
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime

import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget

# PRIVATE_SHOP_PRICE_LIST
import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import consoleModule
import localeInfo

import playerSettingModule
import interfaceModule

import musicInfo
import debugInfo
import stringCommander

if app.ENABLE_GUILDRENEWAL_SYSTEM:
	import uiGuildPopup
	import uiGuildBank
	
if app.ENABLE_KEYCHANGE_SYSTEM:
	import uiKeyChange	
	
if app.ENABLE_EXP_EVENT:
	import uiScriptLocale

from _weakref import proxy

# TEXTTAIL_LIVINGTIME_CONTROL
#if localeInfo.IsJAPAN():
#	app.SetTextTailLivingTime(8.0)
# END_OF_TEXTTAIL_LIVINGTIME_CONTROL

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = False
SCREENSHOT_DIR = None

if localeInfo.IsEUROPE():
	SCREENSHOT_CWDSAVE = True

if localeInfo.IsCIBN10():
	SCREENSHOT_CWDSAVE = False
	SCREENSHOT_DIR = "YT2W"

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0

if app.ENABLE_REFINE_MSG_ADD:
	REFINE_FAIL_GRADE_DOWN	= 0
	REFINE_FAIL_DEL_ITEM	= 1
	REFINE_FAIL_KEEP_GRADE	= 2
	REFINE_FAIL_MAX			= 3
	

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		m2netm2g.SetPhaseWindow(m2netm2g.PHASE_WINDOW_GAME, self)
		playerm2g2.SetGameWindow(self)

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None
		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = None

		self.stream=stream
		self.interface = interfaceModule.Interface()
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard()
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()
		self.interface.SettargetBoard(self.targetBoard)

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()
		self.interface.SetAffectShower(self.affectShower)

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()
		
		#wj 2014.1.2. ESC키를 누를 시 우선적으로 DropQuestionDialog를 끄도록 만들었다. 하지만 처음에 itemDropQuestionDialog가 선언되어 있지 않아 ERROR가 발생하여 init에서 선언과 동시에 초기화 시킴.
		self.itemDropQuestionDialog = None

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()
		
		if app.ENABLE_KEYCHANGE_SYSTEM:
			self.wndKeyChange = uiKeyChange.KeyChangeWindow(self, self.interface)
			self.ADDKEYBUFFERCONTROL = playerm2g2.KEY_ADDKEYBUFFERCONTROL
			self.ADDKEYBUFFERALT         = playerm2g2.KEY_ADDKEYBUFFERALT
			self.ADDKEYBUFFERSHIFT       = playerm2g2.KEY_ADDKEYBUFFERSHIFT
		
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None	

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.interface.PetInfoBindAffectShower(self.affectShower)
			
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.guildVoteCheckDialog = None
			self.guildVoteResultDialog = None
			self.guildVoteQuetionDialog = None
			
		if app.ENABLE_EXP_EVENT:
			self.toolTip = ui.TextLine()
			expEventIconPosX = 10
			expEventIconPosY = 35
			self.toolTip.SetPosition(expEventIconPosX, expEventIconPosY+25)
			self.expEventBonusImageList = []
			self.expEventBonusImageList.append(ui.MakeImageBox(self, uiScriptLocale.WINDOWS_PATH + "exp_bonus.tga", expEventIconPosX, expEventIconPosY))
			self.expEventBonusImageList.append(ui.MakeImageBox(self, uiScriptLocale.WINDOWS_PATH + "exp_bonus_hot_time.tga", expEventIconPosX, expEventIconPosY))
			
			for img in self.expEventBonusImageList:
				img.SAFE_SetStringEvent("MOUSE_OVER_IN", self.__expEventImageOverIn)
				img.SAFE_SetStringEvent("MOUSE_OVER_OUT", self.__expEventImageOverOut)
				img.Hide()			
			
	def __del__(self):
		playerm2g2.SetGameWindow(0)
		m2netm2g.ClearPhaseWindow(m2netm2g.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = False
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

		constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()
		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		#if constInfo.PVPMODE_TEST_ENABLE:
			#self.testPKMode = ui.TextLine()
			#self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			#self.testPKMode.SetPosition(0, 15)
			#self.testPKMode.SetWindowHorizontalAlignCenter()
			#self.testPKMode.SetHorizontalAlignCenter()
			#self.testPKMode.SetFeather()
			#self.testPKMode.SetOutline()
			#self.testPKMode.Show()

			#self.testAlignment = ui.TextLine()
			#self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			#self.testAlignment.SetPosition(0, 35)
			#self.testAlignment.SetWindowHorizontalAlignCenter()
			#self.testAlignment.SetHorizontalAlignCenter()
			#self.testAlignment.SetFeather()
			#self.testAlignment.SetOutline()
			#self.testAlignment.Show()

		if app.ENABLE_KEYCHANGE_SYSTEM:
			pass
		else:
			self.__BuildKeyDict()

		self.__BuildDebugInfo()

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE

		if debugInfo.IsDebugMode():
			self.ToggleDebugInfo()

		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*m2netm2g.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = m2netm2g.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":						
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		m2netm2g.SendEnterGamePacket()
		
		if app.ENABLE_MONSTER_CARD:
			app.IllustratedCreate()
			m2netm2g.SendIllustrationMessage( m2netm2g.REQUEST_ILLUSTRATION )
			
		if app.ENABLE_MYSHOP_DECO:
			app.MyShopDecoBGCreate()
			
		if app.ENABLE_MINI_GAME_YUTNORI:
			app.YutnoriCreate()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT
		
		# NPC가 큐브시스템으로 만들 수 있는 아이템들의 목록을 캐싱
		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0

		mouseModule.mouseController.CreateNumberLine()
		
	def Close(self):
		self.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		chatm2g.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		mouseModule.mouseController.DeattachObject()

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None
	
		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			del self.interface
			self.interface=None
		
		if self.targetBoard:
			self.targetBoard.Destroy()
			self.targetBoard = None

		playerm2g2.ClearSkillDict()
		playerm2g2.ResetCameraRotation()

		self.KillFocus()
		app.HideCursor()
		
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.guildVoteCheckDialog = None
			self.guildVoteResultDialog = None
			self.guildVoteQuetionDialog = None
			
		if app.ENABLE_KEYCHANGE_SYSTEM:
			if self.wndKeyChange:
				self.wndKeyChange.KeyChangeWindowClose(True)
				self.wndKeyChange = None

		mouseModule.mouseController.Destroy()
		#print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	def __BuildKeyDict(self):
		onPressKeyDict = {}

		##PressKey 는 누르고 있는 동안 계속 적용되는 키이다.
		
		## 숫자 단축키 퀵슬롯에 이용된다.(이후 숫자들도 퀵 슬롯용 예약)
		## F12 는 클라 디버그용 키이므로 쓰지 않는 게 좋다.
		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		#캐릭터 이동키
		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			onPressKeyDict[app.DIK_P]			= lambda : self.interface.TogglePetInformationWindow()	##육성펫
			
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

		# CUBE_TEST
		#onPressKeyDict[app.DIK_K]			= lambda : self.interface.OpenCubeWindow()
		# CUBE_TEST_END

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()
		
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			## guild_renewal_war
			## 2014.04.15
			## TEB 키 추가
			onClickKeyDict[app.DIK_TAB] = lambda: self.__PressTabKey()


		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict
		
	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __PressTabKey(self):
			self.interface.OpenGuildScoreWindow()

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			
			if num >= 1 and num <= 9:
				if(chrmgrm2g.IsPossibleEmoticon(-1)):				
					chrmgrm2g.SetEmoticon(-1,int(num)-1)
					m2netm2g.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()


	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if playerm2g2.IsMountingHorse():
				m2netm2g.SendChatPacket("/unmount")
			else:
				#m2netm2g.SendChatPacket("/user_horse_ride")
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(playerm2g2.INVENTORY_PAGE_SIZE):
						if playerm2g2.GetItemIndex(i) in (71114, 71116, 71118, 71120):
							m2netm2g.SendItemUsePacket(i)
							break
	def	__PressHKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/user_horse_ride")
		else:
			self.interface.OpenHelpWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/user_horse_back")
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/user_horse_feed")	
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			m2netm2g.SendChatPacket("/ride")	
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
	
		if app.ENABLE_GROWTH_PET_SYSTEM:
			if localeInfo.IsARABIC():
				if 0 <= localSlotIndex and localSlotIndex < 4:
					localSlotIndex = 3 - localSlotIndex
				else:
					localSlotIndex = 11 - localSlotIndex
			
			result = playerm2g2.CanUseGrowthPetQuickSlot(localSlotIndex)
			
			if playerm2g2.QUICK_SLOT_POS_ERROR == result:
				return
			elif result in [playerm2g2.QUICK_SLOT_ITEM_USE_SUCCESS, playerm2g2.QUICK_SLOT_IS_NOT_ITEM, playerm2g2.QUICK_SLOT_PET_ITEM_USE_SUCCESS]:
				playerm2g2.RequestUseLocalQuickSlot(localSlotIndex)
			elif playerm2g2.QUICK_SLOT_PET_ITEM_USE_FAILED == result:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END)
			elif playerm2g2.QUICK_SLOT_CAN_NOT_USE_PET_ITEM == result:
				return
			
		else:
			if localeInfo.IsARABIC():
				if 0 <= localSlotIndex and localSlotIndex < 4:
					playerm2g2.RequestUseLocalQuickSlot(3-localSlotIndex)
				else:
					playerm2g2.RequestUseLocalQuickSlot(11-localSlotIndex)
			else:
				playerm2g2.RequestUseLocalQuickSlot(localSlotIndex)			
				
	if app.ENABLE_KEYCHANGE_SYSTEM:

		def OpenKeyChangeWindow(self):
			self.wndKeyChange.Open()
		
		def OpenWindow(self,type,state):
			if type == playerm2g2.KEY_OPEN_STATE:
				self.interface.ToggleCharacterWindow(state)
			elif type == playerm2g2.KEY_OPEN_INVENTORY:
				self.interface.ToggleInventoryWindow()
			elif type == playerm2g2.KEY_OPEN_DDS:
				self.interface.ToggleDragonSoulWindowWithNoInfo()
			elif type == playerm2g2.KEY_OPEN_MINIMAP:
				self.interface.ToggleMiniMap()
			elif type == playerm2g2.KEY_OPEN_LOGCHAT:
				self.interface.ToggleChatLogWindow()
			elif type == playerm2g2.KEY_OPEN_GUILD:
				self.interface.ToggleGuildWindow()
			elif type == playerm2g2.KEY_OPEN_MESSENGER:
				self.interface.ToggleMessenger()
			elif type == playerm2g2.KEY_OPEN_HELP:
				self.interface.ToggleHelpWindow()
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if type == playerm2g2.KEY_OPEN_PET:
					self.interface.TogglePetInformationWindow()
			if app.ENABLE_AUTO_SYSTEM:
				if type == playerm2g2.KEY_OPEN_AUTO:
					self.interface.ToggleAutoWindow()
			if app.ENABLE_MONSTER_CARD:
				if type == playerm2g2.KEY_MONSTER_CARD:
					self.interface.ToggleMonsterCardWindow()
			if app.ENABLE_PARTY_MATCH:
				if type == playerm2g2.KEY_PARTY_MATCH:
					self.interface.TogglePartyMatchWindow()
		
		def AppendChat(self,type,chattype):
			if chattype == chatm2g.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_SUMMON_BECAUSE_LIFE_TIME_END)

		def ScrollOnOff(self):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
				
	if app.ENABLE_AUTO_SYSTEM:
		def SetAutoCooltime(self, slotindex, cooltime):
			self.interface.SetAutoCooltime(slotindex, cooltime)
		def SetCloseGame(self):
			self.interface.SetCloseGame()

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		playerm2g2.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)
		
		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)
		
		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		# 오브젝트 그리는 개수
		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		# 시야거리
		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if playerm2g2.GetStatus(playerm2g2.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = playerm2g2.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == playerm2g2.PK_MODE_PROTECT:
			if 0 == playerm2g2.GetGuildID():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = playerm2g2.PK_MODE_GUILD

		elif nextPKMode == playerm2g2.PK_MODE_MAX_NUM:
			nextPKMode = 0

		m2netm2g.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[playerm2g2.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (playerm2g2.GetPKMode())

		#if constInfo.PVPMODE_TEST_ENABLE:
			#curPKMode = playerm2g2.GetPKMode()
			#alignment, grade = chr.testGetPKData()
			#self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			#self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			#self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()
		
	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		## guild_renewal
		def RefreshGuildBaseInfoPage(self):
			self.interface.RefreshGuildBaseInfoPage()

		## guild_renewal
		def RefreshGuildBaseInfoPageBankGold(self):
			self.interface.RefreshGuildBaseInfoPageBankGold()

		## guild_renewal_war
		def RefreshGuildWarInfoPage(self):
			self.interface.RefreshGuildWarInfoPage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):

		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if m2netm2g.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		m2netm2g.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
		self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		if app.ENABLE_SET_ITEM:
			if self.affectShower:
				self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		else:
			self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()
		elif app.ENABLE_PVP_TOURNAMENT == 1 and type == chr.NEW_AFFECT_IMPOSSIBLE_ATTACK :
			playerm2g2.SetAffectImpossibleAttack(True)

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if app.ENABLE_SET_ITEM:
			if self.affectShower:
				self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		else:
			self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()
		elif app.ENABLE_PVP_TOURNAMENT == 1 and type == chr.NEW_AFFECT_IMPOSSIBLE_ATTACK :
			playerm2g2.SetAffectImpossibleAttack(False)	
 
 
	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()
			if app.ENABLE_AUTO_SYSTEM:
				self.interface.RefreshAutoPositionSlot()	

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.ENABLE_PVP_TOURNAMENT and app.ENABLE_BATTLE_FIELD:
		def OnGameOver(self, openDlg, mapidx):
			self.CloseTargetBoard()
			if openDlg == True :
				self.OpenRestartDialog(mapidx)
	elif app.ENABLE_PVP_TOURNAMENT and not app.ENABLE_BATTLE_FIELD:
		def OnGameOver(self, openDlg):
			self.CloseTargetBoard()
			if openDlg == True :
				self.OpenRestartDialog()
	elif not app.ENABLE_PVP_TOURNAMENT and app.ENABLE_BATTLE_FIELD:
		def OnGameOver(self, openDlg, mapidx):
			self.CloseTargetBoard()
			if openDlg == True :
				self.OpenRestartDialog(mapidx)
	else : 
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

	if app.ENABLE_BATTLE_FIELD:
		def OpenRestartDialog(self, mapidx):
			self.interface.OpenRestartDialog(mapidx)
	else:
		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	if app.ENABLE_12ZI:
		def OpenUI12zi(self, yellowmark, greenmark, yellowreward, greenreward, goldreward):
			self.interface.OpenUI12zi(yellowmark, greenmark, yellowreward, greenreward, goldreward)
			
		def Refresh12ziTimer(self, currentFloor, jumpCount, limitTime, elapseTime):
			self.interface.Refresh12ziTimer(currentFloor, jumpCount, limitTime, elapseTime)
			
		def Show12ziJumpButton(self):
			self.interface.Show12ziJumpButton()
			
		def Hide12ziTimer(self):
			self.interface.Hide12ziTimer()
			
		def OpenReviveDialog(self, vid, itemcount):
			self.targetBoard.OpenReviveDialog(vid, itemcount);
			
		def RefreshShopItemToolTip(self):
			self.interface.RefreshShopItemToolTip()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):

		if self.interface.IsHideUiMode == True:
			return

		self.targetBoard.Open(vid, name)
		
		if app.IsPressed(app.DIK_LCONTROL):
			
			if not playerm2g2.IsSameEmpire(vid):
				return

			if playerm2g2.IsMainCharacterIndex(vid):
				return		
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)
			

	def RefreshTargetBoardByVID(self, vid):
		if self.targetBoard:
			self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		if self.targetBoard:
			self.targetBoard.RefreshByName(name)
		
	def __RefreshTargetBoard(self):
		if self.targetBoard:
			self.targetBoard.Refresh()
		
	def SetHPTargetBoard(self, vid, hpPercentage):

		if self.interface.IsHideUiMode == True:
			return

		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.ResetTargetBoard()
			self.targetBoard.SetEnemyVID(vid)

		self.targetBoard.SetHP(hpPercentage)
		self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count, dwChangeLookVnum):
			self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count, dwChangeLookVnum)
	else:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
			self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):

		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME	

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	def OnRecvWhisper(self, mode, name, line):
		if mode == chatm2g.WHISPER_TYPE_GM:
			self.interface.RegisterGameMasterName(name)
		chatm2g.AppendWhisper(mode, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chatm2g.AppendWhisper(chatm2g.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chatm2g.AppendWhisper(chatm2g.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode](name))
		else:
			chatm2g.AppendWhisper(chatm2g.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	def OnPickMoney(self, money):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (money))

	if app.ENABLE_CHEQUE_SYSTEM:
		def OnPickCheque(self, cheque):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHEQUE_SYSTEM_PICK_WON % (cheque))
			
	if app.ENABLE_GEM_SYSTEM:
		def OnPickGem(self, gem):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GEM_SYSTEM_PICK_GEM % (gem))
		def OpenGemShop(self):
			self.interface.OpenGemShop()
		def CloseGemShop(self):
			self.interface.CloseGemShop()		
		def RefreshGemShopWIndow(self):
			self.interface.RefreshGemShopWIndow()
		def GemShopSlotBuy(self, slotindex, enable):
			self.interface.GemShopSlotBuy(slotindex, enable)
		def BINARY_OpenSelectItemWindowEx(self):
			self.interface.BINARY_OpenSelectItemWindowEx()
		def BINARY_RefreshSelectItemWindowEx(self):
			self.interface.BINARY_RefreshSelectItemWindowEx()
		def GemShopSlotAdd(self, slotindex, enable):
			self.interface.GemShopSlotAdd(slotindex, enable)

	if app.ENABLE_BATTLE_FIELD:
		def OnPickBattlePoint(self, point):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_PICK_BATTLE_POINT % (point))
			
	if app.ENABLE_12ZI:
		def SetBeadCount(self, value):
			self.interface.SetBeadCount(value)
			
		def NextBeadUpdateTime(self, value):
			self.interface.NextBeadUpdateTime(value)
			
	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName):
		chatm2g.AppendChatWithDelay(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chatm2g.AppendChatWithDelay(chatm2g.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	## Exchange
	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()
		
	if app.ENABLE_CHEQUE_SYSTEM :
		def AddExchangeItemSlotIndex(self, idx) :
			self.interface.AddExchangeItemSlotIndex(idx)

	## Party
	#파티 가입 제한 시간때문에 수정.
	if app.WJ_NEW_USER_CARE:
		def RecvPartyInviteQuestion(self, leaderVID, leaderName):
			partyInviteQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
			partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.Open(leaderName + localeInfo.PARTY_DO_YOU_JOIN, 10)
			partyInviteQuestionDialog.SetTimeOverMsg(localeInfo.PARTY_ANSWER_TIMEOVER)
			partyInviteQuestionDialog.SetCancelOnTimeOver()
			partyInviteQuestionDialog.partyLeaderVID = leaderVID
			self.partyInviteQuestionDialog = partyInviteQuestionDialog
	else:
		def RecvPartyInviteQuestion(self, leaderVID, leaderName):
			partyInviteQuestionDialog = uiCommon.QuestionDialog()
			partyInviteQuestionDialog.SetText(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
			partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
			partyInviteQuestionDialog.Open()
			partyInviteQuestionDialog.partyLeaderVID = leaderVID
			self.partyInviteQuestionDialog = partyInviteQuestionDialog
	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		# 파티가입에 대한 거리 제한 삭제.
		if not app.WJ_NEW_USER_CARE:
			distance = playerm2g2.GetCharacterDistance(partyLeaderVID)
			if distance < 0.0 or distance > 5000:
				answer = False

		m2netm2g.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None
	
	if app.WJ_SHOW_PARTY_ON_MINIMAP and app.ENABLE_PARTY_CHANNEL_FIX:
		def AddPartyMember(self, pid, name, mapIdx, channel):
			self.interface.AddPartyMember(pid, name, mapIdx, channel)
	elif app.WJ_SHOW_PARTY_ON_MINIMAP:
		def AddPartyMember(self, pid, name, mapIdx):
			self.interface.AddPartyMember(pid, name, mapIdx)
	else:
		def AddPartyMember(self, pid, name):
			self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	if app.WJ_SHOW_PARTY_ON_MINIMAP and app.ENABLE_PARTY_CHANNEL_FIX:
		def LinkPartyMember(self, pid, vid, mapIdx, channel):
			self.interface.LinkPartyMember(pid, vid, mapIdx, channel)
	elif app.WJ_SHOW_PARTY_ON_MINIMAP:
		def LinkPartyMember(self, pid, vid, mapIdx):
			self.interface.LinkPartyMember(pid, vid, mapIdx)
	else:
		def LinkPartyMember(self, pid, vid):
			self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialog2()
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.SetText2(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_2)
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.Open()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		m2netm2g.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		m2netm2g.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	## SafeBox
	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	def RefreshSafeboxMoney(self):
		self.interface.RefreshSafeboxMoney()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			if localeInfo.IsNEWCIBN():
				guildInviteQuestionDialog.SetText(localeInfo.GUILD_DO_YOU_JOIN % (guildName))
			else:
				guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		else:
			guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		m2netm2g.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None

	
	def DeleteGuild(self):
		self.interface.DeleteGuild()
		
	if app.ENABLE_GUILDRENEWAL_SYSTEM:
 
		## GuildWar [guild_renewal]
		def SetGuildWarType(self, index):
			self.interface.SetGuildWarType(index)
		
		## GuildBank
		## 2014.01.14 [guild_renewal]
		def OpenGuildBankWindow(self, size):
			self.interface.OpenGuildBankWindow(size)
		def OpenGuildGoldInOutWindow(self, inout):
			self.interface.OpenGuildGoldInOutWindow(inout)

		# GuildBank
		# [guild_renewal]
		def RefreshGuildBank(self):
			self.interface.RefreshGuildBank()
		# GuildBankInfo
		def RefreshGuildBankInfo(self):
			self.interface.RefreshGuildBankInfo()
		def OpenGuildBankInfo(self):
			self.interface.OpenGuildBankInfo()
		## Guild LandDeal
		def RecvGuildLandDealQuestion(self, guildName, money):
			guildLandDealDialog = uiGuildPopup.GuildVoteDialog2()
			guildLandDealDialog.SetTitleBarText(localeInfo.GUILDLAND_DEAL)
			guildLandDealDialog.SetText1(localeInfo.GUILDLAND_DEAL_TEXT1 % (guildName))
			guildLandDealDialog.SetText2(localeInfo.GUILDLAND_DEAL_TEXT2 % (localeInfo.NumberToMoneyString(money)))
			guildLandDealDialog.SetText3(localeInfo.GUILDLAND_DEAL_TEXT3)
			guildLandDealDialog.SetAcceptText(localeInfo.GUILDLAND_ACCEPT)
			guildLandDealDialog.SetCancleText(localeInfo.GUILDLAND_NOT)
			guildLandDealDialog.SetAcceptEvent(lambda arg=True: self.GuildLandDealResult(arg, guildName, money))
			guildLandDealDialog.SetCancleEvent(lambda arg=False: self.GuildLandDealResult(arg, guildName, money))
			guildLandDealDialog.Open()
			self.guildLandDealDialog = guildLandDealDialog
	
		def GuildLandDealResult(self, answer, guildName, money):
		
			if answer == 1:
				if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
					m2netm2g.SendGuildLandDealResult(answer, money, guildName)
				else:
					if playerm2g2.GetMoney() < money:
						m2netm2g.SendGuildLandDealResult(2, money, guildName)
					else:
						m2netm2g.SendGuildLandDealResult(answer, money, guildName)
			else:
				m2netm2g.SendGuildLandDealResult(answer, money, guildName)
	
			self.guildLandDealDialog.Close()
			self.guildLandDealDialog = None
	
		## Guild Vote
		## 2013.11.07 [guild_renewal]
		## characterName : 투표진행 목적 캐릭터 아이디
		## type : 투표 종류 구분 1 = 길드장 이임 2 = 길드원 추방
		## PythonNetworkStreamPaseGame.cpp 에서 콜
		def RecvGuildVoteQuestion(self, characterName, type):
			print type
			guildVoteQuetionDialog = uiGuildPopup.GuildVoteDialog()
			if type == guild.VOTE_CHANGEMASTER:
				guildVoteQuetionDialog.SetTitleBarText(localeInfo.GUILDVOTE_CHANGEMASTER)
				guildVoteQuetionDialog.SetText1(localeInfo.GUILDVOTE_CHANGEMASTER_VOTETEXT1% (characterName))
				guildVoteQuetionDialog.SetText2(localeInfo.GUILDVOTE_CHANGEMASTER_VOTETEXT2)
			elif type == guild.VOTE_OUTMEMBER:
				guildVoteQuetionDialog.SetTitleBarText(localeInfo.GUILDVOTE_MEMBEROUT)
				guildVoteQuetionDialog.SetText1(localeInfo.GUILDVOTE_MEMBEROUT_VOTETEXT1 % (characterName))
				guildVoteQuetionDialog.SetText2(localeInfo.GUILDVOTE_MEMBEROUT_VOTETEXT2)
			elif type == guild.VOTE_LANDDELA:
				guildVoteQuetionDialog.SetTitleBarText(localeInfo.GUILDLAND_DEAL)
				guildVoteQuetionDialog.SetText1(localeInfo.GUILDLAND_DELA_VOTE % (characterName))
				guildVoteQuetionDialog.SetText2(localeInfo.GUILDLAND_DELA_VOTE_TEXT1)
			elif type == guild.VOTE_LANDABNDON:
				guildVoteQuetionDialog.SetTitleBarText(localeInfo.GUILDLAND_ABANDON)
				guildVoteQuetionDialog.SetText1(localeInfo.GUILDLAND_ABANDON_VOTE % (characterName))
				guildVoteQuetionDialog.SetText2(localeInfo.GUILDLAND_ABANDON_VOTE_TEXT1)
				
			guildVoteQuetionDialog.SetAcceptText(localeInfo.GUILDVOTE_OK)
			guildVoteQuetionDialog.SetCancleText(localeInfo.GUILDVOTE_NO)
			guildVoteQuetionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildVote(arg, type))
			guildVoteQuetionDialog.SetCancleEvent(lambda arg=False: self.AnswerGuildVote(arg, type))
			guildVoteQuetionDialog.Open()
			self.guildVoteQuetionDialog = guildVoteQuetionDialog
				
		def AnswerGuildVote(self, answer, type):
			## 길드 투표의 결과를 알린다.
			## answer = 1 찬성, answer = 0 반대
			m2netm2g.SendGuildVote(playerm2g2.GetMainCharacterName(),type, answer)
			self.guildVoteQuetionDialog.Close()
			self.guildVoteQuetionDialog = None
	
		## Guild Vote Check
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			def RecvGuildVoteCheck(self, type, agreesize, oppesesize, votesize, day, hour, min, sec):
				guildVoteCheckDialog = uiGuildPopup.GuildVoteResultDialog()
				if type == guild.VOTE_CHANGEMASTER:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDVOTE_CHANGEMASTER)
				elif type == guild.VOTE_OUTMEMBER:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDVOTE_MEMBEROUT)
				elif type == guild.VOTE_LANDDELA:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDLAND_DEAL)
				elif type == guild.VOTE_LANDABNDON:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDLAND_ABANDON)
				
				guildVoteCheckDialog.SetText1(localeInfo.LEFT_TIME)	
				guildVoteCheckDialog.SetText2(localeInfo.GUILDVOTE_RESULT_TIME % (day, hour, min, sec) )
				guildVoteCheckDialog.SetText3(localeInfo.GUILDVOTE_RESULT_ALL_MEMBER % (votesize)  )
				guildVoteCheckDialog.SetText4(localeInfo.GUILDVOTE_RESULT_AGGRE_MEMBER % (agreesize) )
				guildVoteCheckDialog.SetText5(localeInfo.GUILDVOTE_RESULT_OPPESE_MEMBER % (oppesesize))
				guildVoteCheckDialog.SetButtonText(localeInfo.UI_OK)
				guildVoteCheckDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildVoteCheckDialog(arg))
				guildVoteCheckDialog.Open()
				self.guildVoteCheckDialog = guildVoteCheckDialog
		else:
			def RecvGuildVoteCheck(self, type, agreesize, oppesesize, votesize, mon, hour, min, sec):
				guildVoteCheckDialog = uiGuildPopup.GuildVoteResultDialog()
				if type == guild.VOTE_CHANGEMASTER:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDVOTE_CHANGEMASTER)
				elif type == guild.VOTE_OUTMEMBER:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDVOTE_MEMBEROUT)
				elif type == guild.VOTE_LANDDELA:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDLAND_DEAL)
				elif type == guild.VOTE_LANDABNDON:
					guildVoteCheckDialog.SetTitleBarText(localeInfo.GUILDLAND_ABANDON)
				
				guildVoteCheckDialog.SetText1(localeInfo.LEFT_TIME)	
				guildVoteCheckDialog.SetText2(localeInfo.GUILDVOTE_RESULT_TIME % (mon, hour, min, sec) )
				guildVoteCheckDialog.SetText3(localeInfo.GUILDVOTE_RESULT_ALL_MEMBER % (votesize)  )
				guildVoteCheckDialog.SetText4(localeInfo.GUILDVOTE_RESULT_AGGRE_MEMBER % (agreesize) )
				guildVoteCheckDialog.SetText5(localeInfo.GUILDVOTE_RESULT_OPPESE_MEMBER % (oppesesize))
				guildVoteCheckDialog.SetButtonText(localeInfo.UI_OK)
				guildVoteCheckDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildVoteCheckDialog(arg))
				guildVoteCheckDialog.Open()
				self.guildVoteCheckDialog = guildVoteCheckDialog
	
		def AnswerGuildVoteCheckDialog(self, answer):
			self.guildVoteCheckDialog.Close()
			self.guildVoteCheckDialog = None
	
		## 길드 투표 결과 띄우기
		def RecvGuildVoteResult(self, characterName, guildname, type, result, agreesize, oppesesize, votesize):
	
			guildVoteResultDialog = uiGuildPopup.GuildVoteResultDialog()
			
			if type == guild.VOTE_CHANGEMASTER:
				guildVoteResultDialog.SetTitleBarText(localeInfo.GUILDVOTE_CHANGEMASTER)
				if result == 0:
					if characterName != chr.GetName():
						guildVoteResultDialog.SetText1(localeInfo.GUILDVOTE_CHANGEMASTER_RESULT5 % (characterName))
						guildVoteResultDialog.SetText2(localeInfo.GUILDVOTE_CHANGEMASTER_RESULT1)
					else:
						guildVoteResultDialog.SetText1(localeInfo.GUILDVOTE_CHANGEMASTER_RESULT2 % (guild.GetGuildName()))
						guildVoteResultDialog.SetText2(localeInfo.GUILDVOTE_CHANGEMASTER_RESULT1)
				else :
					guildVoteResultDialog.SetText1(localeInfo.GUILDVOTE_CHANGEMASTER_RESULT3 % (characterName))
					guildVoteResultDialog.SetText2(localeInfo.GUILDVOTE_CHANGEMASTER_RESULT4)
			elif type == guild.VOTE_OUTMEMBER:
				guildVoteResultDialog.SetTitleBarText(localeInfo.GUILDVOTE_MEMBEROUT)
				if result == 0:
					if characterName != chr.GetName():
						guildVoteResultDialog.SetText1(localeInfo.GUILDVOTE_MEMBEROUT_RESULT1 % (characterName))
						guildVoteResultDialog.SetText2(localeInfo.GUILDVOTE_MEMBEROUT_RESULT2)
					else:
						guildVoteResultDialog.SetText1(localeInfo.GUILDVOTE_MEMBEROUT_RESULT3 % (guildname))
						guildVoteResultDialog.SetText2(localeInfo.GUILDVOTE_MEMBEROUT_RESULT4)
				else :
					guildVoteResultDialog.SetText1(localeInfo.GUILDVOTE_MEMBEROUT_TEXT1 % (characterName))
					guildVoteResultDialog.SetText2(localeInfo.GUILDVOTE_MEMBEROUT_RESULT5)
			elif type == guild.VOTE_LANDDELA:
				guildVoteResultDialog.SetTitleBarText(localeInfo.GUILDLAND_DEAL)
				if result == 0:
					guildVoteResultDialog.SetText1(localeInfo.GUILDLAND_DELA_VOTE_RESULT1 % characterName)
					guildVoteResultDialog.SetText2(localeInfo.GUILDLAND_DELA_VOTE_RESULT2)
				else :
					guildVoteResultDialog.SetText1(localeInfo.GUILDLAND_DELA_VOTE_RESULT3)
					guildVoteResultDialog.SetText2(localeInfo.GUILDLAND_DELA_VOTE_RESULT4)
			elif type == guild.VOTE_LANDABNDON:
				guildVoteResultDialog.SetTitleBarText(localeInfo.GUILDLAND_ABANDON)
				if result == 0:
					guildVoteResultDialog.SetText1(localeInfo.GUILDLAND_ABANDON_VOTE_RESULT1 % guildname)
					guildVoteResultDialog.SetText2(localeInfo.GUILDLAND_ABANDON_VOTE_RESULT2)
				else :
					guildVoteResultDialog.SetText1(localeInfo.GUILDLAND_ABANDON_VOTE_RESULT3)
					guildVoteResultDialog.SetText2(localeInfo.GUILDLAND_ABANDON_VOTE_RESULT4)
			
	
			guildVoteResultDialog.SetText3(localeInfo.GUILDVOTE_RESULT_ALL_MEMBER % (votesize)  )
			guildVoteResultDialog.SetText4(localeInfo.GUILDVOTE_RESULT_AGGRE_MEMBER % (agreesize) )
			guildVoteResultDialog.SetText5(localeInfo.GUILDVOTE_RESULT_OPPESE_MEMBER % (oppesesize))
			guildVoteResultDialog.SetButtonText(localeInfo.UI_OK)
			guildVoteResultDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildResultDialog(arg))
			guildVoteResultDialog.Open()
			self.guildVoteResultDialog = guildVoteResultDialog
			
			if characterName != chr.GetName():
				if self.guildVoteQuetionDialog != None:
					self.guildVoteQuetionDialog.Close()
		
		def AnswerGuildResultDialog(self, answer):
			self.guildVoteResultDialog.Close()
			self.guildVoteResultDialog = None

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		print "save screen"

		# SCREENSHOT_CWDSAVE
		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()
		# END_OF_SCREENSHOT_CWDSAVE

		if succeeded:
			pass
			"""
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, name + localeInfo.SCREENSHOT_SAVE1)
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE2)
			"""
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		if debugInfo.IsDebugMode() or True == self.consoleEnable:
			playerm2g2.EndKeyWalkingImmediately()
			self.console.OpenWindow()

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			playerm2g2.SetQuickPage(self.quickSlotPageIndex+1)

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False
	# END_OF_ADD_ALWAYS_SHOW_NAME
	
	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		if not app.ENABLE_KEYCHANGE_SYSTEM:
			playerm2g2.SetQuickPage(self.quickSlotPageIndex)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		playerm2g2.SetAttackKeyState(True)

	def EndAttack(self):
		playerm2g2.SetAttackKeyState(False)

	def MoveUp(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		playerm2g2.SetSingleDIKKeyState(app.DIK_RIGHT, False)

	def PickUpItem(self):
		playerm2g2.PickCloseItem()

	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			if app.ENABLE_KEYCHANGE_SYSTEM:
				if self.wndKeyChange.IsOpen() == 1:
					## 키설정 창이 열렸을때. 그리고 뭐를 바꿀지 선택했을때
					if self.wndKeyChange.IsSelectKeySlot():
						if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL)
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LALT + self.ADDKEYBUFFERALT)
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						elif app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
							if self.wndKeyChange.IsChangeKey(self.wndKeyChange.GetSelectSlotNumber()):
								self.wndKeyChange.ChangeKey(key + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT)
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.KEYCHANGE_IMPOSSIBLE_CHANGE)
						else:
							self.wndKeyChange.ChangeKey(key)
				else:
					playerm2g2.OnKeyDown(key)
			else:
				self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnKeyUp(self, key):

		if app.ENABLE_KEYCHANGE_SYSTEM:
			playerm2g2.OnKeyUp(key)
		else:
			try:
				self.onClickKeyDict[key]()
			except KeyError:
				pass
			except:
				raise

		return True

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return

		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				playerm2g2.SetMouseState(playerm2g2.MBT_LEFT, playerm2g2.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):

		if self.interface.BUILD_OnMouseLeftButtonUp():
			return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if playerm2g2.SLOT_TYPE_QUICK_SLOT == attachedType:
				playerm2g2.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif playerm2g2.SLOT_TYPE_INVENTORY == attachedType:

				if playerm2g2.ITEM_MONEY == attachedItemIndex:
					#Note : 인벤 돈 셋팅 후, 다른 유저 클릭하면 들어오는 함수
					if app.ENABLE_CHEQUE_SYSTEM:
						cheque = mouseModule.mouseController.GetCheque()
						self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex, cheque)
					else: 
						self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## 바닥에 떨궜을때 악세서리(조합,흡수) 아이템 빼기.
			if playerm2g2.SLOT_TYPE_ACCE == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)
			
			if app.ENABLE_EXTEND_INVEN_SYSTEM:					
				if playerm2g2.SLOT_TYPE_EQUIPMENT == attachedType or \
					playerm2g2.SLOT_TYPE_BELT_INVENTORY == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)
				
			if app.ENABLE_AUTO_SYSTEM:
				if playerm2g2.SLOT_TYPE_AUTO == attachedType:
					if not self.interface.GetAutoStartonoff() == True:
						if attachedItemSlotPos <= playerm2g2.AUTO_SKILL_SLOT_MAX:
							playerm2g2.SetAutoSkillSlotIndex(attachedItemSlotPos,0)
							self.interface.RefreshAutoSkillSlot()
						else:
							playerm2g2.SetAutoPositionSlotIndex(attachedItemSlotPos,playerm2g2.ITEM_SLOT_COUNT)
							self.interface.RefreshAutoPositionSlot()
							
			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)
					
			mouseModule.mouseController.DeattachObject()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chatm2g.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				playerm2g2.SetMouseState(playerm2g2.MBT_LEFT, playerm2g2.MBS_CLICK)

		#playerm2g2.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			
			attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedType)
			
			if playerm2g2.INVENTORY == attachedInvenType or \
				playerm2g2.DRAGON_SOUL_INVENTORY == attachedInvenType or \
				playerm2g2.EQUIPMENT == attachedInvenType or \
				playerm2g2.BELT_INVENTORY == attachedInvenType:
			
				if True == chr.HasInstance(self.PickingCharacterIndex) and playerm2g2.GetMainCharacterIndex() != dstChrID:
					if playerm2g2.IsEquipmentSlot(attachedInvenType, attachedItemSlotPos):
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
							if chr.IsNPC(dstChrID) or chr.IsStone(dstChrID):
									m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
						else:
							if chr.IsNPC(dstChrID):
									m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
			
		else:
			if playerm2g2.SLOT_TYPE_INVENTORY == attachedType or playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedType)
				if True == chr.HasInstance(self.PickingCharacterIndex) and playerm2g2.GetMainCharacterIndex() != dstChrID:
					if playerm2g2.IsEquipmentSlot(attachedItemSlotPos) and playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
						self.stream.popupWindow.Close()
						self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
					else:
						if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
							if chr.IsNPC(dstChrID) or chr.IsStone(dstChrID):
									m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
						else:
							if chr.IsNPC(dstChrID):
									m2netm2g.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
							else:
								m2netm2g.SendExchangeStartPacket(dstChrID)
								m2netm2g.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)
				else:
					self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

		## 바닥에 떨궜을때 악세서리(조합,흡수) 아이템 빼기.
		if playerm2g2.SLOT_TYPE_ACCE == attachedType:
			self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)
			
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	if app.ENABLE_CHEQUE_SYSTEM:
		def __PutMoney(self, attachedType, attachedMoney, dstChrID, cheque):
			if True == chr.HasInstance(dstChrID) and playerm2g2.GetMainCharacterIndex() != dstChrID:
				m2netm2g.SendExchangeStartPacket(dstChrID)
				m2netm2g.SendExchangeElkAddPacket(attachedMoney, cheque)
			else:
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.CHEQUE_SYSTEM_DO_NOT_DROP_MONEY, 0, localeInfo.UI_OK)	
	else:
		def __PutMoney(self, attachedType, attachedMoney, dstChrID):
			if True == chr.HasInstance(dstChrID) and playerm2g2.GetMainCharacterIndex() != dstChrID:
				m2netm2g.SendExchangeStartPacket(dstChrID)
				m2netm2g.SendExchangeElkAddPacket(attachedMoney)
			else:
				self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		# PRIVATESHOP_DISABLE_ITEM_DROP - 개인상점 열고 있는 동안 아이템 버림 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():			
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
		
		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = playerm2g2.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		# PRIVATESHOP_DISABLE_ITEM_DROP - 개인상점 열고 있는 동안 아이템 버림 방지
		if uiPrivateShopBuilder.IsBuildingPrivateShop():			
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
		
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
		
			window_type = playerm2g2.SlotTypeToInvenType(attachedType)
			
			if playerm2g2.IsEquipmentSlot(window_type, attachedItemSlotPos):
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

			else:
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedType or\
					playerm2g2.SLOT_TYPE_BELT_INVENTORY == attachedType:
					
					dropItemIndex = playerm2g2.GetItemIndex(window_type, attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
					dropItemIndex = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

				## 바닥에 떨궜을때 악세서리(조합,흡수) 아이템 빼기.
				if playerm2g2.SLOT_TYPE_ACCE == attachedType:
					m2netm2g.SendAcceRefineCheckOut(attachedItemSlotPos)
					
				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
						m2netm2g.SendChangeLookCheckOut(attachedItemSlotPos)
		else:
		
			if playerm2g2.SLOT_TYPE_INVENTORY == attachedType and playerm2g2.IsEquipmentSlot(attachedItemSlotPos):
				self.stream.popupWindow.Close()
				self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

			else:
				if playerm2g2.SLOT_TYPE_INVENTORY == attachedType:
					dropItemIndex = playerm2g2.GetItemIndex(attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
					dropItemIndex = playerm2g2.GetItemIndex(playerm2g2.DRAGON_SOUL_INVENTORY, attachedItemSlotPos)

					item.SelectItem(dropItemIndex)
					dropItemName = item.GetItemName()

					## Question Text
					questionText = localeInfo.HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, attachedItemCount)

					## Dialog
					itemDropQuestionDialog = uiCommon.QuestionDialog()
					itemDropQuestionDialog.SetText(questionText)
					itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
					itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
					itemDropQuestionDialog.Open()
					itemDropQuestionDialog.dropType = attachedType
					itemDropQuestionDialog.dropNumber = attachedItemSlotPos
					itemDropQuestionDialog.dropCount = attachedItemCount
					self.itemDropQuestionDialog = itemDropQuestionDialog

					constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

				## 바닥에 떨궜을때 악세서리(조합,흡수) 아이템 빼기.
				if playerm2g2.SLOT_TYPE_ACCE == attachedType:
					m2netm2g.SendAcceRefineCheckOut(attachedItemSlotPos)
					
				## 바닥에 떨궜을때 형상변환 아이템 빼기.
				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					if playerm2g2.SLOT_TYPE_CHANGE_LOOK == attachedType:
						m2netm2g.SendChangeLookCheckOut(attachedItemSlotPos)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			dropType = self.itemDropQuestionDialog.dropType
			dropCount = self.itemDropQuestionDialog.dropCount
			dropNumber = self.itemDropQuestionDialog.dropNumber

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				if playerm2g2.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == playerm2g2.ITEM_MONEY:
						m2netm2g.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						# PRIVATESHOP_DISABLE_ITEM_DROP
						self.__SendDropItemPacket(dropNumber, dropCount)
						# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
						
				elif playerm2g2.SLOT_TYPE_BELT_INVENTORY == dropType:
					self.__SendDropItemPacket(dropNumber, dropCount, playerm2g2.BELT_INVENTORY)
					
				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
					# PRIVATESHOP_DISABLE_ITEM_DROP
					self.__SendDropItemPacket(dropNumber, dropCount, playerm2g2.DRAGON_SOUL_INVENTORY)
					# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
			else:
				if playerm2g2.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == playerm2g2.ITEM_MONEY:
						m2netm2g.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						# PRIVATESHOP_DISABLE_ITEM_DROP
						self.__SendDropItemPacket(dropNumber, dropCount)
						# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP
				elif playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
						# PRIVATESHOP_DISABLE_ITEM_DROP
						self.__SendDropItemPacket(dropNumber, dropCount, playerm2g2.DRAGON_SOUL_INVENTORY)
						# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	# PRIVATESHOP_DISABLE_ITEM_DROP
	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = playerm2g2.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		m2netm2g.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
	# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			playerm2g2.SetMouseState(playerm2g2.MBT_RIGHT, playerm2g2.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		playerm2g2.SetMouseState(playerm2g2.MBT_RIGHT, playerm2g2.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		playerm2g2.SetMouseMiddleButtonState(playerm2g2.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		playerm2g2.SetMouseMiddleButtonState(playerm2g2.MBS_CLICK)

	def OnUpdate(self):	
		app.UpdateGame()
		
		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		self.interface.BUILD_OnUpdate()
		
		
	def UpdateDebugInfo(self):
		#
		# 캐릭터 좌표 및 FPS 출력
		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))			

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		#self.Pitch.SetText("Pitch: %.2f" % (app.GetCameraPitch())
		#self.TextureNum.SetText("TN : %s" % (sTextureNum))
		#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()
		
		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME
			
		## Show all name in the range
		
		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################
	
	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING
	
	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.Open(msg, timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: m2netm2g.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: m2netm2g.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		self.confirmDialog = confirmDialog
    # END_OF_QUEST_CONFIRM

    # GIFT command
	def Gift_Show(self):
		self.interface.ShowGift()

	# CUBE
	def BINARY_Cube_Open(self, npcVNUM):
		self.currentCubeNPC = npcVNUM
		
		self.interface.OpenCubeWindow()

		
		if npcVNUM not in self.cubeInformation:
			m2netm2g.SendChatPacket("/cube r_info")
		else:
			cubeInfoList = self.cubeInformation[npcVNUM]
			
			i = 0
			for cubeInfo in cubeInfoList:								
				self.interface.wndCube.AddCubeResultItem(cubeInfo["vnum"], cubeInfo["count"])
				
				j = 0				
				for materialList in cubeInfo["materialList"]:
					for materialInfo in materialList:
						itemVnum, itemCount = materialInfo
						self.interface.wndCube.AddMaterialInfo(i, j, itemVnum, itemCount)
					j = j + 1						
						
				i = i + 1
				
			self.interface.wndCube.Refresh()

	def BINARY_Cube_Close(self):
		self.interface.CloseCubeWindow()

	# 제작에 필요한 골드, 예상되는 완성품의 VNUM과 개수 정보 update
	def BINARY_Cube_UpdateInfo(self, gold, itemVnum, count):
		self.interface.UpdateCubeInfo(gold, itemVnum, count)
		
	def BINARY_Cube_Succeed(self, itemVnum, count):
		print "큐브 제작 성공"
		self.interface.SucceedCubeWork(itemVnum, count)
		pass

	def BINARY_Cube_Failed(self):
		print "큐브 제작 실패"
		self.interface.FailedCubeWork()
		pass

	def BINARY_Cube_ResultList(self, npcVNUM, listText):
		# ResultList Text Format : 72723,1/72725,1/72730.1/50001,5  이런식으로 "/" 문자로 구분된 리스트를 줌
		#print listText
		
		if npcVNUM == 0:
			npcVNUM = self.currentCubeNPC
		
		self.cubeInformation[npcVNUM] = []
		
		try:
			for eachInfoText in listText.split("/"):
				eachInfo = eachInfoText.split(",")
				itemVnum	= int(eachInfo[0])
				itemCount	= int(eachInfo[1])

				self.cubeInformation[npcVNUM].append({"vnum": itemVnum, "count": itemCount})
				self.interface.wndCube.AddCubeResultItem(itemVnum, itemCount)
			
			resultCount = len(self.cubeInformation[npcVNUM])
			requestCount = 5
			modCount = resultCount % requestCount
			splitCount = resultCount / requestCount
			for i in xrange(splitCount):
				#print("/cube r_info %d %d" % (i * requestCount, requestCount))
				m2netm2g.SendChatPacket("/cube r_info %d %d" % (i * requestCount, requestCount))
				
			if 0 < modCount:
				#print("/cube r_info %d %d" % (splitCount * requestCount, modCount))				
				m2netm2g.SendChatPacket("/cube r_info %d %d" % (splitCount * requestCount, modCount))

		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0
			
		pass
		
	def BINARY_Cube_MaterialInfo(self, startIndex, listCount, listText):
		# Material Text Format : 125,1|126,2|127,2|123,5&555,5&555,4/120000
		try:
			#print listText
			
			if 3 > len(listText):
				dbg.TraceError("Wrong Cube Material Infomation")
				return 0

			
			
			eachResultList = listText.split("@")

			cubeInfo = self.cubeInformation[self.currentCubeNPC]			
			
			itemIndex = 0
			for eachResultText in eachResultList:
				cubeInfo[startIndex + itemIndex]["materialList"] = [[], [], [], [], []]
				materialList = cubeInfo[startIndex + itemIndex]["materialList"]
				
				gold = 0
				splitResult = eachResultText.split("/")
				if 1 < len(splitResult):
					gold = int(splitResult[1])
					
				#print "splitResult : ", splitResult
				eachMaterialList = splitResult[0].split("&")
				
				i = 0
				for eachMaterialText in eachMaterialList:
					complicatedList = eachMaterialText.split("|")
					
					if 0 < len(complicatedList):
						for complicatedText in complicatedList:
							(itemVnum, itemCount) = complicatedText.split(",")
							itemVnum = int(itemVnum)
							itemCount = int(itemCount)
							self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)
							
							materialList[i].append((itemVnum, itemCount))
							
					else:
						itemVnum, itemCount = eachMaterialText.split(",")
						itemVnum = int(itemVnum)
						itemCount = int(itemCount)
						self.interface.wndCube.AddMaterialInfo(itemIndex + startIndex, i, itemVnum, itemCount)
						
						materialList[i].append((itemVnum, itemCount))
						
					i = i + 1
					
					
					
				itemIndex = itemIndex + 1
				
			self.interface.wndCube.Refresh()
			
				
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0
			
		pass
	
	# END_OF_CUBE
	
	# 용혼석	
	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		self.interface.Highligt_Item(inven_type, inven_pos)
	
	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()
		
	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)
	
	# END of DRAGON SOUL REFINE WINDOW
	
	def BINARY_SetBigMessage(self, message):
		self.interface.bigBoard.SetTip(message)
		
	if app.ENABLE_OX_RENEWAL:
		def BINARY_SetBigControlMessage(self, message):
			self.interface.bigBoardControl.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		self.interface.tipBoard.SetTip(message)		

	if app.ENABLE_12ZI:
		def BINARY_SetMissionMessage(self, message):
			self.interface.missionBoard.SetMission(message)
			
		def BINARY_SetSubMissionMessage(self, message):
			self.interface.missionBoard.SetSubMission(message)
			
		def BINARY_CleanMissionMessage(self):
			self.interface.missionBoard.CleanMission()
		
	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		## [guild_renewal_war]
		def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType, winType, ScoreType, TimeType, DeclearTargetName):
			mainCharacterName = playerm2g2.GetMainCharacterName()
			masterName = guild.GetGuildMasterName()

			print DeclearTargetName
			print mainCharacterName
				
			if mainCharacterName == DeclearTargetName:
				self.__GuildWar_OpenAskDialog(guildID, warType, winType, ScoreType, TimeType)

		## [guild_renewal_war]
		def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point, winpoint):
			self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point, winpoint)
	else:
		def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
			mainCharacterName = playerm2g2.GetMainCharacterName()
			masterName = guild.GetGuildMasterName()
			if mainCharacterName == masterName:
				self.__GuildWar_OpenAskDialog(guildID, warType)

		def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
			self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			if self.guildWarQuestionDialog:
				self.__GuildWar_CloseAskDialog()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_BettingGuildWar_SetObserverMode(self, isEnable,isButtonShow):
			self.interface.BINARY_SetObserverMode(isEnable,isButtonShow)
	else:
		def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
			self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __GuildWar_OpenAskDialog(self, guildID, warType, winType, ScoreType, TimeType):

			guildName = guild.GetGuildName(guildID)

			# REMOVED_GUILD_BUG_FIX
			if "Noname" == guildName:
				return
			# END_OF_REMOVED_GUILD_BUG_FIX

			import uiGuild
			questionDialog = uiGuild.AcceptGuildWarDialog()
			questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
			questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
			## [guild_renewal_war]
			questionDialog.Open(guildName, warType, winType, ScoreType, TimeType)

			self.guildWarQuestionDialog = questionDialog
	else:
		def __GuildWar_OpenAskDialog(self, guildID, warType):

			guildName = guild.GetGuildName(guildID)

			# REMOVED_GUILD_BUG_FIX
			if "Noname" == guildName:
				return
			# END_OF_REMOVED_GUILD_BUG_FIX

			import uiGuild
			questionDialog = uiGuild.AcceptGuildWarDialog()
			questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
			questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
			questionDialog.Open(guildName, warType)
	
			self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __GuildWar_OnAccept(self):

			guildName = self.guildWarQuestionDialog.GetGuildName()
			guildwarType = self.guildWarQuestionDialog.GetGuildWarTypes()
			m2netm2g.SendChatPacket("/war %s %d %d %d %d" % (guildName, guildwarType.get(0), guildwarType.get(1), guildwarType.get(2), guildwarType.get(3)))
			self.__GuildWar_CloseAskDialog()

			return 1
	else:
		def __GuildWar_OnAccept(self):

			guildName = self.guildWarQuestionDialog.GetGuildName()

			m2netm2g.SendChatPacket("/war " + guildName)
			self.__GuildWar_CloseAskDialog()

			return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		m2netm2g.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update, 
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update, 
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,

			# SKILLBOOK COMBINATION
			"OpenSkillbookCombinationDialog" : self.OpenSkillbookCombinationDialog,

			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,

			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			# END_OF_WEDDING

			# PRIVATE_SHOP_PRICE_LIST
			"MyShopPriceList"		: self.__PrivateShop_PriceList,
			# END_OF_PRIVATE_SHOP_PRICE_LIST
			
			# ACCE
			"ShowAcceCombineDialog" : self.__AcceCombineDialog,
			"ShowAcceAbsorbDialog"  : self.__AcceAbsorbDialog,
			# END_ACCE
			
			# COSTUME_REFINE_SYSTEM
			"ShowItemCombinationDialog"  : self.__ItemCombinationDialog,
			# END_ACCE
			
			# THREEWAY_SAFEZONE
			"threeway_safezone_enable" : self.__ThreeWay_SafeZone_Enable,
			# END_THREEWAY_SAFEZONE
			
			#DRAGON_SOUL
			"ShowMeDSRefinePassword": self.__AskDSRefinePassword,
			"ResetDSActiveButton"	: self.__ResetDSActiveButton,
			"ShowMeDSPassword"		: self.__AskDSPassword,
			"OpenDSInventory"		: self.__OpenDSInventory,
			"CloseDSInventory"		: self.__CloseDSInventory,
		}

		if app.ENABLE_NEW_HALLOWEEN_EVENT:
			serverCommandList["halloween_box"] = self.__Halloween_Box
			
		serverCommandList["mini_game_okey"] = self.__MiniGameOkey
			
		if app.ENABLE_2016_VALENTINE:
			serverCommandList["valentine_drop"] = self.__ValentineEvent
		
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			serverCommandList["clear_guildranking"] = self.__ClearGuildRanking
			serverCommandList["clear_applicant"] = self.__ClearApplicant
			serverCommandList["clear_applicantguild"] = self.__ClearApplicantGuild	
		
		if app.ENABLE_MONSTER_BACK:
			if app.ENABLE_10TH_EVENT:
				serverCommandList["e_monsterback"] = self.__MonsterBack
			else:
				serverCommandList["e_easter_monsterback"] = self.__EasterMonsterBack
		
		if app.ENABLE_CARNIVAL2016:
			serverCommandList["carnival_event"] = self.__CarnivalEvent
			
		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			serverCommandList["clear_guild_reddragonlair_ranking"] = self.__ClearGuildRedDragonLairRanking
			serverCommandList["check_reddragonlairranking_board"] = self.__CheckRedDragonLairRanking
						
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			serverCommandList["mini_game_okey_normal"] = self.__MiniGameOkeyNormal
			
		if app.ENABLE_AUTO_SYSTEM:
			serverCommandList["auto_off"] = self.__AutoOff
			serverCommandList["auto_on"] = self.__AutoOn
			serverCommandList["auto_loginoff"] = self.__AutoLoginOff
		
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			serverCommandList["ShowChangeDialog"] = self.__ChangeWindowOpen
			
		if app.ENABLE_SUMMER_EVENT:
			serverCommandList["e_summer_event"] = self.__SummerEvent
		
		if app.ENABLE_2017_RAMADAN:
			serverCommandList["e_2017_ramadan_event"] = self.__2017RamaDanEvent

		if app.ENABLE_CHEQUE_SYSTEM:
			serverCommandList["OpenPrivateShop_Cash"] = self.__CashPrivateShop_Open
			
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			serverCommandList["guild_war"] = self.__Check_Guild_War
			
		if app.ENABLE_MYSHOP_DECO :
			serverCommandList["OpenMyShopDecoWnd"] = self.__OpenMyShopDecoWnd
			
		if app.ENABLE_BATTLE_FIELD:
			serverCommandList["battle_field"] = self.__BattleFieldInfo
			serverCommandList["battle_field_open"] = self.__BattleFieldOpen
			serverCommandList["battle_field_event"] = self.__BattleFieldEventInfo
			serverCommandList["battle_field_event_open"] = self.__BattleFieldEventOpen
			
		if app.ENABLE_FISH_EVENT:
			serverCommandList["fish_event"] = self.__FishEvent	
		
		if app.ENABLE_MOVE_CHANNEL:
			serverCommandList["server_info"] = self.__SeverInfo
			
		if app.ENABLE_EXP_EVENT:
			serverCommandList["exp_bonus_event_start"] = self.__ExpBonusEventStart
			
		if app.ENABLE_PARTY_MATCH:
			serverCommandList["party_match_off"] = self.__PartyMatchOff
			
		if app.ENABLE_REFINE_MSG_ADD:
			serverCommandList["RefineFailedType"] = self.__RefineFailedTypeMessage
			
		if app.ENABLE_PVP_TOURNAMENT_GF:
			serverCommandList["init_skill_cooltime"] = self.InitSkillCoolTime
			
		if app.ENABLE_SOUL_SYSTEM:
			serverCommandList["RefineSoulSuceeded"] = self.__RefineSoulSuceededMessage
			serverCommandList["RefineSoulFailed"] = self.__RefineSoulFailedMessage
			
		if app.ENABLE_PVP_TOURNAMENT_GF:
			serverCommandList["pvp_tournament_auto"] = self.__PvPTournamentAutoSet
			
		if app.ENABLE_PVP_ONOFF:
			serverCommandList["pvp_onoff"] = self.__PvPOnOff
			
		if app.ENABLE_MINI_GAME_YUTNORI:
			serverCommandList["mini_game_yutnori"] = self.__MiniGameYutnori
			
		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)
			
	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def __Check_Guild_War(self, enable):
			if self.interface:
				if int(enable) == 1:
					self.interface.ShowGuildWarButton()
				else:
					self.interface.HideGuildWarButton()
			
	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def __ChangeWindowOpen(self):
			self.interface.ChangeWindowOpen()
			
	if app.ENABLE_AUTO_SYSTEM:
		def __AutoOff(self):
			if self.interface:
				self.interface.AutoOff()
			if item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):	
				self.BINARY_NEW_RemoveAffect(chr.NEW_AFFECT_AUTO_USE,0)
			chrmgrm2g.SetAutoOnOff(False)
		def __AutoOn(self):
			if self.interface:
				self.interface.AutoOn()
			chrmgrm2g.SetAutoOnOff(True)
			if item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):	
				self.BINARY_NEW_AddAffect(chr.NEW_AFFECT_AUTO_USE,0,0,item.GetAffectDuration(chr.NEW_AFFECT_AUTO_USE))
		def __AutoLoginOff(self):
			chrmgrm2g.SetAutoOnOff(False)

	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def __ClearGuildRedDragonLairRanking(self):
			guild.ClearRedDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED)

		def __CheckRedDragonLairRanking(self):
			if guild.CheckRedDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED) == 0:
				self.interface.RefreshGuildDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED)
				self.interface.OpenGuildDragonLairRanking(guild.GUILD_DRAGONLAIR_TYPE_RED)

	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def __ClearGuildRanking(self):
			guild.ClearGuildRanking()

		def __ClearApplicant(self):
			guild.ClearApplicant()

		def __ClearApplicantGuild(self):
			guild.ClearApplicantGuild()

	if app.ENABLE_NEW_HALLOWEEN_EVENT:
		def __Halloween_Box(self,enable):
			playerm2g2.SetHalloweenBox_Event(int(enable))
	
	def __MiniGameOkey(self, enable):
	
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			if "0" != enable:
				playerm2g2.SetMiniGameWindowOpen(True)
			else:
				playerm2g2.SetMiniGameWindowOpen(False)
			
			if self.interface:
				self.interface.IntegrationEventBanner()
		else:
			if "0" != enable:
				playerm2g2.SetMiniGameWindowOpen(True)
			else:
				playerm2g2.SetMiniGameWindowOpen(False)
			
			if self.interface:
				self.interface.MiniGameOkey()
			
	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def __MiniGameOkeyNormal(self, enable):
			if "0" != enable:
				playerm2g2.SetMiniGameOkeyNormal( True )
			else:
				playerm2g2.SetMiniGameOkeyNormal( False )
				
			if self.interface:
				self.interface.SetOkeyNormalBG()

	if app.ENABLE_2016_VALENTINE:
		def __ValentineEvent(self, enable):
			playerm2g2.SetValentineEvent(int(enable))
			
	if app.ENABLE_MONSTER_BACK:
		if app.ENABLE_10TH_EVENT:
			def __MonsterBack(self, enable):
			
				playerm2g2.SetAttendance(int(enable))
				
				if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
					playerm2g2.SetMonsterBackEvent(int(enable))
					
				if self.interface:
					self.interface.IntegrationEventBanner()
		else:
			def __EasterMonsterBack(self, enable):
			
				playerm2g2.SetAttendance(int(enable))
				
				if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
					playerm2g2.SetMonsterBackEvent(int(enable))
					
				if self.interface:
					self.interface.IntegrationEventBanner()				
				
	if app.ENABLE_CARNIVAL2016:
		def __CarnivalEvent(self, enable):
		
			playerm2g2.SetAttendance(int(enable))
			
			if self.interface:
				self.interface.IntegrationEventBanner()
				
	if app.ENABLE_FISH_EVENT:
		def __FishEvent(self, enable):
		
			playerm2g2.SetFishEventGame(int(enable))
			
			if self.interface:
				self.interface.IntegrationEventBanner()
				
	if app.ENABLE_SUMMER_EVENT:
		def __SummerEvent(self, enable):
			playerm2g2.SetSummerEvent(int(enable))
			
	if app.ENABLE_2017_RAMADAN:
		def __2017RamaDanEvent(self, enable):
			playerm2g2.Set2017RamaDanEvent(int(enable))
			
	if app.ENABLE_MINI_GAME_YUTNORI:
		def __MiniGameYutnori(self, enable):
		
			playerm2g2.SetYutnoriGame(int(enable))
			
			if self.interface:
				self.interface.IntegrationEventBanner()

	def __ThreeWay_SafeZone_Enable(self, enable):
		playerm2g2.SetSafeZoneAttEnable(int(enable))

	def BINARY_ServerCommand_Run(self, line):
		#dbg.TraceError(line)
		try:
			#print " BINARY_ServerCommand_Run", line
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = m2netm2g.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = m2netm2g.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	def OpenSkillbookCombinationDialog(self):
		self.interface.OpenSkillbookCombinationDialog()

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)
		
	if app.ENABLE_SOUL_SYSTEM:
		def __RefineSoulSuceededMessage(self):
			snd.PlaySound("sound/ui/make_soket.wav")
			self.PopupMessage(localeInfo.SOUL_REFINE_SUCCESS)
		def __RefineSoulFailedMessage(self):
			snd.PlaySound("sound/ui/jaeryun_fail.wav")
			self.PopupMessage(localeInfo.SOUL_REFINE_FAILURE)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()
		
	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		# [guild_renewal] 2014.01.17
		def CommandCloseGuildBank(self):
			self.interface.CommandCloseGuildBank()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		if app.ENABLE_CHEQUE_SYSTEM:
			return
		else:
			uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)		
	# END_OF_PRIVATE_SHOP_PRICE_LIST

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon_01",
					"metin2_map_spiderdungeon_02",
					"metin2_map_spiderdungeon_03",
					"metin2_map_deviltower1",
					"season1/metin2_map_sungzi_flame_hill_01",
					"season1/metin2_map_sungzi_flame_hill_02",
					"season1/metin2_map_sungzi_flame_hill_03",
					"season1/metin2_map_sungzi_desert_01",
					"season1/metin2_map_sungzi_desert_hill_01",
					"season1/metin2_map_sungzi_desert_hill_02",
					"season1/metin2_map_sungzi_desert_hill_03",
					"season2/metin2_map_empirewar03",
					"metin2_map_devilsCatacomb",
					"metin2_map_Mt_Thunder",
					"metin2_map_n_flame_dungeon_01",
					"metin2_map_dawnmist_dungeon_01",
					"metin2_map_Mt_Th_dungeon_01",)

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				background.SetXMasShowEvent(1)
			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				background.SetXMasShowEvent(0)
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return			

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)
		self.ShowConsole()

	## PrivateShop
	if app.ENABLE_CHEQUE_SYSTEM:
		def __CashPrivateShop_Open(self):
			if app.ENABLE_MYSHOP_DECO:
				return
				
			self.interface.OpenPrivateShopInputNameDialog(True)
			
		def __PrivateShop_Open(self):
			if app.ENABLE_MYSHOP_DECO:
				return
				
			self.interface.OpenPrivateShopInputNameDialog(False)
	else:
		def __PrivateShop_Open(self):
			self.interface.OpenPrivateShopInputNameDialog()

	if app.ENABLE_MYSHOP_DECO:
		def MyPrivShopOpen(self, cashItem, tabCnt) :
			self.interface.OpenPrivateShopInputNameDialog(cashItem, tabCnt)
			
		def __OpenMyShopDecoWnd(self):
			self.interface.OpenMyShopDecoWnd()
			
		def BINARY_PrivateShop_Appear(self, vid, text, type):
			self.interface.AppearPrivateShop(vid, text, type)
	else:
		def BINARY_PrivateShop_Appear(self, vid, text):
			self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			if app.ENABLE_12ZI:
				if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
					if not background.IsBoomMap():
						return
				else:
					if not self.__IsXMasMap():
						return
					
				background.SetEnvironmentData(background.DAY_MODE_LIGHT)
			else:
				background.SetEnvironmentData(0)
		elif "dark"==mode:

			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return
			
			if app.ENABLE_12ZI:
				background.RegisterEnvironmentData(background.DAY_MODE_DARK, constInfo.ENVIRONMENT_NIGHT)
				background.SetEnvironmentData(background.DAY_MODE_DARK)
			else:
				background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
				background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			if app.ENABLE_12ZI:
				if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
					if not background.IsBoomMap():
							return
					else:
						if not self.__IsXMasMap():
							return
					
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				if not background.IsBoomMap():
					return
			else:
				if not self.__IsXMasMap():
					return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		if app.ENABLE_12ZI:
			background.SetEnvironmentData(background.DAY_MODE_LIGHT)
		else:
			background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		if app.ENABLE_12ZI:
			background.RegisterEnvironmentData(background.DAY_MODE_DARK, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(background.DAY_MODE_DARK)
		else:
			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)
		self.curtain.FadeIn()
		
	if app.ENABLE_12ZI:
		def BINARY_SetEnvironment(self, idx):
			self.indexEnv = idx
			self.curtain.SAFE_FadeOut(self.__SetEnvironment)
		
		def __SetEnvironment(self):
			background.SetEnvironmentData(self.indexEnv)
			self.curtain.FadeIn()

	## XMasBoom
	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = playerm2g2.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	if app.WJ_NEW_USER_CARE:
		def __PartyRequestQuestion(self, vid, name):
			vid = int(vid)
			partyRequestQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
			partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
			partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
			partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.Open(name + localeInfo.PARTY_DO_YOU_ACCEPT, 10)
			partyRequestQuestionDialog.SetTimeOverMsg(localeInfo.PARTY_ANSWER_TIMEOVER)
			partyRequestQuestionDialog.SetCancelOnTimeOver()
			partyRequestQuestionDialog.vid = vid
			self.partyRequestQuestionDialog = partyRequestQuestionDialog
	else:
		def __PartyRequestQuestion(self, vid):
			vid = int(vid)
			partyRequestQuestionDialog = uiCommon.QuestionDialog()
			partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
			partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
			partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
			partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
			partyRequestQuestionDialog.Open()
			partyRequestQuestionDialog.vid = vid
			self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			m2netm2g.SendChatPacket("/party_request_accept " + str(vid))
		else:
			m2netm2g.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	# WEDDING
	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	# END_OF_WEDDING
	
	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def OpenPShopSearchDialog(self):
			self.interface.OpenPShopSearchDialog()
		def OpenPShopSearchDialogCash(self):
			self.interface.OpenPShopSearchDialogCash()
		def RefreshPShopSearchDialog(self):
			self.interface.RefreshPShopSearchDialog()
	
	# ACCE
	def __AcceCombineDialog(self):
		self.interface.AcceDialogOpen(playerm2g2.ACCE_SLOT_TYPE_COMBINE)

	def __AcceAbsorbDialog(self):
		self.interface.AcceDialogOpen(playerm2g2.ACCE_SLOT_TYPE_ABSORB)

	def RefreshAcceWindow(self):
		self.interface.RefreshAcceWindow()
	
	## HilightSlot Change	
	def DeactivateSlot(self, slotindex, type):
		self.interface.DeactivateSlot(slotindex, type)
	
	## HilightSlot Change	
	def ActivateSlot(self, slotindex, type):
		self.interface.ActivateSlot(slotindex, type)

	if app.ENABLE_MOVE_COSTUME_ATTR:
		def __ItemCombinationDialog(self):
			self.interface.ItemCombinationDialogOpen()
	else:
		def __ItemCombinationDialog(self):
			return
			
	def ShowCostumeInventory(self) :
		self.interface.ShowCostumeInventory()

	#DRAGON_SOUL
	if app.ENABLE_DS_PASSWORD:
		def __AskDSRefinePassword(self):
			self.interface.AskDSRefinePassword()
		
		def __ResetDSActiveButton(self):
			self.interface.ResetDSActiveButton()
		
		def __AskDSPassword(self):
			self.interface.AskDSPassword()
			
		def __OpenDSInventory(self):
			self.interface.OpenDSInventory()
		
		def __CloseDSInventory(self):
			self.interface.CloseDSInventory()
	else:
		def __AskDSRefinePassword(self):
			return
		
		def __ResetDSActiveButton(self):
			return
		
		def __AskDSPassword(self):
			return
			
		def __OpenDSInventory(self):
			return
		
		def __CloseDSInventory(self):
			return
			
	
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetHatchingWindowCommand(self, command, window, pos):
			self.interface.PetHatchingWindowCommand(command, window, pos)
		def PetNameChangeWindowCommand(self, command, srcWindow, srcPos, dstWindow, dstPos):
			self.interface.PetNameChangeWindowCommand(command, srcWindow, srcPos, dstWindow, dstPos)
			
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetSkillUpgradeDlgOpen(self, slot, index, gold):
			self.interface.PetSkillUpgradeDlgOpen(slot, index, gold)
			
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetFlashEvent(self, index):
			self.interface.PetFlashEvent(index)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetAffectShowerRefresh(self):
			self.interface.PetAffectShowerRefresh()
	
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetEvolInfo(self, index, value):
			self.interface.PetEvolInfo(index, value)
			
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetFeedReuslt(self, result):
			self.interface.PetFeedReuslt(result)
				
	if app.ENABLE_CHANGED_ATTR :
		def OpenSelectAttrDialog(self, window_type, slotIdx) :
			self.interface.OpenSelectAttrDialog(window_type, slotIdx)

	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def ExInvenItemUseMsg(self, item_vnum, msg, enough_count):
			self.interface.ExInvenItemUseMsg(item_vnum, msg, enough_count)
			
			
	def MiniGameStart(self):
		self.interface.MiniGameStart()
	
	def RumiMoveCard(self, src_pos, src_index, src_color, src_number \
				, dst_pos, dst_index, dst_color, dst_number):
		
		srcCard = (src_pos, src_index, src_color, src_number)
		dstCard = (dst_pos, dst_index, dst_color, dst_number)
		self.interface.RumiMoveCard( srcCard, dstCard )
		
	def MiniGameRumiSetDeckCount(self, deck_card_count):
		self.interface.MiniGameRumiSetDeckCount(deck_card_count)
		
	def RumiIncreaseScore(self, score, total_score):
		self.interface.RumiIncreaseScore( score, total_score )
		
	def MiniGameEnd(self):
		self.interface.MiniGameEnd()
			
	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def RefreshGuildRankingList(self, issearch):
			if self.interface:
				self.interface.RefreshGuildRankingList(issearch)
				
	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
		def MiniGameAttendanceSetData(self, type, value):
			self.interface.MiniGameAttendanceSetData( type, value )
			
		def MiniGameAttendanceRequestRewardList(self):
			self.interface.MiniGameAttendanceRequestRewardList()			
			
	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def OpenGuildDragonLairRanking(self,type):
			self.interface.OpenGuildDragonLairRanking(type)
			
		def RefreshGuildDragonLairRanking(self,type):
			self.interface.RefreshGuildDragonLairRanking(type)

		if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
			def SetGuildDragonLairFistGuildText(self, second):
				self.interface.SetGuildDragonLairFistGuildText(second)
			def SetGuildDragonLiarStart(self):
				self.interface.SetGuildDragonLiarStart()
			def SetGuildDragonLiarSuccess(self):
				self.interface.SetGuildDragonLiarSuccess()			
			
	if app.ENABLE_RANKING_SYSTEM:
		def OpenRankingBoard(self, type, category):
			self.interface.OpenRankingBoardWindow(type, category)
			
	if app.ENABLE_MONSTER_CARD:
		def RefreshMissionPage(self):
			self.interface.RefreshMissionPage()
			
		def ReciveMission(self):
			self.interface.ReciveMission()
			
		def MonsterCardMissionFail(self, type, data):
			self.interface.MonsterCardMissionFail(type, data)
			
		def MonsterCardIllustrationFail(self, type, data):
			self.interface.MonsterCardIllustrationFail(type, data)
			
		def MonsterCardIllustrationRefresh(self):
			self.interface.MonsterCardIllustrationRefresh()
	
	if app.ENABLE_BATTLE_FIELD:
		def __BattleFieldInfo(self, enable):
			playerm2g2.SetBattleFieldInfo(int(enable))
		
		def __BattleFieldOpen(self, open):
			playerm2g2.SetBattleFieldOpen(int(open))
			if self.interface:
				self.interface.RefrashBattleButton()
		
		def __BattleFieldEventInfo(self, enable, start, end):
			playerm2g2.SetBattleFieldEventInfo(int(enable), int(start), int(end))
		
		def __BattleFieldEventOpen(self, open):
			playerm2g2.SetBattleFieldEventOpen(int(open))
			if self.interface:
				self.interface.RefrashBattleButton()
		
		def SetBattleFieldLeftTime(self, leftOpen, leftEnd):
			if self.interface:
				self.interface.SetBattleFieldLeftTime(leftOpen, leftEnd)
				
		def ExitBattleField(self, point):
			if self.interface:
				self.interface.ExitBattleField(point)
				
		def ExitBattleFieldOnDead(self, point):
			if self.interface:
				self.interface.ExitBattleFieldOnDead(point)
				
		def ResetUsedBP(self):
			if self.interface:
				self.interface.ResetUsedBP()
				
	if app.ENABLE_FISH_EVENT:
		def MiniGameFishUse(self, window, pos, shape):
			self.interface.MiniGameFishUse( window, pos, shape )
			
		def MiniGameFishAdd(self, pos, shape):
			self.interface.MiniGameFishAdd( pos, shape )
			
		def MiniGameFishReward(self, vnum):
			self.interface.MiniGameFishReward( vnum )
			
		def MiniGameFishCount(self, count):
			self.interface.MiniGameFishCount( count )			
		

	if app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
		def RefreshAccumulateCount(self, vid):
			if vid == self.targetBoard.GetTargetVID():
				self.targetBoard.RefreshAccumulateCount(vid)
				
	if app.ENABLE_MOVE_CHANNEL:
		def __SeverInfo(self, channelNumber, mapIndex):
			#print "__SeverInfo %s %s" % (channelNumber, mapIndex)
			
			_chNum	= int(channelNumber.strip())
			_mapIdx	= int(mapIndex.strip())
			
			if _chNum == 99 or _mapIdx >= 10000:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % 0)
			else:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MOVE_CHANNEL_NOTICE % _chNum)
				
			m2netm2g.SetChannelName(_chNum)
			m2netm2g.SetMapIndex(_mapIdx)
			self.interface.RefreshServerInfo()
			
	if app.ENABLE_PARTY_MATCH:
		def PartyMatchResult(self, type, data):
			self.interface.PartyMatchResult(type, data)
			
		def __PartyMatchOff(self, enable):
			if self.interface:
				self.interface.PartyMatchOff( enable )
				
			chrmgrm2g.SetPartyMatchOff( int(enable) )

	if app.ENABLE_USER_SITUATION_NOTICE:
		def RefreshUserSituation(self):
			if self.interface:
				self.interface.RefreshUserSituation()
		
		def OpenUserSituationShow(self, data):
			if self.interface:
				self.interface.OpenUserSituationShow( data )
				
	if app.ENABLE_EXP_EVENT:
		def __ExpBonusEventStart(self, state_idx, exp_bonus):
			#print "__ExpBonusEventStart %s %s" % (state_idx, type(state_idx))
			
			state = int(state_idx)
			
			if state >= len(self.expEventBonusImageList):
				self.toolTip.SetText("")
				for img in self.expEventBonusImageList:
					img.Hide()
			else:
				self.toolTip.SetText("%s%%"%exp_bonus)
				for i in xrange(len(self.expEventBonusImageList)):
					if i == state:
						self.expEventBonusImageList[i].Show()
					else:
						self.expEventBonusImageList[i].Hide()
						
		def __expEventImageOverIn(self):
			self.toolTip.Show()
		
		def __expEventImageOverOut(self):
			self.toolTip.Hide()
			
	if app.ENABLE_SPECIAL_GACHA:
		def ShowSpecialGachaAward(self, vnum, day, win, cell):
			self.interface.ShowSpecialGachaAward(vnum, day, win, cell)

	if app.ENABLE_REFINE_MSG_ADD:
		def __RefineFailedTypeMessage(self, value):
			snd.PlaySound("sound/ui/jaeryun_fail.wav")
			
			value = int(value)
			print "type : ", value
			print type(value)
			
			if REFINE_FAIL_GRADE_DOWN == value:
				self.PopupMessage(localeInfo.REFINE_FAILURE_GRADE_DOWN)	
			elif REFINE_FAIL_DEL_ITEM == value:
				self.PopupMessage(localeInfo.REFINE_FAILURE_DEL_ITEM)	
			elif REFINE_FAIL_KEEP_GRADE == value:
				self.PopupMessage(localeInfo.REFINE_FAILURE_KEEP_GRADE)	
			else:
				self.PopupMessage(localeInfo.REFINE_FAILURE)	
	
	if app.ENABLE_PVP_TOURNAMENT_GF:
		def InitSkillCoolTime(self):
			for i in range(1, 7):
				self.RunUseSkillEvent(i, 0)
				playerm2g2.SkillCoolTimeInitialize(i)
				
		def __PvPTournamentAutoSet(self, OnOff):
			self.interface.PvPTournamentAutoSet(int(OnOff))
					
	if app.ENABLE_PVP_ONOFF:
		def __PvPOnOff(self, OnOff):
			#print "interface OnOff"
			m2netm2g.SetPvPOnOffControl(int(OnOff))

	if app.ENABLE_MINI_GAME_YUTNORI:
		def YutnoriProcess(self, type, data):
			if self.interface:
				self.interface.YutnoriProcess(type, data)
			