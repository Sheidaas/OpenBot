import os
import ui
import app
import localeInfo
import constInfo
import ime
import wndMgr
import grp
import interfaceModule
import playerm2g2
import m2netm2g
import chrmgrm2g
import uiCommon

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = False
SCREENSHOT_DIR = None

if localeInfo.IsEUROPE():
	SCREENSHOT_CWDSAVE = True

if localeInfo.IsCIBN10():
	SCREENSHOT_CWDSAVE = False
	SCREENSHOT_DIR = "YT2W"

class SelectTextSlot(ui.ImageBox):
	def __init__(self, x, y, keyslotmax):
		ui.ImageBox.__init__(self)
		self.SetPosition(x, y)
		self.LoadImage("d:/ymir work/ui/public/Parameter_Slot_03.sub")
		self.mouseReflector = MouseReflector(self)
		self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())
		self.Enable = False
		self.textLine = ui.MakeTextLine(self)
		self.OnMouseLeftButtonDownEvent = lambda *arg: None
		self.Show()
		self.SlotNumber = keyslotmax + 1
		self.mouseReflector.UpdateRect()
		self.DontUsingSlot = False

	def __del__(self):
		ui.ImageBox.__del__(self)
		
	def SetEvent(self, event):
		self.OnMouseLeftButtonDownEvent = event

	def SetText(self, text):
		self.textLine.SetText(text)
		if text =="":
			self.mouseReflector.SetEmpty(True)
			self.mouseReflector.Show()
		else:
			self.mouseReflector.SetEmpty(False)
			self.mouseReflector.Hide()
	
	def GetSlotNumber(self):
		return self.SlotNumber

	def GetText(self):
		self.textLine.GetText()

	def Disable(self):
		self.DontUsingSlot = True
	
	def GetAble(self):
		return self.Enable
	
	def GetSlotNumber(self):
		return self.SlotNumber
	
	def EmptySlotShow(self):
		if self.mouseReflector.GetEmpty():
			self.mouseReflector.Show()

	def OnMouseOverIn(self):
		if self.Enable or self.DontUsingSlot:
			return
		self.mouseReflector.Show()

		if self.mouseReflector.GetEmpty():
			self.mouseReflector.SetEmptyOverIn(True)

	def OnMouseOverOut(self):

		self.mouseReflector.SetEmptyOverIn(False)

		if self.Enable or self.DontUsingSlot:
			return
			
		if not self.mouseReflector.GetEmpty():
			self.mouseReflector.Hide()

	def OnMouseLeftButtonDown(self):
		if self.Enable or self.DontUsingSlot:
			return

		self.SlotNumber = self.OnMouseLeftButtonDownEvent(self.SlotNumber, self)

		self.mouseReflector.Down()
		self.Enable = True

	def OnMouseLeftButtonUp(self):
		if self.Enable or self.DontUsingSlot:
			return
		self.mouseReflector.Up()
		
	def RefreshOriSlot(self):
		self.Enable = False
		self.mouseReflector.Up()
		self.mouseReflector.Show()

	def Clear(self):
		self.mouseReflector.Up()
		self.mouseReflector.Hide()
		self.Enable = False
		self.SlotNumber = 0

class MouseReflector(ui.Window):
	def __init__(self, parent):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.AddFlag("not_pick")
		self.width = self.height = 0
		self.isDown = False
		self.isEmpty = False
		self.EmptyOverin = False

	def __del__(self):
		ui.Window.__del__(self)
		
	def SetEmptyOverIn(self,overin):
		self.EmptyOverin = overin
		
	def SetEmpty(self,isempty):
		self.isEmpty = isempty
		
	def GetEmpty(self):
		return self.isEmpty

	def Down(self):
		self.isDown = True

	def Up(self):
		self.isDown = False

	def OnRender(self):

		if self.isDown:
			grp.SetColor(ui.WHITE_COLOR)
		else:
			grp.SetColor(ui.HALF_WHITE_COLOR)
		
		if self.isEmpty:
			if self.isDown:
				grp.SetColor(ui.WHITE_COLOR)
			else:
				grp.SetColor(ui.HALF_RED_COLOR)

			if self.EmptyOverin and not self.isDown:
				grp.SetColor(ui.HALF_WHITE_COLOR)
		

		x, y = self.GetGlobalPosition()
		grp.RenderBar(x+2, y+2, self.GetWidth()-4, self.GetHeight()-4)

KEYSTATE_RUNFRONT  = 0
KEYSTATE_RUNFBACK  = 1
KEYSTATE_RUNFLEFT  = 2
KEYSTATE_RUNFRIGHT = 3
KEYSTATE_CAMRIGHT  = 4
KEYSTATE_CAMLEFT   = 5
KEYSTATE_CAMIN     = 6
KEYSTATE_CAMOUT    = 7
KEYSTATE_CAMDOWN   = 8
KEYSTATE_CAMUP     = 9
KEYSTATE_SHOWNAME  = 10
KEYSTATE_ATT       = 11
KEYSTATE_MAX       = 12

