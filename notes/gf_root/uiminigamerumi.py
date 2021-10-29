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

from collections import deque

STATE_NONE		= 0
STATE_WAITING	= 1
STATE_PLAY		= 2


SHOW_LINE_COUNT_MAX = 18
DEFAULT_DESC_Y	= 7

CARD_IMG_WIDTH	= 38
CARD_IMG_HEIGHT = 52

NONE_POS		= 0
DECK_CARD		= 1
HAND_CARD		= 2
FIELD_CARD		= 3
CARD_POS_MAX	= 4

DECK_CARD_INDEX_MAX		= 3
HAND_CARD_INDEX_MAX		= 5
FIELD_CARD_INDEX_MAX	= 3
	
EMPTY_CARD	= 00
RED_CARD	= 10
BLUE_CARD	= 20
YELLOW_CARD = 30


CARD_COLOR_MAX		= 3	# 카드 색상 개수
CARD_NUMBER_END		= 8 # 한 색상당 카드 숫자
DECK_COUNT_MAX		= CARD_COLOR_MAX * CARD_NUMBER_END

CARD_MOVE_SPEED		= 25.0

DECK_FLUSH_IMG_GAP_X	= 2
DECK_FLUSH_IMG_GAP_Y	= 2

TOTAL_SCORE_LOW_FONT_COLOR = grp.GenerateColor(0.78, 0.78, 0.78, 1.0)
TOTAL_SCORE_MID_FONT_COLOR = grp.GenerateColor(1.0, 0.85, 0.39, 1.0)
TOTAL_SCORE_HIGH_FONT_COLOR = grp.GenerateColor(1.0, 0.0, 0.0, 1.0)

LOW_TOTAL_SCORE	= 300
MID_TOTAL_SCORE = 400

RUMI_ROOT = "d:/ymir work/ui/minigame/rumi/"
CARD_ROOT = "d:/ymir work/ui/minigame/rumi/card/"

CARD_IMG_DICT =  \
{
	RED_CARD + 1 : CARD_ROOT + "card_red_1.sub",
	RED_CARD + 2 : CARD_ROOT + "card_red_2.sub",
	RED_CARD + 3 : CARD_ROOT + "card_red_3.sub",
	RED_CARD + 4 : CARD_ROOT + "card_red_4.sub",
	RED_CARD + 5 : CARD_ROOT + "card_red_5.sub",
	RED_CARD + 6 : CARD_ROOT + "card_red_6.sub",
	RED_CARD + 7 : CARD_ROOT + "card_red_7.sub",
	RED_CARD + 8 : CARD_ROOT + "card_red_8.sub",
	
	BLUE_CARD + 1 : CARD_ROOT + "card_blue_1.sub",
	BLUE_CARD + 2 : CARD_ROOT + "card_blue_2.sub",
	BLUE_CARD + 3 : CARD_ROOT + "card_blue_3.sub",
	BLUE_CARD + 4 : CARD_ROOT + "card_blue_4.sub",
	BLUE_CARD + 5 : CARD_ROOT + "card_blue_5.sub",
	BLUE_CARD + 6 : CARD_ROOT + "card_blue_6.sub",
	BLUE_CARD + 7 : CARD_ROOT + "card_blue_7.sub",
	BLUE_CARD + 8 : CARD_ROOT + "card_blue_8.sub",
	
	YELLOW_CARD + 1 : CARD_ROOT + "card_yellow_1.sub",
	YELLOW_CARD + 2 : CARD_ROOT + "card_yellow_2.sub",
	YELLOW_CARD + 3 : CARD_ROOT + "card_yellow_3.sub",
	YELLOW_CARD + 4 : CARD_ROOT + "card_yellow_4.sub",
	YELLOW_CARD + 5 : CARD_ROOT + "card_yellow_5.sub",
	YELLOW_CARD + 6 : CARD_ROOT + "card_yellow_6.sub",
	YELLOW_CARD + 7 : CARD_ROOT + "card_yellow_7.sub",
	YELLOW_CARD + 8 : CARD_ROOT + "card_yellow_8.sub",
}

DECK_IMG_DICT = \
[
	RUMI_ROOT + "deck/deck1.sub",
	RUMI_ROOT + "deck/deck2.sub",
	RUMI_ROOT + "deck/deck3.sub",
]

def LoadScript(self, fileName):
	pyScrLoader = ui.PythonScriptLoader()
	pyScrLoader.LoadScriptFile(self, fileName)
	
	
