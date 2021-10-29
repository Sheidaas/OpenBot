import ui
import uiScriptLocale
import wndMgr
import playerm2g2
import miniMap
import localeInfo
import m2netm2g
import app
import colorInfo
import constInfo
import background
if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
	import grp

if app.ENABLE_BATTLE_FIELD:
	import uiBattleField

if app.WJ_SHOW_PARTY_ON_MINIMAP:
	QUEST_TOOLTIP_COLOR = 0xfff2cb61

class MapTextToolTip(ui.Window):
	def __init__(self):			
		ui.Window.__init__(self)

		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetOutline()
		if app.WJ_SHOW_PARTY_ON_MINIMAP:
			if localeInfo.IsARABIC():
				textLine.SetHorizontalAlignLeft()
			else:
				textLine.SetHorizontalAlignRight()
		else:
			textLine.SetHorizontalAlignRight()
		textLine.Show()
		self.textLine = textLine

	def __del__(self):			
		ui.Window.__del__(self)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetTooltipPosition(self, PosX, PosY):
		if app.WJ_SHOW_PARTY_ON_MINIMAP:
			self.textLine.SetPosition(PosX - 5, PosY)
		else:
			if localeInfo.IsARABIC():
				w, h = self.textLine.GetTextSize()
				self.textLine.SetPosition(PosX - w - 5, PosY)
			else:
				self.textLine.SetPosition(PosX - 5, PosY)

	def SetTextColor(self, TextColor):
		self.textLine.SetPackedFontColor(TextColor)

	def GetTextSize(self):
		return self.textLine.GetTextSize()
	
	def SetHorizontalAlignLeft(self):
		if self.textLine:
			self.textLine.SetHorizontalAlignLeft()

