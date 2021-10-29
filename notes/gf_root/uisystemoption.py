import dbg
import ui
import snd
import systemSetting
import m2netm2g
import chatm2g
import app
import localeInfo
import constInfo
import chrmgrm2g
import playerm2g2
import musicInfo

import uiSelectMusic
import background
import uiPhaseCurtain

MUSIC_FILENAME_MAX_LEN = 25

blockMode = 0

class OptionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__Load()
		
		if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
			self.curtain = uiPhaseCurtain.PhaseCurtain()
			self.curtain.speed = 0.03
			self.curtain.Hide()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		#print " -------------------------------------- DELETE SYSTEM OPTION DIALOG"

	def __Initialize(self):
		self.tilingMode = 0
		self.titleBar = 0
		self.changeMusicButton = 0
		self.selectMusicFile = 0
		self.ctrlMusicVolume = 0
		self.ctrlSoundVolume = 0
		self.musicListDlg = 0
		self.tilingApplyButton = 0
		self.cameraModeButtonList = []
		self.fogModeButtonList = []
		self.tilingModeButtonList = []
		self.ctrlShadowQuality = 0
		
		if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
			self.nightModeButtonList		= []
			self.snowModeButtonList			= []
			self.snowTextureModeButtonList	= []
			
		if app.ENABLE_FOG_FIX:
			self.fogButtonList	= []
			
		self.IsShow = False
		
	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()
		#print " -------------------------------------- DESTROY SYSTEM OPTION DIALOG"

	def __Load_LoadScript(self, fileName):
		try:
			pyScriptLoader = ui.PythonScriptLoader()
			pyScriptLoader.LoadScriptFile(self, fileName)
		except:
			import exception
			exception.Abort("System.OptionDialog.__Load_LoadScript")

	def __Load_BindObject(self):
		try:
			GetObject = self.GetChild
			self.titleBar = GetObject("titlebar")
			self.selectMusicFile = GetObject("bgm_file")
			self.changeMusicButton = GetObject("bgm_button")
			self.ctrlMusicVolume = GetObject("music_volume_controller")
			self.ctrlSoundVolume = GetObject("sound_volume_controller")			
			self.cameraModeButtonList.append(GetObject("camera_short"))
			self.cameraModeButtonList.append(GetObject("camera_long"))
			
			if app.ENABLE_FOG_FIX:
				self.fogButtonList.append(GetObject("fog_off"))
				self.fogButtonList.append(GetObject("fog_on"))
			else:
				self.fogModeButtonList.append(GetObject("fog_level0"))
				self.fogModeButtonList.append(GetObject("fog_level1"))
				self.fogModeButtonList.append(GetObject("fog_level2"))
				
			self.tilingModeButtonList.append(GetObject("tiling_cpu"))
			self.tilingModeButtonList.append(GetObject("tiling_gpu"))
			self.tilingApplyButton=GetObject("tiling_apply")
			
			if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
				self.nightModeButtonList.append(GetObject("night_mode_off"))
				self.nightModeButtonList.append(GetObject("night_mode_on"))
				self.snowModeButtonList.append(GetObject("snow_mode_off"))
				self.snowModeButtonList.append(GetObject("snow_mode_on"))
				self.snowTextureModeButtonList.append(GetObject("snow_texture_mode_off"))
				self.snowTextureModeButtonList.append(GetObject("snow_texture_mode_on"))
				
			#self.ctrlShadowQuality = GetObject("shadow_bar")
		except:
			import exception
			exception.Abort("OptionDialog.__Load_BindObject")

	def __Load(self):
		self.__Load_LoadScript("uiscript/systemoptiondialog.py")
		self.__Load_BindObject()

		self.SetCenterPosition()
		
		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

		self.ctrlMusicVolume.SetSliderPos(float(systemSetting.GetMusicVolume()))
		self.ctrlMusicVolume.SetEvent(ui.__mem_func__(self.OnChangeMusicVolume))

		self.ctrlSoundVolume.SetSliderPos(float(systemSetting.GetSoundVolume()) / 5.0)
		self.ctrlSoundVolume.SetEvent(ui.__mem_func__(self.OnChangeSoundVolume))

