import ui
import uiScriptLocale
import wndMgr
import playerm2g2
import localeInfo
import m2netm2g
import app
import event
import uiCommon
import item

NUMBER_RES_MAX	= 14	# 숫자 리소스 max
NUMBER_PAGE_MAX = 2		# 총2페이지
SHOW_NUMBER_COUNT = 8	# 한페이지당 8개 노출
DEFAULT_SHOW_NUMBER_MAX = 14	# 총 14번까지 노출

ROOT_PATH = "d:/ymir work/ui/minigame/attendance/"

SHOW_LINE_COUNT_MAX = 7
DEFAULT_DESC_Y	= 7

class MiniGameAttendance(ui.ScriptWindow):
			
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet( self.descIndex )
			
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded		= 0
		self.cur_page		= 0
		self.number_button	= [None]
		self.number_effect  = None
		self.number_board	= None
		self.popup			= None
		self.prev_button	= None
		self.next_button	= None
		
		self.cur_attendance_number	= 0
		self.cur_effect_number		= 0
		self.mission_clear			= 0
		self.get_reward				= 0
		self.reward_dict			= {}
		self.show_max				= DEFAULT_SHOW_NUMBER_MAX
		
		##desc
		self.descBoard		= None
		self.descriptionBox	= None
		self.descIndex		= 0
		self.desc_y			= DEFAULT_DESC_Y
		
		self.reward_question_dialog = None
		
		##
		self.tooltipitem	= None
		self.show_tooltip	= False
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.isLoaded		= 0
		self.cur_page		= 0
		self.number_button	= [None]
		self.number_effect  = None
		self.number_board	= None
		self.popup			= None
		self.prev_button	= None
		self.next_button	= None
		
		self.cur_attendance_number	= 0
		self.cur_effect_number		= 0
		self.mission_clear			= 0
		self.get_reward				= 0
		self.reward_dict			= {}
		self.show_max				= DEFAULT_SHOW_NUMBER_MAX
		
		##desc
		self.descBoard		= None
		self.descriptionBox	= None
		self.descIndex		= 0
		self.desc_y			= DEFAULT_DESC_Y
		
		##
		self.tooltipitem	= None
		self.show_tooltip	= False
		
		self.Close()
		
	def SetItemToolTip(self, tooltip):
		self.tooltipitem = tooltip
		
	def __LoadWindow(self):
		
		if self.isLoaded == 1:
			return
		
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/MiniGameAttendance.py")
			
		except:
			import exception
			exception.Abort("MiniGameAttendance.LoadWindow")
		
		try:
			## close
			self.GetChild("titlebar").SetCloseEvent( ui.__mem_func__(self.Close) )
			
			## number boaard
			self.number_board = self.GetChild("number_board_window")
			
			if localeInfo.IsARABIC():
				self.GetChild("LeftTop").LeftRightReverse()
				self.GetChild("RightTop").LeftRightReverse()
				self.GetChild("LeftBottom").LeftRightReverse()
				self.GetChild("RightBottom").LeftRightReverse()
				self.GetChild("LeftCenterImg").LeftRightReverse()
				self.GetChild("RightCenterImg").LeftRightReverse()
				self.topcenterimg = self.GetChild("TopCenterImg")
				self.topcenterimg.SetPosition(self.GetWidth() - (self.topcenterimg.GetWidth()*2), 0)
				
				self.bottomcenterImg = self.GetChild("BottomCenterImg")
				self.bottomcenterImg.SetPosition(self.GetWidth() - (self.bottomcenterImg.GetWidth()*2), 155)

				self.centerImg = self.GetChild("CenterImg")
				self.centerImg.SetPosition(self.GetWidth() - (self.centerImg.GetWidth()*2) , 16)
			
			## number effect
			self.number_effect = self.GetChild("number_effect")
			self.number_effect.Hide()
			
			## number button setting
			## 1 ~ (8 * 2 + 1)
			for number in range(1, SHOW_NUMBER_COUNT * NUMBER_PAGE_MAX + 1):
				if number > NUMBER_RES_MAX:
					self.number_button.append( None )
				else:
					strNumber = str(number)
					button = self.GetChild("disable_number_button" + strNumber)
					full_path = ROOT_PATH + "attendance_disable_number" + strNumber + ".sub"
					button.SetDisableVisual(full_path)
					button.SAFE_SetEvent(self.__OnClickNumberButton, number)
					button.Hide()
					self.number_button.append( button )

			## number prev button func link
			self.prev_button = self.GetChild("prev_button")
			self.prev_button.SAFE_SetEvent(self.__OnClickPrevButton)
			self.prev_button.Hide()
			## number next button func link
			self.next_button = self.GetChild("next_button")
			self.next_button.SAFE_SetEvent(self.__OnClickNextButton)
			self.next_button.Hide()
			
			if localeInfo.IsARABIC():
				self.prev_button.LeftRightReverse()
				self.next_button.LeftRightReverse()
			
			## desc prev button func link
			self.desc_prev_button = self.GetChild("desc_prev_button")
			self.desc_prev_button.SAFE_SetEvent(self.__OnClickDescPrevButton)
			## desc next button func link
			self.desc_next_button = self.GetChild("desc_next_button")
			self.desc_next_button.SAFE_SetEvent(self.__OnClickDescNextButton)
			
			if localeInfo.IsARABIC():
				self.desc_prev_button.LeftRightReverse()
				self.desc_next_button.LeftRightReverse()
				
			## desc
			self.descBoard		= self.GetChild("desc_board")
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Show()
			
			## number board refresh
			self.RefreshAttendanceBoard()
			self.__NumberFlash( self.cur_effect_number )
			
		except:
			import exception
			exception.Abort("MiniGameAttendance.LoadWindow.BindObject")
			
		m2netm2g.SendMiniGameAttendanceRequestRewardList()
		m2netm2g.SendMiniGameAttendanceRequestData( playerm2g2.ATTENDANCE_DATA_TYPE_DAY )
		m2netm2g.SendMiniGameAttendanceRequestData( playerm2g2.ATTENDANCE_DATA_TYPE_MISSION_CLEAR )
		m2netm2g.SendMiniGameAttendanceRequestData( playerm2g2.ATTENDANCE_DATA_TYPE_GET_REWARD )
		m2netm2g.SendMiniGameAttendanceRequestData( playerm2g2.ATTENDANCE_DATA_TYPE_SHOW_MAX )
		
		self.Hide()
		self.isLoaded	= 1
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
			
	def Open(self):
			
		if self.IsShow():
			self.Close()
		else:
			self.Show()
			self.SetTop()
			
			
	def Close(self):
		self.Hide()
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = -1
		
		if self.descriptionBox:
			self.descriptionBox.Hide()
						
		self.desc_y = DEFAULT_DESC_Y
		
		if self.tooltipitem:
			self.tooltipitem.HideToolTip()
			
	def Show(self):
		self.__LoadWindow()
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet( uiScriptLocale.ATTENDANCE_DESC )
		
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
			
		event.SetVisibleLineCount(self.descIndex, SHOW_LINE_COUNT_MAX)
		
		if localeInfo.IsARABIC():
			event.SetEventSetWidth(self.descIndex, self.descBoard.GetWidth() - 20)

		event.SetRestrictedCount(self.descIndex, 50)
		event.AllProcesseEventSet(self.descIndex)
		event.Skip(self.descIndex)
		
		if self.descriptionBox:
			self.descriptionBox.Show()
			
		if not self.reward_dict:
			m2netm2g.SendMiniGameAttendanceRequestRewardList()
			
		ui.ScriptWindow.Show(self)
 
		
	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + 7, -(yposEventSet + self.desc_y))
		self.descriptionBox.SetIndex(self.descIndex)
		
		## 숫자 버튼 Over 체크
		self.NumberButtonOverCheck()
		
		
	def NumberButtonOverCheck(self):
	
		if not self.tooltipitem:
			return
			
		if not self.reward_dict:
			return
			
		if not self.number_board.IsIn():
			if self.show_tooltip:
				self.tooltipitem.HideToolTip()
				self.show_tooltip = False
							
		isin = False
		
		for number in range(1, SHOW_NUMBER_COUNT * NUMBER_PAGE_MAX + 1):
			if number > NUMBER_RES_MAX:
				break
			elif number > self.show_max:
				break
			
			if self.number_button[number].IsIn():
				if self.tooltipitem:
					if self.reward_dict.has_key(number):
						(item_vnum, item_count) = self.reward_dict[number]
						self.tooltipitem.SetAttendanceRewardItem( item_vnum )
						self.show_tooltip = True
						isin = True
						break
				
		if self.number_board.IsIn() and False == isin:
			self.tooltipitem.HideToolTip()
			self.show_tooltip = False
			
		
	## 날짜 set
	def MiniGameAttendanceSetDay(self, day):
		self.cur_attendance_number = day + 1
	## 오늘 mission clear 여부
	def MiniGameAttendanceSetMissionClear(self, clear):
		self.mission_clear = clear
	## reward 여부
	def MiniGameAttendanceSetReward(self, reward):
		self.get_reward = reward
	## reward list
	def MiniGameAttendanceRequestRewardList(self):
		self.reward_dict = item.GetAttendanceRewardList()
	## 출석 이벤트 기간
	def MiniGameAttendanceSetShowMax(self, value ):
		self.show_max = value
		
		
	## 갱신
	def RefreshAttendanceBoard(self):
	
		for number in range(1, SHOW_NUMBER_COUNT * NUMBER_PAGE_MAX + 1):
			if number > NUMBER_RES_MAX:
				break
			else:
				if number < self.cur_attendance_number:
					strNumber = str(number)
					full_path = "d:/ymir work/ui/minigame/attendance/attendance_close_button.sub"
					self.number_button[number].SetUpVisual( full_path )
					self.number_button[number].SetOverVisual( full_path )
					self.number_button[number].SetDownVisual( full_path )
					self.number_button[number].Enable()
					
				elif number == self.cur_attendance_number:
					
					if self.mission_clear and self.get_reward:
						strNumber = str(number)
						full_path = "d:/ymir work/ui/minigame/attendance/attendance_close_button.sub"
						self.number_button[number].SetUpVisual( full_path )
						self.number_button[number].SetOverVisual( full_path )
						self.number_button[number].SetDownVisual( full_path )
						self.number_button[number].Enable()
					else:
						## 같으면 파란색으로
						strNumber = str(number)
						full_path = ROOT_PATH + "attendance_enable_number" + strNumber + ".sub"
						self.number_button[number].SetUpVisual( full_path )
						self.number_button[number].SetOverVisual( full_path )
						self.number_button[number].SetDownVisual( full_path )
						self.number_button[number].Enable()
				else:
					self.number_button[number].Disable()
					
				
		if self.cur_attendance_number > SHOW_NUMBER_COUNT:
			self.cur_page = 1
 
		## 보여질 숫자 처리
		self.__HideAllNumber()
		self.__ShowCurPageNumber()
		
		## effect
		if self.mission_clear and not self.get_reward:
			self.__NumberFlash( self.cur_attendance_number )
		else:
			self.__NumberFlash(0)
			
		## prev, next button
		if self.prev_button and self.next_button:
			if self.show_max > SHOW_NUMBER_COUNT:
				self.prev_button.Show()
				self.next_button.Show()
			else:
				self.prev_button.Hide()
				self.next_button.Hide()
		
	def __HideAllNumber(self):
		for number in range(1, SHOW_NUMBER_COUNT * NUMBER_PAGE_MAX + 1):
			if number > NUMBER_RES_MAX:
				break
			else:
				self.number_button[number].Hide()
				
	def __ShowCurPageNumber(self):
		## 현재 화면에 보여줄 숫자만 계산
		min_range = self.cur_page * SHOW_NUMBER_COUNT + 1
		max_range = (self.cur_page + 1) * SHOW_NUMBER_COUNT + 1
		
		for number in range(min_range, max_range):
			if number > NUMBER_RES_MAX:
				continue
			elif number > self.show_max:
				continue
			else:
				self.number_button[number].Show()
				
	def __NumberFlash(self, number):
	
		if not self.number_effect:
			return
			
		self.number_effect.Hide()
	
		if number > self.show_max or number < 1:
			return
		
		min_range = self.cur_page * SHOW_NUMBER_COUNT + 1
		max_range = (self.cur_page + 1) * SHOW_NUMBER_COUNT + 1
		
		if number < min_range or number > max_range:
			return
			
		(x, y) = self.number_button[number].GetLocalPosition()
		
		self.number_effect.SetPosition(x,y)
		self.number_effect.ResetFrame()
		self.number_effect.Show()
	
	def __OnClickPrevButton(self):
		temp_page = self.cur_page
		self.cur_page -= 1
		if self.cur_page < 0:
			self.cur_page = 0
			
		if temp_page == self.cur_page:
			return
	
		self.__HideAllNumber()
		self.__ShowCurPageNumber()
		if self.mission_clear and not self.get_reward:
			self.__NumberFlash( self.cur_attendance_number )
		else:
			self.__NumberFlash(0)
		
	def __OnClickNextButton(self):
		temp_page = self.cur_page
		self.cur_page += 1
		if self.cur_page >= NUMBER_PAGE_MAX:
			self.cur_page = NUMBER_PAGE_MAX - 1
			
		if temp_page == self.cur_page:
			return
			
		self.__HideAllNumber()
		self.__ShowCurPageNumber()
		if self.mission_clear and not self.get_reward:
			self.__NumberFlash( self.cur_attendance_number )
		else:
			self.__NumberFlash(0)
		
		
	def __OnClickNumberButton(self, index):
		if self.cur_attendance_number != index:
			return
			
		if self.get_reward:
			# 이미 보상을 받았습니다.
			# 문구 제거
			#self.OpenPopupDialog(localeInfo.ATTENDANCE_ALREADY_RECEIVE)
			return
			
		if not self.mission_clear:
			return 
		
		if None == self.reward_question_dialog:
			self.reward_question_dialog = uiCommon.QuestionDialog()
			self.reward_question_dialog.SetText( localeInfo.ATTENDANCE_REWARD_QUESTION )
			self.reward_question_dialog.SetAcceptEvent(ui.__mem_func__(self.__RewardAccept))
			self.reward_question_dialog.SetCancelEvent(ui.__mem_func__(self.__RewardCancel))
			w,h = self.reward_question_dialog.GetTextSize()
			self.reward_question_dialog.SetWidth( w + 60 )
			line_count = self.reward_question_dialog.GetTextLineCount()
			
			if line_count > 1:
				height = self.reward_question_dialog.GetLineHeight()
				self.reward_question_dialog.SetLineHeight(height + 3)
				
		self.reward_question_dialog.Open()
		
	def __RewardAccept(self):
		m2netm2g.SendMiniGameAttendanceButtonClick(self.cur_attendance_number)
		self.__RewardCancel()
		
	def __RewardCancel(self):
		if self.reward_question_dialog:
			self.reward_question_dialog.Close()
		
	def __OnClickDescPrevButton(self):
	
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		decrease_count = SHOW_LINE_COUNT_MAX
		
		if cur_start_line - decrease_count < 0:
			return;

		event.SetVisibleStartLine(self.descIndex, cur_start_line - decrease_count)
		self.desc_y += ( line_height * decrease_count )
		
	def __OnClickDescNextButton(self):
	
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		total_line_count	= event.GetProcessedLineCount(self.descIndex)
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		increase_count = SHOW_LINE_COUNT_MAX
		
		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return
		
		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.desc_y -= ( line_height * increase_count )
		
		
	def OpenPopupDialog(self, msg):
	
		if not self.popup:
			self.popup = uiCommon.PopupDialog()

		self.popup.SetText(msg)
		self.popup.Open()