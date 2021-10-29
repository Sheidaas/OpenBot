import dbg
import playerm2g2
import item
import m2netm2g
import snd
import ui
import uiToolTip
import localeInfo
import app

class AttachMetinDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.metinItemPos = 0
		self.targetItemPos = 0
		
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			self.metinItemWindow	= None
			self.targetItemWindow	= None
			
	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/attachstonedialog.py")

		except:
			import exception
			exception.Abort("AttachStoneDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.metinImage = self.GetChild("MetinImage")
			self.GetChild("AcceptButton").SetEvent(ui.__mem_func__(self.Accept))
			self.GetChild("CancelButton").SetEvent(ui.__mem_func__(self.Close))
		except:
			import exception
			exception.Abort("AttachStoneDialog.__LoadScript.BindObject")

		oldToolTip = uiToolTip.ItemToolTip()
		oldToolTip.SetParent(self)
		oldToolTip.SetPosition(15, 38)
		oldToolTip.SetFollow(False)
		oldToolTip.Show()
		self.oldToolTip = oldToolTip

		newToolTip = uiToolTip.ItemToolTip()
		newToolTip.SetParent(self)
		newToolTip.SetPosition(230 + 20, 38)
		newToolTip.SetFollow(False)
		newToolTip.Show()
		self.newToolTip = newToolTip

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.titleBar = 0
		self.metinImage = 0
		self.toolTip = 0

	def CanAttachMetin(self, slot, metin):
		if item.METIN_NORMAL == metin:
			if playerm2g2.METIN_SOCKET_TYPE_SILVER == slot or playerm2g2.METIN_SOCKET_TYPE_GOLD == slot:
				return True

		elif item.METIN_GOLD == metin:
			if playerm2g2.METIN_SOCKET_TYPE_GOLD == slot:
				return True

	
	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def Open(self, metinItemWindow, metinItemPos, targetItemWindow, targetItemPos):
			self.metinItemPos = metinItemPos
			self.targetItemPos = targetItemPos
			
			self.metinItemWindow	= metinItemWindow
			self.targetItemWindow	= targetItemWindow

			metinIndex = playerm2g2.GetItemIndex(metinItemWindow, metinItemPos)
			itemIndex = playerm2g2.GetItemIndex(targetItemWindow, targetItemPos)
			self.oldToolTip.ClearToolTip()
			self.newToolTip.ClearToolTip()

			item.SelectItem(metinIndex)

			## Metin Image
			try:
				self.metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("AttachMetinDialog.Open.LoadImage - Failed to find item data")

			## Old Item ToolTip
			metinSlot = []
			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(playerm2g2.GetItemMetinSocket(targetItemWindow, targetItemPos, i))
			self.oldToolTip.AddItemData(itemIndex, metinSlot)

			## New Item ToolTip
			item.SelectItem(metinIndex)
			metinSubType = item.GetItemSubType()

			metinSlot = []
			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(playerm2g2.GetItemMetinSocket(targetItemWindow, targetItemPos, i))
			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				slotData = metinSlot[i]
				if self.CanAttachMetin(slotData, metinSubType):
					metinSlot[i] = metinIndex
					break
			self.newToolTip.AddItemData(itemIndex, metinSlot)

			self.UpdateDialog()
			self.SetTop()
			self.Show()
	else:
	
		def Open(self, metinItemPos, targetItemPos):
			self.metinItemPos = metinItemPos
			self.targetItemPos = targetItemPos

			metinIndex = playerm2g2.GetItemIndex(metinItemPos)
			itemIndex = playerm2g2.GetItemIndex(targetItemPos)
			self.oldToolTip.ClearToolTip()
			self.newToolTip.ClearToolTip()

			item.SelectItem(metinIndex)

			## Metin Image
			try:
				self.metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("AttachMetinDialog.Open.LoadImage - Failed to find item data")

			## Old Item ToolTip
			metinSlot = []
			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(playerm2g2.GetItemMetinSocket(targetItemPos, i))
			self.oldToolTip.AddItemData(itemIndex, metinSlot)

			## New Item ToolTip
			item.SelectItem(metinIndex)
			metinSubType = item.GetItemSubType()

			metinSlot = []
			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				metinSlot.append(playerm2g2.GetItemMetinSocket(targetItemPos, i))
			for i in xrange(playerm2g2.METIN_SOCKET_MAX_NUM):
				slotData = metinSlot[i]
				if self.CanAttachMetin(slotData, metinSubType):
					metinSlot[i] = metinIndex
					break
			self.newToolTip.AddItemData(itemIndex, metinSlot)

			self.UpdateDialog()
			self.SetTop()
			self.Show()

	def UpdateDialog(self):
		newWidth = self.newToolTip.GetWidth() + 230 + 15 + 20
		newHeight = self.newToolTip.GetHeight() + 98

		if localeInfo.IsARABIC():
			self.board.SetPosition( newWidth, 0 )

			(x,y) = self.titleBar.GetLocalPosition()
			self.titleBar.SetPosition( newWidth - 15, y )

		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def Accept(self):
	
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			m2netm2g.SendItemUseToItemPacket(self.metinItemWindow, self.metinItemPos, self.targetItemWindow, self.targetItemPos)
		else:
			m2netm2g.SendItemUseToItemPacket(self.metinItemPos, self.targetItemPos)
			
		snd.PlaySound("sound/ui/metinstone_insert.wav")
		self.Close()

	def Close(self):
		self.Hide()
