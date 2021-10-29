import ui
import mouseModule
import playerm2g2
import m2netm2g
import snd
import safebox
import chatm2g
import app
import localeInfo
import uiScriptLocale
import item

class PasswordDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

		self.sendMessage = "/safebox_password "

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
#			if localeInfo.IsEUROPE()and app.GetLocalePath() != "locale/ca"and app.GetLocalePath() != "locale/sg" :
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "passworddialog.py")
#			else:
#				pyScrLoader.LoadScriptFile(self, "uiscript/passworddialog.py")
		except:
			import exception
			exception.Abort("PasswordDialog.__LoadDialog.LoadObject")

		try:
			self.passwordValue = self.GetChild("password_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")
			self.titleName = self.GetChild("TitleName")
			self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.CloseDialog))
		except:
			import exception
			exception.Abort("PasswordDialog.__LoadDialog.BindObject")

		self.passwordValue.OnIMEReturn = ui.__mem_func__(self.OnAccept)
		self.passwordValue.OnPressEscapeKey = ui.__mem_func__(self.OnCancel)
		self.acceptButton.SetEvent(ui.__mem_func__(self.OnAccept))
		self.cancelButton.SetEvent(ui.__mem_func__(self.OnCancel))

	def Destroy(self):
		self.ClearDictionary()
		self.passwordValue = None
		self.acceptButton = None
		self.cancelButton = None
		self.titleName = None

	def SetTitle(self, title):
		self.titleName.SetText(title)

	def SetSendMessage(self, msg):
		self.sendMessage = msg

	def ShowDialog(self):
		if app.ENABLE_GROWTH_PET_SYSTEM:
			if playerm2g2.IsOpenPetHatchingWindow():
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_HATCHING_WINDOW_OPEN_CAN_NOT_USE)
				return False
				
		self.passwordValue.SetText("")
		self.passwordValue.SetFocus()
		self.SetCenterPosition()
		self.Show()

	def CloseDialog(self):
		self.passwordValue.KillFocus()
		self.Hide()

	def OnAccept(self):
		m2netm2g.SendChatPacket(self.sendMessage + self.passwordValue.GetText())
		self.CloseDialog()
		return True

	def OnCancel(self):
		self.CloseDialog()
		return True

class ChangePasswordDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		self.dlgMessage = ui.ScriptWindow()
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgMessage, "uiscript/popupdialog.py")
			self.dlgMessage.GetChild("message").SetText(localeInfo.SAFEBOX_WRONG_PASSWORD)
			self.dlgMessage.GetChild("accept").SetEvent(ui.__mem_func__(self.OnCloseMessageDialog))
		except:
			import exception
			exception.Abort("SafeboxWindow.__LoadDialog.LoadObject")

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/changepassworddialog.py")

		except:
			import exception
			exception.Abort("ChangePasswordDialog.LoadDialog.LoadObject")

		try:
			self.GetChild("accept_button").SetEvent(ui.__mem_func__(self.OnAccept))
			self.GetChild("cancel_button").SetEvent(ui.__mem_func__(self.OnCancel))
			self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.OnCancel))
			oldPassword = self.GetChild("old_password_value")
			newPassword = self.GetChild("new_password_value")
			newPasswordCheck = self.GetChild("new_password_check_value")
		except:
			import exception
			exception.Abort("ChangePasswordDialog.LoadDialog.BindObject")

		oldPassword.SetTabEvent(lambda arg=1: self.OnNextFocus(arg))
		newPassword.SetTabEvent(lambda arg=2: self.OnNextFocus(arg))
		newPasswordCheck.SetTabEvent(lambda arg=3: self.OnNextFocus(arg))
		oldPassword.SetReturnEvent(lambda arg=1: self.OnNextFocus(arg))
		newPassword.SetReturnEvent(lambda arg=2: self.OnNextFocus(arg))
		newPasswordCheck.SetReturnEvent(ui.__mem_func__(self.OnAccept))
		oldPassword.OnPressEscapeKey = self.OnCancel
		newPassword.OnPressEscapeKey = self.OnCancel
		newPasswordCheck.OnPressEscapeKey = self.OnCancel

		self.oldPassword = oldPassword
		self.newPassword = newPassword
		self.newPasswordCheck = newPasswordCheck

	def OnNextFocus(self, arg):
		if 1 == arg:
			self.oldPassword.KillFocus()
			self.newPassword.SetFocus()
		elif 2 == arg:
			self.newPassword.KillFocus()
			self.newPasswordCheck.SetFocus()
		elif 3 == arg:
			self.newPasswordCheck.KillFocus()
			self.oldPassword.SetFocus()

	def Destroy(self):
		self.ClearDictionary()
		self.dlgMessage.ClearDictionary()
		self.oldPassword = None
		self.newPassword = None
		self.newPasswordCheck = None

	def Open(self):
		self.oldPassword.SetText("")
		self.newPassword.SetText("")
		self.newPasswordCheck.SetText("")
		self.oldPassword.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.oldPassword.SetText("")
		self.newPassword.SetText("")
		self.newPasswordCheck.SetText("")
		self.oldPassword.KillFocus()
		self.newPassword.KillFocus()
		self.newPasswordCheck.KillFocus()
		self.Hide()

	def OnAccept(self):
		oldPasswordText = self.oldPassword.GetText()
		newPasswordText = self.newPassword.GetText()
		newPasswordCheckText = self.newPasswordCheck.GetText()
		if newPasswordText != newPasswordCheckText:
			self.dlgMessage.SetCenterPosition()
			self.dlgMessage.SetTop()
			self.dlgMessage.Show()
			return True
		m2netm2g.SendChatPacket("/safebox_change_password %s %s" % (oldPasswordText, newPasswordText))
		self.Close()
		return True

	def OnCancel(self):
		self.Close()
		return True

	def OnCloseMessageDialog(self):
		self.newPassword.SetText("")
		self.newPasswordCheck.SetText("")
		self.newPassword.SetFocus()
		self.dlgMessage.Hide()