#		self.ctrlShadowQuality.SetSliderPos(float(systemSetting.GetShadowLevel()) / 5.0)
#		self.ctrlShadowQuality.SetEvent(ui.__mem_func__(self.OnChangeShadowQuality))

		self.changeMusicButton.SAFE_SetEvent(self.__OnClickChangeMusicButton)

		self.cameraModeButtonList[0].SAFE_SetEvent(self.__OnClickCameraModeShortButton)
		self.cameraModeButtonList[1].SAFE_SetEvent(self.__OnClickCameraModeLongButton)

		if app.ENABLE_FOG_FIX:
			self.fogButtonList[0].SAFE_SetEvent(self.__OnClickFogModeOffButton)
			self.fogButtonList[1].SAFE_SetEvent(self.__OnClickFogModeOnButton)
		else:
			self.fogModeButtonList[0].SAFE_SetEvent(self.__OnClickFogModeLevel0Button)
			self.fogModeButtonList[1].SAFE_SetEvent(self.__OnClickFogModeLevel1Button)
			self.fogModeButtonList[2].SAFE_SetEvent(self.__OnClickFogModeLevel2Button)

		self.tilingModeButtonList[0].SAFE_SetEvent(self.__OnClickTilingModeCPUButton)
		self.tilingModeButtonList[1].SAFE_SetEvent(self.__OnClickTilingModeGPUButton)

		self.tilingApplyButton.SAFE_SetEvent(self.__OnClickTilingApplyButton)

		self.__SetCurTilingMode()

		self.__ClickRadioButton(self.fogModeButtonList, constInfo.GET_FOG_LEVEL_INDEX())
		self.__ClickRadioButton(self.cameraModeButtonList, constInfo.GET_CAMERA_MAX_DISTANCE_INDEX())

		if app.ENABLE_FOG_FIX:
			self.__ClickRadioButton(self.fogButtonList, background.GetFogMode())

		if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
			self.selectMusicFile.SetText(uiSelectMusic.DEFAULT_THEMA)
		else:
			self.selectMusicFile.SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])
			
		if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:			
			self.nightModeButtonList[0].SAFE_SetEvent(self.__OnClickNightModeOffButton)
			self.nightModeButtonList[1].SAFE_SetEvent(self.__OnClickNightModeOnButton)
			self.__InitNightModeOption()
			
			self.snowModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowModeOffButton)
			self.snowModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowModeOnButton)
			self.__InitSnowModeOption()
			
			self.snowTextureModeButtonList[0].SAFE_SetEvent(self.__OnClickSnowTextureModeOffButton)
			self.snowTextureModeButtonList[1].SAFE_SetEvent(self.__OnClickSnowTextureModeOnButton)		
			self.__InitSnowTextureModeOption()
			
			

	def __OnClickTilingModeCPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_CPU_TILING_3)
		self.__SetTilingMode(0)

	def __OnClickTilingModeGPUButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_1)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_2)
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_GPU_TILING_3)
		self.__SetTilingMode(1)

	def __OnClickTilingApplyButton(self):
		self.__NotifyChatLine(localeInfo.SYSTEM_OPTION_TILING_EXIT)
		if 0==self.tilingMode:
			background.EnableSoftwareTiling(1)
		else:
			background.EnableSoftwareTiling(0)

		m2netm2g.ExitGame()

	def __OnClickChangeMusicButton(self):
		if not self.musicListDlg:
			
			self.musicListDlg=uiSelectMusic.FileListDialog()
			self.musicListDlg.SAFE_SetSelectEvent(self.__OnChangeMusic)

		self.musicListDlg.Open()

		
	def __ClickRadioButton(self, buttonList, buttonIndex):
		try:
			selButton=buttonList[buttonIndex]
		except IndexError:
			return

		for eachButton in buttonList:
			eachButton.SetUp()

		selButton.Down()


	def __SetTilingMode(self, index):
		self.__ClickRadioButton(self.tilingModeButtonList, index)
		self.tilingMode=index

	def __SetCameraMode(self, index):
		constInfo.SET_CAMERA_MAX_DISTANCE_INDEX(index)
		self.__ClickRadioButton(self.cameraModeButtonList, index)

	def __SetFogLevel(self, index):
		constInfo.SET_FOG_LEVEL_INDEX(index)
		self.__ClickRadioButton(self.fogModeButtonList, index)

	def __OnClickCameraModeShortButton(self):
		self.__SetCameraMode(0)

	def __OnClickCameraModeLongButton(self):
		self.__SetCameraMode(1)

	def __OnClickFogModeLevel0Button(self):
		self.__SetFogLevel(0)

	def __OnClickFogModeLevel1Button(self):
		self.__SetFogLevel(1)

	def __OnClickFogModeLevel2Button(self):
		self.__SetFogLevel(2)
		
	if app.ENABLE_FOG_FIX:
		def __OnClickFogModeOnButton(self):
			background.SetFogMode(True)
			self.__ClickRadioButton(self.fogButtonList, 1)
		def __OnClickFogModeOffButton(self):
			background.SetFogMode(False)
			self.__ClickRadioButton(self.fogButtonList, 0)

	def __OnChangeMusic(self, fileName):
		self.selectMusicFile.SetText(fileName[:MUSIC_FILENAME_MAX_LEN])

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==uiSelectMusic.DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()
		
		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __InitNightModeOption(self):
			self.NightModeOn		= systemSetting.GetNightModeOption()
			self.__ClickRadioButton(self.nightModeButtonList, self.NightModeOn)
			background.SetNightModeOption(self.NightModeOn)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __InitSnowModeOption(self):
			self.SnowModeOn	= systemSetting.GetSnowModeOption()
			self.__ClickRadioButton(self.snowModeButtonList, self.SnowModeOn)
			background.SetSnowModeOption(self.SnowModeOn)
	
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __InitSnowTextureModeOption(self):
			self.SnowTextureModeOn	= systemSetting.GetSnowTextureModeOption()
			self.__ClickRadioButton(self.snowTextureModeButtonList, self.SnowTextureModeOn)
			background.SetSnowTextureModeOption(self.SnowTextureModeOn)			
			
				
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __OnClickNightModeOffButton(self):
			self.__ClickRadioButton(self.nightModeButtonList, 0)
			self.__SetNightMode(0)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __OnClickNightModeOnButton(self):
			self.__ClickRadioButton(self.nightModeButtonList, 1)
			self.__SetNightMode(1)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __OnClickSnowModeOffButton(self):
			self.__ClickRadioButton(self.snowModeButtonList, 0)
			self.__SetSnowMode(0)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __OnClickSnowModeOnButton(self):
			self.__ClickRadioButton(self.snowModeButtonList, 1)
			self.__SetSnowMode(1)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __OnClickSnowTextureModeOffButton(self):
			self.__ClickRadioButton(self.snowTextureModeButtonList, 0)
			self.__SetSnowTextureMode(0)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __OnClickSnowTextureModeOnButton(self):
			self.__ClickRadioButton(self.snowTextureModeButtonList, 1)
			self.__SetSnowTextureMode(1)
			
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:	
		def __SetSnowMode(self, index):
			systemSetting.SetSnowModeOption(index)
			background.SetSnowModeOption(index)
			background.EnableSnowMode(index)
	
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:	
		def __SetSnowTextureMode(self, index):
			systemSetting.SetSnowTextureModeOption(index)
			background.SetSnowTextureModeOption(index)
			background.EnableSnowTextureMode()
	
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:	
		def __SetNightMode(self, index):
			systemSetting.SetNightModeOption(index)	
			background.SetNightModeOption(index)
			
			if not background.GetDayMode():
				return
				
			if not background.IsBoomMap():
				return
			
			if 1 == index:
				self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)
			else:
				self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)		
		
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __DayMode_OnCompleteChangeToLight(self):
			if app.ENABLE_12ZI:
				background.ChangeEnvironmentData(background.DAY_MODE_LIGHT)
			else:
				background.ChangeEnvironmentData(0)
			self.curtain.FadeIn()
	
	if app.ENABLE_ENVIRONMENT_EFFECT_OPTION:
		def __DayMode_OnCompleteChangeToDark(self):		
			if app.ENABLE_12ZI:
				background.RegisterEnvironmentData(background.DAY_MODE_DARK, constInfo.ENVIRONMENT_NIGHT)
				background.ChangeEnvironmentData(background.DAY_MODE_DARK)
			else:
				background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
				background.ChangeEnvironmentData(1)
			self.curtain.FadeIn()

	def OnChangeMusicVolume(self):
		pos = self.ctrlMusicVolume.GetSliderPos()
		snd.SetMusicVolume(pos * m2netm2g.GetFieldMusicVolume())
		systemSetting.SetMusicVolume(pos)

	def OnChangeSoundVolume(self):
		pos = self.ctrlSoundVolume.GetSliderPos()
		snd.SetSoundVolumef(pos)
		systemSetting.SetSoundVolumef(pos)

	def OnChangeShadowQuality(self):
		pos = self.ctrlShadowQuality.GetSliderPos()
		systemSetting.SetShadowLevel(int(pos / 0.2))

	def OnCloseInputDialog(self):
		self.inputDialog.Close()
		self.inputDialog = None
		return True

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True
	
	def Show(self):
		ui.ScriptWindow.Show(self)
		self.IsShow = True
	
	def IsShowWindow(self):
		return self.IsShow

	def Close(self):
		self.__SetCurTilingMode()
		self.Hide()
		self.IsShow = False

	def __SetCurTilingMode(self):
		if background.IsSoftwareTiling():
			self.__SetTilingMode(0)
		else:
			self.__SetTilingMode(1)	

	def __NotifyChatLine(self, text):
		chatm2g.AppendChat(chatm2g.CHAT_TYPE_INFO, text)
		
