import ui
import uiCommon
import uiScriptLocale
import playerm2g2
import localeInfo
import m2netm2g
import app
import constInfo
import grpImage
import grp
import event
import uiToolTip
import wndMgr
import snd

from _weakref import proxy
from collections import deque

YUTNORI_YUTSEM1		= 0		# 도
YUTNORI_YUTSEM2		= 1		# 개
YUTNORI_YUTSEM3		= 2		# 걸
YUTNORI_YUTSEM4		= 3		# 윷
YUTNORI_YUTSEM5		= 4		# 모
YUTNORI_YUTSEM6		= 5		# 백도
YUTNORI_YUTSEM_MAX	= 6

YUYNORI_PLAYER_MAX	= 2
YUTNORI_GOAL_AREA	= 11

YUTNORI_IN_DE_CREASE_SCORE = 10
	
prob_name_tuple = ( uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM1
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM2
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM3
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM4
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM5
						, uiScriptLocale.MINI_GAME_YUTNORI_YUTSEM6 )
										

yut_img_path = \
{
	YUTNORI_YUTSEM1 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.sub" ),
	
	YUTNORI_YUTSEM2 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.sub" ),
	
	YUTNORI_YUTSEM3 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.sub" ),
	
	YUTNORI_YUTSEM4 : ( "d:/ymir work/ui/minigame/yutnori/yut_front_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_front_img.sub" ),
	
	YUTNORI_YUTSEM5 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub" ),
	
	YUTNORI_YUTSEM6 : ( "d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_point_img.sub"
	,"d:/ymir work/ui/minigame/yutnori/yut_back_img.sub" ),
}

DEFAULT_DESC_Y		= 7
VISIBLE_LINE_COUNT	= 20
DESC_WIDTH_COUNT	= 66

STATE_NONE		= 0
STATE_WAITING	= 1
STATE_PLAY		= 2

EVENT_TYPE_NOTICE				= 0
EVENT_TYPE_INSER_DELAY			= 1
EVENT_TYPE_DELAY				= 2
EVENT_TYPE_COM_YUT_THROW		= 3
EVENT_TYPE_CHANGE_TEXT_COLOR	= 4
EVENT_TYPE_SHOW_UNIT			= 5
EVENT_TYPE_REQUEST_COM_ACTION	= 6
EVENT_TYPE_BUTTON_FLASH			= 7
EVENT_TYPE_CALL_TURN_CHECK		= 8

YUTNORI_STATE_THROW				= 0		# 윷을 던져야 하는 상태
YUTNORI_STATE_RE_THROW			= 1		# 윷,모가 나와 다시 던지는 상태
YUTNORI_STATE_MOVE				= 2		# 윷말을 이동해야 하는 상태
YUTNORI_BEFORE_TURN_SELECT		= 3		# 턴 결정 전
YUTNORI_AFTER_TURN_SELECT		= 4		# 턴이 결정된 후
YUTNORI_STATE_END				= 5		# 게임이 종료

LOW_TOTAL_SCORE	= 150
MID_TOTAL_SCORE = 220

TOTAL_SCORE_LOW_FONT_COLOR	= grp.GenerateColor(0.78, 0.78, 0.78, 1.0)
TOTAL_SCORE_MID_FONT_COLOR	= 0xffEEA900
TOTAL_SCORE_HIGH_FONT_COLOR = 0xffFFFF99

REMAIN_COUNT_LOW_FONT_COLOR		= grp.GenerateColor(1.0, 0.0, 0.0, 1.0)
REMAIN_COUNT_DEFAULT_FONT_COLOR	= 0xffEEA900


def LoadScript(self, fileName):
	pyScrLoader = ui.PythonScriptLoader()
	pyScrLoader.LoadScriptFile(self, fileName)

class YutnoriWaitingPage(ui.ScriptWindow):

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
		
		self.isLoaded				= 0
		self.startButton			= None
		self.descBoard				= None
		self.descriptionBox			= None
		self.descIndex				= -1
		self.desc_y					= DEFAULT_DESC_Y
		self.btnPrev				= None
		self.btnNext				= None
		self.start_question_dialog	= None
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
	
	def __LoadWindow(self):
	
		if self.isLoaded == 1:
			return
			
		self.isLoaded = 1
		
		try:
			LoadScript(self, "UIScript/MiniGameYutnoriWaitingPage.py")
			
		except:
			import exception
			exception.Abort("MiniGameYutnoriWaitingPage.LoadWindow.LoadObject")
			
		try:
			self.GetChild("board").SetCloseEvent( ui.__mem_func__(self.Close) )
			
			self.startButton	= self.GetChild("game_start_button")
			self.startButton.SetEvent(ui.__mem_func__(self.__ClickStartButton))
			
			self.descBoard		= self.GetChild("desc_board")
			self.descriptionBox = self.DescriptionBox()
			self.descriptionBox.Show()
			
			self.btnPrev = self.GetChild("prev_button")
			self.btnNext = self.GetChild("next_button")
			self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
			self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
			
			if localeInfo.IsARABIC():
				self.btnPrev.LeftRightReverse()
				self.btnNext.LeftRightReverse()
							
		except:
			import exception
			exception.Abort("MiniGameYutnoriWaitingPage.LoadWindow.BindObject")
		
		self.Hide()
		
	def Close(self):
		self.Hide()
		self.CloseStartDlg()
		event.ClearEventSet(self.descIndex)
		self.descIndex = -1
		
		if self.descriptionBox:
			self.descriptionBox.Hide()
						
		self.desc_y					= DEFAULT_DESC_Y
		
	def Destroy(self):
		self.isLoaded				= 0
		self.startButton			= None
		self.descBoard				= None
		self.descriptionBox			= None
		self.descIndex				= -1
		self.desc_y					= DEFAULT_DESC_Y
		self.btnPrev				= None
		self.btnNext				= None
		
		self.CloseStartDlg()
		
	def OnPressEscapeKey(self):
		self.Close()
		return True	
		
	def __ClickStartButton(self):
	
		if None == self.start_question_dialog:
			self.start_question_dialog = uiCommon.QuestionDialog()
			self.start_question_dialog.SetText(localeInfo.MINI_GAME_YUTNORI_START_QUESTION % (30000, 1) )
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
		m2netm2g.SendMiniGameYutnoriStart()
	
	def __StartCancel(self):
		self.start_question_dialog.Close()
				
	def Show(self):
		ui.ScriptWindow.Show(self)
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet( uiScriptLocale.YUTNORI_EVENT_DESC )
		event.SetFontColor( self.descIndex, 0.7843, 0.7843, 0.7843 )
		event.SetVisibleLineCount(self.descIndex, VISIBLE_LINE_COUNT)
		total_line = event.GetTotalLineCount(self.descIndex)
		
		if localeInfo.IsARABIC():
			event.SetEventSetWidth(self.descIndex, self.descBoard.GetWidth() - 20)

		event.SetRestrictedCount(self.descIndex, 90) #DESC_WIDTH_COUNT mainline 과 development 가 폰트체가 달라서
			
		if VISIBLE_LINE_COUNT >= total_line:
			self.btnPrev.Hide()
			self.btnNext.Hide()
		else :
			self.btnPrev.Show()
			self.btnNext.Show()
		
		if self.descriptionBox:
			self.descriptionBox.Show()
		
	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.descBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet + 7, -(yposEventSet + self.desc_y))
		self.descriptionBox.SetIndex(self.descIndex)
		
	def PrevDescriptionPage(self):
	
		line_height			= event.GetLineHeight(self.descIndex) + 4
		if localeInfo.IsARABIC():
			line_height = line_height - 4
			
		cur_start_line		= event.GetVisibleStartLine(self.descIndex)
		
		decrease_count = VISIBLE_LINE_COUNT
		
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
		
		increase_count = VISIBLE_LINE_COUNT
		
		if cur_start_line + increase_count >= total_line_count:
			increase_count = total_line_count - cur_start_line

		if increase_count < 0 or cur_start_line + increase_count >= total_line_count:
			return
		
		event.SetVisibleStartLine(self.descIndex, cur_start_line + increase_count)
		self.desc_y -= ( line_height * increase_count )
		
			
class YutArea:
	def __init__(self, parent, func, x, y, index, prev, next, shortcut_next):
		self.pos			= (x,y)
		self.ani_image		= None
		self.index			= index
		self.prev			= prev
		self.next			= next
		self.shortcut_next	= shortcut_next
		self.arrow_img		= None		
		
		self.__CreateSign( parent, func, index )
		self.__CreateArrowImg( parent )
		
		if localeInfo.IsARABIC():
			# BOARD_WINDOW_WIDTH 436 - 윷판이미지 width 312 = 124
			self.pos			= (x + 124, y)
		
	def __del__(self):
		self.pos			= ()
		
		if self.ani_image:
			del self.ani_image
		self.ani_image = None
		
		self.prev			= None
		self.next			= None
		self.shortcut_next	= None
		
		if self.arrow_img:
			del self.arrow_img
		self.arrow_img = None
		
		
	def GetIndex(self):
		return self.index
	def GetPrevArea(self):
		return self.prev		
	def GetNextArea(self):
		return self.next			
	def GetShortcutNextArea(self):
		if 0 == self.shortcut_next:
			return self.next
		return self.shortcut_next
		
	def __CreateSign(self, parent, func, index):
		(x,y) = self.pos
		self.ani_image = ui.AniImageBox()
		self.ani_image.SetParent( proxy(parent) )
		self.ani_image.SetDelay( 6 )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/2.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/3.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/4.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/5.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/4.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/3.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/2.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.SetPosition(x, y)
		self.ani_image.SetSize(32,32)
		self.ani_image.SetPickAlways()
		self.ani_image.Hide()
		self.ani_image.AddFlag("float")
		
		if localeInfo.IsARABIC():
			# BOARD_WINDOW_WIDTH 436 - 윷판이미지 width 312 = 124
			self.ani_image.SetPosition(x + 124, y)
				
		if func:
			self.ani_image.SetEvent( ui.__mem_func__(func), "mouse_click", index )
		
	def __CreateArrowImg(self, parent ):
		(x,y) = self.pos
		self.arrow_img = ui.AniImageBox()
		self.arrow_img.SetParent( proxy(parent) )
		self.arrow_img.SetDelay( 10 )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/1.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/2.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/3.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/4.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/5.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/4.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/3.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/2.sub" )
		self.arrow_img.SetPosition( x + 7, y - 34 )
		self.arrow_img.Hide()
		self.arrow_img.AddFlag("not_pick")
		self.arrow_img.AddFlag("float")
		
		if localeInfo.IsARABIC():
			# BOARD_WINDOW_WIDTH 436 - 윷판이미지 width 312 = 124
			self.arrow_img.SetPosition(x + 124 + 7, y - 34)
		
	def GetPos(self):
		return self.pos
		
	def GetGlobalPosition(self):
		return self.ani_image.GetGlobalPosition()
		
	def GetLocalPosition(self):
		return self.ani_image.GetLocalPosition()
		
	def Show(self):
		if self.ani_image:
			self.ani_image.ResetFrame()
			self.ani_image.SetTop()
			self.ani_image.Show()
			
		self.ArrowImgShow()
			
	def Hide(self):
		if self.ani_image:
			self.ani_image.Hide()
			
		self.ArrowImgHide()
		
	def ArrowImgShow(self):
		if self.arrow_img:
			self.arrow_img.SetTop()
			self.arrow_img.ResetFrame()
			self.arrow_img.Show()
	def ArrowImgHide(self):
		if self.arrow_img:
			self.arrow_img.Hide()
			
