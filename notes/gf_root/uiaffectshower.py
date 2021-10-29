import ui
import localeInfo
import chr
import item
import app
import skill
import playerm2g2
import uiToolTip
import math

if app.ENABLE_SET_ITEM:
	import uiToolTip
	
# WEDDING
class LovePointImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/LovePoint/"
	FILE_DICT = {
		0 : FILE_PATH + "01.dds",
		1 : FILE_PATH + "02.dds",
		2 : FILE_PATH + "02.dds",
		3 : FILE_PATH + "03.dds",
		4 : FILE_PATH + "04.dds",
		5 : FILE_PATH + "05.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()

	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()

	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)

		if 0 == self.lovePoint:
			loveGrade = 0
		else:
			loveGrade = self.lovePoint / 25 + 1
		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH+"00.dds")

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("LovePointImage.SetLoverInfo(lovePoint=%d) - LoadError %s" % (self.lovePoint, fileName))

		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.loverName)
		self.toolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_WEDDING


class HorseImage(ui.ExpandedImageBox):

	FILE_PATH = "d:/ymir work/ui/pattern/HorseState/"

	FILE_DICT = {
		00 : FILE_PATH+"00.dds",
		01 : FILE_PATH+"00.dds",
		02 : FILE_PATH+"00.dds",
		03 : FILE_PATH+"00.dds",
		10 : FILE_PATH+"10.dds",
		11 : FILE_PATH+"11.dds",
		12 : FILE_PATH+"12.dds",
		13 : FILE_PATH+"13.dds",
		20 : FILE_PATH+"20.dds",
		21 : FILE_PATH+"21.dds",
		22 : FILE_PATH+"22.dds",
		23 : FILE_PATH+"23.dds",
		30 : FILE_PATH+"30.dds",
		31 : FILE_PATH+"31.dds",
		32 : FILE_PATH+"32.dds",
		33 : FILE_PATH+"33.dds",
	}

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		#self.textLineList = []
		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()
		
	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def __GetHorseGrade(self, level):
		if 0 == level:
			return 0

		return (level-1)/10 + 1

	def SetState(self, level, health, battery):
		#self.textLineList=[]
		self.toolTip.ClearToolTip()

		if level>0:

			try:
				grade = self.__GetHorseGrade(level)
				self.__AppendText(localeInfo.LEVEL_LIST[grade])
			except IndexError:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery)
				return

			try:
				healthName=localeInfo.HEALTH_LIST[health]
				if len(healthName)>0:
					self.__AppendText(healthName)
			except IndexError:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - Unknown Index" % (level, health, battery)
				return

			if health>0:
				if battery==0:
					self.__AppendText(localeInfo.NEEFD_REST)

			try:
				fileName=self.FILE_DICT[health*10+battery]
			except KeyError:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - KeyError" % (level, health, battery)

			try:
				self.LoadImage(fileName)
			except:
				print "HorseImage.SetState(level=%d, health=%d, battery=%d) - LoadError %s" % (level, health, battery, fileName)

		self.SetScale(0.7, 0.7)

	def __AppendText(self, text):

		self.toolTip.AppendTextLine(text)
		self.toolTip.ResizeToolTip()

		#x=self.GetWidth()/2
		#textLine = ui.TextLine()
		#textLine.SetParent(self)
		#textLine.SetSize(0, 0)
		#textLine.SetOutline()
		#textLine.Hide()
		#textLine.SetPosition(x, 40+len(self.textLineList)*16)
		#textLine.SetText(text)
		#self.textLineList.append(textLine)

	def OnMouseOverIn(self):
		#for textLine in self.textLineList:
		#	textLine.Show()

		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		#for textLine in self.textLineList:
		#	textLine.Hide()

		self.toolTip.HideToolTip()


# AUTO_POTION
class AutoPotionImage(ui.ExpandedImageBox):

	FILE_PATH_HP = "d:/ymir work/ui/pattern/auto_hpgauge/"
	FILE_PATH_SP = "d:/ymir work/ui/pattern/auto_spgauge/"

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.loverName = ""
		self.lovePoint = 0
		self.potionType = playerm2g2.AUTO_POTION_TYPE_HP
		self.filePath = ""

		self.toolTip = uiToolTip.ToolTip(100)
		self.toolTip.HideToolTip()

	def __del__(self):
		ui.ExpandedImageBox.__del__(self)

	def SetPotionType(self, type):
		self.potionType = type
		
		if playerm2g2.AUTO_POTION_TYPE_HP == type:
			self.filePath = self.FILE_PATH_HP
		elif playerm2g2.AUTO_POTION_TYPE_SP == type:
			self.filePath = self.FILE_PATH_SP
			

	def OnUpdateAutoPotionImage(self):
		self.__Refresh()

	def __Refresh(self):
		print "__Refresh"
	
		isActivated, currentAmount, totalAmount, slotIndex = playerm2g2.GetAutoPotionInfo(self.potionType)
		
		amountPercent = (float(currentAmount) / totalAmount) * 100.0
		grade = math.ceil(amountPercent / 20)
		
		if 5.0 > amountPercent:
			grade = 0
			
		if 80.0 < amountPercent:
			grade = 4
			if 90.0 < amountPercent:
				grade = 5			

		fmt = self.filePath + "%.2d.dds"
		fileName = fmt % grade
		
		print self.potionType, amountPercent, fileName

		try:
			self.LoadImage(fileName)
		except:
			import dbg
			dbg.TraceError("AutoPotionImage.__Refresh(potionType=%d) - LoadError %s" % (self.potionType, fileName))

		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()
		
		if playerm2g2.AUTO_POTION_TYPE_HP == type:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_HP)
		else:
			self.toolTip.SetTitle(localeInfo.TOOLTIP_AUTO_POTION_SP)
			
		self.toolTip.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST	% (amountPercent))
		self.toolTip.ResizeToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
