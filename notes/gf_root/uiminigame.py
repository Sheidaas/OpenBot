import ui
import uiScriptLocale
import wndMgr
import playerm2g2
import localeInfo
import m2netm2g
import app
import constInfo

import uiMiniGameRumi

if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
	import uiMiniGameAttendance
	
if app.ENABLE_FISH_EVENT:
	import uiMiniGameFishEvent

if app.ENABLE_MINI_GAME_YUTNORI:
	import uiMiniGameYutnori
	
MINIGAME_TYPE_RUMI	= playerm2g2.MINIGAME_TYPE_RUMI
MINIGAME_TYPE_MAX	= playerm2g2.MINIGAME_TYPE_MAX

if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
	MINIGAME_ATTENDANCE = playerm2g2.MINIGAME_ATTENDANCE
	
if app.ENABLE_FISH_EVENT:
	MINIGAME_FISH = playerm2g2.MINIGAME_FISH

if app.ENABLE_MONSTER_BACK:
	MINIGAME_MONSTERBACK = playerm2g2.MINIGAME_MONSTERBACK
	
if app.ENABLE_MINI_GAME_YUTNORI:
	MINIGAME_YUTNORI	= playerm2g2.MINIGAME_YUTNORI
	
RUMI_ROOT = "d:/ymir work/ui/minigame/rumi/"



if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:

	button_gap		= 10	## 버튼과 버튼 사이 공간
	button_height	= 25
	
	class MiniGameDialog(ui.ScriptWindow):

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.isLoaded = 0
			
			self.board			= None
			self.close_button	= None
			
			self.button_dict	= {}
			
			self.__LoadWindow()
			
		def __del__(self):
			ui.ScriptWindow.__del__(self)
			self.Destroy()
			
		def Destroy(self):
			self.isLoaded = 0
			
			self.board			= None
			self.close_button	= None
			
			self.button_dict	= {}
			
		def Show(self):
			self.__LoadWindow()
			ui.ScriptWindow.Show(self)
			        
		def Close(self):
			self.Hide()
			
		def OnPressEscapeKey(self):
			self.Close()
			return True
			
		def __LoadWindow(self):
		
			if self.isLoaded == 1:
				return
			
			self.isLoaded = 1
			
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/MiniGameDialog.py")
			except:
				import exception
				exception.Abort("MiniGameDialog.LoadWindow.LoadObject")
				
			
			try:
				self.board			= self.GetChild("board")
				self.close_button	= self.GetChild("close_button")
				self.close_button.SetEvent( ui.__mem_func__(self.Close) )

			except:
				import exception
				exception.Abort("MiniGameDialog.LoadWindow.BindObject")
			
			self.Hide()
			
			
		def AppendButton(self, name, func):
		
			if self.button_dict.has_key(name):
				return
		
			button = ui.Button()
			button.SetParent( self.board )
			button_count = len(self.button_dict)
			pos_y = (button_gap * (button_count + 1)) + button_count * button_height
			button.SetPosition( 10, pos_y )
			button.SetUpVisual( "d:/ymir work/ui/public/XLarge_Button_01.sub" )
			button.SetOverVisual( "d:/ymir work/ui/public/XLarge_Button_02.sub" )
			button.SetDownVisual( "d:/ymir work/ui/public/XLarge_Button_03.sub" )
			
			if name:
				button.SetText(name)
			
			if func: 
				button.SetEvent( ui.__mem_func__(func) )
				
			button.Show()
			self.button_dict[name] = button
			
		def DeleteButton(self, name):
		
			if not self.button_dict.has_key(name):
				return
				
			self.button_dict[name].Hide()
			del self.button_dict[name]
			
		def DeleteAllButton(self):
			
			for button in self.button_dict.values():
				button.Hide()
				del button
				
			self.button_dict.clear()
					
		def RefreshDialog(self):
			## board 의 height 값 계산
			## self.button_dict 에는 close 버튼이 포함되어 있지 않기 때문에 + 1 해준다.
			total_len = len(self.button_dict) + 1
			board_height = (button_height * total_len) + (button_gap * (total_len + 1))
			self.board.SetSize(200, board_height)
			self.SetSize(200, board_height)
			
			## close 버튼의 위치 갱신
			dict_len = len(self.button_dict)
			pos_y = (button_gap * (dict_len + 1)) + dict_len * button_height
			
			if localeInfo.IsARABIC():
				(lx,ly) = self.close_button.GetLocalPosition()
				self.close_button.SetPosition( lx, pos_y )
			else:
				self.close_button.SetPosition( 10, pos_y )
			