class Yut:
	def __init__(self, is_pc, parent, click_func, move_end_func, explosion_end_func, goal_score_func, num, x, y):
		self.is_pc					= is_pc
		self.num					= num
		self.pos					= (x,y)
		self.char_image				= None
		self.ani_image				= None
		self.cur_index				= -1
		self.available_index		= -1
		self.move_deque				= deque()
		self.move_end_func			= move_end_func
		self.slow_motion			= False
		self.catch_motion			= False
		self.join					= False
		self.is_flash				= True
		self.join_member			= []
		self.is_goal				= False
		self.before_goal_cover_img	= None
		self.explosion_ani_img		= None
		self.explosion_end_func		= explosion_end_func
		self.goal_move				= False
		self.arrow_img				= None
		self.goal_score_func		= goal_score_func
		
		if localeInfo.IsARABIC():
			(px,py) = parent.GetLocalPosition()
			self.pos = (px - 32 - x, y)
		
		self.__CreateChar( parent, click_func, num )
		self.__CreateSign( parent )
		self.__CreateCoverImg( parent )
		
		if True == is_pc:
			self.__CreateArrowImg( parent )
			self.__CreateExplosionEffect( parent )			
		
	def __del__(self):
		self.is_pc					= False
		self.num					= -1
		self.pos					= ()
		self.char_image				= None
		if self.ani_image:
			del self.ani_image
		self.ani_image				= None
		self.cur_index				= -1
		self.available_index		= -1
		
		if self.move_deque:
			self.move_deque.clear()
			
		self.move_end_func			= None
		self.slow_motion			= False
		self.catch_motion			= False
		self.join					= False
		self.is_flash				= True
		self.join_member			= []
		self.is_goal				= False
		self.before_goal_cover_img	= None
		self.explosion_ani_img		= None
		self.explosion_end_func		= None
		self.goal_move				= False
		self.arrow_img				= None
		self.goal_score_func		= None
		
	def DisableFlash(self):
		self.is_flash = False
		
	def CatchPostProcess(self):
		self.cur_index			= -1
		self.available_index	= -1
		self.catch_motion		= False
		self.join				= False
		
		(x,y) = self.pos
		self.SetPosition( x, y )
	
	def CatchPreProcess(self):
		self.is_flash		= True
		self.catch_motion	= True
		
		if self.char_image:
			if self.is_pc:
				self.char_image.LoadImage("d:/ymir work/ui/minigame/yutnori/player_img.sub")
			else:
				self.char_image.LoadImage("d:/ymir work/ui/minigame/yutnori/enemy_img.sub")
			self.char_image.Show()
			
	def SetJoin(self):
		self.join = True
		
		if self.is_pc:
			self.char_image.LoadImage("d:/ymir work/ui/minigame/yutnori/player_join_img.sub")
		else:
			self.char_image.LoadImage("d:/ymir work/ui/minigame/yutnori/enemy_join_img.sub")
			
	def	SetJoinMember(self, index):
		
		if index not in self.join_member:
			self.join_member.append(index)
		
	def GetJoinMember(self):
		return self.join_member
		
	def GetJoin(self):
		return self.join
				
	def __CreateChar(self, parent, func, num):
		(x,y) = self.pos
		self.char_image = ui.MoveScaleImageBox()
		self.char_image.SetParent( proxy(parent) )
		if self.is_pc:
			self.char_image.LoadImage("d:/ymir work/ui/minigame/yutnori/player_img.sub")
		else:
			self.char_image.LoadImage("d:/ymir work/ui/minigame/yutnori/enemy_img.sub")
		self.char_image.SetPosition(x, y)
		self.char_image.Show()
		if func:
			self.char_image.SetEvent( ui.__mem_func__(func), "mouse_click", num )
		
		self.char_image.SetEndMoveEvent( ui.__mem_func__(self.__OnMoveEnd) )
		self.char_image.SetMoveSpeed( 2.5 )
		self.char_image.SetMaxScale( 1.5 )
		self.char_image.SetScalePivotCenter( True )
		self.char_image.AddFlag("float")
		
	def __CreateSign(self, parent):
		(x,y) = self.pos
		self.ani_image = ui.AniImageBox()
		self.ani_image.SetParent( proxy(parent) )
		self.ani_image.SetDelay( 6 )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/2.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/3.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/4.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/5.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/4.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/3.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/2.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/sign/1.sub" )
		self.ani_image.SetPosition(x, y)
		self.ani_image.Hide()
		self.ani_image.AddFlag("not_pick")
		self.ani_image.AddFlag("float")
		
	def __CreateCoverImg(self, parent):
		(x,y) = self.pos
		self.before_goal_cover_img = ui.ImageBox()
		self.before_goal_cover_img.SetParent( proxy(parent) )
		self.before_goal_cover_img.LoadImage("d:/ymir work/ui/minigame/yutnori/before_goal_img.sub")
		self.before_goal_cover_img.SetPosition(x-2, y-2)
		self.before_goal_cover_img.Hide()
		
	def __CreateArrowImg(self, parent ):
		(x,y) = self.pos
		self.arrow_img = ui.AniImageBox()
		self.arrow_img.SetParent( proxy(parent) )
		self.arrow_img.SetDelay( 10 )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/1.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/2.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/3.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/4.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/5.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/4.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/3.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/2.sub" )
		self.arrow_img.SetPosition( x + 7, y - 34 )
		self.arrow_img.Hide()
		self.arrow_img.AddFlag("not_pick")
		self.arrow_img.AddFlag("float")
		
	def __CreateExplosionEffect(self, parent):
		(x,y) = self.pos
		self.explosion_ani_img = ui.AniImageBox()
		self.explosion_ani_img.SetParent( proxy(parent) )
		self.explosion_ani_img.SetDelay( 6 )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff1.sub" )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff2.sub" )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff3.sub" )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff4.sub" )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff5.sub" )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff6.sub" )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff7.sub" )
		self.explosion_ani_img.AppendImage( "D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff8.sub" )
		self.explosion_ani_img.SetPosition(x - 50, y - 32)
		self.explosion_ani_img.SetEndFrameEvent( ui.__mem_func__(self.__ExplosionEffectEnd) )
		self.explosion_ani_img.Hide()
		self.explosion_ani_img.AddFlag("not_pick")
		self.explosion_ani_img.AddFlag("float")
		
		if localeInfo.IsARABIC():
			self.explosion_ani_img.SetWindowHorizontalAlignRight()
			self.explosion_ani_img.SetPosition(x + 128 - 50, y - 32)
		
	def __ExplosionEffectEnd(self):
		if self.explosion_ani_img:
			self.explosion_ani_img.Hide()
		
		if self.explosion_end_func:
			self.explosion_end_func()
			
	def GetPos(self):
		return self.pos
		
	def GetLocalPosition(self):
		if self.char_image:
			return self.char_image.GetLocalPosition()
		return (0,0)
		
	def SetPosition(self, x, y):
			
		if self.char_image:
			self.char_image.SetPosition(x, y)
		if self.ani_image:
			self.ani_image.SetPosition(x, y)
		if self.arrow_img:
			self.arrow_img.SetPosition( x + 7, y - 34 )
		
	def SetIndex(self, index):
		self.cur_index = index
		
		if YUTNORI_GOAL_AREA == index:
			self.is_goal = True
			
	def GetIndex(self):
		return self.cur_index
		
	def SetAvailableIndex(self, index):
		self.available_index = index
	def GetAvailableIndex(self):
		return self.available_index
			
	def IsGoal(self):
		return self.is_goal
		
	def FlashShow(self):
		if self.ani_image and True == self.is_flash and False == self.is_goal:
			self.ani_image.ResetFrame()
			self.ani_image.Show()
			
	def FlashHide(self):
		if self.ani_image:
			self.ani_image.Hide()
			
	def CharHide(self):
		if self.char_image:
			self.char_image.Hide()
		
	def SetTop(self):
		if self.char_image:
			self.char_image.SetTop()
		if self.ani_image:
			self.ani_image.SetTop()
		if self.explosion_ani_img:
			self.explosion_ani_img.SetTop()
		if self.arrow_img:
			self.arrow_img.SetTop()
		
	def GetMove(self):
		if self.char_image:
			return self.char_image.GetMove()
		return True
		
	def OnUpdate(self, parent_x, parent_y):
		self.__UpdateMove( parent_x, parent_y )
		
	def __UpdateMove(self, parent_x, parent_y):
		if len(self.move_deque) > 0 :
			if False == self.char_image.GetMove():				
				pos = self.move_deque[0]
				self.char_image.SetMovePosition( parent_x + pos[0], parent_y + pos[1] )
				
				if 1 == len(self.move_deque) and True == self.slow_motion:
					self.char_image.SetMoveSpeed( 1.5 )
					self.char_image.SetMaxScale( 1.8 )
					self.char_image.SetMaxScaleRate( 0.7 )
				elif 1 == len(self.move_deque) and True == self.goal_move:
					self.char_image.SetMoveSpeed( 10.0 )
					self.char_image.SetMaxScale( 1.0 )
					self.char_image.SetMaxScaleRate( 1.0 )
				elif True == self.catch_motion:
					self.char_image.SetMoveSpeed( 8.0 )
					self.char_image.SetMaxScale( 1.0 )
					self.char_image.SetMaxScaleRate( 1.0 )
				else:
					self.char_image.SetMoveSpeed( 2.5 )
					self.char_image.SetMaxScale( 1.5 )
					self.char_image.SetMaxScaleRate( 0.5 )
					
				self.char_image.MoveStart()
							
	def Start(self, trace_index_list):
		
		if len(trace_index_list) < 2:
			return
			
		self.SetTop()
		(x,y) = trace_index_list[0]
		self.SetPosition(x, y)
		
		for pos in trace_index_list[1:]:
			self.move_deque.append( pos )
		
	def __OnMoveEnd(self):
		if len(self.move_deque) > 0:
			(x,y) = self.move_deque.popleft()
			self.SetPosition(x,y)
			
			if len(self.move_deque) == 1:
				if True == self.goal_move:
					if self.goal_score_func:
						self.goal_score_func(self.is_pc, self.join)
						
			if len(self.move_deque) == 0:
				if True == self.slow_motion:
					self.slow_motion = False
				
				is_call_move_end_func = True
				if True == self.catch_motion:
					if True == self.join and 1 == self.num:
						is_call_move_end_func = False
					self.CatchPostProcess()
					
				if True == self.is_goal:
					self.FlashHide()
					
				if True == self.goal_move:
					self.goal_move = False
					
				if self.move_end_func and True == is_call_move_end_func:
					self.move_end_func( self.is_pc, self.num, self.is_goal )
				
	def SetSlowMotion(self, is_slow):
		self.slow_motion = is_slow
			
	def ShowGoalCoverImg(self):
		if self.before_goal_cover_img:
			self.before_goal_cover_img.Show()
			
	def ShowExplosionEffect(self):
		if self.explosion_ani_img:
			(x,y) = self.GetLocalPosition()
			if localeInfo.IsARABIC():
				self.explosion_ani_img.SetPosition(x + 128 - 50, y - 32)
			else:
				self.explosion_ani_img.SetPosition(x - 50, y - 32)
			self.explosion_ani_img.ResetFrame()
			self.explosion_ani_img.SetDelay( 6 )
			self.explosion_ani_img.SetTop()
			self.explosion_ani_img.Show()
			
	def SetGoalMove(self, flag):
		self.goal_move = flag
		
	def ArrowImgShow(self):
		if self.arrow_img and True == self.is_flash and False == self.is_goal:
			if True == self.join and 1 == self.num:
				return
			self.arrow_img.SetTop()
			self.arrow_img.ResetFrame()
			self.arrow_img.Show()
		
	def ArrowImgHide(self):
		if self.arrow_img:
			self.arrow_img.Hide()
					
