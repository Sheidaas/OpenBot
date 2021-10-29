import ui
import uiScriptLocale
import wndMgr
import playerm2g2
import localeInfo
import m2netm2g
import app
import constInfo
import event
import uiCommon
import grpImage
import grp
import mouseModule
import item

STATE_NONE		= 0
STATE_WAITING	= 1
STATE_PLAY		= 2

FISH_WAITING_PAGE_BOX_VISIBLE_LINE_COUNT = 8
DEFAULT_DESC_Y	= 7

fish_event_game_state = STATE_NONE

RESERVED_TYPE		= 0
SPECIAL_TYPE		= 1
NORMAL_TYPE			= 2
FISH_EVENT_TYPE_MAX	= 3

ITEM_FISH_EVENT_BOX				= 25106
ITEM_FISH_EVENT_BOX_SPECIAL 	= 25107


	
def LoadScript(self, fileName):
	pyScrLoader = ui.PythonScriptLoader()
	pyScrLoader.LoadScriptFile(self, fileName)
	
class FishEventGameWaitingPage(ui.ScriptWindow):

	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = -1
		def __del__(self):
			ui.Window.__del__(self)
		def SetIndex(self, index):
			self.descIndex = index
		def OnRender(self):
			event.RenderEventSet( self.descIndex )
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		self.isLoaded			= 0
		self.startButton		= None
		self.descBoard			= None
		self.descriptionBox		= None
		self.descIndex			= -1
		self.desc_y				= DEFAULT_DESC_Y
		self.btnPrev			= None
		self.btnNext			= None
		self.MiniGameFish		= None
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def SetMiniGameFish(self, mini_game_fish):
		self.MiniGameFish = mini_game_fish
	
	def __LoadWindow(self):
	
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			LoadScript(self, "UIScript/MiniGameFishEventWaitingPage.py")
			
		except:
			import exception
			exception.Abort("FishEventGameWaitingPage.LoadWindow.LoadObject")
			
		try:
			self.GetChild("titlebar").SetCloseEvent( ui.__mem_func__(self.Close) )
			self.startButton	= self.GetChild("game_start_button")
			self.startButton.SetEvent(ui.__mem_func__(self.__ClickStartButton))
			
			self.descBoard		= self.GetChild("desc_board")
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Hide()
			
			self.btnPrev = self.GetChild("prev_button")
			self.btnNext = self.GetChild("next_button")
			self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
			
			if localeInfo.IsARABIC():
				self.btnPrev.LeftRightReverse()
				self.btnNext.LeftRightReverse()
			
		except:
			import exception
			exception.Abort("FishEventGameWaitingPage.LoadWindow.BindObject")
		
		self.Hide()
			
	def Close(self):
		self.Hide()
		event.ClearEventSet(self.descIndex)
		self.descIndex = -1
		
		if self.descriptionBox:
			self.descriptionBox.Hide()
		
		self.desc_y = DEFAULT_DESC_Y
		
	def Destroy(self):
		self.isLoaded				= 0
		self.startButton			= None
		self.descBoard				= None
		self.descriptionBox			= None
		self.descIndex				= -1
		self.desc_y					= DEFAULT_DESC_Y
		self.btnPrev				= None
		self.btnNext				= None
		self.MiniGameFish			= None
				
	def OnPressEscapeKey(self):
		self.Close()
		return True		
				
	def __ClickStartButton(self):
		global fish_event_game_state
		fish_event_game_state = STATE_PLAY
		self.Close()
		
		if self.MiniGameFish:
			self.MiniGameFish.Open()
				
	def Show(self):
		ui.ScriptWindow.Show(self)
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet( uiScriptLocale.FISH_EVENT_DESC )
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
		event.SetVisibleLineCount( self.descIndex, FISH_WAITING_PAGE_BOX_VISIBLE_LINE_COUNT )
		total_line = event.GetTotalLineCount(self.descIndex)
		
		if localeInfo.IsARABIC():
			event.SetEventSetWidth(self.descIndex, self.descBoard.GetWidth() - 20)
			
		event.SetRestrictedCount(self.descIndex, 38)
			
		if FISH_WAITING_PAGE_BOX_VISIBLE_LINE_COUNT >= total_line :
			self.btnPrev.Hide()
			self.btnNext.Hide()
		else :
			self.btnPrev.Show()
			self.btnNext.Show()
		
		if self.descriptionBox:
			self.descriptionBox.Show()
	
	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+self.desc_y))
		self.descriptionBox.SetIndex(self.descIndex)
		
	def PrevDescriptionPage(self):
	
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		decrease_count = FISH_WAITING_PAGE_BOX_VISIBLE_LINE_COUNT
		
		if cur_start_line - decrease_count < 0:
			return;

		event.SetVisibleStartLine(self.descIndex, cur_start_line - decrease_count)
		self.desc_y += ( line_height * decrease_count )
	
	def NextDescriptionPage(self):
	
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		total_line_count	= event.GetProcessedLineCount(self.descIndex)
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		increase_count = FISH_WAITING_PAGE_BOX_VISIBLE_LINE_COUNT
		
		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return
		
		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.desc_y -= ( line_height * increase_count )
		
				
