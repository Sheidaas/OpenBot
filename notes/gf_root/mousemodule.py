import app
import grp
import grpImage
import item
import wndMgr
import playerm2g2

import skill
import dbg
import grpText

import ui

import systemSetting

import localeInfo

## Mouse Controler
## 마우스 커서를 제어하며 마우스 커서에 Attach되어 움직이는 Object들까지 제어할 수 있다.

class CursorImage(object):
	def __init__(self):
		self.handle = 0

	def __init__(self, imageName):
		self.handle = 0
		self.LoadImage(imageName)

	def __del__(self):
		grpImage.Delete(self.handle)

	def LoadImage(self, imageName):
		try:
			self.handle = grpImage.Generate(imageName)

		except:
			import sys
			dbg.TraceError("%s %s" % (sys.exc_info()[0], sys.exc_info()[1]))
			self.handle = 0

	def DeleteImage(self):
		if self.handle:
			grpImage.Delete(self.handle)

	def IsImage(self):
		if self.handle:
			return True

		return False

	def SetPosition(self, x, y):
		if self.handle:
			grpImage.SetPosition(self.handle, x, y)

	def Render(self):
		if self.handle:
			grpImage.Render(self.handle)

class CMouseController(object):

	def __init__(self):
		if app.ENABLE_CHEQUE_SYSTEM:
			self.chequeValue = 0
			self.chequeNumberLine = None
		
		self.x = 0
		self.y = 0

		self.IsSoftwareCursor = False
		self.curCursorName = ""
		self.curCursorImage = 0
		self.cursorPosX = 0
		self.cursorPosY = 0

		self.AttachedIconHandle = 0
		self.AttachedOwner = 0
		self.AttachedFlag = False
		self.AttachedType = 0
		self.AttachedSlotNumber = 0
		self.AttachedCount = 1
		self.AttachedIconHalfWidth = 0
		self.AttachedIconHalfHeight = 0
		self.LastAttachedSlotNumber = 0

		self.countNumberLine = None

		self.DeattachObject()

		self.callbackDict = {}

		if app.ENABLE_FISH_EVENT:
			self.IsAttachedIconRender = True
		
	def __del__(self):
		self.callbackDict = {}
		
	def Destroy(self):
		del self.countNumberLine	
		self.countNumberLine = None
		if app.ENABLE_CHEQUE_SYSTEM:
			del self.chequeNumberLine
			self.chequeNumberLine = None
			
	def CreateNumberLine(self):
		self.countNumberLine = ui.NumberLine("GAME")
		self.countNumberLine.SetHorizontalAlignCenter()
		self.countNumberLine.Hide()
		
		if app.ENABLE_CHEQUE_SYSTEM :
			self.chequeNumberLine = ui.NumberLine("GAME")
			self.chequeNumberLine.SetHorizontalAlignCenter()
			self.chequeNumberLine.Hide()		

	def Create(self):
		self.IsSoftwareCursor = systemSetting.IsSoftwareCursor()

		self.cursorDict = {
			app.NORMAL			: CursorImage("D:/Ymir Work/UI/Cursor/cursor.sub"),
			app.ATTACK			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_attack.sub"),
			app.TARGET			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_attack.sub"),
			app.TALK			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_talk.sub"),
			app.CANT_GO			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_no.sub"),
			app.PICK			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_pick.sub"),
			app.DOOR			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_door.sub"),
			app.CHAIR			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_chair.sub"),
			app.MAGIC			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_chair.sub"),
			app.BUY				: CursorImage("D:/Ymir Work/UI/Cursor/cursor_buy.sub"),
			app.SELL			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_sell.sub"),
			app.CAMERA_ROTATE	: CursorImage("D:/Ymir Work/UI/Cursor/cursor_camera_rotate.sub"),
			app.HSIZE			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_hsize.sub"),
			app.VSIZE			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_vsize.sub"),
			app.HVSIZE			: CursorImage("D:/Ymir Work/UI/Cursor/cursor_hvsize.sub"),
		}
		self.cursorPosDict = {
			app.NORMAL			: (0, 0),
			app.TARGET			: (0, 0),
			app.ATTACK			: (0, 0),
			app.TALK			: (0, 0),
			app.CANT_GO			: (0, 0),
			app.PICK			: (0, 0),
			app.DOOR			: (0, 0),
			app.CHAIR			: (0, 0),
			app.MAGIC			: (0, 0),
			app.BUY				: (0, 0),
			app.SELL			: (0, 0),
			app.CAMERA_ROTATE	: (0, 0),
			app.HSIZE			: (-16, -16),
			app.VSIZE			: (-16, -16),
			app.HVSIZE			: (-16, -16),
		}

		app.SetCursor(app.NORMAL)

		"""
		AttachedCountTextLineHandle = grpText.Generate()
		grpText.SetFontName(AttachedCountTextLineHandle, localeInfo.UI_DEF_FONT_SMALL)
		grpText.SetText(AttachedCountTextLineHandle, "1234")
		grpText.SetPosition(AttachedCountTextLineHandle, 100, 100)
		grpText.SetOutline(AttachedCountTextLineHandle, True)
		grpText.SetFontColor(AttachedCountTextLineHandle, 1.0, 1.0, 1.0)
		grpText.SetHorizontalAlign(AttachedCountTextLineHandle, wndMgr.TEXT_HORIZONTAL_ALIGN_CENTER)
		self.AttachedCountTextLineHandle = AttachedCountTextLineHandle
		"""

		#self.countNumberLine = ui.NumberLine("CURTAIN")
		#self.countNumberLine.SetHorizontalAlignCenter()
		#self.countNumberLine.Hide()
		
		#if app.ENABLE_CHEQUE_SYSTEM :
		#	self.chequeNumberLine = ui.NumberLine("CURTAIN")
		#	self.chequeNumberLine.SetHorizontalAlignCenter()
		#	self.chequeNumberLine.Hide()

		return True

	# Cursor Control
	def ChangeCursor(self, cursorNum):
		try:
			self.curCursorNum = cursorNum
			self.curCursorImage = self.cursorDict[cursorNum]
			(self.cursorPosX, self.cursorPosY) = self.cursorPosDict[cursorNum]

			if False == self.curCursorImage.IsImage():
				self.curCursorNum = app.NORMAL
				self.curCursorImage = self.cursorDict[app.NORMAL]

		except KeyError:
			dbg.TraceError("mouseModule.MouseController.SetCursor - 잘못된 커서 번호 [%d]" % cursorNum)
			self.curCursorName = app.NORMAL
			self.curCursorImage = self.cursorDict[app.NORMAL]

	# Attaching
	def AttachObject(self, Owner, Type, SlotNumber, ItemIndex, count = 0):

		self.LastAttachedSlotNumber = self.AttachedSlotNumber

		self.AttachedFlag = True
		self.AttachedOwner = Owner
		self.AttachedType = Type
		self.AttachedSlotNumber = SlotNumber
		self.AttachedItemIndex = ItemIndex
		self.AttachedCount = count
		self.countNumberLine.SetNumber("")
		self.countNumberLine.Hide()

		if count > 1:
			self.countNumberLine.SetNumber(str(count))
			self.countNumberLine.Show()

		try:

			width = 1
			height = 1

			if Type == playerm2g2.SLOT_TYPE_INVENTORY or\
				Type == playerm2g2.SLOT_TYPE_PRIVATE_SHOP or\
				Type == playerm2g2.SLOT_TYPE_SHOP or\
				Type == playerm2g2.SLOT_TYPE_SAFEBOX or\
				Type == playerm2g2.SLOT_TYPE_ACCE or\
				Type == playerm2g2.SLOT_TYPE_MALL or\
				Type == playerm2g2.SLOT_TYPE_DRAGON_SOUL_INVENTORY:

				item.SelectItem(self.AttachedItemIndex)
				self.AttachedIconHandle = item.GetIconInstance()

				if not self.AttachedIconHandle:
					self.AttachedIconHandle = 0
					self.DeattachObject()
					return

				(width, height) = item.GetItemSize()

			elif Type == playerm2g2.SLOT_TYPE_SKILL:
				skillGrade = playerm2g2.GetSkillGrade(SlotNumber)
				self.AttachedIconHandle = skill.GetIconInstanceNew(self.AttachedItemIndex, skillGrade)

			elif Type == playerm2g2.SLOT_TYPE_EMOTION:
				image = playerm2g2.GetEmotionIconImage(ItemIndex)
				self.AttachedIconHandle = grpImage.GenerateFromHandle(image)

			elif Type == playerm2g2.SLOT_TYPE_QUICK_SLOT:
				(quickSlotType, position) = playerm2g2.GetGlobalQuickSlot(SlotNumber)

				if app.ENABLE_EXTEND_INVEN_SYSTEM and ( quickSlotType == playerm2g2.SLOT_TYPE_INVENTORY or quickSlotType == playerm2g2.SLOT_TYPE_BELT_INVENTORY):
						
					window = playerm2g2.SlotTypeToInvenType(quickSlotType)
					itemIndex = playerm2g2.GetItemIndex(window, position)
					item.SelectItem(itemIndex)
					self.AttachedIconHandle = item.GetIconInstance()
					(width, height) = item.GetItemSize()
						
				if not app.ENABLE_EXTEND_INVEN_SYSTEM and quickSlotType == playerm2g2.SLOT_TYPE_INVENTORY:

					itemIndex = playerm2g2.GetItemIndex(position)
					item.SelectItem(itemIndex)
					self.AttachedIconHandle = item.GetIconInstance()
					(width, height) = item.GetItemSize()

				elif quickSlotType == playerm2g2.SLOT_TYPE_SKILL:
					skillIndex = playerm2g2.GetSkillIndex(position)
					skillGrade = playerm2g2.GetSkillGrade(position)
					self.AttachedIconHandle = skill.GetIconInstanceNew(skillIndex, skillGrade)

				elif quickSlotType == playerm2g2.SLOT_TYPE_EMOTION:
					image = playerm2g2.GetEmotionIconImage(position)
					self.AttachedIconHandle = grpImage.GenerateFromHandle(image)
			
			elif app.ENABLE_EXTEND_INVEN_SYSTEM:
				if Type == playerm2g2.SLOT_TYPE_EQUIPMENT or\
					Type == playerm2g2.SLOT_TYPE_BELT_INVENTORY:
						
					item.SelectItem(self.AttachedItemIndex)
					self.AttachedIconHandle = item.GetIconInstance()

					if not self.AttachedIconHandle:
						self.AttachedIconHandle = 0
						self.DeattachObject()
						return

					(width, height) = item.GetItemSize()
							
			if app.ENABLE_GUILDRENEWAL_SYSTEM:
				if Type == playerm2g2.SLOT_TYPE_GUILDBANK:
					item.SelectItem(self.AttachedItemIndex)
					self.AttachedIconHandle = item.GetIconInstance()

					if not self.AttachedIconHandle:
						self.AttachedIconHandle = 0
						self.DeattachObject()
						return

					(width, height) = item.GetItemSize()
					
			if app.ENABLE_AUTO_SYSTEM:
				if Type == playerm2g2.SLOT_TYPE_AUTO:
					if SlotNumber <= playerm2g2.AUTO_SKILL_SLOT_MAX:
						skillIndex = playerm2g2.GetSkillIndex(ItemIndex)
						skillGrade = playerm2g2.GetSkillGrade(ItemIndex)
						self.AttachedIconHandle = skill.GetIconInstanceNew(skillIndex, skillGrade)
					else:
						if app.ENABLE_EXTEND_INVEN_SYSTEM:
							itemIndex = playerm2g2.GetItemIndex(playerm2g2.SLOT_TYPE_INVENTORY, ItemIndex)
						else:
							itemIndex = playerm2g2.GetItemIndex(ItemIndex)
						item.SelectItem(itemIndex)
						self.AttachedIconHandle = item.GetIconInstance()
						(width, height) = item.GetItemSize()
						
			if app.ENABLE_CHANGE_LOOK_SYSTEM:
					if Type == playerm2g2.SLOT_TYPE_CHANGE_LOOK:
						item.SelectItem(self.AttachedItemIndex)
						self.AttachedIconHandle = item.GetIconInstance()

						if not self.AttachedIconHandle:
							self.AttachedIconHandle = 0
							self.DeattachObject()
							return

						(width, height) = item.GetItemSize()

			if not self.AttachedIconHandle:
				self.DeattachObject()
				return

			self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2
			self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2
			self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2
			self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2
			wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, width, height)

		except Exception, e:
			dbg.TraceError("mouseModule.py: AttachObject : " + str(e))
			self.AttachedIconHandle = 0

	def IsAttachedMoney(self):
		if True == self.isAttached():
			if playerm2g2.ITEM_MONEY == self.GetAttachedItemIndex():
				return True

		return False
				
	def GetAttachedMoneyAmount(self):
		if True == self.isAttached():
			if playerm2g2.ITEM_MONEY == self.GetAttachedItemIndex():
				return self.GetAttachedItemCount()
		return 0

	if app.ENABLE_CHEQUE_SYSTEM:
		def AttachMoney(self, owner, type, count, cheque = 0):

			self.LastAttachedSlotNumber = self.AttachedSlotNumber

			self.AttachedFlag = True
			self.AttachedOwner = owner
			self.AttachedType = type
			self.AttachedSlotNumber = -1
			self.AttachedItemIndex = playerm2g2.ITEM_MONEY
			self.AttachedCount = count
			self.AttachedIconHandle = grpImage.Generate("icon/item/money.tga")
			self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2
			self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2
			wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, 1, 1)

			if count > 1:
				self.countNumberLine.SetNumber(str(count))
				self.countNumberLine.Show()
			
			if cheque > 0:
				self.chequeNumberLine.SetNumber(str(cheque), 1.0, 1.0, 0.0)
				self.chequeNumberLine.Show()
				self.SetCheque(cheque)
					
	else:
		def AttachMoney(self, owner, type, count):

			self.LastAttachedSlotNumber = self.AttachedSlotNumber

			self.AttachedFlag = True
			self.AttachedOwner = owner
			self.AttachedType = type
			self.AttachedSlotNumber = -1
			self.AttachedItemIndex = playerm2g2.ITEM_MONEY
			self.AttachedCount = count
			self.AttachedIconHandle = grpImage.Generate("icon/item/money.tga")
			self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2
			self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2
			wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, 1, 1)

			if count > 1:
				self.countNumberLine.SetNumber(str(count))
				self.countNumberLine.Show()
			#grpText.SetText(self.AttachedCountTextLineHandle, str(count))
		
	if app.ENABLE_CHEQUE_SYSTEM:
		def SetCheque(self, cheque) :
			self.chequeValue = cheque
		
		def GetCheque(self) :
			return self.chequeValue

	def DeattachObject(self):

		self.ClearCallBack()
		self.LastAttachedSlotNumber = self.AttachedSlotNumber

		if self.AttachedIconHandle != 0:

			if self.AttachedType == playerm2g2.SLOT_TYPE_INVENTORY or\
				self.AttachedType == playerm2g2.SLOT_TYPE_PRIVATE_SHOP or\
				self.AttachedType == playerm2g2.SLOT_TYPE_SHOP or\
				self.AttachedType == playerm2g2.SLOT_TYPE_SAFEBOX or\
				self.AttachedType == playerm2g2.SLOT_TYPE_MALL:

				item.DeleteIconInstance(self.AttachedIconHandle)

			elif self.AttachedType == playerm2g2.SLOT_TYPE_SKILL:
				skill.DeleteIconInstance(self.AttachedIconHandle)

			elif self.AttachedType == playerm2g2.SLOT_TYPE_EMOTION:
				grpImage.Delete(self.AttachedIconHandle)
				
			if app.ENABLE_GUILDRENEWAL_SYSTEM:
				if self.AttachedType == playerm2g2.SLOT_TYPE_GUILDBANK:
					item.DeleteIconInstance(self.AttachedIconHandle)
					
			if app.ENABLE_FISH_EVENT:
				if self.AttachedType == playerm2g2.SLOT_TYPE_FISH_EVENT:
					self.AttachedOwner.DropQuestionDialog()
					return
		
		if app.ENABLE_FISH_EVENT:
			self.DeattachObjectPostProcess()
		else:
			self.AttachedFlag = False
			self.AttachedType = -1
			self.AttachedItemIndex = -1
			self.AttachedSlotNumber = -1
			self.AttachedIconHandle = 0
			wndMgr.SetAttachingFlag(False)

			if self.countNumberLine:
				self.countNumberLine.Hide()
			
			if app.ENABLE_CHEQUE_SYSTEM:
				self.chequeValue = 0
				if self.chequeNumberLine:
					self.chequeNumberLine.Hide()
			
		if app.ENABLE_CHEQUE_SYSTEM:
			self.chequeValue = 0
			if self.chequeNumberLine:
				self.chequeNumberLine.Hide()

	def isAttached(self):
		return self.AttachedFlag

	def GetAttachedOwner(self):

		if False == self.isAttached():
			return 0

		return self.AttachedOwner

	def GetAttachedType(self):

		if False == self.isAttached():
			return playerm2g2.SLOT_TYPE_NONE

		return self.AttachedType

	def GetAttachedSlotNumber(self):

		if False == self.isAttached():
			return 0

		return self.AttachedSlotNumber

	def GetLastAttachedSlotNumber(self):

		return self.LastAttachedSlotNumber

	def GetAttachedItemIndex(self):

		if False == self.isAttached():
			return 0

		return self.AttachedItemIndex

	def GetAttachedItemCount(self):

		if False == self.isAttached():
			return 0

		return self.AttachedCount

	# Update
	def Update(self, x, y):

		self.x = x
		self.y = y

		if True == self.isAttached():
			if 0 != self.AttachedIconHandle:

				if app.ENABLE_FISH_EVENT:
					if playerm2g2.SLOT_TYPE_FISH_EVENT == self.GetAttachedType():
						grpImage.SetDiffuseColor(self.AttachedIconHandle, 1.0, 1.0, 1.0, 1.0)
					else:
						grpImage.SetDiffuseColor(self.AttachedIconHandle, 1.0, 1.0, 1.0, 0.5)
					grpImage.SetPosition(self.AttachedIconHandle, self.x - self.AttachedIconHalfWidth, self.y - self.AttachedIconHalfHeight)
					self.countNumberLine.SetPosition(self.x, self.y - self.AttachedIconHalfHeight - 3)
				else:
					grpImage.SetDiffuseColor(self.AttachedIconHandle, 1.0, 1.0, 1.0, 0.5)
					grpImage.SetPosition(self.AttachedIconHandle, self.x - self.AttachedIconHalfWidth, self.y - self.AttachedIconHalfHeight)
					self.countNumberLine.SetPosition(self.x, self.y - self.AttachedIconHalfHeight - 3)
				
			if app.ENABLE_CHEQUE_SYSTEM:
				if self.chequeNumberLine.IsShow():
					self.chequeNumberLine.SetPosition(self.x, self.y - self.AttachedIconHalfHeight - 13)

		if self.IsSoftwareCursor:
			if 0 != self.curCursorImage:
				self.curCursorImage.SetPosition(self.x + self.cursorPosX, self.y + self.cursorPosY)
				
	# Render
	def Render(self):

		if True == self.isAttached():
			if 0 != self.AttachedIconHandle:
				if app.ENABLE_FISH_EVENT:
					if True == self.IsAttachedIconRender:
						grpImage.Render(self.AttachedIconHandle)
				else:
					grpImage.Render(self.AttachedIconHandle)

		if self.IsSoftwareCursor:
			if True == app.IsShowCursor():
				if 0 != self.curCursorImage:
					self.curCursorImage.Render()
		else:
			if False == app.IsShowCursor():
				if True == app.IsLiarCursorOn():
					if 0 != self.curCursorImage:
						self.curCursorImage.SetPosition(self.x + self.cursorPosX, self.y + self.cursorPosY)
						self.curCursorImage.Render()

	def SetCallBack(self, type, event=lambda *arg:None):
		self.callbackDict[type] = event

	def RunCallBack(self, type, *arg):

		if not self.callbackDict.has_key(type):
			self.DeattachObject()
			return

		self.callbackDict[type]()

	def ClearCallBack(self):
		self.callbackDict = {}
		
		
	if app.ENABLE_FISH_EVENT:
		def AttachFishPiece(self, owner, shape, img_handle, adjust_x, adjust_y, width, height):
			self.LastAttachedSlotNumber = self.AttachedSlotNumber
			self.countNumberLine.SetNumber("")
			self.countNumberLine.Hide()
			
			self.AttachedFlag = True
			self.AttachedOwner = owner
			self.AttachedType = playerm2g2.SLOT_TYPE_FISH_EVENT
			self.AttachedSlotNumber = -1
			self.AttachedItemIndex = shape
			self.AttachedCount = 0
			self.AttachedIconHandle = img_handle
			self.AttachedIconHalfWidth = grpImage.GetWidth(self.AttachedIconHandle) / 2 + adjust_x
			self.AttachedIconHalfHeight = grpImage.GetHeight(self.AttachedIconHandle) / 2 + adjust_y
			wndMgr.AttachIcon(self.AttachedType, self.AttachedItemIndex, self.AttachedSlotNumber, width, height)
			
		def DeattachObjectPostProcess(self):
			self.AttachedOwner = 0
			self.AttachedFlag = False
			self.AttachedType = -1
			self.AttachedItemIndex = -1
			self.AttachedSlotNumber = -1
			self.AttachedIconHandle = 0
			wndMgr.SetAttachingFlag(False)

			if self.countNumberLine:
				self.countNumberLine.Hide()
			
			if app.ENABLE_CHEQUE_SYSTEM:
				self.chequeValue = 0
				if self.chequeNumberLine:
					self.chequeNumberLine.Hide()
					
			app.ShowCursor()
			
		def SetAttachedIconRender(self, flag):
			self.IsAttachedIconRender = flag
			
		def GetAttachedIconRender(self):
			return self.IsAttachedIconRender

mouseController = CMouseController()
