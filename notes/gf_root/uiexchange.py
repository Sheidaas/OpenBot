import playerm2g2
import exchange
import m2netm2g
import localeInfo
import chatm2g
import item

import ui
import mouseModule
import uiPickMoney
import wndMgr
import app

###################################################################################################
## Exchange
if app.ENABLE_CHEQUE_SYSTEM :
	INVENTORY_PAGE_SIZE = playerm2g2.INVENTORY_PAGE_SIZE
	
class ExchangeDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.TitleName = 0
		self.tooltipItem = 0
		self.xStart = 0
		self.yStart = 0
		self.interface = None
		if app.ENABLE_CHEQUE_SYSTEM:
			self.inven = None
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		if app.ENABLE_CHEQUE_SYSTEM:
			self.inven = None
		
	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		PythonScriptLoader.LoadScriptFile(self, "UIScript/exchangedialog.py")

		## Owner
		self.OwnerSlot = self.GetChild("Owner_Slot")
		self.OwnerSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectOwnerEmptySlot))
		self.OwnerSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectOwnerItemSlot))
		self.OwnerSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInOwnerItem))
		self.OwnerSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.OwnerMoney = self.GetChild("Owner_Money_Value")
		self.OwnerAcceptLight = self.GetChild("Owner_Accept_Light")
		self.OwnerAcceptLight.Disable()
		self.OwnerMoneyButton = self.GetChild("Owner_Money")
		if not app.ENABLE_CHEQUE_SYSTEM:
			self.OwnerMoneyButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		## Target
		self.TargetSlot = self.GetChild("Target_Slot")
		self.TargetSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInTargetItem))
		self.TargetSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.TargetMoney = self.GetChild("Target_Money_Value")
		self.TargetAcceptLight = self.GetChild("Target_Accept_Light")
		self.TargetAcceptLight.Disable()

		if app.ENABLE_CHEQUE_SYSTEM:
			self.OwnerCheque = self.GetChild("Owner_Cheque_Value")
			self.OwnerChequeButton = self.GetChild("Owner_Cheque")
			self.OwnerMoneyButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 0)
			self.OwnerChequeButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog), 1)
			self.TargetCheque = self.GetChild("Target_Cheque_Value")
		
		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
		dlgPickMoney.SetTitleName(localeInfo.EXCHANGE_MONEY)
		dlgPickMoney.SetMax(7)
		dlgPickMoney.Hide()
		self.dlgPickMoney = dlgPickMoney

		## Button
		self.AcceptButton = self.GetChild("Owner_Accept_Button")
		self.AcceptButton.SetToggleDownEvent(ui.__mem_func__(self.AcceptExchange))

		self.TitleName = self.GetChild("TitleName")
		self.GetChild("TitleBar").SetCloseEvent(m2netm2g.SendExchangeExitPacket)

	def Destroy(self):
		#print "---------------------------------------------------------------------------- DESTROY EXCHANGE"
		self.ClearDictionary()
		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0
		self.OwnerSlot = 0
		self.OwnerMoney = 0
		self.OwnerAcceptLight = 0
		self.OwnerMoneyButton = 0
		self.TargetSlot = 0
		self.TargetMoney = 0
		self.TargetAcceptLight = 0
		self.TitleName = 0
		self.AcceptButton = 0
		self.tooltipItem = 0

		if app.ENABLE_CHEQUE_SYSTEM:
			self.OwnerCheque = 0
			self.OwnerChequeButton = 0
			self.TargetCheque = 0
		
	def OpenDialog(self):
	
		if localeInfo.IsEUROPE() or localeInfo.IsYMIR(): 
			self.TitleName.SetText(localeInfo.EXCHANGE_TITLE % (exchange.GetNameFromTarget(), exchange.GetLevelFromTarget()))
		else:
			self.TitleName.SetText(localeInfo.EXCHANGE_TITLE % (exchange.GetNameFromTarget()))

		self.AcceptButton.Enable()
		self.AcceptButton.SetUp()
		self.SetTop()
		self.Show()

		(self.xStart, self.yStart, z) = playerm2g2.GetMainCharacterPosition()

		if app.ENABLE_CHEQUE_SYSTEM:
			self.ItemListIdx = []
			
	def CloseDialog(self):
		wndMgr.OnceIgnoreMouseLeftButtonUpEvent()

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.dlgPickMoney.Close()
		self.Hide()
		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_NONE)
				self.interface.RefreshMarkInventoryBag()

		if app.ENABLE_CHEQUE_SYSTEM:
			self.ItemListIdx = None			

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	if app.ENABLE_CHEQUE_SYSTEM:
		def OpenPickMoneyDialog(self, focus_idx):
			if exchange.GetElkFromSelf() > 0 or exchange.GetChequeFromSelf() > 0 :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANT_EDIT_MONEY)
				return

			self.dlgPickMoney.Open(playerm2g2.GetElk(), playerm2g2.GetCheque())
			self.dlgPickMoney.SetFocus(focus_idx)
			
		def OnPickMoney(self, money, cheque):
			m2netm2g.SendExchangeElkAddPacket(money, cheque)	
	else:
		def OpenPickMoneyDialog(self):
			if exchange.GetElkFromSelf() > 0:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANT_EDIT_MONEY)
				return

			self.dlgPickMoney.Open(playerm2g2.GetElk())
		
		def OnPickMoney(self, money):
			m2netm2g.SendExchangeElkAddPacket(money)

	def AcceptExchange(self):
		m2netm2g.SendExchangeAcceptPacket()
		self.AcceptButton.Disable()

	def SelectOwnerEmptySlot(self, SlotIndex):

		if False == mouseModule.mouseController.isAttached():
			return
		
		if playerm2g2.GetAcceRefineWindowOpen() == 1:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.ACCE_NOT_WINDOWOPEN)
			return

		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_OPEN_OTHER_WINDOW)
				return


		if mouseModule.mouseController.IsAttachedMoney():
			if app.ENABLE_CHEQUE_SYSTEM:
				m2netm2g.SendExchangeElkAddPacket(mouseModule.mouseController.GetAttachedMoneyAmount(), mouseModule.mouseController.GetCheque())
			else:
				m2netm2g.SendExchangeElkAddPacket(mouseModule.mouseController.GetAttachedMoneyAmount())
		else:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			if (playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType
				or playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType):

				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				SrcSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
				DstSlotNumber = SlotIndex

				itemID = playerm2g2.GetItemIndex(attachedInvenType, SrcSlotNumber)
				item.SelectItem(itemID)

				if playerm2g2.IsAntiFlagBySlot(SrcSlotNumber, item.ANTIFLAG_GIVE):
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
					mouseModule.mouseController.DeattachObject()
					return

				m2netm2g.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)
				if app.ENABLE_CHEQUE_SYSTEM :
					self.ItemListIdx.append(SrcSlotNumber)
				
		mouseModule.mouseController.DeattachObject()

	if app.ENABLE_CHEQUE_SYSTEM:
		def SelectOwnerItemSlot(self, SlotIndex):

			if playerm2g2.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():

				money = mouseModule.mouseController.GetAttachedItemCount()
				cheque = mouseModule.mouseController.GetCheque()

				m2netm2g.SendExchangeElkAddPacket(money, cheque)
	else:
		def SelectOwnerItemSlot(self, SlotIndex):

			if playerm2g2.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():

				money = mouseModule.mouseController.GetAttachedItemCount()
				m2netm2g.SendExchangeElkAddPacket(money)

	def RefreshOwnerSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			itemCount = exchange.GetItemCountFromSelf(i)
			if 1 == itemCount:
				itemCount = 0
			self.OwnerSlot.SetItemSlot(i, itemIndex, itemCount)
			
			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				changelookvnum = exchange.GetChangeLookVnumFromSelf(i)
				if not changelookvnum == 0:
					self.OwnerSlot.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
				else:
					self.OwnerSlot.EnableSlotCoverImage(i,False)

		self.OwnerSlot.RefreshSlot()

	def RefreshTargetSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			itemCount = exchange.GetItemCountFromTarget(i)
			if 1 == itemCount:
				itemCount = 0
			self.TargetSlot.SetItemSlot(i, itemIndex, itemCount)
			
			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				changelookvnum = exchange.GetChangeLookVnumFromTarget(i)
				if not changelookvnum == 0:
					self.TargetSlot.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
				else:
					self.TargetSlot.EnableSlotCoverImage(i,False)
			
		self.TargetSlot.RefreshSlot()

	def Refresh(self):

		self.RefreshOwnerSlot()
		self.RefreshTargetSlot()

		if app.ENABLE_CHEQUE_SYSTEM:
			self.OwnerCheque.SetText(str(exchange.GetChequeFromSelf()))
			self.TargetCheque.SetText(str(exchange.GetChequeFromTarget()))
			self.OwnerMoney.SetText(localeInfo.NumberToMoneyString(exchange.GetElkFromSelf()))
			self.TargetMoney.SetText(localeInfo.NumberToMoneyString(exchange.GetElkFromTarget()))
		else:
			self.OwnerMoney.SetText(str(exchange.GetElkFromSelf()))
			self.TargetMoney.SetText(str(exchange.GetElkFromTarget()))	

		if True == exchange.GetAcceptFromSelf():
			self.OwnerAcceptLight.Down()
		else:
			self.AcceptButton.Enable()
			self.AcceptButton.SetUp()
			self.OwnerAcceptLight.SetUp()

		if True == exchange.GetAcceptFromTarget():
			self.TargetAcceptLight.Down()
		else:
			self.TargetAcceptLight.SetUp()

	def OverInOwnerItem(self, slotIndex):

		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeOwnerItem(slotIndex)

	def OverInTargetItem(self, slotIndex):

		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeTargetItem(slotIndex)

	def OverOutItem(self):

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	if not app.WJ_ENABLE_TRADABLE_ICON:
		def OnTop(self):
			self.tooltipItem.SetTop()

	def OnUpdate(self):

		USE_EXCHANGE_LIMIT_RANGE = 1000

		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		if abs(x - self.xStart) > USE_EXCHANGE_LIMIT_RANGE or abs(y - self.yStart) > USE_EXCHANGE_LIMIT_RANGE:
			(self.xStart, self.yStart, z) = playerm2g2.GetMainCharacterPosition()
			m2netm2g.SendExchangeExitPacket()
			
		if app.ENABLE_CHEQUE_SYSTEM :
			if not self.inven :
				return

			page = self.inven.GetInventoryPageIndex() # range 0 ~ 1

			for i in self.ItemListIdx :
				if (page * INVENTORY_PAGE_SIZE) <= i < ((page + 1) * INVENTORY_PAGE_SIZE): # range 0 ~ 44, 45 ~ 89
					lock_idx = i - (page * INVENTORY_PAGE_SIZE) 
					self.inven.wndItem.SetCantMouseEventSlot(lock_idx)
					

	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantTradableItem(self, slotIndex):
			itemIndex = playerm2g2.GetItemIndex(slotIndex)
		
			if itemIndex:
				if playerm2g2.GetItemSealDate(playerm2g2.INVENTORY, slotIndex) != -1: #ºÀÀÎ¾ÆÀÌÅÛ °É·¯³¿.
					return True
				return playerm2g2.IsAntiFlagBySlot(slotIndex, item.ANTIFLAG_GIVE)
			return False
			
		def BindInterface(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)
			
		def OnTop(self):
			self.tooltipItem.SetTop()
			if not self.interface:
				return
			
			self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_EXCHANGE)
			self.interface.RefreshMarkInventoryBag()

	if app.ENABLE_CHEQUE_SYSTEM :
		def SetInven(self, inven) :
			self.inven = inven
		
		def AddExchangeItemSlotIndex(self, idx) :
			self.ItemListIdx.append(idx)