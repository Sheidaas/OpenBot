import ui
import uiScriptLocale
import app
import m2netm2g
import playerm2g2
import localeInfo
import constInfo
import wndMgr
import item
import chatm2g
import chrmgrm2g

MATCH_STATE_NONE = 0
MATCH_STATE_SEARCHING = 1

REQUIRED_ITEM_MAX = playerm2g2.PARTY_MATCH_REQUIRED_ITEM_MAX

PARTY_MEMBER_MAX = 8

## ��Ƽ��Ī
class PartyMatch(ui.ScriptWindow):
			
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI")
		self.isLoaded = 0
		self.SetWindowName("PartyMatchWindow")
		
		self.match_state					= MATCH_STATE_NONE
		self.party_match_button				= None
		self.party_match_cancel_button		= None
		self.entree_level_text				= None
		self.entree_level					= 0
		self.required_items_slot			= None
		self.required_item_vnums			= [0 for col in range(0,REQUIRED_ITEM_MAX)]
		self.required_item_count			= [0 for col in range(0,REQUIRED_ITEM_MAX)]
		self.tooltipItem					= None
		self.dungeon_select_window			= None
		self.dungeon_select_text_window		= None
		self.dungeon_select_button			= None
		self.dungeon_dict					= {}
		self.dungeon_button_dict			= {}
		self.dungeon_select_list_open		= False
		self.dungeon_select_window_height	= 0
		self.mouse_over_img					= None
		self.dungeon_select_text			= None
		self.selected_dungeon				= 0
		self.matching_start_time			= 0
		self.time_check						= False
		self.minimap						= None
		self.off							= False
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def Show(self):
		if True == self.off:
			return
			
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.SetTop()
			
	def Hide(self):
		wndMgr.Hide(self.hWnd)
		
	def Close(self):
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)
		
	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		
		if not playerm2g2.IsPartyMatchLoaded():
			return
			
		self.off = chrmgrm2g.GetPartyMatchOff()
		if True == self.off:
			return
			
		self.isLoaded = 1
		
		
		## Load Script
		try:
			self.__LoadScript("UIScript/PartyMatchWindow.py")
				
		except:
			import exception
			exception.Abort("PartyMatch.LoadWindow.__LoadScript")
		
		## object	
		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("PartyMatch.LoadWindow.__BindObject")
			
		## event
		try:	
			self.__BindEvent()
		except:
			import exception
			exception.Abort("PartyMatch.LoadWindow.__BindEvent")
			
	def Destroy(self):
		self.isLoaded = 0
		
		self.match_state = MATCH_STATE_NONE
		
		if self.party_match_button:
			del self.party_match_button
		if self.party_match_cancel_button:
			del self.party_match_cancel_button
		if self.entree_level_text:
			del self.entree_level_text
		self.entree_level = 0
		
		if self.required_items_slot:
			del self.required_items_slot
			
		self.required_item_vnums	= [0 for col in range(0,REQUIRED_ITEM_MAX)]
		self.required_item_count	= [0 for col in range(0,REQUIRED_ITEM_MAX)]
		self.tooltipItem			= None
		
		if self.dungeon_select_window:
			del self.dungeon_select_window
		
		if self.dungeon_select_text_window:
			del self.dungeon_select_text_window
		
		if self.dungeon_select_button:
			del self.dungeon_select_button
			
		if self.dungeon_dict:
			del self.dungeon_dict
			
		if self.dungeon_button_dict:
			del self.dungeon_button_dict
			
		self.dungeon_select_list_open		= False
		self.dungeon_select_window_height	= 0
		
		if self.mouse_over_img:
			del self.mouse_over_img
			
		if self.dungeon_select_text:
			del self.dungeon_select_text
			
		self.selected_dungeon				= 0
		self.matching_start_time			= 0
		self.time_check						= False
		self.minimap						= None
		
	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem
		
	def __BindObject(self):
		self.party_match_button			= self.GetChild("MatchingButton")
		self.party_match_cancel_button	= self.GetChild("CloseButton")
		self.entree_level_text			= self.GetChild("entree_level_text")
		self.required_items_slot		= self.GetChild("required_items_slot")
		
		## mouse over image
		self.mouse_over_img				= self.GetChild("mouse_over_image")
		self.mouse_over_img.Hide()
		## dungeon select button
		self.dungeon_select_button		= self.GetChild("dungeon_select_button")
		## dungeon select text window
		self.dungeon_select_text_window = self.GetChild("dungeon_select_text_window")
		## dungeon select text
		self.dungeon_select_text		= self.GetChild("dungeon_select_text")
		## dungeon button
		self.dungeon_select_window		= self.GetChild("dungeon_select_window")
		self.__CreateDungeonNameButton()
		
		if localeInfo.IsARABIC():
			self.GetChild("main_bg").LeftRightReverse()
					
	def __BindEvent(self):
		## close event
		self.GetChild("board").SetCloseEvent( ui.__mem_func__(self.Close) )
		
		## dungeon select event
		if self.dungeon_select_button:
			self.dungeon_select_button.SetEvent( ui.__mem_func__(self.__ClickDungeonSelectButton) )
		if self.dungeon_select_text_window:
			self.dungeon_select_text_window.SetOnMouseLeftButtonUpEvent( ui.__mem_func__(self.__ClickDungeonSelectButton) )
		
		## button event
		if self.party_match_button:
			self.party_match_button.SetEvent( ui.__mem_func__(self.__ClickMatchingButton) )
		if self.party_match_cancel_button:
			self.party_match_cancel_button.SetEvent( ui.__mem_func__(self.Close) )
			
		## slot event
		if self.required_items_slot:
			self.required_items_slot.SetOverInItemEvent(ui.__mem_func__(self.__SlotOverInItem))
			self.required_items_slot.SetOverOutItemEvent(ui.__mem_func__(self.__SlotOverOutItem))
			
		
	## partymatch_info.txt �� ������ ���� ��ư�� �����ϰ� �����Ѵ�
	def __CreateDungeonNameButton(self):
		if not self.dungeon_select_window:
			return
			
		self.dungeon_dict = playerm2g2.GetPartyMatchInfoMap()
		if not self.dungeon_dict:
			return
			
		button_height = 16
		dict_len = len( self.dungeon_dict )
		
		self.dungeon_select_window_height = dict_len * button_height
		
		## key �� �������� ����
		for i, key in enumerate( sorted(self.dungeon_dict.iterkeys()) ):
			button = ui.Button()
			button.SetParent( self.dungeon_select_window )
			button.SetPosition( 0, button_height * i )
			
			if 1 == dict_len:
				button.SetUpVisual( "d:/ymir work/ui/game/party_match/button_one.sub" )
				button.SetDownVisual( "d:/ymir work/ui/game/party_match/button_one.sub" )
				button.SetOverVisual( "d:/ymir work/ui/game/party_match/button_one.sub" )								
			elif i == 0:
				button.SetUpVisual( "d:/ymir work/ui/game/party_match/button_top.sub" )
				button.SetDownVisual( "d:/ymir work/ui/game/party_match/button_top.sub" )
				button.SetOverVisual( "d:/ymir work/ui/game/party_match/button_top.sub" )
			elif i == dict_len - 1:
				button.SetUpVisual( "d:/ymir work/ui/game/party_match/button_bottom.sub" )
				button.SetDownVisual( "d:/ymir work/ui/game/party_match/button_bottom.sub" )
				button.SetOverVisual( "d:/ymir work/ui/game/party_match/button_bottom.sub" )
			else:
				button.SetUpVisual( "d:/ymir work/ui/game/party_match/button_middle.sub" )
				button.SetDownVisual( "d:/ymir work/ui/game/party_match/button_middle.sub" )
				button.SetOverVisual( "d:/ymir work/ui/game/party_match/button_middle.sub" )
			
			button.SetEvent( ui.__mem_func__(self.__ClickDungeonSelect), key )
			button.SetOverEvent( ui.__mem_func__(self.__ClickDungeonButtonOver), key )
			button.SetOverOutEvent( ui.__mem_func__(self.__ClickDungeonButtonOverOut), key )
			if localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX.has_key( key ):
				button.SetText( localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX[key] )
			button.Hide()
			
			self.dungeon_button_dict[key] = button
			
	## ���� mouse over ��
	def __ClickDungeonButtonOver(self, map_index):
		if not self.mouse_over_img:
			return
			
		button = self.dungeon_button_dict.get( map_index, 0 )
		if 0 == button:
			return
		
		( button_x, button_y ) = button.GetLocalPosition()
		if localeInfo.IsARABIC():
			self.mouse_over_img.SetPosition( 109+115+15 + button_x, 61 + button_y )
			self.mouse_over_img.Show()
		else:
			self.mouse_over_img.SetPosition( 109 + button_x, 61 + button_y )
			self.mouse_over_img.Show()
		
	## ���� mouse over out ��
	def __ClickDungeonButtonOverOut(self, map_index):
		if not self.mouse_over_img:
			return
		self.mouse_over_img.Hide()
			
	## ���� ������
	def __ClickDungeonSelect(self, map_index):
			
		if not map_index in self.dungeon_dict:
			return
		
		for button in self.dungeon_button_dict.values():
			button.Hide()
			
		## ���� ����â �ݴ´�
		self.__DungeonSelectWindow( False )
		
		## ������ map index ����
		self.selected_dungeon = map_index
		
		## �� �̸� ǥ��
		if self.dungeon_select_text:
			if localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX.has_key( map_index ):
				self.dungeon_select_text.SetText( localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX[map_index] )
		
		## �ش� ������ ���� ������ ����	
		( map_idx, limit_level, items ) = self.dungeon_dict[map_index]
		## ���� ���� ǥ��
		self.__SetEntreeLevel(limit_level)
		## �ʿ� ������ ǥ��
		if REQUIRED_ITEM_MAX != len(items):
			return
		for i, (vnum, count) in enumerate(items):
			self.__SetSlotRequiredItem(i, vnum, count)
	
	## ���� ���� â ����/�ݱ�
	def __DungeonSelectWindow(self, show):
	
		if True == show:
			self.dungeon_select_list_open = True
			if self.dungeon_select_window:
				self.dungeon_select_window.SetSize( 130, self.dungeon_select_window_height )
			
			for button in self.dungeon_button_dict.values():
				button.Show()
		else:
			self.dungeon_select_list_open = False
			if self.dungeon_select_window:
				self.dungeon_select_window.SetSize( 130, 0 )
			for button in self.dungeon_button_dict.values():
				button.Hide()
						
	## ���� ���� ��ư Ŭ��
	def __ClickDungeonSelectButton(self):
		if MATCH_STATE_SEARCHING == self.match_state:
			return
			
		if self.dungeon_select_list_open:
			self.__DungeonSelectWindow( False )
		else:
			self.__DungeonSelectWindow( True )
			
	## �ð� üũ
	def OnUpdate(self):
		if True == self.off:
			return
			
		if False == self.time_check:
			return
			
		## �ð� üũ 10�� ��Ÿ��
		if app.GetGlobalTimeStamp() - self.matching_start_time < 10:
			return
		
		if self.party_match_button:
			self.party_match_button.Enable()
		self.time_check = False
				
	## ��Ƽ ��Ī ��û�� �Ͽ���( ����û ��ư Ŭ�� )
	def __ClickMatchingButton(self):
		if not self.party_match_button:
			return
			
		if not self.dungeon_dict:
			return
			
		## ������ �������� �ʾҴ�.
		if 0 == self.selected_dungeon:
			self.__PartyMatchMsg((playerm2g2.PARTY_MATCH_FAIL_NONE_MAP_INDEX, 0))
			return
	
		## ��� ���
		if MATCH_STATE_SEARCHING == self.match_state:
			self.match_state = MATCH_STATE_NONE
			if self.party_match_button:
				self.party_match_button.SetText( uiScriptLocale.PARTY_MATCH_TEXT_REQUEST_MATCH )
				self.party_match_button.Disable()
			## ��Ƽ��Ī ��� ��Ŷ�� ������.
			m2netm2g.SendPartyMatchCancel( self.selected_dungeon )
			## ��û�� �ð� ����
			self.matching_start_time	= app.GetGlobalTimeStamp()
			self.time_check				= True
			return

		## ���� ������ ����.
		if not self.dungeon_dict.has_key( self.selected_dungeon ):
			return
	
		## ��� ��û
		if MATCH_STATE_NONE == self.match_state:
			( map_idx, limit_level, items ) = self.dungeon_dict[self.selected_dungeon]
			
			## ���� ������ üũ
			if REQUIRED_ITEM_MAX != len(items):
				return
			
			fail_vnum = playerm2g2.IsPartyMatchEnoughItem( self.selected_dungeon )
			if fail_vnum: 
				self.__PartyMatchMsg((playerm2g2.PARTY_MATCH_FAIL_NO_ITEM, fail_vnum))
				return
			
			## ���� üũ
			if playerm2g2.GetStatus(playerm2g2.LEVEL) < limit_level:
				self.__PartyMatchMsg((playerm2g2.PARTY_MATCH_FAIL_LEVEL, 0))
				return
				
			## ���� ��Ƽ��� �������� üũ
			if playerm2g2.IsPartyMember( playerm2g2.GetMainCharacterIndex() ):
				if not playerm2g2.IsPartyLeader( playerm2g2.GetMainCharacterIndex() ):
					self.__PartyMatchMsg((playerm2g2.PARTY_MATCH_FAIL_NOT_LEADER, 0))
					return
				elif playerm2g2.GetPartyMemberCount() >= PARTY_MEMBER_MAX:
					self.__PartyMatchMsg((playerm2g2.PARTY_MATCH_FAIL_FULL_MEMBER, 0))
					return
			
			self.match_state = MATCH_STATE_SEARCHING
			self.party_match_button.SetText( uiScriptLocale.PARTY_MATCH_TEXT_REQUEST_MATCH_CANCEL )
			## ��Ƽ��Ī ��û ��Ŷ�� ������.
			m2netm2g.SendPartyMatchSearch( self.selected_dungeon )
			
			## ���� ���� â �ݴ´�.
			self.__DungeonSelectWindow( False )
					
			
	## ���� ���� ǥ��	
	def __SetEntreeLevel(self, level):
		if not self.entree_level_text:
			return
			
		self.entree_level_text.SetText( uiScriptLocale.PARTY_MATCH_TEXT_ENTREE_LEVEL % level )
		self.entree_level = level
		
	## �ʿ� ������ ǥ��
	def __SetSlotRequiredItem(self, slotIndex, item_vnum, item_count):
		if not self.required_items_slot or not self.required_item_vnums or not self.required_item_count:
			return
			
		self.required_items_slot.SetItemSlot( slotIndex, item_vnum, item_count )
		self.required_item_vnums[slotIndex] = item_vnum
		self.required_item_count[slotIndex] = item_count
		
	## �ʿ� ������ slot mouse over	
	def __SlotOverInItem(self, slotIndex):
		if self.tooltipItem:
			if self.required_item_vnums and self.required_item_vnums[slotIndex]:
				self.tooltipItem.SetItemToolTip( self.required_item_vnums[slotIndex] )
	
	## �ʿ� ������ slot mouse over out
	def __SlotOverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()
			
	## �����κ��� ���� ��Ƽ��ġ ���
	def PartyMatchResult(self, type, data):
		if playerm2g2.PARTY_MATCH_SEARCH == type:
			pass
		elif playerm2g2.PARTY_MATCH_CANCEL == type:
			self.__PartyMatchMsg(data)
			self.__PartyMatchMinimapButton(data)
		elif playerm2g2.PARTY_MATCH_INFO == type:
			self.__SetInfo(data)
		elif playerm2g2.PARTY_MATCH_INFO_MEBMER == type:
			self.__SetInfoMember(data)
		
	## ��Ƽ ��Ī ��ġ�� ���̵��̳� �α��ν� ȣ��	
	def __SetInfo(self, map_index):
		self.__Init()
		self.__ClickDungeonSelect(map_index)
		self.match_state = MATCH_STATE_SEARCHING
		if self.party_match_button:
			self.party_match_button.SetText( uiScriptLocale.PARTY_MATCH_TEXT_REQUEST_MATCH_CANCEL )
		if self.minimap:
			self.minimap.ShowPartyMatchButton()
			
	## ��Ƽ ��Ī ��ġ�� ���̵��̳� �α��ν� ȣ��(��Ƽ���� �ƴ� ����� ���)
	def __SetInfoMember(self, map_index):
		if self.minimap:
			self.minimap.ShowPartyMatchButton()
		
	## ��Ƽ ��ġ �޼���
	def __PartyMatchMsg(self, data):
		(msg_type, add_info) = data
		if playerm2g2.PARTY_MATCH_FAIL == msg_type:
			pass
		elif playerm2g2.PARTY_MATCH_SUCCESS == msg_type:
			# ��Ī ����
			pass
		elif playerm2g2.PARTY_MATCH_START == msg_type:
			# ��Ī ��û ����
			self.Close()
			if localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX.has_key( add_info ):
				chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_START % localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX[add_info] )
			return
		elif playerm2g2.PARTY_MATCH_CANCEL_SUCCESS == msg_type:
			# ��Ƽ��ġ ��û ���
			if localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX.has_key( add_info ):
				chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_CANCEL % localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX[add_info] )
		elif playerm2g2.PARTY_MATCH_FAIL_NO_ITEM == msg_type:
			# �������� ����
			item.SelectItem( add_info )
			itemName = item.GetItemName()
			chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_FAIL_NO_ITEM % itemName )
		elif playerm2g2.PARTY_MATCH_FAIL_LEVEL == msg_type:
			# ������ ����
			chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_FAIL_LEVEL )
		elif playerm2g2.PARTY_MATCH_FAIL_NOT_LEADER == msg_type:
			# ��Ƽ���� �ƴ�
			chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_FAIL_NOT_LEADER )
		elif playerm2g2.PARTY_MATCH_FAIL_MEMBER_NOT_CONDITION == msg_type:
			# ��Ƽ�ɹ��� ���ǿ� �������� �ʴ´�(����,������)
			# pid �޾Ƽ� vid �� �����ؾ���.
			member_name = playerm2g2.GetPartyMemberName( add_info )
			chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_FAIL_MEMBER_NOT_CONDITION % member_name )
		elif playerm2g2.PARTY_MATCH_FAIL_NONE_MAP_INDEX == msg_type:
			# ��Ƽ��Ī�� ���� �ʹ�ȣ�϶�(Ȥ�� ������ ������ ������)
			chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_FAIL_NONE_MAP_INDEX )
		elif playerm2g2.PARTY_MATCH_FAIL_IMPOSSIBLE_MAP == msg_type:
			# ���� ��û �Ұ����� �ʿ� ������
			chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_FAIL_IMPOSSIBLE_MAP )
		elif playerm2g2.PARTY_MATCH_HOLD == msg_type:
			return
		elif playerm2g2.PARTY_MATCH_FAIL_FULL_MEMBER == msg_type:
			chatm2g.AppendChat( chatm2g.CHAT_TYPE_INFO, localeInfo.PARTY_MATCH_FAIL_FULL_MEMBER )
			
		## �ʱ�ȭ �Լ� ȣ��
		self.__Init()
		
	def __PartyMatchMinimapButton(self, data):
		if not self.minimap:
			return
			
		(msg_type, add_info) = data
		if playerm2g2.PARTY_MATCH_START == msg_type:
			self.minimap.ShowPartyMatchButton()
		elif msg_type in [playerm2g2.PARTY_MATCH_CANCEL_SUCCESS, playerm2g2.PARTY_MATCH_SUCCESS, playerm2g2.PARTY_MATCH_FAIL]:
			self.minimap.HidePartyMatchButton()
			
	def __Init(self):
		self.selected_dungeon	= 0
		self.match_state		= MATCH_STATE_NONE
		# ��� ��û ��ư �ؽ�Ʈ �ʱ�ȭ
		if self.party_match_button:
			self.party_match_button.SetText( uiScriptLocale.PARTY_MATCH_TEXT_REQUEST_MATCH )
		# �����̸� �ؽ�Ʈ �ʱ�ȭ
		if self.dungeon_select_text:
			self.dungeon_select_text.SetText( uiScriptLocale.PARTY_MATCH_TEXT_DUNGEON_SELECT )
		# ���� ����â �ݴ´�
		self.__DungeonSelectWindow( False )
		# ���� �ʱ�ȭ
		self.__SetEntreeLevel(0)
		# �ʿ������ ���� �ʱ�ȭ
		for i in range(REQUIRED_ITEM_MAX):
			self.__SetSlotRequiredItem(i,0,0)
		
			
	def BindMiniMap(self, minimap):
		self.minimap = minimap
		
	def Off(self, enable):
		if int(enable):
			self.off = True
			
			self.Close()
			if self.minimap:
				self.minimap.HidePartyMatchButton()
		else:
			self.off = False