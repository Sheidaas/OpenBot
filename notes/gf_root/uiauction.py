import ui
class AuctionWindow(ui.ScriptWindow):

	class PageWindow(ui.ScriptWindow):
		def __init__(self, parent, filename):
			ui.ScriptWindow.__init__(self)
			self.SetParent(parent)
			self.filename = filename
		def GetScriptFileName(self):
			return self.filename

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

		self.SelectPage("UNIQUE_AUCTION")

	def __LoadWindow(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/auctionwindow.py")

		self.pageName = {
			"LIST"				: "�Ÿ� ����Ʈ",
			"REGISTER"			: "�Ÿ� ���",
			"UNIQUE_AUCTION"	: "����ũ ���",
		}
		self.pageWindow = {
			"LIST"				: self.PageWindow(self, "uiscript/auctionwindow_listpage.py"),
			"REGISTER"			: self.PageWindow(self, "uiscript/auctionwindow_registerpage.py"),
			"UNIQUE_AUCTION"	: self.PageWindow(self, "uiscript/auctionwindow_uniqueauctionpage.py"),
		}

		self.board = self.GetChild("Board")
		self.tabDict = {
			"LIST"				: self.GetChild("Tab_01"),
			"REGISTER"			: self.GetChild("Tab_02"),
			"UNIQUE_AUCTION"	: self.GetChild("Tab_03"),
		}
		self.tabButtonDict = {
			"LIST"				: self.GetChild("Tab_Button_01"),
			"REGISTER"			: self.GetChild("Tab_Button_02"),
			"UNIQUE_AUCTION"	: self.GetChild("Tab_Button_03"),
		}
		for page in self.pageWindow.values():
			pyScrLoader.LoadScriptFile(page, page.GetScriptFileName())
		for key, button in self.tabButtonDict.items():
			button.SetEvent(self.SelectPage, key)

		self.__MakeListPage()
		self.__MakeRegisterPage()
		self.__MakeUniqueAuctionPage()

	def Destroy(self):
		self.ClearDictionary()

	def __MakeListPage(self):

		page = self.pageWindow["LIST"]

		yPos = 27

		AUCTION_LINE_COUNT = 10

		for i in xrange(AUCTION_LINE_COUNT):

			numberSlotImage = ui.MakeImageBox(page, "d:/ymir work/ui/public/Parameter_Slot_00.sub", 11, yPos)
			numberSlot = ui.MakeTextLine(numberSlotImage)
			page.Children.append(numberSlotImage)
			page.Children.append(numberSlot)

			nameSlotImage = ui.MakeImageBox(page, "d:/ymir work/ui/public/Parameter_Slot_04.sub", 55, yPos)
			nameSlot = ui.MakeTextLine(nameSlotImage)
			page.Children.append(nameSlotImage)
			page.Children.append(nameSlot)

			priceSlotImage = ui.MakeImageBox(page, "d:/ymir work/ui/public/Parameter_Slot_05.sub", 175, yPos)
			priceSlot = ui.MakeTextLine(priceSlotImage)
			page.Children.append(priceSlotImage)
			page.Children.append(priceSlot)

			deleteButton = ui.Button()
			deleteButton.SetParent(page)
			deleteButton.SetPosition(310, yPos)
			deleteButton.SetUpVisual("d:/ymir work/ui/public/small_button_01.sub")
			deleteButton.SetOverVisual("d:/ymir work/ui/public/small_button_02.sub")
			deleteButton.SetDownVisual("d:/ymir work/ui/public/small_button_03.sub")
			deleteButton.SetText("����")
			deleteButton.Show()
			page.Children.append(deleteButton)

			yPos += 20

	def __MakeRegisterPage(self):
		pass

	def __MakeUniqueAuctionPage(self):

		page = self.pageWindow["UNIQUE_AUCTION"]

		LINE_COUNT = 3

		for i in xrange(LINE_COUNT):

			yPos = 5 + 99*i

			itemSlotImage = ui.MakeSlotBar(page, 10, yPos, 97, 97)
			page.Children.append(itemSlotImage)

			itemName = ui.MakeTextLine(page, False, 117, yPos + 14)
			page.Children.append(itemName)
			## Temporary
			itemName.SetText("������ ���")
			## Temporary

			curPrice = ui.MakeTextLine(page, False, 117, yPos + 31)
			page.Children.append(curPrice)
			## Temporary
			curPrice.SetText("���簡 : 20�� 1234�� 1234��")
			## Temporary

			lastTime = ui.MakeTextLine(page, False, 117, yPos + 48)
			page.Children.append(lastTime)
			## Temporary
			lastTime.SetText("�������� ���� �ð� : 19�� 28��")
			## Temporary

			priceSlotImage = ui.MakeImageBox(page, "d:/ymir work/ui/public/Parameter_Slot_05.sub", 117, yPos + 65)
			priceSlot = ui.MakeTextLine(priceSlotImage)
			page.Children.append(priceSlotImage)
			page.Children.append(priceSlot)
			## Temporary
			priceSlot.SetText("20�� 1234�� 1234��")
			## Temporary

	def SelectPage(self, arg):
		for key, btn in self.tabButtonDict.items():
			if arg != key:
				btn.SetUp()
		for key, img in self.tabDict.items():
			if arg == key:
				img.Show()
			else:
				img.Hide()
		for key, page in self.pageWindow.items():
			if arg == key:
				page.Show()
			else:
				page.Hide()
		self.board.SetTitleName(self.pageName[arg])
