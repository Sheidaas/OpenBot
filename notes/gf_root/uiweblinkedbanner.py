import ui
import uiScriptLocale
import wndMgr
import app
import m2netm2g
import uiToolTip
import dbg
import uiWeb
import grp

if app.ENABLE_WEB_LINKED_BANNER:
	class WebLinkedBannerWindow(ui.ScriptWindow):

		DEFAULT_BANNER_IMAGE_UP = app.GetLocalePath() + "/ui/web_linked_banner/btn_strame_long_001.tga"
		DEFAULT_BANNER_IMAGE_OVER = app.GetLocalePath() + "/ui/web_linked_banner/btn_strame_long_002.tga"
		DEFAULT_BANNER_IMAGE_DOWN = app.GetLocalePath() + "/ui/web_linked_banner/btn_strame_long_003.tga"
				
		def __init__(self):
			ui.ScriptWindow.__init__(self, "UI")
			
			self.isLoaded	= 0
			self.bannertype = []
			self.bannerList	= []
			self.toolTip	= None
			
			if app.ENABLE_WEB_LINKED_BANNER and app.ENABLE_WEB_LINKED_BANNER_LIMIT_REMOVE:
				self.uiWeb		= None
			
			self.window_horizontal	= 0
			self.window_vertical	= 0
			self.banner_horizontal	= 0
			self.banner_vertical	= 0
			self.startX		= 0
			self.startY		= 0
			
			self.__LoadWindow()
			
			
		def __del__(self):
			ui.ScriptWindow.__del__(self)
			self.Destroy()
			
		def Close(self):
			self.Hide()
			
		def Destroy(self):
			self.isLoaded	= 0
			
			if self.bannerList:
				del self.bannerList[:]
				
			self.bannertype	= []
			self.bannerList	= []
			
			if self.toolTip:
				del self.toolTip
				
			self.toolTip	= None

			if app.ENABLE_WEB_LINKED_BANNER and app.ENABLE_WEB_LINKED_BANNER_LIMIT_REMOVE:
				self.uiWeb		= None
			
			self.window_horizontal	= 0
			self.window_vertical	= 0
			self.banner_horizontal	= 0
			self.banner_vertical	= 0
			self.startX		= 0
			self.startY		= 0

		def __LoadScript(self, fileName):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
			
		def __LoadWindow(self):
		
			if self.isLoaded == 1:
				return
			
			if not m2netm2g.IsUsableWebLinkedBanner():
				return
		
			try:
				self.__LoadScript("UIScript/WebLinkedBannerWindow.py")
				
			except:
				import exception
				exception.Abort("WebLinkedBannerWindow.__LoadWindow.LoadObject")
			
			try:
				self.__LoadWebLinkedBannerData()
			except:
				import exception
				exception.Abort("WebLinkedBannerWindow.__LoadWindow.__LoadWebLinkedBannerData")
			
			## object
			try:
				self.__BindObject()
			except:
				import exception
				exception.Abort("WebLinkedBannerWindow.__LoadWindow.__BindObject")
				
			self.isLoaded = 1
			

		if app.ENABLE_WEB_LINKED_BANNER_LIMIT_REMOVE:
			def BindWebBrowser(self, uiWeb):
				from _weakref import proxy
				self.uiWeb = proxy(uiWeb)
			
		def __BindObject(self):
			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.Hide()
			
		def __LoadWebLinkedBannerData(self):
			self.banner_data = m2netm2g.GetWebLinkedBannerData()

			if not self.banner_data:
				return
				
			(self.window_horizontal, self.window_vertical, self.banner_horizontal, self.banner_vertical, self.startX, self.startY) = m2netm2g.GetWebLinkedBannerPositionInfo()
			
			if self.window_horizontal == 2:
				self.startX += wndMgr.GetScreenWidth()/2
			elif self.window_horizontal == 3:
				self.startX += wndMgr.GetScreenWidth()			
			
			if self.window_vertical == 2:
				self.startY += wndMgr.GetScreenHeight()/2
			elif self.window_vertical == 3:
				self.startY += wndMgr.GetScreenHeight()
			
			
			for index in xrange(len(self.banner_data)):
				self.__CreateBannerButton( index )
				
			self.__RefreshButtonLineUp()

		def __CreateBannerButton(self, banner_index):
			try:
				(type, text, tooltip, default_image_path, over_image_path, url, flash) = self.banner_data[banner_index]
			except:
				dbg.TraceError("__CreateBannerButton banner_data error - INVALID data index : %s" % banner_index )
				return
		
			button = ui.Button()
			button.SetParent( self )
			button.SetPosition(0, 0)
			if default_image_path == "":
				button.SetUpVisual(self.DEFAULT_BANNER_IMAGE_UP)
				button.SetOverVisual(self.DEFAULT_BANNER_IMAGE_OVER)
				button.SetDownVisual(self.DEFAULT_BANNER_IMAGE_DOWN)
			else:
				button.SetUpVisual( default_image_path )
				button.SetOverVisual( over_image_path )
				button.SetDownVisual( default_image_path )
				
			if flash:
				button.EnableFlash()
			
			button.SetAutoSizeText(text)
			button.SetTextColor(0xffffffff)
			button.SetEvent( ui.__mem_func__(self.__ClickButton), banner_index )
			button.SetOverEvent( ui.__mem_func__(self.__ButtonOverIn), tooltip )
			button.SetOverOutEvent( ui.__mem_func__(self.__ButtonOverOut) )
		
			button.Show()
			self.bannertype.append( type )
			self.bannerList.append( button )
			
			return True
			
		def __RefreshButtonLineUp(self):
			banner_len	= len( self.bannerList )
							
			button_pos_x = self.startX
			button_pos_y = self.startY
			banner_total_height = 0

			for i, button in enumerate( self.bannerList ):
				if self.bannertype[i] != 0:
					if self.bannertype[i] == 1:
						if app.GetLoginType() != app.LOGIN_TYPE_NONE:
							continue
					if self.bannertype[i] == 2:
						if not app.ENABLE_STEAM or app.GetLoginType() != app.LOGIN_TYPE_STEAM:
							continue
				
				banner_total_height += button.GetHeight() + 5
				
			if self.banner_vertical == 2:
				button_pos_y = button_pos_y - banner_total_height/2
			elif self.banner_vertical == 3:
				button_pos_y = button_pos_y - banner_total_height
			
			for i, button in enumerate( self.bannerList ):
				button.Hide()
				if self.bannertype[i] != 0:
					if self.bannertype[i] == 1:
						if app.GetLoginType() != app.LOGIN_TYPE_NONE:
							continue
					if self.bannertype[i] == 2:
						if not app.ENABLE_STEAM or app.GetLoginType() != app.LOGIN_TYPE_STEAM:
							continue
				
				plus_x = 0	
				if self.banner_horizontal == 2:
					plus_x = -button.GetWidth()/2
				elif self.banner_horizontal == 3:
					plus_x = -button.GetWidth()
				
				button.SetPosition(button_pos_x + plus_x, button_pos_y)
				button_pos_y += button.GetHeight() + 5
				button.Show()
		
		def Open(self):
			if self.isLoaded != 1:
				return
				
			self.Show()
						
		def __ClickButton(self, data_index):
			if self.isLoaded != 1:
				return
				
				
			if app.ENABLE_WEB_LINKED_BANNER_LIMIT_REMOVE:
				if not self.uiWeb:
					return
				
			try:
				(type, text, tooltip, default_image_path, over_image_path, url, flash) = self.banner_data[data_index]
			except IndexError, e:
				dbg.TraceError("__ClickButton banner_data error - INVALID data index : %s" % e )
				return
				
			if app.ENABLE_STEAM and app.GetLoginType() == app.LOGIN_TYPE_STEAM:
				if app.ShowOverlayWebPage(url):
					return

			if app.ENABLE_WEB_LINKED_BANNER_LIMIT_REMOVE:
				self.uiWeb.SetTitle(text)
				self.uiWeb.Open(url)
			
		def __ButtonOverIn(self, text):
			if self.isLoaded != 1:
				return
				
			if not self.toolTip:
				return

			arglen = len( text )
			if arglen == 0:
				return
			
			pos_x, pos_y = wndMgr.GetMousePosition()
			
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(0)
			self.toolTip.SetToolTipPosition(pos_x, pos_y)
			self.toolTip.AutoAppendTextLine(text, 0xffffff00)

			self.toolTip.Show()
				
		def __ButtonOverOut(self):
			if self.isLoaded != 1:
				return
				
			if self.toolTip:
				self.toolTip.Hide()