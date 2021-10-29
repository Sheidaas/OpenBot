import ui
import m2netm2g
import wndMgr
import dbg
import app
import event
import _weakref
import localeInfo
import uiScriptLocale
import snd
import musicInfo
import systemSetting
import uiToolTip

LOCALE_PATH = "uiscript/"+uiScriptLocale.CODEPAGE+"_"

class SelectEmpireWindow(ui.ScriptWindow):
	EMPIRE_NAME = { 
			m2netm2g.EMPIRE_A : localeInfo.EMPIRE_A, 
			m2netm2g.EMPIRE_B : localeInfo.EMPIRE_B, 
			m2netm2g.EMPIRE_C : localeInfo.EMPIRE_C 
		}
	EMPIRE_NAME_COLOR = { 
			m2netm2g.EMPIRE_A : (0.7450, 0, 0), 
			m2netm2g.EMPIRE_B : (0.8666, 0.6156, 0.1843), 
			m2netm2g.EMPIRE_C : (0.2235, 0.2549, 0.7490) 
		}

	EMPIRE_DESCRIPTION_TEXT_FILE_NAME = {	
		m2netm2g.EMPIRE_A : uiScriptLocale.EMPIREDESC_A,
		m2netm2g.EMPIRE_B : uiScriptLocale.EMPIREDESC_B,
		m2netm2g.EMPIRE_C : uiScriptLocale.EMPIREDESC_C, }

	class EmpireButton(ui.Window):
		def __init__(self, owner, arg):
			ui.Window.__init__(self)
			self.owner = owner
			self.arg = arg
		def OnMouseOverIn(self):
			self.owner.OnOverInEmpire(self.arg)

			text = None
			if m2netm2g.EMPIRE_A == self.arg :
				text = localeInfo.EMPIRE_A
			elif m2netm2g.EMPIRE_B == self.arg :
				text = localeInfo.EMPIRE_B
			elif m2netm2g.EMPIRE_C == self.arg :
				text = localeInfo.EMPIRE_C
			else :
				print "ERROR Empire Button"

		def OnMouseOverOut(self):
			self.owner.OnOverOutEmpire(self.arg)
			self.owner.OverOutToolTip()

		def OnMouseLeftButtonDown(self):
			if self.owner.empireID != self.arg:
				self.owner.OnSelectEmpire(self.arg)

	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet(self.descIndex)

	def __init__(self, stream):
		#print "NEW EMPIRE WINDOW  ----------------------------------------------------------------------------"
		ui.ScriptWindow.__init__(self)
		m2netm2g.SetPhaseWindow(m2netm2g.PHASE_WINDOW_EMPIRE, self)

		self.stream=stream
		self.empireID = m2netm2g.GetEmpireID()

		self.descIndex=0
		self.empireArea = {}
		self.empireAreaFlag = {}
		self.empireFlag = {}
		self.empireAreaButton = {}
		self.empireAreaCurAlpha = { m2netm2g.EMPIRE_A:0.0, m2netm2g.EMPIRE_B:0.0, m2netm2g.EMPIRE_C:0.0 }
		self.empireAreaDestAlpha = { m2netm2g.EMPIRE_A:0.0, m2netm2g.EMPIRE_B:0.0, m2netm2g.EMPIRE_C:0.0 }
		self.empireAreaFlagCurAlpha = { m2netm2g.EMPIRE_A:0.0, m2netm2g.EMPIRE_B:0.0, m2netm2g.EMPIRE_C:0.0 }
		self.empireAreaFlagDestAlpha = { m2netm2g.EMPIRE_A:0.0, m2netm2g.EMPIRE_B:0.0, m2netm2g.EMPIRE_C:0.0 }
		self.empireFlagCurAlpha = { m2netm2g.EMPIRE_A:0.0, m2netm2g.EMPIRE_B:0.0, m2netm2g.EMPIRE_C:0.0 }
		self.empireFlagDestAlpha = { m2netm2g.EMPIRE_A:0.0, m2netm2g.EMPIRE_B:0.0, m2netm2g.EMPIRE_C:0.0 }

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		m2netm2g.SetPhaseWindow(m2netm2g.PHASE_WINDOW_EMPIRE, 0)
		#print "---------------------------------------------------------------------------- DELETE EMPIRE WINDOW"

	def Close(self):
		#print "---------------------------------------------------------------------------- CLOSE EMPIRE WINDOW"		

		self.ClearDictionary()
		self.leftButton = None
		self.rightButton = None
		self.selectButton = None
		self.exitButton = None
		self.textBoard = None
		self.descriptionBox = None
		self.empireArea = None
		self.empireAreaButton = None
		
		if musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.selectMusic)

		self.empireName = None
		self.EMPIRE_NAME = None
		self.EMPIRE_NAME_COLOR = None
		self.toolTip = None
		self.ShowToolTip = None
		self.btnPrev = None
		self.btnNext = None

		self.KillFocus()
		self.Hide()

		app.HideCursor()
		event.Destroy()

	def Open(self):
		#print "OPEN EMPIRE WINDOW ----------------------------------------------------------------------------"

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("SelectEmpireWindow")
		self.Show()	

		if not self.__LoadScript(uiScriptLocale.LOCALE_UISCRIPT_PATH + "SelectEmpireWindow.py"):
			dbg.TraceError("SelectEmpireWindow.Open - __LoadScript Error")
			return

		self.OnSelectEmpire(self.empireID)
		self.__CreateButtons()
		self.__CreateDescriptionBox()
		app.ShowCursor()

		if musicInfo.selectMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.selectMusic)	
			
			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.ClearToolTip()
				
			self.ShowToolTip = False

	def __CreateButtons(self):
		for key, img in self.empireArea.items():

			img.SetAlpha(0.0)

			(x, y) = img.GetGlobalPosition()
			btn = self.EmpireButton(_weakref.proxy(self), key)
			btn.SetParent(self)
			btn.SetPosition(x, y)
			btn.SetSize(img.GetWidth(), img.GetHeight())
			btn.Show()
			self.empireAreaButton[key] = btn

	def __CreateDescriptionBox(self):
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.Show()

	def OnOverInEmpire(self, arg):
		self.empireAreaDestAlpha[arg] = 1.0

	def OnOverOutEmpire(self, arg):
		if arg != self.empireID:
			self.empireAreaDestAlpha[arg] = 0.0

	def OnSelectEmpire(self, arg):
		for key in self.empireArea.keys():
			self.empireAreaDestAlpha[key] = 0.0
			self.empireAreaFlagDestAlpha[key] = 0.0
			self.empireFlagDestAlpha[key] = 0.0
		self.empireAreaDestAlpha[arg] = 1.0
		self.empireAreaFlagDestAlpha[arg] = 1.0
		self.empireFlagDestAlpha[arg] = 1.0
		self.empireID = arg

		self.empireName.SetText(self.EMPIRE_NAME.get(self.empireID, ""))
		rgb = self.EMPIRE_NAME_COLOR[self.empireID]
		self.empireName.SetFontColor(rgb[0], rgb[1], rgb[2])
		snd.PlaySound("sound/ui/click.wav")

		event.ClearEventSet(self.descIndex)
		if self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME.has_key(arg):
			self.descIndex = event.RegisterEventSet(self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME[arg])
			
			event.SetFontColor(self.descIndex, 0.7843, 0.7843, 0.7843)

			if localeInfo.IsARABIC():
				event.SetEventSetWidth(self.descIndex, 170)
			else:
				event.SetRestrictedCount(self.descIndex, 35)
		
		if event.BOX_VISIBLE_LINE_COUNT >= event.GetTotalLineCount(self.descIndex) :
			self.btnPrev.Hide()
			self.btnNext.Hide()
		else :
			self.btnPrev.Show()
			self.btnNext.Show()		

	def PrevDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - event.BOX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def NextDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + event.BOX_VISIBLE_LINE_COUNT)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)	
		except:
			import exception
			exception.Abort("SelectEmpireWindow.__LoadScript.LoadObject")

		try:
			GetObject=self.GetChild
			self.leftButton		= GetObject("left_button")
			self.rightButton	= GetObject("right_button")
			self.selectButton	= GetObject("select_button")
			self.exitButton		= GetObject("exit_button")
			self.textBoard		= GetObject("text_board")
			self.empireArea[m2netm2g.EMPIRE_A]	= GetObject("EmpireArea_A")
			self.empireArea[m2netm2g.EMPIRE_B]	= GetObject("EmpireArea_B")
			self.empireArea[m2netm2g.EMPIRE_C]	= GetObject("EmpireArea_C")
			self.empireAreaFlag[m2netm2g.EMPIRE_A]	= GetObject("EmpireAreaFlag_A")
			self.empireAreaFlag[m2netm2g.EMPIRE_B]	= GetObject("EmpireAreaFlag_B")
			self.empireAreaFlag[m2netm2g.EMPIRE_C]	= GetObject("EmpireAreaFlag_C")
			self.empireFlag[m2netm2g.EMPIRE_A]	= GetObject("EmpireFlag_A")
			self.empireFlag[m2netm2g.EMPIRE_B]	= GetObject("EmpireFlag_B")
			self.empireFlag[m2netm2g.EMPIRE_C]	= GetObject("EmpireFlag_C")
			GetObject("prev_text_button").SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			GetObject("next_text_button").SetEvent(ui.__mem_func__(self.NextDescriptionPage))

			self.empireName = GetObject("EmpireName")	
			self.btnPrev = GetObject("prev_text_button")
			self.btnNext = GetObject("next_text_button")
				
			GetObject("left_button").ShowToolTip	= lambda arg = uiScriptLocale.EMPIRE_PREV : self.OverInToolTip(arg)
			GetObject("left_button").HideToolTip	= lambda : self.OverOutToolTip()
			GetObject("right_button").ShowToolTip	= lambda arg = uiScriptLocale.EMPIRE_NEXT : self.OverInToolTip(arg)
			GetObject("right_button").HideToolTip	= lambda : self.OverOutToolTip()
				
			GetObject("prev_text_button").ShowToolTip	= lambda arg = uiScriptLocale.EMPIRE_PREV : self.OverInToolTip(arg)
			GetObject("prev_text_button").HideToolTip	= lambda : self.OverOutToolTip()
			GetObject("next_text_button").ShowToolTip	= lambda arg = uiScriptLocale.EMPIRE_NEXT : self.OverInToolTip(arg)
			GetObject("next_text_button").HideToolTip	= lambda : self.OverOutToolTip()
				
			GetObject("select_button").ShowToolTip	= lambda arg = uiScriptLocale.EMPIRE_SELECT : self.OverInToolTip(arg)
			GetObject("select_button").HideToolTip	= lambda : self.OverOutToolTip()
			GetObject("exit_button").ShowToolTip	= lambda arg = uiScriptLocale.EMPIRE_EXIT : self.OverInToolTip(arg)
			GetObject("exit_button").HideToolTip	= lambda : self.OverOutToolTip()
		except:
			import exception
			exception.Abort("SelectEmpireWindow.__LoadScript.BindObject")					

		self.selectButton.SetEvent(ui.__mem_func__(self.ClickSelectButton))
		self.exitButton.SetEvent(ui.__mem_func__(self.ClickExitButton))
		self.leftButton.SetEvent(ui.__mem_func__(self.ClickRightButton))
		self.rightButton.SetEvent(ui.__mem_func__(self.ClickLeftButton))

		for flag in self.empireAreaFlag.values():
			flag.SetAlpha(0.0)
		for flag in self.empireFlag.values():
			flag.SetAlpha(0.0)

		return 1

	def ClickLeftButton(self):
		self.empireID-=1
		if self.empireID<1:
			self.empireID=3

		self.OnSelectEmpire(self.empireID)

	def ClickRightButton(self):
		self.empireID+=1
		if self.empireID>3:
			self.empireID=1

		self.OnSelectEmpire(self.empireID)

	def ClickSelectButton(self):
		m2netm2g.SendSelectEmpirePacket(self.empireID)
		self.stream.SetSelectCharacterPhase()
		self.Hide()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()
		self.Hide()

	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7))
		self.descriptionBox.SetIndex(self.descIndex)

		self.__UpdateAlpha(self.empireArea, self.empireAreaCurAlpha, self.empireAreaDestAlpha)
		self.__UpdateAlpha(self.empireAreaFlag, self.empireAreaFlagCurAlpha, self.empireAreaFlagDestAlpha)
		self.__UpdateAlpha(self.empireFlag, self.empireFlagCurAlpha, self.empireFlagDestAlpha)

		self.ToolTipProgress()

	def __UpdateAlpha(self, dict, curAlphaDict, destAlphaDict):
		for key, img in dict.items():

			curAlpha = curAlphaDict[key]
			destAlpha = destAlphaDict[key]

			if abs(destAlpha - curAlpha) / 10 > 0.0001:
				curAlpha += (destAlpha - curAlpha) / 7
			else:
				curAlpha = destAlpha

			curAlphaDict[key] = curAlpha
			img.SetAlpha(curAlpha)

	def OnPressEscapeKey(self):
		self.ClickExitButton()
		return True

	def OverInToolTip(self, arg) :	
		arglen = len(str(arg))
		pos_x, pos_y = wndMgr.GetMousePosition()
			
		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(11 * arglen)
		self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.toolTip.AppendTextLine(str(arg), 0xffffff00)
		self.toolTip.Show()
		self.ShowToolTip = True
	
	def OverOutToolTip(self) :
		self.toolTip.Hide()
		self.ShowToolTip = False
			
	def ToolTipProgress(self) :
		if self.ShowToolTip :
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
			
	def OnPressExitKey(self):
		self.stream.SetLoginPhase()
		self.Hide()
		return True

class ReselectEmpireWindow(SelectEmpireWindow):
	def ClickSelectButton(self):
		m2netm2g.SendSelectEmpirePacket(self.empireID)
		self.stream.SetCreateCharacterPhase()
		self.Hide()

	def ClickExitButton(self):
		self.stream.SetLoginPhase()
		self.Hide()
