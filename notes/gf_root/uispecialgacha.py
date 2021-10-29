import ui
import specialgacha
import app
import playerm2g2
import uiToolTip
import item
import localeInfo

class SpecialGachaAward(ui.ScriptWindow):
	def __init__(self):
		#print "__init__"
		
		self.itemToolTip = uiToolTip.ItemToolTip()
		
		ui.ScriptWindow.__init__(self)
		
		self.__LoadScript()
	
	def __del__(self):
		#print "__del__"
		self.itemToolTip = None
		
		ui.ScriptWindow.__del__(self)
		
	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/SpecialGachaWindow.py")
		except:
			import exception
			exception.Abort("SpecialGachaWindow.LoadWindow")
			
		self.stateDic = {
			"default"	: "d:/ymir work/ui/minigame/attendance/award_%s.sub",
			"section"	: "d:/ymir work/ui/minigame/attendance/attendance_disable_number%s.sub",
			"all"		: "d:/ymir work/ui/minigame/attendance/attendance_enable_number%s.sub",
			"accpet"	: "d:/ymir work/ui/minigame/attendance/attendance_close_button.sub",
		}
		
		self.UI_AWARD_MAX = 6
		self.UI_DAY_MAX = 8
		self.awardPage = 0
		self.AWARD_PAGE_MAX = specialgacha.ITEM_GROUP_MAX / self.UI_AWARD_MAX
		
		self.dayPrevBtn = self.GetChild("day_prev_button")
		self.dayPrevBtn.SetEvent(ui.__mem_func__(self.__ClickDayPageButton), 0)
		self.dayNextBtn = self.GetChild("day_next_button")
		self.dayNextBtn.SetEvent(ui.__mem_func__(self.__ClickDayPageButton), 1)
		
		self.awardPrevBtn = self.GetChild("award_prev_button")
		self.awardPrevBtn.SetEvent(ui.__mem_func__(self.__ClickAwardPrevButton))
		self.awardNextBtn = self.GetChild("award_next_button")
		self.awardNextBtn.SetEvent(ui.__mem_func__(self.__ClickAwardNextButton))
		
		self.mainAwardTime = self.GetChild("time2")
		self.subAwardTime = self.GetChild("time1")
		
		self.dayList = []
		for i in xrange(specialgacha.AWARD_DAYS_MAX):
			self.dayList.append(self.GetChild("disable_number_button%s"%(i+1)))

		for i in xrange(specialgacha.AWARD_DAYS_MAX):
			self.dayList[i].SetEvent(ui.__mem_func__(self.__ClickDayButton), i)
			self.dayList[i].Hide()
		
		self.mainSlot = self.GetChild("main_slot")
		self.subSlot = self.GetChild("sub_slot")
		
		self.main_award_vnums	= [0 for col in range(0, self.UI_AWARD_MAX)]
		self.sub_award_vnums	= [0 for col in range(0, self.UI_AWARD_MAX)]
		
		self.mainSlot.SetOverInItemEvent(ui.__mem_func__(self.__MainSlotOverInItem))
		self.mainSlot.SetOverOutItemEvent(ui.__mem_func__(self.__SlotOverOutItem))
		self.subSlot.SetOverInItemEvent(ui.__mem_func__(self.__SubSlotOverInItem))
		self.subSlot.SetOverOutItemEvent(ui.__mem_func__(self.__SlotOverOutItem))
					
		self.GetChild("AcceptButton").SetEvent(ui.__mem_func__(self.__ClickAcceptButton))
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.number_effect = self.GetChild("number_effect")
		self.number_effect.Hide()
		
	def Show(self, vnum, day, win, cell):
		
		self.ITEM_VNUM = vnum
		self.ITEM_WINDOW = win
		self.ITEM_CELL = cell
		
		item.SelectItem(vnum)
		
		(type, value) = item.GetLimit(1)
		
		#print "special gacha limit type %s value %s" % (type, value)
		
		self.LimitCount = value
		
		self.AWARD_DAY = playerm2g2.GetItemMetinSocket(self.ITEM_WINDOW, self.ITEM_CELL, 0)
		
		self.mainTime = playerm2g2.GetItemMetinSocket(self.ITEM_WINDOW, self.ITEM_CELL, 1) - app.GetGlobalTimeStamp()
		self.subTime = playerm2g2.GetItemMetinSocket(self.ITEM_WINDOW, self.ITEM_CELL, 2) - app.GetGlobalTimeStamp()
		
		if self.mainTime > 0:
			self.mainTimeLoop = True
		else:
			self.mainTime = 0
			self.mainTimeLoop = False
			self.mainAwardTime.SetText(localeInfo.SPECIAL_GACHA_AVAILABLE)
		
		if self.subTime > 0:
			self.subTimeLoop = True
		else:
			self.subTime = 0
			self.subTimeLoop = False
			self.subAwardTime.SetText(localeInfo.SPECIAL_GACHA_UNAVAILABLE)
			
		if self.AWARD_DAY == 0:
			self.mainAwardTime.SetText(localeInfo.SPECIAL_GACHA_AVAILABLE)
			self.subAwardTime.SetText(localeInfo.SPECIAL_GACHA_PAYABLE)
		
		
		#print "Show %s %s %s %s" % (self.ITEM_VNUM, self.ITEM_WINDOW, self.ITEM_CELL, self.AWARD_DAY)
		self.dayPage = -1
		if day < self.UI_DAY_MAX:
			self.__ClickDayPageButton(0)
		else:
			self.__ClickDayPageButton(1)
		
		self.__ClickDayButton(day)
		
		ui.ScriptWindow.Show(self)
	
	def Close(self):
		specialgacha.SendClose()
		self.Hide()
		
	def __ClickDayPageButton(self, i):	
		#print "__ClickDayPageButton %s" % i
		
		if self.dayPage == i:
			return
		
		self.dayPage = i
		
		self.__RefreshDaysButton()
		
	def __RefreshDaysButton(self):
		## 버튼 다 숨김
		for i in xrange(specialgacha.AWARD_DAYS_MAX):
			self.dayList[i].Hide()
		
		## 0 ~ 7
		## 8 ~ 15
		minValue = self.UI_DAY_MAX*self.dayPage
		maxValue = min(self.UI_DAY_MAX*(self.dayPage+1), specialgacha.AWARD_DAYS_MAX)
		
		self.dayPrevBtn.Hide()
		self.dayNextBtn.Hide()
		
		if minValue != 0:
			self.dayPrevBtn.Show()
			
		if self.LimitCount > maxValue:
			self.dayNextBtn.Show()
		
		for i in xrange(minValue, maxValue):
			day = i + 1
			
			if day > self.LimitCount:
				continue
			
			if i < self.AWARD_DAY: # 이미 받은 것들
				self.dayList[i].SetUpVisual(self.stateDic["accpet"])
				self.dayList[i].SetOverVisual(self.stateDic["accpet"])
				self.dayList[i].SetDownVisual(self.stateDic["accpet"])
				self.dayList[i].Disable()
				
			elif i == self.AWARD_DAY: # 받을 수 있는 상태
				
				if i == 0: ## 첫쨋날 예외처리
					self.dayList[i].SetUpVisual(self.stateDic["all"]%day)
					self.dayList[i].SetOverVisual(self.stateDic["all"]%day)
					self.dayList[i].SetDownVisual(self.stateDic["all"]%day)
				
				elif self.mainTime > 0: #시간이 안되서 못받음
					self.dayList[i].SetUpVisual(self.stateDic["default"]%day)
					self.dayList[i].SetOverVisual(self.stateDic["default"]%day)
					self.dayList[i].SetDownVisual(self.stateDic["default"]%day)	
					
				elif self.subTime == 0 : #부분적으로 획득 가능
					self.dayList[i].SetUpVisual(self.stateDic["section"]%day)
					self.dayList[i].SetOverVisual(self.stateDic["section"]%day)
					self.dayList[i].SetDownVisual(self.stateDic["section"]%day)	
									
				else: # 다 획득 가능
					self.dayList[i].SetUpVisual(self.stateDic["all"]%day)
					self.dayList[i].SetOverVisual(self.stateDic["all"]%day)
					self.dayList[i].SetDownVisual(self.stateDic["all"]%day)
				
				self.dayList[i].Enable()
								
			else: # 받을수 없는 것들
				self.dayList[i].SetUpVisual(self.stateDic["default"]%day)
				self.dayList[i].SetOverVisual(self.stateDic["default"]%day)
				self.dayList[i].SetDownVisual(self.stateDic["default"]%day)
				self.dayList[i].Enable()
			
			self.dayList[i].Show()
			
		self.__NumberFlash()
		
	def __ClickAwardPrevButton(self):
		#print "__ClickAwardPrevButton"
		
		if self.awardPage <= 0:
			self.awardPage = 0
			return
		
		self.awardPage = self.awardPage - 1
		
		minIdx = self.UI_AWARD_MAX * self.awardPage
		maxIdx = self.UI_AWARD_MAX * (self.awardPage+1)
		
		self.__ShowItemAward(minIdx, maxIdx)
		
	def __ClickAwardNextButton(self):
		#print "__ClickAwardNextButton"
		
		if self.awardPage >= self.AWARD_PAGE_MAX:
			self.awardPage = self.AWARD_PAGE_MAX
			return
		
		self.awardPage = self.awardPage + 1
				
		minIdx = self.UI_AWARD_MAX * self.awardPage
		maxIdx = self.UI_AWARD_MAX * (self.awardPage+1)
		
		self.__ShowItemAward(minIdx, maxIdx)
		
	def __ShowItemAward(self, minIdx, maxIdx):
	
		if self.awardList == None :
			#print "__ShowItemAward Award List None"
			return	
		
		self.awardPrevBtn.Hide()
		self.awardNextBtn.Hide()
		
		if minIdx != 0:
			self.awardPrevBtn.Show()
		
		if maxIdx+1 < specialgacha.ITEM_GROUP_MAX:
			if self.awardList[maxIdx+1][2] != 0 or self.awardList[maxIdx+1][2] != 0:
				self.awardNextBtn.Show()
		
		for i in xrange(minIdx, maxIdx):
			slotIdx = i % self.UI_AWARD_MAX
			
			if i >= specialgacha.ITEM_GROUP_MAX:
				self.mainSlot.SetItemSlot(slotIdx, 0, 0)
				self.subSlot.SetItemSlot(slotIdx, 0, 0)
				
				self.main_award_vnums[slotIdx] = 0
				self.sub_award_vnums[slotIdx] = 0
			else:
				self.mainSlot.SetItemSlot(slotIdx, self.awardList[i][0], self.awardList[i][1])
				self.subSlot.SetItemSlot(slotIdx, self.awardList[i][2], self.awardList[i][3])
				
				self.main_award_vnums[slotIdx] = self.awardList[i][0]
				self.sub_award_vnums[slotIdx] = self.awardList[i][2]
						
	def __ClickAcceptButton(self):
		#print "__ClickAccept"
		
		specialgacha.SendGiveMeAward(self.ITEM_VNUM)
		
		self.Hide()
		
	def __ClickDayButton(self, day):
		#print "__ClickDayButton %s" % day
		
		self.awardList = []
		self.awardList = specialgacha.GetItemAward(self.ITEM_VNUM, day)
		
		if self.awardList == None :
			#print "Award List None"
			return
			
		#print self.awardList
		
		self.awardPage = 0
		self.__ShowItemAward(0, self.UI_AWARD_MAX)
		
	def __MainSlotOverInItem(self, slotIndex):
		if self.itemToolTip and self.main_award_vnums and self.main_award_vnums[slotIndex]:
			self.itemToolTip.SetItemToolTip( self.main_award_vnums[slotIndex] )
			self.itemToolTip.Show()
		
	def __SubSlotOverInItem(self, slotIndex):
		if self.itemToolTip and self.sub_award_vnums and self.sub_award_vnums[slotIndex]:
			self.itemToolTip.SetItemToolTip( self.sub_award_vnums[slotIndex] )
			self.itemToolTip.Show()
		
	def __SlotOverOutItem(self):
		if self.itemToolTip:
			self.itemToolTip.Hide()
			
	def __SecondToHMTime(self, time):
		sec = int(time%60)
		minute = int((time / 60) % 60)
		hour = int((time / 60) / 60) % 24
		
		return "%02i:%02i:%02i" % (hour, minute,sec)
		
	def __NumberFlash(self):
	
		if not self.number_effect:
			return
			
		self.number_effect.Hide()
		
		minValue = self.UI_DAY_MAX*self.dayPage
		maxValue = self.UI_DAY_MAX*(self.dayPage+1)
		
		## 0 ~ 7
		## 7 ~ 14
		if not (minValue <= self.AWARD_DAY < maxValue):
			return
		
		## 첫번째 보상만 예외 처리
		if self.AWARD_DAY == 0 or (self.mainTime == 0 and self.subTime > 0) :
			(x, y) = self.dayList[self.AWARD_DAY].GetLocalPosition()
			self.number_effect.SetPosition(x,y)
			self.number_effect.ResetFrame()
			self.number_effect.Show()
			
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def OnUpdate(self):
		
		if self.AWARD_DAY == 0:
			return
		
		if self.mainTimeLoop:
			if self.mainTime < 0:
				self.mainTime = 0
			
			if self.mainTime == 0:
				self.mainAwardTime.SetText(localeInfo.SPECIAL_GACHA_AVAILABLE)
				#self.__ClickDayPageButton(self.dayPage)
				self.__RefreshDaysButton()
				self.mainTimeLoop = False
			else:
				self.mainAwardTime.SetText(self.__SecondToHMTime(self.mainTime))
				self.mainTime = playerm2g2.GetItemMetinSocket(self.ITEM_WINDOW, self.ITEM_CELL, 1) - app.GetGlobalTimeStamp()
				
		if self.subTimeLoop:
			if self.subTime < 0:
				self.subTime = 0
			
			if self.subTime == 0:
				self.subAwardTime.SetText(localeInfo.SPECIAL_GACHA_UNPAID)
				#self.__ClickDayPageButton(self.dayPage)
				self.__RefreshDaysButton()
				self.subTimeLoop = False
			else:
				self.subAwardTime.SetText(self.__SecondToHMTime(self.subTime))			
				self.subTime = playerm2g2.GetItemMetinSocket(self.ITEM_WINDOW, self.ITEM_CELL, 2) - app.GetGlobalTimeStamp()	
	
	