##
## Interface
##
import constInfo
import systemSetting
import wndMgr
import chatm2g
import app
import playerm2g2
import uiTaskBar
import uiCharacter
import uiInventory
import uiDragonSoul
import uiChat
import uiMessenger
import guild

import ui
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiSystem
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
import uiCube
import miniMap
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiselectitem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
if app.ENABLE_GEM_SYSTEM:
	import uiselectitemEx
import uiScriptLocale
import event
import localeInfo
import item
import uiSkillBookCombination
import uiAcce

if app.ENABLE_12ZI:
	import ui12zi
	
if app.ENABLE_GROWTH_PET_SYSTEM:
	import uiPetInfo 
if app.ENABLE_MOVE_COSTUME_ATTR:
	import uiItemCombination
	
if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
	import uiPrivateShopSearch

if app.ENABLE_CHANGED_ATTR :
	import uiSelectAttr

if app.ENABLE_EXTEND_INVEN_SYSTEM:
	import uiNewInventory
		
if app.ENABLE_GUILDRENEWAL_SYSTEM:
	#[guild_renewal]
	import uiGuildBank	
	
import uiMiniGame
	
if app.ENABLE_AUTO_SYSTEM:
	import uiAuto
	
if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
	import uiGuildDragonLairRanking
	
if app.ENABLE_CHANGE_LOOK_SYSTEM:
	import uiChangeLook
	import shop

if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
	import uiRankingBoard
	
if app.ENABLE_MONSTER_CARD:
	import uiMonsterCard
	
if app.ENABLE_MYSHOP_DECO:
	import uiMyShopDecoration
	import uiPrivateShop
	
if app.ENABLE_BATTLE_FIELD:
	import uiBattleField
	
if app.ENABLE_PARTY_MATCH:
	import uiPartyMatch

if app.ENABLE_GEM_SYSTEM:
	import uiGemShop
	
if app.ENABLE_USER_SITUATION_NOTICE:
	import uiUserSituationNotice
	
if app.ENABLE_SPECIAL_GACHA:
	import uiSpecialGacha

if app.ENABLE_PVP_TOURNAMENT_GF:
	import m2netm2g
		
IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2
	
	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		self.tipBoard = None
		self.bigBoard = None
		
		if app.ENABLE_OX_RENEWAL:
			self.bigBoardControl = None
			
		if app.ENABLE_12ZI:
			self.missionBoard = None

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL

		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndGuildBuilding = None
		if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR:
			self.OnTopWindow = None
			self.dlgShop = None
			self.dlgExchange = None
			self.privateShopBuilder = None
			self.wndSafebox = None
		if app.ENABLE_MOVE_COSTUME_ATTR:
			self.wndItemCombination = None
		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow = None
		
		self.wndSkillBookCombination = None

		if app.ENABLE_CHANGED_ATTR :
			self.wndSelectAttr = None
			
		self.wndMiniGame = None
			
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow = None
			
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = None
			
		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			self.wndRankingBoardWindow = None
			
		if app.ENABLE_MONSTER_CARD:
			self.wndMonsterCardWindow = None

		if app.ENABLE_MYSHOP_DECO:
			self.wndMyShopDeco = None

		if app.ENABLE_BATTLE_FIELD:
			self.wndBattleField = None
		
		if app.ENABLE_12ZI:
			self.wndBead = None
			
		if app.ENABLE_PARTY_MATCH:
			self.wndPartyMatchWindow = None

		if app.ENABLE_GEM_SYSTEM:
			self.wndExpandedMoneyTaskBar = None
			self.wndGemShop = None
			
		if app.ENABLE_USER_SITUATION_NOTICE:
			self.wndUserSituationNotice = None
			
		if app.ENABLE_SPECIAL_GACHA:
			self.wndSpecialGacha = None
						
		if app.ENABLE_PVP_TOURNAMENT_GF:
			self.pvp_tournament_auto_OnOff = 0
			
		event.SetInterfaceWindow(self)
		self.uiAffectshower = None
		self.uitargetBoard = None
		self.IsHideUiMode = False

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):
		
		wndChat = uiChat.ChatWindow()
		
		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 0)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

	def __MakeTaskBar(self):
		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleExpandedButton))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))
			
			import app
			if app.ENABLE_GROWTH_PET_SYSTEM:
				self.PetInformationActivate()
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, ui.__mem_func__(self.TogglePetInformationWindow))
			if app.ENABLE_AUTO_SYSTEM:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_AUTO_WINDOW, ui.__mem_func__(self.ToggleAutoWindow))
			if app.ENABLE_MONSTER_CARD:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_MONSTER_CARD_WINDOW, ui.__mem_func__(self.ToggleMonsterCardWindow))
			if app.ENABLE_PARTY_MATCH:
				self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_PARTY_MATCH_WINDOW, ui.__mem_func__(self.TogglePartyMatchWindow))
				
		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))
		
		self.wndEnergyBar = None
		wndEnergyBar = uiTaskBar.EnergyBar()
		wndEnergyBar.LoadWindow()
		self.wndEnergyBar = wndEnergyBar	
		
		if app.ENABLE_GEM_SYSTEM:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleExpandedMoneyButton))
			self.wndExpandedMoneyTaskBar = uiTaskBar.ExpandedMoneyTaskBar()
			self.wndExpandedMoneyTaskBar.LoadWindow()
			if self.wndInventory:
				self.wndInventory.SetExpandedMoneyBar(self.wndExpandedMoneyTaskBar)

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True
		
	def __MakeWindows(self):
		self.wndCharacter = uiCharacter.CharacterWindow()
		
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			self.wndInventory = uiNewInventory.InventoryWindow()
		else:
			self.wndInventory = uiInventory.InventoryWindow()
		self.wndInventory.BindInterfaceClass(self)
			
		self.wndDragonSoul = uiDragonSoul.DragonSoulWindow()	
		self.wndDragonSoul.BindInterfaceClass(self)
		self.wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		 
		self.wndMiniMap = uiMiniMap.MiniMap()
		self.wndSafebox = uiSafebox.SafeboxWindow()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.wndSafebox.BindInterface(self)
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow = uiPetInfo.PetInformationWindow()
			self.wndPetInfoWindow.BindInterfaceClass(self)
			self.wndInventory.SetPetHatchingWindow( self.wndPetInfoWindow.GetPetHatchingWindow() )
			self.wndInventory.SetPetFeedWindow( self.wndPetInfoWindow.GetPetFeedWindow() )
			self.wndInventory.SetPetNameChangeWindow( self.wndPetInfoWindow.GetPetNameChangeWindow() )
			
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow = uiAuto.AutoWindow()
			
		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			self.wndRankingBoardWindow = uiRankingBoard.RankingBoardWindow()
			
		if app.ENABLE_MONSTER_CARD:
			self.wndMonsterCardWindow = uiMonsterCard.MonsterCardWindow()

		if app.ENABLE_MYSHOP_DECO:
			self.wndMyShopDeco = uiMyShopDecoration.MyShopDecoration()
			
		if app.ENABLE_BATTLE_FIELD:
			self.wndBattleField = uiBattleField.BattleFieldWindow()
		
		if app.ENABLE_PARTY_MATCH:
			self.wndPartyMatchWindow = uiPartyMatch.PartyMatch()
			
		self.wndMall = uiSafebox.MallWindow()

		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.wndGuildBank = uiGuildBank.GuildBankDialog()

		self.wndSkillBookCombination = uiSkillBookCombination.SkillBookCombinationWindow()
			
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSeachWindow()

		if app.ENABLE_CHANGED_ATTR:
			self.wndSelectAttr = uiSelectAttr.SelectAttrWindow()
		
		self.wndAcce = uiAcce.AcceWindow()
		
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook = uiChangeLook.ChangeLookWindow()
			
		if app.ENABLE_MOVE_COSTUME_ATTR:
			wndItemCombination = uiItemCombination.ItemCombinationWindow()
			wndItemCombination.BindInterface(self)
			self.wndItemCombination = wndItemCombination
			
		if app.ENABLE_GEM_SYSTEM:
			self.wndGemShop = uiGemShop.GemShopWindow()

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)
		self.wndChatLog = wndChatLog		
			
		self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
		self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
		self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
		
		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			self.wndGuildDragonLairRanking = uiGuildDragonLairRanking.GuildDragonLairRankingDialog()

		if app.ENABLE_USER_SITUATION_NOTICE:
			self.wndUserSituationNotice = uiUserSituationNotice.UserSituationNotice()
			self.wndUserSituationNotice.BindInterface(self)
			
	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog()
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgExchange.BindInterface(self)
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		self.dlgShop.LoadDialog()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()
		
		if app.ENABLE_MYSHOP_DECO:
			self.dlgPrivateShop = uiPrivateShop.PrivateShopDialog()
			self.dlgPrivateShop.Hide()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		self.dlgSystem = uiSystem.SystemDialog()
		self.dlgSystem.LoadDialog()
		self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.tooltipPetSkill = uiToolTip.PetSkillToolTip()
			self.tooltipPetSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		if app.WJ_ENABLE_TRADABLE_ICON:
			self.privateShopBuilder.BindInterface(self)
		self.privateShopBuilder.Hide()

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		self.dlgRefineNew.Hide()

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()
		
		if app.ENABLE_OX_RENEWAL:
			self.bigBoardControl = uiTip.BigBoardControl()
			self.bigBoardControl.Hide()
		
		if app.ENABLE_12ZI:
			self.missionBoard = uiTip.MissionBoard()
			self.missionBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		self.wndCube = uiCube.CubeWindow()
		self.wndCube.LoadWindow()
		self.wndCube.Hide()

	def __MakeCubeResultWindow(self):
		self.wndCubeResult = uiCube.CubeResultWindow()
		self.wndCubeResult.LoadWindow()
		self.wndCubeResult.Hide()

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiselectitem.SelectItemWindow()
		self.wndItemSelect.Hide()

	if app.ENABLE_GEM_SYSTEM:
		def __MakeItemSelectWindowEx(self):
			print "__MakeItemSelectWindowEx"
			self.wndItemSelectEx = uiselectitemEx.SelectItemWindowEx()
			self.wndItemSelectEx.Hide()
			

	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
				
	def MakeInterface(self):
		self.__MakeTipBoard()	# ENABLE_12ZI 미션 표시가 다른ui 밑에 오도록 위치 이동.
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeWebWindow()
		self.__MakeCubeWindow()
		self.__MakeCubeResultWindow()
		
		
		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_GEM_SYSTEM:
			self.__MakeItemSelectWindowEx()
		
		if app.ENABLE_12ZI:
			self.__Make12ziTimerWindow()
			self.__MakeBeadWindow()
			self.__Make12ziRewardWindow()

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
		self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)
		self.wndCubeResult.SetItemToolTip(self.tooltipItem)
		
		# MT-818 [GF] 아이템 - 제조 성공된 아이템이 펫먹이가 되는 이슈
		self.wndCube.SetInven(self.wndInventory)
		
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			self.wndGuildBank.SetItemToolTip(self.tooltipItem)

		self.wndAcce.SetItemToolTip(self.tooltipItem)
		
		if app.ENABLE_MOVE_COSTUME_ATTR:
			self.wndItemCombination.SetInven(self.wndInventory)
			self.wndItemCombination.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			self.wndPrivateShopSearch.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL

		self.wndSkillBookCombination.SetInven(self.wndInventory)

		if app.ENABLE_CHANGED_ATTR :
			self.wndSelectAttr.SetInven(self.wndInventory)

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)
		
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.SetSkillToolTip(self.tooltipSkill)
			self.wndAutoWindow.SetItemToolTip(self.tooltipItem)
			
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			self.wndChangeLook.SetItemToolTip(self.tooltipItem)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
		if app.ENABLE_GEM_SYSTEM:
			self.wndItemSelectEx.SetItemToolTip(self.tooltipItem)

		self.dlgShop.SetItemToolTip(self.tooltipItem)
		
		if app.ENABLE_MYSHOP_DECO:
			self.dlgPrivateShop.SetItemToolTip(self.tooltipItem)
			
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_CHEQUE_SYSTEM:
			self.privateShopBuilder.SetInven(self.wndInventory)
			self.dlgExchange.SetInven(self.wndInventory)

		self.__InitWhisper()
		self.DRAGON_SOUL_IS_QUALIFIED = False
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.SetItemToolTip(self.tooltipItem)
			self.wndPetInfoWindow.SetInven(self.wndInventory)
			self.wndPetInfoWindow.SetPetSkillToolTip(self.tooltipPetSkill)
			
		if not app.ENABLE_MINI_GAME_OKEY_NORMAL:
			self.MiniGameOkey()
			
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:
			self.IntegrationEventBanner()
				
		if app.ENABLE_PARTY_MATCH:
			self.wndPartyMatchWindow.SetItemToolTip(self.tooltipItem)
			self.wndPartyMatchWindow.BindMiniMap(self.wndMiniMap)
			if self.wndMiniMap:
				self.wndMiniMap.BindPartyMatchEvent( self.TogglePartyMatchWindow )
			
		if app.ENABLE_GEM_SYSTEM:
			self.wndGemShop.SetItemToolTip(self.tooltipItem)

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
				
			if app.ENABLE_GROWTH_PET_SYSTEM and "itempet" == type:
				self.hyperlinkItemTooltip.SetHyperlinkPetItem(tokens)
			
	if app.ENABLE_12ZI:
		def __MakeBeadWindow(self):
			self.wndBead = ui12zi.BeadWindow()
			self.wndBead.Hide()
			
		def __Make12ziRewardWindow(self):
			self.wnd12ziReward = ui12zi.Reward12ziWindow()
			self.wnd12ziReward.SetItemToolTip(self.tooltipItem)
			self.wnd12ziReward.Hide()
			
		def __Make12ziTimerWindow(self):
			self.wnd12ziTimer = ui12zi.FloorLimitTimeWindow()
			self.wnd12ziTimer.Hide()

	## Make Windows & Dialogs
	################################

	def Close(self):
		if app.ENABLE_MOVE_COSTUME_ATTR and self.wndItemCombination:
			self.wndItemCombination.Destroy()
			
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.Hide()
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Destroy()
		
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Destroy()
			
		if app.ENABLE_GEM_SYSTEM:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Destroy()
			
		if self.wndEnergyBar:
			self.wndEnergyBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()
			
		if self.wndDragonSoul:
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Destroy()
			
		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Destroy()
		
		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				self.wndAutoWindow.Destroy()	
				
		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Destroy()	
				
		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				self.wndBattleField.Destroy()
				
		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Hide()
				self.wndBead.Destroy()
				del self.wndBead
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
				self.wnd12ziTimer.Destroy()
				del self.wnd12ziTimer
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()
				self.wnd12ziReward.Destroy()
				del self.wnd12ziReward

		if self.dlgExchange:
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Destroy()
			
		if app.ENABLE_MYSHOP_DECO and self.dlgPrivateShop:
			self.dlgPrivateShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Destroy()
			
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			if self.wndGuildBank:
				self.wndGuildBank.Hide()
				self.wndGuildBank.Destory()
				
		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			if self.wndGuildDragonLairRanking:
				self.wndGuildDragonLairRanking.Destory()	

		if self.wndWeb:
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Destroy()

		if self.wndHelp:
			self.wndHelp.Destroy()

		if self.wndCube:
			self.wndCube.Destroy()
			
		if self.wndCubeResult:
			self.wndCubeResult.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Destroy()

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_GEM_SYSTEM:
			if self.wndItemSelectEx:
				self.wndItemSelectEx.Destroy()

		self.wndSkillBookCombination.Destroy()
		del self.wndSkillBookCombination

		if app.ENABLE_CHANGED_ATTR :
			self.wndSelectAttr.Destroy()
			del self.wndSelectAttr
			
		if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Destroy()
				del self.wndPrivateShopSearch
		
		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				del self.wndAutoWindow
				
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if self.wndChangeLook:
				del self.wndChangeLook
				
		if app.ENABLE_MONSTER_CARD:
			if self.wndMonsterCardWindow:
				self.wndMonsterCardWindow.Destroy()
				del self.wndMonsterCardWindow
				
		if app.ENABLE_MYSHOP_DECO:
			if self.wndMyShopDeco:
				self.wndMyShopDeco.Destroy()
				del self.wndMyShopDeco
				
		if app.ENABLE_GEM_SYSTEM:
			if self.wndGemShop:
				self.wndGemShop.Destroy()
				del self.wndGemShop
				
		if app.ENABLE_USER_SITUATION_NOTICE:
			if self.wndUserSituationNotice:
				self.wndUserSituationNotice.Destroy()
				del self.wndUserSituationNotice

		if app.ENABLE_PARTY_MATCH:
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.Destroy()
				del self.wndPartyMatchWindow
			
		self.wndChatLog.Destroy()
		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar

		if app.ENABLE_GEM_SYSTEM:
			if self.wndExpandedMoneyTaskBar:
				del self.wndExpandedMoneyTaskBar

		del self.wndEnergyBar
		del self.wndCharacter
		del self.wndInventory
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
			
		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				del self.wndPetInfoWindow
				
		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				del self.wndRankingBoardWindow
				
		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				del self.wndBattleField

		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndHelp
		del self.wndCube
		del self.wndCubeResult
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		del self.wndItemSelect

		if app.ENABLE_GEM_SYSTEM:
			del self.wndItemSelectEx
		
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			del self.wndGuildBank

		if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
			del self.wndGuildDragonLairRanking

		if app.ENABLE_OX_RENEWAL:
			del self.bigBoardControl
			
		if app.ENABLE_GROWTH_PET_SYSTEM:
			del self.tooltipPetSkill
			
		if self.wndMiniGame:
			self.wndMiniGame.Destroy()
			del self.wndMiniGame
			
		if app.ENABLE_MYSHOP_DECO:
			del self.dlgPrivateShop
			
		if app.ENABLE_12ZI:
			del self.missionBoard

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.OnActivateSkill()

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)
		if app.ENABLE_AUTO_SYSTEM:
			self.wndAutoWindow.OnDeactivateSkill(slotIndex)


	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if self.wndEnergyBar:
			self.wndEnergyBar.RefreshStatus()
		self.wndDragonSoul.RefreshStatus()
			
		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.wndPetInfoWindow.RefreshStatus()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		self.wndDragonSoul.RefreshItemSlot()
		if playerm2g2.GetAcceRefineWindowOpen() == 1:
			self.wndAcce.RefreshAcceWindow()
		
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			if playerm2g2.GetChangeLookWindowOpen() == 1:
				self.wndChangeLook.RefreshChangeLookWindow()

	def RefreshCharacter(self): ## Character 페이지의 얼굴, Inventory 페이지의 전신 그림 등의 Refresh
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()
		
	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def RefreshGuildBank(self):
			self.wndGuildBank.RefreshBank()
			
	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def RefreshGuildDragonLairRanking(self,type):
			self.wndGuildDragonLairRanking.RefreshGuildDragonLairRanking(type)

		if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
			def SetGuildDragonLairFistGuildText(self, second):
				self.wndMiniMap.SetGuildDragonLairFistGuildText(second)
			def SetGuildDragonLiarStart(self):
				self.wndMiniMap.SetGuildDragonLiarStart()
			def SetGuildDragonLiarSuccess(self):
				self.wndMiniMap.SetGuildDragonLiarSuccess()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()
		
	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		## guild_renewal
		def RefreshGuildBaseInfoPage(self):
			self.wndGuild.RefreshGuildBaseInfoPage()

		## GuildBaseInfoBankGold
		def RefreshGuildBaseInfoPageBankGold(self):
			self.wndGuild.RefreshGuildBaseInfoPageBankGold()
	
		## guild_renewal_war
		def RefreshGuildWarInfoPage(self):
			self.wndGuild.RefreshGuildWarInfoPage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		self.wndInventory.Show()
		self.wndInventory.SetTop()
		
		if app.ENABLE_MYSHOP_DECO:
			import chr
			if chr.IsNPC(vid):
				self.dlgShop.Open(vid)
				self.dlgShop.SetTop()
			else:
				self.dlgPrivateShop.Open(vid)
				self.dlgPrivateShop.SetTop()
		else:
			self.dlgShop.Open(vid)
			self.dlgShop.SetTop()

	def CloseShopDialog(self):
		if app.ENABLE_MYSHOP_DECO:
			if self.dlgPrivateShop.IsShow():
				self.dlgPrivateShop.Close()
			elif self.dlgShop.IsShow():
				self.dlgShop.Close()
			else:
				return
		else:
			self.dlgShop.Close()

	def RefreshShopDialog(self):
		if app.ENABLE_MYSHOP_DECO:
			if self.dlgPrivateShop.IsShow():
				self.dlgPrivateShop.Refresh()
			elif self.dlgShop.IsShow():
				self.dlgShop.Refresh()
			else:
				return
		else:
			self.dlgShop.Refresh()

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))
		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE
		
	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()
		
	if app.ENABLE_CHEQUE_SYSTEM :
		def AddExchangeItemSlotIndex(self, idx) :
			self.dlgExchange.AddExchangeItemSlotIndex(idx)

	## Party
	if app.WJ_SHOW_PARTY_ON_MINIMAP and app.ENABLE_PARTY_CHANNEL_FIX:
		def AddPartyMember(self, pid, name, mapIdx, channel):
			self.wndParty.AddPartyMember(pid, name, mapIdx, channel)
			self.__ArrangeQuestButton()
	elif app.WJ_SHOW_PARTY_ON_MINIMAP:
		def AddPartyMember(self, pid, name, mapIdx):
			self.wndParty.AddPartyMember(pid, name, mapIdx)
			self.__ArrangeQuestButton()
	else:
		def AddPartyMember(self, pid, name):
			self.wndParty.AddPartyMember(pid, name)
			self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	if app.WJ_SHOW_PARTY_ON_MINIMAP and app.ENABLE_PARTY_CHANNEL_FIX:
		def LinkPartyMember(self, pid, vid, mapIdx, channel):
			self.wndParty.LinkPartyMember(pid, vid, mapIdx, channel)
	elif app.WJ_SHOW_PARTY_ON_MINIMAP:
		def LinkPartyMember(self, pid, vid, mapIdx):
			self.wndParty.LinkPartyMember(pid, vid, mapIdx)
	else:
		def LinkPartyMember(self, pid, vid):
			self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		##!! 20061026.levites.퀘스트_위치_보정
		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def RefreshSafeboxMoney(self):
		self.wndSafebox.RefreshSafeboxMoney()

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()
		
	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def OpenGuildBankWindow(self, size):
			self.wndGuildBank.ShowWindow(size)
		def CommandCloseGuildBank(self):
			self.wndGuildBank.CommandCloseGuildBank()
		def RefreshGuildBankInfo(self):
			self.wndGuildBank.RefreshGuildBankInfo()
		def OpenGuildBankInfo(self):
			self.wndGuildBank.OpenBankInfo()
		def SetGuildWarType(self, index):
			self.wndGuild.SetGuildWarType(index)
		def OpenGuildScoreWindow(self):
			self.wndGuild.OpenGuildScoreWindow()
		def OpenGuildGoldInOutWindow(self, inout):
			self.wndGuild.OpenGuildGoldInOutWindow(inout)
			
	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		def OpenGuildDragonLairRanking(self,type):
			self.wndGuildDragonLairRanking.Open(type)
		def GetDragonLairType(self):
			self.wndGuildDragonLairRanking.GetDragonLairType()
		
	if app.ENABLE_PRIVATESHOP_SEARCH_SYSTEM:
		def OpenPShopSearchDialog(self):
			self.wndPrivateShopSearch.Open(0)
		def OpenPShopSearchDialogCash(self):
			self.wndPrivateShopSearch.Open(1)
		def RefreshPShopSearchDialog(self):
			self.wndPrivateShopSearch.RefreshList()

	def AcceDialogOpen(self, type):
		self.wndAcce.Open(type)

		if self.dlgRefineNew:
			if self.dlgRefineNew.IsShow:
				self.wndAcce.Close()
				return

		if False == self.wndInventory.IsShow():
			self.wndInventory.Show()
		
	def RefreshAcceWindow(self):
		self.wndAcce.RefreshAcceWindow()

	## HilightSlot Change			
	def DeactivateSlot(self, slotindex, type):
		self.wndInventory.DeactivateSlot(slotindex, type)

	## HilightSlot Change		
	def ActivateSlot(self, slotindex, type):
		self.wndInventory.ActivateSlot(slotindex, type)
		
	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def ChangeWindowOpen(self):
			if self.wndChangeLook:
				if not shop.GetNameDialogOpen():
					self.wndChangeLook.Open()

				if self.dlgRefineNew:
					if self.dlgRefineNew.IsShow:
						self.wndChangeLook.Close()
			
	if app.ENABLE_MOVE_COSTUME_ATTR:
		def ItemCombinationDialogOpen(self):
			self.wndItemCombination.Open()
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				
	if app.ENABLE_GEM_SYSTEM:
		def OpenGemShop(self):
			if self.wndGemShop:
				self.wndGemShop.Open()
		def CloseGemShop(self):
			if self.wndGemShop:
				self.wndGemShop.Close()
		def RefreshGemShopWIndow(self):
			if self.wndGemShop:
				self.wndGemShop.RefreshGemShopWIndow()
		def GemShopSlotBuy(self, slotindex, enable):
			if self.wndGemShop:
				self.wndGemShop.GemShopSlotBuy(slotindex, enable)
		def GemShopSlotAdd(self, slotindex, enable):
			if self.wndGemShop:
				self.wndGemShop.GemShopSlotAdd(slotindex, enable)

	def OpenSkillbookCombinationDialog(self) :
		if self.wndSkillBookCombination.IsShow() :
			return

		if self.privateShopBuilder.IsShow() :
			chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE_NOT_OPEN)
			return

		self.wndSkillBookCombination.Open()
		self.wndSkillBookCombination.Show()

		if not self.wndInventory.IsShow() :
			self.wndInventory.Show()

	if app.ENABLE_CHANGED_ATTR :
		def OpenSelectAttrDialog(self, window_type, slotIdx) :
			if self.wndSelectAttr.IsShow() :
				return

			if self.privateShopBuilder.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOT_OPEN)
				return

			self.wndSelectAttr.Open(window_type, slotIdx)
			self.wndSelectAttr.Show()

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			## 새로생긴 보드판 들어갈 값 업데이트
			self.wndGuild.GuildWarOppGuildNameSetting(guildSelf, guildOpp)		
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]
		
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			## 새로생긴 보드판 초기화
			self.wndGuild.GuildWarEnd()

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point, winpoint):
			key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
			if not self.guildScoreBoardDict.has_key(key):
				return

			guildBoard = self.guildScoreBoardDict[key]
			guildBoard.SetScore(gainGuildID, opponentGuildID, point)
			## guild_renewal_war
			## 새로생긴 보드판에 들어갈 값 업데이트
			self.wndGuild.GuildWarScoreSetting(gainGuildID, opponentGuildID, point, winpoint)
	else:
		def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
			key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
			if not self.guildScoreBoardDict.has_key(key):
				return

			guildBoard = self.guildScoreBoardDict[key]
			guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
	
		self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	def SetAffectShower(self, shower):
		from _weakref import proxy
		self.uiAffectshower = proxy(shower)

	def SettargetBoard(self, targetBoard):
		from _weakref import proxy
		self.uitargetBoard = proxy(targetBoard)

	## Show & Hide
	def ShowDefaultWindows(self):
		self.wndTaskBar.Show()
		self.wndMiniMap.Show()
		self.wndMiniMap.ShowMiniMap()
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Show()
		if self.wndGameButton:
			self.wndGameButton.Show()
	
		if self.wndMiniGame:
			self.wndMiniGame.show_mini_game_dialog()
	
		if self.uiAffectshower:
			self.uiAffectshower.Show()

		if self.wndParty:
			self.wndParty.Show()

		if self.wndPetInfoWindow:
			if self.wndPetInfoWindow.wndPetMiniInfo:
				if not playerm2g2.GetActivePetItemId() == 0:
					self.wndPetInfoWindow.wndPetMiniInfo.Show()
														
		if app.ENABLE_USER_SITUATION_NOTICE:
			if self.wndUserSituationNotice:
				self.wndUserSituationNotice.Show()
				
		self.IsHideUiMode = False
		
	def IsHideUiMode(self):
		return self.IsHideUiMode

	def ShowAllWindows(self):
		self.wndTaskBar.Show()
		self.wndCharacter.Show()
		self.wndInventory.Show()
		self.wndDragonSoul.Show()
		self.wndDragonSoulRefine.Show()
		self.wndChat.Show()
		self.wndMiniMap.Show()
		
		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Show()
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Show()
			if self.wnd12ziReward:
				self.wnd12ziReward.Show()
				
		if self.wndEnergyBar:
			self.wndEnergyBar.Show()
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Show()
			self.wndExpandedTaskBar.SetTop()
		
		if app.ENABLE_GEM_SYSTEM:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()

	def HideAllWindows(self):
		if self.wndParty:
			self.wndParty.Hide()

		if self.uiAffectshower:
			self.uiAffectshower.Hide()
		
		if self.uitargetBoard:
			self.uitargetBoard.Hide()
	
		if self.wndMiniGame:
			self.wndMiniGame.hide_mini_game_dialog()

		if self.wndTaskBar:
			self.wndTaskBar.Hide()

		if self.wndGameButton:
			self.wndGameButton.Hide()
		
		if self.wndEnergyBar:
			self.wndEnergyBar.Hide()

		if app.ENABLE_DETAILS_UI:
			if self.wndCharacter:
				self.wndCharacter.Close()
		else:
			if self.wndCharacter:
				self.wndCharacter.Hide()

		if self.wndInventory:
			self.wndInventory.Hide()
			
		self.wndDragonSoul.Hide()
		self.wndDragonSoulRefine.Hide()
			
		if app.ENABLE_GROWTH_PET_SYSTEM: 	
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.Hide()
				if self.wndPetInfoWindow.wndPetMiniInfo:
					self.wndPetInfoWindow.wndPetMiniInfo.Hide()
				
		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				self.wndAutoWindow.Hide()

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Hide()
				
		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				self.wndBattleField.Hide()
		
		if app.ENABLE_12ZI:
			if self.wndBead:
				self.wndBead.Hide()
			if self.wnd12ziTimer:
				self.wnd12ziTimer.Hide()
			if self.wnd12ziReward:
				self.wnd12ziReward.Hide()
				
		if self.wndChat:
			self.wndChat.hide_btnChatSizing()
			self.wndChat.Hide()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()

		if self.wndMessenger:
			self.wndMessenger.Hide()

		if self.wndGuild:
			self.wndGuild.Hide()
			
		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()

		if app.ENABLE_GEM_SYSTEM:
			if self.wndExpandedMoneyTaskBar:
				self.wndExpandedMoneyTaskBar.Hide()
 
		if self.wndSkillBookCombination:
			self.wndSkillBookCombination.Hide()

		if app.ENABLE_CHANGED_ATTR :
			if self.wndSelectAttr:
				self.wndSelectAttr.Hide()

		if app.ENABLE_MONSTER_CARD:
			if self.wndMonsterCardWindow:
				self.wndMonsterCardWindow.Hide()
				
		if app.ENABLE_MYSHOP_DECO :
			if self.wndMyShopDeco :
				self.wndMyShopDeco.Hide()
		
		if app.ENABLE_USER_SITUATION_NOTICE:
			if self.wndUserSituationNotice:
				self.wndUserSituationNotice.Hide()
				
		if app.ENABLE_PARTY_MATCH:
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.Hide()

		self.IsHideUiMode = True
				
	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			# 웹페이지가 열렸을때는 채팅 입력이 안됨
			if self.wndWeb and self.wndWeb.IsShow():
				pass
			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.ENABLE_BATTLE_FIELD:
		def OpenRestartDialog(self, mapidx):
			self.dlgRestart.OpenDialog(mapidx)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()
		
	if app.ENABLE_12ZI:
		def OpenUI12zi(self, yellowmark, greenmark, yellowreward, greenreward, goldreward):
			if self.wnd12ziReward == None:
				self.wnd12ziReward = ui12zi.Reward12ziWindow()
			self.wnd12ziReward.Open(yellowmark, greenmark, yellowreward, greenreward, goldreward)
		
		def Refresh12ziTimer(self, currentFloor, jumpCount, limitTime, elapseTime):
			if self.wndMiniMap:
				self.wndMiniMap.Hide()
				
			if self.wnd12ziTimer == None:
				self.wnd12ziTimer = ui12zi.FloorLimitTimeWindow()
				
			self.wnd12ziTimer.Refresh12ziTimer(currentFloor, jumpCount, limitTime, elapseTime)
			self.wnd12ziTimer.Open()
				
		def Show12ziJumpButton(self):
			self.wnd12ziTimer.Show12ziJumpButton()
		
		def Hide12ziTimer(self):
			self.wnd12ziTimer.Hide()
			
		def RefreshShopItemToolTip(self):
			if self.tooltipItem:
				self.tooltipItem.RefreshShopToolTip()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			if self.wndGuildBuilding:
				self.wndGuildBuilding.Close()	
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					if app.ENABLE_DETAILS_UI:
						self.wndCharacter.Close()
					else:
						self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == playerm2g2.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	def ToggleInventoryWindow(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()

	def ShowCostumeInventory(self) :
		if not playerm2g2.IsObserverMode() and self.wndInventory.IsShow():
			self.wndInventory.ShowCostumeInventory()
	
	def ToggleExpandedButton(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()
		
		if app.ENABLE_GEM_SYSTEM:
			##self.wndExpandedMoneyTaskBar.LoadWindow()
			pass
	
	if app.ENABLE_GEM_SYSTEM:
		def ToggleExpandedMoneyButton(self):
			if False == self.wndExpandedMoneyTaskBar.IsShow():
				self.wndExpandedMoneyTaskBar.Show()
				self.wndExpandedMoneyTaskBar.SetTop()
			else:
				self.wndExpandedMoneyTaskBar.Close()
	
	# wj.2014.12.2. 인벤토리와 DS인벤 간의 상태를 확인 및 설정하기 위한 함수.			
	def IsShowDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			return True
		elif self.wndDragonSoul.IsDlgQuestionShow():
			return True
		else:
			return False
	
	def CloseDlgQuestionWindow(self):
		if self.wndInventory.IsDlgQuestionShow():
			self.wndInventory.CancelDlgQuestion()
		if self.wndDragonSoul.IsDlgQuestionShow():
			self.wndDragonSoul.CancelDlgQuestion()
	
	def SetUseItemMode(self, bUse):
		self.wndInventory.SetUseItemMode(bUse)
		self.wndDragonSoul.SetUseItemMode(bUse)
	
	# 용혼석
	def DragonSoulActivate(self, deck):
		self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def DragonSoulDeactivate(self):
		self.wndDragonSoul.DeactivateDragonSoul()
		
	def Highligt_Item(self, inven_type, inven_pos):
		if playerm2g2.DRAGON_SOUL_INVENTORY == inven_type:
			self.wndDragonSoul.HighlightSlot(inven_pos)
		elif app.WJ_ENABLE_PICKUP_ITEM_EFFECT and playerm2g2.INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)
			
	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndDragonSoul.IsShow():
				if app.ENABLE_DS_PASSWORD:
					self.wndDragonSoul.Open()
				else:
					self.wndDragonSoul.Show()
		
	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == playerm2g2.IsObserverMode():
			if False == self.wndDragonSoul.IsShow():
				if app.ENABLE_DS_PASSWORD:
					self.wndDragonSoul.Open()
				else:
					self.wndDragonSoul.Show()
			else:
				self.wndDragonSoul.Close()
				
	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == playerm2g2.IsObserverMode():
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == playerm2g2.IsObserverMode():
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if app.ENABLE_DS_PASSWORD:
			self.wndDragonSoulRefine.WindowStartPos()
			
		if False == playerm2g2.IsObserverMode():
			if False == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.Show()
				if None != self.wndDragonSoul:
					if False == self.wndDragonSoul.IsShow():
						self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == playerm2g2.IsObserverMode():
			if True == self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.Close()

	if app.ENABLE_DS_PASSWORD:
		def AskDSRefinePassword(self):
			if self.wndDragonSoul.IsShow():
				return
			self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
			self.dlgPassword.SetSendMessage("/ds_refine_password ")
			self.dlgPassword.ShowDialog()
		
		def ResetDSActiveButton(self):
			self.wndDragonSoul.DeactivateDragonSoul()
		
		def AskDSPassword(self):
			if self.wndDragonSoul.IsShow():
				return
			self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
			self.dlgPassword.SetSendMessage("/ds_password ")
			self.dlgPassword.ShowDialog()
		
		def OpenDSInventory(self):
			self.wndDragonSoul.Show()
			
		def CloseDSInventory(self):
			self.wndDragonSoul.CloseDSInventory()
	# 용혼석 끝
	
	
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetInformationActivate(self):
			self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_PET_INFO, uiScriptLocale.TASKBAR_PET_INFO)
	
	if app.ENABLE_GROWTH_PET_SYSTEM:	
		def TogglePetInformationWindow(self):
			if False == playerm2g2.IsObserverMode():
				if not self.wndPetInfoWindow.IsShow():
					self.wndPetInfoWindow.Show()
				else:
					self.wndPetInfoWindow.Close()

	if app.ENABLE_AUTO_SYSTEM:
		def ToggleAutoWindow(self):
			if False == playerm2g2.IsObserverMode():
				if not self.wndAutoWindow.IsShow():
					if app.ENABLE_PVP_TOURNAMENT_GF:
						if (m2netm2g.GetMapIndex() == m2netm2g.PVP_TOURNAMENT_MAP_INDEX) and (self.pvp_tournament_auto_OnOff == 0):
							chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PVP_TOURNAMENT_DO_NOT_AUTO)
							return
						else:
							self.wndAutoWindow.Show()
					else:
						self.wndAutoWindow.Show()
				else:
					self.wndAutoWindow.Close()

		def SetAutoCooltime(self, slotindex, cooltime):
			self.wndAutoWindow.SetAutoCooltime(slotindex, cooltime)
			
		def SetCloseGame(self):
			self.wndAutoWindow.SetCloseGame()
			
		def GetAutoStartonoff(self):
			return self.wndAutoWindow.GetAutoStartonoff()

		def RefreshAutoSkillSlot(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.RefreshAutoSkillSlot()
		
		def RefreshAutoPositionSlot(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.RefreshAutoPositionSlot()
				
		def AutoOff(self):
			if self.wndAutoWindow:
				self.wndAutoWindow.AutoOnOff(0,self.wndAutoWindow.AUTO_ONOFF_START,1,True)
			if self.wndExpandedTaskBar:
				self.wndExpandedTaskBar.EnableAutoButton(False)

		def AutoOn(self):
			if self.wndExpandedTaskBar:
				self.wndExpandedTaskBar.EnableAutoButton(True)

				
	if app.ENABLE_RANKING_SYSTEM and app.ENABLE_BATTLE_FIELD:
		def OpenRankingBoardWindow(self, type, category):
			if self.wndBattleField and type == 0 and category == 0:
				self.wndBattleField.Open()
			elif app.ENABLE_RANKING_SYSTEM_PARTY and self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Open(type,category)
				
	elif app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY and not app.ENABLE_BATTLE_FIELD:
		def OpenRankingBoardWindow(self, type, category):
			if self.wndRankingBoardWindow:
				self.wndRankingBoardWindow.Open(type,category)
					
	if app.ENABLE_MONSTER_CARD:
		def ToggleMonsterCardWindow(self):
			if False == playerm2g2.IsObserverMode() and self.wndMonsterCardWindow:
				if not self.wndMonsterCardWindow.IsShow():
					self.wndMonsterCardWindow.Show()
				else:
					self.wndMonsterCardWindow.Close()
					
	if app.ENABLE_PARTY_MATCH:
		def TogglePartyMatchWindow(self):
			if False == playerm2g2.IsObserverMode() and self.wndPartyMatchWindow:
				if not self.wndPartyMatchWindow.IsShow():
					self.wndPartyMatchWindow.Show()
				else:
					self.wndPartyMatchWindow.Close()

	def ToggleGuildWindow(self):
	
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			if not self.wndGuild.CanOpen():
				if self.wndGuild.GuildListDialogIsShow():
					self.wndGuild.CloseGuildListDialog()
				else:
					self.wndGuild.OpenGuildListDialog()
				return
	
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	def __OnClickHelpButton(self):
		playerm2g2.SetPlayTime(1)
		self.CheckGameButton()
		self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()
		
	if app.ENABLE_KEYCHANGE_SYSTEM:
		def ToggleHelpWindow(self):
			if self.wndHelp.IsShow():
				self.CloseHelpWindow()
			else:
				self.OpenHelpWindow()

	def OpenHelpWindow(self):
		self.wndHelp.Open()
		if app.ENABLE_HELP_RENEWAL:
			if self.wndTaskBar.LeftMouseButtonIsShow():
				self.wndTaskBar.ToggleLeftMouseButtonModeWindow()

			if self.wndTaskBar.RightMouseButtonIsShow():
				self.wndTaskBar.ToggleRightMouseButtonModeWindow()

			self.wndTaskBar.ToggleLeftMouseButtonModeWindow()
			self.wndTaskBar.ToggleRightMouseButtonModeWindow()
		else:
			self.wndUICurtain.Show()

	def CloseHelpWindow(self):
		self.wndHelp.Close()
		if app.ENABLE_HELP_RENEWAL:
			self.wndTaskBar.ToggleLeftMouseButtonModeWindow()
			self.wndTaskBar.ToggleRightMouseButtonModeWindow()
		else:
			self.wndUICurtain.Hide()

	def OpenWebWindow(self, url):
		if app.ENABLE_STEAM and app.GetLoginType() == app.LOGIN_TYPE_STEAM:
			if app.ShowOverlayWebPage(url):
				return

		self.wndWeb.Open(url)
		# 웹페이지를 열면 채팅을 닫는다
		self.wndChat.CloseChat()

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()

	def OpenCubeWindow(self):
		self.wndCube.Open()

		if FALSE == self.wndInventory.IsShow():
			self.wndInventory.Show()

	def UpdateCubeInfo(self, gold, itemVnum, count):
		self.wndCube.UpdateInfo(gold, itemVnum, count)

	def CloseCubeWindow(self):
		self.wndCube.Close()

	def FailedCubeWork(self):
		self.wndCube.Refresh()

	def SucceedCubeWork(self, itemVnum, count):
		self.wndCube.Clear()
		
		print "큐브 제작 성공! [%d:%d]" % (itemVnum, count)

		if 0: # 결과 메시지 출력은 생략 한다
			self.wndCubeResult.SetPosition(*self.wndCube.GetGlobalPosition())
			self.wndCubeResult.SetCubeResultItem(itemVnum, count)
			self.wndCubeResult.Open()
			self.wndCubeResult.SetTop()

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.dlgSystem:
			hideWindows += self.dlgSystem,
		
		if self.wndMiniGame:
			hideWindows += self.wndMiniGame,
						
		if self.wndEnergyBar:
			hideWindows += self.wndEnergyBar,
			
		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,
			
		if app.ENABLE_GEM_SYSTEM:
			if self.wndExpandedMoneyTaskBar:
				hideWindows += self.wndExpandedMoneyTaskBar,
			
		hideWindows += self.wndDragonSoul,\
					self.wndDragonSoulRefine,
						
		if app.ENABLE_GROWTH_PET_SYSTEM:
			if self.wndPetInfoWindow:
				hideWindows += self.wndPetInfoWindow,
				
		if app.ENABLE_AUTO_SYSTEM:
			if self.wndAutoWindow:
				hideWindows += self.wndAutoWindow,
				
		if app.ENABLE_MONSTER_CARD:
			if self.wndMonsterCardWindow:
				hideWindows += self.wndMonsterCardWindow,

		if app.ENABLE_RANKING_SYSTEM and app.ENABLE_RANKING_SYSTEM_PARTY:
			if self.wndRankingBoardWindow:
				hideWindows += self.wndRankingBoardWindow,
				
		if app.ENABLE_BATTLE_FIELD:
			if self.wndBattleField:
				hideWindows += self.wndBattleField,
		
		if app.ENABLE_12ZI:
			if self.wndBead:
				hideWindows += self.wndBead,
			if self.wnd12ziTimer:
				hideWindows += self.wnd12ziTimer,
			if self.wnd12ziReward:
				hideWindows += self.wnd12ziReward,
				
		if app.ENABLE_MYSHOP_DECO:
			if self.wndMyShopDeco:
				hideWindows += self.wndMyShopDeco,
				
		if app.ENABLE_PARTY_MATCH:
			if self.wndPartyMatchWindow:
				hideWindows += self.wndPartyMatchWindow,
				
		if app.ENABLE_USER_SITUATION_NOTICE:
			if self.wndUserSituationNotice:
				hideWindows += self.wndUserSituationNotice,
				
		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)
		import sys

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
			
		if self.dlgSystem:
			self.dlgSystem.HideAllSystemOptioin()
		self.wndMiniMap.AtlasWindow.Hide()
	
		if self.wndWeb:
			self.wndWeb.CloseWhenOpenQuest()

		return hideWindows

	def __ShowWindows(self, wnds):
		import sys
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

		if self.dlgSystem:
			self.dlgSystem.ShowAllSystemOptioin()
			
		if self.wndMiniMap.AtlasWindow and self.wndMiniMap.AtlasWindow.IsShowWindow():
			self.wndMiniMap.AtlasWindow.Show()
	
		if self.wndWeb:
			self.wndWeb.OpenWhenOpenQuest()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		def BINARY_SetObserverMode(self, flag, isbuttonshow):
			self.wndGameButton.SetObserverMode(flag,isbuttonshow)
	else:
		def BINARY_SetObserverMode(self, flag):
			self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
	
	if app.ENABLE_GEM_SYSTEM:
		def BINARY_OpenSelectItemWindowEx(self):
			self.wndItemSelectEx.Open()
		def BINARY_RefreshSelectItemWindowEx(self):
			self.wndItemSelectEx.RefreshSlot()

	#####################################################################################
	### Private Shop ###

	if app.ENABLE_MYSHOP_DECO:
		def OpenMyShopDecoWnd(self):
			
			if self.inputDialog :
				return
				
			if self.privateShopBuilder.IsShow() :
				return
			
			if self.wndMyShopDeco:
				self.wndMyShopDeco.Open()
			else:
				#print "[KN] wndMyShopDecon None"
				return

	if app.ENABLE_CHEQUE_SYSTEM and app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopInputNameDialog(self, bCashItem, tabCnt):
	
			if self.wndMyShopDeco.IsShow() :
				return
			
			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return
			
			if self.wndSkillBookCombination.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
				return

			if app.ENABLE_CHANGED_ATTR :
				if self.wndSelectAttr.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				shop.SetNameDialogOpen(True)
			inputDialog = uiCommon.InputDialog()
			inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
			inputDialog.SetMaxLength(32)
			inputDialog.SetUseCodePage(False)	#MT-679 개인 상점 타이틀의 CodePage 이슈
			inputDialog.SetAcceptEvent(lambda arg = bCashItem, arg1 = tabCnt : ui.__mem_func__(self.OpenPrivateShopBuilder)(arg, arg1))	
			inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog
	
	elif app.ENABLE_CHEQUE_SYSTEM and not app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopInputNameDialog(self, bCashItem):
			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return
			
			if self.wndSkillBookCombination.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
				return

			if app.ENABLE_CHANGED_ATTR :
				if self.wndSelectAttr.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				shop.SetNameDialogOpen(True)
			inputDialog = uiCommon.InputDialog()
			inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
			inputDialog.SetMaxLength(32)
			inputDialog.SetAcceptEvent(lambda arg = bCashItem : ui.__mem_func__(self.OpenPrivateShopBuilder)(arg))	
			inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog	
	else:
		def OpenPrivateShopInputNameDialog(self):
			#if playerm2g2.IsInSafeArea():
			#	chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.CANNOT_OPEN_PRIVATE_SHOP_IN_SAFE_AREA)
			#	return

			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return
			
			if self.wndSkillBookCombination.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
				return

			if app.ENABLE_CHANGED_ATTR :
				if self.wndSelectAttr.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				shop.SetNameDialogOpen(True)
			inputDialog = uiCommon.InputDialog()
			inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
			inputDialog.SetMaxLength(32)
			inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
			inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
			inputDialog.Open()
			self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		if app.ENABLE_CHANGE_LOOK_SYSTEM:
			shop.SetNameDialogOpen(False)
		return True

	if app.ENABLE_CHEQUE_SYSTEM and app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopBuilder(self, bCashItem, tabCnt):
			if not self.inputDialog:
				return True

			if not len(self.inputDialog.GetText()):
				return True
				
			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if self.wndSkillBookCombination.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
				return

			if app.ENABLE_CHANGED_ATTR :
				if self.wndSelectAttr.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			self.privateShopBuilder.Open(self.inputDialog.GetText())
			self.privateShopBuilder.SetIsCashItem(bCashItem)
			self.privateShopBuilder.SetTabCount(tabCnt)
			self.ClosePrivateShopInputNameDialog()

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				shop.SetNameDialogOpen(True)

			return True
			
	elif app.ENABLE_CHEQUE_SYSTEM and not app.ENABLE_MYSHOP_DECO:
		def OpenPrivateShopBuilder(self, bCashItem):
			if not self.inputDialog:
				return True

			if not len(self.inputDialog.GetText()):
				return True
				
			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if self.wndSkillBookCombination.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
				return

			if app.ENABLE_CHANGED_ATTR :
				if self.wndSelectAttr.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			self.privateShopBuilder.Open(self.inputDialog.GetText())
			self.privateShopBuilder.SetIsCashItem(bCashItem)
			self.ClosePrivateShopInputNameDialog()

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				shop.SetNameDialogOpen(True)

			return True	
	else:
		def OpenPrivateShopBuilder(self):

			if not self.inputDialog:
				return True

			if not len(self.inputDialog.GetText()):
				return True
				
			if app.ENABLE_GROWTH_PET_SYSTEM:
				pet_id = playerm2g2.GetActivePetItemId()
				if pet_id:
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.PET_CAN_NOT_OPEN_SHOP_BECAUSE_SUMMON)
					return

			if self.wndSkillBookCombination.IsShow() :
				chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.COMB_NOTICE)
				return

			if app.ENABLE_CHANGED_ATTR :
				if self.wndSelectAttr.IsShow() :
					chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, localeInfo.SELECT_ATTR_NOTICE)
					return

			self.privateShopBuilder.Open(self.inputDialog.GetText())
			self.ClosePrivateShopInputNameDialog()

			if app.ENABLE_CHANGE_LOOK_SYSTEM:
				shop.SetNameDialogOpen(True)

			return True

	if app.ENABLE_MYSHOP_DECO:
		def AppearPrivateShop(self, vid, text, type):
			
			board = None
			
			if type == 0:
				board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
				board.Open(vid, text)
			else:
				board = uiPrivateShopBuilder.PrivateShopTitleBar(type)
				board.Open(vid, text)

			self.privateShopAdvertisementBoardDict[vid] = board	
	else:
		def AppearPrivateShop(self, vid, text):
			board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
			board.Open(vid, text)

			self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):

		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	if app.ENABLE_CHANGE_LOOK_SYSTEM:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count, dwChangeLookVnum):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count, dwChangeLookVnum)
	else:
		def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
			if not vid in self.equipmentDialogDict:
				return
			self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###	
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)		
	
	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):

		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		##!! 20061026.levites.퀘스트_이미지_교체
		import item
		
		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if "item"==iconType:
				item.SelectItem(int(iconName))
				buttonImageFileName=item.GetIconImageFileName()
			elif "blue_quest" == iconType:
				buttonImageFileName=localeInfo.GetBlueLetterImageName()
			else:
				buttonImageFileName=iconName
		else:
			if "item"==iconType:
				item.SelectItem(int(iconName))
				buttonImageFileName=item.GetIconImageFileName()
			else:
				buttonImageFileName=iconName

		if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
			if localeInfo.IsEUROPE():
				if "highlight" == iconType:
					btn.SetUpVisual("locale/ymir_ui/highlighted_quest.tga")
					btn.SetOverVisual("locale/ymir_ui/highlighted_quest_r.tga")
					btn.SetDownVisual("locale/ymir_ui/highlighted_quest_r.tga")
				elif "blue_quest" == iconType:
					btn.SetUpVisual(localeInfo.GetBlueLetterCloseImageName())
					btn.SetOverVisual(localeInfo.GetBlueLetterOpenImageName())
					btn.SetDownVisual(localeInfo.GetBlueLetterOpenImageName())
				else:
					btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
					btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
					btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		else:
			if localeInfo.IsEUROPE():
				if "highlight" == iconType:
					btn.SetUpVisual("locale/ymir_ui/highlighted_quest.tga")
					btn.SetOverVisual("locale/ymir_ui/highlighted_quest_r.tga")
					btn.SetDownVisual("locale/ymir_ui/highlighted_quest_r.tga")
				else:
					btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
					btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
					btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
			else:
				btn.SetUpVisual(buttonImageFileName)
				btn.SetOverVisual(buttonImageFileName)
				btn.SetDownVisual(buttonImageFileName)
				btn.Flash()
		# END_OF_QUEST_LETTER_IMAGE

		if localeInfo.IsARABIC():
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignRight()
		else:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()
			
		btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
		btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

		#chatm2g.AppendChat(chatm2g.CHAT_TYPE_NOTICE, localeInfo.QUEST_APPEND)

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		##!! 20061026.levites.퀘스트_위치_보정
		if self.wndParty.IsShow():
			xPos = 100 + 30
		else:
			xPos = 20

		if localeInfo.IsARABIC():
			xPos = xPos + 15

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1
			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				btn.Show()

	def __StartQuest(self, btn):
		event.QuestButtonClick(btn.index)
		self.__DestroyQuestButton(btn)

	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
	#####################################################################################

	#####################################################################################
	### Whisper ###

	def __InitWhisper(self):
		from _weakref import proxy
		chatm2g.InitWhisper(proxy(self))

	## 채팅창의 "메시지 보내기"를 눌렀을때 이름 없는 대화창을 여는 함수
	## 이름이 없기 때문에 기존의 WhisperDialogDict 와 별도로 관리된다.
	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	## 이름 없는 대화창에서 이름을 결정했을때 WhisperDialogDict에 창을 넣어주는 함수
	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	## 캐릭터 메뉴의 1:1 대화 하기를 눌렀을때 이름을 가지고 바로 창을 여는 함수
	def OpenWhisperDialog(self, name):
		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	## 다른 캐릭터로부터 메세지를 받았을때 일단 버튼만 띄워 두는 함수
	def RecvWhisper(self, name):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name)
				btn.Flash()

				chatm2g.AppendChat(chatm2g.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()
		elif self.IsGameMasterName(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	## 버튼을 눌렀을때 창을 여는 함수
	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		## 버튼 초기화
		self.__DestroyWhisperButton(btn)

	## WhisperDialog 창에서 최소화 명령을 수행했을때 호출되는 함수
	## 창을 최소화 합니다.
	def MinimizeWhisperDialog(self, name):

		if 0 != name:
			self.__MakeWhisperButton(name)

		self.CloseWhisperDialog(name)

	## WhisperDialog 창에서 닫기 명령을 수행했을때 호출되는 함수
	## 창을 지웁니다.
	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	## 버튼의 개수가 바뀌었을때 버튼을 재정렬 하는 함수
	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	## 이름으로 Whisper 버튼을 찾아 리턴해 주는 함수
	## 버튼은 딕셔너리로 하지 않는 것은 정렬 되어 버려 순서가 유지 되지 않으며
	## 이로 인해 ToolTip들이 다른 버튼들에 의해 가려지기 때문이다.
	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	## 창을 만듭니다.
	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	## 버튼을 만듭니다.
	def __MakeWhisperButton(self, name):
		whisperButton = uiWhisper.WhisperButton()
		whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)
		
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			if self.wndGuildBuilding.IsPositionChangeMode():
				self.wndGuildBuilding.ChangeWindowUpdate()

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
				if self.wndGuildBuilding.IsPositionChangeMode():
					self.wndGuildBuilding.EndPositionChangeMode()
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = playerm2g2.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != playerm2g2.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	#####################################################################################

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	def EmptyFunction(self):
		pass
	
	if app.WJ_ENABLE_TRADABLE_ICON or app.ENABLE_MOVE_COSTUME_ATTR or app.ENABLE_GROWTH_PET_SYSTEM or app.ENABLE_FISH_EVENT:
	
		if app.ENABLE_EXTEND_INVEN_SYSTEM:
			def AttachInvenItemToOtherWindowSlot(self, slotIndex, slotWindow):
					
				if app.ENABLE_MOVE_COSTUME_ATTR:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_ITEM_COMB and self.wndItemCombination and self.wndItemCombination.IsShow():
						self.wndItemCombination.AttachToCombinationSlot(slotWindow, slotIndex)
						return True
						
				if app.ENABLE_GROWTH_PET_SYSTEM:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_PET_FEED and playerm2g2.IsOpenPetFeedWindow() == True:
						if self.wndInventory:
							self.wndInventory.ItemMoveFeedWindow(slotWindow, slotIndex)
							return True
				
				return False
		else:
			def AttachInvenItemToOtherWindowSlot(self, slotIndex):
					
				if app.ENABLE_MOVE_COSTUME_ATTR:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_ITEM_COMB and self.wndItemCombination and self.wndItemCombination.IsShow():
						self.wndItemCombination.AttachToCombinationSlot(playerm2g2.INVENTORY, slotIndex)
						return True
						
				if app.ENABLE_GROWTH_PET_SYSTEM:
					if self.GetOnTopWindow() == playerm2g2.ON_TOP_WND_PET_FEED and playerm2g2.IsOpenPetFeedWindow() == True:
						if self.wndInventory:
							self.wndInventory.ItemMoveFeedWindow(playerm2g2.INVENTORY, slotIndex)
							return True
				
				return False
				
		def MarkUnusableInvenSlotOnTopWnd(self, onTopWnd, InvenSlot):
			if app.WJ_ENABLE_TRADABLE_ICON:
				if onTopWnd == playerm2g2.ON_TOP_WND_SHOP and self.dlgShop and self.dlgShop.CantSellInvenItem(InvenSlot):
					return True
				elif onTopWnd == playerm2g2.ON_TOP_WND_SAFEBOX and self.wndSafebox and self.wndSafebox.CantCheckInItem(InvenSlot):
					return True
				elif onTopWnd == playerm2g2.ON_TOP_WND_PRIVATE_SHOP and self.privateShopBuilder and self.privateShopBuilder.CantTradableItem(InvenSlot):
					return True
				elif onTopWnd == playerm2g2.ON_TOP_WND_EXCHANGE and self.dlgExchange and self.dlgExchange.CantTradableItem(InvenSlot):
					return True
			
			if app.ENABLE_MOVE_COSTUME_ATTR:
				if onTopWnd == playerm2g2.ON_TOP_WND_ITEM_COMB and self.wndItemCombination and self.wndItemCombination.CantAttachToCombSlot(InvenSlot):
					return True
					
			if app.ENABLE_GROWTH_PET_SYSTEM:
				if onTopWnd == playerm2g2.ON_TOP_WND_PET_FEED and self.wndPetInfoWindow and self.wndPetInfoWindow.CantFeedItem(InvenSlot):
					return True
					
			if app.ENABLE_FISH_EVENT:
				if onTopWnd == playerm2g2.ON_TOP_WND_FISH_EVENT and self.wndMiniGame and self.wndMiniGame.CantFishEventSlot(InvenSlot):
					return True
			
			return False
			
		def SetOnTopWindow(self, onTopWnd):
			self.OnTopWindow = onTopWnd
			
		def GetOnTopWindow(self):
			return self.OnTopWindow
		
		def RefreshMarkInventoryBag(self):
			if self.wndInventory and self.wndInventory.IsShow():
				self.wndInventory.RefreshBagSlotWindow()
	
				
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetHatchingWindowCommand(self, command, window, pos):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetHatching:
					self.wndPetInfoWindow.wndPetHatching.PetHatchingWindowCommand(command, window, pos)
		
		def PetNameChangeWindowCommand(self, command, srcWindow, srcPos, dstWindow, dstPos):
			if self.wndPetInfoWindow:
				if self.wndPetInfoWindow.wndPetNameChange:
					self.wndPetInfoWindow.wndPetNameChange.PetNameChangeWindowCommand(command, srcWindow, srcPos, dstWindow, dstPos)
			
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetSkillUpgradeDlgOpen(self, slot, index, gold):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.OpenPetSkillUpGradeQuestionDialog(slot, index, gold)
				
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetFlashEvent(self, index):
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFlashEvent(index)

	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetInfoBindAffectShower(self, affect_shower):
		
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetInfoBindAffectShower(affect_shower)
				
	
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetAffectShowerRefresh(self):
			
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetAffectShowerRefresh()
	
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetEvolInfo(self, index, value):
		
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetEvolInfo(index, value)
				
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def PetFeedReuslt(self, result):
			
			if self.wndPetInfoWindow:
				self.wndPetInfoWindow.PetFeedReuslt(result)
					
	if app.ENABLE_EXTEND_INVEN_SYSTEM:
		def ExInvenItemUseMsg(self, item_vnum, msg, enough_count):
			self.wndInventory.ExInvenItemUseMsg(item_vnum, msg, enough_count)
				
	def MiniGameOkey(self):
	
		isOpen = playerm2g2.GetMiniGameWindowOpen()
		
		if isOpen == True:
			if not self.wndMiniGame:
				self.wndMiniGame = uiMiniGame.MiniGameWindow()
			
			self.wndMiniGame.MiniGameOkeyEvent(True)
		else:
			if self.wndMiniGame:
				self.wndMiniGame.MiniGameOkeyEvent(False)
		
	def MiniGameStart(self):
		self.wndMiniGame.MiniGameStart()
		
	def RumiMoveCard(self, srcCard, dstCard):
		self.wndMiniGame.RumiMoveCard( srcCard, dstCard )
		
	def MiniGameRumiSetDeckCount(self, deck_card_count):
		self.wndMiniGame.MiniGameRumiSetDeckCount(deck_card_count)
		
	def RumiIncreaseScore(self, score, total_score):
		self.wndMiniGame.RumiIncreaseScore(score, total_score)
		
	def MiniGameEnd(self):
		self.wndMiniGame.MiniGameEnd()
			
	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		def RefreshGuildRankingList(self, issearch):
			if self.wndGuild:
				self.wndGuild.RefreshGuildRankingList(issearch)

		def CloseGuildRankWindow(self):
			if self.wndGuild:
				self.wndGuild.CloseGuildListDialog()
				
		def ShowGuildWarButton(self):
			if self.wndGameButton:
				self.wndGameButton.ShowGuildWarButton()
		
		def HideGuildWarButton(self):
			if self.wndGameButton:
				self.wndGameButton.HideGuildWarButton()
				
	
	if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016 or app.ENABLE_MINI_GAME_OKEY_NORMAL or app.ENABLE_FISH_EVENT or app.ENABLE_MINI_GAME_YUTNORI:
		def IntegrationEventBanner(self):
			isOpen = []
			
			if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
				isOpen.append( playerm2g2.GetAttendance() )
				
			if app.ENABLE_MONSTER_BACK and app.ENABLE_ACCUMULATE_DAMAGE_DISPLAY:
				isOpen.append( playerm2g2.GetMonsterBackEvent() )
				
			if app.ENABLE_MINI_GAME_OKEY_NORMAL:
				isOpen.append( playerm2g2.GetMiniGameWindowOpen() )
				
			if app.ENABLE_FISH_EVENT:
				isOpen.append( playerm2g2.GetFishEventGame() )
				
			if app.ENABLE_MINI_GAME_YUTNORI:
				isOpen.append( playerm2g2.GetYutnoriGame() )
				
			if True in isOpen:
				if not self.wndMiniGame:
					self.wndMiniGame = uiMiniGame.MiniGameWindow()
					
					if app.ENABLE_FISH_EVENT:
						self.wndMiniGame.SetInven( self.wndInventory )
						self.wndMiniGame.BindInterface( self )
					if self.tooltipItem:
						self.wndMiniGame.SetItemToolTip(self.tooltipItem)
				
				self.wndMiniGame.IntegrationMiniGame(True)
			else:
				if self.wndMiniGame:
					self.wndMiniGame.IntegrationMiniGame(False)
			
		def Attendance(self):
		
			isOpen = playerm2g2.GetAttendance()
			
			if isOpen == True:
				if not self.wndMiniGame:
					self.wndMiniGame = uiMiniGame.MiniGameWindow()
					
					if self.tooltipItem:
						self.wndMiniGame.SetItemToolTip(self.tooltipItem) 
				
				self.wndMiniGame.MiniGameAttendance(True)
			else:
				if self.wndMiniGame:
					self.wndMiniGame.MiniGameAttendance(False)
		
		def MiniGameAttendanceSetData(self, type, value):
			if self.wndMiniGame:
				self.wndMiniGame.MiniGameAttendanceSetData( type, value )
				
		def MiniGameAttendanceRequestRewardList(self):
			if self.wndMiniGame:
				self.wndMiniGame.MiniGameAttendanceRequestRewardList()		
			
	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def SetOkeyNormalBG(self):
			if not self.wndMiniGame:
				return
				
			self.wndMiniGame.SetOkeyNormalBG()

	if app.ENABLE_MONSTER_CARD:
		def RefreshMissionPage(self):
			if self.wndMonsterCardWindow:
				self.wndMonsterCardWindow.RefreshMissionPage()

		def ReciveMission(self):
			if self.wndMonsterCardWindow:
				self.wndMonsterCardWindow.ReciveMission()
				
		def MonsterCardMissionFail(self, type, data):
			if self.wndMonsterCardWindow:
				self.wndMonsterCardWindow.MonsterCardMissionFail(type, data)
				
		def MonsterCardIllustrationFail(self, type, data):
			if self.wndMonsterCardWindow:
				self.wndMonsterCardWindow.MonsterCardIllustrationFail(type, data)
				
		def MonsterCardIllustrationRefresh(self):
			if self.wndMonsterCardWindow:
				self.wndMonsterCardWindow.MonsterCardIllustrationRefresh()
				
	if app.ENABLE_BATTLE_FIELD:	
		def RefrashBattleButton(self):
			if self.wndMiniMap:
				self.wndMiniMap.RefrashBattleButton()
				
		def SetBattleFieldLeftTime(self, leftOpen, leftEnd):
			if self.wndBattleField:
				self.wndBattleField.SetBattleFieldLeftTime(leftOpen, leftEnd)
	
		def ExitBattleField(self, point):
			if self.wndBattleField:
				self.wndBattleField.ExitQuestion(point)
				
		def ExitBattleFieldOnDead(self, point):
			if self.wndBattleField:
				self.wndBattleField.ExitOnDeadQuestion(point)
				
		def ResetUsedBP(self):
			if self.dlgShop:
				self.dlgShop.ResetUsedBP()
				
	if app.ENABLE_FISH_EVENT:
		def MiniGameFishUse(self, window, pos, shape):
			self.wndMiniGame.MiniGameFishUse( window, pos, shape )
			
		def MiniGameFishAdd(self, pos, shape):
			self.wndMiniGame.MiniGameFishAdd( pos, shape )
			
		def MiniGameFishReward(self, vnum):
			self.wndMiniGame.MiniGameFishReward( vnum )
			
		def MiniGameFishCount(self, count):
			self.wndMiniGame.MiniGameFishCount( count )	
			
	if app.ENABLE_MOVE_CHANNEL:
		def RefreshServerInfo(self):
			if self.wndMiniMap:
				self.wndMiniMap.RefreshServerInfo()
				
	if app.ENABLE_12ZI:
		def SetBeadCount(self, value):
			if self.wndBead:
				self.wndBead.SetBeadCount(value)
			
		def NextBeadUpdateTime(self, value):
			if self.wndBead:
				self.wndBead.NextBeadUpdateTime(value)
				
	if app.ENABLE_PARTY_MATCH:
		def PartyMatchResult(self, type, data):
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.PartyMatchResult(type, data)
				
		def PartyMatchOff(self, enable):
			if self.wndPartyMatchWindow:
				self.wndPartyMatchWindow.Off( enable )
			
			if self.wndExpandedTaskBar:
				self.wndExpandedTaskBar.PartyMatchOff( enable )
				
	if app.ENABLE_USER_SITUATION_NOTICE:
		def RefreshUserSituation(self):
			if self.wndUserSituationNotice:
				self.wndUserSituationNotice.RefreshUserSituation()
				
		def OpenUserSituationShow(self, data):
			if self.wndUserSituationNotice:
				self.wndUserSituationNotice.OpenUserSituationShow( data )
				
	if app.ENABLE_SPECIAL_GACHA:
		def ShowSpecialGachaAward(self, vnum, day, win, cell):
			if self.wndSpecialGacha:
				self.wndSpecialGacha.Show(vnum, day, win, cell)
			else:
				self.wndSpecialGacha = uiSpecialGacha.SpecialGachaAward()
				self.wndSpecialGacha.Show(vnum, day, win, cell)
				
	if app.ENABLE_PVP_TOURNAMENT_GF:
		def PvPTournamentAutoSet(self, OnOff):
			self.pvp_tournament_auto_OnOff = OnOff
						
	if app.ENABLE_MINI_GAME_YUTNORI:
		def YutnoriProcess(self, type, data):
			if self.wndMiniGame:
				self.wndMiniGame.YutnoriProcess(type, data)
										
if __name__ == "__main__":

	import app
	import wndMgr
	import systemSetting
	import mouseModule
	import grp
	import ui
	import localeInfo

	app.SetMouseHandler(mouseModule.mouseController)
	app.SetHairColorEnable(True)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	mouseModule.mouseController.Create()

	class TestGame(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)

			localeInfo.LoadLocaleData()
			playerm2g2.SetItemData(0, 27001, 10)
			playerm2g2.SetItemData(1, 27004, 10)

			self.interface = Interface()
			self.interface.MakeInterface()
			self.interface.ShowDefaultWindows()
			self.interface.RefreshInventory()
			#self.interface.OpenCubeWindow()

		def __del__(self):
			ui.Window.__del__(self)

		def OnUpdate(self):
			app.UpdateGame()

		def OnRender(self):
			app.RenderGame()
			grp.PopState()
			grp.SetInterfaceRenderState()

	game = TestGame()
	game.SetSize(systemSetting.GetWidth(), systemSetting.GetHeight())
	game.Show()

	app.Loop()