class AtlasWindow(ui.ScriptWindow):

	class AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def __del__(self):
			ui.Window.__del__(self)

		def OnUpdate(self):
			miniMap.UpdateAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			fx = float(x)
			fy = float(y)
			miniMap.RenderAtlas(fx, fy)

		def HideAtlas(self):
			miniMap.HideAtlas()

		def ShowAtlas(self):
			miniMap.ShowAtlas()

	def __init__(self):
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Hide()
		if app.WJ_SHOW_NPC_QUEST_NAME:
			self.tooltipQuest = MapTextToolTip()
			self.tooltipQuest.SetTextColor(QUEST_TOOLTIP_COLOR)
			self.tooltipQuest.Hide()
		self.infoGuildMark = ui.MarkBox()
		self.infoGuildMark.Hide()
		self.AtlasMainWindow = None
		self.mapName = ""
		self.board = 0
		self.IsShowWindowValue = False

		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def SetMapName(self, mapName):
		if 949==app.GetDefaultCodePage():
			try:
				self.board.SetTitleName(localeInfo.MINIMAP_ZONE_NAME_DICT[mapName])
			except:
				pass

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AtlasWindow.py")
		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.LoadScript")

		try:
			self.board = self.GetChild("board")

		except:
			import exception
			exception.Abort("AtlasWindow.LoadWindow.BindObject")

		self.AtlasMainWindow = self.AtlasRenderer()
		self.board.SetCloseEvent(self.Close)
		self.AtlasMainWindow.SetParent(self.board)
		self.AtlasMainWindow.SetPosition(7, 30)
		self.tooltipInfo.SetParent(self.board)
		if app.WJ_SHOW_NPC_QUEST_NAME:
			self.tooltipQuest.SetParent(self.board)
		self.infoGuildMark.SetParent(self.board)
		self.SetPosition(wndMgr.GetScreenWidth() - 136 - 256 - 10 - 165, 78)
		self.Hide()

		miniMap.RegisterAtlasWindow(self)

	def Destroy(self):
		miniMap.UnregisterAtlasWindow()
		self.ClearDictionary()
		self.AtlasMainWindow = None
		self.tooltipAtlasClose = 0
		self.tooltipInfo = None
		if app.WJ_SHOW_NPC_QUEST_NAME:
			self.tooltipQuest = None
		self.infoGuildMark = None
		self.board = None

	def OnUpdate(self):

		if not self.tooltipInfo:
			return

		if not self.infoGuildMark:
			return

		self.infoGuildMark.Hide()
		self.tooltipInfo.Hide()
		if app.WJ_SHOW_NPC_QUEST_NAME:
			self.tooltipQuest.Hide()

		if False == self.board.IsIn():
			return

		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, iPosX, iPosY, dwTextColor, dwGuildID) = miniMap.GetAtlasInfo(mouseX, mouseY)

		if False == bFind:
			return

		if "empty_guild_area" == sName:
			sName = localeInfo.GUILD_EMPTY_AREA

		if app.WJ_SHOW_PARTY_ON_MINIMAP:
			splitsName = sName.split("|")
			isQuest = (len(splitsName)==2)
			if localeInfo.IsARABIC() and sName[-1].isalnum():
				if isQuest and len(splitsName[0])==0:
					self.tooltipInfo.SetText("(%s)%d, %d" % (uiScriptLocale.GUILD_BUILDING_POSITION, iPosX, iPosY))
				else:
					self.tooltipInfo.SetText("(%s)%d, %d" % (splitsName[0], iPosX, iPosY))
			else:
				if isQuest and len(splitsName[0])==0:
					self.tooltipInfo.SetText("%s(%d, %d)" % (uiScriptLocale.GUILD_BUILDING_POSITION, iPosX, iPosY))
				else:
					self.tooltipInfo.SetText("%s(%d, %d)" % (splitsName[0], iPosX, iPosY))
		else:
			if localeInfo.IsARABIC() and sName[-1].isalnum():
				self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))
			else:
				self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))		
			
		(x, y) = self.GetGlobalPosition()
		self.tooltipInfo.SetTooltipPosition(mouseX - x, mouseY - y)
		self.tooltipInfo.SetTextColor(dwTextColor)
		self.tooltipInfo.Show()
		self.tooltipInfo.SetTop()
		
		if app.WJ_SHOW_NPC_QUEST_NAME:
			if isQuest:
				self.tooltipQuest.SetText("%s" % splitsName[1])
				self.tooltipQuest.SetTooltipPosition(mouseX - x, mouseY - y + 15)
				self.tooltipQuest.Show()
				self.tooltipQuest.SetTop()
			

		if 0 != dwGuildID:
			textWidth, textHeight = self.tooltipInfo.GetTextSize()
			self.infoGuildMark.SetIndex(dwGuildID)
			self.infoGuildMark.SetPosition(mouseX - x - textWidth - 18 - 5, mouseY - y)
			self.infoGuildMark.Show()

	def Hide(self):
		if self.AtlasMainWindow:
			self.AtlasMainWindow.HideAtlas()
			self.AtlasMainWindow.Hide()
		ui.ScriptWindow.Hide(self)

	def Show(self):
		if self.AtlasMainWindow:
			(bGet, iSizeX, iSizeY) = miniMap.GetAtlasSize()
			if bGet:
				self.SetSize(iSizeX + 15, iSizeY + 38)

				if localeInfo.IsARABIC():
					self.board.SetPosition(iSizeX+15, 0)

				self.board.SetSize(iSizeX + 15, iSizeY + 38)
				self.SetPosition(wndMgr.GetScreenWidth() - 136 - iSizeX - 25 - 200, 78)			
				#self.AtlasMainWindow.SetSize(iSizeX, iSizeY)
				self.AtlasMainWindow.ShowAtlas()
				self.AtlasMainWindow.Show()
		ui.ScriptWindow.Show(self)
		self.IsShowWindowValue = True
		
	def Close(self):
		self.IsShowWindowValue = False
		self.Hide()
		
	def IsShowWindow(self):
		return self.IsShowWindowValue

	def SetCenterPositionAdjust(self, x, y):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def OnPressEscapeKey(self):
		self.Close()
		return True