class FishEventGamePage(ui.ScriptWindow):
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		self.isLoaded				= 0
		self.MiniGameFish			= None
		self.inven					= None
		self.interface				= None
		
		self.fish_box_slot			= [ 0 for col in range(0,FISH_EVENT_TYPE_MAX)]
		self.fish_box_slot_pos		= [-1 for col in range(0,FISH_EVENT_TYPE_MAX)]
		
		self.tooltipitem			= None
		self.grid_slot				= None
		self.shape					= 0
		self.question_dialog		= None
		self.popup					= None
		self.use_count_text			= None
		self.use_count				= 0
		
		self.score_text_effect		= None
		self.score_effect1			= None
		self.score_effect2			= None
		self.score_effect3			= None
		self.reward_vnum			= 0
		
		self.fishPieceDict = {
			app.FISH_EVENT_SHAPE_1	: grpImage.Generate("D:/Ymir Work/UI/minigame/fish_event/fish_1.sub"),
			app.FISH_EVENT_SHAPE_2	: grpImage.Generate("D:/Ymir Work/UI/minigame/fish_event/fish_2.sub"),
			app.FISH_EVENT_SHAPE_3	: grpImage.Generate("D:/Ymir Work/UI/minigame/fish_event/fish_3.sub"),
			app.FISH_EVENT_SHAPE_4	: grpImage.Generate("D:/Ymir Work/UI/minigame/fish_event/fish_4.sub"),
			app.FISH_EVENT_SHAPE_5	: grpImage.Generate("D:/Ymir Work/UI/minigame/fish_event/fish_5.sub"),
			app.FISH_EVENT_SHAPE_6	: grpImage.Generate("D:/Ymir Work/UI/minigame/fish_event/fish_6.sub"),
			app.FISH_EVENT_SHAPE_7	: grpImage.Generate("D:/Ymir Work/UI/minigame/fish_event/fish_7.sub"),
		}
		self.fishPieceAdjustPosDict = {
			app.FISH_EVENT_SHAPE_1	: (0, -32),
			app.FISH_EVENT_SHAPE_2	: (0, 0),
			app.FISH_EVENT_SHAPE_3	: (-16, -16),
			app.FISH_EVENT_SHAPE_4	: (-16, -16),
			app.FISH_EVENT_SHAPE_5	: (-16, -16),
			app.FISH_EVENT_SHAPE_6	: (-32, -16),
			app.FISH_EVENT_SHAPE_7	: (-32, -16),
		}
		self.fishPieceSizeDict = {
			app.FISH_EVENT_SHAPE_1	: (1, 3),
			app.FISH_EVENT_SHAPE_2	: (1, 1),
			app.FISH_EVENT_SHAPE_3	: (2, 2),
			app.FISH_EVENT_SHAPE_4	: (2, 2),
			app.FISH_EVENT_SHAPE_5	: (2, 2),
			app.FISH_EVENT_SHAPE_6	: (3, 2),
			app.FISH_EVENT_SHAPE_7	: (3, 2),
		}
		
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
	def SetMiniGameFish(self, mini_game_fish):
		self.MiniGameFish = mini_game_fish
		
	def SetInven(self, inven):
		self.inven = inven
		
	def BindInterface(self, interface):
		self.interface = interface
		
	def SetItemToolTip(self, tooltip):
		self.tooltipitem = tooltip
		
	def __LoadWindow(self):
	
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			LoadScript(self, "UIScript/MiniGameFishGamePage.py")
			
		except:
			import exception
			exception.Abort("FishEventGamePage.LoadWindow.LoadObject")
			
		try:
			self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("help_button").SetEvent(ui.__mem_func__(self.__ClickHelpButton))
				
			# special item slot
			special_item_slot = self.GetChild("SpecialItemSlot")
			special_item_slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__SelectEmptySlot), SPECIAL_TYPE)
			special_item_slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem), SPECIAL_TYPE)
			special_item_slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			special_item_slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot), SPECIAL_TYPE)
			special_item_slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__UnselectItemSlot), SPECIAL_TYPE)
			self.fish_box_slot[SPECIAL_TYPE] = special_item_slot
			
			# normal item slot
			normal_item_slot = self.GetChild("NormalItemSlot")
			normal_item_slot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__SelectEmptySlot), NORMAL_TYPE)
			normal_item_slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem), NORMAL_TYPE)
			normal_item_slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			normal_item_slot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot), NORMAL_TYPE)
			normal_item_slot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__UnselectItemSlot), NORMAL_TYPE)
			self.fish_box_slot[NORMAL_TYPE] = normal_item_slot
			
			self.grid_slot = self.GetChild("GameSlot")
			self.grid_slot.SetSelectEmptySlotEvent( ui.__mem_func__(self.__SelectEmptyGameSlot) )
			self.grid_slot.SetUnselectEmptySlotEvent( ui.__mem_func__(self.__UnselectEmptyGameSlot) )
			self.grid_slot.SetUnselectItemSlotEvent( ui.__mem_func__(self.__UnselectItemGameSlotEvent) )
			
			self.use_count_text = self.GetChild("use_count_text")
			self.use_count_text.SetText( str(self.use_count) )
			
			## score completion side effect
			self.score_effect1 = self.GetChild("score_completion_effect1")
			self.score_effect2 = self.GetChild("score_completion_effect2")
			self.score_effect3 = self.GetChild("score_completion_effect3")
			self.score_effect1.SetScale(1.2, 1.2)
			self.score_effect2.SetScale(1.2, 1.2)
			self.score_effect3.SetScale(1.2, 1.2)
			self.score_effect1.Hide()
			self.score_effect2.Hide()
			self.score_effect3.Hide()
			self.score_effect1.SetEndFrameEvent( ui.__mem_func__(self.__ScoreEffectEndFrameEvent1) )
			self.score_effect2.SetEndFrameEvent( ui.__mem_func__(self.__ScoreEffectEndFrameEvent2) )
			self.score_effect3.SetEndFrameEvent( ui.__mem_func__(self.__ScoreEffectEndFrameEvent3) )
			
			## score completion text effect
			self.score_text_effect = self.GetChild("score_completion_text_effect")
			self.score_text_effect.SetEndFrameEvent( ui.__mem_func__(self.__ScoreTextEffectEndFrameEvent) )
			self.score_text_effect.Hide()
			
			if localeInfo.IsARABIC():
				(x1, y1) = self.score_effect1.GetLocalPosition()
				self.score_effect1.SetPosition(x1+60, y1)
				self.score_effect1.SetWindowHorizontalAlignLeft()
				
				(x2, y2) = self.score_effect2.GetLocalPosition()
				self.score_effect2.SetPosition(x2+60, y2)
				self.score_effect2.SetWindowHorizontalAlignLeft()
				
				(x3, y3) = self.score_effect3.GetLocalPosition()
				self.score_effect3.SetPosition(x3+60, y3)
				self.score_effect3.SetWindowHorizontalAlignLeft()

				(e_x, e_y) = self.score_text_effect.GetLocalPosition()
				self.score_text_effect.SetPosition(e_x+60, e_y)
				self.score_text_effect.SetWindowHorizontalAlignLeft()
				
				(s_x, s_y) = self.GetChild("SpecialItemSlotBG").GetLocalPosition()
				special_item_slot.SetPosition(s_x-7, s_y+7)
				special_item_slot.SetWindowHorizontalAlignRight()
				(n_x, n_y) = self.GetChild("NormalItemSlotBG").GetLocalPosition()
				normal_item_slot.SetPosition(n_x-7, n_y+7)
				normal_item_slot.SetWindowHorizontalAlignRight()

		except:
			import exception
			exception.Abort("FishEventGamePage.LoadWindow.BindObject")
		
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Close(self):
		if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
			return
			
		self.SetOnTopWindowNone()
			
		self.ClearFishBoxSlot()
		app.ShowCursor()
		
		if self.tooltipitem:
			self.tooltipitem.HideToolTip()
			
		if self.popup:
			self.popup.Close()
			
		self.Hide()
		
	def Destroy(self):
		self.ClearFishBoxSlot()
		
		if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
			self.__DropAccept()
			
		self.isLoaded				= 0
		self.MiniGameFish			= None
			
		if self.fish_box_slot:
			del self.fish_box_slot[:]
		if self.fish_box_slot_pos:
			del self.fish_box_slot_pos[:]
			
		self.tooltipitem			= None
		self.inven					= None
		self.grid_slot				= None
		self.shape					= 0
		self.popup					= None
		self.use_count_text			= None
		self.score_text_effect		= None
		self.score_effect1			= None
		self.score_effect2			= None
		self.score_effect3			= None
		self.reward_vnum			= 0
		for i in self.fishPieceDict.values():
			grpImage.Delete(i)

	def SetOnTopWindowNone(self):
		if not self.interface:
			return
			
		self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_NONE)
		self.interface.RefreshMarkInventoryBag()
		
	def OnTop(self):
		if not self.interface:
			return
			
		self.interface.SetOnTopWindow(playerm2g2.ON_TOP_WND_FISH_EVENT)
		self.interface.RefreshMarkInventoryBag()
		
	def Show(self):
		ui.ScriptWindow.Show(self)
		
		if 0 == self.use_count:
			m2netm2g.SendRequestFishEventBlock()
		
		mouseModule.mouseController.DeattachObjectPostProcess()	
		## 인벤토리에서 ITEM_FISH_EVENT_BOX, ITEM_FISH_EVENT_BOX_SPECIAL 를 찾는다.
		## 존재한다면 slot 에 등록 시켜준다.
		special_item_pos	= playerm2g2.GetFishEventItemPos(ITEM_FISH_EVENT_BOX_SPECIAL)
		self.__AddFishEventSlot(SPECIAL_TYPE, special_item_pos)
		normal_item_pos		= playerm2g2.GetFishEventItemPos(ITEM_FISH_EVENT_BOX)
		self.__AddFishEventSlot(NORMAL_TYPE, normal_item_pos)
				
			
	def __ClickHelpButton(self):
		if playerm2g2.SLOT_TYPE_FISH_EVENT == mouseModule.mouseController.GetAttachedType():
			return
			
		global fish_event_game_state
		fish_event_game_state = STATE_WAITING
		self.Close()
		
		if self.MiniGameFish:
			self.MiniGameFish.Open()
			
	def OverInItem(self, slotIndex, type):
		if self.tooltipitem and self.fish_box_slot_pos[type] != -1:
			self.tooltipitem.SetInventoryItem( self.fish_box_slot_pos[type] )
				
	def	OverOutItem(self):
		if self.tooltipitem:
			self.tooltipitem.HideToolTip()
			
	def __UnselectItemSlot(self, slotIndex, type):
	
		if mouseModule.mouseController.isAttached():
			return
			
		if self.question_dialog:
			if self.question_dialog.IsShow():
				return
			
		self.ClearFishBoxSlot(type)
		
			
	def __UnselectEmptyGameSlot(self, slotIndex):
		
		if not mouseModule.mouseController.isAttached():
			return
			
		self.DropQuestionDialog()

		
	def	__UnselectItemGameSlotEvent(self, slotIndex):
		
		if not mouseModule.mouseController.isAttached():
			return
			
		self.DropQuestionDialog()
				
	
	def __AddFishEventSlot(self, type, pos):
		if -1 != self.fish_box_slot_pos[type]:
			return
			
		item_vnum  = playerm2g2.GetItemIndex(playerm2g2.INVENTORY, pos)
		item_count = playerm2g2.GetItemCount(playerm2g2.INVENTORY, pos)
		
		self.fish_box_slot_pos[type]	= pos
		self.fish_box_slot[type].SetItemSlot(0, item_vnum, item_count)
		self.fish_box_slot[type].ActivateSlot(0)
		self.fish_box_slot[type].RefreshSlot()
		
	def __SelectEmptySlot(self, slotIndex, type):
		if not mouseModule.mouseController.isAttached():
			return
		
		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
		attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
		
		if playerm2g2.SLOT_TYPE_INVENTORY != attachedSlotType:
			return
			
		mouseModule.mouseController.DeattachObject()
		if attachedSlotPos >= playerm2g2.ITEM_SLOT_COUNT:
			return
			
		if NORMAL_TYPE == type:
			if ITEM_FISH_EVENT_BOX != attachedItemIndex:
				return
		elif SPECIAL_TYPE == type:
			if ITEM_FISH_EVENT_BOX_SPECIAL != attachedItemIndex:
				return
		else:
			return
					
		item_count = playerm2g2.GetItemCount(playerm2g2.INVENTORY, attachedSlotPos)
		
		self.fish_box_slot_pos[type]	= attachedSlotPos
		self.fish_box_slot[type].SetItemSlot(0, attachedItemIndex, item_count)
		self.fish_box_slot[type].ActivateSlot(0)
		self.fish_box_slot[type].RefreshSlot()
		
	def __SelectEmptyGameSlot(self,	slotIndex):
		
		if not mouseModule.mouseController.isAttached():
			return
			
		if 0 == self.shape:
			return
		
		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		if playerm2g2.SLOT_TYPE_FISH_EVENT != attachedSlotType:
			return
			
		if self.question_dialog:
			self.question_dialog.Close()
			del self.question_dialog
			
		self.question_dialog = uiCommon.QuestionDialog()
		self.question_dialog.SetAcceptEvent(lambda arg = slotIndex : ui.__mem_func__(self.__AddAccept)(arg) )
		self.question_dialog.SetCancelEvent(ui.__mem_func__(self.__QuestionCancel))
		self.question_dialog.SetText( localeInfo.MINIGAME_FISH_EVENT_ADD_ACCEPT )
		self.question_dialog.Open()
		mouseModule.mouseController.SetAttachedIconRender(False)
		app.ShowCursor()
		
		if self.grid_slot:
			self.grid_slot.SetPickedAreaRender(False)
		
	def __AddAccept(self, slotIndex):
		self.__QuestionCancel()
		m2netm2g.SendAddFishBox( slotIndex, self.shape)
		self.shape = 0
		self.DeattachObject()
		
	def MiniGameFishAdd(self, pos, shape):
			
		img = grpImage.GetGraphicImagePointer( self.fishPieceDict[shape] )
		(width, height) = self.fishPieceSizeDict[shape]
		self.grid_slot.SetSlot(pos, shape, width, height, img)
		self.grid_slot.RefreshSlot()	
		
	## 이펙트 추가로 인해 clear 와 popup 은 이펙트 종료 후 발생
	def MiniGameFishReward(self, vnum):
		
		self.reward_vnum = vnum
		self.__ClearCompletionEffect()
		if self.score_effect1:
			self.score_effect1.Show()
		if self.score_effect2:
			self.score_effect2.Show()
		if self.score_effect3:
			self.score_effect3.Show()
		if self.score_text_effect:
			self.score_text_effect.Show()
			
	
	def MiniGameFishCount(self, count):
		
		self.use_count = count
		if self.use_count_text:
			self.use_count_text.SetText( str(self.use_count) )
		
	def OnUpdate(self):
		if 0 == self.isLoaded:
			return
			
		if not self.inven:
			return
			
		for type in range(1, FISH_EVENT_TYPE_MAX):
			if self.fish_box_slot_pos[type] == -1:
				continue
				
			invenPage = self.inven.GetInventoryPageIndex() ## 0 or 1
			
			min_range = invenPage * playerm2g2.INVENTORY_PAGE_SIZE			## 0 or 45
			max_range = (invenPage + 1) * playerm2g2.INVENTORY_PAGE_SIZE	## 45 or 90
				
			inven_slot_pos = self.fish_box_slot_pos[type]
			if min_range <= inven_slot_pos < max_range:
				inven_slot_pos = inven_slot_pos - min_range
				if self.inven.wndItem:
					self.inven.wndItem.SetCantMouseEventSlot(inven_slot_pos)
			
	def ClearFishBoxSlot(self, type = FISH_EVENT_TYPE_MAX):
		if not self.inven:
			return
			
		if FISH_EVENT_TYPE_MAX == type:
			for index in range(1, FISH_EVENT_TYPE_MAX):
				if not self.fish_box_slot[index]:
					continue
				
				if self.fish_box_slot_pos[index] == -1:
					continue
				
				inven_slot_pos = self.fish_box_slot_pos[index]
					
				if inven_slot_pos >= playerm2g2.INVENTORY_PAGE_SIZE:
					
					if app.ENABLE_EXTEND_INVEN_SYSTEM:
						inven_page = self.inven.GetInventoryPageIndex()
						inven_slot_pos -= (inven_page * playerm2g2.INVENTORY_PAGE_SIZE)
					else:
						inven_slot_pos -= playerm2g2.INVENTORY_PAGE_SIZE
							
				self.fish_box_slot[index].SetItemSlot(0, 0)
				self.fish_box_slot[index].DeactivateSlot(0)
				self.fish_box_slot[index].RefreshSlot()
				self.fish_box_slot_pos[index]	= -1
				
				if self.inven.wndItem:
					self.inven.wndItem.SetCanMouseEventSlot(inven_slot_pos)
			
		else:	
			if not self.fish_box_slot[type]:
				return
			
			if self.fish_box_slot_pos[type] == -1:
				return		
			
			inven_slot_pos = self.fish_box_slot_pos[type]
				
			if inven_slot_pos >= playerm2g2.INVENTORY_PAGE_SIZE:
				
				if app.ENABLE_EXTEND_INVEN_SYSTEM:
					inven_page = self.inven.GetInventoryPageIndex()
					inven_slot_pos -= (inven_page * playerm2g2.INVENTORY_PAGE_SIZE)
				else:
					inven_slot_pos -= playerm2g2.INVENTORY_PAGE_SIZE
						
			self.fish_box_slot[type].SetItemSlot(0, 0)
			self.fish_box_slot[type].DeactivateSlot(0)
			self.fish_box_slot[type].RefreshSlot()
			self.fish_box_slot_pos[type]	= -1
			
			if self.inven.wndItem:
				self.inven.wndItem.SetCanMouseEventSlot(inven_slot_pos)
					
					
	def SelectItemSlot(self, slotIndex, type):
		if 0 != self.shape:
			return
			
		mouseModule.mouseController.DeattachObject()
			
		if self.question_dialog:
			self.question_dialog.Close()
			del self.question_dialog
			
		self.question_dialog = uiCommon.QuestionDialog()
		self.question_dialog.SetAcceptEvent( lambda arg = type : ui.__mem_func__(self.__UseAccept)(arg) )
		self.question_dialog.SetCancelEvent(ui.__mem_func__(self.__UseAcceptCancel))
		self.question_dialog.SetText( localeInfo.MINIGAME_FISH_EVENT_USE_ACCEPT )
		self.question_dialog.Open()
		
	
	def __UseAccept(self, type):
		self.__QuestionCancel()
		if self.fish_box_slot_pos[type] != -1:
			m2netm2g.SendUseFishBox( playerm2g2.SLOT_TYPE_INVENTORY, self.fish_box_slot_pos[type] )
			
	def __UseAcceptCancel(self):
		if self.question_dialog:
			self.question_dialog.Close()
			self.question_dialog = None
			
	def __QuestionCancel(self):
		if self.question_dialog:
			self.question_dialog.Close()
			self.question_dialog = None
			
		if self.grid_slot:
			self.grid_slot.SetPickedAreaRender(True)
			
		mouseModule.mouseController.SetAttachedIconRender(True)
		app.HideCursor()
			
	def DropQuestionDialog(self):
		if self.question_dialog:
			self.question_dialog.Close()
			del self.question_dialog
			
		self.question_dialog = uiCommon.QuestionDialog()
		self.question_dialog.SetAcceptEvent(ui.__mem_func__(self.__DropAccept))
		self.question_dialog.SetCancelEvent(ui.__mem_func__(self.__QuestionCancel))
		self.question_dialog.SetText( localeInfo.MINIGAME_FISH_EVENT_DROP_ACCEPT )
		self.question_dialog.Open()
		self.question_dialog.SetTop()
		mouseModule.mouseController.SetAttachedIconRender(False)
		app.ShowCursor()
		
		if self.grid_slot:
			self.grid_slot.SetPickedAreaRender(False)
		
	def __DropAccept(self):
		self.__QuestionCancel()
		self.shape = 0
		app.ShowCursor()
		wndMgr.SetDisableDeattach(False)
		self.DeattachObject()
		
				
	def MiniGameFishUse(self, window, pos, shape):
		self.shape = shape
		
		for index in range(1, FISH_EVENT_TYPE_MAX):
			item_count = playerm2g2.GetItemCount(window, self.fish_box_slot_pos[index])
			item_vnum  = playerm2g2.GetItemIndex(window, self.fish_box_slot_pos[index])
			
			if 0 == item_count:
				self.ClearFishBoxSlot(index)
			else:
				self.fish_box_slot[index].SetItemSlot(0, item_vnum, item_count)
				self.fish_box_slot[index].RefreshSlot()
		
		app.HideCursor()
		(adjust_x, adjust_y) = self.fishPieceAdjustPosDict[shape]
		(width, height) = self.fishPieceSizeDict[shape]
		mouseModule.mouseController.AttachFishPiece( self, shape, self.fishPieceDict[shape], adjust_x, adjust_y, width, height)
		
		for type in range(1, FISH_EVENT_TYPE_MAX):
			self.fish_box_slot[type].DeactivateSlot(0)
			
		wndMgr.SetDisableDeattach(True)
		
		self.use_count += 1
		if self.use_count_text:
			self.use_count_text.SetText( str(self.use_count) )
		
	def DeattachObject(self):
		mouseModule.mouseController.DeattachObjectPostProcess()
		
		for type in range(1, FISH_EVENT_TYPE_MAX):
			item_count = playerm2g2.GetItemCount(playerm2g2.INVENTORY, self.fish_box_slot_pos[type])
			if item_count:
				self.fish_box_slot[type].ActivateSlot(0)
			else:
				self.fish_box_slot[type].DeactivateSlot(0)
	
	def __ScoreEffectEndFrameEvent1(self):
		if self.score_effect1:
			self.score_effect1.Hide()
		
	def __ScoreEffectEndFrameEvent2(self):
		if self.score_effect2:
			self.score_effect2.Hide()
		
	def __ScoreEffectEndFrameEvent3(self):
		if self.score_effect3:
			self.score_effect3.Hide()
						
	def __ScoreTextEffectEndFrameEvent(self):
		
		if self.score_text_effect: 
			self.score_text_effect.Hide()
			
		self.use_count = 0
		if self.use_count_text:
			self.use_count_text.SetText( str(self.use_count) )
		
		for slotPos in xrange(self.grid_slot.GetSlotCount()):
			self.grid_slot.ClearSlot(slotPos)
		self.grid_slot.RefreshSlot()
		
		if not self.popup:
			self.popup = uiCommon.PopupDialog()
			
		item.SelectItem(self.reward_vnum)
		item_name = item.GetItemName()
		self.popup.SetText( localeInfo.MINIGAME_FISH_EVENT_REWARD_MSG % item_name )
		self.popup.Open()
		self.reward_vnum = 0
		
	def __ClearCompletionEffect(self):
		if self.score_text_effect:
			self.score_text_effect.Hide()
			self.score_text_effect.ResetFrame()
			self.score_text_effect.SetDelay(6)
		
		if self.score_effect1:
			self.score_effect1.Hide()
			self.score_effect1.ResetFrame()
			self.score_effect1.SetDelay(6)
		
		if self.score_effect2:
			self.score_effect2.Hide()
			self.score_effect2.ResetFrame()
			self.score_effect2.SetDelay(6)
		
		if self.score_effect3:
			self.score_effect3.Hide()
			self.score_effect3.ResetFrame()
			self.score_effect3.SetDelay(6)
			
		