class YutnoriGamePage(ui.ScriptWindow):
			
	def __init__(self):
		ui.Window.__init__(self)
		self.isLoaded = 0
		
		self.prob_select_button			= None
		self.prob_select_list_open		= False
		self.prob_select_window			= None
		self.prob_select_button_list	= []
		self.prob_select_over_img		= None
		self.prob_select_text			= None
		self.prob_text_window			= None
		self.prob_index					= 0
		self.prob_title_widow			= None
		self.reward_button				= None
		self.yut_throw_button			= None
		self.yut_img					= []
		self.yut_alpha_update			= False
		self.yut_cur_alpha				= 0.0
		self.giveup_dialog				= None
		self.toolTip					= None
		self.score_text					= None
		self.remain_count_text			= None
		self.notice_text				= None
		self.player_text				= None
		self.com_text					= None
		self.player_list				= []
		self.enemy_list					= []
		self.player_index				= -1
		self.pc_turn					= True
		self.yut_result_pc				= YUTNORI_YUTSEM_MAX
		self.yut_result_com				= YUTNORI_YUTSEM_MAX
		self.area_dict					= {}
		self.event_deque				= None
		self.board						= None
		self.next_turn					= True
		self.yutnori_state				= YUTNORI_BEFORE_TURN_SELECT
		self.model_view					= None
		self.catch_deque				= None
		self.catch_ani					= None
		self.is_actionable				= True
		self.end_img					= None
		self.score						= 250
		self.before_score				= 250
		
		self.re_throw_popup				= None
		self.com_win_popup				= None
		self.pc_win_popup				= None
		self.player_text_cover_over_img	= None
		self.com_text_cover_over_img	= None
		
		self.goal_effect1				= None
		self.goal_effect2				= None
		self.goal_effect3				= None
		self.goal_text_effect			= None
		self.is_goal_text_effect		= False
		self.goal_effect_end_frame_func = None
		
		self.arrow_img					= None
		self.score_effect				= None
		self.move_text_dict				= {}
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		playerm2g2.YutnoriShow( False )
		self.isLoaded = 0
		
		self.prob_select_button			= None
		self.prob_select_list_open		= False
		self.prob_select_window			= None
		self.prob_select_button_list	= []
		self.prob_select_over_img		= None
		self.prob_select_text			= None
		self.prob_text_window			= None
		self.prob_index					= 0
		self.prob_title_widow			= None
		self.reward_button				= None
		self.yut_throw_button			= None
		self.yut_img					= []
		self.yut_alpha_update			= False
		self.yut_cur_alpha				= 0.0
		self.giveup_dialog				= None
		self.toolTip					= None
		self.score_text					= None
		self.remain_count_text			= None
		self.notice_text				= None
		self.player_text				= None
		self.com_text					= None
		self.player_list				= []
		self.enemy_list					= []
		self.player_index				= -1
		self.pc_turn					= True
		self.yut_result_pc				= YUTNORI_YUTSEM_MAX
		self.yut_result_com				= YUTNORI_YUTSEM_MAX
		self.area_dict					= {}
		self.event_deque				= None
		self.board						= None
		self.next_turn					= True
		self.yutnori_state				= YUTNORI_BEFORE_TURN_SELECT
		self.model_view					= None
		self.catch_deque				= None
		self.catch_ani					= None
		self.is_actionable				= True		
		self.end_img					= None
		self.score						= 250
		self.before_score				= 250
		self.re_throw_popup				= None
		self.com_win_popup				= None
		self.pc_win_popup				= None
		self.player_text_cover_over_img	= None
		self.com_text_cover_over_img	= None
		self.goal_effect1				= None
		self.goal_effect2				= None
		self.goal_effect3				= None
		self.goal_text_effect			= None
		self.is_goal_text_effect		= False
		self.goal_effect_end_frame_func = None
		self.arrow_img					= None
		self.score_effect				= None
		self.move_text_dict				= {}
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def Show(self):
		self.__LoadWindow()
		ui.Window.Show(self)
			
	def Close(self, is_giveup = False):
		if False == is_giveup:
			if False == self.pc_turn:
				return	
			if False == self.is_actionable:
				return
				
		playerm2g2.YutnoriShow( False )
		
		if self.giveup_dialog:
			self.giveup_dialog.Hide()
			
		self.__ClearEffect()
		self.Hide()
			
	def __LoadWindow(self):
		playerm2g2.YutnoriShow( False )
		
		if self.isLoaded == 1:
			return
			
		self.isLoaded	= 1
		
		## Load Script
		try:
			LoadScript(self, "UIScript/MiniGameYutnoriGamePage.py")
		except:
			import exception
			exception.Abort("YutnoriGame.LoadWindow.LoadObject")
		
		## object	
		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("YutnoriGame.LoadWindow.__BindObject")
			
		## event
		try:	
			self.__BindEvent()
		except:
			import exception
			exception.Abort("YutnoriGame.LoadWindow.__BindEvent")
			
		self.__CreateProbSelectButton()
		self.__CreateYutImg()
		self.__CreateCatchImage()
		self.__CreateChar()
		self.__CreateYutArea()
		self.__CreateArrowImg()
		
		self.Hide()
		
	def __BindObject(self):
		self.prob_select_button		= self.GetChild("prob_select_button")
		self.prob_select_window		= self.GetChild("prob_select_window")
		self.prob_select_over_img	= self.GetChild("mouse_over_image")
		self.prob_select_over_img.Hide()
		self.prob_select_text		= self.GetChild("probability_text")
		self.prob_text_window		= self.GetChild("probability_text_window")
		self.prob_title_widow		= self.GetChild("probability_title_window")
		self.reward_button			= self.GetChild("reward_button")
		self.yut_throw_button		= self.GetChild("yut_throw_button")
		self.score_text				= self.GetChild("score_text")
		self.remain_count_text		= self.GetChild("remain_count_text")
		self.notice_text			= self.GetChild("notice_text")
		self.player_text			= self.GetChild("player_text")
		self.com_text				= self.GetChild("enemy_text")
		self.board					= self.GetChild("board")
		self.model_view				= self.GetChild("model_view")
		
		self.event_deque			= deque()
		self.toolTip				= uiToolTip.ToolTip()
		self.catch_deque			= deque()
		self.end_img				= self.GetChild("end_img")
		self.end_img.Hide()
		if localeInfo.IsARABIC():
			(g_x,g_y) = self.end_img.GetLocalPosition()			
			self.end_img.SetPosition( 64, g_y )
		
		self.player_text_cover_over_img	= self.GetChild("player_text_cover_over_img")
		self.com_text_cover_over_img	= self.GetChild("enemy_text_cover_over_img")
		
		self.goal_effect1			= self.GetChild("goal_effect1")
		self.goal_effect2			= self.GetChild("goal_effect2")
		self.goal_effect3			= self.GetChild("goal_effect3")		
		self.goal_text_effect		= self.GetChild("goal_text_effect")
		
		
	def __BindEvent(self):
		## close event
		if self.board:
			self.board.SetCloseEvent( ui.__mem_func__(self.__ShowGiveupDialog) )		
			
		if self.prob_select_button:
			self.prob_select_button.SetEvent( ui.__mem_func__(self.__ClickProbSelectButton) )			
			
		if self.prob_text_window:
			self.prob_text_window.SetOnMouseLeftButtonUpEvent( ui.__mem_func__(self.__ClickProbSelectButton) )
			
		if self.prob_select_text:
			self.prob_select_text.SetText( prob_name_tuple[0] )
			
		if self.reward_button:
			self.reward_button.SetEvent( ui.__mem_func__(self.__ClickRewardButton) )
			self.reward_button.Disable()
			
		if self.yut_throw_button:
			self.yut_throw_button.SetEvent( ui.__mem_func__(self.__ClickThrowButton) )
			self.yut_throw_button.EnableFlash()
			
		if self.notice_text:
			self.notice_text.SetText( localeInfo.MINI_GAME_NOTICE_1 )
		
		if self.player_text_cover_over_img:
			self.player_text_cover_over_img.Show()
		if self.com_text_cover_over_img:
			self.com_text_cover_over_img.Hide()
	
		if self.goal_effect1:
			self.goal_effect1.SetScale(1.2, 1.2)
			self.goal_effect1.Hide()
			self.goal_effect1.SetEndFrameEvent( ui.__mem_func__(self.__GoalEffectEndFrameEvent1) )
			self.goal_effect1.SetKeyFrameEvent( ui.__mem_func__(self.__GoalEffectKeyFrameEvent1) )
			
		if self.goal_effect2:
			self.goal_effect2.SetScale(1.2, 1.2)
			self.goal_effect2.Hide()
			self.goal_effect2.SetEndFrameEvent( ui.__mem_func__(self.__GoalEffectEndFrameEvent2) )
			self.goal_effect2.SetKeyFrameEvent( ui.__mem_func__(self.__GoalEffectKeyFrameEvent2) )
			
		if self.goal_effect3:
			self.goal_effect3.SetScale(1.2, 1.2)
			self.goal_effect3.Hide()
			self.goal_effect3.SetEndFrameEvent( ui.__mem_func__(self.__GoalEffectEndFrameEvent3) )
		
		if self.goal_text_effect:
			self.goal_text_effect.SetEndFrameEvent( ui.__mem_func__(self.__GoalTextEffectEndFrameEvent) )
			self.goal_text_effect.Hide()
			
		if localeInfo.IsARABIC():
			if self.goal_effect1:
				(x, y) = self.goal_effect1.GetLocalPosition()
				self.goal_effect1.SetPosition(x+120, y)
				self.goal_effect1.SetWindowHorizontalAlignLeft()
			if self.goal_effect2:
				(x, y) = self.goal_effect2.GetLocalPosition()
				self.goal_effect2.SetPosition(x+120, y)
				self.goal_effect2.SetWindowHorizontalAlignLeft()
			if self.goal_effect3:
				(x, y) = self.goal_effect3.GetLocalPosition()
				self.goal_effect3.SetPosition(x+120, y)
				self.goal_effect3.SetWindowHorizontalAlignLeft()
			if self.goal_text_effect:
				(x, y) = self.goal_text_effect.GetLocalPosition()
				self.goal_text_effect.SetPosition(x+120, y)
				self.goal_text_effect.SetWindowHorizontalAlignLeft()
			
	def __CreateCatchImage(self):
		if self.board:
			self.catch_ani = ui.AniImageBox()
			self.catch_ani.SetParent( proxy(self.board) )
			self.catch_ani.SetDelay( 6 )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch01.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch02.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch03.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch04.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch05.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch06.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch07.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch08.tga" )
			self.catch_ani.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/catch/catch09.tga" )
			self.catch_ani.SetPosition(0, 0)
			self.catch_ani.SetEndFrameEvent( ui.__mem_func__(self.__CatchAniEndFrameEvent) )
			self.catch_ani.Hide()
			
			
	def __CreateProbSelectButton(self):
	
		if None == self.prob_select_window:
			return
			
		for i in xrange(6):
			button = ui.Button()
			button.SetParent( self.prob_select_window )
			button.SetPosition( 0, 16 * i )
			
			if i == 0:
				button.SetUpVisual( "d:/ymir work/ui/minigame/yutnori/list_top.sub" )
				button.SetDownVisual( "d:/ymir work/ui/minigame/yutnori/list_top.sub" )
				button.SetOverVisual( "d:/ymir work/ui/minigame/yutnori/list_top.sub" )
			elif i == 5:
				button.SetUpVisual( "d:/ymir work/ui/minigame/yutnori/list_bottom.sub" )
				button.SetDownVisual( "d:/ymir work/ui/minigame/yutnori/list_bottom.sub" )
				button.SetOverVisual( "d:/ymir work/ui/minigame/yutnori/list_bottom.sub" )
			else:
				button.SetUpVisual( "d:/ymir work/ui/minigame/yutnori/list_middle.sub" )
				button.SetDownVisual( "d:/ymir work/ui/minigame/yutnori/list_middle.sub" )
				button.SetOverVisual( "d:/ymir work/ui/minigame/yutnori/list_middle.sub" )
				
			button.SetEvent( ui.__mem_func__(self.__ClickProbButton), i )
			button.SetOverEvent( ui.__mem_func__(self.__ClickProbButtonOver), i )
			button.SetOverOutEvent( ui.__mem_func__(self.__ClickProbButtonOverOut), i )
			button.SetText( prob_name_tuple[i] )
			button.Hide()
			
			self.prob_select_button_list.append( button )
		
	def __CreateChar(self):
		if self.board:
			self.player_list.append( Yut(True, self.board, self.__ClickChar, self.__MoveEnd, self.__ComWinPopup, self.__GoalScore, 0, 21, 357) )
			self.player_list.append( Yut(True, self.board, self.__ClickChar, self.__MoveEnd, None, self.__GoalScore, 1, 60, 357) )
			self.enemy_list.append( Yut(False, self.board, None, self.__MoveEnd, None, self.__GoalScore, 0, 183, 357) )
			self.enemy_list.append( Yut(False, self.board, None, self.__MoveEnd, None, self.__GoalScore, 1, 222, 357) )
			
	def __CreateYutArea(self):
		
		if self.board:
			self.area_dict[11] 	= YutArea(self.board, self.__ClickArea, 270, 292,	11, 0, 10, 0)
			self.area_dict[10] 	= YutArea(self.board, self.__ClickArea, 270, 244,	10, 11, 9, 0)
			self.area_dict[9] 	= YutArea(self.board, self.__ClickArea, 270, 196,	9, 10, 8, 0)
			self.area_dict[8] 	= YutArea(self.board, self.__ClickArea, 270, 148,	8, 9, 7, 0)
			self.area_dict[7] 	= YutArea(self.board, self.__ClickArea, 270, 100,	7, 8, 6, 0)
			self.area_dict[6] 	= YutArea(self.board, self.__ClickArea, 270, 52,	6, 7, 5, 26)
			self.area_dict[5] 	= YutArea(self.board, self.__ClickArea, 222, 52, 	5, 6, 4, 0)
			self.area_dict[4] 	= YutArea(self.board, self.__ClickArea, 174, 52, 	4, 5, 3, 0)
			self.area_dict[3] 	= YutArea(self.board, self.__ClickArea, 126, 52, 	3, 4, 2, 0)
			self.area_dict[2] 	= YutArea(self.board, self.__ClickArea, 78,  52, 	2, 3, 1, 0)
			self.area_dict[1] 	= YutArea(self.board, self.__ClickArea, 30,  52, 	1, 2, 20, 21)
			self.area_dict[20] 	= YutArea(self.board, self.__ClickArea, 30,  100,	20, 1, 19, 0)
			self.area_dict[19] 	= YutArea(self.board, self.__ClickArea, 30,  148, 	19, 20, 18, 0)
			self.area_dict[18] 	= YutArea(self.board, self.__ClickArea, 30,  196, 	18, 19, 17, 0)
			self.area_dict[17] 	= YutArea(self.board, self.__ClickArea, 30,  244, 	17, 18, 16, 0)
			self.area_dict[16] 	= YutArea(self.board, self.__ClickArea, 30,  292, 	16, 17, 15, 0)
			self.area_dict[15] 	= YutArea(self.board, self.__ClickArea, 78,  292, 	15, 16, 14, 0)
			self.area_dict[14] 	= YutArea(self.board, self.__ClickArea, 126, 292, 	14, 15, 13, 0)
			self.area_dict[13] 	= YutArea(self.board, self.__ClickArea, 174, 292, 	13, 14, 12, 0)
			self.area_dict[12] 	= YutArea(self.board, self.__ClickArea, 222, 292, 	12, 13, 11, 0)
			self.area_dict[21] 	= YutArea(self.board, self.__ClickArea, 70,  92,	21, 1, 22, 0)
			self.area_dict[22] 	= YutArea(self.board, self.__ClickArea, 110, 132,	22, 21, 23, 0)
			self.area_dict[23] 	= YutArea(self.board, self.__ClickArea, 150, 172,	23, 27, 28, 24)
			self.area_dict[24] 	= YutArea(self.board, self.__ClickArea, 190, 212,	24, 23, 25, 0)
			self.area_dict[25] 	= YutArea(self.board, self.__ClickArea, 230, 252,	25, 24, 11, 0)
			self.area_dict[26] 	= YutArea(self.board, self.__ClickArea, 230, 92,	26, 6, 27, 0)
			self.area_dict[27] 	= YutArea(self.board, self.__ClickArea, 190, 132,	27, 26, 23, 0)
			self.area_dict[28] 	= YutArea(self.board, self.__ClickArea, 110, 212,	28, 23, 29, 0)
			self.area_dict[29] 	= YutArea(self.board, self.__ClickArea, 70,  252,	29, 28, 16, 0)
			
	def __CreateArrowImg(self):
		if not self.yut_throw_button:
			return
			
		(x,y) = self.yut_throw_button.GetLocalPosition()
		
		self.arrow_img = ui.AniImageBox()
		self.arrow_img.SetParent( self )
		self.arrow_img.SetDelay( 10 )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/1.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/2.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/3.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/4.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/5.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/4.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/3.sub" )
		self.arrow_img.AppendImage( "D:/Ymir Work/UI/minigame/yutnori/move_arrow/2.sub" )
		self.arrow_img.SetPosition( x + 7, y - 34 )
		self.arrow_img.Show()
		self.arrow_img.AddFlag("not_pick")
		self.arrow_img.AddFlag("float")
		
		if localeInfo.IsARABIC():
			w = self.yut_throw_button.GetWidth()
			self.arrow_img.SetWindowHorizontalAlignRight()
			self.arrow_img.SetPosition(x - w + 25, y - 34)
			
	def __CreateYutImg(self):
		yut_result_img = self.GetChild("yut_result_img")
		
		for i in xrange(4):
			yut_imagebox = ui.ImageBox()
			yut_imagebox.SetParent( yut_result_img )
			yut_imagebox.SetPosition( 12 + i*21 + i*2, 26 )
			yut_imagebox.Hide()
			self.yut_img.append( yut_imagebox )
	
	
	# 점수 차감	0xFFFF7F27
	# 점수 획득	0xFF2F97FF	
	def __CreateScoreEffect(self, is_increase, score, start_x, start_y):			
		move_text = ui.MoveTextLine()
		move_text.SetParent(self)
		if localeInfo.IsARABIC():
			move_text.SetPosition( 456-start_x, start_y )
		else:
			move_text.SetPosition( start_x, start_y )
		move_text.SetVerticalAlignCenter()
		move_text.SetHorizontalAlignCenter()
		move_text.SetFontName( localeInfo.MINI_GAME_YUTNORI_SCORE_FONT )
		
		score_str = ""
		if True == is_increase:
			score_str += "+"
			move_text.SetPackedFontColor( 0xFF2F97FF )
		else:
			score_str += "-"
			move_text.SetPackedFontColor( 0xFFFF7F27 )
			
		score_str += str(score)
		move_text.SetText( score_str )
		move_text.SetMoveSpeed( 3.0 )
		(parent_global_x, parent_global_y) = self.GetGlobalPosition()
		
		if localeInfo.IsARABIC():
			move_text.SetMovePosition( parent_global_x + 65, parent_global_y + 65 )
		else:
			move_text.SetMovePosition( parent_global_x + 380, parent_global_y + 65 )
		key = len(self.move_text_dict)
		move_text.SetEndMoveEvent( ui.__mem_func__(self.__ScoreEffectEndEvent), key )
		move_text.Show()
		move_text.MoveStart()
				
		self.move_text_dict[key] = move_text
		
	def __ScoreEffectEndEvent(self, index):		
		if index in self.move_text_dict:
			del self.move_text_dict[index]
			
		self.__RefreshScore()
			
	def __GoalEffectEndFrameEvent1(self):
		if self.goal_effect1:
			self.goal_effect1.Hide()
			
	def __GoalEffectEndFrameEvent2(self):
		if self.goal_effect2:
			self.goal_effect2.Hide()
			
	def __GoalEffectEndFrameEvent3(self):
		if self.goal_effect3:
			self.goal_effect3.Hide()
			
		self.__EffectEndCheck()
		
	def __GoalTextEffectEndFrameEvent(self):
		if self.goal_text_effect:
			self.goal_text_effect.Hide()
			
		self.__EffectEndCheck()
			
	def __EffectEndCheck(self):
		if False == self.goal_effect1.IsShow()\
			and False == self.goal_effect2.IsShow()\
			and False == self.goal_effect3.IsShow()\
			and False == self.goal_text_effect.IsShow():
			
			if self.goal_effect_end_frame_func:
				self.goal_effect_end_frame_func()
		
	def __GoalEffectKeyFrameEvent1(self, cur_frame):
		if cur_frame == 2:
			if self.goal_effect2:
				self.goal_effect2.Show()
			if self.goal_text_effect and self.is_goal_text_effect:
				self.goal_text_effect.Show()
				
	def __GoalEffectKeyFrameEvent2(self, cur_frame):
		if cur_frame == 1:
			if self.goal_effect3:
				self.goal_effect3.Show()
				
	def __ClearEffect(self):
		if self.goal_effect1:
			self.goal_effect1.Hide()
			self.goal_effect1.ResetFrame()
			self.goal_effect1.SetDelay(6)
		if self.goal_effect2:
			self.goal_effect2.Hide()
			self.goal_effect2.ResetFrame()
			self.goal_effect2.SetDelay(6)
		if self.goal_effect3:
			self.goal_effect3.Hide()
			self.goal_effect3.ResetFrame()
			self.goal_effect3.SetDelay(6)
		if self.goal_text_effect:
			self.goal_text_effect.Hide()
			self.goal_text_effect.ResetFrame()
			self.goal_text_effect.SetDelay(6)
			
			
	def __ShowGiveupDialog(self):
		if False == self.pc_turn:
			return
			
		if None == self.giveup_dialog:
			self.giveup_dialog = uiCommon.QuestionDialog()
			self.giveup_dialog.SetText( localeInfo.MINI_GAME_GIVEUP_QUESTION )
			self.giveup_dialog.SetAcceptEvent( ui.__mem_func__(self.__GiveupAccept) )
			self.giveup_dialog.SetCancelEvent( ui.__mem_func__(self.__GiveupCancel) )
			w,h = self.giveup_dialog.GetTextSize()
			self.giveup_dialog.SetWidth( w + 60 )
			line_count = self.giveup_dialog.GetTextLineCount()
			
			if line_count > 1:
				height = self.giveup_dialog.GetLineHeight()
				self.giveup_dialog.SetLineHeight(height + 3)
			
		self.giveup_dialog.Show()
		self.giveup_dialog.SetTop()
		
	def __GiveupAccept(self):
		if False == self.pc_turn:
			return
		if False == self.is_actionable:
			return
		m2netm2g.SendMiniGameYutnoriGiveup()
		self.__GiveupCancel()
		
	def __GiveupCancel(self):
		if self.giveup_dialog:
			self.giveup_dialog.Hide()	
			
	def __HideYutArea(self):
		for area in self.area_dict.values():
			area.Hide()	
		
	# Render Target 에 재생되는 윷 애니메이션이 끝나면 호출된다
	def SetYut(self):
		
		self.yut_cur_alpha = 0.0
		
		index = YUTNORI_YUTSEM_MAX
		if True == self.pc_turn:
			index = self.yut_result_pc
		else:
			index = self.yut_result_com
			
		if YUTNORI_YUTSEM_MAX == index:
			return
			
		for i in xrange(4):
			self.yut_img[i].LoadImage( yut_img_path[index][i] )
			self.yut_img[i].SetAlpha( self.yut_cur_alpha )
			self.yut_img[i].Show()
			
		self.yut_alpha_update = True
		
	def __ClickChar(self, event_type, index):		
		if "mouse_click" != event_type:
			return
			
		if YUTNORI_STATE_MOVE != self.yutnori_state:
			return
			
		if False == self.is_actionable:
			return
			
		if False == self.pc_turn:
			return
			
		if -1 == self.player_list[index].GetIndex():
			if YUTNORI_YUTSEM6 == self.yut_result_pc:
				return
			if True == self.player_list[index].IsGoal():
				return
				
		self.__HideYutArea()		
		self.__HideAllUnitFlash()
		
		if index == self.player_index:
			self.player_index = -1
			self.__ShowUnitFlash( True )
			return

		self.player_index = index
				
		available_index = self.player_list[index].GetAvailableIndex()
		if -1 == available_index:
			m2netm2g.SendMiniGameCharClick( self.player_index )
		else:
			self.AvailableAreaShow((index, available_index))
		
	def AvailableAreaShow(self, data):
		(player_index, available_index) = data
		
		if self.area_dict.has_key( available_index ):
			self.area_dict[available_index].Show()
			
		self.player_list[player_index].SetAvailableIndex(available_index)
		
			
	def __GetMoveCount(self, unit):
		
		if 0 == unit:	# 도
			return 1
		elif 1 == unit:	# 개
			return 2
		elif 2 == unit:	# 걸
			return 3
		elif 3 == unit:	# 윷
			return 4
		elif 4 == unit:	# 모
			return 5
		elif 5 == unit:	# 백도
			return -1
			
	def __ClickArea(self, event_type, index):
		if "mouse_click" != event_type:
			return
			
		if False == self.pc_turn:
			return
			
		if YUTNORI_STATE_MOVE != self.yutnori_state:
			return
			
		m2netm2g.SendMiniGameYutMove( self.player_index )
		self.player_index = -1
					
	def __ShowUnitFlash(self, is_pc):
		if True == is_pc:
			for yut in self.player_list:
				if YUTNORI_YUTSEM6 == self.yut_result_pc:
					if -1 == yut.GetIndex():
						continue
				yut.FlashShow()
				yut.ArrowImgShow()
		else:
			for yut in self.enemy_list:
				yut.FlashShow()
				yut.ArrowImgHide()
				
	def __HideAllUnitFlash(self):
		for yut in self.player_list:
				yut.FlashHide()
				yut.ArrowImgHide()
		for yut in self.enemy_list:
				yut.FlashHide()
				yut.ArrowImgHide()
											
	def __ChangeTextColor(self, is_pc_turn):
		
		if True == is_pc_turn:
			if self.player_text:
				self.player_text.SetPackedFontColor( 0xffEEA900 )
			if self.com_text:
				self.com_text.SetPackedFontColor( grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0) )
			if self.player_text_cover_over_img:
				self.player_text_cover_over_img.Show()
			if self.com_text_cover_over_img:
				self.com_text_cover_over_img.Hide()
		else:
			if self.player_text:
				self.player_text.SetPackedFontColor( grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0) )
			if self.com_text:
				self.com_text.SetPackedFontColor( 0xffEEA900 )
			if self.player_text_cover_over_img:
				self.player_text_cover_over_img.Hide()
			if self.com_text_cover_over_img:
				self.com_text_cover_over_img.Show()
				
					
	def __HideYut(self):
		for i in xrange(4):
			self.yut_img[i].Hide()
			
	def __ClickProbSelectButton(self):
		
		if self.prob_select_list_open:
			self.__ProbSelectWindowOpen( False )
		else:
			self.__ProbSelectWindowOpen( True )
			
	def __ProbSelectWindowOpen(self, open):
		
		self.prob_select_list_open = open
		
		if True == open:
			if self.prob_select_window:
				self.prob_select_window.SetSize( 115, 16*6 )
			
			for button in self.prob_select_button_list:
				button.Show()
		else:
			if self.prob_select_window:
				self.prob_select_window.SetSize( 115, 0 )
			for button in self.prob_select_button_list:
				button.Hide()
		
	def __ClickProbButton(self, index):
		if None == self.prob_select_text:
			return
		if len( prob_name_tuple ) <= index:
			return
			
		self.__ProbSelectWindowOpen( False )
		m2netm2g.SendMiniGameYutnoriProb( index )
				
	def SetProb(self, index):
		if None == self.prob_select_text:
			return
		if len( prob_name_tuple ) <= index:
			return
		self.prob_index	= index
		self.prob_select_text.SetText( prob_name_tuple[index] )
		
	## 
	def __ClickProbButtonOver(self, index):
		if not self.prob_select_over_img:
			return
			
		button = None
		if self.prob_select_button_list:
			if self.prob_select_button_list[index]:
				button = self.prob_select_button_list[index]
		if None == button:
			return
			
		self.prob_select_over_img.SetPosition( 328, 168 + 16*index)
		self.prob_select_over_img.Show()
		
		
	def __ClickProbButtonOverOut(self, index):
		if not self.prob_select_over_img:
			return
		self.prob_select_over_img.Hide()
		
	def __ClickRewardButton(self):
		m2netm2g.SendMiniGameYutReward()
		
	def __ClickThrowButton(self):
		if False == self.pc_turn:
			return	
		if False == self.is_actionable:
			return
		if self.yutnori_state not in [YUTNORI_STATE_THROW, YUTNORI_STATE_RE_THROW, YUTNORI_BEFORE_TURN_SELECT]:
			return
			
		m2netm2g.SendMiniGameYutThrow( True )
		
		self.ArrowImgHide()
		
		if self.yut_throw_button:
			self.yut_throw_button.DisableFlash()
			
		if self.re_throw_popup:
			self.re_throw_popup.Hide()
	
	def __ProbTilteOverIn(self):
	
		arglen = len( uiScriptLocale.MINI_GAME_YUTNORI_PROB_DESC )
		pos_x, pos_y = wndMgr.GetMousePosition()
		
		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(11 * arglen)
			self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
			self.toolTip.AppendTextLine( uiScriptLocale.MINI_GAME_YUTNORI_PROB_DESC )
			self.toolTip.Show()
		
	def __ProbTilteOverOut(self):		
		if self.toolTip:
			self.toolTip.Hide()
				
	def OnUpdate(self):
	
		self.__UpdateToolTip()		
		self.__UpdateAlpha()
		self.__UpdateChar()
		self.__UpdateEvent()		
		
	def __UpdateToolTip(self):
		if self.prob_title_widow and self.prob_select_button:
			if self.prob_title_widow.IsIn() or self.prob_select_button.IsIn():
				self.__ProbTilteOverIn()
			else:
				self.__ProbTilteOverOut()
			
	def __UpdateAlpha(self):
	
		if False == self.yut_alpha_update:
			return
	
		self.yut_cur_alpha = self.yut_cur_alpha + 0.02
		
		for i in xrange(4):	
			self.yut_img[i].SetAlpha( self.yut_cur_alpha )
			
		## 윷 던지기 애니메이션이 모두 끝남
		if self.yut_cur_alpha >= 1.0:
			self.yut_alpha_update	= False
			self.is_actionable		= True
					
			if self.yutnori_state in [YUTNORI_BEFORE_TURN_SELECT, YUTNORI_AFTER_TURN_SELECT]:
				yut_result = self.yut_result_pc if True == self.pc_turn else self.yut_result_com
				if self.notice_text:
					self.notice_text.SetText( localeInfo.MINI_GAME_NOTICE_8 % prob_name_tuple[ yut_result ] )	# %s 나왔습니다!
							
			elif True == self.pc_turn:
				move_count	= self.__GetMoveCount( self.yut_result_pc )
				notice_str	= None
				if move_count > 0:
					notice_str = localeInfo.MINI_GAME_NOTICE_6 % (prob_name_tuple[ self.yut_result_pc ], move_count )	# %s 나왔습니다! %d칸 이동할 수 있습니다.
				else:
					notice_str = localeInfo.MINI_GAME_NOTICE_7 % prob_name_tuple[ self.yut_result_pc ]					# %s 나왔습니다! 1칸 뒤로 이동 해야합니다.
					
				if self.notice_text:
					self.notice_text.SetText( notice_str )
			
			# 턴을 체크한다.
			self.__TurnCheck()
		
	def __UpdateEvent(self):
		if not self.event_deque:
			return
		
		if len(self.event_deque) > 0:
			[event_type, data] = self.event_deque[0]
			
			if EVENT_TYPE_NOTICE == event_type:
				self.event_deque.popleft()
				if self.notice_text:
					self.notice_text.SetText( data )
					
			elif EVENT_TYPE_INSER_DELAY == event_type:
				self.event_deque.popleft()
				delay_value = app.GetGlobalTime() + data
				self.event_deque.appendleft( [EVENT_TYPE_DELAY, delay_value] )
									
			elif EVENT_TYPE_DELAY == event_type:
				if app.GetGlobalTime() > data:
					self.event_deque.popleft()			
					
			elif EVENT_TYPE_COM_YUT_THROW == event_type:
				self.event_deque.popleft()
				m2netm2g.SendMiniGameYutThrow( False )
				
			elif EVENT_TYPE_CHANGE_TEXT_COLOR == event_type:
				self.event_deque.popleft()
				self.__ChangeTextColor( data )
				
			elif EVENT_TYPE_SHOW_UNIT == event_type:
				self.event_deque.popleft()
				self.__HideAllUnitFlash()
				self.__ShowUnitFlash( data )
			elif EVENT_TYPE_REQUEST_COM_ACTION == event_type:
				self.event_deque.popleft()
				m2netm2g.SendMiniGameRequestComAction()
				
			elif EVENT_TYPE_BUTTON_FLASH == event_type:
				self.event_deque.popleft()
				(button, enable) = data
				if not button:
					return
					
				if True == enable:
					button.EnableFlash()
					self.ArrowImgShow()
				else:
					button.DisableFlash()
					self.ArrowImgHide()
					
			elif EVENT_TYPE_CALL_TURN_CHECK == event_type:
				self.event_deque.popleft()
				self.__TurnCheck()
				
	def __UpdateChar(self):
		if not self.board:
			return
			
		(x,y) = self.board.GetGlobalPosition()
		
		for player in self.player_list:
			player.OnUpdate(x, y)
		for enemy in self.enemy_list:
			enemy.OnUpdate(x, y)
			
	def ArrowImgShow(self):
		if self.arrow_img:
			self.arrow_img.ResetFrame()
			self.arrow_img.Show()
	def ArrowImgHide(self):
		if self.arrow_img:
			self.arrow_img.Hide()
					
	def ThrowResult(self, data):
		self.is_actionable = False
		
		(bPC, result) = data
		if result < 0 or result > 5:
			return
			
		self.ArrowImgHide()
		self.__HideYut()
		if self.model_view:
			self.model_view.SetTop()
			
		playerm2g2.YutnoriShow( True )
		playerm2g2.YutnoriChangeMotion( result )
		snd.PlaySound("D:/ymir work/ui/minigame/yutnori/yut_throw.wav")
		self.__ThrowScoreCheck()
		if True == bPC:
			self.yut_result_pc = result
		else:
			self.yut_result_com	= result
			
	def YutMove(self, data):
		self.__HideAllUnitFlash()
		self.__HideYutArea()
		
		(is_pc, unit_index, is_catch, start_index, dest_index) = data
		
		move_count = 0
		if is_pc:
			move_count	= self.__GetMoveCount( self.yut_result_pc )
		else:
			move_count	= self.__GetMoveCount( self.yut_result_com )
			
		move_index_list = []
		move_index_list.append( self.area_dict[start_index].GetLocalPosition() )
		
		goal_move = False
		
		if -1 == move_count:
			move_index_list.append( self.area_dict[dest_index].GetLocalPosition() )
			
			if YUTNORI_GOAL_AREA == dest_index:
				goal_move = True
				if True == is_pc:
					if localeInfo.IsARABIC():
						move_index_list.append( (456-32-126, 252) )
					else:
						move_index_list.append( (126, 252) )
				else:
					if localeInfo.IsARABIC():
						move_index_list.append( (456-32-174, 252) )
					else:
						move_index_list.append( (174, 252) )
		else:
			move_index = start_index
			cross_check_index = 0
			for i in xrange(move_count):
				# 22, 27을 지나갈 경우 위치를 기억해야함
				if 22 == move_index or 27 == move_index:
					cross_check_index = move_index
			
				# 첫 시작은 지름길이 있다면 지름길로 이동
				if 0 == i:
					move_index = self.area_dict[move_index].GetShortcutNextArea()
				# 윷판 정가운데 지점을 지날때는 cross_check_index 가 있어야 함.
				# 22에서 왔다면 24로 보내주고
				# 27에서 왔다면 28로 보내줌
				elif 23 == move_index and 0 != cross_check_index:
					if 22 == cross_check_index:
						move_index = self.area_dict[move_index].GetShortcutNextArea()
					else:
						move_index = self.area_dict[move_index].GetNextArea()
				else:
					move_index = self.area_dict[move_index].GetNextArea()
					
				move_index_list.append( self.area_dict[move_index].GetLocalPosition() )
				
				if YUTNORI_GOAL_AREA == move_index:
					goal_move = True
					if True == is_pc:
						if localeInfo.IsARABIC():
							move_index_list.append( (456-32-126, 252) )
						else:
							move_index_list.append( (126, 252) )
					else:
						if localeInfo.IsARABIC():
							move_index_list.append( (456-32-174, 252) )
						else:
							move_index_list.append( (174, 252) )
					break
				
		self.AddFlag("not_move")
		if is_pc:
			self.player_list[unit_index].SetIndex( dest_index )
			
			if self.player_list[unit_index].GetJoin():
				member_list = self.player_list[unit_index].GetJoinMember()
				for member_index in member_list:
					self.player_list[member_index].SetIndex( dest_index )
				
			self.player_list[unit_index].FlashHide()
			self.player_list[unit_index].ArrowImgHide()
			self.player_list[unit_index].SetSlowMotion( is_catch )
			self.player_list[unit_index].SetGoalMove( goal_move )
			self.player_list[unit_index].Start( move_index_list )
		else:
			self.enemy_list[unit_index].SetIndex( dest_index )
			
			if self.enemy_list[unit_index].GetJoin():
				member_list = self.enemy_list[unit_index].GetJoinMember()
				for member_index in member_list:
					self.enemy_list[member_index].SetIndex( dest_index )
					
			self.enemy_list[unit_index].FlashHide()
			self.enemy_list[unit_index].ArrowImgHide()
			self.enemy_list[unit_index].SetSlowMotion( is_catch )
			self.enemy_list[unit_index].SetGoalMove( goal_move )
			self.enemy_list[unit_index].Start( move_index_list )
		
		self.is_actionable = False	
		self.__ClearAvailableIndex( is_pc )
			
	def __ClearAvailableIndex(self, is_pc):
		if is_pc:
			for player in self.player_list:
				player.SetAvailableIndex(-1)
		else:
			for enemy in self.enemy_list:
				enemy.SetAvailableIndex(-1)
				
	def __CatchAniEndFrameEvent(self):
		if self.catch_ani:
			self.catch_ani.Hide()
			
	def __GoalCoverCheck(self):
		for i in xrange(2):
			if self.player_list[i].IsGoal():
				self.player_list[i].ShowGoalCoverImg()
			if self.enemy_list[i].IsGoal():
				self.enemy_list[i].ShowGoalCoverImg()
				
	def __MoveEnd(self, is_pc, index, goal_effect):
		# start 이미지를 goal 이미지로 바꿔준다
		if self.end_img:
			self.end_img.Show()
		
		## 이동 애니메이션이 모두 끝났다
		self.is_actionable = True
			
		self.__GoalCoverCheck()
		self.__RefreshJoinMemberPosition()
		self.__JoinCheck()
		
		## PC 윷말이 Goal 에 통과 했고 게임이 끝난게 아니라면 
		## 이펙트 재생 후 다시 __TurnCheck 호출
		if True == is_pc and True == goal_effect and YUTNORI_STATE_END != self.yutnori_state:
			self.__ClearEffect()
			self.is_goal_text_effect = False
			self.goal_effect_end_frame_func = ui.__mem_func__(self.__TurnCheck) 
			if self.goal_effect1:
				self.goal_effect1.Show()
			return
		
		## 윷말이 잡혔다면 잡힌 애니메이션이 재생 된 후 __MoveEnd 가 다시 호출된다.
		bCatch = self.__CatchCheck()
		if False == bCatch:
			self.AddFlag("movable")
			self.__TurnCheck()
		
	def __RefreshJoinMemberPosition(self):
		
		if self.player_list[0].GetJoin():
			(x, y) = self.player_list[0].GetLocalPosition()
			self.player_list[1].SetPosition(x, y)
			
		if self.enemy_list[0].GetJoin():
			(x, y) = self.enemy_list[0].GetLocalPosition()
			self.enemy_list[1].SetPosition(x, y)		
				
	def __JoinCheck(self):
			
		if True == self.pc_turn:
			if -1 != self.player_list[0].GetIndex():
				if self.player_list[0].GetIndex() == self.player_list[1].GetIndex():
					self.player_list[0].SetJoin()
					self.player_list[0].SetJoinMember(1)
					self.player_list[1].SetJoin()
					self.player_list[1].SetJoinMember(0)
					self.player_list[1].CharHide()
					self.player_list[1].DisableFlash()
		else:
			if -1 != self.enemy_list[0].GetIndex():
				if self.enemy_list[0].GetIndex() == self.enemy_list[1].GetIndex():
					self.enemy_list[0].SetJoin()
					self.enemy_list[0].SetJoinMember(1)
					self.enemy_list[1].SetJoin()
					self.enemy_list[1].SetJoinMember(0)
					self.enemy_list[1].CharHide()
					self.enemy_list[1].DisableFlash()
			
	def __CatchCheck(self):
	
		bCatch= False
		
		catch_count = len(self.catch_deque)
		score_effect_create = True
		
		while len(self.catch_deque) > 0:
			(is_pc, index) = self.catch_deque.popleft()
				
			catch_ani_pos = None
			notice_str = None
			if is_pc:
				(pos_sx, pos_sy) = self.player_list[index].GetLocalPosition()
				(pos_ex, pos_ey) = self.player_list[index].GetPos()
				catch_ani_pos = (pos_sx -16, pos_sy -16)
				self.player_list[index].CatchPreProcess()
				self.player_list[index].Start([(pos_sx, pos_sy),(pos_ex, pos_ey)])
				notice_str = localeInfo.MINI_GAME_NOTICE_11							# COM 윷말이 PC 잡기에 성공했습니다.
				
				if True == score_effect_create:
					score_effect_create = False
					## 잡기 점수 차감
					if localeInfo.IsARABIC():
						pos_sx = 456 - pos_sx
					self.__CreateScoreEffect(False, YUTNORI_IN_DE_CREASE_SCORE * catch_count, pos_sx, pos_sy)
			else:
				(pos_sx, pos_sy) = self.enemy_list[index].GetLocalPosition()
				(pos_ex, pos_ey) = self.enemy_list[index].GetPos()
				catch_ani_pos = (pos_sx -16, pos_sy -16)
				self.enemy_list[index].CatchPreProcess()
				self.enemy_list[index].Start([(pos_sx, pos_sy),(pos_ex, pos_ey)])
				notice_str = localeInfo.MINI_GAME_NOTICE_10							# PC 윷말이 COM 잡기에 성공했습니다.
				
				if True == score_effect_create:
					score_effect_create = False
					## 잡기 점수 증가
					if localeInfo.IsARABIC():
						pos_sx = 456 - pos_sx
					self.__CreateScoreEffect(True, YUTNORI_IN_DE_CREASE_SCORE * catch_count, pos_sx, pos_sy)
				
			if self.notice_text and notice_str:
				self.notice_text.SetText( notice_str )
				
			if self.catch_ani:
				self.catch_ani.SetPosition( catch_ani_pos[0], catch_ani_pos[1] )
				self.catch_ani.ResetFrame()
				self.catch_ani.Show()
			
			bCatch = True
		
		return bCatch
		
		
	def __TurnCheck(self):
		
		if YUTNORI_STATE_END == self.yutnori_state:
			if self.notice_text:
				self.notice_text.SetText( localeInfo.MINI_GAME_NOTICE_13 )
			
			if self.yut_throw_button:
				self.yut_throw_button.DisableFlash()
					
			if self.reward_button:
				self.reward_button.Enable()
				self.reward_button.EnableFlash()
				
			self.__ClearEffect()
			if True == self.next_turn:
				self.is_goal_text_effect = True
				self.goal_effect_end_frame_func = ui.__mem_func__(self.__PlayerWinPopup)
				if self.goal_effect1:
					self.goal_effect1.Show()
			else:
				for i in xrange(2):
					self.player_list[i].ShowExplosionEffect()
									
			return

		## 현재 턴과 다음 턴이 다르면 교체	
		if self.next_turn != self.pc_turn:
			self.pc_turn = self.next_turn
			
			
		## 다음 턴이 PC 턴이다.
		if True == self.next_turn:
			if YUTNORI_AFTER_TURN_SELECT == self.yutnori_state:
				self.yutnori_state = YUTNORI_STATE_THROW
				self.event_deque.append( [EVENT_TYPE_INSER_DELAY, 1000] )
				self.event_deque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_5] )		# PC의 윷셈이 더 낮아 PC 먼저 이동합니다.
				self.event_deque.append( [EVENT_TYPE_INSER_DELAY, 2000] )
				self.event_deque.append( [EVENT_TYPE_CALL_TURN_CHECK, None] )
			elif YUTNORI_BEFORE_TURN_SELECT == self.yutnori_state:
				print "턴결정시 PC 가 먼저 던지기 때문에 YUTNORI_BEFORE_TURN_SELECT 상태가 될 수 없음"
				pass
			elif YUTNORI_STATE_THROW == self.yutnori_state:
				self.event_deque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_2] )			# 윷 던지기를 통해 진행할 수 있습니다.
				self.event_deque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, True] )							# text color pc turn 으로 변경
				self.event_deque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yut_throw_button, True)] )		# Yut Throw button Enalbe Flush
				
			elif YUTNORI_STATE_RE_THROW == self.yutnori_state:
				self.event_deque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_12] )			# 윷 던지기를 한번 더 할 수 있습니다.
				self.event_deque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, True] )							# text color pc turn 으로 변경
				self.event_deque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yut_throw_button, True)] )		# Yut Throw button Enalbe Flush
				self.__OpenReThrowPopup()
				
			elif YUTNORI_STATE_MOVE == self.yutnori_state:
				self.event_deque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yut_throw_button, False)] )	# Yut Throw button Enalbe Flush
				self.event_deque.append( [EVENT_TYPE_SHOW_UNIT, True] )
				
		## 다음 턴이 COM 턴이다.
		else:
			if YUTNORI_AFTER_TURN_SELECT == self.yutnori_state:
				self.yutnori_state = YUTNORI_STATE_THROW
				self.event_deque.append( [EVENT_TYPE_INSER_DELAY, 1000] )
				self.event_deque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yut_throw_button, False)] )	# Yut Throw button Enalbe Flush
				self.event_deque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_4] )			# COM의 윷셈이 더 낮아 COM 먼저 이동합니다.
				self.event_deque.append( [EVENT_TYPE_INSER_DELAY, 2000] )
				self.event_deque.append( [EVENT_TYPE_CALL_TURN_CHECK, None] )
			elif YUTNORI_BEFORE_TURN_SELECT == self.yutnori_state:
				self.event_deque.append( [EVENT_TYPE_INSER_DELAY, 2000] )
				self.event_deque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yut_throw_button, False)] )	# Yut Throw button Enalbe Flush
				self.event_deque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_3] )			# 턴 결정을 위해 COM의 윷던지기가 진행됩니다.
				self.event_deque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, False] )						# text color com turn 으로 변경
				self.event_deque.append( [EVENT_TYPE_COM_YUT_THROW, None] )								# 컴퓨터가 윷을 던지도록 요청.
			elif self.yutnori_state in [YUTNORI_STATE_THROW, YUTNORI_STATE_RE_THROW]:
				self.event_deque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yut_throw_button, False)] )	# Yut Throw button Enalbe Flush
				self.event_deque.append( [EVENT_TYPE_NOTICE, localeInfo.MINI_GAME_NOTICE_9] )			# COM 진행 중 입니다. 잠시만 기다려주세요
				self.event_deque.append( [EVENT_TYPE_CHANGE_TEXT_COLOR, False] )						# text color com turn 으로 변경
				self.event_deque.append( [EVENT_TYPE_COM_YUT_THROW, None] )								# 컴퓨터가 윷을 던지도록 요청.
			elif YUTNORI_STATE_MOVE == self.yutnori_state:
				self.event_deque.append( [EVENT_TYPE_BUTTON_FLASH, (self.yut_throw_button, False)] )	# Yut Throw button Enalbe Flush
				self.event_deque.append( [EVENT_TYPE_SHOW_UNIT, False] )
				self.event_deque.append( [EVENT_TYPE_REQUEST_COM_ACTION, None] )						## COM 말의 움직임을 요청한다.
		
		
	def PushNextTurn(self, data):
		(next_turn, state)	= data
		self.next_turn		= next_turn
		self.yutnori_state	= state
		
	def PushCatchYut(self, data):
		self.catch_deque.append( data )
		
	def SetScore(self, score):
		self.before_score = self.score
		self.score = score
		
	def __RefreshScore(self):
		if not self.score_text:
			return
		
		if self.score < LOW_TOTAL_SCORE:
			self.score_text.SetPackedFontColor( TOTAL_SCORE_LOW_FONT_COLOR )
		elif self.score < MID_TOTAL_SCORE:
			self.score_text.SetPackedFontColor( TOTAL_SCORE_MID_FONT_COLOR )
		else:
			self.score_text.SetPackedFontColor( TOTAL_SCORE_HIGH_FONT_COLOR )
		
		self.score_text.SetText( str(self.score) )
		
	## 윷 던지기 점수 차감
	def __ThrowScoreCheck(self):
		if not self.yut_throw_button:
			return
			
		## COM 은 점수 차감이 없다
		if False == self.pc_turn:
			return
			
		if self.before_score == self.score:
			return
		
		(s_x, s_y) = self.yut_throw_button.GetLocalPosition() # 328, 180
		
		if localeInfo.IsARABIC():
			s_x = s_x - 52
		else:
			s_x = s_x + 52
			
		## 점수 감소
		self.__CreateScoreEffect(False, YUTNORI_IN_DE_CREASE_SCORE, s_x, s_y)
	
	def __GoalScore(self, is_pc, is_join):
		in_de_crease_scroe = YUTNORI_IN_DE_CREASE_SCORE
		if True == is_join:
			in_de_crease_scroe = in_de_crease_scroe * 2
			
		s_x = 283
		s_y = 307
		
		if localeInfo.IsARABIC():
			(b_x, b_y) = self.board.GetLocalPosition()
			s_x = b_x - (s_x + 124)
			
		if True == is_pc:
			self.__CreateScoreEffect(True, in_de_crease_scroe, s_x, s_y)
		else:
			self.__CreateScoreEffect(False, in_de_crease_scroe, s_x, s_y)
		
	def SetRemainCount(self, remain_count):
		if not self.remain_count_text:
			return
		
		if remain_count < 6:
			self.remain_count_text.SetPackedFontColor( REMAIN_COUNT_LOW_FONT_COLOR )
		else:
			self.remain_count_text.SetPackedFontColor( REMAIN_COUNT_DEFAULT_FONT_COLOR )
			
		self.remain_count_text.SetText( str(remain_count) )		
		
	def __OpenReThrowPopup(self):
		if not self.re_throw_popup:
			self.re_throw_popup = uiCommon.PopupDialog()
			self.re_throw_popup.SetText( localeInfo.MINI_GAME_YUTNORI_RETHROW_POPUP )
			self.re_throw_popup.SetAcceptEvent( ui.__mem_func__(self.__ClickThrowButton) )
			self.re_throw_popup.SetWidth( 456 )
			self.re_throw_popup.SetButtonUpVisual( "d:/ymir work/ui/public/large_button_01.sub" )
			self.re_throw_popup.SetButtonOverVisual( "d:/ymir work/ui/public/large_button_02.sub" )
			self.re_throw_popup.SetButtonDownVisual( "d:/ymir work/ui/public/large_button_03.sub" )
			self.re_throw_popup.SetButtonHorizontalAlignCenter()
			self.re_throw_popup.SetButtonNameAutoSize( localeInfo.MINI_GAME_YUTNORI_RETHROW_BUTTON )
			
		self.re_throw_popup.Open()
			
	def __PlayerWinPopup(self):
		if not self.pc_win_popup:
			self.pc_win_popup = uiCommon.PopupDialog2()
			self.pc_win_popup.SetText1( localeInfo.MINI_GAME_YUTNORI_PC_WIN )
			self.pc_win_popup.SetWidth( 456 )
			
		self.pc_win_popup.SetText2( localeInfo.MINI_GAME_YUTNORI_PC_WIN_SCORE % self.score )
		self.pc_win_popup.Open()
						
	def __ComWinPopup(self):
		if not self.com_win_popup:
			self.com_win_popup = uiCommon.PopupDialog()
			self.com_win_popup.SetText( localeInfo.MINI_GAME_YUTNORI_COM_WIN )
			self.com_win_popup.SetWidth( 456 )
		
		self.com_win_popup.Open()
		
		