class KeyChangeWindow(ui.ScriptWindow):
	def __init__(self, game, interface):
		ui.ScriptWindow.__init__(self)
		self.isloded = 0
		self.ADDKEYBUFFERCONTROL = playerm2g2.KEY_ADDKEYBUFFERCONTROL
		self.ADDKEYBUFFERALT         = playerm2g2.KEY_ADDKEYBUFFERALT
		self.ADDKEYBUFFERSHIFT       = playerm2g2.KEY_ADDKEYBUFFERSHIFT

		self.KeySlotMax = 66

		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.KeySlotMax = self.KeySlotMax + 1
		if app.ENABLE_AUTO_SYSTEM:
			self.KeySlotMax = self.KeySlotMax + 1
		if app.ENABLE_MONSTER_CARD:
			self.KeySlotMax = self.KeySlotMax + 1
		if app.ENABLE_PARTY_MATCH:
			self.KeySlotMax = self.KeySlotMax + 1

		self.UsableKeyMax = 221
		self.SelectSlotDikNumber = 0
		
		self.slotList = {}
		self.KeyUiInfoDick = {}
		self.BaseKeyUiInfoDick = {}
		self.KeySaveUiInfoDick = {}


		self.interface = interface
		self.wndGame = game

		self.__BuildKeyInfoText()
		self.__BuildKeyFunction()
		self.__BuildUsableKeyInfo()
		
		self.LoadKeyInfo()
		self.__LoadWindow()
		
		self.popup = None
		
		if app.ENABLE_AUTO_SYSTEM:
			self.AutoSystemText = None
			self.AutoKeySlotNumber = 67
			
		if app.ENABLE_PARTY_MATCH:
			self.PartyMatchText			= None
			self.PartyMatchSlotNumber	= 69

		self.SetWindowName("KeyChangeWindow")
		self.board = None
		
	def __del__(self):
		self.KeyUiInfoDick = None
		self.BaseKeyUiInfoDick = None
		self.KeyFunctionInfo = None
		self.UsableKeyDict = None
		self.KeySaveUiInfoDick = None
		self.popup = None
		ui.ScriptWindow.__del__(self)
		if app.ENABLE_AUTO_SYSTEM:
			self.AutoSystemText = None
		if app.ENABLE_PARTY_MATCH:
			self.PartyMatchText = None
		self.slotList = {}
		self.board = None

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/KeyChange_Window.py")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("CancleButton").SetEvent(ui.__mem_func__(self.CloseAnswer))
			self.GetChild("SaveButton").SetEvent(ui.__mem_func__(self.SaveAndClose))
			self.GetChild("ClearButton").SetEvent(ui.__mem_func__(self.Clear))
			self.board = self.GetChild("board")
			if app.ENABLE_AUTO_SYSTEM:
				self.AutoSystemText = self.GetChild("AutoSystem")
				
			if app.ENABLE_PARTY_MATCH:
				self.PartyMatchText = self.GetChild("PartyMatch")
				
		except:
			import exception
			exception.Abort("KeyChangeWindow.__LoadWindow.UIScript/KeyChange_Window.py")
			
		if localeInfo.IsARABIC():
			self.baseXArabic = 510
			self.Xup = self.baseXArabic
			self.Yup = 0
			for i in xrange(self.KeySlotMax):
				if i == 19:
					self.Xup = self.baseXArabic - 180 - 30
					self.Yup = 0
				
				if i == 38:
					self.Xup = self.baseXArabic - (180 * 2 + 30)
					self.Yup = 0
				
				if i == 50:
					self.Xup = self.baseXArabic - (180 * 3 + 30)
					self.Yup = 0
			
				keytypeSlot = SelectTextSlot((70 + self.Xup + 30), (75 + (self.Yup * 20)), self.KeySlotMax)
				keytypeSlot.SetEvent(ui.__mem_func__(self.OnMouseLeftButtonDownEvent))
				keytypeSlot.SetParent(self.board)				
				keytypeSlot.SetText(self.KeyTextDict[self.KeyUiInfoDick[i]])
				self.slotList[i] = keytypeSlot
				self.Yup += 1
		else:
			self.Xup = 20
			self.Yup = 0

			for i in xrange(self.KeySlotMax):
				if i == 19:
					self.Xup = 180 + 30
					self.Yup = 0
				
				if i == 38:
					self.Xup = 180 * 2 + 30
					self.Yup = 0
				
				if i == 50:
					self.Xup = 180 * 3 + 30
					self.Yup = 0
			
				keytypeSlot = SelectTextSlot((70 + self.Xup + 30), (75 + (self.Yup * 20)), self.KeySlotMax)
				keytypeSlot.SetEvent(ui.__mem_func__(self.OnMouseLeftButtonDownEvent))
				keytypeSlot.SetParent(self.board)
				keytypeSlot.SetText(self.KeyTextDict[self.KeyUiInfoDick[i]])
				self.slotList[i] = keytypeSlot
				self.Yup += 1
	
			## 스크린샷 키 설정 못함.	
			self.slotList[64].Disable()
	
	def OnMouseLeftButtonDownEvent(self, slotnumber, slot):

		returnslotnumber = slotnumber

		for i in xrange(self.KeySlotMax):
			if slot != self.slotList[i]:
				if not self.slotList[i].mouseReflector.GetEmpty():
					self.slotList[i].mouseReflector.Hide()
				self.slotList[i].mouseReflector.Up()
				self.slotList[i].Enable = False
			else:
				returnslotnumber = i

		return returnslotnumber
		
	def Open(self):
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow()
			
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)
		playerm2g2.IsOpenKeySettingWIndow(1)

		for i in xrange(self.KeySlotMax):
			self.slotList[i].EmptySlotShow()
			self.KeySaveUiInfoDick[i] = self.KeyUiInfoDick[i]
		
		self.RefreshKeyText()
		
		if app.ENABLE_AUTO_SYSTEM:
			if not chrmgrm2g.GetAutoOnOff():
				self.AutoSystemText.Hide()
				self.slotList[self.AutoKeySlotNumber].Hide()
			else:
				self.AutoSystemText.Show()
				self.slotList[self.AutoKeySlotNumber].Show()
				
		if app.ENABLE_PARTY_MATCH:
			if chrmgrm2g.GetPartyMatchOff():
				if self.PartyMatchText:
					self.PartyMatchText.Hide()
				self.slotList[self.PartyMatchSlotNumber].Hide()
			else:
				if self.PartyMatchText:
					self.PartyMatchText.Show()
				self.slotList[self.PartyMatchSlotNumber].Show()

	# 저장하고 종료	
	def KeyChangeWindowSaveClose(self, isclose):
		if isclose:
			for i in xrange(self.KeySlotMax):
				self.KeyUiInfoDick[i] = self.KeySaveUiInfoDick[i]
			self.SaveKeyInfo()
			self.SettingKey()
			self.Hide()
			self.isloded = 0
			playerm2g2.IsOpenKeySettingWIndow(0)
			for i in xrange(self.KeySlotMax):
				self.slotList[i].Clear()
		if self.popup:
			self.popup.Close()
			self.popup = None
	
	# 저장안하고 종료		
	def KeyChangeWindowClose(self, isclose):
		if isclose:
			self.Hide()
			self.isloded = 0
			playerm2g2.IsOpenKeySettingWIndow(0)
			for i in xrange(self.KeySlotMax):
				self.slotList[i].Clear()
		if self.popup:
			self.popup.Close()
			self.popup = None
				
	def Close(self):
		self.CloseAnswer()

	def CloseAnswer(self):
		popup = uiCommon.QuestionDialog()
		popup.SetText(localeInfo.KEYCHANGE_DONT_SAVE_EXIT)
		popup.SetAcceptEvent(lambda arg=True: self.KeyChangeWindowClose(arg))
		popup.SetCancelEvent(lambda arg=False: self.KeyChangeWindowClose(arg))
		popup.Open()
		self.popup = popup

	def SaveAndClose(self):
		popup = uiCommon.QuestionDialog()
		popup.SetText(localeInfo.KEYCHANGE_SAVE_EXIT)
		popup.SetAcceptEvent(lambda arg=True: self.KeyChangeWindowSaveClose(arg))
		popup.SetCancelEvent(lambda arg=False: self.KeyChangeWindowSaveClose(arg))
		popup.Open()
		self.popup = popup
		
	def OnPressEscapeKey(self):
		self.CloseAnswer()
		return True
		
	def IsSelectKeySlot(self):
		for i in xrange(self.KeySlotMax):
			if self.slotList[i].GetAble():
				return True
		return False
		
	# 사용 가능한 키 판별
	def CheckUsableKeyValue(self, Key):
		for i in xrange(self.UsableKeyMax):
			if self.UsableKeyDict[i] == Key:
				## 스크린샷 키 사용 안됨.
				if Key == app.DIK_SYSRQ:
					return True
				else:
					return False
		return True

	## KeySetting.txt 파일 읽어 와서 셋팅
	def LoadKeyInfo(self):
	
		for i in xrange(self.KeySlotMax):
			self.KeyUiInfoDick[i] = 0
		
		try:
			import os
			os.remove("KeySetting")
		except:
			pass

		handle = app.OpenTextFile("keysave")
		count = app.GetTextFileLineCount(handle)

		if count > 0:
			for i in xrange(count-1):
				line = app.GetTextFileLine(handle, i)
				self.KeyUiInfoDick[i] = int(line)
			
			if count-1 != self.KeySlotMax:
				if app.ENABLE_GROWTH_PET_SYSTEM:
					if not self.KeyUiInfoDick[64]:
						self.KeyUiInfoDick[66] = app.DIK_P
				if app.ENABLE_AUTO_SYSTEM:
					if not self.KeyUiInfoDick[65]:
						self.KeyUiInfoDick[67] = app.DIK_K
				if app.ENABLE_MONSTER_CARD:
					if not self.KeyUiInfoDick[66]:
						self.KeyUiInfoDick[68] = app.DIK_J
						
				if app.ENABLE_PARTY_MATCH:
					if not self.KeyUiInfoDick[69]:
						self.KeyUiInfoDick[69] = app.DIK_J + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
						
			self.__BuildKeyInfo(True)
			app.CloseTextFile(handle)
			
			## 만약 스크린샷 슬롯에 다른 키가 있다면 초기화 하고 저장.
			if self.KeyUiInfoDick[64] != app.DIK_SYSRQ:
				self.__BuildKeyInfo(False)
				self.SaveKeyInfo()
		else:
			self.__BuildKeyInfo(False)

		self.SettingKey()
			
	## 키 셋팅.
	def SettingKey(self):
		playerm2g2.KeySettingClear()
		for i in xrange(self.KeySlotMax):
			playerm2g2.KeySetting(self.KeyUiInfoDick[i],self.KeyFunctionInfo[i])
			
	## 키 저장.		
	def SaveKeyInfo(self):
		output_KeySettingFile = open("keysave", "w")

		for i in xrange(self.KeySlotMax):
			linestr = str(self.KeyUiInfoDick[i]) +'\n'
			output_KeySettingFile.write(linestr)
			
		output_KeySettingFile.close()
		
	# 선택된 슬롯 번호 리턴.
	def GetSelectSlotNumber(self):
		for i in xrange(self.KeySlotMax):
			if self.slotList[i].GetAble():
				return self.slotList[i].GetSlotNumber()

	# 키 변경	
	def ChangeKey(self, key):
		if self.CheckUsableKeyValue(key):
			return
	
		OldSlotNumber = self.KeySlotMax + 1
		slotNumber = 0

		for i in xrange(self.KeySlotMax):
			if self.slotList[i].GetAble():
				slotNumber = self.slotList[i].GetSlotNumber()
			if self.KeySaveUiInfoDick[i] == key:
				OldSlotNumber = i
		
		self.SelectSlotDikNumber = self.KeySaveUiInfoDick[slotNumber]
		
		# 기존과 같은 키 일경우 return
		if key == self.SelectSlotDikNumber:
			return

		## 기존꺼와 교환.(없으면 패스) UI
		self.KeySaveUiInfoDick[slotNumber] = key
		if OldSlotNumber < self.KeySlotMax + 1:
			self.KeySaveUiInfoDick[OldSlotNumber] = 0
		
		self.RefreshKeyTextTemp()
		
		if not self.slotList[slotNumber].GetAble():
			self.slotList[slotNumber].Clear()
		self.slotList[slotNumber].RefreshOriSlot()
		
	def GetSelectSlotDicNumber(self):
		return self.SelectSlotDikNumber
		
	# 키설정 UI 텍스트 설정.
	def RefreshKeyText(self):
		for i in xrange(self.KeySlotMax):
			self.slotList[i].SetText(self.KeyTextDict[self.KeyUiInfoDick[i]])
			
	# 키설정 UI 텍스트 설정(임시).
	def RefreshKeyTextTemp(self):
		for i in xrange(self.KeySlotMax):
			self.slotList[i].SetText(self.KeyTextDict[self.KeySaveUiInfoDick[i]])
	
	def IsOpen(self):
		return self.isloded

	## 초기화
	def Clear(self):
		for i in xrange(self.KeySlotMax):
			self.KeySaveUiInfoDick[i] = self.BaseKeyUiInfoDick[i]
		self.SettingKey()
		self.RefreshKeyTextTemp()

	## 슬롯키인지 확인
	def IsSlotKey(self, Key):
		for i in [36,37,38,39,40,41,42,43]:
			if self.KeyUiInfoDick[i] == Key:
				return True
		return False
	
	## ========================== KeyDown Function ==========================

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def __PressTabKey(self):
			self.interface.OpenGuildScoreWindow()
		
	## ========================== KeyDown Function ==========================
	
	# 이동 키및, 카메라 조작 키 공격, 거르기.
	def IsChangeKey(self,slotnumber):
		if slotnumber == 0 or slotnumber == 1 or slotnumber == 2 or slotnumber == 3 or \
			slotnumber == 4 or slotnumber == 5 or slotnumber == 6 or slotnumber == 7 or \
			slotnumber == 8 or slotnumber == 9 or \
			slotnumber == 11 or \
			slotnumber == 19 or	slotnumber == 20 or slotnumber == 21 or slotnumber == 22 or \
			slotnumber == 23 or slotnumber == 24 or slotnumber == 25 or slotnumber == 26 or \
			slotnumber == 27 or slotnumber == 28:
			return False
		return True
	
	## =================== 키 셋팅및 변경에 필요한 Dick 들 셋팅 부분 ===================

	def __BuildKeyInfo(self, fileable):
		
		## 실제 UI 표기되고, 작동될 것 Base
		KeyUiInfoDick = {}
		## 기본동작
		KeyUiInfoDick[0] = app.DIK_W
		KeyUiInfoDick[1] = app.DIK_S
		KeyUiInfoDick[2] = app.DIK_A
		KeyUiInfoDick[3] = app.DIK_D
		KeyUiInfoDick[4] = app.DIK_E
		KeyUiInfoDick[5] = app.DIK_Q
		KeyUiInfoDick[6] = app.DIK_R
		KeyUiInfoDick[7] = app.DIK_F
		KeyUiInfoDick[8] = app.DIK_T
		KeyUiInfoDick[9] = app.DIK_G
		KeyUiInfoDick[10] = app.DIK_GRAVE
		KeyUiInfoDick[11] = app.DIK_SPACE
		KeyUiInfoDick[12] = app.DIK_H + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[13] = app.DIK_F + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[14] = app.DIK_1 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[15] = app.DIK_2 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[16] = app.DIK_3 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[17] = app.DIK_4 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL		
		KeyUiInfoDick[18] = app.DIK_NUMLOCK

		KeyUiInfoDick[19] = app.DIK_UP
		KeyUiInfoDick[20] = app.DIK_DOWN
		KeyUiInfoDick[21] = app.DIK_LEFT
		KeyUiInfoDick[22] = app.DIK_RIGHT
		KeyUiInfoDick[23] = app.DIK_NUMPAD6
		KeyUiInfoDick[24] = app.DIK_NUMPAD4
		KeyUiInfoDick[25] = app.DIK_PGUP
		KeyUiInfoDick[26] = app.DIK_PGDN
		KeyUiInfoDick[27] = app.DIK_NUMPAD8
		KeyUiInfoDick[28] = app.DIK_NUMPAD2
		KeyUiInfoDick[29] = app.DIK_Z
		KeyUiInfoDick[30] = app.DIK_G + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[31] = app.DIK_B + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[32] = app.DIK_5 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[33] = app.DIK_6 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[34] = app.DIK_7 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[35] = app.DIK_8 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[36] = app.DIK_9 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[37] = app.DIK_TAB
		## 슬롯 단축키
		KeyUiInfoDick[38] = app.DIK_1
		KeyUiInfoDick[39] = app.DIK_2
		KeyUiInfoDick[40] = app.DIK_3
		KeyUiInfoDick[41] = app.DIK_4
		KeyUiInfoDick[42] = app.DIK_F1
		KeyUiInfoDick[43] = app.DIK_F2
		KeyUiInfoDick[44] = app.DIK_F3
		KeyUiInfoDick[45] = app.DIK_F4
		KeyUiInfoDick[46] = app.DIK_1 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		KeyUiInfoDick[47] = app.DIK_2 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		KeyUiInfoDick[48] = app.DIK_3 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		KeyUiInfoDick[49] = app.DIK_4 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT		
		## 인터페이스
		KeyUiInfoDick[50] = app.DIK_C
		KeyUiInfoDick[51] = app.DIK_V
		KeyUiInfoDick[52] = app.DIK_N
		KeyUiInfoDick[53] = app.DIK_I
		KeyUiInfoDick[54] = app.DIK_O
		KeyUiInfoDick[55] = app.DIK_M
		KeyUiInfoDick[56] = app.DIK_L
		KeyUiInfoDick[57] = app.DIK_Q + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		KeyUiInfoDick[58] = app.DIK_G + app.DIK_LALT + self.ADDKEYBUFFERALT
		KeyUiInfoDick[59] = app.DIK_M + app.DIK_LALT + self.ADDKEYBUFFERALT
		KeyUiInfoDick[60] = app.DIK_H
		KeyUiInfoDick[61] = app.DIK_B		
		KeyUiInfoDick[62] = app.DIK_ADD
		KeyUiInfoDick[63] = app.DIK_SUBTRACT
		KeyUiInfoDick[64] = app.DIK_SYSRQ
		KeyUiInfoDick[65] = app.DIK_X

		if app.ENABLE_GROWTH_PET_SYSTEM:
			KeyUiInfoDick[66] = app.DIK_P
		if app.ENABLE_AUTO_SYSTEM:
			KeyUiInfoDick[67] = app.DIK_K
		if app.ENABLE_MONSTER_CARD:
			KeyUiInfoDick[68] = app.DIK_J
		if app.ENABLE_PARTY_MATCH:
			KeyUiInfoDick[69] = app.DIK_J + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		
		if not fileable:
			self.KeyUiInfoDick = KeyUiInfoDick

		## 초기화에 필요해서 따로 하나더 저장해둠.
		for i in xrange(self.KeySlotMax):
			self.BaseKeyUiInfoDick[i] = KeyUiInfoDick[i]
				
	def __BuildKeyFunction(self):
		KeyFunctionInfo = {}
		## 기본동작
		KeyFunctionInfo[0]   = playerm2g2.KEY_MOVE_UP_1#lambda Key = app.DIK_UP : self.MovePlayer(Key)
		KeyFunctionInfo[1]   = playerm2g2.KEY_MOVE_DOWN_1#lambda Key = app.DIK_DOWN : self.MovePlayer(Key)
		KeyFunctionInfo[2]   = playerm2g2.KEY_MOVE_LEFT_1#lambda Key = app.DIK_LEFT : self.MovePlayer(Key)
		KeyFunctionInfo[3]   = playerm2g2.KEY_MOVE_RIGHT_1#lambda Key = app.DIK_RIGHT : self.MovePlayer(Key)
		KeyFunctionInfo[4]   = playerm2g2.KEY_CAMERA_ROTATE_POSITIVE_1#lambda type = app.CAMERA_TO_POSITIVE : self.RotateCamera(type)
		KeyFunctionInfo[5]   = playerm2g2.KEY_CAMERA_ROTATE_NEGATIVE_1#lambda type = app.CAMERA_TO_NEGATIVE : self.RotateCamera(type)
		KeyFunctionInfo[6]   = playerm2g2.KEY_CAMERA_ZOOM_NEGATIVE_1#lambda type = app.CAMERA_TO_NEGATIVE : self.ZoomCamera(type)
		KeyFunctionInfo[7]   = playerm2g2.KEY_CAMERA_ZOOM_POSITIVE_1#lambda type = app.CAMERA_TO_POSITIVE : self.ZoomCamera(type)
		KeyFunctionInfo[8]   = playerm2g2.KEY_CAMERA_PITCH_NEGATIVE_1#lambda type = app.CAMERA_TO_NEGATIVE : self.PitchCamera(type)
		KeyFunctionInfo[9]   = playerm2g2.KEY_CAMERA_PITCH_POSITIVE_1#lambda type = app.CAMERA_TO_POSITIVE : self.PitchCamera(type)
		KeyFunctionInfo[10] = playerm2g2.KEY_ROOTING_1#lambda : playerm2g2.PickCloseItem()
		KeyFunctionInfo[11] = playerm2g2.KEY_ATTACK#lambda : self.AttStart()
		KeyFunctionInfo[12] = playerm2g2.KEY_RIDEMYHORS#lambda : self.__RideMyHors()
		KeyFunctionInfo[13] = playerm2g2.KEY_FEEDMYHORS#lambda : self.__feedMyHors()
		KeyFunctionInfo[14] = playerm2g2.KEY_EMOTION1#lambda : self.__Emotion(1)
		KeyFunctionInfo[15] = playerm2g2.KEY_EMOTION2#lambda : self.__Emotion(2)
		KeyFunctionInfo[16] = playerm2g2.KEY_EMOTION3#lambda : self.__Emotion(3)
		KeyFunctionInfo[17] = playerm2g2.KEY_EMOTION4#lambda : self.__Emotion(4)
		KeyFunctionInfo[18] = playerm2g2.KEY_AUTO_RUN
		KeyFunctionInfo[19] = playerm2g2.KEY_MOVE_UP_2#lambda Key = app.DIK_UP : self.MovePlayer(Key)
		KeyFunctionInfo[20] = playerm2g2.KEY_MOVE_DOWN_2#lambda Key = app.DIK_DOWN : self.MovePlayer(Key)
		KeyFunctionInfo[21] = playerm2g2.KEY_MOVE_LEFT_2#lambda Key = app.DIK_LEFT : self.MovePlayer(Key)
		KeyFunctionInfo[22] = playerm2g2.KEY_MOVE_RIGHT_2#lambda Key = app.DIK_RIGHT : self.MovePlayer(Key)
		KeyFunctionInfo[23] = playerm2g2.KEY_CAMERA_ROTATE_POSITIVE_2#lambda type = app.CAMERA_TO_POSITIVE : self.RotateCamera(type)
		KeyFunctionInfo[24] = playerm2g2.KEY_CAMERA_ROTATE_NEGATIVE_2#lambda type = app.CAMERA_TO_NEGATIVE : self.RotateCamera(type)
		KeyFunctionInfo[25] = playerm2g2.KEY_CAMERA_ZOOM_NEGATIVE_2#lambda type = app.CAMERA_TO_NEGATIVE : self.ZoomCamera(type)
		KeyFunctionInfo[26] = playerm2g2.KEY_CAMERA_ZOOM_POSITIVE_2#lambda type = app.CAMERA_TO_POSITIVE : self.ZoomCamera(type)
		KeyFunctionInfo[27] = playerm2g2.KEY_CAMERA_PITCH_NEGATIVE_2#lambda type = app.CAMERA_TO_NEGATIVE : self.PitchCamera(type)
		KeyFunctionInfo[28] = playerm2g2.KEY_CAMERA_PITCH_POSITIVE_2#lambda type = app.CAMERA_TO_POSITIVE : self.PitchCamera(type)
		KeyFunctionInfo[29] = playerm2g2.KEY_ROOTING_2#lambda : playerm2g2.PickCloseItem()
		KeyFunctionInfo[30] = playerm2g2.KEY_RIDEHORS#lambda : self.__RideHors()
		KeyFunctionInfo[31] = playerm2g2.KEY_BYEMYHORS#lambda : self.__ByeMyHors()
		KeyFunctionInfo[32] = playerm2g2.KEY_EMOTION5#lambda : self.__Emotion(5)
		KeyFunctionInfo[33] = playerm2g2.KEY_EMOTION6#lambda : self.__Emotion(6)
		KeyFunctionInfo[34] = playerm2g2.KEY_EMOTION7#lambda : self.__Emotion(7)
		KeyFunctionInfo[35] = playerm2g2.KEY_EMOTION8#lambda : self.__Emotion(8)
		KeyFunctionInfo[36] = playerm2g2.KEY_EMOTION9#lambda : self.__Emotion(9)
		KeyFunctionInfo[37] = playerm2g2.KEY_NEXT_TARGET
		## 슬롯 단축키
		KeyFunctionInfo[38] = playerm2g2.KEY_SLOT_1#lambda : self.__PressQuickSlot(0)
		KeyFunctionInfo[39] = playerm2g2.KEY_SLOT_2#lambda : self.__PressQuickSlot(1)
		KeyFunctionInfo[40] = playerm2g2.KEY_SLOT_3#lambda : self.__PressQuickSlot(2)
		KeyFunctionInfo[41] = playerm2g2.KEY_SLOT_4#lambda : self.__PressQuickSlot(3)
		KeyFunctionInfo[42] = playerm2g2.KEY_SLOT_5#lambda : self.__PressQuickSlot(4)
		KeyFunctionInfo[43] = playerm2g2.KEY_SLOT_6#lambda : self.__PressQuickSlot(5)
		KeyFunctionInfo[44] = playerm2g2.KEY_SLOT_7#lambda : self.__PressQuickSlot(6)
		KeyFunctionInfo[45] = playerm2g2.KEY_SLOT_8#lambda : self.__PressQuickSlot(7)
		KeyFunctionInfo[46] = playerm2g2.KEY_SLOT_CHANGE_1#lambda : self.__SelectQuickSlot(0)
		KeyFunctionInfo[47] = playerm2g2.KEY_SLOT_CHANGE_2#lambda : self.__SelectQuickSlot(1)
		KeyFunctionInfo[48] = playerm2g2.KEY_SLOT_CHANGE_3#lambda : self.__SelectQuickSlot(2)
		KeyFunctionInfo[49] = playerm2g2.KEY_SLOT_CHANGE_4#lambda : self.__SelectQuickSlot(3)
		## 인터페이스
		KeyFunctionInfo[50] = playerm2g2.KEY_OPEN_STATE#lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		KeyFunctionInfo[51] = playerm2g2.KEY_OPEN_SKILL#lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		KeyFunctionInfo[52] = playerm2g2.KEY_OPEN_QUEST#lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		KeyFunctionInfo[53] = playerm2g2.KEY_OPEN_INVENTORY#lambda : self.interface.ToggleInventoryWindow()
		KeyFunctionInfo[54] = playerm2g2.KEY_OPEN_DDS#lambda : self.interface.ToggleDragonSoulWindowWithNoInfo()
		KeyFunctionInfo[55] = playerm2g2.KEY_OPEN_MINIMAP#lambda : self.interface.ToggleMiniMap()
		KeyFunctionInfo[56] = playerm2g2.KEY_OPEN_LOGCHAT#lambda : self.interface.ToggleChatLogWindow()
		KeyFunctionInfo[57] = playerm2g2.KEY_SCROLL_ONOFF#lambda : self.__QuestOnOff()
		KeyFunctionInfo[58] = playerm2g2.KEY_OPEN_GUILD#lambda : self.interface.ToggleGuildWindow()
		KeyFunctionInfo[59] = playerm2g2.KEY_OPEN_MESSENGER#lambda : self.interface.ToggleMessenger()
		KeyFunctionInfo[60] = playerm2g2.KEY_OPEN_HELP#lambda : self.interface.OpenHelpWindow()
		KeyFunctionInfo[61] = playerm2g2.KEY_OPEN_ACTION#lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		KeyFunctionInfo[62] = playerm2g2.KEY_PLUS_MINIMAP#lambda : self.interface.MiniMapScaleUp()
		KeyFunctionInfo[63] = playerm2g2.KEY_MIN_MINIMAP#lambda : self.interface.MiniMapScaleDown()
		KeyFunctionInfo[64] = playerm2g2.KEY_SCREENSHOT#lambda : self.SaveScreen()
		KeyFunctionInfo[65] = playerm2g2.KEY_SHOW_NAME#lambda : self.ShowName()

		if app.ENABLE_GROWTH_PET_SYSTEM:
			KeyFunctionInfo[66] = playerm2g2.KEY_OPEN_PET#lambda : self.interface.TogglePetInformationWindow()
		if app.ENABLE_AUTO_SYSTEM:
			KeyFunctionInfo[67] = playerm2g2.KEY_OPEN_AUTO #lambda : self.interface.ToggleAutoWindow
		if app.ENABLE_MONSTER_CARD:
			KeyFunctionInfo[68] = playerm2g2.KEY_MONSTER_CARD #lambda : self.interface.ToggleMonsterCardWindow
		if app.ENABLE_PARTY_MATCH:
			KeyFunctionInfo[69] = playerm2g2.KEY_PARTY_MATCH
			
		self.KeyFunctionInfo = KeyFunctionInfo

	def __BuildKeyInfoText(self):
	
		## 키 텍스트 정보
		KeyTextDict = {}
		KeyTextDict[0]																	                            = ""
		KeyTextDict[app.DIK_GRAVE]												                            = localeInfo.KEY_GRAVE
		KeyTextDict[app.DIK_0]														                            = localeInfo.KEY_0
		KeyTextDict[app.DIK_1]														                            = localeInfo.KEY_1
		KeyTextDict[app.DIK_2]														                            = localeInfo.KEY_2
		KeyTextDict[app.DIK_3]														                            = localeInfo.KEY_3
		KeyTextDict[app.DIK_4]														                            = localeInfo.KEY_4
		KeyTextDict[app.DIK_5]														                            = localeInfo.KEY_5
		KeyTextDict[app.DIK_6]														                            = localeInfo.KEY_6
		KeyTextDict[app.DIK_7]														                            = localeInfo.KEY_7
		KeyTextDict[app.DIK_8]														                            = localeInfo.KEY_8
		KeyTextDict[app.DIK_9]														                            = localeInfo.KEY_9
		KeyTextDict[app.DIK_GRAVE + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]	= localeInfo.KEY_GRAVE_LCONTROL
		KeyTextDict[app.DIK_0 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_0_LCONTROL
		KeyTextDict[app.DIK_1 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_1_LCONTROL
		KeyTextDict[app.DIK_2 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_2_LCONTROL
		KeyTextDict[app.DIK_3 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_3_LCONTROL
		KeyTextDict[app.DIK_4 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_4_LCONTROL
		KeyTextDict[app.DIK_5 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_5_LCONTROL
		KeyTextDict[app.DIK_6 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_6_LCONTROL
		KeyTextDict[app.DIK_7 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_7_LCONTROL
		KeyTextDict[app.DIK_8 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_8_LCONTROL
		KeyTextDict[app.DIK_9 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_9_LCONTROL
		KeyTextDict[app.DIK_GRAVE + app.DIK_LALT + self.ADDKEYBUFFERALT]			        = localeInfo.KEY_GRAVE_LALT
		KeyTextDict[app.DIK_0 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_0_LALT
		KeyTextDict[app.DIK_1 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_1_LALT
		KeyTextDict[app.DIK_2 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_2_LALT
		KeyTextDict[app.DIK_3 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_3_LALT
		KeyTextDict[app.DIK_4 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_4_LALT
		KeyTextDict[app.DIK_5 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_5_LALT
		KeyTextDict[app.DIK_6 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_6_LALT
		KeyTextDict[app.DIK_7 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_7_LALT
		KeyTextDict[app.DIK_8 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_8_LALT
		KeyTextDict[app.DIK_9 + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_9_LALT
		KeyTextDict[app.DIK_GRAVE + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]		        = localeInfo.KEY_GRAVE_LSHIFT
		KeyTextDict[app.DIK_0 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_0_LSHIFT
		KeyTextDict[app.DIK_1 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_1_LSHIFT
		KeyTextDict[app.DIK_2 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_2_LSHIFT
		KeyTextDict[app.DIK_3 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_3_LSHIFT
		KeyTextDict[app.DIK_4 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_4_LSHIFT
		KeyTextDict[app.DIK_5 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_5_LSHIFT
		KeyTextDict[app.DIK_6 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_6_LSHIFT
		KeyTextDict[app.DIK_7 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_7_LSHIFT
		KeyTextDict[app.DIK_8 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_8_LSHIFT
		KeyTextDict[app.DIK_9 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_9_LSHIFT
		KeyTextDict[app.DIK_F1]														                            = localeInfo.KEY_F1
		KeyTextDict[app.DIK_F2]														                            = localeInfo.KEY_F2
		KeyTextDict[app.DIK_F3]														                            = localeInfo.KEY_F3
		KeyTextDict[app.DIK_F4]														                            = localeInfo.KEY_F4
		KeyTextDict[app.DIK_F5]														                            = localeInfo.KEY_F5
		KeyTextDict[app.DIK_F6]														                            = localeInfo.KEY_F6
		KeyTextDict[app.DIK_F7]														                            = localeInfo.KEY_F7
		KeyTextDict[app.DIK_F8]														                            = localeInfo.KEY_F8
		KeyTextDict[app.DIK_F9]														                            = localeInfo.KEY_F9
		KeyTextDict[app.DIK_F10]													                                = localeInfo.KEY_F10
		KeyTextDict[app.DIK_F1 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F1_LCONTROL
		KeyTextDict[app.DIK_F2 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F2_LCONTROL
		KeyTextDict[app.DIK_F3 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F3_LCONTROL
		KeyTextDict[app.DIK_F4 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F4_LCONTROL
		KeyTextDict[app.DIK_F5 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F5_LCONTROL
		KeyTextDict[app.DIK_F6 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F6_LCONTROL
		KeyTextDict[app.DIK_F7 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F7_LCONTROL
		KeyTextDict[app.DIK_F8 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F8_LCONTROL
		KeyTextDict[app.DIK_F9 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F9_LCONTROL
		KeyTextDict[app.DIK_F10 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		= localeInfo.KEY_F10_LCONTROL
		KeyTextDict[app.DIK_F1 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F1_LALT
		KeyTextDict[app.DIK_F2 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F2_LALT
		KeyTextDict[app.DIK_F3 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F3_LALT
		KeyTextDict[app.DIK_F4 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F4_LALT
		KeyTextDict[app.DIK_F5 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F5_LALT
		KeyTextDict[app.DIK_F6 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F6_LALT
		KeyTextDict[app.DIK_F7 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F7_LALT
		KeyTextDict[app.DIK_F8 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F8_LALT
		KeyTextDict[app.DIK_F9 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F9_LALT
		KeyTextDict[app.DIK_F10 + app.DIK_LALT + self.ADDKEYBUFFERALT]				        = localeInfo.KEY_F10_LALT
		KeyTextDict[app.DIK_F1 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F1_LSHIFT
		KeyTextDict[app.DIK_F2 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F2_LSHIFT
		KeyTextDict[app.DIK_F3 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F3_LSHIFT
		KeyTextDict[app.DIK_F4 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F4_LSHIFT
		KeyTextDict[app.DIK_F5 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F5_LSHIFT
		KeyTextDict[app.DIK_F6 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F6_LSHIFT
		KeyTextDict[app.DIK_F7 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F7_LSHIFT
		KeyTextDict[app.DIK_F8 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F8_LSHIFT
		KeyTextDict[app.DIK_F9 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F9_LSHIFT
		KeyTextDict[app.DIK_F10 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_F10_LSHIFT
		KeyTextDict[app.DIK_LCONTROL]												                        = localeInfo.KEY_LCONTROL
		KeyTextDict[app.DIK_LALT]														                        = localeInfo.KEY_LALT
		KeyTextDict[app.DIK_LSHIFT]														                        = localeInfo.KEY_LSHIFT
		KeyTextDict[app.DIK_SYSRQ]														                        = localeInfo.KEY_SYSRQ
		KeyTextDict[app.DIK_SPACE]														                        = localeInfo.KEY_SPACE
		KeyTextDict[app.DIK_TAB]														                            = localeInfo.KEY_TAB
		KeyTextDict[app.DIK_UP]															                        = localeInfo.KEY_UP
		KeyTextDict[app.DIK_DOWN]														                        = localeInfo.KEY_DOWN
		KeyTextDict[app.DIK_LEFT]														                        = localeInfo.KEY_LEFT
		KeyTextDict[app.DIK_RIGHT]														                        = localeInfo.KEY_RIGHT
		KeyTextDict[app.DIK_Q]															                        = localeInfo.KEY_Q
		KeyTextDict[app.DIK_W]															                        = localeInfo.KEY_W
		KeyTextDict[app.DIK_E]															                        = localeInfo.KEY_E
		KeyTextDict[app.DIK_R]															                        = localeInfo.KEY_R
		KeyTextDict[app.DIK_T]															                        = localeInfo.KEY_T
		KeyTextDict[app.DIK_Y]															                        = localeInfo.KEY_Y
		KeyTextDict[app.DIK_U]															                        = localeInfo.KEY_U
		KeyTextDict[app.DIK_I]															                            = localeInfo.KEY_I
		KeyTextDict[app.DIK_O]															                        = localeInfo.KEY_O
		KeyTextDict[app.DIK_P]															                        = localeInfo.KEY_P
		KeyTextDict[app.DIK_A]															                        = localeInfo.KEY_A
		KeyTextDict[app.DIK_S]															                        = localeInfo.KEY_S
		KeyTextDict[app.DIK_D]															                        = localeInfo.KEY_D
		KeyTextDict[app.DIK_F]															                        = localeInfo.KEY_F
		KeyTextDict[app.DIK_G]															                        = localeInfo.KEY_G
		KeyTextDict[app.DIK_H]															                        = localeInfo.KEY_H
		KeyTextDict[app.DIK_J]															                            = localeInfo.KEY_J
		KeyTextDict[app.DIK_K]															                        = localeInfo.KEY_K
		KeyTextDict[app.DIK_L]															                        = localeInfo.KEY_L
		KeyTextDict[app.DIK_Z]															                        = localeInfo.KEY_Z
		KeyTextDict[app.DIK_X]															                        = localeInfo.KEY_X
		KeyTextDict[app.DIK_C]															                        = localeInfo.KEY_C
		KeyTextDict[app.DIK_V]															                        = localeInfo.KEY_V
		KeyTextDict[app.DIK_B]															                        = localeInfo.KEY_B
		KeyTextDict[app.DIK_N]															                        = localeInfo.KEY_N
		KeyTextDict[app.DIK_M]															                        = localeInfo.KEY_M
		KeyTextDict[app.DIK_COMMA]														                    = localeInfo.KEY_COMMA
		KeyTextDict[app.DIK_PERIOD]														                    = localeInfo.KEY_PERIOD
		KeyTextDict[app.DIK_Q + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_Q_LCONTROL
		KeyTextDict[app.DIK_W + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_W_LCONTROL
		KeyTextDict[app.DIK_E + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_E_LCONTROL
		KeyTextDict[app.DIK_R + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_R_LCONTROL
		KeyTextDict[app.DIK_T + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_T_LCONTROL
		KeyTextDict[app.DIK_Y + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_Y_LCONTROL
		KeyTextDict[app.DIK_U + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_U_LCONTROL
		KeyTextDict[app.DIK_I + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_I_LCONTROL
		KeyTextDict[app.DIK_O + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_O_LCONTROL
		KeyTextDict[app.DIK_P + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_P_LCONTROL
		KeyTextDict[app.DIK_A + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_A_LCONTROL
		KeyTextDict[app.DIK_S + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_S_LCONTROL
		KeyTextDict[app.DIK_D + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_D_LCONTROL
		KeyTextDict[app.DIK_F + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_F_LCONTROL
		KeyTextDict[app.DIK_G + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_G_LCONTROL
		KeyTextDict[app.DIK_H + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_H_LCONTROL
		KeyTextDict[app.DIK_J + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_J_LCONTROL
		KeyTextDict[app.DIK_K + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_K_LCONTROL
		KeyTextDict[app.DIK_L + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_L_LCONTROL
		KeyTextDict[app.DIK_Z + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_Z_LCONTROL
		KeyTextDict[app.DIK_X + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_X_LCONTROL
		KeyTextDict[app.DIK_C + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_C_LCONTROL
		KeyTextDict[app.DIK_V + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_V_LCONTROL
		KeyTextDict[app.DIK_B + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_B_LCONTROL
		KeyTextDict[app.DIK_N + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_N_LCONTROL
		KeyTextDict[app.DIK_M + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]		    = localeInfo.KEY_M_LCONTROL
		KeyTextDict[app.DIK_COMMA + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]	= localeInfo.KEY_COMMA_LCONTROL
		KeyTextDict[app.DIK_PERIOD + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL]	= localeInfo.KEY_PERIOD_LCONTROL
		KeyTextDict[app.DIK_Q + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_Q_LALT
		KeyTextDict[app.DIK_W + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_W_LALT
		KeyTextDict[app.DIK_E + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_E_LALT
		KeyTextDict[app.DIK_R + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_R_LALT
		KeyTextDict[app.DIK_T + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_T_LALT
		KeyTextDict[app.DIK_Y + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_Y_LALT
		KeyTextDict[app.DIK_U + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_U_LALT
		KeyTextDict[app.DIK_I + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_I_LALT
		KeyTextDict[app.DIK_O + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_O_LALT
		KeyTextDict[app.DIK_P + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_P_LALT
		KeyTextDict[app.DIK_A + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_A_LALT
		KeyTextDict[app.DIK_S + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_S_LALT
		KeyTextDict[app.DIK_D + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_D_LALT
		KeyTextDict[app.DIK_F + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_F_LALT
		KeyTextDict[app.DIK_G + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_G_LALT
		KeyTextDict[app.DIK_H + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_H_LALT
		KeyTextDict[app.DIK_J + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_J_LALT
		KeyTextDict[app.DIK_K + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_K_LALT
		KeyTextDict[app.DIK_L + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_L_LALT
		KeyTextDict[app.DIK_Z + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_Z_LALT
		KeyTextDict[app.DIK_X + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_X_LALT
		KeyTextDict[app.DIK_C + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_C_LALT
		KeyTextDict[app.DIK_V + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_V_LALT
		KeyTextDict[app.DIK_B + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_B_LALT
		KeyTextDict[app.DIK_N + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_N_LALT
		KeyTextDict[app.DIK_M + app.DIK_LALT + self.ADDKEYBUFFERALT]				            = localeInfo.KEY_M_LALT
		KeyTextDict[app.DIK_COMMA + app.DIK_LALT + self.ADDKEYBUFFERALT]			        = localeInfo.KEY_COMMA_LALT
		KeyTextDict[app.DIK_PERIOD + app.DIK_LALT + self.ADDKEYBUFFERALT]			        = localeInfo.KEY_PERIOD_LALT
		KeyTextDict[app.DIK_Q + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_Q_LSHIFT
		KeyTextDict[app.DIK_W + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_W_LSHIFT
		KeyTextDict[app.DIK_E + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_E_LSHIFT
		KeyTextDict[app.DIK_R + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_R_LSHIFT
		KeyTextDict[app.DIK_T + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_T_LSHIFT
		KeyTextDict[app.DIK_Y + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_Y_LSHIFT
		KeyTextDict[app.DIK_U + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_U_LSHIFT
		KeyTextDict[app.DIK_I + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_I_LSHIFT
		KeyTextDict[app.DIK_O + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_O_LSHIFT
		KeyTextDict[app.DIK_P + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_P_LSHIFT
		KeyTextDict[app.DIK_A + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_A_LSHIFT
		KeyTextDict[app.DIK_S + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_S_LSHIFT
		KeyTextDict[app.DIK_D + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_D_LSHIFT
		KeyTextDict[app.DIK_F + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_F_LSHIFT
		KeyTextDict[app.DIK_G + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_G_LSHIFT
		KeyTextDict[app.DIK_H + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_H_LSHIFT
		KeyTextDict[app.DIK_J + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_J_LSHIFT
		KeyTextDict[app.DIK_K + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_K_LSHIFT
		KeyTextDict[app.DIK_L + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_L_LSHIFT
		KeyTextDict[app.DIK_Z + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_Z_LSHIFT
		KeyTextDict[app.DIK_X + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_X_LSHIFT
		KeyTextDict[app.DIK_C + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_C_LSHIFT
		KeyTextDict[app.DIK_V + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_V_LSHIFT
		KeyTextDict[app.DIK_B + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_B_LSHIFT
		KeyTextDict[app.DIK_N + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			            = localeInfo.KEY_N_LSHIFT
		KeyTextDict[app.DIK_M + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]			        = localeInfo.KEY_M_LSHIFT
		KeyTextDict[app.DIK_COMMA + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]		    = localeInfo.KEY_COMMA_LSHIFT
		KeyTextDict[app.DIK_PERIOD + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT]		    = localeInfo.KEY_PERIOD_LSHIFT
		KeyTextDict[app.DIK_NUMPAD0]												                            = localeInfo.KEY_NUMPAD0
		KeyTextDict[app.DIK_NUMPAD1]												                            = localeInfo.KEY_NUMPAD1
		KeyTextDict[app.DIK_NUMPAD2]												                            = localeInfo.KEY_NUMPAD2
		KeyTextDict[app.DIK_NUMPAD3]												                            = localeInfo.KEY_NUMPAD3
		KeyTextDict[app.DIK_NUMPAD4]												                            = localeInfo.KEY_NUMPAD4
		KeyTextDict[app.DIK_NUMPAD5]												                            = localeInfo.KEY_NUMPAD5
		KeyTextDict[app.DIK_NUMPAD6]												                            = localeInfo.KEY_NUMPAD6
		KeyTextDict[app.DIK_NUMPAD7]												                            = localeInfo.KEY_NUMPAD7
		KeyTextDict[app.DIK_NUMPAD8]												                            = localeInfo.KEY_NUMPAD8
		KeyTextDict[app.DIK_NUMPAD9]												                            = localeInfo.KEY_NUMPAD9
		KeyTextDict[app.DIK_ADD]													                            = localeInfo.KEY_ADD
		KeyTextDict[app.DIK_SUBTRACT]												                        = localeInfo.KEY_SUBTRACT
		KeyTextDict[app.DIK_PGUP]													                            = localeInfo.KEY_PGUP
		KeyTextDict[app.DIK_PGDN]													                            = localeInfo.KEY_PGDN
		KeyTextDict[app.DIK_NUMLOCK]												                            = localeInfo.KEY_NUMLOCK

		self.KeyTextDict = KeyTextDict
		
	def __BuildUsableKeyInfo(self):
		## 키 텍스트 정보
		UsableKeyDict = {}
		UsableKeyDict[0]	= app.DIK_GRAVE
		UsableKeyDict[1]	= app.DIK_0
		UsableKeyDict[2]	= app.DIK_1
		UsableKeyDict[3]	= app.DIK_2
		UsableKeyDict[4]	= app.DIK_3
		UsableKeyDict[5]	= app.DIK_4
		UsableKeyDict[6]	= app.DIK_5
		UsableKeyDict[7]	= app.DIK_6
		UsableKeyDict[8]	= app.DIK_7
		UsableKeyDict[9]	= app.DIK_8
		UsableKeyDict[10]	= app.DIK_9
		UsableKeyDict[11]	= app.DIK_GRAVE + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[12]	= app.DIK_0 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[13]	= app.DIK_1 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[14]	= app.DIK_2 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[15]	= app.DIK_3 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[16]	= app.DIK_4 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[17]	= app.DIK_5 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[18]	= app.DIK_6 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[19]	= app.DIK_7 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[20]	= app.DIK_8 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[21]	= app.DIK_9 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL    
		UsableKeyDict[22]	= app.DIK_GRAVE + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[23]	= app.DIK_0 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[24]	= app.DIK_1 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[25]	= app.DIK_2 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[26]	= app.DIK_3 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[27]	= app.DIK_4 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[28]	= app.DIK_5 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[29]	= app.DIK_6 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[30]	= app.DIK_7 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[31]	= app.DIK_8 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[32]	= app.DIK_9 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[33]	= app.DIK_GRAVE + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[34]	= app.DIK_0 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[35]	= app.DIK_1 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[36]	= app.DIK_2 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[37]	= app.DIK_3 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[38]	= app.DIK_4 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[39]	= app.DIK_5 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[40]	= app.DIK_6 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[41]	= app.DIK_7 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[42]	= app.DIK_8 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[43]	= app.DIK_9 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[44]	= app.DIK_F1
		UsableKeyDict[45]	= app.DIK_F2
		UsableKeyDict[46]	= app.DIK_F3
		UsableKeyDict[47]	= app.DIK_F4
		UsableKeyDict[48]	= app.DIK_F5
		UsableKeyDict[49]	= app.DIK_F6
		UsableKeyDict[50]	= app.DIK_F7
		UsableKeyDict[51]	= app.DIK_F8
		UsableKeyDict[52]	= app.DIK_F9
		UsableKeyDict[53]	= app.DIK_F10
		UsableKeyDict[54]	= app.DIK_F1 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[55]	= app.DIK_F2 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[56]	= app.DIK_F3 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[57]	= app.DIK_F4 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[58]	= app.DIK_F5 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[59]	= app.DIK_F6 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[60]	= app.DIK_F7 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[61]	= app.DIK_F8 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[62]	= app.DIK_F9 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[63]	= app.DIK_F10 + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[64]	= app.DIK_F1 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[65]	= app.DIK_F2 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[66]	= app.DIK_F3 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[67]	= app.DIK_F4 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[68]	= app.DIK_F5 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[69]	= app.DIK_F6 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[70]	= app.DIK_F7 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[71]	= app.DIK_F8 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[72]	= app.DIK_F9 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[73]	= app.DIK_F10 + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[74]	= app.DIK_F1 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[75]	= app.DIK_F2 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[76]	= app.DIK_F3 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[77]	= app.DIK_F4 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[78]	= app.DIK_F5 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[79]	= app.DIK_F6 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[80]	= app.DIK_F7 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[81]	= app.DIK_F8 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[82]	= app.DIK_F9 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[83]	= app.DIK_F10 + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[84]	= app.DIK_LCONTROL
		UsableKeyDict[85]	= app.DIK_LALT    
		UsableKeyDict[86]	= app.DIK_LSHIFT  
		UsableKeyDict[87]	= app.DIK_SYSRQ   
		UsableKeyDict[88]	= app.DIK_SPACE   
		UsableKeyDict[89]	= app.DIK_TAB     
		UsableKeyDict[90]	= app.DIK_UP   
		UsableKeyDict[91]	= app.DIK_DOWN 
		UsableKeyDict[92]	= app.DIK_LEFT 
		UsableKeyDict[93]	= app.DIK_RIGHT
		UsableKeyDict[94]	= app.DIK_Q
		UsableKeyDict[95]	= app.DIK_W
		UsableKeyDict[96]	= app.DIK_E
		UsableKeyDict[97]	= app.DIK_R
		UsableKeyDict[98]	= app.DIK_T
		UsableKeyDict[99]	= app.DIK_Y
		UsableKeyDict[100]	= app.DIK_U
		UsableKeyDict[101]	= app.DIK_I
		UsableKeyDict[102]	= app.DIK_O
		UsableKeyDict[103]	= app.DIK_P
		UsableKeyDict[104]	= app.DIK_A
		UsableKeyDict[105]	= app.DIK_S
		UsableKeyDict[106]	= app.DIK_D
		UsableKeyDict[107]	= app.DIK_F
		UsableKeyDict[108]	= app.DIK_G
		UsableKeyDict[109]	= app.DIK_H
		UsableKeyDict[110]	= app.DIK_J
		UsableKeyDict[111]	= app.DIK_K
		UsableKeyDict[112]	= app.DIK_L
		UsableKeyDict[113]	= app.DIK_Z
		UsableKeyDict[114]	= app.DIK_X
		UsableKeyDict[115]	= app.DIK_C
		UsableKeyDict[116]	= app.DIK_V
		UsableKeyDict[117]	= app.DIK_B
		UsableKeyDict[118]	= app.DIK_N
		UsableKeyDict[119]	= app.DIK_M
		UsableKeyDict[120]	= app.DIK_COMMA
		UsableKeyDict[121]	= app.DIK_PERIOD
		UsableKeyDict[122]	= app.DIK_Q + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[123]	= app.DIK_W + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[124]	= app.DIK_E + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[125]	= app.DIK_R + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[126]	= app.DIK_T + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[127]	= app.DIK_Y + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[128]	= app.DIK_U + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[129]	= app.DIK_I + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[130]	= app.DIK_O + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[131]	= app.DIK_P + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[132]	= app.DIK_A + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[133]	= app.DIK_S + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[134]	= app.DIK_D + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[135]	= app.DIK_F + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[136]	= app.DIK_G + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[137]	= app.DIK_H + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[138]	= app.DIK_J + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[139]	= app.DIK_K + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[140]	= app.DIK_L + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[141]	= app.DIK_Z + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[142]	= app.DIK_X + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[143]	= app.DIK_C + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[144]	= app.DIK_V + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[145]	= app.DIK_B + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[146]	= app.DIK_N + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[147]	= app.DIK_M + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[148]	= app.DIK_COMMA + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL 
		UsableKeyDict[149]	= app.DIK_PERIOD + app.DIK_LCONTROL + self.ADDKEYBUFFERCONTROL
		UsableKeyDict[150]	= app.DIK_Q + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[151]	= app.DIK_W + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[152]	= app.DIK_E + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[153]	= app.DIK_R + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[154]	= app.DIK_T + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[155]	= app.DIK_Y + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[156]	= app.DIK_U + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[157]	= app.DIK_I + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[158]	= app.DIK_O + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[159]	= app.DIK_P + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[160]	= app.DIK_A + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[161]	= app.DIK_S + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[162]	= app.DIK_D + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[163]	= app.DIK_F + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[164]	= app.DIK_G + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[165]	= app.DIK_H + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[166]	= app.DIK_J + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[167]	= app.DIK_K + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[168]	= app.DIK_L + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[169]	= app.DIK_Z + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[170]	= app.DIK_X + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[171]	= app.DIK_C + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[172]	= app.DIK_V + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[173]	= app.DIK_B + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[174]	= app.DIK_N + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[175]	= app.DIK_M + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[176]	= app.DIK_COMMA + app.DIK_LALT + self.ADDKEYBUFFERALT 
		UsableKeyDict[177]	= app.DIK_PERIOD + app.DIK_LALT + self.ADDKEYBUFFERALT
		UsableKeyDict[178]	= app.DIK_Q + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[179]	= app.DIK_W + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[180]	= app.DIK_E + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[181]	= app.DIK_R + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[182]	= app.DIK_T + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[183]	= app.DIK_Y + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[184]	= app.DIK_U + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[185]	= app.DIK_I + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[186]	= app.DIK_O + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[187]	= app.DIK_P + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[188]	= app.DIK_A + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[189]	= app.DIK_S + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[190]	= app.DIK_D + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[191]	= app.DIK_F + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[192]	= app.DIK_G + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[193]	= app.DIK_H + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[194]	= app.DIK_J + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[195]	= app.DIK_K + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[196]	= app.DIK_L + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[197]	= app.DIK_Z + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[198]	= app.DIK_X + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[199]	= app.DIK_C + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[200]	= app.DIK_V + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[201]	= app.DIK_B + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[202]	= app.DIK_N + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[203]	= app.DIK_M + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[204]	= app.DIK_COMMA + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT 
		UsableKeyDict[205]	= app.DIK_PERIOD + app.DIK_LSHIFT + self.ADDKEYBUFFERSHIFT
		UsableKeyDict[206]	= app.DIK_NUMPAD0
		UsableKeyDict[207]	= app.DIK_NUMPAD1
		UsableKeyDict[208]	= app.DIK_NUMPAD2
		UsableKeyDict[209]	= app.DIK_NUMPAD3
		UsableKeyDict[210]	= app.DIK_NUMPAD4
		UsableKeyDict[211]	= app.DIK_NUMPAD5
		UsableKeyDict[212]	= app.DIK_NUMPAD6
		UsableKeyDict[213]	= app.DIK_NUMPAD7
		UsableKeyDict[214]	= app.DIK_NUMPAD8
		UsableKeyDict[215]	= app.DIK_NUMPAD9
		UsableKeyDict[216]	= app.DIK_ADD
		UsableKeyDict[217]	= app.DIK_SUBTRACT
		UsableKeyDict[218]	= app.DIK_PGUP
		UsableKeyDict[219]	= app.DIK_PGDN
		UsableKeyDict[220] = app.DIK_NUMLOCK

		self.UsableKeyDict = UsableKeyDict
		
	## =================== 키 셋팅민 변경에 필요한 Dick 들 셋팅 부분 ===================
	
