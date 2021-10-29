import ui
import localeInfo
import app
import uiScriptLocale
import playerm2g2
import mouseModule
import snd
import m2netm2g
import guild
import chatm2g
import uiCommon
import uiToolTip
import wndMgr

class GuildListDialog(ui.ScriptWindow):
	MAX_LINE_COUNT = 8
	PAGEBUTTON_MAX_SIZE = 9
	SPECIAL_TITLE_COLOR  = 0xff4E3D30
	PAGEBUTTON_NUMBER_SIZE = 5
	PAGEONE_MAX_SIZE = 50
	CLICK_LIMIT_TIME = 3
	EMPIRE_ALL = 0
	APPLICANT = 4
	
	M2JOBLIST = {
		0	:	localeInfo.JOB_WARRIOR,	
		1	:	localeInfo.JOB_ASSASSIN,	
		2	:	localeInfo.JOB_SURA,	
		3	:	localeInfo.JOB_SHAMAN,		 
		4	:	localeInfo.JOB_WOLFMAN,	
	}
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isLoaded = 0
		self.bigpagecount = 1
		self.nowpagenumber = 1
		self.pagecount = 0
		self.nowempire = 0
		self.nowtype = 0
		self.searchguildclicktime = 0.0
		self.applicantclicktime = 0.0
		self.selectslotindex = -1
		self.isshowpromoteguild = False
		self.isShow = False
		self.isGuildMember = False
		self.isSearchResult = False
		self.board = None
		self.pageName = None
		self.tabDict = None
		self.tabButtonDict = None
		self.GuildNameValue = None
		self.SearchGuildNameButton = None
		self.ApplicantGuildButton = None
		self.GuildNameImg = None
		self.ResultNameRanking = None
		self.ResultNameGuildOrPlayer = None
		self.ResultNameLevel = None
		self.ResultNameLadderOrJob = None
		self.ResultNameMemberOrSKill = None
		self.ResultNamePromote = None
		self.popup = None
		self.ResultCheckBoxList = {}
		self.ResutlSlotButtonList = {}
		self.ResultApplicantSlotButtonList = {}
		self.ResultSlotList = {}
		self.pagebuttonList = {}
		self.tooltipbutton = None
		self.ShowButtonToolTip = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Destroy(self):
		self.isLoaded = 0
		self.bigpagecount = 1
		self.nowpagenumber = 1
		self.pagecount = 0
		self.nowempire = 0
		self.nowtype = 0
		self.selectslotindex = -1
		self.searchguildclicktime = 0.0
		self.applicantclicktime = 0.0
		self.isshowpromoteguild = False
		self.isShow = False
		self.isGuildMember = False
		self.isSearchResult = False
		self.board = None
		self.pageName = None
		self.tabDict = None
		self.tabButtonDict = None
		self.GuildNameValue = None
		self.SearchGuildNameButton = None
		self.ApplicantGuildButton = None
		self.GuildNameImg = None
		self.ResultNameRanking = None
		self.ResultNameGuildOrPlayer = None
		self.ResultNameLevel = None
		self.ResultNameLadderOrJob = None
		self.ResultNameMemberOrSKill = None
		self.ResultNamePromote = None
		self.popup = None
		self.ResultCheckBoxList = {}
		self.ResutlSlotButtonList = {}
		self.ResultApplicantSlotButtonList = {}
		self.ResultSlotList = {}
		self.pagebuttonList = {}
		self.buttontooltip = None
		self.ShowButtonToolTip = False
		self.Close()
		
	def Open(self):
		if self.isLoaded==0:
			self.isLoaded = 1
			self.__LoadWindow()
			self.__MakeResultUI()
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)
		self.isShow = True
		self.isGuildMember = guild.IsGuildEnable()
		self.SelectPage("EMPIRE_ALL")
			
	def IsShow(self):
		return self.isShow

	def Close(self):
		self.isShow = False
		self.Hide()
		if self.buttontooltip:
			self.buttontooltip.Hide()
			self.ShowButtonToolTip = False


	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/GuildWindow_GuildListWindow.py")
		except:
			import exception
			exception.Abort("GuildWindow_GuildListWindow.__LoadWindow.LoadScript")
			
		self.buttontooltip = uiToolTip.ToolTip()
		self.buttontooltip.ClearToolTip()
			
		try:
			getObject = self.GetChild

			self.board = getObject("Board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))

			self.tabDict = {
				"EMPIRE_ALL"	    : getObject("Tab_01"),
				"EMPIRE_A"		: getObject("Tab_02"),
				"EMPIRE_B"		: getObject("Tab_03"),
				"EMPIRE_C"		: getObject("Tab_04"),
				"APPLICANT"      : getObject("Tab_05"),
			}
			self.tabButtonDict = {
				"EMPIRE_ALL" 	: getObject("Tab_Button_01"),
				"EMPIRE_A"		: getObject("Tab_Button_02"),
				"EMPIRE_B"		: getObject("Tab_Button_03"),
				"EMPIRE_C"		: getObject("Tab_Button_04"),
				"APPLICANT"      : getObject("Tab_Button_05"),
			}
			self.tabEmpireDict = {
				"EMPIRE_ALL" 	: self.EMPIRE_ALL,
				"EMPIRE_A"		: m2netm2g.EMPIRE_A,
				"EMPIRE_B"		: m2netm2g.EMPIRE_B,
				"EMPIRE_C"		: m2netm2g.EMPIRE_C,
				"APPLICANT"      : self.APPLICANT,
			}

			## 길드명 값
			self.GuildNameValue = getObject("GuildNameValue")
			self.GuildNameValue.SetEscapeEvent(ui.__mem_func__(self.Close))
			## 길드명 슬롯 이미지
			self.GuildNameImg = getObject("GuildNameSlot")
			## 길드 검색 버튼
			self.SearchGuildNameButton = getObject("SearchGuildButton")
			self.SearchGuildNameButton .SetEvent(ui.__mem_func__(self.SearchGuildForName))
			## 등록길드 버튼
			self.ShowPromoteGuildButton = getObject("ShowPromoteGuildButton")
			self.ShowPromoteGuildButton.SetEvent(ui.__mem_func__(self.ShowPromoteGuild))
			## 신청하기 버튼
			self.ApplicantGuildButton = getObject("ApplicantGuildButton")
			self.ApplicantGuildButton.SetEvent(ui.__mem_func__(self.ApplicantGuild))
			## 페이지 버튼 셋팅
			self.prev_button = self.GetChild("prev_button")
			self.prev_button.SetEvent(ui.__mem_func__(self.prevbutton))
			## 목록 텍스트
			self.ResultNameRanking = getObject("ResultNameRanking")
			self.ResultNameGuildOrPlayer = getObject("ResultNameGuildOrPlayer")
			self.ResultNameLevel = getObject("ResultNameLevel")
			self.ResultNameLadderOrJob = getObject("ResultNameLadderOrJob")
			self.ResultNameMemberOrSKill = getObject("ResultNameMemberOrSKill")
			self.ResultNamePromote = getObject("ResultNamePromote")
			### 아랍 포지션 변경
			if localeInfo.IsARABIC():
				self.ResultNameRanking.SetPosition(15, 4)
				self.ResultNameGuildOrPlayer.SetPosition(95, 4)
				self.ResultNameLevel.SetPosition(190, 4)
				self.ResultNameLadderOrJob.SetPosition(250, 4)
				self.ResultNameMemberOrSKill.SetPosition(345, 4)
				self.ResultNamePromote.SetPosition(390, 4)
			self.SetRankingResultNameText()

			self.next_button = self.GetChild("next_button")
			self.next_button.SetEvent(ui.__mem_func__(self.nextbutton))

			self.first_prev_button = self.GetChild("first_prev_button")
			self.first_prev_button.SetEvent(ui.__mem_func__(self.firstprevbutton))

			self.last_next_button = self.GetChild("last_next_button")
			self.last_next_button.SetEvent(ui.__mem_func__(self.lastnextbutton))
			
			if localeInfo.IsARABIC():
				self.prev_button.LeftRightReverse()
				self.next_button.LeftRightReverse()
				self.first_prev_button.LeftRightReverse()
				self.last_next_button.LeftRightReverse()
				self.GetChild("leftcenterImg").LeftRightReverse()
				self.GetChild("rightcenterImg").LeftRightReverse()
				self.GetChild("LeftTop").LeftRightReverse()
				self.GetChild("RightTop").LeftRightReverse()
				self.GetChild("LeftBottom").LeftRightReverse()
				self.GetChild("RightBottom").LeftRightReverse()
					
				self.topcenterimg = self.GetChild("topcenterImg")
				self.topcenterimg.SetPosition(self.GetWidth() - (self.topcenterimg.GetWidth()*2)+10,57)
				
				self.bottomcenterImg = self.GetChild("bottomcenterImg")
				self.bottomcenterImg.SetPosition(self.GetWidth() - (self.bottomcenterImg.GetWidth()*2)+10,290)

				self.centerImg = self.GetChild("centerImg")
				self.centerImg.SetPosition(self.GetWidth() - (self.centerImg.GetWidth()*2)+10,57+15)
				
				for key, img in self.tabDict.items():
					img.LeftRightReverse()	

			self.page1_button = self.GetChild("page1_button")
			self.page1_button.SetEvent(ui.__mem_func__(self.Pagebutton), 1)

			self.page2_button = self.GetChild("page2_button")
			self.page2_button.SetEvent(ui.__mem_func__(self.Pagebutton), 2)

			self.page3_button = self.GetChild("page3_button")
			self.page3_button.SetEvent(ui.__mem_func__(self.Pagebutton), 3)

			self.page4_button = self.GetChild("page4_button")
			self.page4_button.SetEvent(ui.__mem_func__(self.Pagebutton), 4)

			self.page5_button = self.GetChild("page5_button")
			self.page5_button.SetEvent(ui.__mem_func__(self.Pagebutton), 5)
			
			TemppageSlotButton = []
			TemppageSlotButton.append(self.page1_button)
			TemppageSlotButton.append(self.page2_button)
			TemppageSlotButton.append(self.page3_button)
			TemppageSlotButton.append(self.page4_button)
			TemppageSlotButton.append(self.page5_button)
			TemppageSlotButton.append(self.prev_button)
			TemppageSlotButton.append(self.next_button)
			TemppageSlotButton.append(self.first_prev_button)
			TemppageSlotButton.append(self.last_next_button)
			self.pagebuttonList[0] = TemppageSlotButton
			self.HidePageButton()

			self.tabButtonDict["EMPIRE_ALL"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_ALL)
			self.tabButtonDict["EMPIRE_ALL"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.tabButtonDict["EMPIRE_A"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_EMPIRE_A)
			self.tabButtonDict["EMPIRE_A"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.tabButtonDict["EMPIRE_B"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_EMPIRE_B)
			self.tabButtonDict["EMPIRE_B"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.tabButtonDict["EMPIRE_C"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_EMPIRE_C)
			self.tabButtonDict["EMPIRE_C"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.tabButtonDict["APPLICANT"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_REGISTER)
			self.tabButtonDict["APPLICANT"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.SearchGuildNameButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_SEARCH)
			self.SearchGuildNameButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.ShowPromoteGuildButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_PROMOTE_GUILD)
			self.ShowPromoteGuildButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
			self.ApplicantGuildButton.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), localeInfo.GUILDWINDOW_LIST_REGISTER_GUILD)
			self.ApplicantGuildButton.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))

		except:
			import exception
			exception.Abort("GuildWindow_GuildListWindow.__LoadWindow.SetObject")
			
		for key, btn in self.tabButtonDict.items():
			btn.SetEvent(ui.__mem_func__(self.SelectPage), key)

		self.SelectPage("EMPIRE_ALL")

	def OverInToolTipButton(self, arg):
		arglen = len(str(arg))
		pos_x, pos_y = wndMgr.GetMousePosition()
	
		self.buttontooltip.ClearToolTip()
		self.buttontooltip.SetThinBoardSize(11 * arglen)
		self.buttontooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.buttontooltip.AppendTextLine(arg, 0xffffffff)
		self.buttontooltip.Show()
		self.ShowButtonToolTip = True
	
	def OverOutToolTipButton(self):
		self.buttontooltip.Hide()
		self.ShowButtonToolTip = False

	def ButtonToolTipProgress(self) :
		if self.ShowButtonToolTip :
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.buttontooltip.SetToolTipPosition(pos_x + 50, pos_y + 50)

	def SetRankingResultNameText(self):
		self.ResultNameRanking.SetText(localeInfo.GUILDWINDOW_LIST_RANKING)
		self.ResultNameGuildOrPlayer.SetText(localeInfo.GUILDWINDOW_LIST_GUILD_NAME)
		self.ResultNameLevel.SetText(localeInfo.GUILDWINDOW_LIST_GUILD_LV)
		self.ResultNameLadderOrJob.SetText(localeInfo.GUILDWINDOW_LIST_LADDER)
		(x,y) = self.ResultNameLadderOrJob.GetLocalPosition()
		self.ResultNameLadderOrJob.SetPosition(250,y)
		self.ResultNameMemberOrSKill.SetText(localeInfo.GUILDWINDOW_LIST_GUILDMEMBER)
		(x,y) = self.ResultNameMemberOrSKill.GetLocalPosition()
		self.ResultNameMemberOrSKill.SetPosition(325,y)
		self.ResultNamePromote.SetText(localeInfo.GUILDWINDOW_LIST_PROMOTE_GUILD)
	
	def SetApplicantResultNameText(self):
		self.ResultNameRanking.SetText(localeInfo.GUILDWINDOW_LIST_RANKING_COUNT)
		self.ResultNameGuildOrPlayer.SetText(localeInfo.GUILDWINDOW_LIST_CHRACTER_NAME)
		self.ResultNameLevel.SetText(localeInfo.GUILDWINDOW_LIST_CHRACTER_LV)
		self.ResultNameLadderOrJob.SetText(localeInfo.GUILDWINDOW_LIST_CHRACTER_JOB)
		(x,y) = self.ResultNameLadderOrJob.GetLocalPosition()
		self.ResultNameLadderOrJob.SetPosition(275,y)
		self.ResultNameMemberOrSKill.SetText(localeInfo.GUILDWINDOW_LIST_CHRACTER_SUB_JOB)
		(x,y) = self.ResultNameMemberOrSKill.GetLocalPosition()
		self.ResultNameMemberOrSKill.SetPosition(365,y)
		self.ResultNamePromote.SetText("")
		
	def __MakeResultUI(self):
		yPos = 0
		for i in range(0,self.MAX_LINE_COUNT):
			yPos = 84 + i * 25

			## 순위
			RankingSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", 23, yPos)
			RankingSlotImage.SetAlpha(0)
			RankingSlot = ui.MakeTextLine(RankingSlotImage)
			self.Children.append(RankingSlotImage)
			self.Children.append(RankingSlot)

			## 길드명
			GuildNameImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_04.sub", 77, yPos)
			GuildNameImage.SetAlpha(0)
			GuildNameSlot = ui.MakeTextLine(GuildNameImage)
			self.Children.append(GuildNameImage)
			self.Children.append(GuildNameSlot)

			## 길드LV
			GuildLevelSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", 205, yPos)
			GuildLevelSlotImage.SetAlpha(0)
			GuildLevelSlot = ui.MakeTextLine(GuildLevelSlotImage)
			self.Children.append(GuildLevelSlotImage)
			self.Children.append(GuildLevelSlot)
			
			## 래더점수
			LadderSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_00.sub", 270, yPos)
			LadderSlotImage.SetAlpha(0)
			LadderSlot = ui.MakeTextLine(LadderSlotImage)
			self.Children.append(LadderSlotImage)
			self.Children.append(LadderSlot)
			
			## 길드원수
			GuildMemberCountImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_01.sub", 337, yPos)
			GuildMemberCountImage.SetAlpha(0)
			GuildMemberCountSlot = ui.MakeTextLine(GuildMemberCountImage)
			self.Children.append(GuildMemberCountImage)
			self.Children.append(GuildMemberCountSlot)
			
			## 아랍 포지션 변경
			if localeInfo.IsARABIC():
				RankingSlotImage.SetPosition(self.GetWidth() - (40 + 25), yPos)
				GuildNameImage.SetPosition(self.GetWidth() - (160 + 25), yPos)
				GuildLevelSlotImage.SetPosition(self.GetWidth() - (224 + 25), yPos)
				LadderSlotImage.SetPosition(self.GetWidth() - (290 + 25), yPos)
				GuildMemberCountImage.SetPosition(self.GetWidth() - (360 + 25), yPos)

			tempguildlankingslotlist = []
			tempguildlankingslotlist.append(RankingSlot)
			tempguildlankingslotlist.append(GuildNameSlot)
			tempguildlankingslotlist.append(GuildLevelSlot)
			tempguildlankingslotlist.append(LadderSlot)
			tempguildlankingslotlist.append(GuildMemberCountSlot)
			
			self.ResultSlotList[i] = tempguildlankingslotlist
			
			## 결과 목록 버튼
			itemSlotButtonImage = ui.MakeButton(self, 22, yPos, "", "d:/ymir work/ui/game/guild/guildRankingList/", "ranking_list_button01.sub", "ranking_list_button02.sub", "ranking_list_button02.sub")
			itemSlotButtonImage.Hide()
			itemSlotButtonImage.SetEvent(ui.__mem_func__(self.__SelectItem),i)
			self.Children.append(itemSlotButtonImage)

			if localeInfo.IsARABIC():
				itemSlotButtonImage.LeftRightReverse()

			TempitemSlotButtonImage = []
			TempitemSlotButtonImage.append(itemSlotButtonImage)
			self.ResutlSlotButtonList[i] = TempitemSlotButtonImage
			
			## 신청자 목록 결과 버튼
			applicantslotbuttonimage = ui.MakeButton(self, 22, yPos, "", "d:/ymir work/ui/game/guild/guildRankingList/", "applicant_list_button01.sub", "applicant_list_button02.sub", "applicant_list_button02.sub")
			applicantslotbuttonimage.Hide()
			applicantslotbuttonimage.SetEvent(ui.__mem_func__(self.__SelectItem),i)
			self.Children.append(applicantslotbuttonimage)
			
			if localeInfo.IsARABIC():
				applicantslotbuttonimage.LeftRightReverse()
			
			TempapplicantbuttonImage = []
			TempapplicantbuttonImage.append(applicantslotbuttonimage)
			self.ResultApplicantSlotButtonList[i] = TempapplicantbuttonImage
			
			## 등록길드 체크 박스 이미지.
			PromoteCheckBoxImg = ui.MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 414, yPos)
			PromoteCheckBoxImg.Hide()
			self.Children.append(PromoteCheckBoxImg)
			TempCheckBoxImg = []
			TempCheckBoxImg.append(PromoteCheckBoxImg)
			self.ResultCheckBoxList[i] = TempCheckBoxImg
			
			## 아랍 포지션 변경
			if localeInfo.IsARABIC():	
				PromoteCheckBoxImg.SetPosition(self.GetWidth() - (414 + 25),yPos)
			


	## 길드 명 검색 타임 리밋 설정.
	def OnUpdate(self):
		if (app.GetTime() - self.searchguildclicktime) > self.CLICK_LIMIT_TIME and self.SearchGuildNameButton.IsDIsable() == 0:
			self.SearchGuildNameButton.Enable()
			
		if (app.GetTime() - self.applicantclicktime) > self.CLICK_LIMIT_TIME and self.ApplicantGuildButton.IsDIsable() == 0:
			self.ApplicantGuildButton.Enable()
			
		self.ButtonToolTipProgress()
		
	## 길드 가입 신청
	def ApplicantGuild(self):
		if self.selectslotindex == -1:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO,localeInfo.GUILDWINDOW_LIST_SELECT_GUILD)
		else:
			if not self.isGuildMember:
				## 검색하기 버튼 설정		
				self.applicantclicktime = app.GetTime()
				self.ApplicantGuildButton.Disable()
				self.ApplicantGuildButton.SetUp()
					
				self.popup = uiCommon.QuestionDialog()
				self.popup.SetText(localeInfo.GUILDLIST_APPLICANT)
				self.popup.SetAcceptEvent(lambda arg=True: self.ApplicantGuildDialog(arg))
				self.popup.SetCancelEvent(lambda arg=False: self.ApplicantGuildDialog(arg))
				self.popup.Open()

	##  길드 가입 신청 확인 Dialog
	def ApplicantGuildDialog(self, arg):

		if arg:
			type = self.nowtype
			if self.isSearchResult:
				type = guild.RANKING_INFO_SEARCH
			(allpage, nowpage, nowpagecount) = guild.GetRankingPageInfo(type, self.nowempire)
			(guildname, level, ladderpoint, minmember, maxmember, promote, Ranking) = guild.GetRankingInfo(nowpage, type, self.nowempire, self.selectslotindex)
			if m2netm2g.SendRequestApplicant(guildname) == 0:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO,localeInfo.GUILDWINDOW_LIST_ALREADY_REGISTER)
			## 결과 슬롯 버튼들 Up
			self.AllResultSlotButtonUp()
			self.popup.Close()
			self.popup = None
		else:
			self.popup.Close()
			self.popup = None
							
	## 길드 명으로 검색 하기
	def SearchGuildForName(self):
		name = self.GuildNameValue.GetText()
		if name=="":
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO,localeInfo.GUILDWINDOW_LIST_INPUT_GUILDNAME)
			return

		## 검색하기 버튼 설정		
		self.searchguildclicktime = app.GetTime()
		self.SearchGuildNameButton.Disable()
		self.SearchGuildNameButton.SetUp()

		## 다른 부분 초기화.
		self.ClearBase()
		self.isSearchResult = True

		## 국가 탭 다시 올리기.
		for key, btn in self.tabButtonDict.items():
			btn.SetUp()

		m2netm2g.SendRequestSearchGuild(name, self.nowtype, self.nowempire)

	## 등록 길드 보여주기.		
	def ShowPromoteGuild(self):
		## 길드명 입력 editline 클리어
		self.GuildNameValue.SetText("")
		## 등록길드 보여주기 등록
		self.isshowpromoteguild = True
		## 길드명 검색 확인 False
		self.isSearchResult = False
		self.ClearBase()

		if self.nowempire == 0:
			self.nowtype = guild.RANKING_INFO_PROMOTE_ALL
			m2netm2g.SendRequestGuildList(0, guild.RANKING_INFO_PROMOTE_ALL, self.nowempire)
		else:
			self.nowtype = guild.RANKING_INFO_PROMOTE_EMPIRE
			m2netm2g.SendRequestGuildList(0, guild.RANKING_INFO_PROMOTE_EMPIRE, self.nowempire)
		
	## 국가 탭 클릭시
	def SelectPage(self,arg):

		## 길드명 입력 editline 클리어
		self.GuildNameValue.SetText("")
		for key, btn in self.tabButtonDict.items():
			if arg != key:
				btn.SetUp()

		for key, img in self.tabDict.items():
			if arg == key:
				img.Show()
			else:
				img.Hide()

		## 현재 선택된 국가 저장.
		self.nowempire = self.tabEmpireDict[arg]
		self.ClearBase()

		## 신청 관리 탭 부분 때문에 국가 탭 클릭시
		## 길드멤버 여부에 따라 버튼 보여주기/안보여주기		
		if self.isGuildMember:
			self.ShowPromoteGuildButton.Show()
		else:
			self.ShowPromoteGuildButton.Show()

		## 같은 국가 만 버튼 보이기.
		if self.nowempire == m2netm2g.GetEmpireID():
			if not self.isGuildMember:
				self.ApplicantGuildButton.Show()
			else:
				self.ApplicantGuildButton.Hide()
		else:
			self.ApplicantGuildButton.Hide()

		## 길드 검색 부분
		self.GuildNameValue.Show()
		self.SearchGuildNameButton.Show()
		self.GuildNameImg.Show()
		## 타이틀바
		self.board.SetTitleName(localeInfo.GUILDWINDOW_LIST_GUILD_LIST)
		## 메뉴 
		self.SetRankingResultNameText()

		if arg == "EMPIRE_ALL":
			self.HidePageButton()
			self.nowtype = guild.RANKING_INFO_ALL
			m2netm2g.SendRequestGuildList(0, guild.RANKING_INFO_ALL, self.tabEmpireDict[arg])
		elif arg == "APPLICANT":
			self.HidePageButton()
			self.ApplicantGuildButton.Hide()
			self.ShowPromoteGuildButton.Hide()
			self.GuildNameValue.Hide()
			self.SearchGuildNameButton.Hide()
			self.GuildNameImg.Hide()
			
			if self.isGuildMember:
				self.board.SetTitleName(localeInfo.GUILDWINDOW_LIST_APPLICANT_LIST)
				self.SetApplicantResultNameText()
				self.nowtype = guild.RANKING_INFO_APPLICANT
				m2netm2g.SendRequestApplicantList(0)
			else:
				self.board.SetTitleName(localeInfo.GUILDWINDOW_LIST_PROMOTE_GUILD_LIST)
				self.nowtype = guild.RANKING_INFO_APPLICANT_GUILD
				m2netm2g.SendRequestApplicantGuildList(0)
		else:
			self.HidePageButton()
			self.nowtype = guild.RANKING_INFO_EMPIRE
			m2netm2g.SendRequestGuildList(0, guild.RANKING_INFO_EMPIRE, self.tabEmpireDict[arg])

		## 등록길드 보여주기 해제
		self.isshowpromoteguild = False
		## 길드명 검색 확인 False
		self.isSearchResult = False

		## 국가 탭 다시 올리기.
		for key, btn in self.tabButtonDict.items():
			btn.SetUp()
	
	## 길드 목록 버튼 선택시
	def __SelectItem(self,arg):
		## 길드가입 안된 사람만 가능.
		if not self.isGuildMember and self.nowtype != guild.RANKING_INFO_APPLICANT_GUILD:
			type = self.nowtype
			if self.isSearchResult:
				type = guild.RANKING_INFO_SEARCH
			(allpage, nowpage, nowpagecount) = guild.GetRankingPageInfo(type, self.nowempire)
			(guildname, level, ladderpoint, minmember, maxmember, promote, Ranking) = guild.GetRankingInfo(nowpage, type, self.nowempire, arg)
			if promote:
				self.AllResultSlotButtonUp()
				self.ResutlSlotButtonList[arg][0].Disable()
				self.ResutlSlotButtonList[arg][0].Down()
				self.selectslotindex = arg
			else:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO,localeInfo.GUILDWINDOW_LIST_NOTPROMOTEGUILD)
		
	## 리프레쉬 (길드 검색해서 리프레쉬 한것과 그냥 뿌리는것 나뉜다.)
	def RefreshGuildRankingList(self, issearch):
		## 길드목록 버튼 setup
		self.AllResultSlotButtonUp()
		type = self.nowtype
		if issearch:
			type = guild.RANKING_INFO_SEARCH

		(allpage, nowpage, nowpagecount) = guild.GetRankingPageInfo(type, self.nowempire)

		if type == guild.RANKING_INFO_APPLICANT:
			for line, ResultSlotList in self.ResultSlotList.items():
				(charname, level, job, skillgroup) = guild.GetApplicantInfo(nowpage,line)
				if "" == charname:
					ResultSlotList[0].SetText("")
					ResultSlotList[1].SetText("")
					ResultSlotList[2].SetText("")
					ResultSlotList[3].SetText("")
					ResultSlotList[4].SetText("")
					self.ResultApplicantSlotButtonList[line][0].Hide()
				else:
					ResultSlotList[0].SetText( str( (line +1) + (8 * nowpage) ))
					ResultSlotList[1].SetText(charname)
					ResultSlotList[2].SetText(str(level))
					
					ResultSlotList[3].SetText(self.M2JOBLIST[job])
					(x,y) = ResultSlotList[3].GetLocalPosition()
					ResultSlotList[3].SetPosition(20,y)
					
					ResultSlotList[4].SetText(localeInfo.JOBINFO_TITLE[job][skillgroup])
					(x,y) = ResultSlotList[4].GetLocalPosition()
					ResultSlotList[4].SetPosition(40,y)

					self.ResultApplicantSlotButtonList[line][0].Show()
		else:
			for line, ResultSlotList in self.ResultSlotList.items():
				(guildname, level, ladderpoint, minmember, maxmember, promote, Ranking) = guild.GetRankingInfo(nowpage, type, self.nowempire, line)
				if "" == guildname:
					ResultSlotList[0].SetText("")
					ResultSlotList[1].SetText("")
					ResultSlotList[2].SetText("")
					ResultSlotList[3].SetText("")
					ResultSlotList[4].SetText("")
					self.ResutlSlotButtonList[line][0].Hide()
					self.ResultCheckBoxList[line][0].Hide()
				else:
					ResultSlotList[0].SetText(str( Ranking ))
					ResultSlotList[1].SetText(guildname)
					ResultSlotList[2].SetText(str(level))

					ResultSlotList[3].SetText(str(ladderpoint))
					(x,y) = ResultSlotList[3].GetLocalPosition()
					ResultSlotList[3].SetPosition(0,y)

					ResultSlotList[4].SetText(str(minmember) + "/" + str(maxmember))
					(x,y) = ResultSlotList[4].GetLocalPosition()
					ResultSlotList[4].SetPosition(0,y)					
					
					self.ResutlSlotButtonList[line][0].Show()
					if promote:
						self.ResultCheckBoxList[line][0].Show()
					else:
						self.ResultCheckBoxList[line][0].Hide()
				if issearch:
					break

		if issearch:
			if "" == guildname:
				self.HidePageButton()
				self.HideItemButton()
				#chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO,localeInfo.GUILDWINDOW_LIST_GUILD_NOT)
				return

		self.SetPageButton(allpage, nowpage)

		## 중간 앞 점프 버튼 활성화/비활성화
		if self.bigpagecount == 1:
			self.prev_button.Disable()
			self.prev_button.Down()
		else:
			self.prev_button.Enable()

		## 맨 앞으로 점프 버튼 활성화/비활성화
		if self.bigpagecount - 1 <= 1:			
			self.first_prev_button.Disable()
			self.first_prev_button.Down()
		else:
			self.first_prev_button.Enable()

		## 중간 뒤 점프 버튼 활성화/비활성화
		if allpage > (self.PAGEBUTTON_NUMBER_SIZE * self.bigpagecount):
			self.next_button.Enable()
		else:
			self.next_button.Disable()
			self.next_button.Down()
			
		## 맨 뒤로 점프 버튼 활성화/비활성화
		if allpage > (self.PAGEBUTTON_NUMBER_SIZE * (self.bigpagecount+1)):
			self.last_next_button.Enable()
		else:
			self.last_next_button.Disable()
			self.last_next_button.Down()

	## 페이지 버튼 셋팅
	def SetPageButton(self, maxsize, page):

		pagebuttonindex = 0
		pagebuttonindex = page - (self.bigpagecount-1) * 5
		self.pagecount = maxsize
		
		if self.pagecount > 5:
			if (5 * self.bigpagecount - self.pagecount) < 0:
				self.pagecount = 5
			else:
				self.pagecount = 5 - (5 * self.bigpagecount - self.pagecount)
		
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(self.pagecount):
				pagebutton[i].Show()
				
		self.pagebuttonList[0][5].Show()
		self.pagebuttonList[0][6].Show()
		self.pagebuttonList[0][7].Show()
		self.pagebuttonList[0][8].Show()
		
		self.clearPagebuttoncolor()
		self.pagebuttonList[0][pagebuttonindex].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][pagebuttonindex].Down()
		self.pagebuttonList[0][pagebuttonindex].Disable()
		self.nowpagenumber = pagebuttonindex					

	## 페이지버튼 모두 숨기기
	def HidePageButton(self):
		for line, pagebutton in self.pagebuttonList.items():
			for i in range(0,self.PAGEBUTTON_MAX_SIZE):
				pagebutton[i].Hide()

	## 페이지 버튼 클릭
	def Pagebutton(self,number):
		if number == self.nowpagenumber+1:
			return
		if self.bigpagecount > 1:
			if number == self.nowpagenumber - (self.bigpagecount-1) * 5:
				return
		self.clearPagebuttoncolor()
		self.pagebuttonList[0][number-1].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][number-1].Down()
		self.pagebuttonList[0][number-1].Disable()
		self.nowpagenumber = int(self.pagebuttonList[0][number-1].GetText())-1
		
		## 모든 국가탭
		if self.nowempire == self.EMPIRE_ALL:
			if self.isshowpromoteguild:
				m2netm2g.SendRequestGuildList(self.nowpagenumber, guild.RANKING_INFO_PROMOTE_ALL,self.nowempire)
				self.nowtype = guild.RANKING_INFO_PROMOTE_ALL
			else:
				m2netm2g.SendRequestGuildList(self.nowpagenumber, guild.RANKING_INFO_ALL,self.nowempire)
				self.nowtype = guild.RANKING_INFO_ALL
		## 신청 관리 탭
		elif self.nowempire == self.APPLICANT:
				if self.nowtype == guild.RANKING_INFO_APPLICANT_GUILD:
					m2netm2g.SendRequestApplicantGuildList(self.nowpagenumber)
				if self.nowtype == guild.RANKING_INFO_APPLICANT:
					m2netm2g.SendRequestApplicantList(self.nowpagenumber)
		## 각국가탭
		else:
			if self.isshowpromoteguild:
				m2netm2g.SendRequestGuildList(self.nowpagenumber, guild.RANKING_INFO_PROMOTE_EMPIRE,self.nowempire)
				self.nowtype = guild.RANKING_INFO_PROMOTE_EMPIRE
			else:
				m2netm2g.SendRequestGuildList(self.nowpagenumber, guild.RANKING_INFO_EMPIRE,self.nowempire)
				self.nowtype = guild.RANKING_INFO_EMPIRE
	
	## 서버에 타입 맞게 리스트 요청.
	def SendRequestList(self):
		if self.nowtype == guild.RANKING_INFO_APPLICANT:
			m2netm2g.SendRequestApplicantList(self.nowpagenumber)
		elif self.nowtype == guild.RANKING_INFO_APPLICANT_GUILD:
			m2netm2g.SendRequestApplicantGuildList(self.nowpagenumber)
		else:
			m2netm2g.SendRequestGuildList(self.nowpagenumber, self.nowtype, self.nowempire)
	
	## 맨처음 페이지로 이동.
	def firstprevbutton(self):
		if self.bigpagecount - 1 <= 1:
			return

		self.clearPagebuttoncolor()
		self.bigpagecount = 1
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagebutton[i].SetText(str(i+1))

		self.nowpagenumber = int(self.pagebuttonList[0][0].GetText())-1
		self.pagebuttonList[0][0].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][0].Down()
		self.pagebuttonList[0][0].Disable()
		## 서버에 리스트 요청
		self.SendRequestList	()
		
	## 맨 마지막으로 이동 버튼.
	def lastnextbutton(self):
		(allpage, nowpage, nowpagecount) = guild.GetRankingPageInfo(self.nowtype, self.nowempire)
		self.pagecount = allpage
		self.HidePageButton()
		self.clearPagebuttoncolor()
		
		if self.pagecount%5 == 0:
			self.bigpagecount = (self.pagecount/5)
		else:
			self.bigpagecount = (self.pagecount/5) + 1

		pagenumber = 5 * (self.pagecount/5)
		if pagenumber == self.pagecount:
			pagenumber -= 5
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagebutton[i].SetText(str(i+pagenumber+1))

		self.nowpagenumber = self.pagecount-1
		## 서버에 리스트 요청
		self.SendRequestList	()
		
	## 이전 페이지 점프
	def prevbutton(self):
		if self.bigpagecount == 1:
			return

		self.clearPagebuttoncolor()
		self.bigpagecount -= 1

		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagenumber = int(pagebutton[i].GetText()) - 5
				pagebutton[i].SetText(str(pagenumber))
		
		self.nowpagenumber = int(self.pagebuttonList[0][0].GetText())-1
		self.pagebuttonList[0][0].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][0].Down()
		self.pagebuttonList[0][0].Disable()
		## 서버에 리스트 요청
		self.SendRequestList	()

	## 다음 페이지 점프
	def nextbutton(self):
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagenumber = int(pagebutton[i].GetText()) + 5
				pagebutton[i].SetText(str(pagenumber))
				
		self.nowpagenumber = int(self.pagebuttonList[0][0].GetText())-1
		self.bigpagecount += 1
		self.HidePageButton()
		self.clearPagebuttoncolor()
		self.pagebuttonList[0][0].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][0].Down()
		self.pagebuttonList[0][0].Disable()
		## 서버에 리스트 요청
		self.SendRequestList	()

	## 숫자 페이지 버튼 색 흰색으로.
	def clearPagebuttoncolor(self):
		for line, pagebutton in self.pagebuttonList.items():
			for i in range(0,self.PAGEBUTTON_NUMBER_SIZE):
				pagebutton[i].SetTextColor(0xffffffff)
				pagebutton[i].SetUp()
				pagebutton[i].Enable()
		
	## 페이지버튼 모두 숨기기
	def HidePageButton(self):
		for line, pagebutton in self.pagebuttonList.items():
			for i in range(0,self.PAGEBUTTON_MAX_SIZE):
				pagebutton[i].Hide()

	## 아이템 목록 모두 숨기기
	def HideItemButton(self):
		for line, ResultSlotList in self.ResultSlotList.items():
			ResultSlotList[0].SetText("")
			ResultSlotList[1].SetText("")
			ResultSlotList[2].SetText("")
			ResultSlotList[3].SetText("")
			ResultSlotList[4].SetText("")
			self.ResutlSlotButtonList[line][0].Hide()
			self.ResultCheckBoxList[line][0].Hide()
			self.ResultApplicantSlotButtonList[line][0].Hide()
			
	## 아이템 목록 모두 Up
	def AllResultSlotButtonUp(self):
		for line in range(0,self.MAX_LINE_COUNT):
			self.ResutlSlotButtonList[line][0].SetUp()
			self.ResutlSlotButtonList[line][0].Enable()
			self.ResultApplicantSlotButtonList[line][0].SetUp()
			self.ResultApplicantSlotButtonList[line][0].Enable()
		## 선택 인덱스도 초기화
		self.selectslotindex = -1

	## 새로운 탭, 등록길드 보여줄때 초기화.
	def ClearBase(self):
		self.bigpagecount = 1
		self.HidePageButton()
		self.HideItemButton()
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagebutton[i].SetText(str(i+1))

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
		