class RumiWaitingPage(ui.ScriptWindow):

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
		self.scrollbar			= None
		self.descIndex			= -1
		self.desc_y				= DEFAULT_DESC_Y
		
		self.start_question_dialog = None
		
		self.confirm_window_check_button = None
		self.check_image = None
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __LoadWindow(self):
	
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			LoadScript(self, "UIScript/MiniGameRumiWaitingPage.py")
			
		except:
			import exception
			exception.Abort("MiniGameRumiWaitingPage.LoadWindow.LoadObject")
			
		try:
			self.GetChild("titlebar").SetCloseEvent( ui.__mem_func__(self.Close) )
			self.startButton	= self.GetChild("game_start_button")
			self.startButton.SetEvent(ui.__mem_func__(self.__ClickStartButton))
			
			self.descBoard		= self.GetChild("desc_board")
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Show()
			
			self.scrollbar		= self.GetChild("scrollbar")
			self.scrollbar.SetPos(0.0)
			self.scrollbar.SetScrollEvent(ui.__mem_func__(self.__OnScroll))
			self.scrollbar.SetUpScrollButtonEvent(ui.__mem_func__(self.__OnUpScrollButton))
			self.scrollbar.SetDownScrollButtonEvent(ui.__mem_func__(self.__OnDownScrollButton))
			self.scrollbar.SetEvnetFuncCall( False )
			
			self.confirm_window_check_button = self.GetChild("confirm_check_button")
			self.confirm_window_check_button.SetEvent(ui.__mem_func__(self.__ClickConfirmCheckButton), "mouse_click", 0)
			
			self.check_image = self.GetChild("check_image")
			self.check_image.Show()
			
			
			if localeInfo.IsARABIC():
				self.startButton.SetWindowHorizontalAlignLeft()
				start_button_width = self.startButton.GetWidth()
				(start_button_lx, start_button_ly) = self.startButton.GetLocalPosition()
				self.startButton.SetPosition(start_button_lx - start_button_width, start_button_ly)
				
				
				confirm_text_window = self.GetChild("confirm_check_button_text_window")
				confirm_text_window.SetWindowHorizontalAlignLeft()
				confirm_text_window_width = confirm_text_window.GetWidth()
				(confirm_text_window_lx, confirm_text_window_ly) = confirm_text_window.GetLocalPosition()
				confirm_text_window.SetPosition(confirm_text_window_lx - confirm_text_window_width - 24, confirm_text_window_ly - 4)
				
				
				confirm_text = self.GetChild("confirm_check_button_text")
				confirm_text.SetHorizontalAlignLeft()

				
				self.confirm_window_check_button.SetWindowHorizontalAlignLeft()
				confirm_check_button_width = self.confirm_window_check_button.GetWidth()
				(confirm_check_button_lx, confirm_check_button_ly) = self.confirm_window_check_button.GetLocalPosition()
				self.confirm_window_check_button.SetPosition(confirm_check_button_lx - confirm_check_button_width, confirm_check_button_ly)
				
				self.check_image.SetWindowHorizontalAlignLeft()
				check_image_width = self.check_image.GetWidth()
				(check_image_lx, check_image_ly) = self.check_image.GetLocalPosition()
				self.check_image.SetPosition(check_image_lx - check_image_width, check_image_ly)
			
			
		except:
			import exception
			exception.Abort("MiniGameRumiWaitingPage.LoadWindow.BindObject")
		
		self.Hide()
		
	def Close(self):
		self.Hide()
		self.CloseStartDlg()
		event.ClearEventSet(self.descIndex)
		self.descIndex = -1
		
		if self.descriptionBox:
			self.descriptionBox.Hide()
			
		if self.scrollbar:
			self.scrollbar.SetPos(0.0)
						
		self.desc_y					= DEFAULT_DESC_Y
		
	def Destroy(self):
		self.isLoaded				= 0
		self.startButton			= None
		self.descBoard				= None
		self.descriptionBox			= None
		self.scrollbar				= None
		self.descIndex				= -1
		
		self.desc_y					= DEFAULT_DESC_Y
		
		self.confirm_window_check_button = None
		self.check_image = None
		
		self.CloseStartDlg()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True	
		
	def GetConfirmWindowCheck(self):
		
		if self.check_image:
			if self.check_image.IsShow():
				return True
			else:
				return False
				
		return False
	
	def __ClickConfirmCheckButton(self):
	
		if self.check_image:
			if self.check_image.IsShow():
				self.check_image.Hide()
			else:
				self.check_image.Show()
				
	def __ClickStartButton(self):
	
		if None == self.start_question_dialog:
			self.start_question_dialog = uiCommon.QuestionDialog()
			self.start_question_dialog.SetText(localeInfo.MINI_GAME_RUMI_START_QUESTION % (30000, 1) )
			self.start_question_dialog.SetAcceptEvent(ui.__mem_func__(self.__StartAccept))
			self.start_question_dialog.SetCancelEvent(ui.__mem_func__(self.__StartCancel))
			w,h = self.start_question_dialog.GetTextSize()
			self.start_question_dialog.SetWidth( w + 60 )
			line_count = self.start_question_dialog.GetTextLineCount()
			
			if line_count > 1:
				height = self.start_question_dialog.GetLineHeight()
				self.start_question_dialog.SetLineHeight(height + 3)
				
		self.start_question_dialog.Open()
	
	def CloseStartDlg(self):
	
		if self.start_question_dialog:
			self.start_question_dialog.Close() 
			self.start_question_dialog	= None
	
	def __StartAccept(self):
	
		m2netm2g.SendMiniGameRumiStart()
	
	def __StartCancel(self):
	
		self.start_question_dialog.Close()
		
	def OnUpdate(self):
	
		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + 7, -(yposEventSet + self.desc_y))
		self.descriptionBox.SetIndex(self.descIndex)
				
	def Show(self):
		ui.ScriptWindow.Show(self)
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet( uiScriptLocale.MINIGAME_RUMI_DESC )
		
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
			
		event.SetVisibleLineCount(self.descIndex, SHOW_LINE_COUNT_MAX)
		
		if localeInfo.IsARABIC():
			event.SetEventSetWidth(self.descIndex, self.descBoard.GetWidth() - 20)

		event.SetRestrictedCount(self.descIndex, 60) #47 mainline 과 development 가 폰트체가 달라서
			
		event.AllProcesseEventSet(self.descIndex)
		
		total_line = event.GetProcessedLineCount(self.descIndex)
		total_line = max( 1, total_line)
		denominator = total_line / SHOW_LINE_COUNT_MAX - 1
		denominator = max(1, denominator)
		scroll_step	= 1.0 / denominator
		
		self.scrollbar.SetScrollStep(scroll_step)
		event.Skip(self.descIndex)
		
		if self.descriptionBox:
			self.descriptionBox.Show()
			
		if self.check_image:
			self.check_image.Show()		
		
	def __OnScroll(self):
		
		self.scrollBarPos = self.scrollbar.GetPos()
		
		if self.scrollBarPos < 0.5:
			self.PrevDescriptionPage()
		else:
			self.NextDescriptionPage()
		
		scroll_step = self.scrollbar.GetScrollStep()
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		page = cur_start_line / SHOW_LINE_COUNT_MAX

		self.scrollbar.SetPos( scroll_step * page, False)
		
		
	def __OnUpScrollButton(self):
	
		self.PrevDescriptionPage()
		return
	
	def __OnDownScrollButton(self):
		
		self.NextDescriptionPage()
		return
	
	def PrevDescriptionPage(self):
		
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		decrease_count = SHOW_LINE_COUNT_MAX
		
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
		
		increase_count = SHOW_LINE_COUNT_MAX
		
		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return
		
		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.desc_y -= ( line_height * increase_count )
			
	

