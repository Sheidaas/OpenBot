import app
import ui
import event
import ranking
import localeInfo
import uiScriptLocale
import uiCommon
import m2netm2g
import background
import playerm2g2
import uiToolTip
import wndMgr

class BattleFieldWindow(ui.ScriptWindow):

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

	SHOW_LINE_COUNT_MAX = 18
	DEFAULT_DESC_Y	= 7
	DESCRIPTION_FILE_NAME = uiScriptLocale.DESC_BATTLE_FIELD_PATH
	M2EMPIREICON = {
			0 : "d:/ymir work/ui/public/battle/empire_empty.sub",
			1 : "d:/ymir work/ui/public/battle/empire_shinsu.sub",
			2 : "d:/ymir work/ui/public/battle/empire_chunjo.sub",
			3 : "d:/ymir work/ui/public/battle/empire_jinno.sub",
		}

	def __init__(self):
		self.rankPosX = 207;
		self.rankNameX = 262;
		self.rankEmpireX = 388;
		self.rankRecordX = 435;
		self.rankCoverX = 196;
		self.state = "ACCUM_RANK"
		self.tabDict = None
		self.tabButtonDict = None
		self.ResultSlotList = {}
		self.ResutlSlotCoverList = {}
		self.MyResultSlotList = []
		self.MyResultSlotCoverList = []
		self.descIndex = 0
		self.desc_y	= self.DEFAULT_DESC_Y
		self.popup = None
		self.EnterBtnPressd = False
		self.EnterBtnDelay = 0
		self.buttontooltip		= None
		self.ShowButtonToolTip	= False
		self.leftOpenTime = 0
		self.leftEndTime = 0

		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "BattleFieldWindow.py")
				self.rankPosX = 271
				self.rankNameX = 144
				self.rankEmpireX = 100
				self.rankRecordX = 42
				self.rankCoverX = 20
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/BattleFieldWindow.py")			
				self.rankPosX = 207
				self.rankNameX = 262
				self.rankEmpireX = 388
				self.rankRecordX = 435
				self.rankCoverX = 196
					
			getChild = self.GetChild
			self.textBoard = getChild("explanation")
			self.btnPrev = getChild("prev_button")
			self.btnNext = getChild("next_button")
			self.btnEnter = getChild("enter_button")
			self.TitleBar = getChild("titlebar")
			self.textNotice = getChild("notice")
			self.textPoint = getChild("my_point")
			
			if localeInfo.IsARABIC():
				self.btnPrev.LeftRightReverse()
				self.btnNext.LeftRightReverse()
			
			##Job Description##
			self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
			self.btnEnter.SetEvent(ui.__mem_func__(self.EnterBattleField))
			self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
		
			##Job Description Box##
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Show()
			self.descriptionBox.SetParent(self.textBoard)

			self.__BindObject()
			self.__BindEvent()
			self.__DescBattleField()
			self.__MakeRankingUI()
			
			self.buttontooltip = uiToolTip.ToolTip()
			self.buttontooltip.ClearToolTip()
		except:
			import exception
			exception.Abort("BattleFieldWindow.__LoadWindow.UIScript/BattleFieldWindow.py")

	def __BindObject(self):
		self.tabDict = {
			"CURRENT_RANK"	: self.GetChild("tab_01"),
			"ACCUM_RANK"	: self.GetChild("tab_02"),
		}

		self.tabButtonDict = {
			"CURRENT_RANK"	: self.GetChild("tab_button_01"),
			"ACCUM_RANK"	: self.GetChild("tab_button_02"),
		}
		
		if localeInfo.IsARABIC():
			for (tabKey, tabImage) in self.tabDict.items():
				tabImage.LeftRightReverse()
		

	def __BindEvent(self):
		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)
				
		self.tabButtonDict["CURRENT_RANK"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.WEEKLY_RANKING)
		self.tabButtonDict["CURRENT_RANK"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.tabButtonDict["ACCUM_RANK"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.TOTAL_RANKING)
		self.tabButtonDict["ACCUM_RANK"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

	def __OnClickTabButton(self, stateKey):
		self.SetState(stateKey)


	def OverInToolTipButton(self, btnText, text_len = 0):
	
		if self.buttontooltip:
			
			if 0 == text_len:
				arglen = len(str(btnText))
			else:
				arglen = text_len
				
			pos_x, pos_y = wndMgr.GetMousePosition()
			
			self.buttontooltip.ClearToolTip()
			self.buttontooltip.SetThinBoardSize(11 * arglen)
			self.buttontooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)
			self.buttontooltip.AppendTextLine(btnText, 0xffffffff)
			self.buttontooltip.Show()
			self.buttontooltip.SetTop()
			self.ShowButtonToolTip = True

	def OverOutToolTipButton(self):
	
		if self.buttontooltip:
			self.buttontooltip.Hide()
			self.ShowButtonToolTip = False

	def ButtonToolTipProgress(self):
		if self.buttontooltip and self.ShowButtonToolTip:
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.buttontooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)

	def __DescBattleField(self):
		event.ClearEventSet(self.descIndex)

		self.descIndex = event.RegisterEventSet(self.DESCRIPTION_FILE_NAME)
		
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
		event.SetVisibleLineCount(self.descIndex, self.SHOW_LINE_COUNT_MAX)

		if localeInfo.IsARABIC():
			event.SetEventSetWidth(self.descIndex, 157)
			
		event.SetRestrictedCount(self.descIndex, 47)
		event.AllProcesseEventSet(self.descIndex)

		if event.BOX_VISIBLE_LINE_COUNT >= event.GetTotalLineCount(self.descIndex) :
			self.btnPrev.Hide()
			self.btnNext.Hide()
		else :
			self.btnPrev.Show()
			self.btnNext.Show()

	##Description Prev & Next Button##
	def PrevDescriptionPage(self):
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		decrease_count = self.SHOW_LINE_COUNT_MAX
		
		if cur_start_line - decrease_count < 0:
			return;

		event.SetVisibleStartLine(self.descIndex, cur_start_line - decrease_count)
		self.desc_y += ( line_height * decrease_count )
	
	def NextDescriptionPage(self):
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		total_line_count	= event.GetProcessedLineCount(self.descIndex)
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		increase_count = self.SHOW_LINE_COUNT_MAX
		
		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return
		
		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.desc_y -= ( line_height * increase_count )

	def EnterBattleField(self):
		if playerm2g2.IsBattleFieldOpen() == False:
			self.DisableEnterButton()
			return
				
		m2netm2g.SendChatPacket("/goto_battle");
		self.EnterBtnPressd = True
		self.EnterBtnDelay = app.GetGlobalTime() + 5000;
		self.DisableEnterButton()
		
	def DisableEnterButton(self):
		self.btnEnter.Down()
		self.btnEnter.Disable()
		
	def EnableEnterButton(self):
		self.btnEnter.SetUp()
		self.btnEnter.Enable()
		
	def OnUpdate(self):
	
		self.ButtonToolTipProgress()
	
		if self.EnterBtnPressd == True and self.EnterBtnDelay < app.GetGlobalTime():
			self.EnterBtnPressd = False 
			self.EnableEnterButton()			
		
		(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+self.desc_y))
		self.descriptionBox.SetIndex(self.descIndex)
		self.descriptionBox.SetTop()

	def SetState(self, stateKey):
		self.state = stateKey

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if stateKey!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.itervalues():
			tabValue.Hide()

		self.tabDict[stateKey].Show()

		if self.state != "ACCUM_RANK":			
			self.RefreshRankingList(ranking.TYPE_RK_SOLO, ranking.SOLO_RK_CATEGORY_BF_WEAK)
		else:
			self.RefreshRankingList(ranking.TYPE_RK_SOLO, ranking.SOLO_RK_CATEGORY_BF_TOTAL)

	def SetPoint(self, point):
		self.textPoint.SetText(str(point))
		
	def SetBattleFieldLeftTime(self, leftOpen, leftEnd):
		self.leftOpenTime = leftOpen
		self.leftEndTime = leftEnd
		
	def SetNotice(self, enable):
		if enable == False:
			self.textNotice.SetText(uiScriptLocale.BATTLE_FIELD_OPERATION_TIME_NA)
		else:	
			if self.leftOpenTime < 0 or self.leftEndTime < 0:
				self.textNotice.SetText(uiScriptLocale.BATTLE_FIELD_OPERATION_TIME_NA)
				
			if self.leftOpenTime < self.leftEndTime:
				self.textNotice.SetText(uiScriptLocale.BATTLE_FIELD_OPERATION_TIME_OPEN % (localeInfo.SecondToColonTypeHM(self.leftOpenTime), localeInfo.SecondToH(self.leftEndTime - self.leftOpenTime)))
			elif self.leftOpenTime > self.leftEndTime:
				self.textNotice.SetText(uiScriptLocale.BATTLE_FIELD_OPERATION_TIME_END % (localeInfo.SecondToColonTypeHM(self.leftEndTime)))
			
		
	def Open(self):
		self.SetPoint(playerm2g2.GetBattlePoint())
		self.SetNotice(playerm2g2.GetBattleFieldEnable())
		if playerm2g2.IsBattleFieldOpen() == False:
			self.DisableEnterButton()
		else:
			self.EnableEnterButton()
		self.SetState("CURRENT_RANK")
		self.Show()

	def Close(self):
		self.Hide()
		
		if self.buttontooltip:
			self.buttontooltip.Hide()
			self.ShowButtonToolTip	= False

	def Destroy(self):
		self.descIndex = 0
		self.desc_y	=  self.DEFAULT_DESC_Y
		self.Hide()
	
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __MakeRankingUI(self):
		yPos = 335
		
		self.MyResultSlotList = self.__MakeResultSlotUI(yPos)	
		self.MyResultSlotCoverList = self.__MakeResultSlotCoverUI(yPos)

		for i in range(0,10):
			yPos = 93 + i * 24
			self.ResultSlotList[i] = self.__MakeResultSlotUI(yPos)
			self.ResutlSlotCoverList[i] = self.__MakeResultSlotCoverUI(yPos)
			self.ResutlSlotCoverList[i][0].Hide()

	def __MakeResultSlotUI(self, yPos):
		## 순위
		RankingSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", self.rankPosX , yPos)
		RankingSlotImage.SetAlpha(0)
		if localeInfo.IsARABIC():
			RankingSlotImage.LeftRightReverse()
		RankingSlot = ui.MakeTextLine(RankingSlotImage)
		self.Children.append(RankingSlotImage)
		self.Children.append(RankingSlot)

		## 이름
		NameImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_04.sub", self.rankNameX , yPos)
		NameImage.SetAlpha(0)			
		if localeInfo.IsARABIC():
			NameImage.LeftRightReverse()	
		NameSlot = ui.MakeTextLine(NameImage)
		self.Children.append(NameImage)
		self.Children.append(NameSlot)
		
		## 국가
		EmpireSlotImage = ui.MakeImageBox(self, self.M2EMPIREICON[0], self.rankEmpireX , yPos+2)
		EmpireSlotImage.SetAlpha(1)
		if localeInfo.IsARABIC():
			EmpireSlotImage.LeftRightReverse()
		self.Children.append(EmpireSlotImage)
		#self.Children.append(EmpireSlot)

		## 기록
		RecordSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", self.rankRecordX , yPos)
		RecordSlotImage.SetAlpha(0)
		if localeInfo.IsARABIC():
			RecordSlotImage.LeftRightReverse()
		RecordSlot = ui.MakeTextLine(RecordSlotImage)
		self.Children.append(RecordSlotImage)
		self.Children.append(RecordSlot)

		rankingslotlist = []
		rankingslotlist.append(RankingSlot)
		rankingslotlist.append(NameSlot)
		rankingslotlist.append(EmpireSlotImage)
		rankingslotlist.append(RecordSlot)

		return rankingslotlist

	def __MakeResultSlotCoverUI(self, yPos):
		itemSlotCoverImage = ui.MakeImageBox(self,"d:/ymir work/ui/public/battle/rank_list.sub", self.rankCoverX , yPos)
		itemSlotCoverImage.SetAlpha(1)
		if localeInfo.IsARABIC():
			itemSlotCoverImage.LeftRightReverse()
		self.Children.append(itemSlotCoverImage)

		TempitemSlotCoverImage = []
		TempitemSlotCoverImage.append(itemSlotCoverImage)
		
		return TempitemSlotCoverImage

	def RefreshRankingList(self, type, category):	
		Getinfo = None
		GetMyinfo = None
		
		if type == ranking.TYPE_RK_SOLO:
			GetInfo = ranking.GetHighRankingInfoSolo
			GetMyinfo = ranking.GetMyRankingInfoSolo

		for line, ResultSlotList in self.ResultSlotList.items():
			(charname, record0, record1, time, empire) = GetInfo(category, line)
			if "" == charname:
				ResultSlotList[0].SetText("")
				ResultSlotList[1].SetText("")
				ResultSlotList[2].LoadImage(self.M2EMPIREICON[0])
				ResultSlotList[3].SetText("")
				self.ResutlSlotCoverList[line][0].Hide()
			else:
				ResultSlotList[0].SetText( str( (line +1) ))
				ResultSlotList[1].SetText(charname)
				ResultSlotList[2].LoadImage(self.M2EMPIREICON[empire])
				ResultSlotList[3].SetText(str(record0))
				self.ResutlSlotCoverList[line][0].Show()

		(rankingIdx, mycharname, myrecord0, myrecord1, mytime, myempire) = GetMyinfo(category)
		rankingStr = ""
		
		if rankingIdx > 0:
			rankingStr = str(rankingIdx)
		
		if "" == mycharname:
			self.MyResultSlotList[0].SetText("")
			self.MyResultSlotList[1].SetText("")
			self.MyResultSlotList[2].LoadImage(self.M2EMPIREICON[0])
			self.MyResultSlotList[3].SetText("")
			self.MyResultSlotCoverList[0].Hide()
		else:
			self.MyResultSlotList[0].SetText(rankingStr)
			self.MyResultSlotList[1].SetText(mycharname)
			self.MyResultSlotList[2].LoadImage(self.M2EMPIREICON[myempire])
			self.MyResultSlotList[3].SetText(str(myrecord0))
			self.MyResultSlotCoverList[0].Show()


	def ExitQuestion(self, point):
		if self.popup and self.popup.IsShow():
			return
		popup = uiCommon.QuestionDialog2()
		popup.SetText1(uiScriptLocale.CURRENT_POINT % (point))
		popup.SetText2(uiScriptLocale.EXIT_BATTLE_FIELD)
		popup.SetAcceptEvent(lambda arg=True: self.ExitEvent(arg))
		popup.SetCancelEvent(lambda arg=False: self.ExitEvent(arg))
		popup.Open()
		self.popup = popup
		
	def ExitOnDeadQuestion(self, point):
		popup = uiCommon.QuestionDialogWithTimeLimit()
		popup.SetAcceptEvent(lambda arg=True: self.ExitOnDeadEvent(arg))
		popup.SetCancelEvent(lambda arg=False: self.ExitOnDeadEvent(arg))
		popup.Open(uiScriptLocale.EXIT_BATTLE_FIELD_ON_DEAD % point, 10)
		popup.SetCancelOnTimeOver()
		self.popup = popup
		
	def ExitEvent(self, arg):
		if arg==True:
			self.popup.Close()
			m2netm2g.SendChatPacket("/exit_battle_field")
		else:
			self.popup.Close()
			
	def ExitOnDeadEvent(self, arg):
		if arg==True:
			self.popup.Close()
			m2netm2g.SendChatPacket("/exit_battle_field_on_dead 1")
		else:
			self.popup.Close()
			m2netm2g.SendChatPacket("/exit_battle_field_on_dead 0")