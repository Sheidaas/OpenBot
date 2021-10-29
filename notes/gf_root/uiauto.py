import ui
import app
import localeInfo
import constInfo
import playerm2g2
import m2netm2g
import chrmgrm2g
import wndMgr
import mouseModule
import guild
import skill
import item
import chr
import uiToolTip

class AutoWindow(ui.ScriptWindow):
	AUTO_COOLTIME_POS_Y = 4
	AUTO_COOLTIME_POS_X = 4
	AUTO_COOLTIME_MAX = AUTO_COOLTIME_POS_Y * AUTO_COOLTIME_POS_X
	AUTO_ONOFF_START = 1
	AUTO_ONOFF_ATTACK = 2
	AUTO_ONOFF_SKILL = 3
	AUTO_ONOFF_POSITION = 4
	AUTO_ONOFF_AUTO_RANGE = 5	

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isloded = 0
		self.isOpen = 0
		self.tooltipSkill = 0
		self.tooltipItem = 0
		self.autostartonoff = 0
		self.autoslotindex = {}
		self.timeeditlist = {}
		self.autoonoffbuttonlist =[]
		self.autoslot = None
		self.AutoSkillClearButton = None
		self.AutoPositionClearButton = None
		self.AutoAllClearButton = None
		self.AutoToolTipButton = None
		self.AutoToolTip = None
		for i in xrange(playerm2g2.AUTO_SKILL_SLOT_MAX):
			self.autoslotindex[i] = 0
		
		for i in range(playerm2g2.AUTO_POSITINO_SLOT_START,playerm2g2.AUTO_POSITINO_SLOT_MAX):
			self.autoslotindex[i] = playerm2g2.ITEM_SLOT_COUNT
			
		self.AutoSystemToolTipList = [localeInfo.AUTO_TOOLTIP_LINE1, 
		localeInfo.AUTO_TOOLTIP_LINE2, 
		localeInfo.AUTO_TOOLTIP_LINE3,
		localeInfo.AUTO_TOOLTIP_LINE4,
		localeInfo.AUTO_TOOLTIP_LINE5]
		self.closegame = False
		self.LoadAutoWindow()
		self.isFirstReadFile = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.isloded = 0
		self.isOpen = 0
		self.tooltipSkill = 0
		self.tooltipItem = 0
		self.autostartonoff = 0
		self.autoslotindex = {}
		self.timeeditlist = {}
		self.autoonoffbuttonlist =[]
		self.autoslot = None
		self.AutoSkillClearButton = None
		self.AutoPositionClearButton = None
		self.AutoAllClearButton = None
		self.AutoToolTipButton = None
		self.AutoToolTip = None
		self.closegame = False
		self.isFirstReadFile = False

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AutoWindow.py")
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			autostartonbutton = self.GetChild("AutoStartOnButton")
			autostartonbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_START, 0)
			self.autoonoffbuttonlist.append(autostartonbutton)
			
			autostartoffbutton = self.GetChild("AutoStartOffButton")
			autostartoffbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_START, 1)
			autostartoffbutton.Down()
			autostartoffbutton.Disable()
			self.autoonoffbuttonlist.append(autostartoffbutton)
			
			autoattackonbutton = self.GetChild("AutoAttackOnButton")
			autoattackonbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_ATTACK, 2)
			self.autoonoffbuttonlist.append(autoattackonbutton)			
			autoattackoffbutton = self.GetChild("AutoAttackOffButton")
			autoattackoffbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_ATTACK, 3)
			autoattackoffbutton.Down()
			autoattackoffbutton.Disable()
			self.autoonoffbuttonlist.append(autoattackoffbutton)
			
			autoskillonbutton = self.GetChild("AutoSkillOnButton")
			autoskillonbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_SKILL, 4)
			self.autoonoffbuttonlist.append(autoskillonbutton)
			autoskilloffbutton = self.GetChild("AutoSkillOffButton")
			autoskilloffbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_SKILL, 5)
			autoskilloffbutton.Down()
			autoskilloffbutton.Disable()
			self.autoonoffbuttonlist.append(autoskilloffbutton)
			
			autopositiononbutton = self.GetChild("AutoPositionlOnButton")
			autopositiononbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_POSITION, 6)
			self.autoonoffbuttonlist.append(autopositiononbutton)
			autopositionoffbutton = self.GetChild("AutoPositionlOffButton")
			autopositionoffbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_POSITION, 7)
			autopositionoffbutton.Down()
			autopositionoffbutton.Disable()
			self.autoonoffbuttonlist.append(autopositionoffbutton)
			
			autorangeonbutton = self.GetChild("AutoRangeOnButton")
			autorangeonbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 1, self.AUTO_ONOFF_AUTO_RANGE, 8)
			self.autoonoffbuttonlist.append(autorangeonbutton)
			autorangeoffbutton = self.GetChild("AutoRangeOffButton")
			autorangeoffbutton.SetEvent(ui.__mem_func__(self.AutoOnOff), 0, self.AUTO_ONOFF_AUTO_RANGE, 9)
			autorangeoffbutton.Down()
			autorangeoffbutton.Disable()
			self.autoonoffbuttonlist.append(autorangeoffbutton)

			self.AutoSkillClearButton = self.GetChild("AutoSkillClearButton")
			self.AutoSkillClearButton.SetEvent(ui.__mem_func__(self.AutoSkillClear))
			self.AutoPositionClearButton = self.GetChild("AutoPositionClearButton")
			self.AutoPositionClearButton.SetEvent(ui.__mem_func__(self.AutoPositionClear))
			self.AutoAllClearButton = self.GetChild("AutoAllClearButton")
			self.AutoAllClearButton.SetEvent(ui.__mem_func__(self.AutoAllClear))

			for x in xrange(self.AUTO_COOLTIME_MAX):
				childname = "editline" + str(x)
				self.timeeditlist[x] = self.GetChild(childname)
				self.timeeditlist[x].SetEscapeEvent(ui.__mem_func__(self.Close))
			
			if localeInfo.IsARABIC():
				xPos = 22+160
				yPos = 105
				templist = {}
				for x in xrange(self.AUTO_COOLTIME_POS_Y):
					for i in xrange(self.AUTO_COOLTIME_POS_X):
						tempchildimgname = "cool_time_Image" + str(i+(x*4))
						templist[x] = self.GetChild(tempchildimgname)
						templist[x].SetPosition( xPos, yPos )
						xPos -= 40
					if x == 1:
						yPos = yPos+27
					xPos = 22+160
					yPos += 70
				templist = {}
				

			self.autoslot = self.GetChild("Auto_Active_Skill_Slot_Table")
			self.autoslot.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
			self.autoslot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectActiveSkillEmptySlot))
			self.autoslot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectActiveSkillSlot))
			self.autoslot.SetOverInItemEvent(ui.__mem_func__(self.OverActiveSkillSlot))
			self.autoslot.SetOverOutItemEvent(ui.__mem_func__(self.OverSkillSlotOutItem))
			self.autoslot.Show()

			self.AutoToolTipButton = self.GetChild("AutoToolTIpButton")
			self.AutoToolTip = self.__CreateGameTypeToolTip(localeInfo.AUTO_TOOLTIP_TITLE,self.AutoSystemToolTipList)
			self.AutoToolTip.SetTop()
			self.AutoToolTipButton.SetToolTipWindow(self.AutoToolTip)
		
		except:
			import exception
			exception.Abort("AutoWindow.__LoadWindow.UIScript/AutoWindow.py")

	def __CreateGameTypeToolTip(self, title, descList):
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)
		toolTip.AppendSpace(5)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)

		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip

	def AutoSkillClear(self):
		if self.GetAutoStartonoff() == False:
			playerm2g2.ClearAutoSKillSlot()
			self.RefreshAutoSkillSlot()
			for i in xrange(playerm2g2.AUTO_SKILL_SLOT_MAX):
				self.autoslotindex[i] = 0

	def AutoPositionClear(self):
		if self.GetAutoStartonoff() == False:
			playerm2g2.ClearAutoPositionSlot()
			self.RefreshAutoPositionSlot()
			for i in range(playerm2g2.AUTO_POSITINO_SLOT_START,playerm2g2.AUTO_POSITINO_SLOT_MAX):
				self.autoslotindex[i] = playerm2g2.ITEM_SLOT_COUNT
	
	def AutoAllClear(self):
		if self.GetAutoStartonoff() == False:
			playerm2g2.ClearAutoAllSlot()	
			self.RefreshAutoSkillSlot()
			self.RefreshAutoPositionSlot()
			for i in xrange(playerm2g2.AUTO_SKILL_SLOT_MAX):
				self.autoslotindex[i] = 0
			for i in range(playerm2g2.AUTO_POSITINO_SLOT_START,playerm2g2.AUTO_POSITINO_SLOT_MAX):
				self.autoslotindex[i] = playerm2g2.ITEM_SLOT_COUNT

	def IsNumberic(self, text) :
		try :
			int(text)
			return True
		except ValueError :
			return False

	def CheckCooltimeText(self, cooltime):
			if cooltime == "":
				return 0
			if not self.IsNumberic(cooltime):
				return 0
			return cooltime
	
	## 버튼 OnOff 셋팅.
	def AutoOnOff(self, onoff,type,number,command = False):
		
		if not self.isloded:
			return

		if type == self.AUTO_ONOFF_START:
			if playerm2g2.CanStartAuto() == False:
				return
			if onoff == 1:
				## 스킬 슬롯
				for i in xrange(playerm2g2.AUTO_SKILL_SLOT_MAX):
					cooltime = self.timeeditlist[i].GetText()
					cooltime = self.CheckCooltimeText(cooltime)
					cooltime = playerm2g2.CheckSkillSlotCoolTime(i,self.autoslotindex[i],int(cooltime))
					if self.autoslotindex[i] == 0:
						self.timeeditlist[i].SetText("")
					if not cooltime == 0:
						playerm2g2.SetAutoSlotCoolTime(i,int(cooltime))
						self.timeeditlist[i].SetText(str(cooltime))

				## 물약 슬롯
				for i in range(playerm2g2.AUTO_POSITINO_SLOT_START,playerm2g2.AUTO_POSITINO_SLOT_MAX):
					cooltime = self.timeeditlist[i-1].GetText()
					cooltime = self.CheckCooltimeText(cooltime)
					cooltime = playerm2g2.CheckPositionSlotCoolTime(i,self.autoslotindex[i],int(cooltime))
					if not cooltime == 0:
						playerm2g2.SetAutoSlotCoolTime(i,int(cooltime))
						self.timeeditlist[i-1].SetText(str(cooltime))
			else:
				for i in range(playerm2g2.AUTO_POSITINO_SLOT_START,playerm2g2.AUTO_POSITINO_SLOT_MAX):
					self.SetAutoCooltime(i,0)

			chrmgrm2g.AutoStartOnOff(onoff,command)
			self.autostartonoff = onoff
			
		elif type == self.AUTO_ONOFF_ATTACK:
			chrmgrm2g.AutoAttackOnOff(onoff)

		elif type == self.AUTO_ONOFF_SKILL:
			chrmgrm2g.AutoSkillOnOff(onoff)
		elif type == self.AUTO_ONOFF_POSITION:
			chrmgrm2g.AutoPositionOnOff(onoff)
		elif type == self.AUTO_ONOFF_AUTO_RANGE:
			chrmgrm2g.AutoRangeOnOff(onoff)

		if command == True:
			if onoff == False:
				self.Close()
				return

		self.autoonoffbuttonlist[number].Down()
		self.autoonoffbuttonlist[number].Disable()
		if onoff == 1:
			number = number+1
		else:
			number = number-1
		self.autoonoffbuttonlist[number].SetUp()
		self.autoonoffbuttonlist[number].Enable()
		
	def LoadAutoWindow(self):
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow()
			self.SetCenterPosition()
			self.ReadAutoInfo()
	
	def Show(self):
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow()
			self.SetCenterPosition()

		self.SetTop()
		self.ReadAutoInfo()
		self.RefreshAutoPositionSlot()
		self.RefreshAutoSkillSlot()
		self.isOpen = 1
		
		if not item.CheckAffect(chr.NEW_AFFECT_AUTO_USE,0):
			for i in range(4,7):
				self.autoonoffbuttonlist[i].Down()
				self.autoonoffbuttonlist[i].Disable()
			chrmgrm2g.AutoSkillOnOff(0)
			chrmgrm2g.AutoPositionOnOff(0)
				
		if not chrmgrm2g.GetAutoOnOff():
			return
		else:
			ui.ScriptWindow.Show(self)

	def ReadAutoInfo(self):
	
		if (str)(chr.GetName()) == "0":
			return

		handle = app.OpenTextFile('UserData/'+chr.GetName())
		count = app.GetTextFileLineCount(handle)
		count = count / 2
		index = 0

		if count > 0:
			for slotindex in xrange(count):
				slotline = app.GetTextFileLine(handle, index)

				if slotindex < playerm2g2.AUTO_SKILL_SLOT_MAX:
					playerm2g2.SetAutoSkillSlotIndex(slotindex,int(slotline))
				else:
					playerm2g2.SetAutoPositionSlotIndex(slotindex+1,int(slotline))

				line = app.GetTextFileLine(handle, index+1)
				if not line == "":
					if slotindex < playerm2g2.AUTO_SKILL_SLOT_MAX:
						cooltime = playerm2g2.CheckSkillSlotCoolTime(slotindex,int(slotline),int(line))
						playerm2g2.SetAutoSlotCoolTime(slotindex,int(cooltime))
						self.timeeditlist[slotindex].SetText(str(cooltime))
					else:
						cooltime = playerm2g2.CheckPositionSlotCoolTime(slotindex, int(slotline), int(line))
						playerm2g2.SetAutoSlotCoolTime(slotindex,int(cooltime))
						self.timeeditlist[slotindex].SetText(str(cooltime))

				index +=2
				
		
		app.CloseTextFile(handle)
		self.isFirstReadFile = True

		self.RefreshAutoPositionSlot()
		self.RefreshAutoSkillSlot()
		
				
	def SaveAutoInfo(self):
	
		if (str)(chr.GetName()) == "0":
			return
			
		import os
		if os.path.exists('UserData') is False:
			os.makedirs('UserData')

		output_AutoSystemFile = open('UserData/'+chr.GetName(), 'w')

		for slotindex in xrange(playerm2g2.AUTO_SKILL_SLOT_MAX):
			linestr = str( self.autoslotindex[slotindex] ) + '\n'
			output_AutoSystemFile.write(linestr)
			
			if not self.timeeditlist[slotindex].GetText() == "":
				cooltime = playerm2g2.CheckSkillSlotCoolTime(slotindex,self.autoslotindex[slotindex],int(self.timeeditlist[slotindex].GetText()))
				linestr = str(cooltime) + '\n'
			else:
				linestr = self.timeeditlist[slotindex].GetText() + '\n'
			output_AutoSystemFile.write(linestr)
			

		for slotindex in range(playerm2g2.AUTO_POSITINO_SLOT_START,playerm2g2.AUTO_POSITINO_SLOT_MAX):
			linestr = str( self.autoslotindex[slotindex] ) + '\n'
			output_AutoSystemFile.write(linestr)
			
			if not self.timeeditlist[slotindex-1].GetText() =="":
				cooltime = playerm2g2.CheckPositionSlotCoolTime(slotindex+1,self.autoslotindex[slotindex],int(self.timeeditlist[slotindex-1].GetText()))
				linestr = str(cooltime) + '\n'
			else:
				linestr = self.timeeditlist[slotindex-1].GetText() + '\n'
			output_AutoSystemFile.write(linestr)
			
		output_AutoSystemFile.close()

	def Close(self):
		self.Hide()
		self.isOpen = 0
		self.SaveAutoInfo()
		self.EditLineKillFocus()
		
	def EditLineKillFocus(self):
		for x in xrange(self.AUTO_COOLTIME_MAX):
			self.timeeditlist[x].KillFocus()

	def Destroy(self):
		self.isloded = 0
		self.Hide()
		if 0 != self.tooltipSkill:
			self.tooltipSkill.HideToolTip()
			
	## 스킬 슬롯 관련 ##
	def OnActivateSkill(self):
		if self.isOpen:
			self.RefreshAutoSkillSlot()
	
	def OnDeactivateSkill(self, slotindex):
		if self.isOpen:
			for i in xrange(playerm2g2.AUTO_SKILL_SLOT_MAX):
				(Position) = playerm2g2.GetAutoSlotIndex(i)
				if slotindex == Position:	
					self.autoslot.DeactivateSlot(i)
			
	def OnUseSkill(self, slotindex, coolTime):
		if self.isOpen:
			self.RefreshAutoSkillSlot()

	def SetSkillToolTip(self, tooltip):
		self.tooltipSkill = tooltip
	
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def SetAutoCooltime(self, slotindex, cooltime):
		self.autoslot.SetSlotCoolTime(slotindex, cooltime, 0)
		
	def SetCloseGame(self):
		self.closegame = True
		
	def GetAutoStartonoff(self):
		return self.autostartonoff
		
	def RefreshAutoPositionSlot(self):

		if not self.autoslot:
			return
		
		if self.closegame:
			return

		for slotindex in range(playerm2g2.AUTO_POSITINO_SLOT_START,playerm2g2.AUTO_POSITINO_SLOT_MAX):
		
			Position = playerm2g2.GetAutoSlotIndex(slotindex)
			if Position == playerm2g2.ITEM_SLOT_COUNT:
				self.autoslot.ClearSlot(slotindex)
				self.timeeditlist[slotindex-1].SetText("")
				self.autoslotindex[slotindex] = playerm2g2.ITEM_SLOT_COUNT
				continue

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				itemIndex = playerm2g2.GetItemIndex(playerm2g2.SLOT_TYPE_INVENTORY, Position)
				itemCount = playerm2g2.GetItemCount(playerm2g2.SLOT_TYPE_INVENTORY, Position)
			else:
				itemIndex = playerm2g2.GetItemIndex(Position)
				itemCount = playerm2g2.GetItemCount(Position)

			if itemCount <= 1:
				itemCount = 0
				
			self.autoslot.SetItemSlot(slotindex, itemIndex, itemCount)
			self.autoslotindex[slotindex] = Position

			coolTime = playerm2g2.GetAutoSlotCoolTime(slotindex)
			if self.timeeditlist[slotindex-1].GetText() == "":
				self.timeeditlist[slotindex-1].SetText(str(coolTime))
				
			if itemIndex == 0:
				self.autoslot.ClearSlot(slotindex)
				self.timeeditlist[slotindex-1].SetText("")
				playerm2g2.SetAutoPositionSlotIndex(slotindex, playerm2g2.ITEM_SLOT_COUNT)
				self.RefreshAutoPositionSlot()

		self.autoslot.RefreshSlot()
		
		if self.isFirstReadFile:
			self.SaveAutoInfo()
		else:
			self.ReadAutoInfo()

	def RefreshAutoSkillSlot(self):

		for slotindex in xrange(playerm2g2.AUTO_SKILL_SLOT_MAX):
		
			Position = playerm2g2.GetAutoSlotIndex(slotindex)
			
			if Position == 0:
				self.autoslot.ClearSlot(slotindex)
				self.timeeditlist[slotindex].SetText("")
				self.autoslotindex[slotindex] = 0
				continue
	
			skillIndex = playerm2g2.GetSkillIndex(Position)
			if 0 == skillIndex:
				self.autoslot.ClearSlot(slotindex)

			skillType = skill.GetSkillType(skillIndex)
			if skill.SKILL_TYPE_GUILD == skillType:
				import guild
				skillGrade = 0
				skillLevel = guild.GetSkillLevel(Position)
			else:
				skillGrade = playerm2g2.GetSkillGrade(Position)
				skillLevel = playerm2g2.GetSkillLevel(Position)

			self.autoslot.SetSkillSlotNew(slotindex, skillIndex, skillGrade, skillLevel)
			self.autoslot.SetSlotCountNew(slotindex, skillGrade, skillLevel)
			self.autoslot.SetCoverButton(slotindex)

			## NOTE : CoolTime 체크
			if playerm2g2.IsSkillCoolTime(Position):
				(coolTime, elapsedTime) = playerm2g2.GetSkillCoolTime(Position)
				self.autoslot.SetSlotCoolTime(slotindex, coolTime, elapsedTime)

			## NOTE : Activate 되어 있다면 아이콘도 업데이트
			if playerm2g2.IsSkillActive(Position):
				self.autoslot.ActivateSlot(slotindex)

			self.autoslotindex[slotindex] = Position

			## 쿨타임 셋팅
			coolTime = playerm2g2.GetAutoSlotCoolTime(slotindex)
			if self.timeeditlist[slotindex].GetText() == "":
				self.timeeditlist[slotindex].SetText(str(coolTime))
			
		self.autoslot.RefreshSlot()

	def AddAutoSlot(self, slotindex):
		AttachedSlotType = mouseModule.mouseController.GetAttachedType()
		AttachedSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
		AttachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
		
		if slotindex <= playerm2g2.AUTO_SKILL_SLOT_MAX:
			if playerm2g2.SLOT_TYPE_SKILL == AttachedSlotType:
				playerm2g2.SetAutoSkillSlotIndex(slotindex,AttachedSlotNumber)
				self.RefreshAutoSkillSlot()
			elif playerm2g2.SLOT_TYPE_AUTO == AttachedSlotType:
				if slotindex == AttachedSlotNumber:
					return
				if AttachedSlotNumber >= playerm2g2.AUTO_SKILL_SLOT_MAX:
					return
				playerm2g2.SetAutoSkillSlotIndex(slotindex,AttachedItemIndex)
				self.RefreshAutoSkillSlot()
		else:
			if playerm2g2.SLOT_TYPE_INVENTORY == AttachedSlotType:
				itemIndex = playerm2g2.GetItemIndex(AttachedSlotNumber)
				item.SelectItem(itemIndex)
				ItemType		= item.GetItemType()
				ItemSubType	= item.GetItemSubType()
				itemRemaintime = 0

				if not ItemType == item.ITEM_TYPE_USE:
					return;
					
				if ItemSubType == item.USE_ABILITY_UP:
					itemRemaintime = item.GetValue(1)
				elif ItemSubType == item.USE_AFFECT:
					itemRemaintime = item.GetValue(3)

				if ItemSubType == item.USE_POTION \
				or ItemSubType == item.USE_ABILITY_UP \
				or ItemSubType == item.USE_POTION_NODELAY \
				or ItemSubType == item.USE_AFFECT:
					if itemRemaintime < 9999:
						playerm2g2.SetAutoPositionSlotIndex(slotindex,AttachedSlotNumber)
						self.RefreshAutoPositionSlot()

			elif playerm2g2.SLOT_TYPE_AUTO == AttachedSlotType:
				if slotindex == AttachedSlotNumber:
					return
				if AttachedSlotNumber <= playerm2g2.AUTO_SKILL_SLOT_MAX:
					return
				playerm2g2.SetAutoPositionSlotIndex(slotindex,AttachedItemIndex)
				self.RefreshAutoPositionSlot()
				
		mouseModule.mouseController.DeattachObject()
		
	def SelectActiveSkillEmptySlot(self, slotindex):
	
		if self.autostartonoff:
			return
			
		if True == mouseModule.mouseController.isAttached():
			self.AddAutoSlot(slotindex)

	def SelectActiveSkillSlot(self,slotindex):
		mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_AUTO, slotindex, self.autoslotindex[slotindex])

	def OverActiveSkillSlot(self,slotindex):
	
		if mouseModule.mouseController.isAttached():
			return	

		if slotindex <= playerm2g2.AUTO_SKILL_SLOT_MAX:
			Position = playerm2g2.GetAutoSlotIndex(slotindex)
			if Position == 0:
				return
			skillIndex = playerm2g2.GetSkillIndex(Position)
			skillType = skill.GetSkillType(skillIndex)
			if skill.SKILL_TYPE_GUILD == skillType:
				import guild
				skillGrade = 0
				skillLevel = guild.GetSkillLevel(Position)
			else:
				skillGrade = playerm2g2.GetSkillGrade(Position)
				skillLevel = playerm2g2.GetSkillLevel(Position)
			self.tooltipSkill.SetSkillNew(Position, skillIndex, skillGrade, skillLevel)
		else:
			Position = playerm2g2.GetAutoSlotIndex(slotindex)
			if Position == playerm2g2.ITEM_SLOT_COUNT:
				return
			if app.ENABLE_EXTEND_INVEN_SYSTEM:	
				self.tooltipItem.SetInventoryItem(Position, playerm2g2.SLOT_TYPE_INVENTORY)
				self.tooltipSkill.HideToolTip()
			else:
				self.tooltipItem.SetInventoryItem(Position)
				self.tooltipSkill.HideToolTip()
			
	def OverSkillSlotOutItem(self):
		if 0 != self.tooltipSkill:
			self.tooltipSkill.HideToolTip()

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()			
	## 스킬 슬롯 관련 ##

	def OnPressEscapeKey(self):
		self.Close()
		return True		
		