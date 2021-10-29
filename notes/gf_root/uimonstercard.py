import ui
import uiScriptLocale
import app
import m2netm2g
import dbg
import snd
import playerm2g2
import mouseModule
import wndMgr
import skill
import playerSettingModule
import quest
import localeInfo
import uiToolTip
import constInfo
import emotion
import chr
import item
import uiPrivateShopBuilder
import chatm2g
import uiCommon
import uiAffectShower
import uiToolTip
import nonplayer

from collections import deque

def unsigned32(n):
	return n & 0xFFFFFFFFL
	
ROOT_PATH = "d:/ymir work/ui/game/monster_card/"
CARD_PATH = "d:/ymir work/ui/game/monster_card/card/"

## 카드 미션
WAIT_ARRAY_WIDTH		= 8		## 미션 페이지 WAIT 화면 가로 8칸
WAIT_ARRAY_HEIGHT		= 2		## 미션 페이지 WAIT 화면 세로 2칸
SELECTED_ARRAY_WIDTH	= 3		## 미션 페이지 선택 화면 가로 3칸, 세로 1칸

MISSION_STATE_NONE		 = 0
MISSION_STATE_WAIT		 = 1	## 대기 상태( 미션 받기 전)
MISSION_STATE_PROCEEDING = 2	## 진행중
MISSION_STATE_REWARD	 = 3	## 보상단계

MISSION_INDEX_STAGE			= 0
MISSION_INDEX_MOB_VNUM		= 1
MISSION_INDEX_MOB_CLEAR		= 2
MISSION_INDEX_RESET_TIME	= 3
MISSION_INDEX_RESET_COUNT	= 4
MISSION_INDEX_SHUFFLE_COUNT = 5

CARD_MOVE_SPEED		= 10.0		## 카드 이동 속도

SHUFFLE_MAX = 1					## 셔플 최대 횟수

FAILED_MISSION_SHUFFLE_NO_ITEM			= 0
FAILED_MISSION_INIT_ITEM_FALL_SHORT		= 1
FAILED_MISSION_REWARD_INVEN_FULL		= 2
FAILED_MISSION_REWARD_NO_CLEAR			= 3
FAILED_MSSION_COMMON_MSG				= 4
FAILED_MISSION_MSG_MAX					= 5
	
CARD_IMG_DICT =  \
{
	0	: ROOT_PATH + "empty_card.sub",
	151 : CARD_PATH + "151.sub",
	152 : CARD_PATH + "152.sub",
	153 : CARD_PATH + "153.sub",
	154 : CARD_PATH + "154.sub",
	155 : CARD_PATH + "155.sub",
	191 : CARD_PATH + "191.sub",
	192 : CARD_PATH + "192.sub",
	193 : CARD_PATH + "193.sub",
	194 : CARD_PATH + "194.sub",
	391 : CARD_PATH + "391.sub",
	393 : CARD_PATH + "393.sub",
	394 : CARD_PATH + "394.sub",
	431 : CARD_PATH + "431.sub",
	432 : CARD_PATH + "432.sub",
	433 : CARD_PATH + "433.sub",
	434 : CARD_PATH + "434.sub",
	435 : CARD_PATH + "435.sub",
	436 : CARD_PATH + "436.sub",
	491 : CARD_PATH + "491.sub",
	492 : CARD_PATH + "492.sub",
	493 : CARD_PATH + "493.sub",
	494 : CARD_PATH + "494.sub",
	533 : CARD_PATH + "533.sub",
	534 : CARD_PATH + "534.sub",
	591 : CARD_PATH + "591.sub",
	595 : CARD_PATH + "595.sub",
	691 : CARD_PATH + "691.sub",
	791 : CARD_PATH + "791.sub",
	1091 : CARD_PATH + "1091.sub",
	1093 : CARD_PATH + "1093.sub",
	1192 : CARD_PATH + "1192.sub",
	1901 : CARD_PATH + "1901.sub",
	1304 : CARD_PATH + "1304.sub",
	2092 : CARD_PATH + "2092.sub",
	2191 : CARD_PATH + "2191.sub",
	2206 : CARD_PATH + "2206.sub",
	2402 : CARD_PATH + "2402.sub",
	2306 : CARD_PATH + "2306.sub",
	2492 : CARD_PATH + "2492.sub",
	2493 : CARD_PATH + "2493.sub",
	2597 : CARD_PATH + "2597.sub",
	3091 : CARD_PATH + "3091.sub",
	3191 : CARD_PATH + "3191.sub",
	3291 : CARD_PATH + "3291.sub",
	3491 : CARD_PATH + "3491.sub",
	3591 : CARD_PATH + "3591.sub",
	3596 : CARD_PATH + "3596.sub",
	3791 : CARD_PATH + "3791.sub",
	3891 : CARD_PATH + "3891.sub",
	3910 : CARD_PATH + "3910.sub",
	5161 : CARD_PATH + "5161.sub",
	5162 : CARD_PATH + "5162.sub",
	5163 : CARD_PATH + "5163.sub",
	6009 : CARD_PATH + "6009.sub",
	6091 : CARD_PATH + "6091.sub",
	6109 : CARD_PATH + "6109.sub",
	6191 : CARD_PATH + "6191.sub",
	6192 : CARD_PATH + "6192.sub",
	6392 : CARD_PATH + "6392.sub",
	6405 : CARD_PATH + "6405.sub",
	6116 : CARD_PATH + "6116.sub",
	6407 : CARD_PATH + "6407.sub",
	6408 : CARD_PATH + "6408.sub",
}

if app.ENABLE_12ZI:
	CARD_IMG_DICT[2752] = CARD_PATH + "2752.sub"	## 12zi 자
	CARD_IMG_DICT[2762] = CARD_PATH + "2762.sub"	## 12zi 축
	CARD_IMG_DICT[2772] = CARD_PATH + "2772.sub"	## 12zi 인
	CARD_IMG_DICT[2782] = CARD_PATH + "2782.sub"	## 12zi 묘
	CARD_IMG_DICT[2792] = CARD_PATH + "2792.sub"	## 12zi 진
	CARD_IMG_DICT[2802] = CARD_PATH + "2802.sub"	## 12zi 사
	CARD_IMG_DICT[2812] = CARD_PATH + "2812.sub"	## 12zi 오
	CARD_IMG_DICT[2822] = CARD_PATH + "2822.sub"	## 12zi 미
	CARD_IMG_DICT[2832] = CARD_PATH + "2832.sub"	## 12zi 신
	CARD_IMG_DICT[2842] = CARD_PATH + "2842.sub"	## 12zi 유
	CARD_IMG_DICT[2852] = CARD_PATH + "2852.sub"	## 12zi 술
	CARD_IMG_DICT[2862] = CARD_PATH + "2862.sub"	## 12zi 해
	

## 도감
ILLUSTRATED_ARRAY_WIDTH		= 4
ILLUSTRATED_ARRAY_HEIGHT	= 2
STAR_COUNT = 5

ILLUSTRATION_PAGE_MAX			= 5

CLASS_COUNT_MAX = \
{
	0 : 9,		# 별0 ~ 별1
	1 : 21,		# 별1 ~ 별2
	2 : 30,		# 별2 ~ 별3
	3 : 60,		# 별3 ~ 별4
	4 : 90,		# 별4 ~ 별5
	5 : 120,	# 별5 ~ MAX
}

ILLUSTRATION_MODEL_RENDER	= 1
ILLUSTRATION_MOTION_CALSS	= 2
ILLUSTRATION_POLY_CLASS		= 3
ILLUSTRATION_WARP_CLASS		= 4
ILLUSTRATION_SUMMON_CLASS	= 100	# 추후구현
	
	
FAILED_COUNT_MAX = 0
FAILED_POLY_COOLTIME = 1
FAILED_WARP_LIMIT_LEVEL = 2
FAILED_WARP_TRADE = 3
FAILED_ILLUSTRATION_MSG_MAX = 4

TRADE_COUNT = 10	# 교환에 필요한 카드 개수

class MissionPage:
	pass
 
class IllustrationPage:
	pass
 

