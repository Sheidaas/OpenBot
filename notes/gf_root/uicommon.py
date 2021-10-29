import ui
import localeInfo
import app
import ime
import uiScriptLocale
import chatm2g

if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM or app.ENABLE_CHEQUE_SYSTEM :
	import playerm2g2

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()
		self.acceptEvent()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		
		if self.board.IsRTL():
			self.board.SetPosition(width, 0)
			
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.accceptButton.SetText(name)

	def OnPressEscapeKey(self):
		self.Close()
		
		if app.ENABLE_FISH_EVENT:
			if self.cancelButton:
				self.cancelButton.CallEvent()
				
		return True

	def OnIMEReturn(self):
		self.Close()
		return True
		
	def GetTextSize(self):
		if self.message:
			return self.message.GetTextSize()
			
		return (0,0)
		
	def GetLineHeight(self):
		if self.message:
			return self.message.GetLineHeight()
		
		return 0
		
	def SetLineHeight(self, Height):
		self.message.SetLineHeight(Height)
		
	def GetTextLineCount(self):
		return self.message.GetTextLineCount()
	
	if app.ENABLE_MINI_GAME_YUTNORI:
		def SetButtonNameAutoSize(self, name):
			self.accceptButton.SetAutoSizeText(name)
		def SetButtonHorizontalAlignCenter(self):
			self.accceptButton.SetWindowHorizontalAlignCenter()
		def SetButtonUpVisual(self, filename):
			self.accceptButton.SetUpVisual( filename )
		def SetButtonOverVisual(self, filename):
			self.accceptButton.SetOverVisual( filename )
		def SetButtonDownVisual(self, filename):
			self.accceptButton.SetDownVisual( filename )

if app.ENABLE_MINI_GAME_YUTNORI:
	class PopupDialog2(ui.ScriptWindow):

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.__LoadDialog()
			self.acceptEvent = lambda *arg: None

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __LoadDialog(self):
			try:
				PythonScriptLoader = ui.PythonScriptLoader()
				PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog2.py")

				self.board = self.GetChild("board")
				self.message1 = self.GetChild("message1")
				self.message2 = self.GetChild("message2")
				self.accceptButton = self.GetChild("accept")
				self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

			except:
				import exception
				exception.Abort("PopupDialog2.LoadDialog.BindObject")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()
			self.acceptEvent()

		def Destroy(self):
			self.Close()
			self.ClearDictionary()

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)
			
			if self.board.IsRTL():
				self.board.SetPosition(width, 0)
			
			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SetText1(self, text):
			self.message1.SetText(text)
		def SetText2(self, text):
			self.message2.SetText(text)

		def SetAcceptEvent(self, event):
			self.acceptEvent = event

		def SetButtonName(self, name):
			self.accceptButton.SetText(name)

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def OnIMEReturn(self):
			self.Close()
			return True
			
		def GetTextSize(self):
			if self.message1:
				return self.message1.GetTextSize()
				
			return (0,0)
			
		def GetLineHeight(self):
			if self.message1:
				return self.message1.GetLineHeight()
			
			return 0
				
		def SetLineHeight(self, Height):
			self.message1.SetLineHeight(Height)
			
		def GetTextLineCount(self):
			return self.message1.GetTextLineCount()
			
												
class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	#MT-679 개인 상점 타이틀의 CodePage 이슈
	def SetUseCodePage(self, bUse = True):
		self.inputValue.SetUseCodePage(bUse)
		
	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())	
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		if localeInfo.IsARABIC() :
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "inputdialogwithdescription.py")
		else:
			pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
	
		if self.board.IsRTL():
			self.board.SetPosition(width, 0)
					
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def GetTextSize(self):
		if self.textLine:
			return self.textLine.GetTextSize()
			
		return (0,0)
		
	def GetLineHeight(self):
		if self.textLine:
			return self.textLine.GetLineHeight()
		
		return 0
			
	def SetLineHeight(self, Height):
		self.textLine.SetLineHeight(Height)
		
	def GetTextLineCount(self):
		return self.textLine.GetTextLineCount()
			
class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)
	
	if app.ENABLE_GROWTH_PET_SKILL_DEL:
		def GetTextSize1(self):
			if self.textLine1:
				return self.textLine1.GetTextSize()
				
			return (0,0)
			
		def GetTextSize2(self):
			if self.textLine2:
				return self.textLine2.GetTextSize()
				
			return (0,0)

class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0
		self.timeoverMsg = None
		self.isCancelOnTimeover = False

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, msg, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.SetText1(msg)
		self.endTime = app.GetTime() + timeout

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2(localeInfo.UI_LEFT_TIME % (leftTime))
		if leftTime<0.5:
			if self.timeoverMsg:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, self.timeoverMsg)
			if self.isCancelOnTimeover:
				self.cancelButton.CallEvent()
			
	def SetTimeOverMsg(self, msg):
		self.timeoverMsg = msg
	
	def SetCancelOnTimeOver(self):
		self.isCancelOnTimeover = True

class MoneyInputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.SetMaxLength(10)
		else:
			self.SetMaxLength(9)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")
		
		if app.ENABLE_CHEQUE_SYSTEM:
			self.chequeText = getObject("ChequeValue")
			self.inputChequeValue = getObject("InputValue_Cheque")
			self.inputChequeValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
			self.inputChequeValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickChequeEditLine)
			self.inputValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		if app.ENABLE_CHEQUE_SYSTEM:
			self.inputChequeValue = None
		
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			length = min(10, length)
		else:
			length = min(9, length)

		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.OnIMEReturn = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.OnPressEscapeKey = event

	def SetValue(self, value):
		value=str(value)
		self.inputValue.SetText(value)
		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value)+1)		


	def GetText(self):
		return self.inputValue.GetText()

	if app.ENABLE_CHEQUE_SYSTEM:
		def SetCheque(self, cheque):
			cheque=str(cheque)
			self.inputChequeValue.SetText(cheque)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(cheque)+1)
		
		def __ClickChequeEditLine(self) :
			self.inputChequeValue.SetFocus()
			if len(self.inputValue.GetText()) <= 0:
				self.inputValue.SetText(str(0))

		def __ClickValueEditLine(self) :
			self.inputValue.SetFocus()
			if len(self.inputChequeValue.GetText()) <= 0:
				self.inputChequeValue.SetText(str(0))
						
		def GetCheque(self):
			return self.inputChequeValue.GetText()
			
		def __OnValueUpdate(self):
			if self.inputValue.IsFocus() :
				ui.EditLine.OnIMEUpdate(self.inputValue)
			elif self.inputChequeValue.IsFocus() :
				ui.EditLine.OnIMEUpdate(self.inputChequeValue)
			else:
				pass
				
			text = self.inputValue.GetText()
			cheque_text = self.inputChequeValue.GetText()
			
			money = 0
			cheque = 0
			
			if text and text.isdigit() :
				try:
					money = int(text)
					
					if money >= playerm2g2.GOLD_MAX:
						money = playerm2g2.GOLD_MAX - 1
						self.inputValue.SetText(str(money))
				except ValueError:
					money = 0

			if cheque_text and cheque_text.isdigit() :
				try:
					cheque = int(cheque_text)
					
					if cheque >= playerm2g2.CHEQUE_MAX:
						cheque = playerm2g2.CHEQUE_MAX - 1
						self.inputValue.SetText(str(cheque))
				except ValueError:
					cheque = 0
			
			self.chequeText.SetText(str(cheque) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
			self.moneyText.SetText(localeInfo.NumberToMoneyString(money) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_YANG)
 
	else:
		def __OnValueUpdate(self):
			ui.EditLine.OnIMEUpdate(self.inputValue)

			text = self.inputValue.GetText()

			money = 0
			if text and text.isdigit():
				try:
					money = int(text)
					
					if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
						if money >= playerm2g2.GOLD_MAX:
							money = playerm2g2.GOLD_MAX - 1
							self.inputValue.SetText(str(money))

				except ValueError:
					money = 199999999

			self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(money))
			



if app.ENABLE_MONSTER_CARD:
	class ExPopupDialog(ui.ScriptWindow):

		def __init__(self, layer = "UI"):
			ui.ScriptWindow.__init__(self, layer)
			self.__LoadDialog()
			self.acceptEvent = lambda *arg: None

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __LoadDialog(self):
			try:
				PythonScriptLoader = ui.PythonScriptLoader()
				PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

				self.board = self.GetChild("board")
				self.message = self.GetChild("message")
				self.accceptButton = self.GetChild("accept")
				self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

			except:
				import exception
				exception.Abort("PopupDialog.LoadDialog.BindObject")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()
			self.acceptEvent()

		def Destroy(self):
			self.Close()
			self.ClearDictionary()

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)
			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SetText(self, text):
			self.message.SetText(text)

		def SetAcceptEvent(self, event):
			self.acceptEvent = event

		def SetButtonName(self, name):
			self.accceptButton.SetText(name)

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def OnIMEReturn(self):
			self.Close()
			return True
			
		def GetTextSize(self):
			if self.message:
				return self.message.GetTextSize()
				
			return (0,0)
			
		def GetLineHeight(self):
			if self.message:
				return self.message.GetLineHeight()
			
			return 0
				
		if app.WJ_MULTI_TEXTLINE or app.ENABLE_EXTEND_INVEN_SYSTEM:
			def SetLineHeight(self, Height):
				self.message.SetLineHeight(Height)
				
			def GetTextLineCount(self):
				return self.message.GetTextLineCount()
				
				
	class ExQuestionDialog(ui.ScriptWindow):

		def __init__(self, layer = "UI"):
			ui.ScriptWindow.__init__(self, layer)
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

			self.board = self.GetChild("board")
			self.textLine = self.GetChild("message")
			self.acceptButton = self.GetChild("accept")
			self.cancelButton = self.GetChild("cancel")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)
			
			if self.board.IsRTL():
				self.board.SetPosition(width, 0)
				
			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SAFE_SetAcceptEvent(self, event):
			self.acceptButton.SAFE_SetEvent(event)

		def SAFE_SetCancelEvent(self, event):
			self.cancelButton.SAFE_SetEvent(event)

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)

		def SetCancelEvent(self, event):
			self.cancelButton.SetEvent(event)

		def SetText(self, text):
			self.textLine.SetText(text)

		def SetAcceptText(self, text):
			self.acceptButton.SetText(text)

		def SetCancelText(self, text):
			self.cancelButton.SetText(text)

		def OnPressEscapeKey(self):
			self.Close()
			return True
			
		def GetTextSize(self):
			if self.textLine:
				return self.textLine.GetTextSize()
				
			return (0,0)
			
		def GetLineHeight(self):
			if self.textLine:
				return self.textLine.GetLineHeight()
			
			return 0
				
		def SetLineHeight(self, Height):
			self.textLine.SetLineHeight(Height)
			
		def GetTextLineCount(self):
			return self.textLine.GetTextLineCount()