class RumiGamePage(ui.ScriptWindow):
	
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		
		self.isLoaded	= 0
		self.card_slot	= [None]
		
		self.card_img_handle_dict	= {}
		self.card_img_dict			= {}
		
		self.cur_score_text		= None
		self.cur_score			= 0
		self.total_score_text	= None
		self.total_score		= 0
		
		self.deck_card_cnt_text = None
		self.deck_card_cnt		= 0
		
		self.hand_card_cnt		= 0
		self.field_card_cnt		= 0
		
		self.score_text_effect	= None
		
		self.score_effect1		= None
		self.score_effect2		= None
		self.score_effect3		= None
		
		self.deck_flush_effect	= None
		self.lock				= False
		
		self.move_img			= None
		self.deck_cur_index		= DECK_CARD_INDEX_MAX - 1
		
		self.card_move_queue	= deque()
		
		self.exit_question_dialog = None
		
		self.confirm_window_on		= True
		self.discard_confirm_dialog = None
		self.discard_index			= -1
		
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			self.back_ground		= None

		self.__LoadWindow()
		
		
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
		self.card_slot	= [None]
		self.__DeleteCardImg()
		
		self.cur_score_text		= None
		self.cur_score			= 0
		self.total_score_text	= None
		self.total_score		= 0
		
		self.deck_card_cnt_text = None
		self.deck_card_cnt		= 0
		self.hand_card_cnt		= 0
		self.field_card_cnt		= 0
		
		self.score_text_effect	= None
		
		self.score_effect1		= None
		self.score_effect2		= None
		self.score_effect3		= None
		
		self.deck_flush_effect	= None
		self.lock				= False
		
		self.move_img			= None
		
		self.deck_cur_index		= DECK_CARD_INDEX_MAX - 1
		
		self.confirm_window_on		= True
		if self.discard_confirm_dialog:
			self.discard_confirm_dialog.Close()
		self.discard_confirm_dialog = None
		self.discard_index			= -1
		
		if self.card_move_queue:
			self.card_move_queue.clear()
			
		self.__CloseExitQuestionDialog()
		
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			self.back_ground		= None
		
	def __DeleteCardImg(self):
		
		for i in self.card_img_handle_dict.values():
			grpImage.Delete(i)
		self.card_img_handle_dict.clear()
		self.card_img_dict.clear()
		
	def __LoadWindow(self):
	
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			LoadScript(self, "UIScript/MiniGameRumiGamePage.py")
			
		except:
			import exception
			exception.Abort("MiniGameRumiGamePage.LoadWindow.LoadObject")
			
		try:
			self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("game_exit_button").SetEvent(ui.__mem_func__(self.__ExitButtonClick))
			self.cur_score_text	= self.GetChild("score_number_text")
			self.cur_score_text.SetText("")
			self.cur_score = 0
			self.total_score_text = self.GetChild("total_score")
			self.cur_score_text.SetText("0")
			self.total_score = 0
			self.deck_card_cnt_text = self.GetChild("card_cnt_text")
			
			## Deck
			deck_card_slot = self.GetChild("DeckCardSlot")
			deck_card_slot.SAFE_SetButtonEvent("LEFT", "ALWAYS", self.LButtonClickDeck)
			self.card_slot.append( deck_card_slot )
			
			## Hand
			hand_card_slot = self.GetChild("HandCardSlot")
			hand_card_slot.SAFE_SetButtonEvent("LEFT", "EXIST", self.LButtonClickHand)
			hand_card_slot.SAFE_SetButtonEvent("RIGHT", "EXIST", self.RButtonClickHand)
			self.card_slot.append( hand_card_slot )
			
			## Field
			field_card_slot = self.GetChild("FieldCardSlot")
			field_card_slot.SAFE_SetButtonEvent("LEFT", "EXIST", self.LButtonClickField)
			self.card_slot.append( field_card_slot )
			
			## score completion text effect
			self.score_text_effect = self.GetChild("score_completion_text_effect")
			self.score_text_effect.SetEndFrameEvent( ui.__mem_func__(self.__ScoreTextEffectEndFrameEvent) )
			self.score_text_effect.Hide()
			
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
			
			self.score_effect1.SetKeyFrameEvent( ui.__mem_func__(self.__ScoreEffectKeyFrameEvent1) )
			self.score_effect2.SetKeyFrameEvent( ui.__mem_func__(self.__ScoreEffectKeyFrameEvent2) )
			
			
			self.__ClearScoreCompletionEffect()
			
			## deck flush effect
			self.deck_flush_effect = self.GetChild("deck_flush_effect")
			self.deck_flush_effect.Hide()
			self.__ClearDeckFlushEffect()
			
			## 카드이미지 로드
			self.__LoadCardImage()
			
			##### 카드 애니메이션에 사용될 move image 한장 생성.	
			self.move_img = ui.MoveImageBox()
			self.move_img.SetParent( self.GetChild("board") )
			self.move_img.SetEndMoveEvent( ui.__mem_func__(self.CardMoveEndEvnet) )
			self.move_img.SetMoveSpeed(CARD_MOVE_SPEED)
			self.move_img.Hide()
			#####
			
			total_score_text_window = self.GetChild("total_score_text")
			total_score_text_window.SetWindowHorizontalAlignRight()
			
			if app.ENABLE_MINI_GAME_OKEY_NORMAL:
				self.back_ground = ui.ExpandedImageBox()
				self.back_ground.SetParent( self.GetChild("BG") )
				self.back_ground.LoadImage("d:/ymir work/ui/minigame/rumi_nor/rumi_nor_bg.tga")
				self.back_ground.Hide()

			if localeInfo.IsARABIC():
				## score completion effect adjust
				self.score_text_effect.SetWindowHorizontalAlignLeft()
				self.score_effect1.SetWindowHorizontalAlignLeft()
				self.score_effect2.SetWindowHorizontalAlignLeft()
				self.score_effect3.SetWindowHorizontalAlignLeft()
				
				## deck flush effect adjust
				self.deck_flush_effect.SetWindowHorizontalAlignLeft()
				
				## text adjust
				## score
				score_window = self.GetChild("score_window")
				score_window.SetWindowHorizontalAlignLeft()
				score_window_width = score_window.GetWidth()
				(score_lx, score_ly) = score_window.GetLocalPosition()
				score_window.SetPosition(score_lx - score_window_width, score_ly)
				## cross(X) text
				cross_text_window = self.GetChild("cross_text_window")
				cross_text_window.SetWindowHorizontalAlignLeft()
				cross_text_window_width = cross_text_window.GetWidth()
				(cross_text_window_lx, cross_text_window_ly) = cross_text_window.GetLocalPosition()
				cross_text_window.SetPosition(cross_text_window_lx - cross_text_window_width, cross_text_window_ly)
				## card count text
				card_cnt_window = self.GetChild("card_cnt_window")
				card_cnt_window.SetWindowHorizontalAlignLeft()
				card_cnt_window_width = card_cnt_window.GetWidth()
				(card_cnt_window_lx, card_cnt_window_ly) = card_cnt_window.GetLocalPosition()
				card_cnt_window.SetPosition(card_cnt_window_lx - card_cnt_window_width, card_cnt_window_ly)
				## total_score_text
				total_score_text_window = self.GetChild("total_score_text_window")
				total_score_text_window.SetWindowHorizontalAlignLeft()
				total_score_text_width = total_score_text_window.GetWidth()
				(total_score_text_lx, total_score_text_ly) = total_score_text_window.GetLocalPosition()
				total_score_text_window.SetPosition(total_score_text_lx - total_score_text_width - 10, total_score_text_ly)
				## total_score
				total_score_window = self.GetChild("total_score_window")
				total_score_window.SetWindowHorizontalAlignLeft()
				total_score_width = total_score_window.GetWidth()
				(total_score_lx, total_score_ly) = total_score_window.GetLocalPosition()
				total_score_window.SetPosition(total_score_lx - total_score_width, total_score_ly)
				
				
		except:
			import exception
			exception.Abort("MiniGameRumiGamePage.LoadWindow.BindObject")
		
		self.Hide()
	
	def OnPressEscapeKey(self):
		self.Hide()
		return True
		
	def	SetConfirmWindowCheck(self, bFlag):
		
		self.confirm_window_on = bFlag
		
		
	def OnUpdate(self):
	
		## deck card flush 여부를 체크한다.
		self.__DeckFlushEffectCheck()
		
		## 카드 애니메이션 관련
		if len(self.card_move_queue) > 0:
		
			if False == self.move_img.GetMove():
				self.CardMoveStartEvent()
				
			else:
				(dst_pos, dst_index, dst_color, dst_number) = self.card_move_queue[0][1]
				(dstX, dstY) = self.card_slot[dst_pos].GetSlotGlobalPosition(dst_index)
				self.move_img.SetMovePosition(dstX, dstY)

		
	def CardMoveStartEvent(self):
				
		if len(self.card_move_queue) > 0:
			
			(src_pos, src_index, src_color, src_number) = self.card_move_queue[0][0]
			(dst_pos, dst_index, dst_color, dst_number) = self.card_move_queue[0][1]
			
			## Clear
			if DECK_CARD != src_pos:
				self.card_slot[src_pos].ClearSlot(src_index)
			
			## 이미지 셋팅
			self.move_img.LoadImage( CARD_IMG_DICT[dst_color + dst_number] )
			
			## 시작점 셋팅
			(local_x, local_y) = self.card_slot[src_pos].GetLocalPosition()
			if src_pos == DECK_CARD:
				src_index = self.deck_cur_index
			(slot_local_x, slot_local_y) = self.card_slot[src_pos].GetSlotLocalPosition(src_index)
			self.move_img.SetPosition( local_x + slot_local_x, local_y + slot_local_y)
		
			## 도착점 셋팅
			(dstX, dstY) = self.card_slot[dst_pos].GetSlotGlobalPosition(dst_index)
			self.move_img.SetMovePosition(dstX, dstY)
			
			## 덱 카드 숫자 차감
			if DECK_CARD == src_pos and HAND_CARD == dst_pos:
				self.SetDeckCount(self.deck_card_cnt - 1)
				
			## 시작
			self.move_img.Show()
			self.move_img.MoveStart()

				
	def CardMoveEndEvnet(self):
	
		if len(self.card_move_queue) > 0:
			
			[srcCard, dstCard] = self.card_move_queue.popleft()
			(dst_pos, dst_index, dst_color, dst_number) = dstCard
			
			self.card_slot[dst_pos].SetSlot( dst_index \
										, dst_index \
										, 1, 1 \
										, self.card_img_dict.get( dst_color + dst_number ) )
										
			self.move_img.Hide()
			
			if len(self.card_move_queue) == 0 \
				and False == self.score_text_effect.IsShow()\
				and False == self.score_effect1.IsShow()\
				and False == self.score_effect2.IsShow()\
				and False == self.score_effect3.IsShow():
				self.lock = False
				
	def Clear(self):
	
		self.__ClearDeckCardSlot()
		self.__ClearHandCardSlot()
		self.__ClearFieldCardSlot()
					
		self.__SetScore(0)
		self.__SetTotalScore(0)
		
		self.lock				= False
		
		self.confirm_window_on	= True
		self.discard_index		= -1
		
		self.__ClearScoreCompletionEffect()
		self.__ClearDeckFlushEffect()
		
		self.__HideAllDeckSlotBaseImage()
		
		self.__CloseExitQuestionDialog()
		
	def __ClearDeckCardSlot(self):
		for index in range(DECK_CARD_INDEX_MAX):
			self.card_slot[DECK_CARD].ClearSlot(index)
					
	def __ClearHandCardSlot(self):
		
		self.hand_card_cnt		= 0
		
		for index in range(HAND_CARD_INDEX_MAX):
			self.card_slot[HAND_CARD].ClearSlot(index)
			
	def __ClearFieldCardSlot(self):
		
		self.field_card_cnt		= 0
		
		for index in range(FIELD_CARD_INDEX_MAX):
			self.card_slot[FIELD_CARD].ClearSlot(index)
			
	def __ClearScoreCompletionEffect(self):
	
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
			
			
	def __ClearDeckFlushEffect(self):
	
		if not self.deck_flush_effect:
			return
			
		self.deck_flush_effect.ResetFrame()
		
	def __StartDeckFlushEffect(self):
	
		self.__ClearDeckFlushEffect()
		(local_x, local_y) = self.card_slot[DECK_CARD].GetLocalPosition()
		(slot_local_x, slot_local_y) = self.card_slot[DECK_CARD].GetSlotLocalPosition(self.deck_cur_index)
		
		## 카드 이미지와 flush 이미지의 width, height 가 다르다.
		## 그래서 gap 만큼 더 해줘야 한다.
		result_x = local_x + slot_local_x + DECK_FLUSH_IMG_GAP_X
		result_y = local_y + slot_local_y + DECK_FLUSH_IMG_GAP_Y
		
		self.deck_flush_effect.SetPosition(result_x, result_y)
		self.deck_flush_effect.Show()
		
	def __DeckFlushEffectCheck(self):
		
		if not self.deck_flush_effect:
			return
			
		if HAND_CARD_INDEX_MAX > self.hand_card_cnt \
			and 0 == self.field_card_cnt \
			and self.deck_card_cnt > 0:
		
			if False == self.deck_flush_effect.IsShow():
				self.__StartDeckFlushEffect()
			
		else:
			self.deck_flush_effect.Hide()	

	
	def __LoadCardImage(self):
	
		for key, value in CARD_IMG_DICT.items():
		
			img_handle = grpImage.Generate( value )
			img = grpImage.GetGraphicImagePointer(img_handle)
			
			self.card_img_handle_dict[key] = img_handle
			self.card_img_dict[key] = img										
	
	def RumiIncreaseScore(self, score, total_score):
		
		self.lock				= True
		
		self.__SetScore(score)
		self.__SetTotalScore(total_score)
		
		self.__ClearScoreCompletionEffect()
		self.score_effect1.Show()
		
	def RumiMoveCard(self, srcCard, dstCard):
	
		(src_pos, src_index, src_color, src_number) = srcCard
		(dst_pos, dst_index, dst_color, dst_number) = dstCard
			
		if not self.__IsExistSlotIndex(src_pos, src_index, src_color, src_number):
			return
			
		if not self.__IsExistSlotIndex(dst_pos, dst_index, dst_color, dst_number):
			return
			
		self.lock = True
		
		if DECK_CARD == src_pos and HAND_CARD == dst_pos:
			self.MoveCardDeckToHand(srcCard, dstCard)
			
		elif HAND_CARD == src_pos and FIELD_CARD == dst_pos:
			self.MoveCardHandToField(srcCard, dstCard)
		
		elif FIELD_CARD == src_pos and HAND_CARD == dst_pos:
			self.MoveCardFieldToHand(srcCard, dstCard)
				
		elif HAND_CARD == src_pos and NONE_POS == dst_pos:
			self.MoveCardHandToGrave(srcCard, dstCard)		
			
		else:
			self.lock = False
	
	## Deck -> Hand
	def	MoveCardDeckToHand(self, srcCard, dstCard):	
		
		self.hand_card_cnt = self.hand_card_cnt + 1
		self.card_move_queue.append([srcCard,dstCard])
			
	## Hand -> Field									
	def MoveCardHandToField(self, srcCard, dstCard):
		
		self.hand_card_cnt = self.hand_card_cnt - 1
		self.field_card_cnt = self.field_card_cnt + 1
		self.card_move_queue.append([srcCard,dstCard])
	
	## Field -> Hand
	def MoveCardFieldToHand(self, srcCard, dstCard):
		
		self.hand_card_cnt = self.hand_card_cnt + 1
		self.field_card_cnt = self.field_card_cnt - 1
		self.card_move_queue.append([srcCard,dstCard])	
	
	## Hand -> Grave, 핸드 카드 파괴									
	def MoveCardHandToGrave(self, srcCard, dstCard):
		
		self.hand_card_cnt = self.hand_card_cnt - 1
		(src_pos, src_index, src_color, src_number) = srcCard
		self.card_slot[src_pos].ClearSlot(src_index)
		self.lock = False
		
		
	def __IsExistSlotIndex(self, card_pos, slot_index, color, number):
	
		if number < 0 or number > 8:
			return False

		if color not in [EMPTY_CARD, RED_CARD, BLUE_CARD, YELLOW_CARD]:
			return False 
	
		if card_pos < 0 or card_pos >= CARD_POS_MAX:
			return False
			
		if NONE_POS != card_pos and False == self.card_slot[card_pos].HasSlot(slot_index):
			return False
		
		return True
		
		
	def Close(self):
		if self.discard_confirm_dialog:
			if self.discard_confirm_dialog.IsShow():
				self.discard_confirm_dialog.Close()
			
		self.Hide()
		
	def Destroy(self):
		self.isLoaded = 0
		
	def Show(self):
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			self.SetOkeyNormalBG()
			
		ui.ScriptWindow.Show(self)
		
	def SetDeckCount(self, deck_card_count):
		self.deck_card_cnt = deck_card_count
		self.deck_card_cnt_text.SetText( str(self.deck_card_cnt) )
		self.__SetDeckImg( self.deck_card_cnt )
		
	def __SetDeckImg(self, deck_cnt):
		
		if deck_cnt == 0:
			self.__HideAllDeckSlotBaseImage()
			return
			
		for i in range(CARD_COLOR_MAX, 0,-1):
			if deck_cnt == ( CARD_NUMBER_END * i ):
				self.deck_cur_index = i - 1
				self.__ShowDeckSlotBaseImage(i-1)
				self.card_slot[DECK_CARD].SetSlotBaseImage(DECK_IMG_DICT[i-1], 1.0, 1.0, 1.0, 1.0)
				
			
	def __ShowDeckSlotBaseImage(self, index):
		dekc_slot_cnt = self.card_slot[DECK_CARD].GetSlotCount()
		for i in range(0,dekc_slot_cnt):
			if i == index:
				self.card_slot[DECK_CARD].ShowSlotBaseImage(i)
			else:
				self.card_slot[DECK_CARD].HideSlotBaseImage(i)
			
	def __HideAllDeckSlotBaseImage(self):
		dekc_slot_cnt = self.card_slot[DECK_CARD].GetSlotCount()
		for i in range(0,dekc_slot_cnt): 
			self.card_slot[DECK_CARD].HideSlotBaseImage(i)
		
	def __SetScore(self, score):
		self.cur_score = score
		
		if self.cur_score == 0:
			self.cur_score_text.SetText("")
		else:
			self.cur_score_text.SetText( str(self.cur_score) )
		
	def __SetTotalScore(self, total_score):
	
		self.total_score = total_score
		
		if self.total_score < LOW_TOTAL_SCORE:
			self.total_score_text.SetPackedFontColor( TOTAL_SCORE_LOW_FONT_COLOR )
		elif self.total_score < MID_TOTAL_SCORE:
			self.total_score_text.SetPackedFontColor( TOTAL_SCORE_MID_FONT_COLOR )
		else:
			self.total_score_text.SetPackedFontColor( TOTAL_SCORE_HIGH_FONT_COLOR )
			
		self.total_score_text.SetText( str(self.total_score) )
	
				
	def __ExitButtonClick(self):
		
		if None == self.exit_question_dialog:
			self.exit_question_dialog = uiCommon.QuestionDialog()
			self.exit_question_dialog.SetText( localeInfo.MINI_GAME_RUMI_EXIT_QUESTION )
			self.exit_question_dialog.SetAcceptEvent(ui.__mem_func__(self.__AcceptExit))
			self.exit_question_dialog.SetCancelEvent(ui.__mem_func__(self.__CancelExit))
			
			w,h = self.exit_question_dialog.GetTextSize()
			self.exit_question_dialog.SetWidth( w + 60 )
			line_count = self.exit_question_dialog.GetTextLineCount()
			
			if line_count > 1:
				height = self.exit_question_dialog.GetLineHeight()
				self.exit_question_dialog.SetLineHeight(height + 3)
			
		self.exit_question_dialog.Open()
		
	def __AcceptExit(self):
	
		m2netm2g.SendMiniGameRumiExit()
		
		if self.exit_question_dialog :
			self.exit_question_dialog.Close()
	
	def __CancelExit(self):	
		if self.exit_question_dialog :
			self.exit_question_dialog.Close()
			
	def __CloseExitQuestionDialog(self):
		if self.exit_question_dialog :
			self.exit_question_dialog.Close()
			self.exit_question_dialog = None
				
	
	def __DiscardConfirmDialog(self, index):
		
		if None == self.discard_confirm_dialog:
			self.discard_confirm_dialog = uiCommon.QuestionDialog()
			self.discard_confirm_dialog.SetText( localeInfo.MINI_GAME_RUMI_DISCARD_QUESTION )
			self.discard_confirm_dialog.SetAcceptEvent(ui.__mem_func__(self.__AcceptDiscard))
			self.discard_confirm_dialog.SetCancelEvent(ui.__mem_func__(self.__CancelDiscard))	
			
		self.discard_index = index
		self.discard_confirm_dialog.SetTop()
		self.discard_confirm_dialog.Open()
		
	def __AcceptDiscard(self):
		if self.discard_confirm_dialog:
			self.discard_confirm_dialog.Close()
			
		if -1 == self.discard_index:
			return
			
		m2netm2g.SendMiniGameRumiHandCardClick(False, self.discard_index)
		self.discard_index = -1
		
	def __CancelDiscard(self):
		
		if self.discard_confirm_dialog:
			self.discard_confirm_dialog.Close()
			
		self.discard_index = -1
		
	def __CloseDiscardConfirmDialog(self):
		
		if self.discard_confirm_dialog:
			if self.discard_confirm_dialog.IsShow():
				self.discard_confirm_dialog.Close()
				return True
				
		return False
		
	def LButtonClickDeck(self):
		
		if self.lock:
			return
			
		if True == self.__CloseDiscardConfirmDialog():
			return
			
		m2netm2g.SendMiniGameRumiDeckCardClick()
		
	def LButtonClickHand(self, index):
		
		if self.lock:
			return
			
		if True == self.__CloseDiscardConfirmDialog():
			return
			
		m2netm2g.SendMiniGameRumiHandCardClick(True, index)
		
	def RButtonClickHand(self, index):	
		
		if self.lock:
			return
			
		if self.confirm_window_on == True:
			self.__DiscardConfirmDialog(index)
		else:
			m2netm2g.SendMiniGameRumiHandCardClick(False, index)
		
	def LButtonClickField(self, index):
		
		if self.lock:
			return
			
		if True == self.__CloseDiscardConfirmDialog():
			return

		m2netm2g.SendMiniGameRumiFieldCardClick(index)
		
	def __ScoreTextEffectEndFrameEvent(self):
		
		if self.score_text_effect: 
			self.score_text_effect.Hide()
			
		self.__SetScore(0)
		self.__ClearFieldCardSlot()
		self.lock = False
	
	def __ScoreEffectKeyFrameEvent1(self, cur_frame):
		if cur_frame == 2:
			
			if self.score_text_effect:
				self.score_text_effect.Show()
			if self.score_effect2:
				self.score_effect2.Show()
			
	def __ScoreEffectKeyFrameEvent2(self, cur_frame):
		if cur_frame == 1:
			if self.score_effect3:
				self.score_effect3.Show()
	
	def __ScoreEffectEndFrameEvent1(self):
		if self.score_effect1:
			self.score_effect1.Hide()
		
	def __ScoreEffectEndFrameEvent2(self):
		if self.score_effect2:
			self.score_effect2.Hide()
		
	def __ScoreEffectEndFrameEvent3(self):
		if self.score_effect3:
			self.score_effect3.Hide()
			
	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def SetOkeyNormalBG(self):
			if playerm2g2.GetMiniGameOkeyNormal():
				if self.back_ground:
					self.back_ground.Show()
			
		