class SafeboxWindow(ui.ScriptWindow):

	BOX_WIDTH = 176

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.pageButtonList = []
		self.curPageIndex = 0
		self.isLoaded = 0
		self.xSafeBoxStart = 0
		self.ySafeBoxStart = 0
		if app.ENABLE_EXTEND_MALLBOX:
			self.timeSendClosePacket = 0
		self.interface = None

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)		

	def Destroy(self):
		self.ClearDictionary()

		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = None
		self.dlgChangePassword.Destroy()
		self.dlgChangePassword = None

		self.tooltipItem = None
		self.wndMoneySlot = None
		self.wndMoney = None
		self.wndBoard = None
		self.wndItem = None

		self.pageButtonList = []

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "UIScript/SafeboxWindow.py")

		from _weakref import proxy

		## Item
		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self)
		wndItem.SetPosition(8, 35)
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.Show()

		## PickMoneyDialog
		import uiPickMoney
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
		dlgPickMoney.Hide()

		## ChangePasswrod
		dlgChangePassword = ChangePasswordDialog()
		dlgChangePassword.LoadDialog()
		dlgChangePassword.Hide()

		## Close Button
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		self.GetChild("ChangePasswordButton").SetEvent(ui.__mem_func__(self.OnChangePassword))
		self.GetChild("ExitButton").SetEvent(ui.__mem_func__(self.Close))

		self.wndItem = wndItem
		self.dlgPickMoney = dlgPickMoney
		self.dlgChangePassword = dlgChangePassword
		self.wndBoard = self.GetChild("board")
		#self.wndMoney = self.GetChild("Money")
		#self.wndMoneySlot = self.GetChild("Money_Slot")
		#self.wndMoneySlot.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		## Initialize
		self.SetTableSize(3)
		self.RefreshSafeboxMoney()

	def OpenPickMoneyDialog(self):

		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if playerm2g2.SLOT_TYPE_INVENTORY == mouseModule.mouseController.GetAttachedType():

				if playerm2g2.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					m2netm2g.SendSafeboxSaveMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

			mouseModule.mouseController.DeattachObject()

		else:
			curMoney = safebox.GetMoney()

			if curMoney <= 0:
				return

			self.dlgPickMoney.Open(curMoney)

	def ShowWindow(self, size):

		(self.xSafeBoxStart, self.ySafeBoxStart, z) = playerm2g2.GetMainCharacterPosition()

		self.SetTableSize(size)
		self.SetTop()
		self.Show()
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			playerm2g2.SetOpenSafeBox(True)

	def __MakePageButton(self, pageCount):

		self.curPageIndex = 0
		self.pageButtonList = []

		text = "I"
		pos = -int(float(pageCount-1)/2 * 52)
		for i in xrange(pageCount):
			button = ui.RadioButton()
			button.SetParent(self)
			button.SetUpVisual("d:/ymir work/ui/game/windows/tab_button_middle_01.sub")
			button.SetOverVisual("d:/ymir work/ui/game/windows/tab_button_middle_02.sub")
			button.SetDownVisual("d:/ymir work/ui/game/windows/tab_button_middle_03.sub")
			button.SetWindowHorizontalAlignCenter()
			button.SetWindowVerticalAlignBottom()
			button.SetPosition(pos, 85)
			button.SetText(text)
			button.SetEvent(lambda arg=i: self.SelectPage(arg))
			button.Show()
			self.pageButtonList.append(button)

			pos += 52
			text += "I"

		self.pageButtonList[0].Down()

	def SelectPage(self, index):

		self.curPageIndex = index

		for btn in self.pageButtonList:
			btn.SetUp()

		self.pageButtonList[index].Down()
		self.RefreshSafebox()

	def __LocalPosToGlobalPos(self, local):
		return self.curPageIndex*safebox.SAFEBOX_PAGE_SIZE + local

	def SetTableSize(self, size):

		pageCount = max(1, size / safebox.SAFEBOX_SLOT_Y_COUNT)
		pageCount = min(3, pageCount)
		size = safebox.SAFEBOX_SLOT_Y_COUNT

		self.__MakePageButton(pageCount)

		self.wndItem.ArrangeSlot(0, safebox.SAFEBOX_SLOT_X_COUNT, size, 32, 32, 0, 0)
		self.wndItem.RefreshSlot()
		self.wndItem.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)

		wnd_height = 130 + 32 * size
		self.wndBoard.SetSize(self.BOX_WIDTH, wnd_height)
		self.SetSize(self.BOX_WIDTH, wnd_height)
		self.UpdateRect()

	def RefreshSafebox(self):
		getItemID=safebox.GetItemID
		getItemCount=safebox.GetItemCount
		setItemID=self.wndItem.SetItemSlot

		for i in xrange(safebox.SAFEBOX_PAGE_SIZE):
			slotIndex = self.__LocalPosToGlobalPos(i)
			itemCount = getItemCount(slotIndex)
			if itemCount <= 1:
				itemCount = 0
			setItemID(i, getItemID(slotIndex), itemCount)
			
			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				changelookitemvnum = safebox.GetItemChangeLookVnum(slotIndex)
				if not changelookitemvnum == 0:
					self.wndItem.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
				else:
					self.wndItem.EnableSlotCoverImage(i,False)	
					
			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.__SetCollTimePetItemSlot( slotIndex, getItemID(slotIndex) )

		self.wndItem.RefreshSlot()

	def RefreshSafeboxMoney(self):
		pass
		#self.wndMoney.SetText(str(safebox.GetMoney()))
		
		
	if app.ENABLE_GROWTH_PET_SYSTEM:
		## 남은 시간에 따른 쿨타임 표시
		def __SetCollTimePetItemSlot(self, slotNumber, itemVnum):
			if 0 == itemVnum:
				return
				
			item.SelectItem(itemVnum)
			itemSubType = item.GetItemSubType()
				
			if itemSubType not in [item.PET_UPBRINGING, item.PET_BAG]:
				return
						
			if itemSubType == item.PET_BAG:
				id = safebox.GetItemMetinSocket(slotNumber, 2)
				if id == 0:
					return
					
			(limitType, limitValue) = item.GetLimit(0)
					
			#육성펫의 LimitValue 는 1번 소켓에 있다.
			if itemSubType == item.PET_UPBRINGING:
				limitValue = safebox.GetItemMetinSocket(slotNumber, 1)
							
			if limitType in [item.LIMIT_REAL_TIME, item.LIMIT_REAL_TIME_START_FIRST_USE]:
										
				sock_time   = safebox.GetItemMetinSocket(slotNumber, 0)
				remain_time = max( 0, sock_time - app.GetGlobalTimeStamp() )

				if slotNumber >= safebox.SAFEBOX_PAGE_SIZE:
					slotNumber -= (self.curPageIndex * safebox.SAFEBOX_PAGE_SIZE)
					
				## SetSlotCoolTimeInverse 의 slotNumber는 0 ~ 44
				self.wndItem.SetSlotCoolTimeInverse(slotNumber, limitValue, limitValue - remain_time)
		
	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def Close(self):
		m2netm2g.SendChatPacket("/safebox_close")

	def CommandCloseSafebox(self):
		if app.ENABLE_GROWTH_PET_SYSTEM:
			playerm2g2.SetOpenSafeBox(False)
	
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if app.WJ_ENABLE_TRADABLE_ICON:
			if self.interface:
				self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_NONE)
				self.interface.RefreshMarkInventoryBag()
		self.dlgPickMoney.Close()
		self.dlgChangePassword.Close()
		self.Hide()

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):

		selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			if playerm2g2.SLOT_TYPE_SAFEBOX == attachedSlotType:

				m2netm2g.SendSafeboxItemMovePacket(attachedSlotPos, selectedSlotPos, 0)
				#snd.PlaySound("sound/ui/drop.wav")
			else:
				attachedInvenType = playerm2g2.SlotTypeToInvenType(attachedSlotType)
				if playerm2g2.RESERVED_WINDOW == attachedInvenType:
					return
					
				if playerm2g2.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					m2netm2g.SendSafeboxSaveMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					m2netm2g.SendSafeboxCheckinPacket(attachedInvenType, attachedSlotPos, selectedSlotPos)
					#snd.PlaySound("sound/ui/drop.wav")
			
			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, selectedSlotPos):

		selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()

			if playerm2g2.SLOT_TYPE_INVENTORY == attachedSlotType:

				if playerm2g2.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
					m2netm2g.SendSafeboxSaveMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					#m2netm2g.SendSafeboxCheckinPacket(attachedSlotPos, selectedSlotPos)
					#snd.PlaySound("sound/ui/drop.wav")

			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SAFEBOX_SELL_DISABLE_SAFEITEM)

			elif app.BUY == curCursorNum:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			else:
				selectedItemID = safebox.GetItemID(selectedSlotPos)
				mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_SAFEBOX, selectedSlotPos, selectedItemID)
				snd.PlaySound("sound/ui/pick.wav")

	def UseItemSlot(self, slotIndex):
		if app.ENABLE_FISH_EVENT:
			if mouseModule.mouseController.isAttached():
				if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
					return
					
		if app.ENABLE_SAFEBOX_IMPROVING:
			mouseModule.mouseController.DeattachObject()
			slotIndex = self.__LocalPosToGlobalPos(slotIndex)
			m2netm2g.SendSafeboxCheckoutPacket(slotIndex, playerm2g2.INVENTORY, 0)
		else:
			mouseModule.mouseController.DeattachObject()

	def __ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetSafeBoxItem(slotIndex)

	def OverInItem(self, slotIndex):
		slotIndex = self.__LocalPosToGlobalPos(slotIndex)
		self.wndItem.SetUsableItem(False)
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPickMoney(self, money):
		mouseModule.mouseController.AttachMoney(self, playerm2g2.SLOT_TYPE_SAFEBOX, money)

	def OnChangePassword(self):
		self.dlgChangePassword.Open()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):

		USE_SAFEBOX_LIMIT_RANGE = 1000

		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		if app.ENABLE_EXTEND_MALLBOX:
			if self.timeSendClosePacket < app.GetTime() and (abs(x - self.xSafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE or abs(y - self.ySafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE):
				self.timeSendClosePacket = app.GetTime() + 10
				self.Close()
		else:
			if abs(x - self.xSafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE or abs(y - self.ySafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE:
				self.Close()
	
	if app.WJ_ENABLE_TRADABLE_ICON:
		def CantCheckInItem(self, slotIndex):
			itemIndex = playerm2g2.GetItemIndex(slotIndex)
		
			if itemIndex:
				return playerm2g2.IsAntiFlagBySlot(slotIndex, item.ANTIFLAG_SAFEBOX)
			
			return False
			
		def BindInterface(self, interface):
			from _weakref import proxy
			self.interface = proxy(interface)
			
		def OnTop(self):
			if not self.interface:
				return
			
			self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_SAFEBOX)
			self.interface.RefreshMarkInventoryBag()

class MallWindow(ui.ScriptWindow):

	BOX_WIDTH = 176

	if app.ENABLE_EXTEND_MALLBOX:
		PAGE_TEXT = ( "I", "II", "III", "IV", "V")

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.pageButtonList = []
		self.curPageIndex = 0
		self.isLoaded = 0
		self.xSafeBoxStart = 0
		self.ySafeBoxStart = 0
		if app.ENABLE_EXTEND_MALLBOX:
			self.timeSendClosePacket = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)		

	def Destroy(self):
		self.ClearDictionary()

		self.tooltipItem = None
		self.wndBoard = None
		self.wndItem = None

		self.pageButtonList = []

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "UIScript/MallWindow.py")

		from _weakref import proxy

		## Item
		wndItem = ui.GridSlotWindow()
		wndItem.SetParent(self)
		wndItem.SetPosition(8, 35)
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.Show()

		## Close Button
		self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
		self.GetChild("ExitButton").SetEvent(ui.__mem_func__(self.Close))

		self.wndItem = wndItem
		self.wndBoard = self.GetChild("board")

		## Initialize
		self.SetTableSize(3)

	def ShowWindow(self, size):

		(self.xSafeBoxStart, self.ySafeBoxStart, z) = playerm2g2.GetMainCharacterPosition()

		self.SetTableSize(size)
		self.Show()
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			playerm2g2.SetOpenMall(True)

	def SetTableSize(self, size):

		pageCount = max(1, size / safebox.SAFEBOX_SLOT_Y_COUNT)
		if app.ENABLE_EXTEND_MALLBOX:
			pageCount = min(5, pageCount)
		else:
			pageCount = min(3, pageCount)
		size = safebox.SAFEBOX_SLOT_Y_COUNT
		
		if app.ENABLE_EXTEND_MALLBOX:
			self.__MakePageButton(pageCount)

		self.wndItem.ArrangeSlot(0, safebox.SAFEBOX_SLOT_X_COUNT, size, 32, 32, 0, 0)
		self.wndItem.RefreshSlot()
		self.wndItem.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		if app.ENABLE_EXTEND_MALLBOX:
			self.wndBoard.SetSize(self.BOX_WIDTH, 102 + 32*size)
			self.SetSize(self.BOX_WIDTH, 105 + 32*size)
		else:
			self.wndBoard.SetSize(self.BOX_WIDTH, 82 + 32*size)
			self.SetSize(self.BOX_WIDTH, 85 + 32*size)
		self.UpdateRect()

	if app.ENABLE_EXTEND_MALLBOX:
		def __MakePageButton(self, pageCount):
			
			self.curPageIndex = 0
			self.pageButtonList = []
			
			pos = -int(float(pageCount-1)/2 * 32)
			for i in xrange(pageCount):
				text = self.PAGE_TEXT[i]
				button = ui.RadioButton()
				button.SetParent(self)
				button.SetUpVisual("d:/ymir work/ui/game/windows/tab_button_small_01.sub")
				button.SetOverVisual("d:/ymir work/ui/game/windows/tab_button_small_02.sub")
				button.SetDownVisual("d:/ymir work/ui/game/windows/tab_button_small_03.sub")
				button.SetWindowHorizontalAlignCenter()
				button.SetWindowVerticalAlignBottom()
				button.SetPosition(pos, 65)
				button.SetText(text)
				button.SetEvent(lambda arg=i: self.SelectPage(arg))
				button.Show()
				self.pageButtonList.append(button)
				
				pos += 32
			
			self.pageButtonList[0].Down()
			
		def SelectPage(self, index):
		
			self.curPageIndex = index
		
			for btn in self.pageButtonList:
				btn.SetUp()
		
			self.pageButtonList[index].Down()
			self.RefreshMall()
			
			
		def __LocalPosToGlobalPos(self, local):
			return self.curPageIndex*safebox.SAFEBOX_PAGE_SIZE + local
			
	def RefreshMall(self):
		getItemID=safebox.GetMallItemID
		getItemCount=safebox.GetMallItemCount
		setItemID=self.wndItem.SetItemSlot

		if app.ENABLE_EXTEND_MALLBOX:
			for i in xrange(safebox.SAFEBOX_PAGE_SIZE):
				slotIndex = self.__LocalPosToGlobalPos(i)
				itemCount = getItemCount(slotIndex)
				if itemCount <= 1:
					itemCount = 0
				setItemID(i, getItemID(slotIndex), itemCount)
			
				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					changelookitemvnum = safebox.GetMallItemChangeLookVnum(slotIndex)
					if not changelookitemvnum == 0:
						self.wndItem.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
					else:
						self.wndItem.EnableSlotCoverImage(i,False)
		else:
			for i in xrange(safebox.GetMallSize()):
				itemID = getItemID(i)
				itemCount = getItemCount(i)
				if itemCount <= 1:
					itemCount = 0
				setItemID(i, itemID, itemCount)
			
				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					changelookitemvnum = safebox.GetMallItemChangeLookVnum(i)
					if not changelookitemvnum == 0:
						self.wndItem.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
					else:
						self.wndItem.EnableSlotCoverImage(i,False)

		self.wndItem.RefreshSlot()

	def SetItemToolTip(self, tooltip):
		self.tooltipItem = tooltip

	def Close(self):
		m2netm2g.SendChatPacket("/mall_close")

	def CommandCloseMall(self):
		if app.ENABLE_GROWTH_PET_SYSTEM:
			playerm2g2.SetOpenMall(False)
	
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.Hide()

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):

		if mouseModule.mouseController.isAttached():

			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MALL_CANNOT_INSERT)
			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, selectedSlotPos):
		if app.ENABLE_EXTEND_MALLBOX:
			selectedSlotPos = self.__LocalPosToGlobalPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.MALL_CANNOT_INSERT)
			mouseModule.mouseController.DeattachObject()

		else:

			curCursorNum = app.GetCursor()
			selectedItemID = safebox.GetMallItemID(selectedSlotPos)
			mouseModule.mouseController.AttachObject(self, playerm2g2.SLOT_TYPE_MALL, selectedSlotPos, selectedItemID)
			snd.PlaySound("sound/ui/pick.wav")

	def UseItemSlot(self, slotIndex):
		
		if app.ENABLE_FISH_EVENT:
			if mouseModule.mouseController.isAttached():
				if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
					return
					
		if app.ENABLE_SAFEBOX_IMPROVING:
			mouseModule.mouseController.DeattachObject()
			if app.ENABLE_EXTEND_MALLBOX:
				slotIndex = self.__LocalPosToGlobalPos(slotIndex)
			m2netm2g.SendMallCheckoutPacket(slotIndex, playerm2g2.INVENTORY, 0)
		else:
			mouseModule.mouseController.DeattachObject()

	def __ShowToolTip(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.SetMallItem(slotIndex)

	def OverInItem(self, slotIndex):
		if app.ENABLE_EXTEND_MALLBOX:
			slotIndex = self.__LocalPosToGlobalPos(slotIndex)
		self.__ShowToolTip(slotIndex)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnUpdate(self):

		USE_SAFEBOX_LIMIT_RANGE = 1000

		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		if app.ENABLE_EXTEND_MALLBOX:
			if self.timeSendClosePacket < app.GetTime() and (abs(x - self.xSafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE or abs(y - self.ySafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE):
				self.timeSendClosePacket = app.GetTime() + 10
				self.Close()
		else:
			if abs(x - self.xSafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE or abs(y - self.ySafeBoxStart) > USE_SAFEBOX_LIMIT_RANGE:
				self.Close()


if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import chr
	import background
	import playerm2g2

	#wndMgr.SetOutlineFlag(True)

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create("METIN2 CLOSED BETA", systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()


	wnd = SafeboxWindow()
	wnd.ShowWindow(1)
	
	app.Loop()
