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

class AcceWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.type = 0
		self.isloded = 0
		self.tooltipitem = None
		self.xAcceWindowStart = 0
		self.yAcceWindowStart = 0
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.tooltipitem = None
		
	def __LoadWindow(self, type):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			if type == playerm2g2.ACCE_SLOT_TYPE_COMBINE:
				pyScrLoader.LoadScriptFile(self, "UIScript/Acce_CombineWindow.py")
				self.cost = self.GetChild("Cost")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/Acce_AbsorbWindow.py")
		except:
			import exception
			exception.Abort("AcceWindow.__LoadWindow.UIScript/Acce_CombineWindow.py")
		try:
			wnditem = self.GetChild("AcceSlot")
			self.GetChild("CancelButton").SetEvent(ui.__mem_func__(self.Close))
			self.GetChild("AcceptButton").SetEvent(ui.__mem_func__(self.Accept))
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("AcceWindow.__LoadWindow.AcceSlot")
			
		wnditem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wnditem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wnditem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wnditem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))						
		wnditem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wnditem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wnditem.Show()

		self.wnditem = wnditem
		
	def Accept(self):
		if playerm2g2.GetCurrentItemCount() == 3:
			m2netm2g.SendAcceRefineAccept(self.type)
		else:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_INITEM)

	def Open(self,type):
	
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow(type)
			self.type = type
			self.SetCenterPosition()
			self.SetTop()
			ui.ScriptWindow.Show(self)
			playerm2g2.SetAcceRefineWindowOpen(type)
			(self.xAcceWindowStart, self.yAcceWindowStart, z) = playerm2g2.GetMainCharacterPosition()				
	
	def Close(self):
		if playerm2g2.IsAcceWindowEmpty() == 1:
			self.Hide()
			self.isloded = 0
			playerm2g2.SetAcceRefineWindowOpen(self.type)
		else:
			self.Hide()
			self.isloded = 0
			playerm2g2.SetAcceRefineWindowOpen(self.type)
			m2netm2g.SendAcceRefineCheckOut(0)
			m2netm2g.SendAcceRefineCheckOut(1)
		m2netm2g.SendAcceRefineCanCle()

	def SetItemToolTip(self, tooltip):
		self.tooltipitem = tooltip
		
	def __ShowToolTip(self, slotIndex):
		if self.tooltipitem:
			self.tooltipitem.SetAcceWindowItem(slotIndex)

	# 아이템 툴팁 보여주기
	def OverInItem(self, slotIndex):
		self.wnditem.SetUsableItem(False)
		self.__ShowToolTip(slotIndex)
	
	# 아이템 툴팁 감추기
	def OverOutItem(self):
		self.wnditem.SetUsableItem(False)
		if self.tooltipitem:
			self.tooltipitem.HideToolTip()
	
	# 인벤 -> 악사세리 창.
	def SelectEmptySlot(self, selectedSlotPos):
		if selectedSlotPos == (playerm2g2.ACCE_SLOT_MAX - 1):
			return
		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			ItemVNum = playerm2g2.GetItemIndex(attachedSlotPos)
			item.SelectItem(ItemVNum)

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				window = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if window == playerm2g2.EQUIPMENT:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_USINGITEM)
					return
										
			else:
				if attachedSlotPos > playerm2g2.EQUIPMENT_SLOT_START-1: ## 인벤창 안에 있는 것만.
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_USINGITEM)
					return

			if playerm2g2.SLOT_TYPE_ACCE != attachedSlotType:
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if playerm2g2.RESERVED_WINDOW == attachedInvenType:
					return
				possablecheckin = 0
				# 조합창일때
				if playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_COMBINE:
					if item.GetItemType() == item.ITEM_TYPE_COSTUME:
						if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
						
							if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
								socketInDrainValue = playerm2g2.GetItemMetinSocket(attachedSlotPos, 1)
								if socketInDrainValue >= app.ACCE_MAX_DRAINRATE:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_MAX_DRAINRATE)
									return

								usingSlot = playerm2g2.FindActivedAcceSlot(attachedSlotPos)
								if playerm2g2.FindUsingAcceSlot(usingSlot) == attachedSlotPos:
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_ALREADY_REGISTER)
									return
								possablecheckin = 1
							else:
								if item.GetRefinedVnum() == 0: ## 전선등급 아이템은 걸러냄.
									chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_MAXGRADE)
									return
								else:
									usingSlot = playerm2g2.FindActivedAcceSlot(attachedSlotPos)
									if playerm2g2.FindUsingAcceSlot(usingSlot) == attachedSlotPos:
										chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_ALREADY_REGISTER)
										return
									possablecheckin = 1	
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCE)
							return
					else:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCE)
						return

				# 흡수창일때 악세서리, 아이템 구분
				if playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_ABSORB:
					if selectedSlotPos == playerm2g2.ACCE_SLOT_LEFT:
						if item.GetItemType() == item.ITEM_TYPE_COSTUME:
							if item.GetItemSubType() == item.COSTUME_TYPE_ACCE:
								if playerm2g2.GetItemMetinSocket(attachedSlotPos,0) == 0:
									possablecheckin = 1
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCE)
								return
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCE)
							return

					elif selectedSlotPos == playerm2g2.ACCE_SLOT_RIGHT:
						if item.GetItemType() == item.ITEM_TYPE_WEAPON:
							possablecheckin = 1
						elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
							if item.GetItemSubType() == item.ARMOR_BODY:
								possablecheckin = 1
							else:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCEITEM)
								return
						else:
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCEITEM)
							return

						if localeInfo.IsBRAZIL():
							## 브라질에서 아래 나열된 아이템은 능력치가 상당히 강해서 흡수 안되게 해달라고 조름.
							## 어쩔수 없이 하드코딩함. 
							itemvnum = item.GetVnum()
							if itemvnum == 11979 or itemvnum == 11980 or itemvnum == 11981 or itemvnum == 11982 or itemvnum == 11971 or itemvnum == 11972 or itemvnum == 11973 or itemvnum == 11974:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_DONOT_ABSORDITEM)
								return

						if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
							itemvnum = item.GetVnum()
							if item.IsWedddingItem(itemvnum) == 1:
								chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_POSSIBLE_ACCEITEM)
								return

				if possablecheckin:
					## 봉인아이템 걸러냄
					if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, attachedSlotPos) != -1:
						chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_SEALITEM)
						return
						
					if playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_COMBINE:
						playerm2g2.SetAcceActivedItemSlot(selectedSlotPos, attachedSlotPos)
						m2netm2g.SendAcceRefineCheckIn(attachedInvenType, attachedSlotPos, selectedSlotPos, self.type)
						

					elif playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_ABSORB:
					
						if selectedSlotPos == playerm2g2.ACCE_SLOT_RIGHT:
							popup = uiCommon.QuestionDialog()
							popup.SetText(localeInfo.ACCE_DEL_ABSORDITEM)
							popup.SetAcceptEvent(lambda arg1=attachedInvenType, arg2=attachedSlotPos, arg3=selectedSlotPos: self.OnAcceAcceptEvent(arg1,arg2,arg3))
							popup.SetCancelEvent(self.OnAcceCloseEvent)
							popup.Open()
							self.pop = popup
						else:
							playerm2g2.SetAcceActivedItemSlot(selectedSlotPos, attachedSlotPos)
							m2netm2g.SendAcceRefineCheckIn(attachedInvenType, attachedSlotPos, selectedSlotPos, self.type)
						
					snd.PlaySound("sound/ui/drop.wav")

			## 경고 메시지 띄우기.
			if not playerm2g2.FindUsingAcceSlot(playerm2g2.ACCE_SLOT_RIGHT) == playerm2g2.ITEM_SLOT_COUNT and not playerm2g2.FindUsingAcceSlot(playerm2g2.ACCE_SLOT_LEFT) == playerm2g2.ITEM_SLOT_COUNT:
				if selectedSlotPos != playerm2g2.ACCE_SLOT_MAX:
					popup = uiCommon.PopupDialog()
					if playerm2g2.GetAcceRefineWindowType() == playerm2g2.ACCE_SLOT_TYPE_COMBINE:

						if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
							socketInDrainValue = playerm2g2.GetAcceItemMetinSocket(0, 1)
							socketInDrainValue2 = playerm2g2.GetAcceItemMetinSocket(1, 1)
							socketInDrainValue3 = playerm2g2.GetItemMetinSocket(attachedSlotPos, 1)
							## 메인 서버 중. 등록된 아이템이 전설일때 경고 메시지 변경.
							if socketInDrainValue > 0 or socketInDrainValue2 > 0 or socketInDrainValue3 > 0:
								popup.SetText(localeInfo.ACCE_DEL_SERVEITEM2)
							else:
								popup.SetText(localeInfo.ACCE_DEL_SERVEITEM)
						else:
							popup.SetText(localeInfo.ACCE_DEL_SERVEITEM)
								
						popup.SetAcceptEvent(self.__OnClosePopupDialog)
						popup.Open()
						self.popup = popup
				
			mouseModule.mouseController.DeattachObject()
				
	## 아이템 흡수시 흡수될 아이템 할지 안할지 선택 팝업
	def OnAcceAcceptEvent(self, attachedInvenType, attachedSlotPos, selectedSlotPos):
		self.pop.Close()
		self.pop = None
		playerm2g2.SetAcceActivedItemSlot(selectedSlotPos, attachedSlotPos)
		m2netm2g.SendAcceRefineCheckIn(attachedInvenType, attachedSlotPos, selectedSlotPos, self.type)

	def OnAcceCloseEvent(self):
		self.pop.Close()
		self.pop = None

	def UseItemSlot(self, slotIndex):
	
		if slotIndex == (playerm2g2.ACCE_SLOT_MAX - 1):
			return

		mouseModule.mouseController.DeattachObject()
		m2netm2g.SendAcceRefineCheckOut(slotIndex)

	def SelectItemSlot(self, selectedSlotPos):
		if selectedSlotPos == (playerm2g2.ACCE_SLOT_MAX - 1):
			return		

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
				selectedItemID = playerm2g2.GetAcceItemID(selectedSlotPos)
				mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_ACCE, selectedSlotPos, selectedItemID)
				snd.PlaySound("sound/ui/pick.wav")
	
	def RefreshAcceWindow(self):
		getAcceItem = playerm2g2.GetAcceItemID
		setAcceItem = self.wnditem.SetItemSlot
		AcceItemSize = playerm2g2.GetAcceItemSize()
		
		for i in xrange(AcceItemSize):
			setAcceItem(i, getAcceItem(i), 1)
			if self.type == playerm2g2.ACCE_SLOT_TYPE_COMBINE:

				if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
					if i == playerm2g2.ACCE_SLOT_LEFT:
						if getAcceItem(i) != 0:
							item.SelectItem(getAcceItem(i))
							self.cost.SetText(localeInfo.ACCE_ABSORB_COST % (item.GetIBuyItemPrice()))
						else:
							self.cost.SetText("")
				else:
					if i == playerm2g2.ACCE_SLOT_MAX - playerm2g2.ACCE_SLOT_MAX:
						if getAcceItem(i) != 0:
							item.SelectItem(getAcceItem(i))
							self.cost.SetText(localeInfo.ACCE_ABSORB_COST % (item.GetIBuyItemPrice()))
						else:
							self.cost.SetText("")
							

				if app.ENABLE_ACCE_SECOND_COSTUME_SYSTEM:
					if i == playerm2g2.ACCE_SLOT_RIGHT:
						if getAcceItem(i) != 0:
							item.SelectItem(getAcceItem(i))
							if item.GetRefinedVnum() == 0:
								self.cost.SetText(localeInfo.ACCE_ABSORB_COST % (item.GetIBuyItemPrice()))		
			
			if app.ENABLE_CHANGE_LOOK_SYSTEM:	
				if self.type == playerm2g2.ACCE_SLOT_TYPE_ABSORB:
					changelookvnum = playerm2g2.GetAcceWindowChangeLookVnum(i)
					if not changelookvnum == 0:
						self.wnditem.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
					else:
						self.wnditem.EnableSlotCoverImage(i,False)						
	
		self.wnditem.RefreshSlot()
	
	def __OnClosePopupDialog(self):
		self.popup = None
		
	def OnUpdate(self):
		USE_ACCEWINDOW_LIMIT_RANGE = 500
		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		if abs(x - self.xAcceWindowStart) > USE_ACCEWINDOW_LIMIT_RANGE or abs(y - self.yAcceWindowStart) > USE_ACCEWINDOW_LIMIT_RANGE:
			self.Close()
	
	def OnPressEscapeKey(self):
		self.Close()
		return True

		
	
