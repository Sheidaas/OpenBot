import app
import ui
import playerm2g2
import m2netm2g

if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
	import uiCommon
	import localeInfo

class GameButtonWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow("UIScript/gamewindow.py")
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			self.popup = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self, filename):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, filename)
		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		try:
			self.gameButtonDict={
				"STATUS" : self.GetChild("StatusPlusButton"),
				"SKILL" : self.GetChild("SkillPlusButton"),
				"QUEST" : self.GetChild("QuestButton"),
				"HELP" : self.GetChild("HelpButton"),
				"BUILD" : self.GetChild("BuildGuildBuilding"),
				"EXIT_OBSERVER" : self.GetChild("ExitObserver"),
			}
			
			if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
				self.gameButtonDict["GUILDWAR"] = self.GetChild("GuildWarButton")
				self.gameButtonDict["GUILDWAR"].SetEvent(ui.__mem_func__(self.__RequestGuildWarEnter))

			self.gameButtonDict["EXIT_OBSERVER"].SetEvent(ui.__mem_func__(self.__OnClickExitObserver))

			if app.ENABLE_GEM_SYSTEM:
				posx, posy = self.gameButtonDict["SKILL"].GetGlobalPosition()
				self.gameButtonDict["SKILL"].SetPosition(posx, posy - 25 )
				
				posx, posy = self.gameButtonDict["BUILD"].GetGlobalPosition()
				self.gameButtonDict["BUILD"].SetPosition(posx, posy - 25 )
				
				posx, posy = self.gameButtonDict["EXIT_OBSERVER"].GetGlobalPosition()
				self.gameButtonDict["EXIT_OBSERVER"].SetPosition(posx, posy - 25 )

		except Exception, msg:
			import dbg
			dbg.TraceError("GameButtonWindow.LoadScript - %s" % (msg))
			app.Abort()
			return False

		self.__HideAllGameButton()
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.SetObserverMode(playerm2g2.IsObserverMode(),True)
		else:
			self.SetObserverMode(playerm2g2.IsObserverMode())
		return True
		
	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def __RequestGuildWarEnter(self):
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.GAME_GUILDWAR_NOW_JOIN)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptGuildWarEnter))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.ClosePopUpDialog))
			questionDialog.Open()
			self.popup = questionDialog
			
		def AcceptGuildWarEnter(self):
			m2netm2g.SendChatPacket("/guildwar_request_enter")
			if self.popup:
				self.popup.Close()
			self.popup = None
		
		def ClosePopUpDialog(self):
			if self.popup:
				self.popup.Close()
			self.popup = None
		
		def ShowGuildWarButton(self):
			self.gameButtonDict["GUILDWAR"].Show()
		
		def HideGuildWarButton(self):
			self.gameButtonDict["GUILDWAR"].Hide()

	def Destroy(self):
		for key in self.gameButtonDict:
			self.gameButtonDict[key].SetEvent(0)

		self.gameButtonDict={}

		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			self.popup = None

	def SetButtonEvent(self, name, event):
		try:
			self.gameButtonDict[name].SetEvent(event)
		except Exception, msg:
			print "GameButtonWindow.LoadScript - %s" % (msg)
			app.Abort()
			return

	def ShowBuildButton(self):
		self.gameButtonDict["BUILD"].Show()

	def HideBuildButton(self):
		self.gameButtonDict["BUILD"].Hide()

	def CheckGameButton(self):

		if not self.IsShow():
			return

		statusPlusButton=self.gameButtonDict["STATUS"]
		skillPlusButton=self.gameButtonDict["SKILL"]
		helpButton=self.gameButtonDict["HELP"]

		if playerm2g2.GetStatus(playerm2g2.STAT) > 0:
			statusPlusButton.Show()
		else:
			statusPlusButton.Hide()

		if self.__IsSkillStat():
			skillPlusButton.Show()
		else:
			skillPlusButton.Hide()

		if 0 == playerm2g2.GetPlayTime():
			helpButton.Show()
		else:
			helpButton.Hide()

	def __IsSkillStat(self):
		if playerm2g2.GetStatus(playerm2g2.SKILL_ACTIVE) > 0:
			return True

		return False

	def __OnClickExitObserver(self):
		m2netm2g.SendChatPacket("/observer_exit")

	def __HideAllGameButton(self):
		for btn in self.gameButtonDict.values():
			btn.Hide()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def SetObserverMode(self, isEnable, isButtonShow):
			if isButtonShow:
				if isEnable:
					self.gameButtonDict["EXIT_OBSERVER"].Show()
				else:
					self.gameButtonDict["EXIT_OBSERVER"].Hide()
	else:
		def SetObserverMode(self, isEnable):
			if isEnable:
				self.gameButtonDict["EXIT_OBSERVER"].Show()
			else:
				self.gameButtonDict["EXIT_OBSERVER"].Hide()
