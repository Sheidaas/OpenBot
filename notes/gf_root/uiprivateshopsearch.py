import ui
import m2netm2g
import app
import item
import chatm2g
import grp
import uiCommon
import localeInfo
import shop
import background
import playerm2g2

from _weakref import proxy

class ActionTextSlot(ui.ImageBox):
	def __init__(self, parent, x, y):
		ui.ImageBox.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.LoadImage("d:/ymir work/ui/public/Parameter_Slot_00.sub")

		self.mouseReflector = MouseReflector(self)
		self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())

		self.Enable = True
		self.textLine = ui.MakeTextLine(self)
		self.event = lambda *arg: None
		self.arg = 0
		self.Show()

		self.mouseReflector.UpdateRect()

	def __del__(self):
		ui.ImageBox.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetEvent(self, event, arg):
		self.event = event
		self.arg = arg

	def Disable(self):
		self.Enable = False

	def OnMouseOverIn(self):
		if not self.Enable:
			return
		self.mouseReflector.Show()

	def OnMouseOverOut(self):
		if not self.Enable:
			return
		self.mouseReflector.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.Enable:
			return
		self.mouseReflector.Down()

	def OnMouseLeftButtonUp(self):
		if not self.Enable:
			return
		self.mouseReflector.Up()
		self.event(self.arg)

class MouseReflector(ui.Window):
	def __init__(self, parent):
		ui.Window.__init__(self)
		self.SetParent(parent)
		self.AddFlag("not_pick")
		self.width = self.height = 0
		self.isDown = False

	def __del__(self):
		ui.Window.__del__(self)

	def Down(self):
		self.isDown = True

	def Up(self):
		self.isDown = False

	def OnRender(self):

		if self.isDown:
			grp.SetColor(ui.WHITE_COLOR)
		else:
			grp.SetColor(ui.HALF_WHITE_COLOR)

		x, y = self.GetGlobalPosition()
		grp.RenderBar(x+2, y+2, self.GetWidth()-4, self.GetHeight()-4)
		
class CheckBox(ui.ImageBox):
	def __init__(self, parent, x, y, event, filename = "d:/ymir work/ui/privatesearch/private_checkboxImg.sub"):
		ui.ImageBox.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.LoadImage(filename)

		self.mouseReflector = MouseReflector(self)
		self.mouseReflector.SetSize(self.GetWidth(), self.GetHeight())

		image = ui.MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 0, 0)
		image.AddFlag("not_pick")
		image.SetWindowHorizontalAlignCenter()
		image.SetWindowVerticalAlignCenter()
		image.Hide()
		self.Enable = True
		self.image = image
		self.event = event
		self.Show()

		self.mouseReflector.UpdateRect()

	def __del__(self):
		ui.ImageBox.__del__(self)

	def SetCheck(self, flag):
		if flag:
			self.image.Show()
		else:
			self.image.Hide()

	def Disable(self):
		self.Enable = False

	def OnMouseOverIn(self):
		if not self.Enable:
			return
		self.mouseReflector.Show()

	def OnMouseOverOut(self):
		if not self.Enable:
			return
		self.mouseReflector.Hide()

	def OnMouseLeftButtonDown(self):
		if not self.Enable:
			return
		self.mouseReflector.Down()

	def OnMouseLeftButtonUp(self):
		if not self.Enable:
			return
		self.mouseReflector.Up()
		self.event()
		