# END_OF_AUTO_POTION

if app.ENABLE_GROWTH_PET_SYSTEM:
	# GROWTH PET IMAGE
	class GrowthPetImage(ui.ExpandedImageBox):

		def __init__(self):
			ui.ExpandedImageBox.__init__(self)
		
			self.toolTipText = None
			self.description = None			

		def __del__(self):
			ui.ExpandedImageBox.__del__(self)

		def SetToolTipText(self, text, x = 0, y = -19):
			
			if not self.toolTipText:
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetSize(0, 0)
				textLine.SetOutline()
				textLine.Hide()
				self.toolTipText = textLine

			self.toolTipText.SetText(text)
			w, h = self.toolTipText.GetTextSize()
			if localeInfo.IsARABIC():
				self.toolTipText.SetPosition(w+20, y)
			else:
				self.toolTipText.SetPosition(max(0, x + self.GetWidth()/2 - w/2), y)
				
		def SetDescription(self, description):
			self.description = description
			
		def OnMouseOverIn(self):
			if self.toolTipText:
				self.toolTipText.Show()

		def OnMouseOverOut(self):
			if self.toolTipText:
				self.toolTipText.Hide()

	# END OF GROWTH PET IMAGE


class AffectImage(ui.ExpandedImageBox):

	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTipText = None
		self.isSkillAffect = TRUE
		self.description = None
		self.endTime = 0
		self.affect = None
		self.isClocked = TRUE

		if app.ENABLE_SET_ITEM:
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()
		if app.ENABLE_LUCKY_EVENT:
			self.multi_affect_dict = {}

	if app.ENABLE_SET_ITEM:
		def __del__(self):
			ui.ExpandedImageBox.__del__(self)
			del self.tooltipItem

	def SetAffect(self, affect):
		self.affect = affect

	def GetAffect(self):
		return self.affect

	if app.ENABLE_SET_ITEM:
		def SetToolTipText(self, text, x = 0, y = -19, adjust_line_height = False, line_height_distance = 20):
			if not self.toolTipText:
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetSize(0, 0)
				textLine.SetOutline()
				textLine.Hide()
				self.toolTipText = textLine

				if adjust_line_height:
					line_height = self.toolTipText.GetLineHeight()
					self.toolTipText.SetLineHeight(line_height + line_height_distance)

			self.toolTipText.SetText(text)
			w, h = self.toolTipText.GetTextSize()
			if localeInfo.IsARABIC():
				self.toolTipText.SetPosition(w+20, y)
			else:
				self.toolTipText.SetPosition(max(0, x + self.GetWidth()/2 - w/2), y)
	else:
		def SetToolTipText(self, text, x = 0, y = -19):

			if not self.toolTipText:
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetSize(0, 0)
				textLine.SetOutline()
				textLine.Hide()
				self.toolTipText = textLine

			self.toolTipText.SetText(text)
			w, h = self.toolTipText.GetTextSize()
			if localeInfo.IsARABIC():
				self.toolTipText.SetPosition(w+20, y)
			else:
				self.toolTipText.SetPosition(max(0, x + self.GetWidth()/2 - w/2), y)

	def SetDescription(self, description):
		self.description = description

	def SetDuration(self, duration):
		self.endTime = 0
		if duration > 0:
			self.endTime = app.GetGlobalTimeStamp() + duration

	def UpdateAutoPotionDescription(self):		
		
		potionType = 0
		if self.affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			potionType = playerm2g2.AUTO_POTION_TYPE_HP
		else:
			potionType = playerm2g2.AUTO_POTION_TYPE_SP	
		
		isActivated, currentAmount, totalAmount, slotIndex = playerm2g2.GetAutoPotionInfo(potionType)
		
		#print "UpdateAutoPotionDescription ", isActivated, currentAmount, totalAmount, slotIndex
		
		amountPercent = 0.0
		
		try:
			amountPercent = (float(currentAmount) / totalAmount) * 100.0		
		except:
			amountPercent = 100.0
		
		self.SetToolTipText(self.description % amountPercent, 0, 40)
		
	def SetClock(self, isClocked):
		self.isClocked = isClocked
		
	def UpdateDescription(self):
		if not self.isClocked:
			self.__UpdateDescription2()
			return
	
		if not self.description:
			return
			
		toolTip = self.description
		if self.endTime > 0:
			leftTime = localeInfo.SecondToDHM(self.endTime - app.GetGlobalTimeStamp())
			toolTip += " (%s : %s)" % (localeInfo.LEFT_TIME, leftTime)
		self.SetToolTipText(toolTip, 0, 40)
		
	#독일버전에서 시간을 제거하기 위해서 사용 
	def __UpdateDescription2(self):
		if not self.description:
			return

		toolTip = self.description
		self.SetToolTipText(toolTip, 0, 40)

	if app.ENABLE_SET_ITEM:
		def UpdateSetItemDescription(self):
			if not self.description:
				return

			if not self.tooltipItem:
				toolTip = self.description
			else:
				toolTip = self.description
				toolTip += "\\n"
				setitem_effect_dict = playerm2g2.GetSetItemEffect()

				if type(setitem_effect_dict) is dict:
					if len(setitem_effect_dict) > 0:
						for k in setitem_effect_dict.keys():
							toolTip += self.tooltipItem.GetAffectString( k, setitem_effect_dict[k] )
							toolTip += "\\n"

			self.SetToolTipText(toolTip, 0, 30, True, 15)
	
	if app.ENABLE_LUCKY_EVENT:
		def AddMultiLineDescription(self, affect_type, affect_value, duration):
			
			endTime = 0
			if duration > 0:
				endTime = app.GetGlobalTimeStamp() + duration
				
			applyType = item.GetPointApply(affect_type)
			if not applyType:
				return	
			self.multi_affect_dict[applyType] = [affect_value, endTime]
			
		def UpdateMultiLineDescription(self):
			if not self.tooltipItem:
				return
			
			toolTip = ""
			for k, v in self.multi_affect_dict.items():
				toolTip += self.tooltipItem.GetAffectString( k, v[0] )
				if v[1] > 0:
					leftTime = localeInfo.SecondToDHM(v[1] - app.GetGlobalTimeStamp())
					toolTip += " (%s : %s)" % (localeInfo.LEFT_TIME, leftTime)
				toolTip += "\\n"
			self.SetToolTipText(toolTip, 0, 30, True, 15)
		
	def SetSkillAffectFlag(self, flag):
		self.isSkillAffect = flag

	def IsSkillAffect(self):
		return self.isSkillAffect

	def OnMouseOverIn(self):
		if self.toolTipText:
			self.toolTipText.Show()

	def OnMouseOverOut(self):
		if self.toolTipText:
			self.toolTipText.Hide()

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	IMAGE_STEP = 25
	AFFECT_MAX_NUM = 32

	INFINITE_AFFECT_DURATION = 0x1FFFFFFF 
	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DATA_DICT =	{
				chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/poison.sub"),
				chr.AFFECT_BLEEDING : (localeInfo.SKILL_BLEEDING, "d:/ymir work/ui/skill/common/affect/poison.sub"),
				chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/slow.sub"),
				chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.sub"),

				chr.AFFECT_ATT_SPEED_POTION : (localeInfo.SKILL_INC_ATKSPD, "d:/ymir work/ui/skill/common/affect/Increase_Attack_Speed.sub"),
				chr.AFFECT_MOV_SPEED_POTION : (localeInfo.SKILL_INC_MOVSPD, "d:/ymir work/ui/skill/common/affect/Increase_Move_Speed.sub"),
				chr.AFFECT_FISH_MIND : (localeInfo.SKILL_FISHMIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub"),

				chr.AFFECT_JEONGWI : (localeInfo.SKILL_JEONGWI, "d:/ymir work/ui/skill/warrior/jeongwi_03.sub",),
				chr.AFFECT_GEOMGYEONG : (localeInfo.SKILL_GEOMGYEONG, "d:/ymir work/ui/skill/warrior/geomgyeong_03.sub",),
				chr.AFFECT_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
				chr.AFFECT_GYEONGGONG : (localeInfo.SKILL_GYEONGGONG, "d:/ymir work/ui/skill/assassin/gyeonggong_03.sub",),
				chr.AFFECT_EUNHYEONG : (localeInfo.SKILL_EUNHYEONG, "d:/ymir work/ui/skill/assassin/eunhyeong_03.sub",),
				chr.AFFECT_GWIGEOM : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/sura/gwigeom_03.sub",),
				chr.AFFECT_GONGPO : (localeInfo.SKILL_GONGPO, "d:/ymir work/ui/skill/sura/gongpo_03.sub",),
				chr.AFFECT_JUMAGAP : (localeInfo.SKILL_JUMAGAP, "d:/ymir work/ui/skill/sura/jumagap_03.sub"),
				chr.AFFECT_HOSIN : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin_03.sub",),
				chr.AFFECT_BOHO : (localeInfo.SKILL_BOHO, "d:/ymir work/ui/skill/shaman/boho_03.sub",),
				chr.AFFECT_KWAESOK : (localeInfo.SKILL_KWAESOK, "d:/ymir work/ui/skill/shaman/kwaesok_03.sub",),
				chr.AFFECT_HEUKSIN : (localeInfo.SKILL_HEUKSIN, "d:/ymir work/ui/skill/sura/heuksin_03.sub",),
				chr.AFFECT_MUYEONG : (localeInfo.SKILL_MUYEONG, "d:/ymir work/ui/skill/sura/muyeong_03.sub",),
				chr.AFFECT_GICHEON : (localeInfo.SKILL_GICHEON, "d:/ymir work/ui/skill/shaman/gicheon_03.sub",),
				chr.AFFECT_JEUNGRYEOK : (localeInfo.SKILL_JEUNGRYEOK, "d:/ymir work/ui/skill/shaman/jeungryeok_03.sub",),
				chr.AFFECT_PABEOP : (localeInfo.SKILL_PABEOP, "d:/ymir work/ui/skill/sura/pabeop_03.sub",),
				chr.AFFECT_FALLEN_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
				28 : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
				chr.AFFECT_CHINA_FIREWORK : (localeInfo.SKILL_POWERFUL_STRIKE, "d:/ymir work/ui/skill/common/affect/powerfulstrike.sub",),
				chr.AFFECT_RED_POSSESSION : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/wolfman/red_possession_03.sub",),
				chr.AFFECT_BLUE_POSSESSION : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/wolfman/blue_possession_03.sub",),

				#64 - END
				chr.NEW_AFFECT_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),

				chr.NEW_AFFECT_ITEM_BONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
				chr.NEW_AFFECT_SAFEBOX : (localeInfo.TOOLTIP_MALL_SAFEBOX, "d:/ymir work/ui/skill/common/affect/safebox.sub",),
				chr.NEW_AFFECT_AUTOLOOT : (localeInfo.TOOLTIP_MALL_AUTOLOOT, "d:/ymir work/ui/skill/common/affect/autoloot.sub",),
				chr.NEW_AFFECT_FISH_MIND : (localeInfo.TOOLTIP_MALL_FISH_MIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub",),
				chr.NEW_AFFECT_MARRIAGE_FAST : (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, "d:/ymir work/ui/skill/common/affect/marriage_fast.sub",),
				chr.NEW_AFFECT_GOLD_BONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),

				chr.NEW_AFFECT_NO_DEATH_PENALTY : (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				chr.NEW_AFFECT_SKILL_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				
				# 자동물약 hp, sp
				chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_hpgauge/05.dds"),			
				chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_spgauge/05.dds"),
				#chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),			
				#chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub"),			

				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/def_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_EXPBONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_ITEMBONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_GOLDBONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,"d:/ymir work/ui/skill/common/affect/critical.sub"),
				MALL_DESC_IDX_START+playerm2g2.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				MALL_DESC_IDX_START+playerm2g2.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				MALL_DESC_IDX_START+playerm2g2.POINT_MAX_SP_PCT : (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),	

				MALL_DESC_IDX_START+playerm2g2.POINT_PC_BANG_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/EXP_Bonus_p_on.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_PC_BANG_DROP_BONUS: (localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/Item_Bonus_p_on.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MELEE_MAGIC_ATT_BONUS_PER : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
		}
	else:
		AFFECT_DATA_DICT =	{
				chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/poison.sub"),
				chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/slow.sub"),
				chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.sub"),

				chr.AFFECT_ATT_SPEED_POTION : (localeInfo.SKILL_INC_ATKSPD, "d:/ymir work/ui/skill/common/affect/Increase_Attack_Speed.sub"),
				chr.AFFECT_MOV_SPEED_POTION : (localeInfo.SKILL_INC_MOVSPD, "d:/ymir work/ui/skill/common/affect/Increase_Move_Speed.sub"),
				chr.AFFECT_FISH_MIND : (localeInfo.SKILL_FISHMIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub"),

				chr.AFFECT_JEONGWI : (localeInfo.SKILL_JEONGWI, "d:/ymir work/ui/skill/warrior/jeongwi_03.sub",),
				chr.AFFECT_GEOMGYEONG : (localeInfo.SKILL_GEOMGYEONG, "d:/ymir work/ui/skill/warrior/geomgyeong_03.sub",),
				chr.AFFECT_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
				chr.AFFECT_GYEONGGONG : (localeInfo.SKILL_GYEONGGONG, "d:/ymir work/ui/skill/assassin/gyeonggong_03.sub",),
				chr.AFFECT_EUNHYEONG : (localeInfo.SKILL_EUNHYEONG, "d:/ymir work/ui/skill/assassin/eunhyeong_03.sub",),
				chr.AFFECT_GWIGEOM : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/sura/gwigeom_03.sub",),
				chr.AFFECT_GONGPO : (localeInfo.SKILL_GONGPO, "d:/ymir work/ui/skill/sura/gongpo_03.sub",),
				chr.AFFECT_JUMAGAP : (localeInfo.SKILL_JUMAGAP, "d:/ymir work/ui/skill/sura/jumagap_03.sub"),
				chr.AFFECT_HOSIN : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin_03.sub",),
				chr.AFFECT_BOHO : (localeInfo.SKILL_BOHO, "d:/ymir work/ui/skill/shaman/boho_03.sub",),
				chr.AFFECT_KWAESOK : (localeInfo.SKILL_KWAESOK, "d:/ymir work/ui/skill/shaman/kwaesok_03.sub",),
				chr.AFFECT_HEUKSIN : (localeInfo.SKILL_HEUKSIN, "d:/ymir work/ui/skill/sura/heuksin_03.sub",),
				chr.AFFECT_MUYEONG : (localeInfo.SKILL_MUYEONG, "d:/ymir work/ui/skill/sura/muyeong_03.sub",),
				chr.AFFECT_GICHEON : (localeInfo.SKILL_GICHEON, "d:/ymir work/ui/skill/shaman/gicheon_03.sub",),
				chr.AFFECT_JEUNGRYEOK : (localeInfo.SKILL_JEUNGRYEOK, "d:/ymir work/ui/skill/shaman/jeungryeok_03.sub",),
				chr.AFFECT_PABEOP : (localeInfo.SKILL_PABEOP, "d:/ymir work/ui/skill/sura/pabeop_03.sub",),
				chr.AFFECT_FALLEN_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
				28 : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
				chr.AFFECT_CHINA_FIREWORK : (localeInfo.SKILL_POWERFUL_STRIKE, "d:/ymir work/ui/skill/common/affect/powerfulstrike.sub",),

				#64 - END
				chr.NEW_AFFECT_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),

				chr.NEW_AFFECT_ITEM_BONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
				chr.NEW_AFFECT_SAFEBOX : (localeInfo.TOOLTIP_MALL_SAFEBOX, "d:/ymir work/ui/skill/common/affect/safebox.sub",),
				chr.NEW_AFFECT_AUTOLOOT : (localeInfo.TOOLTIP_MALL_AUTOLOOT, "d:/ymir work/ui/skill/common/affect/autoloot.sub",),
				chr.NEW_AFFECT_FISH_MIND : (localeInfo.TOOLTIP_MALL_FISH_MIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub",),
				chr.NEW_AFFECT_MARRIAGE_FAST : (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, "d:/ymir work/ui/skill/common/affect/marriage_fast.sub",),
				chr.NEW_AFFECT_GOLD_BONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),

				chr.NEW_AFFECT_NO_DEATH_PENALTY : (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				chr.NEW_AFFECT_SKILL_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				
				# 자동물약 hp, sp
				chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_hpgauge/05.dds"),			
				chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_spgauge/05.dds"),
				#chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),			
				#chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub"),			

				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/def_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_EXPBONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_ITEMBONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MALL_GOLDBONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,"d:/ymir work/ui/skill/common/affect/critical.sub"),
				MALL_DESC_IDX_START+playerm2g2.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				MALL_DESC_IDX_START+playerm2g2.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
				MALL_DESC_IDX_START+playerm2g2.POINT_MAX_SP_PCT : (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),	

				MALL_DESC_IDX_START+playerm2g2.POINT_PC_BANG_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/EXP_Bonus_p_on.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_PC_BANG_DROP_BONUS: (localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/Item_Bonus_p_on.sub",),
				MALL_DESC_IDX_START+playerm2g2.POINT_MELEE_MAGIC_ATT_BONUS_PER : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
		}
	
	# 용혼석 천, 지 덱.
	AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK1] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga")
	AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK2] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/dragonsoul/buff_ds_land1.tga")

	if app.ENABLE_PVP_TOURNAMENT:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_PVP_EXPBONUS] = (localeInfo.TOOLTIP_PVP_TOURNAMENT_EXPBONUS, "d:/ymir work/ui/skill/common/affect/pvp_exp_bonus.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_PVP_ENTER] = (localeInfo.TOOLTIP_PVP_TOURNAMENT_ENTER, "d:/ymir work/ui/skill/common/affect/pvp_enter.sub")		

	if app.ENABLE_GUILDRENEWAL_SYSTEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_GUILD_SKILL_BLOOD] = (localeInfo.TOOLTIP_GUILD_SKILL_BLOOD, "d:/ymir work/ui/skill/common/affect/guildskill_blood.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_GUILD_SKILL_BLESS] = (localeInfo.TOOLTIP_GUILD_SKILL_BLESS, "d:/ymir work/ui/skill/common/affect/guildskill_bless.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_GUILD_SKILL_SEONGHWI] = (localeInfo.TOOLTIP_GUILD_SKILL_SEONGHWI, "d:/ymir work/ui/skill/common/affect/guildskill_seonghwi.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_GUILD_SKILL_ACCEL] = (localeInfo.TOOLTIP_GUILD_SKILL_ACCEL, "d:/ymir work/ui/skill/common/affect/guildskill_accel.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_GUILD_SKILL_BUNNO] = (localeInfo.TOOLTIP_GUILD_SKILL_BUNNO, "d:/ymir work/ui/skill/common/affect/guildskill_bunno.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_GUILD_SKILL_JUMUN] = (localeInfo.TOOLTIP_GUILD_SKILL_JUMUN, "d:/ymir work/ui/skill/common/affect/guildskill_jumun.sub")
		
	if app.ENABLE_AUTO_SYSTEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_AUTO_USE] = (localeInfo.TOOLTIP_AUTO_SYSTEM_PRIMIUM, "d:/ymir work/ui/skill/common/affect/auto_premium.sub")
		
	if app.ENABLE_SET_ITEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_SET_ITEM] = (localeInfo.TOOLTIP_SET_ITEM, "d:/ymir work/ui/skill/common/affect/set_bonus.sub")

	if app.ENABLE_MONSTER_BACK:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_EXP_BONUS_EVENT] = (localeInfo.TOOLTIP_EXP_BONUS_EVENT, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_ATT_SPEED_SLOW] = (localeInfo.TOOLTIP_ATT_SPEED_SLOW, "d:/ymir work/ui/skill/common/affect/att_slow.sub")
		
	if app.ENABLE_PEPSI_EVENT:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_PEPSI_EVENT] = (localeInfo.TOOLTIP_PEPSI_EVENT, "d:/ymir work/ui/skill/common/affect/pepsi_bonus.sub")
	
	if app.ENABLE_BATTLE_FIELD:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_BATTLE_POTION] = (localeInfo.TOOLTIP_BATTLE_POTION, "d:/ymir work/ui/public/battle/buff_battle_potion.sub")
		
	if app.ENABLE_MONSTER_CARD:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_POLYMORPH] = (localeInfo.TOOLTIP_AFFECT_POLYMORPH, "d:/ymir work/ui/game/monster_card/poly_affect.sub")
		
	if app.ENABLE_LUCKY_EVENT:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_LUCKEY_EVENT_BUFF] = (localeInfo.TOOLTIP_SET_ITEM, "d:/ymir work/ui/skill/common/affect/set_bonus.sub")

	if app.ENABLE_ELEMENT_ADD:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_MOUNT_FALL] = (localeInfo.TOOLTIP_AFFECT_MOUNT_FALL, "d:/ymir work/ui/skill/common/affect/mount_fall.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_NO_RECOVERY] = (localeInfo.TOOLTIP_AFFECT_RHP_REGEN, "d:/ymir work/ui/skill/common/affect/rhp_regen.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_REDUCE_CAST_SPEED] = (localeInfo.TOOLTIP_AFFECT_RCAST_SPEED, "d:/ymir work/ui/skill/common/affect/rcast_speed.sub")

	if app.ENABLE_12ZI:
		AFFECT_DATA_DICT[chr.AFFECT_ELECTRIC_SHOCK]			= (localeInfo.TOOLTIP_AFFECT_ELECTRIC_SHOCK,		"d:/ymir work/ui/skill/common/affect/poison.sub")
		AFFECT_DATA_DICT[chr.AFFECT_CONFUSION]				= (localeInfo.TOOLTIP_AFFECT_CONFUSION,				"d:/ymir work/ui/skill/common/affect/confusion.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_ATT_GRADE_DOWN]		= (localeInfo.TOOLTIP_AFFECT_ATT_GRADE_DOWN,		"d:/ymir work/ui/skill/common/affect/att_grade_down.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DEF_GRADE_DOWN]		= (localeInfo.TOOLTIP_AFFECT_DEF_GRADE_DOWN,		"d:/ymir work/ui/skill/common/affect/def_grade_down.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_CRITICAL_PCT_DOWN]	= (localeInfo.TOOLTIP_AFFECT_CRITICAL_GRADE_DOWN,	"d:/ymir work/ui/skill/common/affect/critical_pct_down.sub")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_CZ_UNLIMIT_ENTER]	= (localeInfo.TOOLTIP_AFFECT_CZ_UNLIMIT_ENTER,	"d:/ymir work/ui/skill/common/affect/cz_unlimit_enter.sub")

	if app.ENABLE_FLOWER_EVENT:
		AFFECT_DATA_DICT[chr.AFFECT_FLOWER_EVENT]	= ("",	"d:/ymir work/ui/skill/common/affect/flower_event.sub")
		
	if app.ENABLE_RESEARCHER_ELIXIR_FIX:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_RESEARCHER_ELIXIR] = (localeInfo.TOOLTIP_AFFECT_RESEARCHER_ELIXIR, "d:/ymir work/ui/skill/common/affect/researcher_elixir.sub")
	
	def __init__(self):
		ui.Window.__init__(self)

		self.serverPlayTime=0
		self.clientPlayTime=0
		
		self.lastUpdateTime=0
		self.affectImageDict={}
		self.horseImage=None
		self.lovePointImage=None
		self.autoPotionImageHP = AutoPotionImage()
		self.autoPotionImageSP = AutoPotionImage()
		self.SetPosition(10, 10)
		self.Show()
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.petSkillaffectImageDict = {}

		if app.ENABLE_SET_ITEM:
			self.SetItemAffectCheck()
		
	def __del__(self):
		ui.Window.__del__(self)

	if app.ENABLE_SET_ITEM:
		def SetItemAffectCheck(self):
			#set affect off
			if playerm2g2.EmptySetItemEffect():
				self.BINARY_NEW_RemoveAffect(chr.NEW_AFFECT_SET_ITEM, 0)
			#set affect on
			else:
				self.BINARY_NEW_RemoveAffect(chr.NEW_AFFECT_SET_ITEM, 0)
				self.BINARY_NEW_AddAffect(chr.NEW_AFFECT_SET_ITEM, 0, 0, self.INFINITE_AFFECT_DURATION)

	def ClearAllAffects(self):
		self.horseImage=None
		self.lovePointImage=None
		self.affectImageDict={}
		
		if app.ENABLE_GROWTH_PET_SYSTEM:
			self.petSkillaffectImageDict = {}
			
		self.__ArrangeImageList()

	def ClearAffects(self): ## 스킬 이펙트만 없앱니다.
		self.living_affectImageDict={}
		for key, image in self.affectImageDict.items():
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image
		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):

		if app.ENABLE_GUILDRENEWAL_SYSTEM:
			if type < 500:
				if type >= chr.NEW_AFFECT_GUILD_SKILL_BLOOD and type <= chr.NEW_AFFECT_GUILD_SKILL_JUMUN:
					pass
				else:
					if app.ENABLE_MONSTER_CARD and type == chr.NEW_AFFECT_POLYMORPH:
						pass
					else:
						return
		else:
			if type < 500:
				if app.ENABLE_MONSTER_CARD and type == chr.NEW_AFFECT_POLYMORPH:
					pass
				else:
					return

		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type

		if app.ENABLE_LUCKY_EVENT:
			if self.affectImageDict.has_key(affect):
				if affect == chr.NEW_AFFECT_LUCKEY_EVENT_BUFF:
					self.affectImageDict[affect].AddMultiLineDescription(pointIdx, value, duration)
					self.affectImageDict[affect].UpdateMultiLineDescription()
				return
		else:
			if self.affectImageDict.has_key(affect):
				return

		if not self.AFFECT_DATA_DICT.has_key(affect):
			return
			
		if app.ENABLE_AUTO_SYSTEM:
			if type == chr.NEW_AFFECT_AUTO_USE:
				import chrmgrm2g
				if not chrmgrm2g.GetAutoOnOff():
					return

		## 용신의 가호, 선인의 교훈은 Duration 을 0 으로 설정한다.
		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or\
		   affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or\
		   affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or\
		   affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]
		description = affectData[0]
		filename = affectData[1]

		if pointIdx == playerm2g2.POINT_MALL_ITEMBONUS or\
		   pointIdx == playerm2g2.POINT_MALL_GOLDBONUS:
			value = 1 + float(value) / 100.0

		trashValue = 123
		#if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
		if trashValue == 1:
			try:
				#image = AutoPotionImage()
				#image.SetParent(self)
				image = None
				
				if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
					image.SetPotionType(playerm2g2.AUTO_POTION_TYPE_SP)
					image = self.autoPotionImageSP
					#self.autoPotionImageSP = image;
				else:
					image.SetPotionType(playerm2g2.AUTO_POTION_TYPE_HP)
					image = self.autoPotionImageHP
					#self.autoPotionImageHP = image;
				
				image.SetParent(self)
				image.Show()
				image.OnUpdateAutoPotionImage()
				
				self.affectImageDict[affect] = image
				self.__ArrangeImageList()
				
			except Exception, e:
				print "except Aff auto potion affect ", e
				pass				
			
		else:
			if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY:

				if app.ENABLE_FLOWER_EVENT:
					if affect == chr.AFFECT_FLOWER_EVENT:
						description = uiToolTip.ItemToolTip.AFFECT_DICT[item.GetPointApply(pointIdx)](float(value))
					else:
						description = description(float(value))
				else:
					description = description(float(value))

			try:
				print "Add affect %s" % affect
				image = AffectImage()
				image.SetParent(self)
				image.LoadImage(filename)
				image.SetDescription(description)
				image.SetDuration(duration)
				image.SetAffect(affect)

				if app.ENABLE_SET_ITEM and affect == chr.NEW_AFFECT_SET_ITEM:
					image.SetClock(FALSE)
					image.UpdateSetItemDescription()
				elif app.ENABLE_LUCKY_EVENT and affect == chr.NEW_AFFECT_LUCKEY_EVENT_BUFF:
					image.AddMultiLineDescription(pointIdx, value, duration)
					image.UpdateMultiLineDescription()
				elif affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE or\
					affect == chr.NEW_AFFECT_EXP_BONUS_EURO_FREE_UNDER_15 or\
					self.INFINITE_AFFECT_DURATION < duration:
					image.SetClock(FALSE)
					image.UpdateDescription()
				elif affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
					image.UpdateAutoPotionDescription()
				elif app.ENABLE_MONSTER_BACK and affect == chr.NEW_AFFECT_ATT_SPEED_SLOW:
					image.SetClock(FALSE)
					image.UpdateDescription()
				elif app.ENABLE_12ZI and (affect == chr.NEW_AFFECT_ATT_GRADE_DOWN or affect == chr.NEW_AFFECT_DEF_GRADE_DOWN or affect == chr.NEW_AFFECT_CRITICAL_PCT_DOWN or\
				 affect == chr.NEW_AFFECT_MOUNT_FALL or affect == chr.NEW_AFFECT_NO_RECOVERY or affect == chr.NEW_AFFECT_REDUCE_CAST_SPEED):
					image.SetClock(FALSE)
					image.UpdateDescription()
				elif app.ENABLE_RESEARCHER_ELIXIR_FIX and affect == chr.NEW_AFFECT_RESEARCHER_ELIXIR:
					image.SetClock(FALSE)
					image.UpdateDescription()				
				else:
					image.UpdateDescription()

				if affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK1 or affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK2:
					image.SetScale(1, 1)
				else:
					image.SetScale(0.7, 0.7)
				image.SetSkillAffectFlag(FALSE)
				image.Show()
				self.affectImageDict[affect] = image
				self.__ArrangeImageList()
			except Exception, e:
				print "except Aff affect ", e
				pass

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type
	
		#print "Remove Affect %s %s" % ( type , pointIdx )
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level==0:
			self.horseImage=None
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage=image
			self.__ArrangeImageList()

	def SetPlayTime(self, playTime):
		self.serverPlayTime = playTime
		self.clientPlayTime = app.GetTime()
		
		if localeInfo.IsVIETNAM():		
			image = PlayTimeImage()
			image.SetParent(self)
			image.SetPlayTime(playTime)
			image.Show()

			self.playTimeImage=image
			self.__ArrangeImageList()

	def __AppendAffect(self, affect):

		if self.affectImageDict.has_key(affect):
			return

		try:
			affectData = self.AFFECT_DATA_DICT[affect]
		except KeyError:
			return

		name = affectData[0]
		filename = affectData[1]

		skillIndex = playerm2g2.AffectIndexToSkillIndex(affect)
		if 0 != skillIndex:
			name = skill.GetSkillName(skillIndex)

		image = AffectImage()
		image.SetParent(self)
		image.SetSkillAffectFlag(TRUE)

		try:
			image.LoadImage(filename)
		except:
			pass

		image.SetToolTipText(name, 0, 40)
		image.SetScale(0.7, 0.7)
		image.Show()
		self.affectImageDict[affect] = image

	def __RemoveAffect(self, affect):
		"""
		if affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
			self.autoPotionImageSP.Hide()

		if affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			self.autoPotionImageHP.Hide()
		"""
			
		if not self.affectImageDict.has_key(affect):
			#print "__RemoveAffect %s ( No Affect )" % affect
			return

		#print "__RemoveAffect %s ( Affect )" % affect
		del self.affectImageDict[affect]
		
		self.__ArrangeImageList()

	def __ArrangeImageList(self):

		width = len(self.affectImageDict) * self.IMAGE_STEP
		if self.lovePointImage:
			width+=self.IMAGE_STEP
		if self.horseImage:
			width+=self.IMAGE_STEP
			
		if app.ENABLE_GROWTH_PET_SYSTEM:
			width += len(self.petSkillaffectImageDict) * self.IMAGE_STEP
			
		self.SetSize(width, 26)

		xPos = 0

		if app.ENABLE_GROWTH_PET_SYSTEM:
			tempDict = {}
			for value in self.petSkillaffectImageDict.values():
				tempDict[value[0]] = value[1]
			
			for value in range(1,4):
				if tempDict.has_key(value):
					tempDict[value].SetPosition(xPos, 0)
					xPos += self.IMAGE_STEP
			
		
		if self.lovePointImage:
			if self.lovePointImage.IsShow():
				self.lovePointImage.SetPosition(xPos, 0)
				xPos += self.IMAGE_STEP

		if self.horseImage:
			self.horseImage.SetPosition(xPos, 0)
			xPos += self.IMAGE_STEP

		for image in self.affectImageDict.values():
			image.SetPosition(xPos, 0)
			xPos += self.IMAGE_STEP

	def OnUpdate(self):		
		try:
			# MT-342 둔갑시 시간 표시 버그
			if app.GetGlobalTimeStamp() > self.lastUpdateTime:
			#if app.GetGlobalTime() - self.lastUpdateTime > 500:
			#if 0 < app.GetGlobalTime():
				# MT-342 둔갑시 시간 표시 버그
				#self.lastUpdateTime = app.GetGlobalTime()
				self.lastUpdateTime = app.GetGlobalTimeStamp()

				for image in self.affectImageDict.values():
					if image.GetAffect() == chr.NEW_AFFECT_AUTO_HP_RECOVERY or image.GetAffect() == chr.NEW_AFFECT_AUTO_SP_RECOVERY:
						image.UpdateAutoPotionDescription()
						continue

					if app.ENABLE_SET_ITEM:
						if image.GetAffect() == chr.NEW_AFFECT_SET_ITEM:
							continue
					
					if app.ENABLE_LUCKY_EVENT:
						if image.GetAffect() == chr.NEW_AFFECT_LUCKEY_EVENT_BUFF:
							image.UpdateMultiLineDescription()
							continue

					if not image.IsSkillAffect():
						image.UpdateDescription()
		except Exception, e:
			print "AffectShower::OnUpdate error : ", e
			
			
			
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def SetPetSkillAffect(self, index, affect):
		
			if self.__AppendPetSkillAffect(index, affect):
				self.__ArrangeImageList()
				
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def ClearPetSkillAffect(self):
			self.petSkillaffectImageDict.clear()
			self.__ArrangeImageList()
				
	if app.ENABLE_GROWTH_PET_SYSTEM:
		def __AppendPetSkillAffect(self, index, affect):
			
			if self.petSkillaffectImageDict.has_key(affect):
				return False
			
			filename = skill.GetPetSkillIconPath(affect)
			if "" == filename:
				return False
				
			( pet_skill_name, pet_skill_desc, pet_skill_use_type, pet_skill_cool_time ) = skill.GetPetSkillInfo(affect)

			image = GrowthPetImage()
			image.SetParent(self)

			try:
				image.LoadImage(filename)
			except:
				print "LoadImage Except nn"
				return False
				
			image.SetToolTipText(pet_skill_name, 0, 40)
			
			image.SetDescription(pet_skill_desc)
		
			image.SetScale(0.7, 0.7)
			
			image.Show()
	
			self.petSkillaffectImageDict[affect] = [index, image]
			
			return True