def __RegisterMiniMapColor(type, rgb):
	miniMap.RegisterColor(type, rgb[0], rgb[1], rgb[2])

class MiniMap(ui.ScriptWindow):

	CANNOT_SEE_INFO_MAP_DICT = {
		"metin2_map_monkeydungeon" : False,
		"metin2_map_monkeydungeon_02" : False,
		"metin2_map_monkeydungeon_03" : False,
		"metin2_map_devilsCatacomb" : False,
		"metin2_12zi_stage" : False,
	}

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__Initialize()

		miniMap.Create()
		miniMap.SetScale(2.0)

		self.AtlasWindow = AtlasWindow()
		self.AtlasWindow.LoadWindow()
		self.AtlasWindow.Hide()

		self.tooltipMiniMapOpen = MapTextToolTip()
		self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
		self.tooltipMiniMapOpen.Show()
		self.tooltipMiniMapClose = MapTextToolTip()
		self.tooltipMiniMapClose.SetText(localeInfo.UI_CLOSE)
		self.tooltipMiniMapClose.Show()
		self.tooltipScaleUp = MapTextToolTip()
		self.tooltipScaleUp.SetText(localeInfo.MINIMAP_INC_SCALE)
		self.tooltipScaleUp.Show()
		self.tooltipScaleDown = MapTextToolTip()
		self.tooltipScaleDown.SetText(localeInfo.MINIMAP_DEC_SCALE)
		self.tooltipScaleDown.Show()
		self.tooltipAtlasOpen = MapTextToolTip()
		self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		self.tooltipAtlasOpen.Show()
		if app.ENABLE_BATTLE_FIELD:
			self.tooltipBattleField = MapTextToolTip()
			self.tooltipBattleField.SetText(localeInfo.MAP_BATTLE_FIELD)
			self.tooltipBattleField.Show()
			
		self.tooltipInfo = MapTextToolTip()
		self.tooltipInfo.Show()
		if app.WJ_SHOW_NPC_QUEST_NAME:
			self.tooltipQuest = MapTextToolTip()
			self.tooltipQuest.SetTextColor(QUEST_TOOLTIP_COLOR)
			self.tooltipQuest.Hide()

		if miniMap.IsAtlas():
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_SHOW_AREAMAP)
		else:
			self.tooltipAtlasOpen.SetText(localeInfo.MINIMAP_CAN_NOT_SHOW_AREAMAP)
			
		self.tooltipAtlasOpen.SetHorizontalAlignLeft()
			
		if app.ENABLE_PARTY_MATCH:
			self.party_match_event	= None
			self.tooltipPartyMatch = MapTextToolTip()
			self.tooltipPartyMatch.SetText(localeInfo.PARTY_MATCH_SEARCHING)
			self.tooltipPartyMatch.Show()

		self.mapName = ""

		self.isLoaded = 0
		self.canSeeInfo = True
		
		# AUTOBAN
		self.imprisonmentDuration = 0
		self.imprisonmentEndTime = 0
		self.imprisonmentEndTimeText = ""
		# END_OF_AUTOBAN

	def __del__(self):
		miniMap.Destroy()
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.positionInfo = 0
		self.observerCount = 0

		self.OpenWindow = 0
		self.CloseWindow = 0
		self.ScaleUpButton = 0
		self.ScaleDownButton = 0
		self.MiniMapHideButton = 0
		self.MiniMapShowButton = 0
		self.AtlasShowButton = 0
		if app.ENABLE_BATTLE_FIELD:
			self.BattleButton = 0

		self.tooltipMiniMapOpen = 0
		self.tooltipMiniMapClose = 0
		self.tooltipScaleUp = 0
		self.tooltipScaleDown = 0
		self.tooltipAtlasOpen = 0
		if app.ENABLE_BATTLE_FIELD:
			self.tooltipBattleField = 0
		self.tooltipInfo = None
		if app.WJ_SHOW_NPC_QUEST_NAME:
			self.tooltipQuest = None
		if app.ENABLE_PARTY_MATCH:
			self.party_match_event	= None
			self.tooltipPartyMatch	= 0
			self.PartyMatchButton	= 0
			self.PartyMatchEffect	= 0
		self.serverInfo = None

		if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
			self.GuildDragonlairFirstGuildText = None
			self.GuildDragonlairFirstGuildSecond = None
			self.GuildDragonlairFirstGuildLeftTime = 0
			self.isGuildDragonLairStart = False

	def SetMapName(self, mapName):
		self.mapName=mapName
		self.AtlasWindow.SetMapName(mapName)

		if self.CANNOT_SEE_INFO_MAP_DICT.has_key(mapName):
			self.canSeeInfo = False
			self.HideMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP_CANNOT_SEE)
		else:
			self.canSeeInfo = True
			self.ShowMiniMap()
			self.tooltipMiniMapOpen.SetText(localeInfo.MINIMAP)
			
	# AUTOBAN
	def SetImprisonmentDuration(self, duration):
		self.imprisonmentDuration = duration
		self.imprisonmentEndTime = app.GetGlobalTimeStamp() + duration				
		
		self.__UpdateImprisonmentDurationText()
		
	def __UpdateImprisonmentDurationText(self):
		restTime = max(self.imprisonmentEndTime - app.GetGlobalTimeStamp(), 0)
		
		imprisonmentEndTimeText = localeInfo.SecondToDHM(restTime)
		if imprisonmentEndTimeText != self.imprisonmentEndTimeText:
			self.imprisonmentEndTimeText = imprisonmentEndTimeText
			self.serverInfo.SetText("%s: %s" % (uiScriptLocale.AUTOBAN_QUIZ_REST_TIME, self.imprisonmentEndTimeText))
	# END_OF_AUTOBAN	

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			if localeInfo.IsARABIC():
				pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "Minimap.py")
			else:
				pyScrLoader.LoadScriptFile(self, "UIScript/MiniMap.py")
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.LoadScript")

		try:
			self.OpenWindow = self.GetChild("OpenWindow")
			self.MiniMapWindow = self.GetChild("MiniMapWindow")
			self.ScaleUpButton = self.GetChild("ScaleUpButton")
			self.ScaleDownButton = self.GetChild("ScaleDownButton")
			self.MiniMapHideButton = self.GetChild("MiniMapHideButton")
			self.AtlasShowButton = self.GetChild("AtlasShowButton")
			self.CloseWindow = self.GetChild("CloseWindow")
			self.MiniMapShowButton = self.GetChild("MiniMapShowButton")
			self.positionInfo = self.GetChild("PositionInfo")
			self.observerCount = self.GetChild("ObserverCount")
			self.serverInfo = self.GetChild("ServerInfo")
			if app.ENABLE_BATTLE_FIELD:
				self.BattleButton = self.GetChild("BattleButton")
			if app.ENABLE_PARTY_MATCH:
				self.PartyMatchButton = self.GetChild("PartyMatchButton")
				if self.party_match_event:
					self.PartyMatchButton.SetEvent( self.party_match_event )
				self.PartyMatchButton.Hide()
				self.PartyMatchEffect = self.GetChild("PartyMatchEffect")
				self.PartyMatchEffect.Hide()
			if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
				self.GuildDragonlairFirstGuildText = self.GetChild("GuildDragonlairFirstGuildText")
				self.GuildDragonlairFirstGuildText.Hide()
				self.GuildDragonlairFirstGuildSecond = self.GetChild("GuildDragonlairFirstGuildSecond")
				self.GuildDragonlairFirstGuildSecond.SetFontName(localeInfo.UI_BOLD_FONT)
				self.GuildDragonlairFirstGuildSecond.Hide()
				self.observerCount.Hide()
			
			if localeInfo.IsARABIC():
				self.GetChild("OpenWindowBGI").LeftRightReverse()
		except:
			import exception
			exception.Abort("MiniMap.LoadWindow.Bind")

		if constInfo.MINIMAP_POSITIONINFO_ENABLE==0:
			self.positionInfo.Hide()

		self.serverInfo.SetText(m2netm2g.GetServerInfo())
		self.ScaleUpButton.SetEvent(ui.__mem_func__(self.ScaleUp))
		self.ScaleDownButton.SetEvent(ui.__mem_func__(self.ScaleDown))
		self.MiniMapHideButton.SetEvent(ui.__mem_func__(self.HideMiniMap))
		self.MiniMapShowButton.SetEvent(ui.__mem_func__(self.ShowMiniMap))

		if miniMap.IsAtlas():
			self.AtlasShowButton.SetEvent(ui.__mem_func__(self.ShowAtlas))
		if app.ENABLE_BATTLE_FIELD:
			self.BattleButton.SetEvent(ui.__mem_func__(self.OpenbattleField))

		(ButtonPosX, ButtonPosY) = self.MiniMapShowButton.GetGlobalPosition()
		self.tooltipMiniMapOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.MiniMapHideButton.GetGlobalPosition()
		self.tooltipMiniMapClose.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleUpButton.GetGlobalPosition()
		self.tooltipScaleUp.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.ScaleDownButton.GetGlobalPosition()
		self.tooltipScaleDown.SetTooltipPosition(ButtonPosX, ButtonPosY)

		(ButtonPosX, ButtonPosY) = self.AtlasShowButton.GetGlobalPosition()
		self.tooltipAtlasOpen.SetTooltipPosition(ButtonPosX, ButtonPosY)
		
		if app.ENABLE_BATTLE_FIELD:
			(ButtonPosX, ButtonPosY) = self.BattleButton.GetGlobalPosition()
			self.tooltipBattleField.SetTooltipPosition(ButtonPosX, ButtonPosY)
			self.RefrashBattleButton(playerm2g2.IsBattleButtonFlush())
			playerm2g2.SetBattleButtonFlush(False)
		if app.ENABLE_PARTY_MATCH:
			(ButtonPosX, ButtonPosY) = self.PartyMatchButton.GetGlobalPosition()
			self.tooltipPartyMatch.SetTooltipPosition(ButtonPosX, ButtonPosY)
			

		self.ShowMiniMap()

	if app.ENABLE_BATTLE_FIELD:
		def OpenbattleField(self):
			m2netm2g.SendChatPacket("/open_battle_ui")
		
	def Destroy(self):
		self.HideMiniMap()

		self.AtlasWindow.Destroy()
		self.AtlasWindow = None

		self.ClearDictionary()

		self.__Initialize()

	def UpdateObserverCount(self, observerCount):
		if observerCount>0:
			self.observerCount.Show()
		elif observerCount<=0:
			self.observerCount.Hide()

		self.observerCount.SetText(localeInfo.MINIMAP_OBSERVER_COUNT % observerCount)
		
	def OnUpdate(self):
		(x, y, z) = playerm2g2.GetMainCharacterPosition()
		miniMap.Update(x, y)

		self.positionInfo.SetText("(%.0f, %.0f)" % (x/100, y/100))

		if self.tooltipInfo:
			if app.WJ_SHOW_NPC_QUEST_NAME:
				if 1 == self.MiniMapWindow.IsIn():
					(mouseX, mouseY) = wndMgr.GetMousePosition()
					(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
					
					splitsName = sName.split("|")
					isQuest = (len(splitsName)==2)
						
					if bFind == 0:
						self.tooltipInfo.Hide()
						self.tooltipQuest.Hide()
					elif not self.canSeeInfo:
						if isQuest and len(splitsName[0])==0:
							self.tooltipInfo.SetText("%s(%s)" % (uiScriptLocale.GUILD_BUILDING_POSITION, localeInfo.UI_POS_UNKNOWN))
						else:
							self.tooltipInfo.SetText("%s(%s)" % (splitsName[0], localeInfo.UI_POS_UNKNOWN))
						self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
						self.tooltipInfo.SetTextColor(dwTextColor)
						self.tooltipInfo.Show()
						if isQuest:
							self.tooltipQuest.SetText("%s" % splitsName[1])
							self.tooltipQuest.SetTooltipPosition(mouseX - 5, mouseY + 15)
							self.tooltipQuest.Show()
							self.tooltipQuest.SetTop()
						else:
							self.tooltipQuest.Hide()
					else:
						if localeInfo.IsARABIC() and splitsName[0].isalnum():
							if isQuest and len(splitsName[0])==0:
								self.tooltipInfo.SetText("(%s)%d, %d" % (uiScriptLocale.GUILD_BUILDING_POSITION, iPosX, iPosY))
							else:
								self.tooltipInfo.SetText("(%s)%d, %d" % (splitsName[0], iPosX, iPosY))
						else:
							if isQuest and len(splitsName[0])==0:
								self.tooltipInfo.SetText("%s(%d, %d)" % (uiScriptLocale.GUILD_BUILDING_POSITION, iPosX, iPosY))
							else:
								self.tooltipInfo.SetText("%s(%d, %d)" % (splitsName[0], iPosX, iPosY))
						self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
						self.tooltipInfo.SetTextColor(dwTextColor)
						self.tooltipInfo.Show()
						
						if isQuest:
							self.tooltipQuest.SetText("%s" % splitsName[1])
							self.tooltipQuest.SetTooltipPosition(mouseX - 5, mouseY + 15)
							self.tooltipQuest.Show()
							self.tooltipQuest.SetTop()
						else:
							self.tooltipQuest.Hide()					

				else:
					self.tooltipInfo.Hide()
					self.tooltipQuest.Hide()
			else:
				if 1 == self.MiniMapWindow.IsIn():
					(mouseX, mouseY) = wndMgr.GetMousePosition()
					(bFind, sName, iPosX, iPosY, dwTextColor) = miniMap.GetInfo(mouseX, mouseY)
					if bFind == 0:
						self.tooltipInfo.Hide()
					elif not self.canSeeInfo:
						self.tooltipInfo.SetText("%s(%s)" % (sName, localeInfo.UI_POS_UNKNOWN))
						self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
						self.tooltipInfo.SetTextColor(dwTextColor)
						self.tooltipInfo.Show()
					else:
						if localeInfo.IsARABIC() and sName[-1].isalnum():
							self.tooltipInfo.SetText("(%s)%d, %d" % (sName, iPosX, iPosY))
						else:
							self.tooltipInfo.SetText("%s(%d, %d)" % (sName, iPosX, iPosY))
						self.tooltipInfo.SetTooltipPosition(mouseX - 5, mouseY)
						self.tooltipInfo.SetTextColor(dwTextColor)
						self.tooltipInfo.Show()
				else:
					self.tooltipInfo.Hide()
			
			# AUTOBAN
			if self.imprisonmentDuration:
				self.__UpdateImprisonmentDurationText()				
			# END_OF_AUTOBAN

		if True == self.MiniMapShowButton.IsIn():
			self.tooltipMiniMapOpen.Show()
		else:
			self.tooltipMiniMapOpen.Hide()

		if True == self.MiniMapHideButton.IsIn():
			self.tooltipMiniMapClose.Show()
		else:
			self.tooltipMiniMapClose.Hide()

		if True == self.ScaleUpButton.IsIn():
			self.tooltipScaleUp.Show()
		else:
			self.tooltipScaleUp.Hide()

		if True == self.ScaleDownButton.IsIn():
			self.tooltipScaleDown.Show()
		else:
			self.tooltipScaleDown.Hide()

		if True == self.AtlasShowButton.IsIn():
			self.tooltipAtlasOpen.Show()
		else:
			self.tooltipAtlasOpen.Hide()

		if app.ENABLE_BATTLE_FIELD:
			if True == self.BattleButton.IsIn():
				self.tooltipBattleField.Show()
				self.BattleButton.DisableFlash()
			else:
				self.tooltipBattleField.Hide()
				
		if app.ENABLE_PARTY_MATCH:
			if True == self.PartyMatchButton.IsIn():
				self.tooltipPartyMatch.Show()
			else:
				self.tooltipPartyMatch.Hide()
				
		if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
			self.GuildTextUpdate()

	def OnRender(self):
		(x, y) = self.GetGlobalPosition()
		fx = float(x)
		fy = float(y)
		if app.ENABLE_12ZI and not localeInfo.IsARABIC():
			miniMap.Render(fx + 19.0, fy + 5.0)
		else:
			miniMap.Render(fx + 4.0, fy + 5.0)

	def Close(self):
		self.HideMiniMap()

	def HideMiniMap(self):
		miniMap.Hide()
		self.OpenWindow.Hide()
		self.CloseWindow.Show()

	def ShowMiniMap(self):
		if not self.canSeeInfo:
			return

		miniMap.Show()
		self.OpenWindow.Show()
		self.CloseWindow.Hide()

	def isShowMiniMap(self):
		return miniMap.isShow()

	def ScaleUp(self):
		miniMap.ScaleUp()

	def ScaleDown(self):
		miniMap.ScaleDown()

	def ShowAtlas(self):
		if not miniMap.IsAtlas():
			return
		if not self.AtlasWindow.IsShow():
			self.AtlasWindow.Show()

	def ToggleAtlasWindow(self):
		if not miniMap.IsAtlas():
			return
		if self.AtlasWindow.IsShow():
			self.AtlasWindow.Hide()
		else:
			self.AtlasWindow.Show()
			
	if app.ENABLE_BATTLE_FIELD:
		def RefrashBattleButton(self, isFlash = True):
			IsEnable = playerm2g2.GetBattleFieldEnable()
			IsEventEnable = playerm2g2.GetBattleFieldEventEnable()
			
			IsOpen = playerm2g2.IsBattleFieldOpen()
			IsEventOpen = playerm2g2.IsBattleFieldEventOpen()
			
			if IsOpen == True and IsEventOpen == True:
				self.BattleButton.SetUpVisual("d:/ymir work/ui/minimap/E_open_default.tga")
				self.BattleButton.SetOverVisual("d:/ymir work/ui/minimap/E_open_over.tga")
				self.BattleButton.SetDownVisual("d:/ymir work/ui/minimap/E_open_down.tga")
				if isFlash:
					self.BattleButton.EnableFlash()
			elif IsOpen == True and IsEventOpen == False:
				self.BattleButton.SetUpVisual("d:/ymir work/ui/minimap/battle_open_default.tga")
				self.BattleButton.SetOverVisual("d:/ymir work/ui/minimap/battle_open_over.tga")
				self.BattleButton.SetDownVisual("d:/ymir work/ui/minimap/battle_open_down.tga")
				if isFlash:
					self.BattleButton.EnableFlash()
			else:
				self.BattleButton.SetUpVisual("d:/ymir work/ui/minimap/battle_open_down.tga")
				self.BattleButton.SetOverVisual("d:/ymir work/ui/minimap/battle_open_down.tga")
				self.BattleButton.SetDownVisual("d:/ymir work/ui/minimap/battle_open_down.tga")
				self.BattleButton.Down()
				
	if app.ENABLE_MOVE_CHANNEL:
		def RefreshServerInfo(self):
			self.serverInfo.SetText(m2netm2g.GetServerInfo())

	if app.ENABLE_PARTY_MATCH:
		def ShowPartyMatchButton(self):
			if self.PartyMatchButton:
				self.PartyMatchButton.Show()
			if self.PartyMatchEffect:
				self.PartyMatchEffect.Show()
				self.PartyMatchEffect.ResetFrame()
		def HidePartyMatchButton(self):
			if self.PartyMatchButton:
				self.PartyMatchButton.Hide()
			if self.PartyMatchEffect:
				self.PartyMatchEffect.Hide()
		def BindPartyMatchEvent(self, event):
			if self.PartyMatchButton:
				self.PartyMatchButton.SetEvent( ui.__mem_func__(event) )
			else:
				self.party_match_event = ui.__mem_func__(event)

		if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM:
			def SetGuildDragonLiarStart(self):
				self.isGuildDragonLairStart = True
				if self.GuildDragonlairFirstGuildLeftTime != 0 :
					self.GuildDragonlairFirstGuildLeftTime = app.GetTime() + self.GuildDragonlairFirstGuildLeftTime
				
			def SetGuildDragonLiarSuccess(self):
				self.GuildDragonlairFirstGuildSecond.SetPackedFontColor(grp.GenerateColor(0.0, 0.5, 1.0, 1.0))
				self.GuildDragonlairFirstGuildSecond.SetText(localeInfo.GUILD_DRAGONLAIR_RANKING_SUCCESS)
				self.isGuildDragonLairStart = False
				
			def SetGuildDragonLairFistGuildText(self, second):
				self.GuildDragonlairFirstGuildText.Show()
				self.GuildDragonlairFirstGuildSecond.Show()
				
				if second == 0 :
					self.GuildDragonlairFirstGuildSecond.SetText(localeInfo.GUILD_DRAGONLAIR_RANKING_NONE)
				else:
					self.GuildDragonlairFirstGuildSecond.SetText(localeInfo.SecondToColonTypeMS(second))
					self.GuildDragonlairFirstGuildLeftTime = second

				self.isGuildDragonLairStart = False

				if self.positionInfo.IsShow() :
					(x,y) = self.GuildDragonlairFirstGuildText.GetLocalPosition()
					self.GuildDragonlairFirstGuildText.SetPosition(x, y+20)
					(x,y) = self.GuildDragonlairFirstGuildSecond.GetLocalPosition()
					self.GuildDragonlairFirstGuildSecond.SetPosition(x, y+20)
					
				if self.observerCount.IsShow() :
					(x,y) = self.GuildDragonlairFirstGuildText.GetLocalPosition()
					self.GuildDragonlairFirstGuildText.SetPosition(x, y+20)
					(x,y) = self.GuildDragonlairFirstGuildSecond.GetLocalPosition()
					self.GuildDragonlairFirstGuildSecond.SetPosition(x, y+20)				
					
			def GuildTextUpdate(self):
				if self.isGuildDragonLairStart == True:
					if self.GuildDragonlairFirstGuildLeftTime != 0 :
						lefttime = self.GuildDragonlairFirstGuildLeftTime - app.GetTime()
						if lefttime <= 0:
							self.GuildDragonlairFirstGuildSecond.SetPackedFontColor(grp.GenerateColor(1.0, 0.0, 0.0, 1.0))
							self.GuildDragonlairFirstGuildSecond.SetText(localeInfo.GUILD_DRAGONLAIR_RANKING_FAIL)
							self.isGuildDragonLairStart = False
						else:
							self.GuildDragonlairFirstGuildSecond.SetText(localeInfo.SecondToColonTypeMS(lefttime))
							if lefttime < 60 :
								self.GuildDragonlairFirstGuildSecond.SetPackedFontColor(grp.GenerateColor(1.0, 0.0, 0.0, 1.0))