class PrivateShopSeachWindow(ui.ScriptWindow):
	MAX_LINE_COUNT = 10
	MAX_CHAR_LEVEL = 105
	CLICK_LIMIT_TIME = 3
	PAGEBUTTON_MAX_SIZE = 9
	PAGEBUTTON_NUMBER_SIZE = 5
	PAGEONE_MAX_SIZE = 50
	#SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	SPECIAL_TITLE_COLOR  = 0xff4E3D30
	
	if app.ENABLE_WOLFMAN_CHARACTER:
		JOB_MAX_COUNT = 5
		JOB_NAME_DIC = {	0 : localeInfo.JOB_WARRIOR,
				1 : localeInfo.JOB_ASSASSIN,
				2 : localeInfo.JOB_SURA,
				3 : localeInfo.JOB_SHAMAN, 
				4 : localeInfo.JOB_WOLFMAN, }
	else:
		JOB_MAX_COUNT = 4
		JOB_NAME_DIC = {	0 : localeInfo.JOB_WARRIOR,
				1 : localeInfo.JOB_ASSASSIN,
				2 : localeInfo.JOB_SURA,
				3 : localeInfo.JOB_SHAMAN, }

		
	ITEM_MASK_TYPE_DIC = { 	
		item.MASK_ITEM_TYPE_MOUNT_PET			:	localeInfo.CATEGORY_MOUNT_PET,
		item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON	:	localeInfo.CATEGORY_EQUIPMENT_WEAPON, 
		item.MASK_ITEM_TYPE_EQUIPMENT_ARMOR		:	localeInfo.CATEGORY_EQUIPMENT_ARMOR, 
		item.MASK_ITEM_TYPE_EQUIPMENT_JEWELRY	:	localeInfo.CATEGORY_EQUIPMENT_JEWELRY, 
		item.MASK_ITEM_TYPE_TUNING				:	localeInfo.CATEGORY_TUNING, 
		item.MASK_ITEM_TYPE_POTION				:	localeInfo.CATEGORY_POTION, 
		item.MASK_ITEM_TYPE_FISHING_PICK		:	localeInfo.CATEGORY_FISHING_PICK, 
		item.MASK_ITEM_TYPE_DRAGON_STONE		:	localeInfo.CATEGORY_DRAGON_STONE, 
		item.MASK_ITEM_TYPE_COSTUMES			:	localeInfo.CATEGORY_COSTUMES, 
		item.MASK_ITEM_TYPE_SKILL				:	localeInfo.CATEGORY_SKILL, 
		item.MASK_ITEM_TYPE_UNIQUE				:	localeInfo.CATEGORY_UNIQUE, 
		item.MASK_ITEM_TYPE_ETC					:	localeInfo.CATEGORY_ETC, 
	}

	## 1. Mount & Pet
	MOUNT_PET_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_MOUNT_PET_MOUNT 			: localeInfo.CATEGORY_MOUNT_PET_MOUNT,
		item.MASK_ITEM_SUBTYPE_MOUNT_PET_CHARGED_PET	: localeInfo.CATEGORY_MOUNT_PET_CHARGED_PET,
		item.MASK_ITEM_SUBTYPE_MOUNT_PET_FREE_PET 		: localeInfo.CATEGORY_MOUNT_PET_FREE_PET,
		item.MASK_ITEM_SUBTYPE_MOUNT_PET_EGG 			: localeInfo.CATEGORY_MOUNT_PET_EGG,	
	}
	
	## 2. Weapon
	WEAPON_MASK_SUBTYPE_DIC = { 
		0 : { 	
			item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_SWORD  : localeInfo.CATEGORY_WEAPON_WEAPON_SWORD,
			item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_TWO_HANDED : localeInfo.CATEGORY_WEAPON_WEAPON_TWO_HANDED,
		},
		
		1 : {	
			item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_SWORD  : localeInfo.CATEGORY_WEAPON_WEAPON_SWORD,
			item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_DAGGER : localeInfo.CATEGORY_WEAPON_WEAPON_DAGGER,
			item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_BOW : localeInfo.CATEGORY_WEAPON_WEAPON_BOW,
			item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_ARROW : localeInfo.CATEGORY_WEAPON_WEAPON_ARROW,
			item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_QUIVER : localeInfo.CATEGORY_WEAPON_WEAPON_QUIVER,
		}, 
		
		2 : { item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_SWORD  : localeInfo.CATEGORY_WEAPON_WEAPON_SWORD,}, 
		
		3 : {	item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_BELL   : localeInfo.CATEGORY_WEAPON_WEAPON_BELL,
				item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_FAN : localeInfo.CATEGORY_WEAPON_WEAPON_FAN,
		}, 
		4 : { item.MASK_ITEM_SUBTYPE_WEAPON_WEAPON_CLAW   : localeInfo.CATEGORY_WEAPON_WEAPON_CLAW,}, 
	}
	
	## 3. Armor
	ARMOR_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_ARMOR_ARMOR_BODY : localeInfo.CATEGORY_ARMOR_ARMOR_BODY,
		item.MASK_ITEM_SUBTYPE_ARMOR_ARMOR_HEAD : localeInfo.CATEGORY_ARMOR_ARMOR_HEAD,
		item.MASK_ITEM_SUBTYPE_ARMOR_ARMOR_SHIELD : localeInfo.CATEGORY_ARMOR_ARMOR_SHIELD,	
	}
	
	## 4. Jewelry
	JEWELRY_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_WRIST : localeInfo.CATEGORY_JEWELRY_ARMOR_WRIST,
		item.MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_FOOTS : localeInfo.CATEGORY_JEWELRY_ARMOR_FOOTS,
		item.MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_NECK : localeInfo.CATEGORY_JEWELRY_ARMOR_NECK,
		item.MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_EAR : localeInfo.CATEGORY_JEWELRY_ARMOR_EAR,
		item.MASK_ITEM_SUBTYPE_JEWELRY_ITEM_BELT : localeInfo.CATEGORY_JEWELRY_ITEM_BELT,	
	}
	if app.ENABLE_PENDANT:
		JEWELRY_MASK_SUBTYPE_DIC[item.MASK_ITEM_SUBTYPE_JEWELRY_ARMOR_PENDANT] = localeInfo.CATEGORY_JEWELRY_ARMOR_PENDANT
		
	## 5. Tuning
	TUNING_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_TUNING_RESOURCE : localeInfo.CATEGORY_TUNING_RESOURCE,
		item.MASK_ITEM_SUBTYPE_TUNING_STONE : localeInfo.CATEGORY_TUNING_STONE,
		item.MASK_ITEM_SUBTYPE_TUNING_ETC : localeInfo.CATEGORY_TUNING_ETC,
	}
	
	## 6. Potion
	POTION_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_POTION_ABILITY : localeInfo.CATEGORY_POTION_ABILITY,
		item.MASK_ITEM_SUBTYPE_POTION_HAIRDYE : localeInfo.CATEGORY_POTION_HAIRDYE,
		item.MASK_ITEM_SUBTYPE_POTION_ETC : localeInfo.CATEGORY_POTION_ETC,
	}
	
	## 7. Fishing & Pick
	FISHING_PICK_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_FISHING_PICK_FISHING_POLE : localeInfo.CATEGORY_FISHING_PICK_FISHING_POLE,
		item.MASK_ITEM_SUBTYPE_FISHING_PICK_EQUIPMENT_PICK : localeInfo.CATEGORY_FISHING_PICK_EQUIPMENT_PICK,
		item.MASK_ITEM_SUBTYPE_FISHING_PICK_FOOD : localeInfo.CATEGORY_FISHING_PICK_FOOD,
		item.MASK_ITEM_SUBTYPE_FISHING_PICK_STONE : localeInfo.CATEGORY_FISHING_PICK_STONE,
		item.MASK_ITEM_SUBTYPE_FISHING_PICK_ETC : localeInfo.CATEGORY_FISHING_PICK_ETC, 
	}
	
	## 8. DragonStone
	DRAGON_STONE_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_DIAMOND : localeInfo.CATEGORY_DRAGON_STONE_DRAGON_DIAMOND,
		item.MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_RUBY : localeInfo.CATEGORY_DRAGON_STONE_DRAGON_RUBY,
		item.MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_JADE : localeInfo.CATEGORY_DRAGON_STONE_DRAGON_JADE,
		item.MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_SAPPHIRE : localeInfo.CATEGORY_DRAGON_STONE_DRAGON_SAPPHIRE,
		item.MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_GARNET : localeInfo.CATEGORY_DRAGON_STONE_DRAGON_GARNET,
		item.MASK_ITEM_SUBTYPE_DRAGON_STONE_DRAGON_ONYX : localeInfo.CATEGORY_DRAGON_STONE_DRAGON_ONYX,
		item.MASK_ITEM_SUBTYPE_DRAGON_STONE_ETC : localeInfo.CATEGORY_DRAGON_STONE_ETC,
	}
	
	## 9. Costumes
	COSTUMES_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_COSTUMES_COSTUME_WEAPON : localeInfo.CATEGORY_COSTUMES_COSTUME_WEAPON,
		item.MASK_ITEM_SUBTYPE_COSTUMES_COSTUME_BODY : localeInfo.CATEGORY_COSTUMES_COSTUME_BODY,
		item.MASK_ITEM_SUBTYPE_COSTUMES_COSTUME_HAIR : localeInfo.CATEGORY_COSTUMES_COSTUME_HAIR,
		item.MASK_ITEM_SUBTYPE_COSTUMES_SASH : localeInfo.CATEGORY_COSTUMES_SASH,
		item.MASK_ITEM_SUBTYPE_COSTUMES_ETC : localeInfo.CATEGORY_COSTUMES_ETC,
	}
	
	## 10. Skill
	SKILL_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_SKILL_PAHAE : localeInfo.CATEGORY_SKILL_PAHAE,
		item.MASK_ITEM_SUBTYPE_SKILL_SKILL_BOOK : localeInfo.CATEGORY_SKILL_SKILL_BOOK,
		item.MASK_ITEM_SUBTYPE_SKILL_BOOK_OF_OBLIVION : localeInfo.CATEGORY_SKILL_BOOK_OF_OBLIVION,
		item.MASK_ITEM_SUBTYPE_SKILL_ETC : localeInfo.CATEGORY_SKILL_ETC,
	}
	
	## 11. Unique
	UNIQUE_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_UNIQUE_ABILITY : localeInfo.CATEGORY_UNIQUE_ABILITY,
		item.MASK_ITEM_SUBTYPE_UNIQUE_ETC : localeInfo.CATEGORY_UNIQUE_ETC,
	}
	
	## 12. Etc
	ETC_MASK_SUBTYPE_DIC = {
		item.MASK_ITEM_SUBTYPE_ETC_GIFTBOX : localeInfo.CATEGORY_ETC_GIFTBOX,
		item.MASK_ITEM_SUBTYPE_ETC_MATRIMORY : localeInfo.CATEGORY_ETC_MATRIMORY,
		item.MASK_ITEM_SUBTYPE_ETC_EVENT : localeInfo.CATEGORY_ETC_EVENT,
		item.MASK_ITEM_SUBTYPE_ETC_SEAL : localeInfo.CATEGORY_ETC_SEAL,
		item.MASK_ITEM_SUBTYPE_ETC_PARTI : localeInfo.CATEGORY_ETC_PARTI,
		item.MASK_ITEM_SUBTYPE_ETC_POLYMORPH : localeInfo.CATEGORY_ETC_POLYMORPH,
		item.MASK_ITEM_SUBTYPE_ETC_RECIPE : localeInfo.CATEGORY_ETC_RECIPE,
		item.MASK_ITEM_SUBTYPE_ETC_ETC : localeInfo.CATEGORY_ETC_ETC,
	}
	
	ITEM_MASK_MASK_SUBTYPE_DICS = {
		item.MASK_ITEM_TYPE_MOUNT_PET			:	MOUNT_PET_MASK_SUBTYPE_DIC,
		item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON	:	WEAPON_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_EQUIPMENT_ARMOR		:	ARMOR_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_EQUIPMENT_JEWELRY	:	JEWELRY_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_TUNING				:	TUNING_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_POTION				:	POTION_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_FISHING_PICK		:	FISHING_PICK_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_DRAGON_STONE		:	DRAGON_STONE_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_COSTUMES			:	COSTUMES_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_SKILL				:	SKILL_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_UNIQUE				:	UNIQUE_MASK_SUBTYPE_DIC, 
		item.MASK_ITEM_TYPE_ETC					:	ETC_MASK_SUBTYPE_DIC, 
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isloded = 0
		self.ItemNameValue = None
		self.minlevelvalue = 0
		self.maxlevelvalue = 0
		self.minrefinevalue = 0
		self.maxrefinevalue = 0
		self.mingoldvalue = 0
		self.maxgoldvalue = 0
		self.buybutton = None
		self.searchbutton = None
		self.listslotcount = 0
		self.selectitemRealindex = -1
		self.selectitemindex = -1
		self.SerchItemSlotList = {}
		self.ItemSlotButtonList = {}
		self.pagebuttonList = {}
		## ENABLE_PRIVATESHOP_CATEGORY
		self.saveitemMasktypeselectnumber = item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON
		#self.saveitemtypeselectnumber = item.ITEM_TYPE_WEAPON
		self.savejobselectnumber = 0
		self.saveitemMasksubtypeselectnumber = 0
		self.searchclicktime = 0.0
		self.buyclicktime = 0.0
		self.nowpagenumber = 1
		self.pluspagenumber = 0
		self.pagecount = 0
		self.bigpagecount = 1
		self.iscashitem = 0
		self.popup = None
		
		if app.ENABLE_CHEQUE_SYSTEM:
			self.minchequevalue = 0
			self.maxchequevalue = 0

	def __del__(self):
		self.ItemNameValue = None
		self.buybutton = None
		self.searchbutton = None
		self.popup = None
		self.SerchItemSlotList = {}
		self.ItemSlotButtonList = {}
		self.pagebuttonList = {}
		ui.ScriptWindow.__del__(self)

	
	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PrivateShopSearchDialog.py")
		except:
			import exception
			exception.Abort("PrivateShopSeachWindow.__LoadWindow.UIScript/PrivateShopSearchDialog.py")
			
		try:
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))
			self.searchbutton = self.GetChild("SearchButton")
			self.searchbutton.SetEvent(ui.__mem_func__(self.Search))
			self.buybutton = self.GetChild("BuyButton")
			self.buybutton.SetEvent(ui.__mem_func__(self.Buy))
			
			if localeInfo.IsARABIC():
				self.GetChild("leftcenterImg").LeftRightReverse()
				self.GetChild("rightcenterImg").LeftRightReverse()
				self.GetChild("LeftTop").LeftRightReverse()
				self.GetChild("RightTop").LeftRightReverse()
				self.GetChild("LeftBottom").LeftRightReverse()
				self.GetChild("RightBottom").LeftRightReverse()
				
				self.topcenterimg = self.GetChild("topcenterImg")
				self.topcenterimg.SetPosition(self.GetWidth() - (self.topcenterimg.GetWidth()*2)+10,36)
				
				self.bottomcenterImg = self.GetChild("bottomcenterImg")
				self.bottomcenterImg.SetPosition(self.GetWidth() - (self.bottomcenterImg.GetWidth()*2)+10,320)

				self.centerImg = self.GetChild("centerImg")
				self.centerImg.SetPosition(self.GetWidth() - (self.centerImg.GetWidth()*2)+10,52)

			self.ItemNameValue = self.GetChild("ItemNameValue")
			self.ItemNameValue.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.minlevelvalue = self.GetChild("minLevelValue")
			self.minlevelvalue.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.maxlevelvalue = self.GetChild("maxLevelValue")
			self.maxlevelvalue.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.minrefinevalue = self.GetChild("minrefineValue")
			self.minrefinevalue.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.maxrefinevalue = self.GetChild("maxrefineValue")
			self.maxrefinevalue.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.mingoldvalue = self.GetChild("GoldminValue")
			self.mingoldvalue.SetEscapeEvent(ui.__mem_func__(self.Close))
			self.maxgoldvalue = self.GetChild("GoldmaxValue")
			self.maxgoldvalue.SetEscapeEvent(ui.__mem_func__(self.Close))
			if app.ENABLE_CHEQUE_SYSTEM:
				self.minchequevalue = self.GetChild("ChequeminValue")
				self.minchequevalue.SetEscapeEvent(ui.__mem_func__(self.Close))
				self.maxchequevalue = self.GetChild("ChequemaxValue")
				self.maxchequevalue.SetEscapeEvent(ui.__mem_func__(self.Close))
			
			self.prev_button = self.GetChild("prev_button")
			self.prev_button.SetEvent(ui.__mem_func__(self.prevbutton))

			self.next_button = self.GetChild("next_button")
			self.next_button.SetEvent(ui.__mem_func__(self.nextbutton))

			self.first_prev_button = self.GetChild("first_prev_button")
			self.first_prev_button.SetEvent(ui.__mem_func__(self.firstprevbutton))

			self.last_next_button = self.GetChild("last_next_button")
			self.last_next_button.SetEvent(ui.__mem_func__(self.lastnextbutton))
			
			if localeInfo.IsARABIC():
				self.prev_button.LeftRightReverse()
				self.next_button.LeftRightReverse()
				self.first_prev_button.LeftRightReverse()
				self.last_next_button.LeftRightReverse()
			

			self.page1_button = self.GetChild("page1_button")
			self.page1_button.SetEvent(ui.__mem_func__(self.Pagebutton), 1)

			self.page2_button = self.GetChild("page2_button")
			self.page2_button.SetEvent(ui.__mem_func__(self.Pagebutton), 2)

			self.page3_button = self.GetChild("page3_button")
			self.page3_button.SetEvent(ui.__mem_func__(self.Pagebutton), 3)

			self.page4_button = self.GetChild("page4_button")
			self.page4_button.SetEvent(ui.__mem_func__(self.Pagebutton), 4)

			self.page5_button = self.GetChild("page5_button")
			self.page5_button.SetEvent(ui.__mem_func__(self.Pagebutton), 5)
			
			TemppageSlotButton = []
			TemppageSlotButton.append(self.page1_button)
			TemppageSlotButton.append(self.page2_button)
			TemppageSlotButton.append(self.page3_button)
			TemppageSlotButton.append(self.page4_button)
			TemppageSlotButton.append(self.page5_button)
			TemppageSlotButton.append(self.prev_button)
			TemppageSlotButton.append(self.next_button)
			TemppageSlotButton.append(self.first_prev_button)
			TemppageSlotButton.append(self.last_next_button)
			self.pagebuttonList[0] = TemppageSlotButton
			
			self.HidePageButton()

		except:
			import exception
			exception.Abort("PrivateShopSeachWindow.__LoadWindow.PrivateShopSearchDialog")

	def Open(self,iscash):
		if self.isloded == 0:
			self.isloded = 1
			self.__LoadWindow()
			self.SetCenterPosition()
			self.SetTop()
			self.__MakeResultSlot()
			self.iscashitem = 1
			if not iscash:
				self.iscashitem = 0
				self.buybutton.Disable()
				self.buybutton.Down()
			ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()
		self.isloded = 0
		background.DeletePrivateShopPos()
		self.selectitemRealindex = -1
		self.selectitemindex = -1
		self.savejobselectnumber = 0
		## ENABLE_PRIVATESHOP_CATEGORY
		self.saveitemMasktypeselectnumber = item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON
		#self.saveitemtypeselectnumber = item.ITEM_TYPE_WEAPON
		self.saveitemMasksubtypeselectnumber = 0
		if self.popup:
			self.popup.Close()
			self.popup = None
		self.ItemNameValue.KillFocus()
		
		m2netm2g.ClosePrivateShopSearchWindow()

	def Destroy(self):
		self.Hide()
		self.ClearDictionary()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __MakeResultSlot(self):
		yPos = 0
		for i in range(0,self.MAX_LINE_COUNT):
			yPos = 63 + i * 25

			## 아이템명
			itemSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_04.sub", 150+30, yPos)
			itemSlotImage.SetAlpha(0)
			itemNameSlot = ui.MakeTextLine(itemSlotImage)
			self.Children.append(itemSlotImage)
			self.Children.append(itemNameSlot)

			## 판매자
			SellerNameImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/parameter_slot_04.sub", 140+125+38, yPos)
			SellerNameImage.SetAlpha(0)
			SellerNameSlot = ui.MakeTextLine(SellerNameImage)
			self.Children.append(SellerNameImage)
			self.Children.append(SellerNameSlot)

			## 수량
			CountSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/Parameter_Slot_01.sub", 140+125+120+40, yPos)
			CountSlotImage.SetAlpha(0)
			CountSlot = ui.MakeTextLine(CountSlotImage)
			self.Children.append(CountSlotImage)
			self.Children.append(CountSlot)
			
			if app.ENABLE_CHEQUE_SYSTEM:
				## 가격
				PriceSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/Parameter_Slot_03.sub", 556, yPos)
				PriceSlotImage.SetAlpha(0)
				PriceSlot = ui.MakeTextLine(PriceSlotImage)
				self.Children.append(PriceSlotImage)
				self.Children.append(PriceSlot)	
				
				ChequeSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/Parameter_Slot_01.sub", 490, yPos)
				ChequeSlotImage.SetAlpha(0)
				ChequeSlot = ui.MakeTextLine(ChequeSlotImage)
				self.Children.append(ChequeSlotImage)
				self.Children.append(ChequeSlot)
			else:
				## 가격
				PriceSlotImage = ui.MakeImageBox(self, "d:/ymir work/ui/public/Parameter_Slot_03.sub", 140+125+85+90+40, yPos)
				PriceSlotImage.SetAlpha(0)
				PriceSlot = ui.MakeTextLine(PriceSlotImage)
				self.Children.append(PriceSlotImage)
				self.Children.append(PriceSlot)				

			if localeInfo.IsARABIC():
				itemSlotImage.SetPosition(self.GetWidth() - (140+30) - itemSlotImage.GetWidth() - 3,yPos)
				SellerNameImage.SetPosition(self.GetWidth() - (140+125+38) - SellerNameImage.GetWidth() - 3,yPos)
				CountSlotImage.SetPosition(self.GetWidth() - (140+125+120+40) - CountSlotImage.GetWidth() - 3,yPos)
				
				if app.ENABLE_CHEQUE_SYSTEM:
					ChequeSlotImage.SetPosition(self.GetWidth() - (490) - ChequeSlotImage.GetWidth() - 3,yPos)
					PriceSlotImage.SetPosition(self.GetWidth() - (556) - PriceSlotImage.GetWidth() - 3,yPos)
				else: 
					PriceSlotImage.SetPosition(self.GetWidth() - (140+125+85+90+40) - PriceSlotImage.GetWidth() - 3,yPos)

			anameslotlist = []
			anameslotlist.append(itemNameSlot)
			anameslotlist.append(SellerNameSlot)
			anameslotlist.append(CountSlot)
			anameslotlist.append(PriceSlot)
			if app.ENABLE_CHEQUE_SYSTEM:
				anameslotlist.append(ChequeSlot)

			self.SerchItemSlotList[i] = anameslotlist
			
			## 아이템 목록 버튼
			itemSlotButtonImage = ui.MakeButton(self, 138, yPos, "", "d:/ymir work/ui/", "tab_01.tga", "tab_02.tga", "tab_02.tga")
			itemSlotButtonImage.ShowToolTip = lambda slotIndex = i : self.OverInToolTip(slotIndex)
			itemSlotButtonImage.HideToolTip = lambda slotIndex = i : self.OverOutToolTip(slotIndex)
			itemSlotButtonImage.Hide()
			itemSlotButtonImage.SetEvent(ui.__mem_func__(self.__SelectItem),i)
			self.Children.append(itemSlotButtonImage)

			if localeInfo.IsARABIC():
				itemSlotButtonImage.LeftRightReverse()
				itemSlotButtonImage.SetPosition(self.GetWidth() - 138 - itemSlotButtonImage.GetWidth(),yPos)

			TempitemSlotButtonImage = []
			TempitemSlotButtonImage.append(itemSlotButtonImage)
			self.ItemSlotButtonList[i] = TempitemSlotButtonImage

		## 아이템 유형(서브타입)
		self.itemMasksubtypeselectslot = ui.ComboBoxImage(self, "d:/ymir work/ui/privatesearch/private_leftSlotImg.sub",12,115)
		self.itemMasksubtypeselectslot.SetEvent(lambda Masksubtypenumber, argSelf=proxy(self): argSelf.OnChangeItemSubTypeSlot(Masksubtypenumber))
		for i in self.WEAPON_MASK_SUBTYPE_DIC[0]:
			self.itemMasksubtypeselectslot.InsertItem(i,self.WEAPON_MASK_SUBTYPE_DIC[0][i])
		self.itemMasksubtypeselectslot.SetCurrentItem(self.WEAPON_MASK_SUBTYPE_DIC[0][0])
		self.itemMasksubtypeselectslot.Show()
		self.Children.append(self.itemMasksubtypeselectslot)

		if localeInfo.IsARABIC():
			self.itemMasksubtypeselectslot.SetPosition(self.GetWidth() - 12 - self.itemMasksubtypeselectslot.GetWidth() - 3,115)
		
		## 아이템 유형(타입)
		self.itemMasktypeselectslot = ui.ComboBoxImage(self, "d:/ymir work/ui/privatesearch/private_leftSlotImg.sub",12,95)
		self.itemMasktypeselectslot.SetEvent(lambda Masktypenumber, argSelf=proxy(self): argSelf.OnChangeItemTypeSlot(Masktypenumber))

		## ENABLE_PRIVATESHOP_CATEGORY
		for index, itemtypedic in self.ITEM_MASK_TYPE_DIC.items() :
			self.itemMasktypeselectslot.InsertItem(index,self.ITEM_MASK_TYPE_DIC[index])
		
		self.itemMasktypeselectslot.SetCurrentItem(self.ITEM_MASK_TYPE_DIC[item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON])
		self.itemMasktypeselectslot.Show()
		self.Children.append(self.itemMasktypeselectslot)			

		if localeInfo.IsARABIC():
			self.itemMasktypeselectslot.SetPosition(self.GetWidth() - 12 - self.itemMasktypeselectslot.GetWidth() - 3,95)

		## 장비 검색 대상
		self.jobselectslot = ui.ComboBoxImage(self, "d:/ymir work/ui/privatesearch/private_leftSlotImg.sub",12,55)
		self.jobselectslot.SetEvent(lambda jobnumber, argSelf=proxy(self): argSelf.OnChangeJobSlot(jobnumber))
		
		
		for i in range(0,self.JOB_MAX_COUNT):
			self.jobselectslot.InsertItem(i,self.JOB_NAME_DIC[i])
		self.jobselectslot.SetCurrentItem(self.JOB_NAME_DIC[0])
		self.jobselectslot.Show()
		self.Children.append(self.jobselectslot)
		
		if localeInfo.IsARABIC():
			self.jobselectslot.SetPosition(self.GetWidth() - 12 - self.jobselectslot.GetWidth() - 3,55)
			
	## 리프레쉬
	def RefreshList(self):
		count = shop.GetPrivateShopSearchResultCount()
		maxcount = shop.GetPrivateShopSearchResultMaxCount()
		page = shop.GetPrivateShopSearchResultPage()
		
		for line, nameSlotList in self.SerchItemSlotList.items():
			if app.ENABLE_CHEQUE_SYSTEM:
				itemname, sellername, count, price, cheque = shop.GetPrivateShopSearchResult(line)
				if "" == itemname:
					nameSlotList[0].SetText("")
					nameSlotList[1].SetText("")
					nameSlotList[2].SetText("")
					nameSlotList[3].SetText("")
					nameSlotList[4].SetText("")
					self.ItemSlotButtonList[line][0].Hide()
				else:
					nameSlotList[0].SetText(itemname)
					nameSlotList[1].SetText(sellername)
					nameSlotList[2].SetText(str(count))
					nameSlotList[3].SetText(self.NumberToMoneyString(price))
					nameSlotList[4].SetText(str(cheque))
					self.ItemSlotButtonList[line][0].Show()				
			else:
				itemname, sellername, count, price = shop.GetPrivateShopSearchResult(line)
				if "" == itemname:
					nameSlotList[0].SetText("")
					nameSlotList[1].SetText("")
					nameSlotList[2].SetText("")
					nameSlotList[3].SetText("")
					self.ItemSlotButtonList[line][0].Hide()
				else:
					nameSlotList[0].SetText(itemname)
					nameSlotList[1].SetText(sellername)
					nameSlotList[2].SetText(str(count))
					nameSlotList[3].SetText(self.NumberToMoneyString(price))
					self.ItemSlotButtonList[line][0].Show()
				
		self.ShowPageButton(maxcount,page)
		
		## 중간 앞 점프 버튼 활성화/비활성화
		if self.bigpagecount == 1:
			self.prev_button.Disable()
			self.prev_button.Down()
			#self.prev_button.Hide()
		else:
			self.prev_button.Enable()
			#self.prev_button.Show()

		## 맨 앞으로 점프 버튼 활성화/비활성화
		if self.bigpagecount - 1 <= 1:			
			self.first_prev_button.Disable()
			self.first_prev_button.Down()
			#self.first_prev_button.Hide()
		else:
			self.first_prev_button.Enable()
			#self.first_prev_button.Show()

		## 중간 뒤 점프 버튼 활성화/비활성화
		if maxcount <= self.bigpagecount * self.PAGEONE_MAX_SIZE:
			self.next_button.Disable()
			self.next_button.Down()
			#self.next_button.Hide()
		else:
			self.next_button.Enable()
			#self.next_button.Show()
			
		## 맨 뒤로 점프 버튼 활성화/비활성화
		if maxcount <= (self.bigpagecount+1) * self.PAGEONE_MAX_SIZE:
			self.last_next_button.Disable()
			self.last_next_button.Down()
			#self.last_next_button.Hide()
		else:
			self.last_next_button.Enable()
			#self.last_next_button.Show()
		 
	## 숫자에 콤마 추가.	
	def NumberToMoneyString(self,n) :
		if n <= 0 :
			return "0"

		return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), "") 
	
	## 페이지 버튼 클릭
	def Pagebutton(self,number):
		if number == self.nowpagenumber:
			return
		if self.bigpagecount > 1:
			if number == self.nowpagenumber - (self.bigpagecount-1) * 5:
				return
		
		self.clearPagebuttoncolor()
		self.pagebuttonList[0][number-1].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][number-1].Down()
		self.pagebuttonList[0][number-1].Disable()
		self.nowpagenumber = int(self.pagebuttonList[0][number-1].GetText())
		m2netm2g.SendPrivateShopSearchInfoSub(self.nowpagenumber)
		self.clearEffectEtc()
	
	## 맨처음 페이지로 이동.
	def firstprevbutton(self):

		if self.bigpagecount - 1 <= 1:
			return

		self.clearPagebuttoncolor()
		self.bigpagecount = 1
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagebutton[i].SetText(str(i+1))

		self.nowpagenumber = int(self.pagebuttonList[0][0].GetText())
		self.pagebuttonList[0][0].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][0].Down()
		self.pagebuttonList[0][0].Disable()
		m2netm2g.SendPrivateShopSearchInfoSub(self.nowpagenumber)
		self.clearEffectEtc()
			
	## 맨 마지막으로 이동 버튼.
	def lastnextbutton(self):
		maxsize = shop.GetPrivateShopSearchResultMaxCount()
		self.pagecount = maxsize / 10
		self.HidePageButton()
		self.clearPagebuttoncolor()
		
		if self.pagecount%5 == 0:
			self.bigpagecount = (self.pagecount/5)
		else:
			self.bigpagecount = (self.pagecount/5) + 1

		pagenumber = 5 * (self.pagecount/5)
		if pagenumber == self.pagecount:
			pagenumber -= 5
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagebutton[i].SetText(str(i+pagenumber+1))

		self.nowpagenumber = self.pagecount
		m2netm2g.SendPrivateShopSearchInfoSub(self.nowpagenumber)
		self.clearEffectEtc()
	
	## 이전 페이지 점프
	def prevbutton(self):
		if self.bigpagecount == 1:
			return

		self.clearPagebuttoncolor()
		self.bigpagecount -= 1

		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagenumber = int(pagebutton[i].GetText()) - 5
				pagebutton[i].SetText(str(pagenumber))
		
		self.nowpagenumber = int(self.pagebuttonList[0][0].GetText())
		self.pagebuttonList[0][0].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][0].Down()
		self.pagebuttonList[0][0].Disable()
		m2netm2g.SendPrivateShopSearchInfoSub(self.nowpagenumber)
		self.clearEffectEtc()

	
	## 다음 페이지 점프
	def nextbutton(self):
		maxitemcount = shop.GetPrivateShopSearchResultMaxCount()
		if maxitemcount < self.bigpagecount * self.PAGEONE_MAX_SIZE:
			return

		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagenumber = int(pagebutton[i].GetText()) + 5
				pagebutton[i].SetText(str(pagenumber))
				
		self.nowpagenumber = int(self.pagebuttonList[0][0].GetText())
		self.bigpagecount += 1
		self.HidePageButton()
		self.clearPagebuttoncolor()
		self.pagebuttonList[0][0].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][0].Down()
		self.pagebuttonList[0][0].Disable()
		m2netm2g.SendPrivateShopSearchInfoSub(self.nowpagenumber)
		self.clearEffectEtc()

	## 숫자 페이지 버튼 색 흰색으로.
	def clearPagebuttoncolor(self):
		for line, pagebutton in self.pagebuttonList.items():
			for i in range(0,self.PAGEBUTTON_NUMBER_SIZE):
				pagebutton[i].SetTextColor(0xffffffff)
				pagebutton[i].SetUp()
				pagebutton[i].Enable()
		
	## 페이지버튼 모두 숨기기
	def HidePageButton(self):
		for line, pagebutton in self.pagebuttonList.items():
			for i in range(0,self.PAGEBUTTON_MAX_SIZE):
				pagebutton[i].Hide()
	
	## 페이지 버튼들 골라서 보이기.		
	def ShowPageButton(self,maxsize,page):
	
		if self.bigpagecount > 1:
			maxsize = maxsize - ((self.bigpagecount-1) * self.PAGEONE_MAX_SIZE)
			page = page - (self.bigpagecount-1) * 5
			
		self.pagecount = maxsize / 10
		
		if not maxsize%10 == 0:
			self.pagecount = self.pagecount + 1

		if self.pagecount > 5:
			self.pagecount = 5
		
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(self.pagecount):
				pagebutton[i].Show()
				
		self.pagebuttonList[0][5].Show()
		self.pagebuttonList[0][6].Show()
		self.pagebuttonList[0][7].Show()
		self.pagebuttonList[0][8].Show()
		
		self.clearPagebuttoncolor()
		self.pagebuttonList[0][page-1].SetTextColor(self.SPECIAL_TITLE_COLOR)
		self.pagebuttonList[0][page-1].Down()
		self.pagebuttonList[0][page-1].Disable()
		self.nowpagenumber = page

	## button enable, disbale
	def OnUpdate(self):

		if (app.GetTime() - self.searchclicktime) > self.CLICK_LIMIT_TIME and self.searchbutton.IsDIsable() == 0:
			self.searchbutton.Enable()

		if (app.GetTime() - self.buyclicktime) > self.CLICK_LIMIT_TIME and self.buybutton.IsDIsable() == 0 and self.iscashitem == 1:
			self.buybutton.Enable()
			
	## 찾기 버튼 클릭
	def Search(self):
	
		privatesearchitemcount_6004 = playerm2g2.GetItemCountByVnum(60004)
		privatesearchitemcount_6005 = playerm2g2.GetItemCountByVnum(60005)

		if privatesearchitemcount_6004 <= 0 and privatesearchitemcount_6005 <= 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PRIVATESHOPSEARCH_NEED_ITEM_FIND)
			self.Close()
			return

		self.searchclicktime = app.GetTime()
		self.searchbutton.Disable()
		self.searchbutton.SetUp()
		
		job = self.savejobselectnumber
		Masktype = self.saveitemMasktypeselectnumber
		Masksub = self.saveitemMasksubtypeselectnumber
		
		## 강화
		if len(self.minrefinevalue.GetText()) <= 0:
			self.minrefinevalue.SetText("0")
		if len(self.maxrefinevalue.GetText()) <= 0:
			self.maxrefinevalue.SetText("9")
		## 레벨
		if len(self.minlevelvalue.GetText()) <= 0:
			self.minlevelvalue.SetText("1")
		if len(self.maxlevelvalue.GetText()) <= 0:
			self.maxlevelvalue.SetText("105")
		## 돈
		if len(self.mingoldvalue.GetText()) <= 0:
			self.mingoldvalue.SetText("1")
		if len(self.maxgoldvalue.GetText()) <= 0:
			self.maxgoldvalue.SetText("900000000")

		minrefine = int(self.minrefinevalue.GetText())
		maxrefine = int(self.maxrefinevalue.GetText())
		minlevel = int(self.minlevelvalue.GetText())
		if minlevel == 1:
			minlevel = 0
		
		maxlevel = int(self.maxlevelvalue.GetText())
		mingold = int(self.mingoldvalue.GetText())
		maxgold = int(self.maxgoldvalue.GetText())
		itemname = self.ItemNameValue.GetText()
		
		if mingold > playerm2g2.GOLD_MAX - 1:
			mingold = playerm2g2.GOLD_MAX - 1
			self.mingoldvalue.SetText(str(playerm2g2.GOLD_MAX - 1))
			
		if maxgold > playerm2g2.GOLD_MAX - 1:
			maxgold = playerm2g2.GOLD_MAX - 1
			self.maxgoldvalue.SetText(str(playerm2g2.GOLD_MAX - 1))
		
		if app.ENABLE_CHEQUE_SYSTEM:
			if len(self.minchequevalue.GetText()) <= 0:
				self.minchequevalue.SetText(str(0))
			if len(self.maxchequevalue.GetText()) <= 0:
				self.maxchequevalue.SetText(str(CHEQUE_MAX-1))
			
			mincheque = int(self.minchequevalue.GetText())
			maxcheque = int(self.maxchequevalue.GetText())
			if mincheque > playerm2g2.CHEQUE_MAX - 1:
				mincheque = playerm2g2.CHEQUE_MAX - 1
				self.minchequevalue.SetText(str(playerm2g2.CHEQUE_MAX - 1))
				
			if maxcheque > playerm2g2.CHEQUE_MAX - 1:
				maxcheque = playerm2g2.CHEQUE_MAX - 1
				self.maxchequevalue.SetText(str(playerm2g2.CHEQUE_MAX - 1))
					
			m2netm2g.SendPrivateShopSearchInfo(job,Masktype,Masksub,minrefine,maxrefine,minlevel,maxlevel,mingold,maxgold,itemname,mincheque,maxcheque)
		else:
			m2netm2g.SendPrivateShopSearchInfo(job,Masktype,Masksub,minrefine,maxrefine,minlevel,maxlevel,mingold,maxgold,itemname)

		for line, nameSlotList in self.SerchItemSlotList.items():
			nameSlotList[0].SetText("")
			nameSlotList[1].SetText("")
			nameSlotList[2].SetText("")
			nameSlotList[3].SetText("")
			if app.ENABLE_CHEQUE_SYSTEM:
				nameSlotList[4].SetText("")
			
			self.ItemSlotButtonList[line][0].Hide()
			
		self.clearEffectEtc()
		self.HidePageButton()
		self.bigpagecount = 1
		for line, pagebutton in self.pagebuttonList.items():
			for i in xrange(5):
				pagenumber = int(pagebutton[i].GetText()) - 5
				pagebutton[i].SetText(str(i+1))

	## 구매 버튼 클릭
	def Buy(self):
	
		privatesearchitemcount_60005 = playerm2g2.GetItemCountByVnum(60005)
		if privatesearchitemcount_60005 <= 0:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PRIVATESHOPSEARCH_NEED_ITEM_BUY)
			self.Close()
			return

		if self.selectitemRealindex == -1:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PRIVATESHOPSEARCH_SELECTITEM)
			return

		self.buyclicktime = app.GetTime()
		self.buybutton.Disable()
		self.buybutton.SetUp()

		popup = uiCommon.QuestionDialog()
		popup.SetText(localeInfo.PRIVATESHOPSEARCH_BUYTIME)
		popup.SetAcceptEvent(self.OnBuyAcceptEvent)
		popup.SetCancelEvent(self.OnBuyCloseEvent)
		popup.Open()
		self.popup = popup

	## 구매 확인
	def OnBuyAcceptEvent(self):
		if self.selectitemRealindex == -1:
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PRIVATESHOPSEARCH_SELECTITEM)
			return
		m2netm2g.SendPrivateShopSerchBuyItem(self.selectitemRealindex)
		self.clearEffectEtc()
		self.Search()
		self.popup.Close()
		self.popup = None
		
	## 구매 취소
	def OnBuyCloseEvent(self):
		self.popup.Close()
		self.popup = None
		self.clearEffectEtc()
		
	## 선택 버튼 클릭
	def __SelectItem(self,arg):
		self.selectitemRealindex = arg
		self.selectitemindex = arg
		self.__SelectItemSlotButtonList(arg)

		## 타겟 이펙트 생성	
		chrvid = shop.GetPrivateShopSelectItemChrVID(self.selectitemRealindex)
		background.DeletePrivateShopPos(chrvid)
		background.CreatePrivateShopPos(chrvid)

	## 모든 선택 버튼 Up
	def __ClearItemSlotButtonList(self):
		for line, ItemSlotButtonList in self.ItemSlotButtonList.items():
			ItemSlotButtonList[0].SetUp()

	## 해당 슬롯 제외한 모든 버튼 Up
	def __SelectItemSlotButtonList(self, index):
		for line, ItemSlotButtonList in self.ItemSlotButtonList.items():
			if index != line:
				ItemSlotButtonList[0].SetUp()
			else:
				ItemSlotButtonList[0].Down()

	## ===== 툴팁 관련 =====
	def SetItemToolTip(self, tooltip):
		self.tooltipitem = tooltip
		
	def __ShowToolTip(self, slotIndex):
		if self.tooltipitem:
			self.tooltipitem.SetPrivateSearchItem(slotIndex)

	def OverInToolTip(self,slotIndex):
		self.__ShowToolTip(slotIndex)
		
	def OverOutToolTip(self,slotIndex):
		if self.tooltipitem:
			self.tooltipitem.HideToolTip()

		if self.selectitemindex == slotIndex:
			self.ItemSlotButtonList[slotIndex][0].Down()
	
	## 아이템 서브타입 선택시
	def OnChangeItemSubTypeSlot(self, Masksubtypenumber):
		## ENABLE_PRIVATESHOP_CATEGORY
		if self.saveitemMasktypeselectnumber == item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON:
			self.itemMasksubtypeselectslot.SetCurrentItem(self.WEAPON_MASK_SUBTYPE_DIC[self.savejobselectnumber][Masksubtypenumber])
		else:
			self.itemMasksubtypeselectslot.SetCurrentItem(self.ITEM_MASK_MASK_SUBTYPE_DICS[self.saveitemMasktypeselectnumber][Masksubtypenumber])
		self.saveitemMasksubtypeselectnumber = Masksubtypenumber
	
	## 직업 유형 선택시.
	def OnChangeJobSlot(self,jobnumber):
		self.jobselectslot.SetCurrentItem(self.JOB_NAME_DIC[jobnumber])
		if jobnumber != self.savejobselectnumber:
			## ENABLE_PRIVATESHOP_CATEGORY
			if self.saveitemMasktypeselectnumber == item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON:
				self.itemMasksubtypeselectslot.ClearItem()
				Masksubtype = 0
				savefirst = 0
				for i in self.WEAPON_MASK_SUBTYPE_DIC[jobnumber]:
					self.itemMasksubtypeselectslot.InsertItem(i,self.WEAPON_MASK_SUBTYPE_DIC[jobnumber][i])
					if Masksubtype == 0:
						if savefirst == 0:
							Masksubtype = i
							savefirst = 1
				self.itemMasksubtypeselectslot.SetCurrentItem(self.WEAPON_MASK_SUBTYPE_DIC[jobnumber][Masksubtype])
				self.saveitemMasksubtypeselectnumber = Masksubtype # 서브타입 저장.
			self.savejobselectnumber = jobnumber

	## 아이템 유형 타입 선택시
	def OnChangeItemTypeSlot(self,Masktypenumber):
		self.itemMasktypeselectslot.SetCurrentItem(self.ITEM_MASK_TYPE_DIC[Masktypenumber])
		if Masktypenumber != self.saveitemMasktypeselectnumber:
			self.itemMasksubtypeselectslot.ClearItem()
			## ENABLE_PRIVATESHOP_CATEGORY
			if Masktypenumber == item.MASK_ITEM_TYPE_EQUIPMENT_WEAPON:
				Masksubtype = 0
				savefirst = 0
				for i in self.WEAPON_MASK_SUBTYPE_DIC[self.savejobselectnumber]:
					self.itemMasksubtypeselectslot.InsertItem(i,self.WEAPON_MASK_SUBTYPE_DIC[self.savejobselectnumber][i])
					if Masksubtype == 0:
						if savefirst == 0:
							Masksubtype = i
							savefirst = 1
				self.itemMasksubtypeselectslot.SetCurrentItem(self.WEAPON_MASK_SUBTYPE_DIC[self.savejobselectnumber][Masksubtype])
				self.saveitemMasksubtypeselectnumber = Masksubtype # 서브타입 저장.
			else:
				Masksubtype = 0
				savefirst = 0
				for i in self.ITEM_MASK_MASK_SUBTYPE_DICS[Masktypenumber]:
					self.itemMasksubtypeselectslot.InsertItem(i,self.ITEM_MASK_MASK_SUBTYPE_DICS[Masktypenumber][i])
					if Masksubtype == 0:
						if savefirst == 0:
							Masksubtype = i
							savefirst = 1
				self.itemMasksubtypeselectslot.SetCurrentItem(self.ITEM_MASK_MASK_SUBTYPE_DICS[Masktypenumber][Masksubtype])
				self.saveitemMasksubtypeselectnumber = Masksubtype # 서브타입 저장.
			self.saveitemMasktypeselectnumber = Masktypenumber
			
	## 이펙트 및 아이템 선택 초기화
	def clearEffectEtc(self):
		background.DeletePrivateShopPos()
		self.__ClearItemSlotButtonList()
		self.selectitemRealindex = -1
		self.selectitemindex = -1

	def OnTop(self):
		self.ItemNameValue.SetFocus()