class MiniGameYutnori(ui.Window):
			
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

	def Destroy(self):
		self.isLoaded	= 0
		self.state		= STATE_NONE
		self.cur_page	= None
		
		if self.waiting_page:
			self.waiting_page.Destroy()
			self.waiting_page = None
			
		if self.game_page:
			self.game_page.Destroy()
			self.game_page = None
		
	def __LoadWindow(self):
		
		if self.isLoaded == 1:
			return
			
		self.isLoaded	= 1
		self.state		= STATE_WAITING
		
		try:
			self.waiting_page	= YutnoriWaitingPage()
			self.game_page		= YutnoriGamePage()
			
		except:
			import exception
			exception.Abort("MiniGameYutnori.LoadWindow")
		
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
	
	def YutnoriProcess(self, type, data):
				
		if not self.cur_page:
			return
		if not self.waiting_page:
			return
		if not self.game_page:
			return
			
		if 10 == type:
			if STATE_PLAY == self.state:
				self.game_page.SetYut()
				
		elif 0 == type:
		
			self.state = STATE_PLAY
			if self.waiting_page:
				self.waiting_page.Close()
			if self.game_page:
				self.game_page.Destroy()
				
			self.Open()
			
		elif 1 == type:
			if STATE_PLAY == self.state:
				self.state = STATE_WAITING
				self.game_page.Close( True )
				self.game_page.Destroy()
				
		elif 2 == type:
			if STATE_PLAY == self.state:
				self.game_page.SetProb(data)
				
		elif 3 == type:
			if STATE_PLAY == self.state:
				self.game_page.ThrowResult(data)
				
		elif 4 == type:
			if STATE_PLAY == self.state:
				self.game_page.YutMove(data)
				
		elif 5 == type:
			if STATE_PLAY == self.state:
				self.game_page.AvailableAreaShow(data)
				
		elif 6 == type:
			if STATE_PLAY == self.state:
				self.game_page.PushCatchYut(data)
				
		elif 7 == type:
			if STATE_PLAY == self.state:
				self.game_page.SetScore(data)
				
		elif 8 == type:
			if STATE_PLAY == self.state:
				self.game_page.SetRemainCount(data)
				
		elif 9 == type:
			if STATE_PLAY == self.state:
				self.game_page.PushNextTurn(data)