# Mini Game Button Area
class MiniGameWindow(ui.ScriptWindow):

	def __init__(self):
		
		self.isLoaded = 0
		self.main_game = None
		self.rumi_game = None
		
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			self.attendance_game = None
		
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:
			self.mini_game_dialog = None
			self.isshow_mini_game_dialog = False
			
		if app.ENABLE_FISH_EVENT:
			self.inven		= None
			self.interface	= None
			self.fish_game	= None
			
		if app.ENABLE_MINI_GAME_YUTNORI:
			self.yutnori_game	= None
			
		self.game_type = MINIGAME_TYPE_MAX
		self.tooltipitem = None
		
		ui.ScriptWindow.__init__(self)
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:
			if self.mini_game_dialog and self.isshow_mini_game_dialog:
				self.mini_game_dialog.Show()
		        
	def Close(self):
		self.Hide()
		
	def Hide(self):
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:
			if self.mini_game_dialog:
				self.isshow_mini_game_dialog = self.mini_game_dialog.IsShow()
				self.mini_game_dialog.Hide()
		
		wndMgr.Hide(self.hWnd)
		
	def Destroy(self):
		self.isLoaded = 0
		
		self.main_game = None		
		
		if self.rumi_game:
			self.rumi_game.Destroy()
			self.rumi_game = None
			
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if self.attendance_game:
				self.attendance_game.Destroy()
				self.attendance_game = None
				
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:
			if self.mini_game_dialog:
				self.mini_game_dialog.Destroy()
				self.mini_game_dialog = None
				
		if app.ENABLE_FISH_EVENT:
			if self.fish_game:
				self.fish_game.Destroy()
				self.fish_game = None
			self.inven		= None
			self.interface	= None
			
		if app.ENABLE_MINI_GAME_YUTNORI:
			if self.yutnori_game:
				self.yutnori_game.Destroy()
				self.yutnori_game = None
				
		self.game_type = MINIGAME_TYPE_MAX
		self.tooltipitem = None
		
	def SetItemToolTip(self, tooltip):
		self.tooltipitem = tooltip
		
	def __LoadWindow(self):
		
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			self.__LoadScript("UIScript/MiniGameWindow.py")
			
		except:
			import exception
			exception.Abort("MiniGameWindow.LoadWindow.LoadObject")
			
		try:
			## 2015 크리스마스 이벤트 미니게임 Okey
			self.minigame_rumi_button = self.GetChild("minigame_rumi_button")
			self.minigame_rumi_button.SetEvent( ui.__mem_func__(self.__ClickRumiButton) )
			self.minigame_rumi_button.Hide()
			
			self.minigame_rumi_button_effect = self.GetChild("minigame_rumi_button_effect")
			self.minigame_rumi_button_effect.Hide()
			
			if localeInfo.IsARABIC():
				mini_game_window  = self.GetChild("mini_game_window")
				window_width	  = mini_game_window.GetWidth()
				rumi_button_width = self.minigame_rumi_button.GetWidth()
				adjust_pos_x = window_width - rumi_button_width
				(lx,ly) = self.minigame_rumi_button.GetLocalPosition()
				## 버튼 위치 조정
				self.minigame_rumi_button.SetPosition( lx + adjust_pos_x, 0 )
				## 이팩트 위치 조정
				self.minigame_rumi_button_effect.SetWindowHorizontalAlignLeft()
		except:
			import exception
			exception.Abort("MiniGameWindow.LoadWindow.Okey.BindObject")


		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT:
			try:
				mini_game_window = self.GetChild("mini_game_window")
				self.event_banner_button = ui.Button()
				self.event_banner_button.SetParent( mini_game_window )
				self.event_banner_button.SetPosition(0, 0)
				self.event_banner_button.SetUpVisual("d:/ymir work/ui/minigame/banner.sub")
				self.event_banner_button.SetOverVisual("d:/ymir work/ui/minigame/banner.sub")
				self.event_banner_button.SetDownVisual("d:/ymir work/ui/minigame/banner.sub")
				self.event_banner_button.SetEvent( ui.__mem_func__(self.__ClickIntegrationEventBannerButton) )
				self.event_banner_button.Hide()
				self.event_banner_button_enable = False
			
			except:
				import exception
				exception.Abort("MiniGameWindow.LoadWindow.EventBannerButton.BindObject")
			
			try:
				## Mini Game Integration Event Button Dialog	
				self.mini_game_dialog = MiniGameDialog()
				self.mini_game_dialog.Hide()
			except:
				import exception
				exception.Abort("MiniGameWindow.LoadWindow.MiniGameDialog")
				
		self.Show()
		
	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)
		
	
	def MiniGameOkeyEvent(self, enable):
	
		if enable:
			self.minigame_rumi_button.Show()	
		else:
			self.minigame_rumi_button.Hide()
			self.minigame_rumi_button_effect.Hide()
			
		if self.rumi_game:
			self.rumi_game.Destroy()
			self.rumi_game = None
			
		if self.game_type == MINIGAME_TYPE_RUMI:
			self.main_game = None
		

	def __ClickRumiButton(self):
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			self.__CloseAll( MINIGAME_TYPE_RUMI )
			
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT:
			if self.mini_game_dialog:
				self.mini_game_dialog.Close()
		
		if not self.rumi_game:
			self.rumi_game = uiMiniGameRumi.MiniGameRumi()
		
		self.main_game = self.rumi_game
		self.game_type = MINIGAME_TYPE_RUMI
		self.main_game.Open()
			
	def MiniGameStart(self):
	
		if not self.main_game:
			return
		
		self.minigame_rumi_button.SetUpVisual( RUMI_ROOT + "rumi_button_max.sub" )
		self.minigame_rumi_button.SetOverVisual( RUMI_ROOT + "rumi_button_max.sub" )
		self.minigame_rumi_button.SetDownVisual( RUMI_ROOT + "rumi_button_max.sub" )
		
		if not app.ENABLE_MINI_GAME_OKEY_NORMAL:
			if self.minigame_rumi_button_effect:
				self.minigame_rumi_button_effect.ResetFrame()
				self.minigame_rumi_button_effect.Show()
		
		self.main_game.GameStart()
		
	def	MiniGameEnd(self):
		
		if not self.main_game:
			return
		
		self.minigame_rumi_button.SetUpVisual( RUMI_ROOT + "rumi_button_min.sub" )
		self.minigame_rumi_button.SetOverVisual( RUMI_ROOT + "rumi_button_min.sub" )
		self.minigame_rumi_button.SetDownVisual( RUMI_ROOT + "rumi_button_min.sub" )
		
		if not app.ENABLE_MINI_GAME_OKEY_NORMAL:
			if self.minigame_rumi_button_effect:
				self.minigame_rumi_button_effect.Hide()
				
		self.main_game.GameEnd()
		
		
		
	def RumiMoveCard(self, srcCard, dstCard):
		
		if MINIGAME_TYPE_RUMI != self.game_type:
			return
			
		self.main_game.RumiMoveCard( srcCard, dstCard )	
		
	def MiniGameRumiSetDeckCount(self, deck_card_count):
		
		if MINIGAME_TYPE_RUMI != self.game_type:
			return
			
		self.main_game.SetDeckCount(deck_card_count)
		
	def RumiIncreaseScore(self, score, total_score):
		
		if MINIGAME_TYPE_RUMI != self.game_type:
			return
			
		self.main_game.RumiIncreaseScore(score, total_score)
		
	

	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			
		def MiniGameAttendance(self, enable):

			if enable:
				if self.attendance_button:
					self.attendance_button.Show()
			else:
				if self.attendance_button:
					self.attendance_button.Hide()
				
			if self.attendance_game:
				self.attendance_game.Destroy()
				self.attendance_game = None
				
			if self.game_type == MINIGAME_ATTENDANCE:
				self.main_game = None
			
		def __ClickAttendanceButton(self):
			
			if app.ENABLE_MINI_GAME_OKEY_NORMAL:
				self.__CloseAll( MINIGAME_ATTENDANCE )

			if self.mini_game_dialog:
				self.mini_game_dialog.Close()
		
			if not self.attendance_game:
				self.attendance_game = uiMiniGameAttendance.MiniGameAttendance()
				
				if self.tooltipitem:
					self.attendance_game.SetItemToolTip( self.tooltipitem )
			
			self.main_game = self.attendance_game
			self.game_type = MINIGAME_ATTENDANCE
			self.main_game.Open()
			
		def MiniGameAttendanceSetData(self, type, value):
			if MINIGAME_ATTENDANCE != self.game_type:
				return
				
			if not self.main_game:
				return

			if type == playerm2g2.ATTENDANCE_DATA_TYPE_DAY:
				self.main_game.MiniGameAttendanceSetDay( value )
			elif type == playerm2g2.ATTENDANCE_DATA_TYPE_MISSION_CLEAR:
				self.main_game.MiniGameAttendanceSetMissionClear( value )
			elif type == playerm2g2.ATTENDANCE_DATA_TYPE_GET_REWARD:
				self.main_game.MiniGameAttendanceSetReward( value )
			elif type == playerm2g2.ATTENDANCE_DATA_TYPE_SHOW_MAX:
				self.main_game.MiniGameAttendanceSetShowMax( value )
				
			self.main_game.RefreshAttendanceBoard()
			
			
		def MiniGameAttendanceRequestRewardList(self):
		
			if MINIGAME_ATTENDANCE != self.game_type:
				return
				
			if not self.main_game:
				return
				
			self.main_game.MiniGameAttendanceRequestRewardList()
			
			
	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or ENABLE_MINI_GAME_YUTNORI:
		def __ClickIntegrationEventBannerButton(self):
		
			if not self.mini_game_dialog:
				return
				
			if self.mini_game_dialog.IsShow():
				self.mini_game_dialog.Close()
			else:			
				self.mini_game_dialog.Show()
				
		def IntegrationMiniGame(self, enable):
			
			if enable:
				self.event_banner_button.Show()	
				self.event_banner_button_enable = True
			else:
				self.event_banner_button.Hide()
				self.event_banner_button_enable = False
					
			if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
				if self.attendance_game:
					self.attendance_game.Destroy()
					self.attendance_game = None
				
			if app.ENABLE_MINI_GAME_OKEY_NORMAL:
				if self.rumi_game:
					self.rumi_game.Destroy()
					self.rumi_game = None
					
			if app.ENABLE_FISH_EVENT:
				if self.fish_game:
					self.fish_game.Destroy()
					self.fish_game = None
			
			if app.ENABLE_MINI_GAME_YUTNORI:
				if self.yutnori_game:
					self.yutnori_game.Destroy()
					self.yutnori_game = None
							
			if self.mini_game_dialog:
			
				self.mini_game_dialog.DeleteAllButton()
				
				if False == enable:
					self.mini_game_dialog.Hide()
				else:
					if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
						if playerm2g2.GetAttendance():
							self.mini_game_dialog.AppendButton(uiScriptLocale.BANNER_ATTENDANCE_BUTTON, self.__ClickAttendanceButton)
					if app.ENABLE_MONSTER_BACK and app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
						if playerm2g2.GetMonsterBackEvent():
							self.mini_game_dialog.AppendButton(uiScriptLocale.BANNER_MONSTERBACK_BUTTON, self.__ClickMonsterBackButton)
					if app.ENABLE_MINI_GAME_OKEY_NORMAL:
						if playerm2g2.GetMiniGameWindowOpen():
							self.mini_game_dialog.AppendButton(uiScriptLocale.BANNER_OKEY_BUTTON, self.__ClickRumiButton)
					if app.ENABLE_FISH_EVENT:
						if playerm2g2.GetFishEventGame():
							self.mini_game_dialog.AppendButton(uiScriptLocale.BANNER_FISH_BUTTON, self.__ClickFishEventButton)
					if app.ENABLE_MINI_GAME_YUTNORI:
						if playerm2g2.GetYutnoriGame():
							self.mini_game_dialog.AppendButton(uiScriptLocale.BANNER_YUTNORI_BUTTON, self.__ClickYutnoriButton)
									
				self.mini_game_dialog.RefreshDialog()
				
				self.game_type = MINIGAME_TYPE_MAX
				self.main_game = None
			
	if app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:
		def __CloseAll(self, except_game = MINIGAME_TYPE_MAX):
		
			if self.rumi_game and except_game != MINIGAME_TYPE_RUMI:
				self.rumi_game.Close()
				
			if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
				if self.attendance_game and except_game != MINIGAME_ATTENDANCE:
					self.attendance_game.Close()
					
			if app.ENABLE_FISH_EVENT:
				if self.fish_game and except_game != MINIGAME_FISH:
					self.fish_game.Close()
				
			if app.ENABLE_MINI_GAME_YUTNORI:
				if self.yutnori_game and except_game != MINIGAME_YUTNORI:
					self.yutnori_game.Close()
						
		def SetOkeyNormalBG(self):
			if not self.rumi_game:
				return
				
			self.rumi_game.SetOkeyNormalBG()

	if app.ENABLE_FISH_EVENT:
		def SetInven(self, inven):
			self.inven = inven
		def BindInterface(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)
			
		def CantFishEventSlot(self, InvenSlot):
			ItemVnum = playerm2g2.GetItemIndex(InvenSlot)
			if ItemVnum in [25106, 25107]:
				return False
					
			return True
			#if not self.fish_game:
			#	return True
				
			#return self.fish_game.CantFishEventSlot( InvenSlot )
			
		def __ClickFishEventButton(self):
			self.__CloseAll( MINIGAME_FISH )
				
			if self.mini_game_dialog:
				self.mini_game_dialog.Close()
			
			if not self.fish_game:
				self.fish_game = uiMiniGameFishEvent.MiniGameFish()
				self.fish_game.SetInven( self.inven )
				self.fish_game.BindInterface( self.interface )
				
				if self.tooltipitem:
					self.fish_game.SetItemToolTip( self.tooltipitem )
					
			self.main_game = self.fish_game
			self.game_type = MINIGAME_FISH
			self.main_game.Open()

		def MiniGameFishUse(self, window, pos, shape):			
			if MINIGAME_FISH != self.game_type:
				return
				
			if not self.fish_game:
				return
				
			self.fish_game.MiniGameFishUse( window, pos, shape )
			
		def MiniGameFishAdd(self, pos, shape):
			
			if MINIGAME_FISH != self.game_type:
				return
				
			if not self.fish_game:
				return
				
			self.fish_game.MiniGameFishAdd( pos, shape )
			
		def MiniGameFishReward(self, vnum):
		
			if MINIGAME_FISH != self.game_type:
				return
				
			if not self.fish_game:
				return
				
			self.fish_game.MiniGameFishReward( vnum )
			
		def MiniGameFishCount(self, count):
		
			if MINIGAME_FISH != self.game_type:
				return
				
			if not self.fish_game:
				return
				
			self.fish_game.MiniGameFishCount( count )
			
	if app.ENABLE_MONSTER_BACK:
		def __ClickMonsterBackButton(self):
			self.__CloseAll()
			if self.mini_game_dialog:
				self.mini_game_dialog.Close()
				
			m2netm2g.SendRequestEventQuest("e_monsterback")
			self.main_game = None
			self.game_type = MINIGAME_TYPE_MAX
	
	if app.ENABLE_MINI_GAME_YUTNORI:	
		def __ClickYutnoriButton(self):
			self.__CloseAll( MINIGAME_YUTNORI )
				
			if self.mini_game_dialog:
				self.mini_game_dialog.Close()
			
			if not self.yutnori_game:
				self.yutnori_game = uiMiniGameYutnori.MiniGameYutnori()
									
			self.main_game = self.yutnori_game
			self.game_type = MINIGAME_YUTNORI
			self.main_game.Open()
			
		def YutnoriProcess(self, type, data):
		
			if MINIGAME_YUTNORI != self.game_type:
				return
				
			if not self.yutnori_game:
				return
				
			self.yutnori_game.YutnoriProcess( type, data )
					
	def hide_mini_game_dialog(self):
		if self.event_banner_button:
			if self.event_banner_button.IsShow():
				self.event_banner_button.Hide()
		
		if self.mini_game_dialog:
			if self.mini_game_dialog.IsShow():
				self.mini_game_dialog.Hide()
			
	def show_mini_game_dialog(self):
		if self.event_banner_button:
			if self.event_banner_button_enable:
				self.event_banner_button.Show()		
			