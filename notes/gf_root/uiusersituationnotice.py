import ui
import uiScriptLocale
import wndMgr
import app
import playerm2g2
import m2netm2g
import uiToolTip
import dbg

BUTTON_COUNT_MAX	= 3			# ��ư�� �ִ� 3������ ����
AUTO_CLOSE_TIME		= 10		# �������ڴ� 10�� �ڿ� ����
REQUEST_TIME		= 10800		# 3�ð��� �ѹ� ��û�Ѵ�

DEFAULT_UI_SIZE_WIDTH	= 111
DEFAULT_UI_SIZE_HEIGHT	= 43

BUTTON_HEIGHT			= 21
TASKBAR_HEIGHT			= 37

DEFAULT_START_X			= 158 - 6

icon_path_dict = \
{
	1	: "d:/ymir work/ui/game/user_alram/icon_payment.sub",
	2	: "d:/ymir work/ui/game/user_alram/icon_promotion.sub",
	3	: "d:/ymir work/ui/game/user_alram/icon_event.sub",
	4	: "d:/ymir work/ui/game/user_alram/icon_sales.sub",
}

class UserSituationNotice(ui.ScriptWindow):
	
	def __init__(self):
		ui.ScriptWindow.__init__(self, "UI")
		
		self.isLoaded				= 0
		self.isShowButton			= False
		self.ShowButtonTime			= 0
		self.gift_box_img			= None
		self.buttonList				= []
		self.iconList				= []
		self.interface				= None
		self.user_situation_data	= []
		self.show_button_index		= []
		self.last_request_time		= 0
		self.toolTip				= None
		
		self.address_dict			= {}
		self.button_text_dict		= {}
		self.is_update				= True
		self.last_data_index		= -1
		
		self.__LoadWindow()
		
	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Destroy()
		
	def Destroy(self):
		self.isLoaded				= 0
		self.isShowButton			= False
		self.ShowButtonTime			= 0
		
		self.gift_box_img			= None
		self.buttonList				= []
		self.iconList				= []			
		self.interface				= None
		self.user_situation_data	= []
		self.show_button_index		= []
		self.last_request_time		= 0
		
		if self.toolTip:
			del self.toolTip
		self.toolTip = None
			
		self.address_dict			= {}
		self.button_text_dict		= {}
		self.is_update				= True
		self.last_data_index		= -1		
		
	def __LoadScript(self, fileName):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, fileName)
		
	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)
		
	def __LoadWindow(self):
	
		if self.isLoaded == 1:
			return
			
		if not playerm2g2.IsUserSituationLoaded():
			return
		
		try:
			self.__LoadScript("UIScript/UserSituationNotice.py")
			
		except:
			import exception
			exception.Abort("UserSituationNotice.LoadWindow.LoadObject")
			
		## object
		try:
			self.__BindObject()
		except:
			import exception
			exception.Abort("UserSituationNotice.LoadWindow.__BindObject")
			
		## event
		try:
			self.__BindEvent()
		except:
			import exception
			exception.Abort("UserSituationNotice.LoadWindow.__BindEvent")
			
		## config �� ������ link address �� ������
		self.address_dict		= playerm2g2.GetUserSituationLinkAddress()
		## config �� ������ loca �� ������
		self.button_text_dict	= playerm2g2.GetUserSituationMinimizationLoca()
		## gf backend �� ���� ������ data �� ������ ��ư���� ����� �ش�.
		self.__LoadUserSituationData()
		## data �� ������ �ð��� �����Ѵ�. REQUEST_TIME ���� gf backend �� data �� ��û�Ѵ�.
		self.last_request_time = app.GetGlobalTimeStamp()
		self.isLoaded = 1
		
	def __BindObject(self):
		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.Hide()
		
		self.gift_box_img = self.GetChild("gift_box_img")
		self.gift_box_img.Hide()
		
	def __BindEvent(self):
		if self.gift_box_img:
			self.gift_box_img.SetOnMouseLeftButtonUpEvent( ui.__mem_func__(self.__ClickGiftBoxButton) )
			
	def Close(self):
		self.Hide()
				
	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)
		self.SetTop()
		
		if self.buttonList:
			if self.gift_box_img:
				self.gift_box_img.ResetFrame()
				self.gift_box_img.Show()
		else:
			if self.gift_box_img:
				self.gift_box_img.Hide()
				
	def __LoadUserSituationData(self):
		self.user_situation_data = playerm2g2.GetUserSituationData()
		
		if not self.user_situation_data:
			return
			
		show_button_count = 0
		for index, data in enumerate(self.user_situation_data):
			if show_button_count >= BUTTON_COUNT_MAX:
				break
				
			(address_index, start_time, end_time, text_index, icon_index, campaign_id, hash) = data
			
			cur_time = app.GetGlobalTimeStamp()
			if start_time > cur_time:
				print "���� �ð��� �ȵƴ� : ", start_time - cur_time
				continue
			if end_time < cur_time:
				print "�ð��� ����ƴ� : ", cur_time - end_time
				continue
			
			if True == self.__CreateButton( index ):
				self.show_button_index.append( index )
				show_button_count = show_button_count + 1
			else:
				# ���н� update �� ���ϰ� �Ѵ�.
				# �����ó� ���� ���ӽ� �������� �����Ͱ� ���´ٸ� update �� �����ϴ�.
				self.is_update = False
				
	def __CreateButton(self, data_index):
	
		try:
			(address_index, start_time, end_time, text_index, icon_index, campaign_id, hash) = self.user_situation_data[data_index]
		except IndexError, e:
			dbg.TraceError("User Situation error - INVALID data index : %s" % e )
			return
	
		if BUTTON_COUNT_MAX <= len(self.buttonList):
			return False
		
		if not self.address_dict.has_key( address_index ):
			dbg.TraceError("User Situation error - INVALID link index : %d" % address_index )
			return False
		if not self.button_text_dict.has_key( text_index ):
			dbg.TraceError("User Situation error - INVALID loca index : %d" % text_index )
			return False
		if not icon_path_dict.has_key( icon_index ):
			dbg.TraceError("User Situation error - INVALID icon index : %d" % icon_index )
			return False		
			
		button_text	= self.button_text_dict[text_index]
		icon_path	= icon_path_dict[icon_index]
		
		button = ui.Button()
		button.SetParent( self )
		button.SetPosition(0, 0)
		button.SetUpVisual( "d:/ymir work/ui/game/user_alram/bg.sub" )
		button.SetOverVisual( "d:/ymir work/ui/game/user_alram/bg.sub" )
		button.SetDownVisual( "d:/ymir work/ui/game/user_alram/bg.sub" )
		button.SetEvent( ui.__mem_func__(self.__ClickButton), data_index )
		button.SetOverEvent( ui.__mem_func__(self.__ButtonOverIn), button_text )
		button.SetOverOutEvent( ui.__mem_func__(self.__ButtonOverOut) )
		if 12 < len(button_text):
			button.SetTextAddPos( button_text[:12] + ".", 8 )
		else:
			button.SetTextAddPos( button_text, 8 )
		button.Hide()
		self.buttonList.append( button )
		
		icon = ui.ImageBox()
		icon.SetParent( button )
		icon.LoadImage( icon_path )
		icon.SetPosition(2, 3)
		icon.Hide()
		self.iconList.append( icon )
		
		return True
		
	def __RefreshButtonPosition(self):
		
		button_len	= len( self.buttonList )
		
		pos_x	= DEFAULT_START_X
		pos_y	= wndMgr.GetScreenHeight() - TASKBAR_HEIGHT - DEFAULT_UI_SIZE_HEIGHT
		ui_x	= DEFAULT_UI_SIZE_WIDTH
		ui_y	= DEFAULT_UI_SIZE_HEIGHT
					
		if True == self.isShowButton:
			pos_y	= pos_y - button_len * BUTTON_HEIGHT
			ui_y	= ui_y + button_len  * BUTTON_HEIGHT
			
			self.SetPosition( pos_x, pos_y )
			self.SetSize( ui_x, ui_y )
								
			button_pos_x = 0
			button_pos_y = DEFAULT_UI_SIZE_HEIGHT
				
			for i, button in enumerate( self.buttonList ):
				button.SetPosition(button_pos_x, button_pos_y + BUTTON_HEIGHT * i)
				
		else:
			self.SetPosition( pos_x, pos_y )
			self.SetSize( ui_x, ui_y )
	
	def __ButtonOverIn(self, text):
		if not self.toolTip:
			return

		arglen = len( text )
		pos_x, pos_y = wndMgr.GetMousePosition()
		
		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(11 * arglen)
		self.toolTip.SetToolTipPosition(pos_x, pos_y)
		self.toolTip.AppendTextLine(text, 0xffffff00)
		self.toolTip.Show()
			
	def __ButtonOverOut(self):
		if self.toolTip:
			self.toolTip.Hide()
			
	def __ShowAllButton(self):
		for button in self.buttonList:
			button.Show()
		for icon in self.iconList:
			icon.Show()
			
	def __HideAllButton(self):
		for button in self.buttonList:
			button.Hide()
		for icon in self.iconList:
			icon.Hide()
					
	def __ClickGiftBoxButton(self):
		
		if True == self.isShowButton:
			self.isShowButton	= False
			self.ShowButtonTime = 0
			self.__RefreshButtonPosition()
			self.__HideAllButton()
		else:
			self.isShowButton	= True
			self.ShowButtonTime = app.GetGlobalTimeStamp()
			self.__RefreshButtonPosition()
			self.__ShowAllButton()
		
	def __ClickButton(self, data_index):
		
		if -1 != self.last_data_index:
			return
			
		try:
			(address_index, start_time, end_time, text_index, icon_index, campaign_id, hash) = self.user_situation_data[data_index]
		except IndexError, e:
			dbg.TraceError("User Situation error - INVALID data index : %s" % e )
			return
			
		if not self.address_dict.has_key( address_index ):
			return
			
		self.last_data_index = data_index
		m2netm2g.RequestUserSituationSuffix()
		
		
	def OnUpdate(self):
		if 0 == self.isLoaded:
			return
			
		self.__RequestUserSituationData()
		
		if not self.buttonList:
			if self.gift_box_img:
				self.gift_box_img.Hide()				
			return
			
		self.__OnUpdateBoxButton()
		self.__OnUpdateButton()
		
	## REQUEST_TIME �ð��� �ѹ��� ���� ��Ȳ �����͸� ��û��
	def __RequestUserSituationData(self):
		 
		cur_time = app.GetGlobalTimeStamp()
		if cur_time > self.last_request_time + REQUEST_TIME:			
			if self.buttonList:
				del self.buttonList[:]
			self.buttonList = []
		
			if self.iconList:
				del self.iconList[:]
			self.iconList = []
		
			self.last_data_index = -1
			self.user_situation_data	= []
			self.show_button_index		= []
		
			m2netm2g.RequestUserSituationNotice()
			self.last_request_time = cur_time
		
	## ���� ���� ��ư�� Ȱ��ȭ �� ���¿����� 10�ʵڿ� �˾Ƽ� ����
	def __OnUpdateBoxButton(self):
	
		if False == self.isShowButton:
			return
			
		if app.GetGlobalTimeStamp() < self.ShowButtonTime + AUTO_CLOSE_TIME:
			return
			
		self.__ClickGiftBoxButton()
		
	## ��ư�� �ð��� üũ
	def __OnUpdateButton(self):
		if False == self.is_update:
			return
			
		if not self.user_situation_data:
			return
			
		isRefresh = False
		cur_time = app.GetGlobalTimeStamp()
		show_button_count = 0
		
		for index, data in enumerate(self.user_situation_data):
			if show_button_count >= BUTTON_COUNT_MAX:
				break;
				
			(address_index, start_time, end_time, text_index, icon_index, campaign_id, hash) = data
			# �������� �ִ� ��ư�̶��
			if index in self.show_button_index:
				# ���� �ð��� üũ
				if end_time < cur_time:
					isRefresh = True
					break
				else:
					show_button_count = show_button_count + 1
			# �Ⱥ������� �ִ� ��ư �̶��
			else:
				# ���۽ð��� ����ð��� �����ϴµ�...
				if start_time < cur_time and end_time > cur_time:
					# ���� show ��Ͽ� ����.
					if not index in self.show_button_index:
						isRefresh = True
						break
						
		if True == isRefresh:
			self.RefreshUserSituation()
			
		
	def RefreshUserSituation(self):
		if 0 == self.isLoaded:
			return
			
		if True == self.isShowButton:
			self.__ClickGiftBoxButton()
			
		if self.buttonList:
			del self.buttonList[:]
		self.buttonList = []
		
		if self.iconList:
			del self.iconList[:]
		self.iconList = []
		
		self.last_data_index = -1
		
		self.user_situation_data	= []
		self.show_button_index		= []
		
		self.is_update = True
		
		# �����͸� �ٽ� �ε��Ѵ�
		self.__LoadUserSituationData()
		# ��ư ��ġ�� �����Ѵ�
		self.__RefreshButtonPosition()
		
		if self.buttonList:
			if self.gift_box_img:
				self.gift_box_img.ResetFrame()
				self.gift_box_img.Show()
		else:
			if self.gift_box_img:
				self.gift_box_img.Hide()
				
	def OpenUserSituationShow(self, data):
		if not self.interface:
			return
		if not self.address_dict:
			return
						
		(address_index, start_time, end_time, text_index, icon_index, campaign_id, hash) = self.user_situation_data[self.last_data_index]
						
		if not self.address_dict.has_key( address_index ):
			self.last_data_index = -1
			return
					
		url = self.address_dict[address_index]
		result_url = url + '/campaign/show/' + str(campaign_id) + '/' + str(data) + '/' + str(hash)
		
		self.interface.CloseWbWindow()
		self.interface.OpenWebWindow( result_url )
		self.last_data_index = -1