class MiniGameFish(ui.Window):
			
	def __init__(self):
		ui.Window.__init__(self)
		self.isLoaded		= 0
		
		self.cur_page		= None
		self.waiting_page	= None
		self.game_page		= None
		self.inven			= None
		self.tooltipitem	= None
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.Window.__del__(self)
		
	def Show(self):
		self.__LoadWindow()
		ui.Window.Show(self)
		        
	def Close(self):
		self.Hide()
		
		if self.cur_page:
			self.cur_page.Close()

	def Destroy(self):
		global fish_event_game_state
		fish_event_game_state	= STATE_NONE
		self.isLoaded			= 0
		self.cur_page			= None
		self.inven				= None
		self.interface			= None
		self.tooltipitem		= None
		if self.waiting_page:
			self.waiting_page.Destroy()
			
		if self.game_page:
			self.game_page.Destroy()
		
	def __LoadWindow(self):
		
		if self.isLoaded == 1:
			return
			
		self.isLoaded	= 1
		global fish_event_game_state
		fish_event_game_state		= STATE_WAITING
		
		try:
			## 게임 설명창
			self.waiting_page	= FishEventGameWaitingPage()
			self.waiting_page.SetMiniGameFish(self)
			
			## 게임 진행창
			self.game_page		= FishEventGamePage()
			self.game_page.SetMiniGameFish(self)
		except:
			import exception
			exception.Abort("MiniGameFish.LoadWindow")
		
		self.Hide()
			
			
	def SetInven(self, inven):
		self.inven = inven
		
		if self.game_page:
			self.game_page.SetInven(self.inven)
			
	def BindInterface(self, interface):
		self.interface = interface
		
		if self.game_page:
			self.game_page.BindInterface(self.interface)
			
	def SetItemToolTip(self, tooltip):
		self.tooltipitem = tooltip
		
		if self.game_page:
			self.game_page.SetItemToolTip( self.tooltipitem )
		
	def Open(self):
		global fish_event_game_state
		
		if STATE_WAITING == fish_event_game_state:
			self.cur_page = self.waiting_page
			
		elif STATE_PLAY == fish_event_game_state:
			self.cur_page = self.game_page
			
		else:
			return
			
		if self.cur_page.IsShow():
			self.cur_page.Close()
		else:
			self.cur_page.Show()
			self.cur_page.SetTop()
	
	def MiniGameFishUse(self, window, pos, shape):
		
		if STATE_PLAY != fish_event_game_state:
			return
			
		self.cur_page.MiniGameFishUse(window, pos, shape)
		
		
	def MiniGameFishAdd(self, pos, shape):
			
		if STATE_PLAY != fish_event_game_state:
			return
			
		self.cur_page.MiniGameFishAdd( pos, shape )
		
	def MiniGameFishReward(self, vnum):
	
		if STATE_PLAY != fish_event_game_state:
			return
			
		self.cur_page.MiniGameFishReward( vnum )
		
	def MiniGameFishCount(self, count):
	
		if STATE_PLAY != fish_event_game_state:
			return
			
		self.cur_page.MiniGameFishCount( count )
		
	def CantFishEventSlot(self, InvenSlot):
		ItemVnum = playerm2g2.GetItemIndex(InvenSlot)
		if ItemVnum in [ITEM_FISH_EVENT_BOX, ITEM_FISH_EVENT_BOX_SPECIAL]:
			return False
				
		return True