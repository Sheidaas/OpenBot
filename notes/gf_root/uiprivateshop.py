import m2netm2g
import playerm2g2
import item
import snd
import shop

import ui
import uiCommon
import mouseModule
import localeInfo
import constInfo

import app

if app.ENABLE_MYSHOP_DECO:
	## 개인 상점 ##
	class PrivateShopDialog(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__ClearVariable()
			self.__LoadDialog()
			
		def __del__(self):
			ui.ScriptWindow.__del__(self)
			
		def __LoadDialog(self):
			try:
				PythonScriptLoader = ui.PythonScriptLoader()
				PythonScriptLoader.LoadScriptFile(self, "UIScript/PrivateShopDialog.py")
			except:
				import exception
				exception.Abort("PrivateShopDialog.LoadDialog.LoadObject")
			
			try:
				GetObject = self.GetChild
				self.ItemSlotWnd1 = GetObject("ItemSlot1")
				self.ItemSlotWnd2 = GetObject("ItemSlot2")
				self.CloseBtn = GetObject("CloseButton")
				self.MainBoard = GetObject("board")
				self.TitleBar = GetObject("TitleBar")
				self.TitleName = GetObject("TitleName")
				self.Tab2Btn = GetObject("tab2")
			except:
				import exception
				exception.Abort("PrivateShopDialog.LoadDialog.BindObject")
				
			self.ItemSlotWnd1.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.ItemSlotWnd1.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.ItemSlotWnd2.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.ItemSlotWnd2.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			
			self.ItemSlotWnd1.SAFE_SetButtonEvent("LEFT", "EMPTY", self.SelectEmptySlot)
			self.ItemSlotWnd1.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
			self.ItemSlotWnd1.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
			
			self.ItemSlotWnd2.SAFE_SetButtonEvent("LEFT", "EMPTY", self.SelectEmptySlot)
			self.ItemSlotWnd2.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
			self.ItemSlotWnd2.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)
			
			self.CloseBtn.SetEvent(ui.__mem_func__(self.AskClosePrivateShop))
			self.TitleBar.SetCloseEvent(ui.__mem_func__(self.Close))
			
			self.USE_SHOP_LIMIT_RANGE = 1000
			
		def Open(self, vid):
		
			tabCnt = shop.GetTabCount()
			
			if localeInfo.IsARABIC():
				if tabCnt == 2 :
					self.SetSize(345, 354)
					self.MainBoard.SetPosition(345, 0)
					self.MainBoard.SetSize(345, 354)
					self.TitleBar.SetPosition(345 - 8, 8)
					self.TitleBar.SetWidth(345-18)
					self.TitleName.SetPosition(345/2, 4)
					self.CloseBtn.SetPosition(345/2 - 43 + 87, 354-33)
					self.Tab2Btn.Show()
					self.ItemSlotWnd2.Show()
				elif tabCnt == 1:
					self.SetSize(184, 354)
					self.MainBoard.SetPosition(184, 0)
					self.MainBoard.SetSize(184, 354)
					self.TitleBar.SetPosition(184 - 8, 8)
					self.TitleBar.SetWidth(184-18)
					self.TitleName.SetPosition(184/2, 4)
					self.CloseBtn.SetPosition(184/2 - 43 + 87, 354-33)
					self.Tab2Btn.Hide()
					self.ItemSlotWnd2.Hide()
				else:
					return
			else:
				if tabCnt == 2 :
					self.SetSize(345, 354)
					self.MainBoard.SetSize(345, 354)
					self.TitleBar.SetWidth(345-18)
					self.TitleName.SetPosition(345/2, 4)
					self.CloseBtn.SetPosition(345/2 - 43, 354-33)
					self.Tab2Btn.Show()
					self.ItemSlotWnd2.Show()
				elif tabCnt == 1:
					self.SetSize(184, 354)
					self.MainBoard.SetSize(184, 354)
					self.TitleBar.SetWidth(184-18)
					self.TitleName.SetPosition(184/2, 4)
					self.CloseBtn.SetPosition(184/2 - 43, 354-33)
					self.Tab2Btn.Hide()
					self.ItemSlotWnd2.Hide()
				else:
					return
				
			self.UpdateRect()
		
			isMyShop = False
			
			if playerm2g2.IsMainCharacterIndex(vid) :
				isMyShop = True
				self.CloseBtn.Show()
			else:
				isMyShop = False
				self.CloseBtn.Hide()
				
			shop.Open(True, isMyShop)
			
			self.Refresh()
			self.SetTop()

			self.Show()
			
			(self.ShopPosX, self.ShopPosY, z) = playerm2g2.GetMainCharacterPosition()
			
		def Refresh(self):
			getItemID=shop.GetItemID
			getItemCount=shop.GetItemCount
			for i in xrange(shop.SHOP_SLOT_COUNT):
				itemCount = getItemCount(i)
				if itemCount <= 1:
					itemCount = 0
				self.ItemSlotWnd1.SetItemSlot(i, getItemID(i), itemCount)
				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					changelookvnum = shop.GetItemChangeLookVnum(i)
					if not changelookvnum == 0:
						self.ItemSlotWnd1.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
					else:
						self.ItemSlotWnd1.EnableSlotCoverImage(i,False)
			
			self.ItemSlotWnd1.RefreshSlot()
			
			if not self.ItemSlotWnd2.IsShow():
				return
				
			for i in xrange(shop.SHOP_SLOT_COUNT):
				idx = i + shop.SHOP_SLOT_COUNT
				itemCount = getItemCount(idx)
				if itemCount <= 1:
					itemCount = 0
				self.ItemSlotWnd2.SetItemSlot(idx, getItemID(idx), itemCount)
				if app.ENABLE_CHANGE_LOOK_SYSTEM:
					changelookvnum = shop.GetItemChangeLookVnum(idx)
					if not changelookvnum == 0:
						self.ItemSlotWnd2.SetSlotCoverImage(i,"icon/item/ingame_convert_Mark.tga")
					else:
						self.ItemSlotWnd2.EnableSlotCoverImage(i,False)
			
			self.ItemSlotWnd2.RefreshSlot()
			
		def Close(self):
			shop.Close()
			m2netm2g.SendShopEndPacket()
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
			self.Hide()
			
		def __ClearVariable(self):
			self.ItemSlotWnd1 = None
			self.ItemSlotWnd2 = None
			self.CloseBtn = None
			self.MainBoard = None
			self.TitleBar = None
			self.TitleName = None
			self.tooltipItem = None
			self.questionDialog = None
			
		def Destroy(self):
			self.__ClearVariable()
			self.Close()
			self.ClearDictionary()
				
		def OnPressEscapeKey(self):
			self.Close()
			
		def SetItemToolTip(self, tooltipItem):
			self.tooltipItem = tooltipItem
		
		def OverInItem(self, slotIdx):
			if mouseModule.mouseController.isAttached():
				return
				
			if self.tooltipItem:
				self.tooltipItem.SetShopItem(slotIdx)
			
		def OverOutItem(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
			
		def AskClosePrivateShop(self):
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(localeInfo.PRIVATE_SHOP_CLOSE_QUESTION)
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnClosePrivateShop))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			questionDialog.Open()
			self.questionDialog = questionDialog

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		
		def OnClosePrivateShop(self):
			m2netm2g.SendChatPacket("/close_shop")
			self.OnCloseQuestionDialog()
			
		def OnCloseQuestionDialog(self):
			if not self.questionDialog:
				return
				
			self.questionDialog.Close()
			self.questionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		
		def OnUpdate(self):
			(x, y, z) = playerm2g2.GetMainCharacterPosition()
			if abs(x - self.ShopPosX) > self.USE_SHOP_LIMIT_RANGE or abs(y - self.ShopPosY) > self.USE_SHOP_LIMIT_RANGE:
				self.Close()
				
		def SelectEmptySlot(self, selectedSlotPos):
			if mouseModule.mouseController.isAttached():
				mouseModule.mouseController.DeattachObject()
				
		def UnselectItemSlot(self, selectedSlotPos):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return
			
			self.AskBuyItem(selectedSlotPos)
			
		def SelectItemSlot(self, selectedSlotPos):
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return
			
			if True == shop.IsMainPlayerPrivateShop():
				return
			
			selectedItemID = shop.GetItemID(selectedSlotPos)
			itemCount = shop.GetItemCount(selectedSlotPos)
			type = playerm2g2.SLOT_TYPE_PRIVATE_SHOP
			mouseModule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
			mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))
			snd.PlaySound("sound/ui/pick.wav")
			
		def DropToInventory(self):
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			self.AskBuyItem(attachedSlotPos)
			
		def AskBuyItem(self, slotPos):	
			itemIndex = shop.GetItemID(slotPos)
			itemPrice = shop.GetItemPrice(slotPos)
			itemCount = shop.GetItemCount(slotPos)
			
			item.SelectItem(itemIndex)
			itemName = item.GetItemName()
			
			itemBuyQuestionDialog = uiCommon.QuestionDialog()
			
			itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, localeInfo.NumberToMoneyString(itemPrice), shop.GetItemCheque(slotPos)))
			
			itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
			itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
			itemBuyQuestionDialog.Open()
			itemBuyQuestionDialog.pos = slotPos
			self.itemBuyQuestionDialog = itemBuyQuestionDialog
			
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)
		
		def AnswerBuyItem(self, flag):
			if flag:
				pos = self.itemBuyQuestionDialog.pos
				m2netm2g.SendShopBuyPacket(pos)
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)