## 몬스터 카드
class MonsterCardWindow(ui.ScriptWindow):
			
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI")
		self.isLoaded = 0
		self.SetWindowName("MonsterCardWindow")
		
		self.tabDict		= None
		self.tabButtonDict	= None
		self.pageDict		= None
		self.curKey			= None
		self.popup			= None
		self.question		= None
		
		## 미션 페이지
		self.mission_page	= MissionPage()
		self.mission_page.waitArray				= [[0 for col in range(0,WAIT_ARRAY_WIDTH)] for row in range(0,WAIT_ARRAY_HEIGHT)]
		self.mission_page.waitVnumDict			= {}
		self.mission_page.selectedArray			= [0 for col in range(0,SELECTED_ARRAY_WIDTH)]	# 초상화
		self.mission_page.MissionClearImgArray	= [0 for col in range(0,SELECTED_ARRAY_WIDTH)]	# 미션 클리어
		self.mission_page.selectedFrameArray	= [0 for col in range(0,SELECTED_ARRAY_WIDTH)]	# 초상화 프레임
		self.mission_page.seletedMobNameArray	= [0 for col in range(0,SELECTED_ARRAY_WIDTH)]	# 이름(text) 배열
		self.mission_page.seletedAreaImageArray	= [0 for col in range(0,SELECTED_ARRAY_WIDTH)]	# 출현 지역 이미지 배열
		self.mission_page.setectedAreaTextArray	= [0 for col in range(0,SELECTED_ARRAY_WIDTH)]	# 출현 지역 이름(text) 배열
		self.mission_page.recive_mission_button = None	# 미션받기 버튼
		self.mission_page.shuffle_card_button	= None	# 카드배치 버튼		
		self.mission_page.reward_card_button	= None	# 카드받기 버튼
		self.mission_page.mission_init_button	= None	# 초기화 버튼
		self.mission_page.init_question_button	= None	# 물음표 버튼
		self.mission_page.mission_state			= MISSION_STATE_NONE
		self.mission_page.mission_data			= None
		self.mission_page.mission_tuple			= []
		
		self.mission_page.card_move_queue		= deque()
		self.mission_page.move_img				= None
		self.mission_page.lock					= False
		
		
		
		## 일러스트 페이지
		self.illustration_page = IllustrationPage()
		self.illustration_page.CardImageArray		= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardImageAlpha		= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardSelectImage		= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardData				= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardEnergyBGArray	= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]		
		self.illustration_page.CardEnergyImageArray = [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]		
		self.illustration_page.CardAreaImageArray	= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardAreaTextArray	= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardMobNameArray		= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardStarOnArray		= [[[0 for col in range(0,STAR_COUNT)] for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.CardStarOffArray		= [[[0 for col in range(0,STAR_COUNT)] for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		self.illustration_page.solo_cur_page		= 1
		self.illustration_page.solo_page_max		= 0
		self.illustration_page.party_cur_page		= 1
		self.illustration_page.party_page_max		= 0
		
		# 깜박임
		self.illustration_page.flushArray			= [[0 for col in range(0,ILLUSTRATED_ARRAY_WIDTH)] for row in range(0,ILLUSTRATED_ARRAY_HEIGHT)]
		
		## page 버튼
		self.illustration_page.page_button_list		= [0 for col in range(0,ILLUSTRATION_PAGE_MAX)]
		self.illustration_page.first_prev_button	= None	# <<
		self.illustration_page.prev_button			= None	# <
		self.illustration_page.next_button			= None	# >
		self.illustration_page.last_next_button		= None	# >>
		
		## 일러스트 페이지 툴팁
		self.illustration_page.motion_button_tooltip	= None
		self.illustration_page.motion_button_tooltip2	= None
		self.illustration_page.poly_button_tooltip		= None
		self.illustration_page.poly_button_tooltip2		= None
		self.illustration_page.warp_button_tooltip		= None
		self.illustration_page.warp_button_tooltip2		= None
		
		## 모델
		self.illustration_page.cur_model_vnum		= 0
		self.illustration_page.cur_data				= None
		self.illustration_page.cur_model_rotation	= 0.0
		
		## 툴팁
		self.buttontooltip		= None
		self.ShowButtonToolTip	= False
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		
		if self.mission_page.card_move_queue:
			self.mission_page.card_move_queue.clear()
		
	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.ShowPage()
		self.SetTop()
			
	def Hide(self):
		wndMgr.Hide(self.hWnd)
		
	def Close(self):
		
		playerm2g2.IllustrationShow( False )
		playerm2g2.IllustrationSelectModel( 0 )
		self.__ClearIllustrationButton()
		self.illustration_page.cur_model_vnum		= 0
		self.illustration_page.cur_data				= None
		self.illustration_page.cur_model_rotation	= 0.0
		
		if self.illustration_page.mv_reset_button:
			self.illustration_page.mv_reset_button.Hide()
		if self.illustration_page.left_rotation_button:
			self.illustration_page.left_rotation_button.Hide()
		if self.illustration_page.right_rotation_button:
			self.illustration_page.right_rotation_button.Hide()
		if self.illustration_page.zoomin_button:
			self.illustration_page.zoomin_button.Hide()
		if self.illustration_page.zoomout_button:
			self.illustration_page.zoomout_button.Hide()
		if self.illustration_page.mv_up_button:
			self.illustration_page.mv_up_button.Hide()
		if self.illustration_page.mv_down_button:
			self.illustration_page.mv_down_button.Hide()
		
		if self.illustration_page.mv_count_text:
			self.illustration_page.mv_count_text.SetText("")
		if self.illustration_page.mv_name_text:
			self.illustration_page.mv_name_text.SetText("")
			
		self.Hide()
		
		if self.buttontooltip:
			self.buttontooltip.Hide()
			self.ShowButtonToolTip	= False
		
	def OnPressEscapeKey(self):
		self.Close()
		return True
		
	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)
		
	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)
		
	def __LoadWindow(self):
	
		playerm2g2.IllustrationShow( False )
		playerm2g2.IllustrationSelectModel( 0 )
		
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		
		## script
		try:
			self.__LoadScript("UIScript/MonsterCardWindow.py")
				
		except:
			import exception
			exception.Abort("MonsterCardWindow.LoadWindow.__LoadScript")
		
		## object	
		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("MonsterCardWindow.LoadWindow.__BindObject")
			
		## event
		try:	
			self.__BindEvent()
		except:
			import exception
			exception.Abort("MonsterCardWindow.LoadWindow.__BindEvent")
		
		self.SetPage("MISSION")
		
			
	def Destroy(self):
		self.isLoaded = 0
		
	def OnRender(self):
		pass
		
	def __BindObject(self):
		self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))
		
		## 카드미션, 솔플도감, 파티도감
		self.tabDict = {
			"MISSION"	: self.GetChild("tab_menu_1"),
			"SOLO"		: self.GetChild("tab_menu_2"),
			"PARTY"		: self.GetChild("tab_menu_3"),
		}

		self.tabButtonDict = {
			"MISSION"	: self.GetChild("tab_menu_button_1"),
			"SOLO"		: self.GetChild("tab_menu_button_2"),
			"PARTY"		: self.GetChild("tab_menu_button_3"),
		}
		
		
		self.pageDict = {
			"MISSION"	: self.GetChild("mission_page"),
			"SOLO"		: self.GetChild("illustration_page"),
			"PARTY"		: self.GetChild("illustration_page"),
		}
		
		##미션 페이지########################################################################
		## 카드 미션 페이지
		## wait window 에 표시될 이미지들 생성
		## 가로 8 * 세로 2
		wait_window = self.GetChild("wait_card_window")
		for row in xrange(0, WAIT_ARRAY_HEIGHT):
			for col in xrange(0, WAIT_ARRAY_WIDTH):
				ex_image = ui.ExpandedImageBox()
				ex_image.SetParent( wait_window )
				ex_image.LoadImage( CARD_IMG_DICT[0] )
				ex_image.SetPosition( 69 * col + 13 * col , 84 * row + 6 *row )
				ex_image.SetScale( 0.75, 0.75 )
				ex_image.Show()
				self.mission_page.waitArray[row][col] = ex_image
				
		## 미션에 선택된 카드들
		for col in xrange(0,SELECTED_ARRAY_WIDTH):
			# 초상화
			self.mission_page.selectedArray[col] = self.GetChild( "selected_img" + str(col) )
			# 미션 클리어
			self.mission_page.MissionClearImgArray[col] = self.GetChild( "selected_clear_img" + str(col) )
			self.mission_page.MissionClearImgArray[col].Hide()
			# 프레임
			self.mission_page.selectedFrameArray[col] = self.GetChild( "selected_frame" + str(col) )
			# 출현지역
			self.mission_page.seletedAreaImageArray[col] = self.GetChild( "selected_area" + str(col) )
			
			
		## 카드 미션 각종 버튼들
		# 미션받기 버튼
		self.mission_page.recive_mission_button = self.GetChild("recive_mission_button")
		# 카드배치 버튼
		self.mission_page.shuffle_card_button = self.GetChild("shuffle_card_button")
		# 카드받기 버튼
		self.mission_page.reward_card_button = self.GetChild("reward_card_button")
		# 초기화 버튼
		self.mission_page.mission_init_button = self.GetChild("mission_init_button")
		# 물음표 버튼
		self.mission_page.init_question_button = self.GetChild("init_question_button")
		
		## wait 위치 alpha bg
		self.mission_page.wait_card_alpha = self.GetChild("wait_card_alpha_bg_window")
		
		## Alter Text
		self.mission_page.alter_text = self.GetChild("MissionAlterText")
		
		##### 카드 애니메이션에 사용될 move image 한장 생성.	
		self.mission_page.move_img = ui.MoveImageBox()
		self.mission_page.move_img.SetParent( self.GetChild("mission_page") )
		self.mission_page.move_img.SetEndMoveEvent( ui.__mem_func__(self.CardMoveEndEvnet) )
		self.mission_page.move_img.SetMoveSpeed(CARD_MOVE_SPEED)
		self.mission_page.move_img.Hide()
		#####
		
		##일러스트 페이지########################################################################
		## illustration card 표시될 이미지들 생성
		## 가로 4 * 세로 2
		#ILLUSTRATED_ARRAY_WIDTH	= 4
		#ILLUSTRATED_ARRAY_HEIGHT	= 2
		for row in xrange(0, ILLUSTRATED_ARRAY_HEIGHT):
			for col in xrange(0, ILLUSTRATED_ARRAY_WIDTH):
				## 초상화
				ex_image = ui.ExpandedImageBox()
				ex_image.SetParent( self.GetChild("illustrated_window") )
				ex_image.LoadImage( CARD_IMG_DICT[0] )
				# x,y = (42,113) - (21,75)
				# img width, height = (92,112)
				# gap 29, 89
				ex_image.SetPosition( 21 + (col* 92) + (col*29), 38 + (row*112) + (row*89) )
				ex_image.Show()
				self.illustration_page.CardImageArray[row][col] = ex_image
				## 초상화 알파
				alpha_image = ui.ExpandedImageBox()
				alpha_image.SetParent( self.GetChild("illustrated_window") )
				alpha_image.LoadImage( ROOT_PATH + "card_alpha.sub" )
				alpha_image.SetPosition( 21 + (col* 92) + (col*29), 38 + (row*112) + (row*89) )
				alpha_image.Show()
				self.illustration_page.CardImageAlpha[row][col] = alpha_image
				
				## 초상화 라인
				alpha_image = ui.ExpandedImageBox()
				alpha_image.SetParent( self.GetChild("illustrated_window") )
				alpha_image.LoadImage( ROOT_PATH + "card_view_line.sub" )
				alpha_image.SetPosition( 21 + (col* 92) + (col*29), 38 + (row*112) + (row*89) )
				alpha_image.Hide()
				self.illustration_page.CardSelectImage[row][col] = alpha_image
				
				## 깜박임
				ani_image = ui.AniImageBox()
				ani_image.SetParent( self.GetChild("illustrated_window") )
				ani_image.SetDelay( 6 )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect2.sub" )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect3.sub" )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect4.sub" )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect5.sub" )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect4.sub" )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect3.sub" )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect2.sub" )
				ani_image.AppendImage( "D:/Ymir Work/UI/game/monster_card/card_effect/card_effect1.sub" )
				ani_image.SetPosition( 21 + (col* 92) + (col*29), 38 + (row*112) + (row*89) )
				ani_image.Hide()
				self.illustration_page.flushArray[row][col] = ani_image
				
				## 에너지바 bg 생성
				# x,y = (44,234) - (21,75)
				# img width, height = (88,10)
				# gap 33, 191
				energy_bg_image = ui.ExpandedImageBox()
				energy_bg_image.SetParent( self.GetChild("illustrated_window") )
				energy_bg_image.LoadImage( ROOT_PATH + "energy_bar_bg.sub" )
				energy_bg_image.SetPosition( 23 + (col* 88) + (col*33), 159 + (row*10) + (row*191) )
				energy_bg_image.Show()
				self.illustration_page.CardEnergyBGArray[row][col] = energy_bg_image
				## 에너지바 img 생성
				energu_image = ui.ExpandedImageBox()
				energu_image.SetParent( energy_bg_image )
				energu_image.LoadImage( ROOT_PATH + "energy_bar.sub" )
				energu_image.SetPosition(1,1)
				energu_image.Show()
				self.illustration_page.CardEnergyImageArray[row][col] = energu_image
				
				## 등급(star) 생성
				for cnt in xrange(0, STAR_COUNT):
					star_off_image = ui.ExpandedImageBox()
					star_off_image.SetParent( self.GetChild("star_window" + str(row) + str(col) ) )
					star_off_image.LoadImage( ROOT_PATH + "star_bg.sub" )
					star_off_image.SetPosition( 16 * cnt , 0)
					star_off_image.Show()
					self.illustration_page.CardStarOffArray[row][col][cnt] = star_off_image
					
					star_on_image = ui.ExpandedImageBox()
					star_on_image.SetParent( self.GetChild("star_window" + str(row) + str(col) ) )
					star_on_image.LoadImage( ROOT_PATH + "star_img.sub" )
					star_on_image.SetPosition( 16 * cnt , 0)
					star_on_image.Show()
					self.illustration_page.CardStarOnArray[row][col][cnt] = star_on_image
				#출현지역
				self.illustration_page.CardAreaImageArray[row][col] = self.GetChild( "illustrated_area" + str(row) + str(col) )
			
		## 승급 버튼
		self.illustration_page.promotion_button		= self.GetChild("promotion_button")
		## 교환 버튼
		self.illustration_page.exchange_button		= self.GetChild("exchange_button")
		## 모션 버튼
		self.illustration_page.motion_button		= self.GetChild("motion_button")
		## 변신 버튼
		self.illustration_page.poly_button			= self.GetChild("poly_button")
		## 이동 버튼
		self.illustration_page.warp_button			= self.GetChild("warp_button")
		## 소환 버튼
		self.illustration_page.summon_button		= self.GetChild("summon_button")
		
		## 모델뷰 이름
		self.illustration_page.mv_name_text			= self.GetChild("MV_name_text")
		## 모델뷰 초기화 버튼
		self.illustration_page.mv_reset_button		= self.GetChild( "mv_reset_button" )
		self.illustration_page.mv_reset_button.Hide()
		## 모델뷰 회전 버튼
		self.illustration_page.left_rotation_button	= self.GetChild( "mv_left_rotation_button" )
		self.illustration_page.left_rotation_button.Hide()
		self.illustration_page.right_rotation_button= self.GetChild( "mv_right_rotation_button" )
		self.illustration_page.right_rotation_button.Hide()
		## 모델뷰 확대,축소 버튼
		self.illustration_page.zoomin_button		= self.GetChild( "mv_zoomin_button" )
		self.illustration_page.zoomin_button.Hide()
		self.illustration_page.zoomout_button		= self.GetChild( "mv_zoomout_button" )
		self.illustration_page.zoomout_button.Hide()
		## 모델뷰 상,하 버튼
		self.illustration_page.mv_up_button			= self.GetChild( "mv_up_camera_button" )
		self.illustration_page.mv_up_button.Hide()
		self.illustration_page.mv_down_button		= self.GetChild( "mv_down_camera_button" )
		self.illustration_page.mv_down_button.Hide()
		
		## 누적 등록 횟수
		self.illustration_page.mv_count_text		= self.GetChild("MV_countText")
		## page 버튼
		for button_index in range(ILLUSTRATION_PAGE_MAX):
			self.illustration_page.page_button_list[button_index] = self.GetChild( "page_button" + str(button_index) )
		
		self.illustration_page.first_prev_button	= self.GetChild( "first_prev_button" )	# <<
		self.illustration_page.prev_button			= self.GetChild( "prev_button" )		# <
		self.illustration_page.next_button			= self.GetChild( "next_button" )		# >
		self.illustration_page.last_next_button		= self.GetChild( "last_next_button" )	# >>
		
		## 툴팁
		self.buttontooltip = uiToolTip.ToolTip()
		self.buttontooltip.ClearToolTip()
		
		
		
	def __BindEvent(self):
		##미션 페이지########################################################################
		## 몬스터 카드 상단 탭 ui. 카드미션,솔플도감,파티도감
		if localeInfo.IsARABIC():
			for (tabKey, tabValue) in self.tabDict.items():
				tabValue.LeftRightReverse()
			
		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.__OnClickTabButton), tabKey)
			
		self.tabButtonDict["MISSION"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_TAB_BUTTON_CARD_MISSION)
		self.tabButtonDict["MISSION"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.tabButtonDict["SOLO"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_TAB_BUTTON_SOLO)
		self.tabButtonDict["SOLO"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		self.tabButtonDict["PARTY"].SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_TAB_BUTTON_PARTY)
		self.tabButtonDict["PARTY"].SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		
		## 미션에 선택된 카드들
		for col in xrange(0,SELECTED_ARRAY_WIDTH):
			# 프레임
			self.mission_page.selectedFrameArray[col].SetEvent(ui.__mem_func__(self.__SelectedImgOverIn), "mouse_over_in", col)
			self.mission_page.selectedFrameArray[col].SetEvent(ui.__mem_func__(self.__SelectedImgOverOut), "mouse_over_out", col)
			# 출현지역
			self.mission_page.seletedAreaImageArray[col].SetEvent(ui.__mem_func__(self.__EmergenceAreaOverIn), "mouse_over_in", col)
			self.mission_page.seletedAreaImageArray[col].SetEvent(ui.__mem_func__(self.__EmergenceAreaOverOut), "mouse_over_out", col)
			
		# 미션받기 버튼
		self.mission_page.recive_mission_button.SetEvent(ui.__mem_func__(self.__OnClickReciveMissionButton) )
		self.mission_page.recive_mission_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_REQUEST_MISSION_BUTTON)
		self.mission_page.recive_mission_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		# 카드배치 버튼
		self.mission_page.shuffle_card_button.SetEvent(ui.__mem_func__(self.__OnClickShuffleCardButton) )
		self.mission_page.shuffle_card_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_SHUFFLE_BUTTON)
		self.mission_page.shuffle_card_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		# 카드받기 버튼
		self.mission_page.reward_card_button.SetEvent(ui.__mem_func__(self.__OnClickRewardCardButton) )
		self.mission_page.reward_card_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_REWARD_CARD_BUTTON)
		self.mission_page.reward_card_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		# 초기화 버튼
		self.mission_page.mission_init_button.SetEvent(ui.__mem_func__(self.__OnClickMissionInitButton) )
		self.mission_page.mission_init_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_MISSION_INIT_BUTTON)
		self.mission_page.mission_init_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		# 물음표 버튼
		self.mission_page.init_question_button = self.GetChild("init_question_button")
		init_question_desclist = [localeInfo.MC_QUESTION_BUTTON_DESC1, localeInfo.MC_QUESTION_BUTTON_DESC2, localeInfo.MC_QUESTION_BUTTON_DESC3]
		self.mission_page.init_question_button.SetToolTipWindow( self.__CreateGameTypeToolTip("", init_question_desclist) )
		self.mission_page.init_question_button.SetEvent(ui.__mem_func__(self.__OnClickQuestionButton) )
		
		
		## 일러스트 페이지 ########################################################	
		## 승급 버튼
		self.illustration_page.promotion_button.SetEvent(ui.__mem_func__(self.__OnClickPromotionButton) )
		self.illustration_page.promotion_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_PROMOTION_BUTTON)
		self.illustration_page.promotion_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		## 교환 버튼
		self.illustration_page.exchange_button.SetEvent(ui.__mem_func__(self.__OnClickExchangeButton) )
		self.illustration_page.exchange_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_EXCHANGE_BUTTON)
		self.illustration_page.exchange_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))
		## 모션 버튼
		self.illustration_page.motion_button.SetEvent(ui.__mem_func__(self.__OnClickMotionButton) )
		self.illustration_page.motion_button.SetAlwaysToolTip(True)
		## 모션 툴팁
		self.illustration_page.motion_button_tooltip = uiToolTip.ToolTip()
		self.illustration_page.motion_button_tooltip.ClearToolTip()
		self.illustration_page.motion_button_tooltip.SetThinBoardSize(11 * len(str(uiScriptLocale.MC_MOTION_BUTTON)))
		self.illustration_page.motion_button_tooltip.AppendTextLine(uiScriptLocale.MC_MOTION_BUTTON, 0xffffffff)
		motion_tooltip_list = [uiScriptLocale.MC_MOTION_BUTTON, localeInfo.MC_MOTION_BUTTON_OVER_MSG]
		self.illustration_page.motion_button_tooltip2 = self.__CreateGameTypeToolTip("", motion_tooltip_list)
		## 변신 버튼
		self.illustration_page.poly_button.SetEvent(ui.__mem_func__(self.__OnClickPolyButton) )
		self.illustration_page.poly_button.SetAlwaysToolTip(True)
		## 변신 툴팁
		self.illustration_page.poly_button_tooltip = uiToolTip.ToolTip()
		self.illustration_page.poly_button_tooltip.ClearToolTip()
		self.illustration_page.poly_button_tooltip.SetThinBoardSize(11 * len(str(uiScriptLocale.MC_POLY_BUTTON)))
		self.illustration_page.poly_button_tooltip.AppendTextLine(uiScriptLocale.MC_POLY_BUTTON, 0xffffffff)
		poly_tooltip_list = [uiScriptLocale.MC_POLY_BUTTON, localeInfo.MC_POLY_BUTTON_OVER_MSG]
		self.illustration_page.poly_button_tooltip2 = self.__CreateGameTypeToolTip("", poly_tooltip_list)		
		## 이동 버튼
		self.illustration_page.warp_button.SetEvent(ui.__mem_func__(self.__OnClickWarpButton) )
		self.illustration_page.warp_button.SetAlwaysToolTip(True)
		## 이동 툴팁
		self.illustration_page.warp_button_tooltip = uiToolTip.ToolTip()
		self.illustration_page.warp_button_tooltip.ClearToolTip()
		self.illustration_page.warp_button_tooltip.SetThinBoardSize(11 * len(str(uiScriptLocale.MC_WARP_BUTTON)))
		self.illustration_page.warp_button_tooltip.AppendTextLine(uiScriptLocale.MC_WARP_BUTTON, 0xffffffff)
		warp_tooltip_list = [uiScriptLocale.MC_WARP_BUTTON, localeInfo.MC_WARP_BUTTON_OVER_MSG]
		self.illustration_page.warp_button_tooltip2 = self.__CreateGameTypeToolTip("", warp_tooltip_list)
		## 소환 버튼
		self.illustration_page.summon_button.SetEvent(ui.__mem_func__(self.__OnClickSummonButton) )
		self.illustration_page.summon_button.SetShowToolTipEvent(ui.__mem_func__(self.OverInToolTipButton), uiScriptLocale.MC_SUMMON_BUTTON)
		self.illustration_page.summon_button.SetHideToolTipEvent(ui.__mem_func__(self.OverOutToolTipButton))		
		self.illustration_page.summon_button.SetAlwaysToolTip(True)
		
		## 모델뷰 초기화 버튼
		self.illustration_page.mv_reset_button.SetEvent(ui.__mem_func__(self.__ModelViewReset) )
		
		## page 버튼
		for button_index in range(ILLUSTRATION_PAGE_MAX):
			self.illustration_page.page_button_list[button_index].SetEvent(ui.__mem_func__(self.__OnClickPageButton), button_index)
		
		self.illustration_page.first_prev_button.SetEvent(ui.__mem_func__(self.__OnClickFirstPrevPageButton))
		self.illustration_page.prev_button.SetEvent(ui.__mem_func__(self.__OnClickPrevPageButton))
		self.illustration_page.next_button.SetEvent(ui.__mem_func__(self.__OnClickNextPageButton))
		self.illustration_page.last_next_button.SetEvent(ui.__mem_func__(self.__OnClickLastNextPageButton))
		
		if localeInfo.IsARABIC():
			temp_pos_list = [0 for col in range(0,ILLUSTRATION_PAGE_MAX)]
			for button_index in range(ILLUSTRATION_PAGE_MAX):
				temp_pos_list[button_index] = self.illustration_page.page_button_list[button_index].GetLocalPosition()
				
			for button_index in range(ILLUSTRATION_PAGE_MAX):
				x = temp_pos_list[ILLUSTRATION_PAGE_MAX -1 -button_index][0]
				y = temp_pos_list[ILLUSTRATION_PAGE_MAX -1 -button_index][1]
				self.illustration_page.page_button_list[button_index].SetPosition(x, y)
				
			temp_pos	= self.illustration_page.first_prev_button.GetLocalPosition()
			temp_pos2	= self.illustration_page.last_next_button.GetLocalPosition()
			self.illustration_page.first_prev_button.SetPosition( temp_pos2[0], temp_pos2[1])
			self.illustration_page.last_next_button.SetPosition( temp_pos[0], temp_pos[1])
			
			temp_pos	= self.illustration_page.prev_button.GetLocalPosition()
			temp_pos2	= self.illustration_page.next_button.GetLocalPosition()
			self.illustration_page.prev_button.SetPosition( temp_pos2[0], temp_pos2[1])
			self.illustration_page.next_button.SetPosition( temp_pos[0], temp_pos[1])
			
			self.illustration_page.first_prev_button.LeftRightReverse()
			self.illustration_page.prev_button.LeftRightReverse()
			self.illustration_page.next_button.LeftRightReverse()
			self.illustration_page.last_next_button.LeftRightReverse()
				
		for row in xrange(0, ILLUSTRATED_ARRAY_HEIGHT):
			for col in xrange(0, ILLUSTRATED_ARRAY_WIDTH):
				## 초상화
				self.illustration_page.CardImageArray[row][col].SetEvent(ui.__mem_func__(self.__IllustrationImgOverIn), "mouse_over_in", row, col)
				self.illustration_page.CardImageArray[row][col].SetEvent(ui.__mem_func__(self.__IllustrationImgOverOut), "mouse_over_out", row, col)				
				self.illustration_page.CardImageArray[row][col].SetEvent( ui.__mem_func__(self.__CardImgClick), "mouse_click", row, col)
				## 초상화 라인
				self.illustration_page.CardSelectImage[row][col].SetEvent(ui.__mem_func__(self.__IllustrationImgOverIn), "mouse_over_in", row, col)
				self.illustration_page.CardSelectImage[row][col].SetEvent(ui.__mem_func__(self.__IllustrationImgOverOut), "mouse_over_out", row, col)	
				self.illustration_page.CardSelectImage[row][col].SetEvent( ui.__mem_func__(self.__CardImgClick), "mouse_click", row, col)
				## 초상화 알파
				self.illustration_page.CardImageAlpha[row][col].SetEvent(ui.__mem_func__(self.__IllustrationImgOverIn), "mouse_over_in", row, col)
				self.illustration_page.CardImageAlpha[row][col].SetEvent(ui.__mem_func__(self.__IllustrationImgOverOut), "mouse_over_out", row, col)	
				self.illustration_page.CardImageAlpha[row][col].SetEvent( ui.__mem_func__(self.__CardImgClick), "mouse_click", row, col)
				## 출현지역
				self.illustration_page.CardAreaImageArray[row][col].SetEvent(ui.__mem_func__(self.__IllustrationEmergenceAreaOverIn), "mouse_over_in", row, col)
				self.illustration_page.CardAreaImageArray[row][col].SetEvent(ui.__mem_func__(self.__IllustrationEmergenceAreaOverOut), "mouse_over_out", row, col)	
		
				
	def __CreateGameTypeToolTip(self, title, descList):
		
		toolTip = uiToolTip.ToolTip()
		
		if title:
			toolTip.SetTitle(title)
			toolTip.AppendSpace(5)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)
			
		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip
	
	def __OnClickTabButton(self, tabKey):
		if self.mission_page.lock:
			return
			
		self.SetPage( tabKey )
		
	def SetPage(self, key):
	
		self.curKey = key
	
		for (tabKey, tabButton) in self.tabButtonDict.items():
			if tabKey != key:
				tabButton.SetUp()
				
		for tabMenuImg in self.tabDict.itervalues():
			tabMenuImg.Hide()
			
		for pageWindow in self.pageDict.itervalues():
			pageWindow.Hide()
			
		
		self.tabDict[key].Show()
		self.pageDict[key].Show()
		self.ShowPage()
		
	def ShowPage(self):
	
		if not self.IsShow():
			return
			
		if "MISSION" == self.curKey:
			self.__ShowMissionPage()
		if "SOLO" == self.curKey:
			self.ShowSoloPage()
		if "PARTY" == self.curKey:
			self.ShowPartyPage()
	
	def OverInToolTipButton(self, btnText):
	
		if self.buttontooltip:
			texts = btnText.split('\\n')
			if texts[-1] == "":
				del texts[-1]
			lens = [len(text) for text in texts]
			text_max_len = max(lens) + 2
			
			pos_x, pos_y = wndMgr.GetMousePosition()
			
			self.buttontooltip.ClearToolTip()
			self.buttontooltip.SetThinBoardSize(11 * text_max_len)
			for text in texts:
				self.buttontooltip.AppendTextLine(text, 0xffffffff)
			self.buttontooltip.SetToolTipPosition(pos_x, pos_y - 20)
			self.buttontooltip.Show()
			self.buttontooltip.SetTop()
			self.ShowButtonToolTip = True

	def OverOutToolTipButton(self):
	
		if self.buttontooltip:
			self.buttontooltip.Hide()
			self.ShowButtonToolTip = False
			
	def ButtonToolTipProgress(self):
		if self.buttontooltip and self.ShowButtonToolTip:
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.buttontooltip.SetToolTipPosition(pos_x, pos_y - 20)
			
	## Update
	def OnUpdate(self):
	
		self.ButtonToolTipProgress()
		
		self.__ModelUpDownCameraProgress()
		self.__ModelRotationProgress()
		self.__ModelZoomProgress()
			
		## 카드 애니메이션 관련
		if len(self.mission_page.card_move_queue) > 0:
		
			if False == self.mission_page.move_img.GetMove():
				self.CardMoveStartEvent()
				
			else:
				(dst_index, dst_vnum) = self.mission_page.card_move_queue[0][1]
				(dstX, dstY) = self.mission_page.selectedArray[dst_index].GetGlobalPosition()
				self.mission_page.move_img.SetMovePosition(dstX, dstY)
			
	## 미션 페이지 ########################################################
	## 상태 갱신
	def __RefreshMissionState(self):
			
		## mob_vnum 이 하나라도 0 이면 미션 받기 전 상태
		if False == any( self.mission_page.mission_data[MISSION_INDEX_MOB_VNUM] ):
			self.mission_page.mission_state		= MISSION_STATE_WAIT
			return
		
		## mission clear 가 모두 참이면 보상단계, 아니라면 진행중
		if all( self.mission_page.mission_data[MISSION_INDEX_MOB_CLEAR] ):
			self.mission_page.mission_state	= MISSION_STATE_REWARD
		else:
			self.mission_page.mission_state	= MISSION_STATE_PROCEEDING
		
	def RefreshMissionPage(self):
		self.mission_page.mission_data = playerm2g2.GetMonsterCardMissionInfo()
		
		if not self.mission_page.mission_data:
			print "if not self.mission_page.mission_data"
			return
			
		## 상태 갱신
		self.__RefreshMissionState()
		
		## 상태에 따른 동작
		if MISSION_STATE_WAIT == self.mission_page.mission_state:
			self.__SetMissionWait()
		elif MISSION_STATE_NONE == self.mission_page.mission_state:
			print "MISSION_STATE_NONE 입니다~~~~~~~~~"
		else: 
			# MISSION_STATE_PROCEEDING, MISSION_STATE_REWARD 상태일때
			self.__SetMissionProceeding()		
			
			
	## 대기상태( 미션 받기 전 )
	def __SetMissionWait(self):
		if MISSION_STATE_WAIT != self.mission_page.mission_state:
			return
			
		## 화면 초기화
		self.__MissionPageClear()
			
		if not self.mission_page.mission_data:
			print "if not self.mission_page.mission_data"
			return
			
		cur_stage = self.mission_page.mission_data[MISSION_INDEX_STAGE]
		if 0 == cur_stage:
			return

		if self.mission_page.alter_text:
			self.mission_page.alter_text.SetText(localeInfo.MC_ALTER_TEXT % (cur_stage))
		
		
		self.mission_page.mission_tuple = playerm2g2.GetMissionVec( cur_stage )
		if not self.mission_page.mission_tuple:
			return
		data_count = len( self.mission_page.mission_tuple )
		
		if 0 >= data_count or data_count > WAIT_ARRAY_HEIGHT*WAIT_ARRAY_WIDTH:
			return
		
		# type 0 : solo, type 1 : party
		#	(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = data		
		for row in xrange(0, WAIT_ARRAY_HEIGHT):
			for col in xrange(0, WAIT_ARRAY_WIDTH):
				index = row * WAIT_ARRAY_WIDTH + col
				if index < data_count:
					(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = self.mission_page.mission_tuple[index]
					
					if CARD_IMG_DICT.has_key(mob_vnum):
						self.mission_page.waitArray[row][col].LoadImage( CARD_IMG_DICT[mob_vnum] )
						self.mission_page.waitArray[row][col].SetScale( 0.75, 0.75 )
						self.mission_page.waitVnumDict[mob_vnum] = (row,col)
				else:
					self.mission_page.waitArray[row][col].LoadImage( CARD_IMG_DICT[0] )
					self.mission_page.waitArray[row][col].SetScale( 0.75, 0.75 )
					
		
	## 진행중, 보상단계
	def __SetMissionProceeding(self):
		if not self.mission_page.mission_state in [MISSION_STATE_PROCEEDING, MISSION_STATE_REWARD]:
			return
				
		## 화면 초기화
		self.__MissionPageClear()
		
		if not self.mission_page.mission_data:
			print "if not self.mission_page.mission_data"
			return
		
		cur_stage = self.mission_page.mission_data[MISSION_INDEX_STAGE]
		if 0 == cur_stage:
			return
			
		## 미션 받기 버튼
		if self.mission_page.recive_mission_button:
			self.mission_page.recive_mission_button.DisableFlash()
			
		## 상단 TEXT
		if self.mission_page.alter_text:
			self.mission_page.alter_text.SetText(localeInfo.MC_ALTER_TEXT % (cur_stage))
		
		#####  wait 화면
		self.mission_page.mission_tuple = playerm2g2.GetMissionVec( cur_stage )
		data_count = len( self.mission_page.mission_tuple )
		
		if 0 == data_count or data_count > WAIT_ARRAY_HEIGHT*WAIT_ARRAY_WIDTH:
			return
		
		## (mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = data
		for row in xrange(0, WAIT_ARRAY_HEIGHT):
			for col in xrange(0, WAIT_ARRAY_WIDTH):
				index = row * WAIT_ARRAY_WIDTH + col
				if index < data_count:
					(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = self.mission_page.mission_tuple[index]
					
					if CARD_IMG_DICT.has_key(mob_vnum):
						if mob_vnum in self.mission_page.mission_data[MISSION_INDEX_MOB_VNUM]:
							self.mission_page.waitArray[row][col].LoadImage( CARD_IMG_DICT[0] )
							self.mission_page.waitArray[row][col].SetScale( 0.75, 0.75 )
						else:
							self.mission_page.waitArray[row][col].LoadImage( CARD_IMG_DICT[mob_vnum] )
							self.mission_page.waitArray[row][col].SetScale( 0.75, 0.75 )
							self.mission_page.waitVnumDict[mob_vnum] = (row,col)
				else:
					self.mission_page.waitArray[row][col].LoadImage( CARD_IMG_DICT[0] )
					self.mission_page.waitArray[row][col].SetScale( 0.75, 0.75 )
					
		if self.mission_page.wait_card_alpha:
			self.mission_page.wait_card_alpha.Show()
			
		
		#####  선택된 화면
		for index in xrange(SELECTED_ARRAY_WIDTH):
			mob_vnum = self.mission_page.mission_data[MISSION_INDEX_MOB_VNUM][index]
			## 초상화
			self.mission_page.selectedArray[index].LoadImage( CARD_IMG_DICT[mob_vnum] )
			## 미션 클리어
			if self.mission_page.mission_data[MISSION_INDEX_MOB_CLEAR][index]:
				self.mission_page.MissionClearImgArray[index].Show()
			else:
				self.mission_page.MissionClearImgArray[index].Hide()
			## 이름
			mob_name = nonplayer.GetMonsterName(mob_vnum)
			self.mission_page.seletedMobNameArray[index] = mob_name
			## 출현지역
			area_text=""
			area_indexs = playerm2g2.GetMobEmergenceAreaIndex(mob_vnum)
			if area_indexs:
				for map_index in area_indexs:
					if 0 == map_index:
						continue
					if localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX.has_key(map_index):
						area_text += localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX[map_index]
						area_text += "\\n"
			self.mission_page.setectedAreaTextArray[index] = area_text
			
		
		## 보상받기 버튼 깜박임
		if all( self.mission_page.mission_data[MISSION_INDEX_MOB_CLEAR] ):
			self.mission_page.reward_card_button.EnableFlash()
			

	def __ShowMissionPage(self):
		
		IsLoad = playerm2g2.IsMissionDataLoad()
		
		if not IsLoad:
			self.__MissionPageClear()
			m2netm2g.SendMissionMessage( m2netm2g.REQUEST_MISSION )
			return
	
	def __MissionPageClear(self):
		## 미션 받기 버튼
		if self.mission_page.recive_mission_button:
			self.mission_page.recive_mission_button.EnableFlash()
			
		## 보상 받기 깜박임
		if self.mission_page.reward_card_button:
			self.mission_page.reward_card_button.DisableFlash()
		
		## 선택 위치 vnum dict clear
		self.mission_page.waitVnumDict.clear()
		
		## 선택 위치 미션 clear
		self.__SelectCellClear()
		## 대기 위치 미션 clear
		self.__WaitCellClear()
		
		## Alter Text
		if self.mission_page.alter_text:
			self.mission_page.alter_text.SetText("")
		
	def __SelectCellClear(self):
		
		for col in xrange(0,SELECTED_ARRAY_WIDTH):
			# 초상화
			self.mission_page.selectedArray[col].LoadImage( CARD_IMG_DICT[0] )
			## 미션 클리어
			self.mission_page.MissionClearImgArray[col].Hide()
			# 이름
			self.mission_page.seletedMobNameArray[col] = None
			# 출현지역 Text
			self.mission_page.setectedAreaTextArray[col] = None
			
	def __WaitCellClear(self):
	
		if self.mission_page.wait_card_alpha:
			self.mission_page.wait_card_alpha.Hide()
		
		for row in xrange(0, WAIT_ARRAY_HEIGHT):
			for col in xrange(0, WAIT_ARRAY_WIDTH):
				self.mission_page.waitArray[row][col].LoadImage( CARD_IMG_DICT[0] )
				self.mission_page.waitArray[row][col].SetScale( 0.75, 0.75 )
				
	# 출현지역 over in
	def __EmergenceAreaOverIn(self, type, index):

		if index >= len(self.mission_page.setectedAreaTextArray):
			return
			
		area_text = self.mission_page.setectedAreaTextArray[index]
		if not area_text:
			return
		
		self.OverInToolTipButton( area_text )
	
	# 출현지역 over out
	def __EmergenceAreaOverOut(self, type, index):
		self.OverOutToolTipButton()
		
	## 초상화 over in
	def __SelectedImgOverIn(self, type, index):
		
		if index >= len(self.mission_page.seletedMobNameArray):
			return
			
		name = self.mission_page.seletedMobNameArray[index]
		if not name:
			return
			
		self.OverInToolTipButton( name )
		
	## 초상화 over out
	def __SelectedImgOverOut(self, type, index):
		self.OverOutToolTipButton()
		
		
	#미션받기 버튼 On Click Event
	def __OnClickReciveMissionButton(self):
		if self.mission_page.lock:
			return
			
		if not self.mission_page.mission_data:
			return
			
		if MISSION_STATE_WAIT != self.mission_page.mission_state:
			return
			
		m2netm2g.SendMissionMessage( m2netm2g.RECIVE_MISSION )
		
	#카드배치 버튼 On Click Event(셔플)
	def __OnClickShuffleCardButton(self):
		if self.mission_page.lock:
			return
			
		if self.question:
			self.question.Close()
			
		question = uiCommon.ExQuestionDialog("TOP_MOST")
		question.SetText(localeInfo.MC_CARD_SHUFFLE)
		question.SetAcceptEvent( ui.__mem_func__(self.__ShuffleAccept) )
		question.SetCancelEvent( ui.__mem_func__(self.__CloseQuestionDialog) )
		question.Open()
		self.question = question
		
				
	def __ShuffleAccept(self):
	
		self.__CloseQuestionDialog()
		
		if not self.mission_page.mission_data:
			return

		# 진행중에만 가능하다			
		if not self.mission_page.mission_state in [MISSION_STATE_PROCEEDING, MISSION_STATE_REWARD]:
			self.MonsterCardMissionFail(FAILED_MSSION_COMMON_MSG, 0)
			return
		
		# 한 미션당 1회 셔플 가능
		# 기획자의 요청으로 셔플 제한 없애다.
		#if self.mission_page.mission_data[MISSION_INDEX_SHUFFLE_COUNT] >= SHUFFLE_MAX:
		#	self.MonsterCardMissionFail(FAILED_MSSION_COMMON_MSG, 0)
		#	return
			
		m2netm2g.SendMissionMessage( m2netm2g.SHUFFLE_MISSION )
			
	#카드받기 버튼 On Click Event(보상)
	def __OnClickRewardCardButton(self):
		if self.mission_page.lock:
			return
			
		if self.question:
			self.question.Close()
			
		question = uiCommon.ExQuestionDialog("TOP_MOST")
		question.SetText(localeInfo.MC_REWARD_MISSION)
		question.SetAcceptEvent( ui.__mem_func__(self.__RewardAccept) )
		question.SetCancelEvent( ui.__mem_func__(self.__CloseQuestionDialog) )
		question.Open()
		self.question = question
			
			
	def __RewardAccept(self):
		
		self.__CloseQuestionDialog()
		
		if not self.mission_page.mission_data:
			return
			
		if not self.mission_page.mission_state in [MISSION_STATE_REWARD]:
			self.MonsterCardMissionFail(FAILED_MISSION_REWARD_NO_CLEAR, 0)
			return
		
		# 미션을 모두 clear 한 상태
		if not all( self.mission_page.mission_data[MISSION_INDEX_MOB_CLEAR] ):
			self.MonsterCardMissionFail(FAILED_MISSION_REWARD_NO_CLEAR, 0)
			return
			
		m2netm2g.SendMissionMessage( m2netm2g.REWARD_MISSION )
		
	#초기화 버튼 On Click Event	
	def __OnClickMissionInitButton(self):
		if self.mission_page.lock:
			return
			
		if self.question:
			self.question.Close()
			
		question = uiCommon.ExQuestionDialog("TOP_MOST")
		question.SetText(localeInfo.MC_MISSION_INIT)
		question.SetAcceptEvent( ui.__mem_func__(self.__InitAccept) )
		question.SetCancelEvent( ui.__mem_func__(self.__CloseQuestionDialog) )
		question.Open()
		self.question = question
			
	def __InitAccept(self):
	
		self.__CloseQuestionDialog()
		
		if not self.mission_page.mission_data:
			return
			
		cur_stage = self.mission_page.mission_data[MISSION_INDEX_STAGE]
		if cur_stage <= 1 and self.mission_page.mission_state in [MISSION_STATE_NONE, MISSION_STATE_WAIT]:
			self.MonsterCardMissionFail(FAILED_MSSION_COMMON_MSG, 0)
			return
		
		# 미션 초기화 제한시간내 6회모두 사용하고 7회사용하려고 할때 못한다
		# 코드 추가해야함.
		#self.MonsterCardMissionFail(FAILED_MISSION_INIT_ITEM_FALL_SHORT, 3)
		#return
		
		m2netm2g.SendMissionMessage( m2netm2g.INIT_MISSION )
		
	def __OnClickQuestionButton(self):
	
		if not self.mission_page.mission_data:
			return
			
		reset_time = self.mission_page.mission_data[MISSION_INDEX_RESET_TIME]
		
		if 0 == reset_time: 
			return
		
		curTime = app.GetGlobalTimeStamp()
		
		reset_time = max(0, reset_time + 86400 - curTime)
		reset_time_str = localeInfo.SecondToHM(reset_time)
		self.__OpenPopupDialog(localeInfo.MC_TIME % reset_time_str)
		
	## 미션을 받았음(mob_vnum 3개 가져온다)
	def ReciveMission(self):
		## 데이터 갱신
		self.mission_page.mission_data = playerm2g2.GetMonsterCardMissionInfo() 
		if not self.mission_page.mission_data:
			print "if not self.mission_page.mission_data"
			return
		
		## 상태 강제로 변경
		self.mission_page.mission_state = MISSION_STATE_WAIT
		
		## Wait 초기 화면으로 셋팅
		self.__SetMissionWait()
		
		## 미션 받기 버튼
		if self.mission_page.recive_mission_button:
			self.mission_page.recive_mission_button.DisableFlash()

		for index in xrange(SELECTED_ARRAY_WIDTH):
			mob_vnum = self.mission_page.mission_data[MISSION_INDEX_MOB_VNUM][index]
			if not self.mission_page.waitVnumDict.has_key(mob_vnum):
				return
			src_index = self.mission_page.waitVnumDict[mob_vnum]
			self.__InsertMoveCard( (src_index, mob_vnum),(index, mob_vnum) )
		
		self.mission_page.lock = True
		
		## 상태 갱신
		self.__RefreshMissionState()

	def CardMoveStartEvent(self):
				
		if len(self.mission_page.card_move_queue) > 0:
			(src_index, src_vnum) = self.mission_page.card_move_queue[0][0]
			(dst_index, dst_vnum) = self.mission_page.card_move_queue[0][1]
			
			## Wait Image Clear
			wait_image = self.mission_page.waitArray[src_index[0]][src_index[1]]
			wait_image.LoadImage( CARD_IMG_DICT[0] )
			origin_width	= wait_image.GetWidth()
			origin_height	= wait_image.GetHeight()
			wait_image.SetScale( 0.75, 0.75 )
			
			## 이미지 셋팅
			self.mission_page.move_img.LoadImage( CARD_IMG_DICT[dst_vnum] )
			
			## 시작점 셋팅
			(parent_x, parent_y) = self.pageDict["MISSION"].GetGlobalPosition()
			(left,top,width,height) = wait_image.GetRect()
			center_pos_x = left + width/2
			center_pos_y = top + height/2
			result_x = center_pos_x - origin_width/2 - parent_x
			result_y = center_pos_y - origin_height/2 - parent_y
			self.mission_page.move_img.SetPosition( result_x, result_y )
		
			## 도착점 셋팅
			(dstX, dstY) = self.mission_page.selectedArray[dst_index].GetGlobalPosition()
			self.mission_page.move_img.SetMovePosition(dstX, dstY)
				
			## 시작
			self.mission_page.move_img.Show()
			self.mission_page.move_img.MoveStart()
				
	def CardMoveEndEvnet(self):
		
		if len(self.mission_page.card_move_queue) > 0:
			[srcCard, dstCard] = self.mission_page.card_move_queue.popleft()
			(dst_index, dst_vnum) = dstCard
			
			## 초상화
			self.mission_page.selectedArray[dst_index].LoadImage( CARD_IMG_DICT[dst_vnum] )
			## 이름
			mob_name = nonplayer.GetMonsterName(dst_vnum)
			self.mission_page.seletedMobNameArray[dst_index] = mob_name
			## 출현지역
			area_text=""
			area_indexs = playerm2g2.GetMobEmergenceAreaIndex(dst_vnum)
			if area_indexs:
				for map_index in area_indexs:
					if 0 == map_index:
						continue
					if localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX.has_key(map_index):
						area_text += localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX[map_index]
						area_text += "\\n"
			self.mission_page.setectedAreaTextArray[dst_index] = area_text
				
			# move card hide
			self.mission_page.move_img.Hide()
			
			if len(self.mission_page.card_move_queue) == 0:
				self.mission_page.lock = False
				self.mission_page.wait_card_alpha.Show()
		
	def __InsertMoveCard(self, srcCard, dstCard):
		(src_index, src_vnum) = srcCard
		(dst_index, dst_vnum) = dstCard
		
		src_real_index = src_index[0] * WAIT_ARRAY_WIDTH + src_index[1]
		
		if src_real_index >= WAIT_ARRAY_WIDTH * WAIT_ARRAY_HEIGHT:
			return
			
		if not CARD_IMG_DICT.has_key(src_vnum):
			return
			
		if dst_index >= SELECTED_ARRAY_WIDTH:
			return
			
		if not CARD_IMG_DICT.has_key(dst_vnum):
			return
			
		self.mission_page.card_move_queue.append([srcCard,dstCard])
		
	def MonsterCardMissionFail(self, type, data):
		
		if FAILED_MISSION_SHUFFLE_NO_ITEM == type:
			self.__OpenPopupDialog(localeInfo.MC_SHUFFLE_NO_ITEM)
		elif FAILED_MISSION_INIT_ITEM_FALL_SHORT == type:
			self.__OpenPopupDialog( localeInfo.MC_INIT_ITEM_FALL_SHORT % (data) , True)
		elif FAILED_MISSION_REWARD_INVEN_FULL == type:
			self.__OpenPopupDialog(localeInfo.MC_REWARD_FAIL)
		elif FAILED_MISSION_REWARD_NO_CLEAR == type:
			self.__OpenPopupDialog(localeInfo.MC_MISSION_NO_CLEAR)
		elif FAILED_MSSION_COMMON_MSG == type:
			self.__OpenPopupDialog(localeInfo.MC_MISSION_FAIL_MSG)
		elif FAILED_MISSION_MSG_MAX == type:
			return
					
	def MonsterCardIllustrationFail(self, type, data):
	
		if FAILED_COUNT_MAX == type:
			self.__OpenPopupDialog( localeInfo.MC_USE_ITEM_FAIL )
		elif FAILED_POLY_COOLTIME == type:
			self.__OpenPopupDialog(localeInfo.MC_POLY_FAIL)
		elif FAILED_WARP_LIMIT_LEVEL == type:
			self.__OpenPopupDialog(localeInfo.MC_WARP_LIMIT_LEVEL)
		elif FAILED_WARP_TRADE == type:
			self.__OpenPopupDialog(localeInfo.MC_WARP_FAIL)
			
	## 팝업 창
	def __OpenPopupDialog(self, msg, resize_width = False):
	
		if not self.popup:
			self.popup = uiCommon.ExPopupDialog("TOP_MOST")

		self.popup.SetText(msg)
		
		if resize_width:
			w,h = self.popup.GetTextSize()
			self.popup.SetWidth( w + 60 )
			
		self.popup.Open()
		
	## 질문 창
	def __CloseQuestionDialog(self):
		if self.question:
			self.question.Close()
			self.question = None
			
	## 일러스트 페이지 ########################################################
	
	def MonsterCardIllustrationRefresh(self):
		self.__ClearIllustrationButton()
		self.ShowPage()
			
	def ShowSoloPage(self):
		playerm2g2.IllustrationShow( True )
		
		IsFileLoad = playerm2g2.GetIllustrationFileLoad()
		if not IsFileLoad:
			return
		
		dataLoad = playerm2g2.IsIllustrationDataLoad()
		if not dataLoad:
			m2netm2g.SendIllustrationMessage( m2netm2g.REQUEST_ILLUSTRATION )
			return
		
		if 0 == self.illustration_page.solo_page_max:
			self.illustration_page.solo_page_max = playerm2g2.GetIllustrationSoloPageMax()
			## 초기화
			self.__ClearIllustrationPage()
		
		self.__ShowPageButton( self.illustration_page.solo_page_max , self.illustration_page.solo_cur_page )
		
	def ShowPartyPage(self):
		playerm2g2.IllustrationShow( True )
		
		IsFileLoad = playerm2g2.GetIllustrationFileLoad()
		if not IsFileLoad:
			return
			
		dataLoad = playerm2g2.IsIllustrationDataLoad()
		if not dataLoad:
			m2netm2g.SendIllustrationMessage( m2netm2g.REQUEST_ILLUSTRATION )
			return
			
		if 0 == self.illustration_page.party_page_max:
			self.illustration_page.party_page_max = playerm2g2.GetIllustrationPartyPageMax()
			## 초기화
			self.__ClearIllustrationPage()
			
		self.__ShowPageButton( self.illustration_page.party_page_max , self.illustration_page.party_cur_page )
			
	## 페이지 버튼 표시,위치 계산
	## ILLUSTRATION_PAGE_MAX : 한 페이지당 보여질수 있는 숫자 버튼 MAX
	## max_page : 4 -> 1,2,3,4
	## cur_page : 1,2,3,...
	def __ShowPageButton(self, max_page, cur_page):
		if not self.curKey in ["SOLO", "PARTY"]:
			return
			
		if 0 == max_page:
			return
		if cur_page > max_page:
			return
			
		if "SOLO" == self.curKey:
			if max_page > self.illustration_page.solo_page_max:
				return
				
			self.illustration_page.solo_cur_page = cur_page
		elif "PARTY" == self.curKey:
			if max_page > self.illustration_page.party_page_max:
				return
				
			self.illustration_page.party_cur_page = cur_page
		
		total_page_count	= max_page / ILLUSTRATION_PAGE_MAX		# 2 : 0,1,2
		last_page_btn_max	= max_page % ILLUSTRATION_PAGE_MAX		# 4 : 1,2,3,4
		
		cur_page_count	 = (cur_page-1) /  ILLUSTRATION_PAGE_MAX	# 2 : 0,1,2
		down_pos		 = (cur_page % ILLUSTRATION_PAGE_MAX) - 1
		
		btn_count_max = ILLUSTRATION_PAGE_MAX
		if cur_page_count == total_page_count:
			btn_count_max = last_page_btn_max
		
		for button_index in range(ILLUSTRATION_PAGE_MAX):
			self.illustration_page.page_button_list[button_index].Enable()
			self.illustration_page.page_button_list[button_index].SetUp()
			text_number = cur_page_count * ILLUSTRATION_PAGE_MAX + (button_index+1)
			self.illustration_page.page_button_list[button_index].SetText(str(text_number))
			if button_index < btn_count_max:
				self.illustration_page.page_button_list[button_index].Show()
			else:
				self.illustration_page.page_button_list[button_index].Hide()
				
		self.illustration_page.page_button_list[down_pos].Disable()
		self.illustration_page.page_button_list[down_pos].Down()
		
		## 해당 페이지에 맞는 데이터 셋팅
		self.__ShowIllustrationPage( cur_page )
	
	def __ShowIllustrationPage(self, page):
	
		if not self.curKey in ["SOLO", "PARTY"]:
			return
		
		if "SOLO" == self.curKey:
			page_tuple = playerm2g2.GetIllustrationSoloPageData( page )
			if not page_tuple:
				return
		elif "PARTY" == self.curKey:
			page_tuple = playerm2g2.GetIllustrationPartyPageData( page )
			if not page_tuple:
				return
			
		data_count = len( page_tuple )
		if 0 >= data_count or data_count > (ILLUSTRATED_ARRAY_WIDTH * ILLUSTRATED_ARRAY_HEIGHT):
			return
			
		## 버튼
		if self.illustration_page.cur_model_vnum:
			ill_data = playerm2g2.GetIllustrationData( self.illustration_page.cur_model_vnum )
			if ill_data:
				(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data
				
				# 모션
				if self.illustration_page.motion_button:
					if ILLUSTRATION_MOTION_CALSS > cur_class:
						self.illustration_page.motion_button.Disable()
						self.illustration_page.motion_button.Down()
						self.illustration_page.motion_button.SetToolTipWindow( self.illustration_page.motion_button_tooltip2 )
					else:
						self.illustration_page.motion_button.Enable()
						self.illustration_page.motion_button.SetUp()
						self.illustration_page.motion_button.SetToolTipWindow( self.illustration_page.motion_button_tooltip )
				# 변신
				if self.illustration_page.poly_button:
					if ILLUSTRATION_POLY_CLASS > cur_class:
						self.illustration_page.poly_button.Disable()
						self.illustration_page.poly_button.Down()
						self.illustration_page.poly_button.SetToolTipWindow( self.illustration_page.poly_button_tooltip2 )
					else:
						self.illustration_page.poly_button.Enable()
						self.illustration_page.poly_button.SetUp()
						self.illustration_page.poly_button.SetToolTipWindow( self.illustration_page.poly_button_tooltip )
				# 이동
				if self.illustration_page.warp_button:
					if ILLUSTRATION_WARP_CLASS > cur_class:
						self.illustration_page.warp_button.Disable()
						self.illustration_page.warp_button.Down()
						self.illustration_page.warp_button.SetToolTipWindow( self.illustration_page.warp_button_tooltip2 )
					else:
						self.illustration_page.warp_button.Enable()
						self.illustration_page.warp_button.SetUp()
						self.illustration_page.warp_button.SetToolTipWindow( self.illustration_page.warp_button_tooltip )
		
		## 초상화
		for row in xrange(0, ILLUSTRATED_ARRAY_HEIGHT):
			for col in xrange(0, ILLUSTRATED_ARRAY_WIDTH):
				index = row * ILLUSTRATED_ARRAY_WIDTH + col
				
				if index < data_count:
					(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = page_tuple[index]
					
					## Data
					self.illustration_page.CardData[row][col] = page_tuple[index]
					
					if CARD_IMG_DICT.has_key(mob_vnum):
						ill_data = playerm2g2.GetIllustrationData(mob_vnum)
						
						accumulation_count = 0
						cur_count = 0
						cur_class = 0
						cooltime0 = 0
						cooltime1 = 0
						
						if ill_data:
							(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data

						## 초상화
						self.illustration_page.CardImageArray[row][col].LoadImage( CARD_IMG_DICT[mob_vnum] )
						self.illustration_page.CardImageArray[row][col].Show()
					
						## 초상화 알파
						if cur_class > 0:
							self.illustration_page.CardImageAlpha[row][col].Hide()
						else:
							self.illustration_page.CardImageAlpha[row][col].Show()
						
						## 초상화 라인
						if self.illustration_page.cur_model_vnum == mob_vnum:
							self.illustration_page.CardSelectImage[row][col].Show()
						else:
							self.illustration_page.CardSelectImage[row][col].Hide()
						
						## 에너지바 bg 생성
						self.illustration_page.CardEnergyBGArray[row][col].Show()
						
						## 에너지바 img 생성
						count_max = CLASS_COUNT_MAX[cur_class]
						self.illustration_page.CardEnergyImageArray[row][col].SetPercentage( cur_count, count_max )
						self.illustration_page.CardEnergyImageArray[row][col].Show()
						
						## 초상화 깜박임
						if count_max <= cur_count:
							self.illustration_page.flushArray[row][col].ResetFrame()
							self.illustration_page.flushArray[row][col].Show()
						else:
							self.illustration_page.flushArray[row][col].Hide()
						
						## 등급(star) 생성
						for cnt in xrange(0, STAR_COUNT):
							if cnt < cur_class:
								self.illustration_page.CardStarOnArray[row][col][cnt].Show()
								self.illustration_page.CardStarOffArray[row][col][cnt].Hide()
							else:
								self.illustration_page.CardStarOnArray[row][col][cnt].Hide()
								self.illustration_page.CardStarOffArray[row][col][cnt].Show()
						
						# 이름
						mob_name = nonplayer.GetMonsterName(mob_vnum)
						self.illustration_page.CardMobNameArray[row][col] = mob_name
						# 출현지역
						self.illustration_page.CardAreaImageArray[row][col].Show()
						area_text=""
						area_indexs = playerm2g2.GetMobEmergenceAreaIndex(mob_vnum)
						if area_indexs:
							for map_index in area_indexs:
								if 0 == map_index:
									continue
								if localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX.has_key(map_index):
									area_text += localeInfo.MINIMAP_ZONE_NAME_DICT_BY_IDX[map_index]
									area_text += "\\n"
						self.illustration_page.CardAreaTextArray[row][col] = area_text
						
					## 그려야 하지만 dict 에 없다.
					else:
						print "이러면 안돼~~~~~ : ", mob_vnum
				## 그리면 안된다.
				else:
					## Data
					self.illustration_page.CardData[row][col] = None
					
					## 초상화
					self.illustration_page.CardImageArray[row][col].LoadImage( CARD_IMG_DICT[0] )
					self.illustration_page.CardImageArray[row][col].Show()
				
					## 초상화 알파
					self.illustration_page.CardImageAlpha[row][col].Show()
					
					## 초상화 라인
					self.illustration_page.CardSelectImage[row][col].Hide()
							
					## 초상화 깜박임
					self.illustration_page.flushArray[row][col].Hide()
			
					## 에너지바 bg 생성
					self.illustration_page.CardEnergyBGArray[row][col].Hide()
					
					## 에너지바 img 생성
					self.illustration_page.CardEnergyImageArray[row][col].Hide()
				
					## 등급(star) 생성
					for cnt in xrange(0, STAR_COUNT):
						self.illustration_page.CardStarOnArray[row][col][cnt].Hide()
						self.illustration_page.CardStarOffArray[row][col][cnt].Hide()
						
					# 이름
					self.illustration_page.CardMobNameArray[row][col] = ""
						
					#출현지역
					self.illustration_page.CardAreaImageArray[row][col].Hide()
					self.illustration_page.CardAreaTextArray[row][col] = ""
					
					
	def __ClearIllustrationButton(self):
		# 모션
		if self.illustration_page.motion_button:
			self.illustration_page.motion_button.Disable()
			self.illustration_page.motion_button.Down()
			self.illustration_page.motion_button_tooltip.Hide()
			self.illustration_page.motion_button_tooltip2.Hide()
			self.illustration_page.motion_button.SetToolTipWindow( self.illustration_page.motion_button_tooltip2 )
		# 변신
		if self.illustration_page.poly_button:
			self.illustration_page.poly_button.Disable()
			self.illustration_page.poly_button.Down()
			self.illustration_page.poly_button_tooltip.Hide()
			self.illustration_page.poly_button_tooltip2.Hide()
			self.illustration_page.poly_button.SetToolTipWindow( self.illustration_page.poly_button_tooltip2 )
		# 이동
		if self.illustration_page.warp_button:
			self.illustration_page.warp_button.Disable()
			self.illustration_page.warp_button.Down()
			self.illustration_page.warp_button_tooltip.Hide()
			self.illustration_page.warp_button_tooltip2.Hide()
			self.illustration_page.warp_button.SetToolTipWindow( self.illustration_page.warp_button_tooltip2 )
		# 소환
		if self.illustration_page.summon_button:
			self.illustration_page.summon_button.Disable()
			self.illustration_page.summon_button.Down()
			
	## 초기값으로 셋팅
	def __ClearIllustrationPage(self):
	
		## 모델뷰 이름
		if self.illustration_page.mv_name_text:
			self.illustration_page.mv_name_text.SetText("")
		## 누적 등록 횟수
		if self.illustration_page.mv_count_text:
			self.illustration_page.mv_count_text.SetText("")
		
		## 버튼
		self.__ClearIllustrationButton()

		## 초상화
		for row in xrange(0, ILLUSTRATED_ARRAY_HEIGHT):
			for col in xrange(0, ILLUSTRATED_ARRAY_WIDTH):
				## Data
				self.illustration_page.CardData[row][col] = None
				
				## 초상화
				self.illustration_page.CardImageArray[row][col].LoadImage( CARD_IMG_DICT[0] )
				self.illustration_page.CardImageArray[row][col].Show()
				## 초상화 라인
				self.illustration_page.CardSelectImage[row][col].Hide()
				## 초상화 알파
				self.illustration_page.CardImageAlpha[row][col].Show()
				## 깜박임
				self.illustration_page.flushArray[row][col].Hide()
				## 에너지바 bg 생성
				self.illustration_page.CardEnergyBGArray[row][col].Hide()
				
				## 에너지바 img 생성
				self.illustration_page.CardEnergyImageArray[row][col].Hide()
				
				## 등급(star) 생성
				for cnt in xrange(0, STAR_COUNT):
					self.illustration_page.CardStarOnArray[row][col][cnt].Hide()
					self.illustration_page.CardStarOffArray[row][col][cnt].Hide()
				
				# 이름	
				self.illustration_page.CardMobNameArray[row][col] = ""
				
				#출현지역
				self.illustration_page.CardAreaImageArray[row][col].Hide()
				self.illustration_page.CardAreaTextArray[row][col] = ""
	
	
	## 초상화, 초상화 알파 클릭
	def __CardImgClick(self, type, row, col):
			
		data = self.illustration_page.CardData[row][col]
		if not data:
			return
			
		(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = data
		if mob_vnum == self.illustration_page.cur_model_vnum:
			return
			
		accumulation_count = 0
		cur_count = 0
		cur_class = 0
		cooltime0 = 0
		cooltime1 = 0
		
		ill_data = playerm2g2.GetIllustrationData(mob_vnum)
		if ill_data:
			(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data
			
		if self.illustration_page.mv_count_text:
			self.illustration_page.mv_count_text.SetText( localeInfo.MC_ACCUMULATION_COUNT % (accumulation_count) )
			
		if self.illustration_page.mv_name_text:
			mob_name = nonplayer.GetMonsterName(mob_vnum)
			self.illustration_page.mv_name_text.SetText( mob_name )
			
		## 선택한 mob vnum 저장
		self.illustration_page.cur_model_vnum		= mob_vnum
		self.illustration_page.cur_data				= data
		self.illustration_page.cur_model_rotation	= 0.0
		
		if ILLUSTRATION_MODEL_RENDER <= cur_class:
			playerm2g2.IllustrationSelectModel( mob_vnum )
		else:
			playerm2g2.IllustrationSelectModel( 0 )
		
		## 초상화 라인 그리기
		for _row in xrange(0, ILLUSTRATED_ARRAY_HEIGHT):
			for _col in xrange(0, ILLUSTRATED_ARRAY_WIDTH):
				self.illustration_page.CardSelectImage[_row][_col].Hide()
		self.illustration_page.CardSelectImage[row][col].Show()
		
		## 버튼
		if self.illustration_page.mv_reset_button:
			self.illustration_page.mv_reset_button.Show()
		if self.illustration_page.left_rotation_button:
			self.illustration_page.left_rotation_button.Show()
		if self.illustration_page.right_rotation_button:
			self.illustration_page.right_rotation_button.Show()
		if self.illustration_page.zoomin_button:
			self.illustration_page.zoomin_button.Show()
		if self.illustration_page.zoomout_button:
			self.illustration_page.zoomout_button.Show()
		if self.illustration_page.mv_up_button:
			self.illustration_page.mv_up_button.Show()
		if self.illustration_page.mv_down_button:
			self.illustration_page.mv_down_button.Show()	
			
		# 모션
		if self.illustration_page.motion_button:	
			
			if ILLUSTRATION_MOTION_CALSS > cur_class:
				self.illustration_page.motion_button.Disable()
				self.illustration_page.motion_button.Down()
				self.illustration_page.motion_button.SetToolTipWindow( self.illustration_page.motion_button_tooltip2 )
			else:
				self.illustration_page.motion_button.Enable()
				self.illustration_page.motion_button.SetUp()
				self.illustration_page.motion_button.SetToolTipWindow( self.illustration_page.motion_button_tooltip )
				
		# 변신
		if self.illustration_page.poly_button:	
			
			if ILLUSTRATION_POLY_CLASS > cur_class:
				self.illustration_page.poly_button.Disable()
				self.illustration_page.poly_button.Down()
				self.illustration_page.poly_button.SetToolTipWindow( self.illustration_page.poly_button_tooltip2 )
			else:
				self.illustration_page.poly_button.Enable()
				self.illustration_page.poly_button.SetUp()
				self.illustration_page.poly_button.SetToolTipWindow( self.illustration_page.poly_button_tooltip )
		# 이동
		if self.illustration_page.warp_button:
			
			if ILLUSTRATION_WARP_CLASS > cur_class:
				self.illustration_page.warp_button.Disable()
				self.illustration_page.warp_button.Down()
				self.illustration_page.warp_button.SetToolTipWindow( self.illustration_page.warp_button_tooltip2 )
			else:
				self.illustration_page.warp_button.Enable()
				self.illustration_page.warp_button.SetUp()
				self.illustration_page.warp_button.SetToolTipWindow( self.illustration_page.warp_button_tooltip )
		# 소환
		if self.illustration_page.summon_button:
			if ILLUSTRATION_SUMMON_CLASS > cur_class:
				self.illustration_page.summon_button.Disable()
				self.illustration_page.summon_button.Down()
			else:
				self.illustration_page.summon_button.Enable()
				self.illustration_page.summon_button.SetUp()
		
	# 출현지역 over in
	def __IllustrationEmergenceAreaOverIn(self, type, row, col):
			
		area_text = self.illustration_page.CardAreaTextArray[row][col]
		if not area_text:
			return
		
		self.OverInToolTipButton( area_text )
	
	# 출현지역 over out
	def __IllustrationEmergenceAreaOverOut(self, type, row, col):
		self.OverOutToolTipButton()
		
		
	def __OnClickPageButton(self, index):
		
		if "SOLO" == self.curKey:
			page_max		= self.illustration_page.solo_page_max
			temp_page		= self.illustration_page.solo_cur_page
		elif "PARTY" == self.curKey:
			page_max		= self.illustration_page.party_page_max
			temp_page		= self.illustration_page.party_cur_page
		else:
			return
			
		cur_page_count	= (temp_page-1) /  ILLUSTRATION_PAGE_MAX
		cur_page		= cur_page_count * ILLUSTRATION_PAGE_MAX + (index+1)
		self.__ShowPageButton( page_max, cur_page )
		
		
	def __OnClickFirstPrevPageButton(self):
		if "SOLO" == self.curKey:
			page_max		= self.illustration_page.solo_page_max
			temp_page		= self.illustration_page.solo_cur_page
		elif "PARTY" == self.curKey:
			page_max		= self.illustration_page.party_page_max
			temp_page		= self.illustration_page.party_cur_page
		else:
			return
			
		temp_page_count = temp_page - ILLUSTRATION_PAGE_MAX
		temp_page_count = max( [1, temp_page_count] )
		cur_page_count	= (temp_page_count-1) /  ILLUSTRATION_PAGE_MAX
		cur_page		= cur_page_count * ILLUSTRATION_PAGE_MAX + 1
		self.__ShowPageButton( page_max, cur_page )
		
	def __OnClickPrevPageButton(self):
		if "SOLO" == self.curKey:
			page_max		= self.illustration_page.solo_page_max
			temp_page		= self.illustration_page.solo_cur_page
		elif "PARTY" == self.curKey:
			page_max		= self.illustration_page.party_page_max
			temp_page		= self.illustration_page.party_cur_page
		else:
			return
			
		cur_page = max( [1, temp_page - 1] )
		self.__ShowPageButton( page_max, cur_page )
		
	def __OnClickNextPageButton(self):
		if "SOLO" == self.curKey:
			page_max		= self.illustration_page.solo_page_max
			temp_page		= self.illustration_page.solo_cur_page
		elif "PARTY" == self.curKey:
			page_max		= self.illustration_page.party_page_max
			temp_page		= self.illustration_page.party_cur_page
		else:
			return
			
		cur_page = min( [page_max, temp_page + 1] )
		self.__ShowPageButton( page_max, cur_page )
		
	def __OnClickLastNextPageButton(self):
		if "SOLO" == self.curKey:
			page_max		= self.illustration_page.solo_page_max
			temp_page		= self.illustration_page.solo_cur_page
		elif "PARTY" == self.curKey:
			page_max		= self.illustration_page.party_page_max
			temp_page		= self.illustration_page.party_cur_page
		else:
			return
			
		temp_page_count = temp_page + ILLUSTRATION_PAGE_MAX
		temp_page_count = min( [page_max, temp_page_count] )
		cur_page_count	= (temp_page_count-1) /  ILLUSTRATION_PAGE_MAX
		cur_page		= cur_page_count * ILLUSTRATION_PAGE_MAX + 1
		
		if cur_page > temp_page:
			self.__ShowPageButton( page_max, cur_page )
		
	## 초상화 over in
	def __IllustrationImgOverIn(self, type, row, col):
		name = self.illustration_page.CardMobNameArray[row][col]
		if not name:
			return
			
		self.OverInToolTipButton( name )
		
	## 초상화 over out
	def __IllustrationImgOverOut(self, type, row, col):
		self.OverOutToolTipButton()
			
	def __OnClickPromotionButton(self):
		
		if self.question:
			self.question.Close()
			
		if not self.illustration_page.cur_data:
			return
			
		(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = self.illustration_page.cur_data
		accumulation_count = 0
		cur_count = 0
		cur_class = 0
		cooltime0 = 0
		cooltime1 = 0
		
		ill_data = playerm2g2.GetIllustrationData(mob_vnum)
		if not ill_data:
			self.__OpenPopupDialog(localeInfo.MC_CARD_FALL_SHORT)
			return
		
		(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data
		count_max = CLASS_COUNT_MAX[cur_class]
		
		if cur_count != count_max:
			self.__OpenPopupDialog(localeInfo.MC_CARD_FALL_SHORT)
			return
		if cur_class == STAR_COUNT and cur_count == count_max:
			self.__OpenPopupDialog(localeInfo.MC_PROMOTION_MAX)
			return
			
		question = uiCommon.ExQuestionDialog("TOP_MOST")
		question.SetText(localeInfo.MC_PROMOTION_QUESTION)
		question.SetAcceptEvent( lambda arg = mob_vnum : self.__PromotionAccept(arg) )
		question.SetCancelEvent( ui.__mem_func__(self.__CloseQuestionDialog) )
		question.Open()
		self.question = question
	
	def __PromotionAccept(self, mob_vnum):
		m2netm2g.SendIllustrationMessage( m2netm2g.MC_PROMOTION , mob_vnum )
		self.__CloseQuestionDialog()
		
	def __OnClickExchangeButton(self):
		if self.question:
			self.question.Close()
			
		if not self.illustration_page.cur_data:
			return
			
		(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = self.illustration_page.cur_data
		accumulation_count = 0
		cur_count = 0
		cur_class = 0
		cooltime0 = 0
		cooltime1 = 0
		
		ill_data = playerm2g2.GetIllustrationData(mob_vnum)
		if not ill_data:
			self.__OpenPopupDialog(localeInfo.MC_CARD_FALL_SHORT)
			return
		
		(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data
		count_max = CLASS_COUNT_MAX[cur_class]
		
		if cur_count < TRADE_COUNT:
			self.__OpenPopupDialog(localeInfo.MC_CARD_FALL_SHORT)
			return
			
		question = uiCommon.ExQuestionDialog("TOP_MOST")
		question.SetText(localeInfo.MC_TRADE_QUESTION % TRADE_COUNT )
		question.SetAcceptEvent( lambda arg = mob_vnum : self.__TradeAccept(arg) )
		question.SetCancelEvent( ui.__mem_func__(self.__CloseQuestionDialog) )
		(w,h) = question.GetTextSize()
		question.SetWidth(w+20)
		question.Open()
		self.question = question
	
	def __TradeAccept(self, mob_vnum):
		m2netm2g.SendIllustrationMessage( m2netm2g.MC_TRADE , mob_vnum )
		self.__CloseQuestionDialog()
		
		
	def __OnClickMotionButton(self):		
		ill_data = playerm2g2.GetIllustrationData( self.illustration_page.cur_model_vnum  )
		if not ill_data:
			return
			
		(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data
		if cur_class < ILLUSTRATION_MOTION_CALSS:
			return
						
		playerm2g2.IllustrationChangeMotion( self.illustration_page.cur_model_vnum )
		
		
	def __OnClickPolyButton(self):
		if self.question:
			self.question.Close()
			
		if not self.illustration_page.cur_data:
			return
			
		(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = self.illustration_page.cur_data
		accumulation_count = 0
		cur_count = 0
		cur_class = 0
		cooltime0 = 0
		cooltime1 = 0
		
		ill_data = playerm2g2.GetIllustrationData(mob_vnum)
		if not ill_data:
			return
		
		(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data
		
		if cur_class < ILLUSTRATION_POLY_CLASS:
			self.__OpenPopupDialog(localeInfo.MC_POLY_FAIL)
			return
			
		curTime = app.GetGlobalTimeStamp()
		cooltime = max(0, cooltime0 - curTime)
		cooltime_str = localeInfo.SecondToHM(cooltime)
		if cooltime:
			self.__OpenPopupDialog( localeInfo.MC_TIME % cooltime_str )
			return
			
		question = uiCommon.ExQuestionDialog("TOP_MOST")
		question.SetText(localeInfo.MC_POLY_QUESTION )
		question.SetAcceptEvent( lambda arg = mob_vnum : self.__PolyAccept(arg) )
		question.SetCancelEvent( ui.__mem_func__(self.__CloseQuestionDialog) )
		question.Open()
		self.question = question
	
	def __PolyAccept(self, mob_vnum):
		m2netm2g.SendIllustrationMessage( m2netm2g.MC_POLY , mob_vnum )
		self.__CloseQuestionDialog()
		
		
	def __OnClickWarpButton(self):
		if self.question:
			self.question.Close()
			
		if not self.illustration_page.cur_data:
			return
			
		(mob_vnum, mob_level, type, mapindex0, mapindex1,mapindex2) = self.illustration_page.cur_data
		accumulation_count = 0
		cur_count = 0
		cur_class = 0
		cooltime0 = 0
		cooltime1 = 0
		
		ill_data = playerm2g2.GetIllustrationData(mob_vnum)
		if not ill_data:
			return
		
		(accumulation_count, cur_count, cur_class, cooltime0, cooltime1) = ill_data
		
		if cur_class < ILLUSTRATION_WARP_CLASS:
			self.__OpenPopupDialog(localeInfo.MC_WARP_FAIL)
			return
			
		curTime = app.GetGlobalTimeStamp()
		cooltime = max(0, cooltime1 - curTime)
		cooltime_str = localeInfo.SecondToHM(cooltime)
		if cooltime:
			self.__OpenPopupDialog( localeInfo.MC_TIME % cooltime_str )
			return
			
		question = uiCommon.ExQuestionDialog("TOP_MOST")
		question.SetText(localeInfo.MC_WARP_QUESTION )
		question.SetAcceptEvent( lambda arg = mob_vnum : self.__WarpAccept(arg) )
		question.SetCancelEvent( ui.__mem_func__(self.__CloseQuestionDialog) )
		question.Open()
		self.question = question
	
	def __WarpAccept(self, mob_vnum):
		m2netm2g.SendIllustrationMessage( m2netm2g.MC_WARP , mob_vnum )
		self.__CloseQuestionDialog()
		
		
	def __OnClickSummonButton(self):
		print "추후 구현 예정"
		
	## 모델 상,하 카메라
	def __ModelUpDownCameraProgress(self):
	
		if self.illustration_page.mv_up_button:
			if self.illustration_page.mv_up_button.IsDown():
				playerm2g2.IllustrationModelUpDown( True )
				
		if self.illustration_page.mv_down_button:
			if self.illustration_page.mv_down_button.IsDown():
				playerm2g2.IllustrationModelUpDown( False )
			
	## 모델 회전
	def __ModelRotationProgress(self):
	
		if self.illustration_page.left_rotation_button:
			if self.illustration_page.left_rotation_button.IsDown():
				self.illustration_page.cur_model_rotation -= 2
				playerm2g2.IllustrationModelRotation( self.illustration_page.cur_model_rotation )
				
		if self.illustration_page.right_rotation_button:
			if self.illustration_page.right_rotation_button.IsDown():
				self.illustration_page.cur_model_rotation += 2
				playerm2g2.IllustrationModelRotation( self.illustration_page.cur_model_rotation )
				
	## 모델 줌 in/out			
	def __ModelZoomProgress(self):
	
		if self.illustration_page.zoomin_button:
			if self.illustration_page.zoomin_button.IsDown():
				playerm2g2.IllustrationModelZoom( True )
				
		if self.illustration_page.zoomout_button:
			if self.illustration_page.zoomout_button.IsDown():
				playerm2g2.IllustrationModelZoom( False )
				
	
	## 모델뷰 초기화
	def __ModelViewReset(self):
		self.illustration_page.cur_model_rotation = 0.0
		playerm2g2.IllustrationModelViewReset()