class MiniGameRumi(ui.Window):
			
	def __init__(self):
		ui.Window.__init__(self)
		self.isLoaded		= 0
		self.state			= STATE_NONE
		
		self.cur_page		= None
		self.waiting_page	= None
		self.game_page		= None
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.Window.__del__(self)
		
	def Show(self):
		self.__LoadWindow()
		ui.Window.Show(self)
		        
	def Close(self):
		self.Hide()
		
		if app.ENABLE_MINI_GAME_OKEY_NORMAL:
			if self.cur_page:
				self.cur_page.Close()

	def Destroy(self):
		self.isLoaded	= 0
		self.state		= STATE_NONE
		self.cur_page	= None
		
		if self.waiting_page:
			self.waiting_page.Destroy()
			
		if self.game_page:
			self.game_page.Destroy()
		
	def __LoadWindow(self):
		
		if self.isLoaded == 1:
			return
			
		self.isLoaded	= 1
		self.state		= STATE_WAITING
		
		try:
			## 게임 설명창
			self.waiting_page	= RumiWaitingPage()
			
			## 게임 진행창
			self.game_page		= RumiGamePage()
			
		except:
			import exception
			exception.Abort("MiniGameRumi.LoadWindow")
		
		self.Hide()
			
	def Open(self):
		
		if STATE_WAITING == self.state:
			self.cur_page = self.waiting_page
			
		elif STATE_PLAY == self.state:
			self.cur_page = self.game_page
			
		else:
			return
			
		if self.cur_page.IsShow():
			self.cur_page.Close()
		else:
			self.cur_page.Show()
			self.cur_page.SetTop()
			
				
	def GameStart(self):
		
		if self.cur_page:
			self.cur_page.Close()
			
		self.state = STATE_PLAY
		self.game_page.Clear()
		self.game_page.SetConfirmWindowCheck( self.waiting_page.GetConfirmWindowCheck() )
		self.Open()
		
	def GameEnd(self):
		self.state = STATE_WAITING
		self.game_page.Clear()
		self.game_page.Close()
		
	def RumiMoveCard(self, srcCard, dstCard):
		self.game_page.RumiMoveCard( srcCard, dstCard )

	def SetDeckCount(self, deck_card_count):
		self.game_page.SetDeckCount(deck_card_count)
		
	def RumiIncreaseScore(self, score, total_score):
		self.game_page.RumiIncreaseScore(score, total_score)
		
	if app.ENABLE_MINI_GAME_OKEY_NORMAL:
		def SetOkeyNormalBG(self):
			if self.game_page:
				self.game_page.SetOkeyNormalBG()
