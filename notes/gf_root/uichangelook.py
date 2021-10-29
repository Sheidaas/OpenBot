import ui
import playerm2g2
import mouseModule
import m2netm2g
import app
import snd
import item
import playerm2g2
import chatm2g
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiPickMoney
import uiCommon
import uiPrivateShopBuilder # 개인상점 열동안 ItemMove 방지
import localeInfo
import constInfo
import ime
import wndMgr
import uiToolTip

class ChangeLookWindow(ui.ScriptWindow):

	USE_CHANGELOOKWINDOW_LIMIT_RANGE = 500
	CHANGELOOK_SLOT_LEFT = 0
	CHANGELOOK_SLOT_RIGHT = 1
	CHANGELOOK_SLOT_MAX = 2
	if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
		CHANGELOOK_COST = 50000000
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isloded = 0
		self.tooltipitem = None
		self.xChangeLookWindowStart = 0
		self.yChangeLookWindowStart = 0
		self.ChangeLookToolTIpButton = None
		self.ChangeLookToolTip = None
		self.pop = None
		if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
			self.ChangeLookCost = None
		
			self.ChangeLookToolTipList = [localeInfo.CHANGE_TOOLTIP_LINE1, 
			localeInfo.CHANGE_TOOLTIP_LINE2,
			localeInfo.CHANGE_TOOLTIP_LINE3,
			localeInfo.CHANGE_TOOLTIP_LINE4,
			localeInfo.CHANGE_TOOLTIP_LINE5,
			localeInfo.CHANGE_TOOLTIP_LINE6]
		else:

			self.ChangeLookToolTipList = [localeInfo.CHANGE_TOOLTIP_LINE1, 
			localeInfo.CHANGE_TOOLTIP_LINE2,
			localeInfo.CHANGE_TOOLTIP_LINE3,
			localeInfo.CHANGE_TOOLTIP_LINE4]
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.isloded = 0
		self.tooltipitem = None
		self.pop = None
		self.ChangeLookToolTIpButton = None
		self.ChangeLookToolTip = None
		if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
			self.ChangeLookCost = None
		
	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/ChangeLookWindow.py")
		except:
			import exception
			exception.Abort("ChangeLookWindow.__LoadWindow.UIScript/ChangeLookWindow.py")
		try:
			wnditem = self.GetChild("ChangeLookSlot")
			if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
				wndpassitem = self.GetChild("ChangeLookSlot_PassYangItem")
			self.GetChild("CancelButton").SetEvent(ui.__mem_func__(self.Close))
			self.GetChild("AcceptButton").SetEvent(ui.__mem_func__(self.Accept))
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
	
			if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
				self.ChangeLookCost = self.GetChild("Cost")
				self.ChangeLookCost.SetText(localeInfo.CHANGE_LOOK_COST % (localeInfo.NumberToMoneyString(self.CHANGELOOK_COST)))
			else:
				self.GetChild("Cost").SetText(localeInfo.CHANGE_LOOK_COST)

			self.GetChild("TitleName").SetText(localeInfo.CHANGE_LOOK_TITLE)
		except:
			import exception
			exception.Abort("ChangeLookWindow.__LoadWindow.ChangeLookSlot")
			
		wnditem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wnditem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wnditem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wnditem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))						
		wnditem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wnditem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wnditem.Show()
		
		
		if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
			wndpassitem.SetOverInItemEvent(ui.__mem_func__(self.OverInItemFreeYang))
			wndpassitem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			wndpassitem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlotFreepass))
			wndpassitem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlotFreepass))						
			wndpassitem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlotFreepass))
			wndpassitem.Show()
			self.wndpassitem = wndpassitem
		
		self.wnditem = wnditem

		self.ChangeLookToolTIpButton = self.GetChild("ChangeLookToolTIpButton")
		self.ChangeLookToolTip = self.__CreateGameTypeToolTip(localeInfo.CHANGE_TOOLTIP_TITLE,self.ChangeLookToolTipList)
		self.ChangeLookToolTip.SetTop()
		self.ChangeLookToolTIpButton.SetToolTipWindow(self.ChangeLookToolTip)

	def __CreateGameTypeToolTip(self, title, descList):
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)
		if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
			toolTip.AppendSpace(7)
		else:
			toolTip.AppendSpace(5)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)

		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip

	def OnUpdate(self):
		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		if abs(x - self.xChangeLookWindowStart) > self.USE_CHANGELOOKWINDOW_LIMIT_RANGE or abs(y - self.yChangeLookWindowStart) > self.USE_CHANGELOOKWINDOW_LIMIT_RANGE:
			self.Close()
	
	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Open(self):
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow()
		self.SetCenterPosition()
		self.SetTop()
		ui.ScriptWindow.Show(self)
		(self.xChangeLookWindowStart, self.yChangeLookWindowStart, z) = playerm2g2.GetMainCharacterPosition()				
		playerm2g2.SetChangeLookWindow(True)
		self.RefreshChangeLookWindow()

	def Close(self):
		self.Hide()
		m2netm2g.SendChangeLookCanCle()
		playerm2g2.SetChangeLookWindow(False)
		
	def Accept(self):
		leftvnum = 	playerm2g2.GetChangeLookItemID(self.CHANGELOOK_SLOT_LEFT)
		rightvnum = playerm2g2.GetChangeLookItemID(self.CHANGELOOK_SLOT_RIGHT)
		if  leftvnum == 0 or rightvnum == 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_INSERT_ITEM)
		else:
			popup = uiCommon.QuestionDialog()
			popup.SetText(localeInfo.CHANGE_LOOK_CHANGE_ITEM)
			popup.SetAcceptEvent(self.SendAccept)
			popup.SetCancelEvent(self.OnCloseEvent)
			popup.Open()
			self.pop = popup

			
	def SendAccept(self):
		self.pop.Close()
		self.pop = None
		m2netm2g.SendChangeLookAccept()

	def SetItemToolTip(self, tooltip):
		self.tooltipitem = tooltip
		
	def __ShowToolTip(self, slotIndex):
		if self.tooltipitem:
			self.tooltipitem.SetChangeLookWindowItem(slotIndex)

	# 아이템 툴팁 보여주기
	def OverInItem(self, slotIndex):
		self.wnditem.SetUsableItem(False)
		self.__ShowToolTip(slotIndex)
	#
	## 아이템 툴팁 감추기
	def OverOutItem(self):
		self.wnditem.SetUsableItem(False)
		if self.tooltipitem:
			self.tooltipitem.HideToolTip()
			
	if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
		def OverInItemFreeYang(self, slotIndex):
			self.wnditem.SetUsableItem(False)
			self.__ShowToolTip_FreeItem(playerm2g2.GetChangeLookFreeYangInvenSlotPos())	
	
		def __ShowToolTip_FreeItem(self, slotIndex):
			if self.tooltipitem:
				self.tooltipitem.SetInventoryItem(slotIndex, playerm2g2.INVENTORY)
	
		## 외형변경 -> 인벤 (양 패스 아이템)
		def UseItemSlotFreepass(self, slotIndex):
			mouseModule.mouseController.DeattachObject()
			m2netm2g.SendChangeLookCheckOutFreeYangItem()
			self.ChangeLookCost.SetText(localeInfo.CHANGE_LOOK_COST % (localeInfo.NumberToMoneyString(self.CHANGELOOK_COST)))

		## 인벤 -> 외형변경 (양 패스 아이템)
		def SelectEmptySlotFreepass(self, selectedSlotPos):
			if mouseModule.mouseController.isAttached():

				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				ItemVNum = playerm2g2.GetItemIndex(attachedSlotPos)
			
				## 아이템 체크.
				if item.IsChangeLookFreePassYangItem(ItemVNum) == 0:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_REGISTER_ITEM)
					return
			
				m2netm2g.SendChangeLookCheckInFreeYangItem(attachedInvenType, attachedSlotPos)
				mouseModule.mouseController.DeattachObject()
				self.ChangeLookCost.SetText(localeInfo.CHANGE_LOOK_COST % (localeInfo.NumberToMoneyString(0)))

	## 인벤 -> 외형변경 창.
	def SelectEmptySlot(self, selectedSlotPos):

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			ItemVNum = playerm2g2.GetItemIndex(attachedSlotPos)
			
			## 아이템 체크.
			if selectedSlotPos == self.CHANGELOOK_SLOT_LEFT:
				if item.IsPossibleChangeLookLeft(ItemVNum) == 0:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_CHANGE_LOOK_ITEM)
					return
			else:
				if playerm2g2.GetChangeLookItemID(self.CHANGELOOK_SLOT_LEFT) == 0:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_INSERT_CHANGE_LOOK_ITEM)
					return
				if item.IsPossibleChangeLookRight(playerm2g2.GetChangeLookItemID(self.CHANGELOOK_SLOT_LEFT), ItemVNum) == 0:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_REGISTER_ITEM)
					return
			## 아이템 체크.

			item.SelectItem(ItemVNum)
			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				window = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if window == playerm2g2.EQUIPMENT:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_EQUIP_ITEM)
					return

			else:
				if attachedSlotPos > playerm2g2.EQUIPMENT_SLOT_START-1:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_EQUIP_ITEM)
					return

			if playerm2g2.SLOT_TYPE_CHANGE_LOOK != attachedSlotType:
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if playerm2g2.RESERVED_WINDOW == attachedInvenType:
					return

				if selectedSlotPos == self.CHANGELOOK_SLOT_LEFT:
					m2netm2g.SendChangeLookCheckIn(attachedInvenType, attachedSlotPos, selectedSlotPos)
				else:
					if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, attachedSlotPos) != -1:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_SEAL_ITEM)
						return
						
					if playerm2g2.GetChangeLookItemInvenSlot(self.CHANGELOOK_SLOT_LEFT) == attachedSlotPos:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_ALREADY_REGISTER)
						return
					
					m2netm2g.SendChangeLookCheckIn(attachedInvenType, attachedSlotPos, selectedSlotPos)							
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.CHANGE_LOOK_DEL_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.Open()
					self.pop = popup				
			
			mouseModule.mouseController.DeattachObject()

	## 아이템 사용 시 없애기
	def UseItemSlot(self, slotIndex):
		if slotIndex == self.CHANGELOOK_SLOT_LEFT:
			if playerm2g2.GetChangeLookItemID(self.CHANGELOOK_SLOT_RIGHT) == 0:
				mouseModule.mouseController.DeattachObject()
				m2netm2g.SendChangeLookCheckOut(slotIndex)
			else:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_CHECK_OUT_REGISTER_ITEM)
		else:
			mouseModule.mouseController.DeattachObject()
			m2netm2g.SendChangeLookCheckOut(slotIndex)

	## 아이템 클릭
	def SelectItemSlot(self, selectedSlotPos):

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType:
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				snd.PlaySound("sound/ui/drop.wav")
			mouseModule.mouseController.DeattachObject()
		else:			
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SAFEBOX_SELL_DISABLE_SAFEITEM)
			elif app.BUY == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			else:
				if selectedSlotPos == self.CHANGELOOK_SLOT_LEFT:
					if playerm2g2.GetChangeLookItemID(self.CHANGELOOK_SLOT_RIGHT) == 0:
						selectedItemID = playerm2g2.GetChangeLookItemID(selectedSlotPos)
						mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_CHANGE_LOOK, selectedSlotPos, selectedItemID)
						snd.PlaySound("sound/ui/pick.wav")
					else:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_CHECK_OUT_REGISTER_ITEM)
				else:
					selectedItemID = playerm2g2.GetChangeLookItemID(selectedSlotPos)
					mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_CHANGE_LOOK, selectedSlotPos, selectedItemID)
					snd.PlaySound("sound/ui/pick.wav")
	
	## 갱신
	def RefreshChangeLookWindow(self):

		if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
			if not playerm2g2.GetChangeLookWindowOpen():
				return

		setChangeLookItem = self.wnditem.SetItemSlot
		getChangeLookItem = playerm2g2.GetChangeLookItemID
		
		for i in xrange(self.CHANGELOOK_SLOT_MAX):
			ChangeLookSlotVnum = getChangeLookItem(i)
			if not ChangeLookSlotVnum == playerm2g2.ITEM_SLOT_COUNT:
				setChangeLookItem(i, ChangeLookSlotVnum, 1)
			else:
				setChangeLookItem(i, 0, 1)
				
			changelookvnum = playerm2g2.GetChangeWIndowChangeLookVnum(i)
			if not changelookvnum == 0:
				self.wnditem.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
			else:
				self.wnditem.EnableSlotCoverImage(i,False)	

		self.wnditem.RefreshSlot()

		if app.ENABLE_CHANGE_LOOK_ITEM_SYSTEM:
			ChangeLookFreeItemVnum = playerm2g2.GetChangeLookFreeYangItemID()
		
			if not  ChangeLookFreeItemVnum == 0:
				self.wndpassitem.SetItemSlot(0, ChangeLookFreeItemVnum, 1)
			else:
				self.ChangeLookCost.SetText(localeInfo.CHANGE_LOOK_COST % (localeInfo.NumberToMoneyString(self.CHANGELOOK_COST)))
				self.wndpassitem.SetItemSlot(0, 0, 1)

	def OnCloseEvent(self):
		self.pop.Close()
		self.pop = None

	def __OnClosePopupDialog(self):
		self.popup = None