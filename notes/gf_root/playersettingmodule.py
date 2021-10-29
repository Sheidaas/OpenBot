import chr
import chrmgrm2g
import skill
import m2netm2g
import item
import playerm2g2
import effect
import constInfo
import localeInfo
import emotion

import app

if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
	import guild

JOB_WARRIOR		= 0
JOB_ASSASSIN	= 1
JOB_SURA		= 2
JOB_SHAMAN		= 3
if app.ENABLE_WOLFMAN_CHARACTER:
	JOB_WOLFMAN		= 4

RACE_WARRIOR_M	= 0
RACE_ASSASSIN_W	= 1
RACE_SURA_M		= 2
RACE_SHAMAN_W	= 3
RACE_WARRIOR_W	= 4
RACE_ASSASSIN_M	= 5
RACE_SURA_W		= 6
RACE_SHAMAN_M	= 7
if app.ENABLE_WOLFMAN_CHARACTER:
	RACE_WOLFMAN_M	= 8

COMBO_TYPE_1 = 0
COMBO_TYPE_2 = 1
COMBO_TYPE_3 = 2

COMBO_INDEX_1 = 0
COMBO_INDEX_2 = 1
COMBO_INDEX_3 = 2
COMBO_INDEX_4 = 3
COMBO_INDEX_5 = 4
COMBO_INDEX_6 = 5

HORSE_SKILL_WILDATTACK = chr.MOTION_SKILL+121
HORSE_SKILL_CHARGE = chr.MOTION_SKILL+122
HORSE_SKILL_SPLASH = chr.MOTION_SKILL+123

GUILD_SKILL_DRAGONBLOOD = chr.MOTION_SKILL+101
GUILD_SKILL_DRAGONBLESS = chr.MOTION_SKILL+102
GUILD_SKILL_BLESSARMOR = chr.MOTION_SKILL+103
GUILD_SKILL_SPPEDUP = chr.MOTION_SKILL+104
GUILD_SKILL_DRAGONWRATH = chr.MOTION_SKILL+105
GUILD_SKILL_MAGICUP = chr.MOTION_SKILL+106

PASSIVE_GUILD_SKILL_INDEX_LIST = ( 151, )
ACTIVE_GUILD_SKILL_INDEX_LIST = ( 152, 153, 154, 155, 156, 157, )

if app.ENABLE_678TH_SKILL:
	NEW_678TH_SKILL_ENABLE = 1
else:
	NEW_678TH_SKILL_ENABLE = 0
SKILL_INDEX_DICT = []

def DefineSkillIndexDict():
	global NEW_678TH_SKILL_ENABLE
	global SKILL_INDEX_DICT
	
	#NEW_678TH_SKILL_ENABLE = localeInfo.IsYMIR()
	if app.ENABLE_WOLFMAN_CHARACTER:
		if NEW_678TH_SKILL_ENABLE:
			SKILL_INDEX_DICT = {
				JOB_WARRIOR : { 
					1 : (1, 2, 3, 4, 5, 6, 0, 0, 137, 0, 138, 0, 139, 0,), 
					2 : (16, 17, 18, 19, 20, 21, 0, 0, 137, 0, 138, 0, 139, 0,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_ASSASSIN : { 
					1 : (31, 32, 33, 34, 35, 36, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					2 : (46, 47, 48, 49, 50, 51, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_SURA : { 
					1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_SHAMAN : { 
					1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_WOLFMAN : { # TODO: 수인족 스킬 등록
					1 : (170, 171, 172, 173, 174, 175, 0, 0, 137, 0, 138, 0, 139, 0,), 
					2 : (170, 171, 172, 173, 174, 175, 0, 0, 137, 0, 138, 0, 139, 0,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},			
			}
		else:
			SKILL_INDEX_DICT = {
				JOB_WARRIOR : { 
					1 : (1, 2, 3, 4, 5, 0, 0, 0, 137, 0, 138, 0, 139, 0,), 
					2 : (16, 17, 18, 19, 20, 0, 0, 0, 137, 0, 138, 0, 139, 0,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_ASSASSIN : { 
					1 : (31, 32, 33, 34, 35, 0, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					2 : (46, 47, 48, 49, 50, 0, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_SURA : { 
					1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_SHAMAN : { 
					1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_WOLFMAN : { # TODO: 수인족 스킬 등록
					1 : (170, 171, 172, 173, 174, 175, 0, 0, 137, 0, 138, 0, 139, 0,), 
					2 : (170, 171, 172, 173, 174, 175, 0, 0, 137, 0, 138, 0, 139, 0,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
			}
	else:
		if NEW_678TH_SKILL_ENABLE:
			SKILL_INDEX_DICT = {
				JOB_WARRIOR : { 
					1 : (1, 2, 3, 4, 5, 6, 0, 0, 137, 0, 138, 0, 139, 0,), 
					2 : (16, 17, 18, 19, 20, 21, 0, 0, 137, 0, 138, 0, 139, 0,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131, 141, 142,),
				},
				JOB_ASSASSIN : { 
					1 : (31, 32, 33, 34, 35, 36, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					2 : (46, 47, 48, 49, 50, 51, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131, 141, 142,),
				},
				JOB_SURA : { 
					1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131, 141, 142,),
				},
				JOB_SHAMAN : { 
					1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131, 141, 142,),
				},		
			}
		else:
			SKILL_INDEX_DICT = {
				JOB_WARRIOR : { 
					1 : (1, 2, 3, 4, 5, 0, 0, 0, 137, 0, 138, 0, 139, 0,), 
					2 : (16, 17, 18, 19, 20, 0, 0, 0, 137, 0, 138, 0, 139, 0,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_ASSASSIN : { 
					1 : (31, 32, 33, 34, 35, 0, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					2 : (46, 47, 48, 49, 50, 0, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_SURA : { 
					1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
				JOB_SHAMAN : { 
					1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
					2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
					"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,),
				},
			}
	
	if app.ENABLE_AUTO_ATTACK:
		UPDATE_SKILL_INDEX_DICK = {"SUPPORT" : (122, 123, 121, 124, 125, 129, 0, 0, 130, 131,132,),}
		if app.ENABLE_WOLFMAN_CHARACTER:
			SKILL_INDEX_DICT[JOB_WOLFMAN].update(UPDATE_SKILL_INDEX_DICK)
		SKILL_INDEX_DICT[JOB_WARRIOR].update(UPDATE_SKILL_INDEX_DICK)
		SKILL_INDEX_DICT[JOB_ASSASSIN].update(UPDATE_SKILL_INDEX_DICK)
		SKILL_INDEX_DICT[JOB_SURA].update(UPDATE_SKILL_INDEX_DICK)
		SKILL_INDEX_DICT[JOB_SHAMAN].update(UPDATE_SKILL_INDEX_DICK)

def RegisterSkill(race, group, empire=0):

	DefineSkillIndexDict()
	
	job = chr.RaceToJob(race)

	## Character Skill
	if SKILL_INDEX_DICT.has_key(job):

		if SKILL_INDEX_DICT[job].has_key(group):
		
			activeSkillList = SKILL_INDEX_DICT[job][group]

			for i in xrange(len(activeSkillList)):
				skillIndex = activeSkillList[i]
				
				## 7번 8번 스킬은 여기서 설정하면 안됨
				if i != 6 and i != 7:
					playerm2g2.SetSkill(i+1, skillIndex)

			supportSkillList = SKILL_INDEX_DICT[job]["SUPPORT"]

			for i in xrange(len(supportSkillList)):
				playerm2g2.SetSkill(i+100+1, supportSkillList[i])

	## Language Skill
	if 0 != empire:
		languageSkillList = []
		for i in xrange(3):
			if (i+1) != empire:
				languageSkillList.append(playerm2g2.SKILL_INDEX_LANGUAGE1+i)
		for i in xrange(len(languageSkillList)):
			playerm2g2.SetSkill(107+i, languageSkillList[i])

	## Guild Skill
	for i in xrange(len(PASSIVE_GUILD_SKILL_INDEX_LIST)):
		playerm2g2.SetSkill(200+i, PASSIVE_GUILD_SKILL_INDEX_LIST[i])

	for i in xrange(len(ACTIVE_GUILD_SKILL_INDEX_LIST)):
		playerm2g2.SetSkill(210+i, ACTIVE_GUILD_SKILL_INDEX_LIST[i])

def RegisterSkillAt(race, group, pos, num):
	
	DefineSkillIndexDict()
	
	job = chr.RaceToJob(race)
	tmp = list(SKILL_INDEX_DICT[job][group])
	tmp[pos] = num
	SKILL_INDEX_DICT[job][group] = tuple(tmp)
	playerm2g2.SetSkill(pos+1, num)

FACE_IMAGE_DICT = {
	RACE_WARRIOR_M	: "d:/ymir work/ui/game/windows/face_warrior.sub",
	RACE_ASSASSIN_W	: "d:/ymir work/ui/game/windows/face_assassin.sub",
	RACE_SURA_M	: "d:/ymir work/ui/game/windows/face_sura.sub",
	RACE_SHAMAN_W	: "d:/ymir work/ui/game/windows/face_shaman.sub",
}

isInitData=0

def SetGeneralMotions(mode, folder):
	chrmgrm2g.SetPathName(folder)
	chrmgrm2g.RegisterMotionMode(mode)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_WAIT,				"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_RUN,					"run.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE,				"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE,				"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_BACK,			"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_BACK,			"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_FLYING,		"damage_flying.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_STAND_UP,			"falling_stand.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_FLYING_BACK,	"back_damage_flying.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_STAND_UP_BACK,		"back_falling_stand.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DIG,					"dig.msa")

def SetNewGeneralMotions(mode, folder):
	chrmgrm2g.SetPathName(folder)
	chrmgrm2g.RegisterMotionMode(mode)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_WAIT,				"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_RUN,					"run.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE,				"front_damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE,				"front_damage1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_BACK,			"back_damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_BACK,			"back_damage1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_FLYING,		"front_damage_flying.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_STAND_UP,			"front_falling_standup.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DAMAGE_FLYING_BACK,	"back_damage_flying.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_STAND_UP_BACK,		"back_falling_standup.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_DIG,					"dig.msa")

def SetIntroMotions(mode, folder):
	chrmgrm2g.SetPathName(folder)
	chrmgrm2g.RegisterMotionMode(mode)
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_INTRO_WAIT,			"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_INTRO_SELECTED,		"selected.msa")
	chrmgrm2g.RegisterCacheMotionData(mode,		chr.MOTION_INTRO_NOT_SELECTED,	"not_selected.msa")



def __InitData():
	global isInitData

	if isInitData:
		return			

	isInitData = 1

	chrmgrm2g.SetDustGap(250)
	chrmgrm2g.SetHorseDustGap(500)

	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DUST, "", "d:/ymir work/effect/etc/dust/dust.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_HORSE_DUST, "", "d:/ymir work/effect/etc/dust/running_dust.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_HIT, "", "d:/ymir work/effect/hit/blow_1/blow_1_low.mse")

	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_HPUP_RED, "", "d:/ymir work/effect/etc/recuperation/drugup_red.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_SPUP_BLUE, "", "d:/ymir work/effect/etc/recuperation/drugup_blue.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_SPEEDUP_GREEN, "", "d:/ymir work/effect/etc/recuperation/drugup_green.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DXUP_PURPLE, "", "d:/ymir work/effect/etc/recuperation/drugup_purple.mse")

	#자동물약 HP, SP
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_AUTO_HPUP, "", "d:/ymir work/effect/etc/recuperation/autodrugup_red.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_AUTO_SPUP, "", "d:/ymir work/effect/etc/recuperation/autodrugup_blue.mse")
	
	#라마단 초승달의 반지(71135) 착용순간 발동 이펙트
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_RAMADAN_RING_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item1.mse")
	
	#할로윈 사탕 착용순간 발동 이펙트
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_HALLOWEEN_CANDY_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item2.mse")
	
	#행복의 반지 착용순간 발동 이펙트
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_HAPPINESS_RING_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item3.mse")

	#사랑의 팬던트 착용순간 발동 이펙트
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_LOVE_PENDANT_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item4.mse")
	
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_ACCE_SUCESS_ABSORB, "", "d:/ymir work/effect/etc/buff/buff_item6.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_ACCE_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item7.mse")

	#부활절 캔디(71188) 착용순간 발동 이펙트
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_EASTER_CANDY_EQIP, "", "d:/ymir work/effect/etc/buff/buff_item8.mse")

	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_PENETRATE, "Bip01", "d:/ymir work/effect/hit/gwantong.mse")
	#chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_BLOCK, "", "d:/ymir work/effect/etc/")
	#chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DODGE, "", "d:/ymir work/effect/etc/")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_FIRECRACKER, "", "d:/ymir work/effect/etc/firecracker/newyear_firecracker.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_SPIN_TOP, "", "d:/ymir work/effect/etc/firecracker/paing_i.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_SELECT, "", "d:/ymir work/effect/etc/click/click_select.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_TARGET, "", "d:/ymir work/effect/etc/click/click_glow_select.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_STUN, "Bip01 Head", "d:/ymir work/effect/etc/stun/stun.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_CRITICAL, "Bip01 R Hand", "d:/ymir work/effect/hit/critical.mse")
	playerm2g2.RegisterCacheEffect(playerm2g2.EFFECT_PICK, "d:/ymir work/effect/etc/click/click.mse")
	
	
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_TARGET, "", "d:/ymir work/effect/affect/damagevalue/target.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_NOT_TARGET, "", "d:/ymir work/effect/affect/damagevalue/nontarget.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_SELFDAMAGE, "", "d:/ymir work/effect/affect/damagevalue/damage.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_SELFDAMAGE2, "", "d:/ymir work/effect/affect/damagevalue/damage_1.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_POISON, "", "d:/ymir work/effect/affect/damagevalue/poison.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_MISS, "", "d:/ymir work/effect/affect/damagevalue/miss.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_TARGETMISS, "", "d:/ymir work/effect/affect/damagevalue/target_miss.mse")
	#chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_DAMAGE_CRITICAL, "", "d:/ymir work/effect/affect/damagevalue/critical.mse")

	#chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_SUCCESS, "",			"season1/effect/success.mse")
	#chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_FAIL, "",	"season1/effect/fail.mse")
	
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_LEVELUP_ON_14_FOR_GERMANY, "","season1/effect/paymessage_warning.mse")	#레벨업 14일때 ( 독일전용 )
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_LEVELUP_UNDER_15_FOR_GERMANY, "", "season1/effect/paymessage_decide.mse" )#레벨업 15일때 ( 독일전용 )

	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_PERCENT_DAMAGE1, "", "d:/ymir work/effect/hit/percent_damage1.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_PERCENT_DAMAGE2, "", "d:/ymir work/effect/hit/percent_damage2.mse")
	chrmgrm2g.RegisterCacheEffect(chrmgrm2g.EFFECT_PERCENT_DAMAGE3, "", "d:/ymir work/effect/hit/percent_damage3.mse")
	
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_THUNDER_AREA, "", "D:/ymir work/effect/monster/light_emissive3.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_THUNDER, "", "D:/ymir work/effect/monster/yellow_tigerman_24_1.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_HEAL, "", "D:/ymir work/pc/shaman/effect/jeongeop_2.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_CAPE_OF_COURAGE, "", "D:/ymir work/effect/etc/buff/buff_item9.mse")

	if app.ENABLE_2016_VALENTINE:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_CHOCOLATE_PENDANT, "", "D:/ymir work/effect/etc/buff/buff_item10.mse")
 	
	if app.ENABLE_PEPSI_EVENT:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_PEPSI_EVENT, "", "D:/ymir work/effect/etc/buff/buff_item11.mse")
	
	if app.ENABLE_GUILD_DRAGONLAIR_SYSTEM:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_DRAGONLAIR_STONE_UNBEATABLE_1, "", "D:/ymir work/effect/monster2/redD_moojuk.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_DRAGONLAIR_STONE_UNBEATABLE_2, "", "D:/ymir work/effect/monster2/redD_moojuk_blue.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_DRAGONLAIR_STONE_UNBEATABLE_3, "", "D:/ymir work/effect/monster2/redD_moojuk_green.mse")
		
	if app.ENABLE_BALANCE_IMPROVING:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_FEATHER_WALK, "", "d:/ymir work/effect/hit/gyeonggong_boom.mse")
		
	if app.ENABLE_BATTLE_FIELD:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_BATTLE_POTION, "", "D:/ymir work/effect/etc/buff/buff_item12.mse")
		
	if app.ENABLE_AI_FLAG_REFLECT:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFLECT, "", "D:/ymir work/effect/hit/blow_4/blow_4_ref.mse")
		
	if app.ENABLE_12ZI:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_SKILL_DAMAGE_ZONE, "", "D:/ymir work/effect/monster2/12_shelter_in_01.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_SKILL_SAFE_ZONE, "", "D:/ymir work/effect/monster2/12_shelter_in_02.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_METEOR, "", "D:/ymir work/effect/monster2/12_tiger_s3_drop.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_BEAD_RAIN, "", "D:/ymir work/effect/monster2/12_dra_s2_drop.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_FALL_ROCK, "", "D:/ymir work/effect/monster2/12_mon_s3_drop.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_ARROW_RAIN, "", "D:/ymir work/effect/monster2/12_sna_s3_drop.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_HORSE_DROP, "", "D:/ymir work/effect/monster2/12_hor_s3_drop.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EGG_DROP, "", "D:/ymir work/effect/monster2/12_chi_s3_drop.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_DEAPO_BOOM, "", "D:/ymir work/effect/monster2/daepo_na_02_boom.mse")
		

	if app.ENABLE_FLOWER_EVENT:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_FLOWER_EVENT, "", "d:/ymir work/effect/etc/buff/buff_item15_flower.mse")		
		
	if app.ENABLE_GEM_SYSTEM:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_GEM_PENDANT, "", "d:/ymir work/effect/etc/buff/buff_item16.mse")

	##############
	# WARRIOR
	##############
	chrmgrm2g.CreateRace(RACE_WARRIOR_M)
	chrmgrm2g.SelectRace(RACE_WARRIOR_M)	
	chrmgrm2g.LoadLocalRaceData("warrior_m.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc/warrior/intro/")

	chrmgrm2g.CreateRace(RACE_WARRIOR_W)
	chrmgrm2g.SelectRace(RACE_WARRIOR_W)	
	chrmgrm2g.LoadLocalRaceData("warrior_w.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc2/warrior/intro/")


	##############
	# ASSASSIN
	##############
	chrmgrm2g.CreateRace(RACE_ASSASSIN_W)
	chrmgrm2g.SelectRace(RACE_ASSASSIN_W)
	chrmgrm2g.LoadLocalRaceData("assassin_w.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc/assassin/intro/")

	chrmgrm2g.CreateRace(RACE_ASSASSIN_M)
	chrmgrm2g.SelectRace(RACE_ASSASSIN_M)
	chrmgrm2g.LoadLocalRaceData("assassin_m.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc2/assassin/intro/")


	##############
	# SURA
	##############
	chrmgrm2g.CreateRace(RACE_SURA_M)
	chrmgrm2g.SelectRace(RACE_SURA_M)	
	chrmgrm2g.LoadLocalRaceData("sura_m.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc/sura/intro/")

	chrmgrm2g.CreateRace(RACE_SURA_W)
	chrmgrm2g.SelectRace(RACE_SURA_W)	
	chrmgrm2g.LoadLocalRaceData("sura_w.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc2/sura/intro/")


	##############
	# SHAMAN
	##############
	chrmgrm2g.CreateRace(RACE_SHAMAN_W)
	chrmgrm2g.SelectRace(RACE_SHAMAN_W)
	chrmgrm2g.LoadLocalRaceData("shaman_w.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc/shaman/intro/")

	chrmgrm2g.CreateRace(RACE_SHAMAN_M)
	chrmgrm2g.SelectRace(RACE_SHAMAN_M)
	chrmgrm2g.LoadLocalRaceData("shaman_m.msm")
	SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc2/shaman/intro/")

	if app.ENABLE_WOLFMAN_CHARACTER:
		##############
		# WOLFMAN
		##############
		chrmgrm2g.CreateRace(RACE_WOLFMAN_M)
		chrmgrm2g.SelectRace(RACE_WOLFMAN_M)
		chrmgrm2g.LoadLocalRaceData("wolfman_m.msm")
		SetIntroMotions(chr.MOTION_MODE_GENERAL, "d:/ymir work/pc3/wolfman/intro/")



def __LoadGameSound():
	item.SetUseSoundFileName(item.USESOUND_DEFAULT, "sound/ui/drop.wav")
	item.SetUseSoundFileName(item.USESOUND_ACCESSORY, "sound/ui/equip_ring_amulet.wav")
	item.SetUseSoundFileName(item.USESOUND_ARMOR, "sound/ui/equip_metal_armor.wav")
	item.SetUseSoundFileName(item.USESOUND_BOW, "sound/ui/equip_bow.wav")
	item.SetUseSoundFileName(item.USESOUND_WEAPON, "sound/ui/equip_metal_weapon.wav")
	item.SetUseSoundFileName(item.USESOUND_POTION, "sound/ui/eat_potion.wav")
	item.SetUseSoundFileName(item.USESOUND_PORTAL, "sound/ui/potal_scroll.wav")

	item.SetDropSoundFileName(item.DROPSOUND_DEFAULT, "sound/ui/drop.wav")
	item.SetDropSoundFileName(item.DROPSOUND_ACCESSORY, "sound/ui/equip_ring_amulet.wav")
	item.SetDropSoundFileName(item.DROPSOUND_ARMOR, "sound/ui/equip_metal_armor.wav")
	item.SetDropSoundFileName(item.DROPSOUND_BOW, "sound/ui/equip_bow.wav")
	item.SetDropSoundFileName(item.DROPSOUND_WEAPON, "sound/ui/equip_metal_weapon.wav")

# 이펙트를 대한 설정이다. CInstanceBase클래스의 static DWORD ms_adwCRCAffectEffect[EFFECT_NUM] 이라는 배열에다가 저장해 놓는다.
def __LoadGameEffect():
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_SPAWN_APPEAR, "Bip01", "d:/ymir work/effect/etc/appear_die/monster_appear.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_SPAWN_DISAPPEAR, "Bip01", "d:/ymir work/effect/etc/appear_die/monster_die.mse")		
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_FLAME_ATTACK, "equip_right_hand", "d:/ymir work/effect/hit/blow_flame/flame_3_weapon.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_FLAME_HIT, "", "d:/ymir work/effect/hit/blow_flame/flame_3_blow.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_FLAME_ATTACH, "", "d:/ymir work/effect/hit/blow_flame/flame_3_body.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_ELECTRIC_ATTACK, "equip_right", "d:/ymir work/effect/hit/blow_electric/light_1_weapon.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_ELECTRIC_HIT, "", "d:/ymir work/effect/hit/blow_electric/light_1_blow.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_ELECTRIC_ATTACH, "", "d:/ymir work/effect/hit/blow_electric/light_1_body.mse")
	
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_LEVELUP, "", "d:/ymir work/effect/etc/levelup_1/level_up.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_SKILLUP, "", "d:/ymir work/effect/etc/skillup/skillup_1.mse")

	if localeInfo.IsNEWCIBN():
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMPIRE+1, "Bip01", "locale/newcibn/effect/empire/empire_A.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMPIRE+2, "Bip01", "locale/newcibn/effect/empire/empire_B.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMPIRE+3, "Bip01", "locale/newcibn/effect/empire/empire_C.mse")
	else :
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMPIRE+1, "Bip01", "d:/ymir work/effect/etc/empire/empire_A.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMPIRE+2, "Bip01", "d:/ymir work/effect/etc/empire/empire_B.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMPIRE+3, "Bip01", "d:/ymir work/effect/etc/empire/empire_C.mse")
 
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_WEAPON+1, "equip_right_hand", "d:/ymir work/pc/warrior/effect/geom_sword_loop.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_WEAPON+2, "equip_right_hand", "d:/ymir work/pc/warrior/effect/geom_spear_loop.mse")

	# LOCALE
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+0, "Bip01", localeInfo.FN_GM_MARK)
	# END_OF_LOCALE
	
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_POISON, "Bip01", "d:/ymir work/effect/hit/blow_poison/poison_loop.mse") ## 중독
	
	if app.ENABLE_WOLFMAN_CHARACTER:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_BLEEDING, "Bip01", "d:/ymir work/effect/hit/blow_poison/bleeding_loop.mse") ## 출혈

	if app.ENABLE_12ZI:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_ELECTRIC_SHOCK, "Bip01", "d:/ymir work/effect/monster2/12_pc_damage_elec_01.mse") ## 감전
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_CONFUSION, "Bip01 Head", "d:/ymir work/effect/monster2/12_pc_cant_01.mse") ## 조작불능
				
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_SLOW, "", "d:/ymir work/effect/affect/slow.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_STUN, "Bip01 Head", "d:/ymir work/effect/etc/stun/stun_loop.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_DUNGEON_READY, "", "d:/ymir work/effect/etc/ready/ready.mse")
	#chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_BUILDING_CONSTRUCTION_SMALL, "", "d:/ymir work/guild/effect/10_construction.mse")
	#chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_BUILDING_CONSTRUCTION_LARGE, "", "d:/ymir work/guild/effect/20_construction.mse")
	#chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_BUILDING_UPGRADE, "", "d:/ymir work/guild/effect/20_upgrade.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_CHEONGEUN, "", "d:/ymir work/pc/warrior/effect/gyeokgongjang_loop.mse") ## 천근추 (밑에도 있따-_-)
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_GYEONGGONG, "", "d:/ymir work/pc/assassin/effect/gyeonggong_loop.mse") ## 자객 - 경공
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_GWIGEOM, "Bip01 R Finger2", "d:/ymir work/pc/sura/effect/gwigeom_loop.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_GONGPO, "", "d:/ymir work/pc/sura/effect/fear_loop.mse") ## 수라 - 공포
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_JUMAGAP, "", "d:/ymir work/pc/sura/effect/jumagap_loop.mse") ## 수라 - 주마갑
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_HOSIN, "", "d:/ymir work/pc/shaman/effect/3hosin_loop.mse") ## 무당 - 호신
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_BOHO, "", "d:/ymir work/pc/shaman/effect/boho_loop.mse") ## 무당 - 보호
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_KWAESOK, "", "d:/ymir work/pc/shaman/effect/10kwaesok_loop.mse") ## 무당 - 쾌속
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_HEUKSIN, "", "d:/ymir work/pc/sura/effect/heuksin_loop.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_MUYEONG, "", "d:/ymir work/pc/sura/effect/muyeong_loop.mse")
	
	if app.ENABLE_BALANCE_IMPROVING:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_FIRE, "Bip01", "d:/ymir work/effect/hit/hwayeom_loop_1.mse")
	else:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_FIRE, "Bip01", "d:/ymir work/effect/hit/blow_flame/flame_loop.mse")
		
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_GICHEON, "Bip01 R Hand", "d:/ymir work/pc/shaman/effect/6gicheon_hand.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_JEUNGRYEOK, "Bip01 L Hand", "d:/ymir work/pc/shaman/effect/jeungryeok_hand.mse")

	if app.ENABLE_WOLFMAN_CHARACTER:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_RED_POSSESSION, "Bip01", "d:/ymir work/effect/hit/blow_flame/flame_loop_w.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_BLUE_POSSESSION, "", "d:/ymir work/pc3/common/effect/gyeokgongjang_loop_w.mse")
	
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_PABEOP, "Bip01 Head", "d:/ymir work/pc/sura/effect/pabeop_loop.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_FALLEN_CHEONGEUN, "", "d:/ymir work/pc/warrior/effect/gyeokgongjang_loop.mse") ## 천근추 (Fallen)
	## 34 Polymoph
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_WAR_FLAG1, "", "d:/ymir work/effect/etc/guild_war_flag/flag_red.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_WAR_FLAG2, "", "d:/ymir work/effect/etc/guild_war_flag/flag_blue.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_WAR_FLAG3, "", "d:/ymir work/effect/etc/guild_war_flag/flag_yellow.mse")
	
	if app.ENABLE_BATTLE_FIELD:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_TARGET_VICTIM,		"", "d:/Ymir Work/effect/etc/direction/direction_land_dragonroom.mse")
		
	## SWORD
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+1, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_7.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+2, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_8.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+3, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_9.mse")
	## BOW
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+4, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_7_b.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+5, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_8_b.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+6, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_9_b.mse")
	## FAN
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+7, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_7_f.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+8, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_8_f.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+9, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_9_f.mse")
	## DEGER RIGHT
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+10, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_7_s.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+11, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_8_s.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+12, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_9_s.mse")
	## DEGER LEFT
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+13, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_7_s.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+14, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_8_s.mse")
	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+15, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_9_s.mse")
	
	## 수인족 추가
	if app.ENABLE_WOLFMAN_CHARACTER:
		## CLAW RIGHT
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+16, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_7_w.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+17, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_8_w.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+18, "PART_WEAPON", "D:/ymir work/pc/common/effect/sword/sword_9_w.mse")
		## CLAW LEFT
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+19, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_7_w.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+20, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_8_w.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+21, "PART_WEAPON_LEFT", "D:/ymir work/pc/common/effect/sword/sword_9_w.mse")
		## BODY
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+22, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_7.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+23, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_8.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+24, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_9.mse")
		## BODY SPECIAL
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+25, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-4-2-1.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+26, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-4-2-2.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+27, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-5-1.mse")
	else:
		## BODY
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+16, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_7.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+17, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_8.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+18, "Bip01", "D:/ymir work/pc/common/effect/armor/armor_9.mse")
		## BODY SPECIAL
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+19, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-4-2-1.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+20, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-4-2-2.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_REFINED+21, "Bip01", "D:/ymir work/pc/common/effect/armor/armor-5-1.mse")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_ACCE_BACK, "Bip01", "D:/ymir work/pc/common/effect/armor/acc_01.mse")

	## FlyData
	effect.RegisterIndexedFlyData(effect.FLY_EXP, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_yellow_small2.msf")				## 노란색 (EXP)
	effect.RegisterIndexedFlyData(effect.FLY_HP_MEDIUM, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_red_small.msf")			## 빨간색 (HP) 작은거
	effect.RegisterIndexedFlyData(effect.FLY_HP_BIG, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_red_big.msf")				## 빨간색 (HP) 큰거
	effect.RegisterIndexedFlyData(effect.FLY_SP_SMALL, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_blue_warrior_small.msf")	## 파란색 꼬리만 있는거
	effect.RegisterIndexedFlyData(effect.FLY_SP_MEDIUM, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_blue_small.msf")			## 파란색 작은거
	effect.RegisterIndexedFlyData(effect.FLY_SP_BIG, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_blue_big.msf")				## 파란색 큰거
	effect.RegisterIndexedFlyData(effect.FLY_FIREWORK1, effect.INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_1.msf")		## 폭죽 1
	effect.RegisterIndexedFlyData(effect.FLY_FIREWORK2, effect.INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_2.msf")		## 폭죽 2
	effect.RegisterIndexedFlyData(effect.FLY_FIREWORK3, effect.INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_3.msf")		## 폭죽 3
	effect.RegisterIndexedFlyData(effect.FLY_FIREWORK4, effect.INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_4.msf")		## 폭죽 4
	effect.RegisterIndexedFlyData(effect.FLY_FIREWORK5, effect.INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_5.msf")		## 폭죽 5
	effect.RegisterIndexedFlyData(effect.FLY_FIREWORK6, effect.INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_6.msf")		## 폭죽 6
	effect.RegisterIndexedFlyData(effect.FLY_FIREWORK_XMAS, effect.INDEX_FLY_TYPE_FIRE_CRACKER, "d:/ymir work/effect/etc/firecracker/firecracker_xmas.msf")	## 폭죽 X-Mas
	effect.RegisterIndexedFlyData(effect.FLY_CHAIN_LIGHTNING, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/pc/shaman/effect/pokroe.msf")						## 폭뢰격
	effect.RegisterIndexedFlyData(effect.FLY_HP_SMALL, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/effect/etc/gathering/ga_piece_red_smallest.msf")			## 빨간색 매우 작은거
	effect.RegisterIndexedFlyData(effect.FLY_SKILL_MUYEONG, effect.INDEX_FLY_TYPE_AUTO_FIRE, "d:/ymir work/pc/sura/effect/muyeong_fly.msf")					## 무영진
	if app.ENABLE_QUIVER_SYSTEM:
		effect.RegisterIndexedFlyData(effect.FLY_QUIVER_ATTACK_NORMAL, effect.INDEX_FLY_TYPE_NORMAL, "d:/ymir work/pc/assassin/effect/arrow_02.msf")	    ## 일반 활공격 이펙트 1

	#########################################################################################
	## Emoticon
	EmoticonStr = "d:/ymir work/effect/etc/emoticon/"

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+0, "", EmoticonStr+"sweat.mse")
	m2netm2g.RegisterEmoticonString("(황당)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+1, "", EmoticonStr+"money.mse")
	m2netm2g.RegisterEmoticonString("(돈)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+2, "", EmoticonStr+"happy.mse")
	m2netm2g.RegisterEmoticonString("(기쁨)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+3, "", EmoticonStr+"love_s.mse")
	m2netm2g.RegisterEmoticonString("(좋아)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+4, "", EmoticonStr+"love_l.mse")
	m2netm2g.RegisterEmoticonString("(사랑)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+5, "", EmoticonStr+"angry.mse")
	m2netm2g.RegisterEmoticonString("(분노)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+6, "", EmoticonStr+"aha.mse")
	m2netm2g.RegisterEmoticonString("(아하)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+7, "", EmoticonStr+"gloom.mse")
	m2netm2g.RegisterEmoticonString("(우울)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+8, "", EmoticonStr+"sorry.mse")
	m2netm2g.RegisterEmoticonString("(죄송)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+9, "", EmoticonStr+"!_mix_back.mse")
	m2netm2g.RegisterEmoticonString("(!)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+10, "", EmoticonStr+"question.mse")
	m2netm2g.RegisterEmoticonString("(?)")

	chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_EMOTICON+11, "", EmoticonStr+"fish.mse")
	m2netm2g.RegisterEmoticonString("(fish)")


	## Emoticon
	#########################################################################################

	if app.ENABLE_SOUL_SYSTEM:
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_SOUL_RED, "", "d:/ymir work/effect/etc/soul/soul_red_001.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_SOUL_BLUE, "", "d:/ymir work/effect/etc/soul/soul_blue_001.mse")
		chrmgrm2g.RegisterEffect(chrmgrm2g.EFFECT_AFFECT+chr.AFFECT_SOUL_MIX, "", "d:/ymir work/effect/etc/soul/soul_mix_001.mse")

def __LoadGameWarrior():
	__LoadGameWarriorEx(RACE_WARRIOR_M, "d:/ymir work/pc/warrior/")
	__LoadGameWarriorEx(RACE_WARRIOR_W, "d:/ymir work/pc2/warrior/")

def __LoadGameAssassin():
	__LoadGameAssassinEx(RACE_ASSASSIN_W, "d:/ymir work/pc/assassin/")
	__LoadGameAssassinEx(RACE_ASSASSIN_M, "d:/ymir work/pc2/assassin/")

def __LoadGameSura():
	__LoadGameSuraEx(RACE_SURA_M, "d:/ymir work/pc/sura/")
	__LoadGameSuraEx(RACE_SURA_W, "d:/ymir work/pc2/sura/")

def __LoadGameShaman():
	__LoadGameShamanEx(RACE_SHAMAN_W, "d:/ymir work/pc/shaman/")
	__LoadGameShamanEx(RACE_SHAMAN_M, "d:/ymir work/pc2/shaman/")

def __LoadGameWolfman():
	if app.ENABLE_WOLFMAN_CHARACTER:
		__LoadGameWolfmanEx(RACE_WOLFMAN_M, "d:/ymir work/pc3/wolfman/")

def __LoadGameWolfmanEx(race, path):
	## Wolfman
	#########################################################################################
	chrmgrm2g.SelectRace(race)


	## EMOTION
	emotion.RegisterEmotionAnis(path)

	## GENERAL MOTION MODE
	SetNewGeneralMotions(chr.MOTION_MODE_GENERAL, path + "general/")
	
	chrmgrm2g.SetMotionRandomWeight(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, 0, 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT,            "wait1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT,            "wait2.msa", 20)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1,  "attack1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1,  "attack2.msa", 50)

	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, 1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)

	## SKILL
	chrmgrm2g.SetPathName(path + "skill/")
	for i in xrange(skill.SKILL_EFFECT_COUNT):
		END_STRING = ""
		if i != 0: END_STRING = "_%d" % (i)
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+1, "split_Slash" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+2, "wind_death" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+3, "reef_attack" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+4, "wreckage" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+5, "red_possession" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+6, "blue_possession" + END_STRING + ".msa")

		
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLOOD, "guild_yongsinuipi.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLESS, "guild_yongsinuichukbok.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_BLESSARMOR, "guild_seonghwigap.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_SPPEDUP, "guild_gasokhwa.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONWRATH, "guild_yongsinuibunno.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_MAGICUP, "guild_jumunsul.msa")
	

	## CLAW 
	chrmgrm2g.SetPathName(path + "claw/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_CLAW)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_WAIT,			"wait.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_WAIT,			"wait1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_WAIT,			"wait2.msa", 20)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_WALK,			"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_RUN,			"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_DAMAGE,		"front_damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_DAMAGE,		"front_damage1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_DAMAGE_BACK,	"back_damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_DAMAGE_BACK,	"back_damage1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_COMBO_ATTACK_4, "combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_COMBO_ATTACK_5, "combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_COMBO_ATTACK_6, "combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_CLAW, chr.MOTION_COMBO_ATTACK_7, "combo_07.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_CLAW, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_4)
	


	## FISHING
	chrmgrm2g.SetPathName(path + "fishing/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_FISHING)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WAIT,					"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WALK,					"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_RUN,					"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_THROW,		"throw.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_WAIT,			"fishing_wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_STOP,			"fishing_cancel.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_REACT,		"fishing_react.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_CATCH,		"fishing_catch.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_FAIL,			"fishing_fail.msa")

	## HORSE
	chrmgrm2g.SetPathName(path + "horse/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait.msa", 90)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait1.msa", 9)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait2.msa", 1)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE,			"front_damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE_BACK,		"front_damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_CHARGE,			"skill_charge.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_SPLASH,			"skill_splash.msa")

	## HORSE_CLAW
	chrmgrm2g.SetPathName(path + "horse_claw/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_CLAW)
	#chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait.msa", 90)
	#chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait1.msa", 9)
	#chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait2.msa", 1)
	#chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WALK,				"walk.msa")
	#chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_RUN,				"run.msa")	
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_CLAW, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_CLAW, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_CLAW, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_CLAW, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_CLAW, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_CLAW, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_CLAW, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_CLAW, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)


	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON, "equip_right_weapon")
	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON_LEFT, "equip_left_weapon")
	
def __LoadGameWarriorEx(race, path):

	## Warrior
	#########################################################################################
	chrmgrm2g.SelectRace(race)

	## GENERAL MODE
	SetGeneralMotions(chr.MOTION_MODE_GENERAL, path + "general/")
	chrmgrm2g.SetMotionRandomWeight(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, 0, 70)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait_1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1, "attack.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1, "attack_1.msa", 50)

	## SKILL
	chrmgrm2g.SetPathName(path + "skill/")
	for i in xrange(skill.SKILL_EFFECT_COUNT):
		END_STRING = ""
		if i != 0: END_STRING = "_%d" % (i+1)
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+1, "samyeon" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+2, "palbang" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+3, "jeongwi" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+4, "geomgyeong" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+5, "tanhwan" + END_STRING + ".msa")
		if NEW_678TH_SKILL_ENABLE:
			chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+6, "gihyeol" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+16, "gigongcham" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+17, "gyeoksan" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+18, "daejin" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+19, "cheongeun" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+20, "geompung" + END_STRING + ".msa")
		if NEW_678TH_SKILL_ENABLE:
			chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+21, "noegeom" + END_STRING + ".msa")

	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLOOD, "guild_yongsinuipi.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLESS, "guild_yongsinuichukbok.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_BLESSARMOR, "guild_seonghwigap.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_SPPEDUP, "guild_gasokhwa.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONWRATH, "guild_yongsinuibunno.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_MAGICUP, "guild_jumunsul.msa")

	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, 1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)

	## EMOTION
	emotion.RegisterEmotionAnis(path)

	## ONEHAND_SWORD BATTLE
	chrmgrm2g.SetPathName(path + "onehand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_ONEHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WAIT,				"wait.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WAIT,				"wait_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE,			"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE,			"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE_BACK,		"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE_BACK,		"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_1,	"combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_2,	"combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_3,	"combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_4,	"combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_5,	"combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_6,	"combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_7,	"combo_07.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_4)

	## TWOHAND_SWORD BATTLE
	chrmgrm2g.SetPathName(path + "twohand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_TWOHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_WAIT,				"wait.msa", 70)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_WAIT,				"wait_1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_DAMAGE,			"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_DAMAGE,			"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_DAMAGE_BACK,		"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_DAMAGE_BACK,		"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_1,	"combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_2,	"combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_3,	"combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_4,	"combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_5,	"combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_6,	"combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_7,	"combo_07.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_TWOHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_4)

	## FISHING
	chrmgrm2g.SetPathName(path + "fishing/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_FISHING)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WAIT,			"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WALK,			"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_THROW,	"throw.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_WAIT,	"fishing_wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_STOP,	"fishing_cancel.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_REACT,	"fishing_react.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_CATCH,	"fishing_catch.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_FAIL,	"fishing_fail.msa")

	## HORSE
	chrmgrm2g.SetPathName(path + "horse/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait.msa", 90)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_1.msa", 9)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_2.msa", 1)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE,			"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE_BACK,		"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_CHARGE,			"skill_charge.msa")

	## HORSE_ONEHAND_SWORD
	chrmgrm2g.SetPathName(path + "horse_onehand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_ONEHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, HORSE_SKILL_SPLASH, "skill_splash.msa")

	## HORSE_TWOHAND_SWORD
	chrmgrm2g.SetPathName(path + "horse_twohand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_TWOHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_TWOHAND_SWORD, HORSE_SKILL_SPLASH, "skill_splash.msa")

	## Bone
	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON, "equip_right_hand")

def __LoadGameAssassinEx(race, path):
	## Assassin
	#########################################################################################
	chrmgrm2g.SelectRace(race)

	## GENERAL MOTION MODE
	SetGeneralMotions(chr.MOTION_MODE_GENERAL, path + "general/")
	chrmgrm2g.SetMotionRandomWeight(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, 0, 70)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait_1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1, "attack.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1, "attack_1.msa", 50)

	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, 1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)

	## SKILL
	chrmgrm2g.SetPathName(path + "skill/")
	for i in xrange(skill.SKILL_EFFECT_COUNT):
		END_STRING = ""
		if i != 0: END_STRING = "_%d" % (i+1)
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+1, "amseup" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+2, "gungsin" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+3, "charyun" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+4, "eunhyeong" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+5, "sangong" + END_STRING + ".msa")
		if NEW_678TH_SKILL_ENABLE:
			chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+6, "seomjeon" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+16, "yeonsa" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+17, "gwangyeok" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+18, "hwajo" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+19, "gyeonggong" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+20, "dokgigung" + END_STRING + ".msa")
		if NEW_678TH_SKILL_ENABLE:
			chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+21, "seomgwang" + END_STRING + ".msa")

	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLOOD, "guild_yongsinuipi.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLESS, "guild_yongsinuichukbok.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_BLESSARMOR, "guild_seonghwigap.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_SPPEDUP, "guild_gasokhwa.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONWRATH, "guild_yongsinuibunno.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_MAGICUP, "guild_jumunsul.msa")

	## EMOTION
	emotion.RegisterEmotionAnis(path)

	## ONEHAND_SWORD BATTLE
	chrmgrm2g.SetPathName(path + "onehand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_ONEHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WAIT,		"wait.msa", 70)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WAIT,		"wait_1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WALK,		"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_RUN,		"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE,		"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE,		"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE_BACK,	"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE_BACK,	"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_4, "combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_5, "combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_6, "combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_7, "combo_07.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_4)

	## DUALHAND_SWORD BATTLE
	chrmgrm2g.SetPathName(path + "dualhand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_DUALHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_WAIT,			"wait.msa", 70)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_WAIT,			"wait_1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_WALK,			"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_RUN,			"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_DAMAGE,		"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_DAMAGE,		"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_DAMAGE_BACK,	"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_DAMAGE_BACK,	"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_4, "combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_5, "combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_6, "combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_7, "combo_07.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_8, "combo_08.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_DUALHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_8)

	## BOW BATTLE
	chrmgrm2g.SetPathName(path + "bow/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_BOW)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_WAIT,			"wait.msa", 70)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_WAIT,			"wait_1.msa", 30)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_WALK,			"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_RUN,			"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_DAMAGE,		"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_DAMAGE,		"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_DAMAGE_BACK,	"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_DAMAGE_BACK,	"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BOW, chr.MOTION_COMBO_ATTACK_1,		"attack.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_BOW, COMBO_TYPE_1, 1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BOW, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)

	## FISHING
	chrmgrm2g.SetPathName(path + "fishing/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_FISHING)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WAIT,					"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WALK,					"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_RUN,					"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_THROW,		"throw.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_WAIT,			"fishing_wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_STOP,			"fishing_cancel.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_REACT,		"fishing_react.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_CATCH,		"fishing_catch.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_FAIL,			"fishing_fail.msa")

	## HORSE
	chrmgrm2g.SetPathName(path + "horse/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait.msa", 90)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_1.msa", 9)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_2.msa", 1)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE,			"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE_BACK,		"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_CHARGE, "skill_charge.msa")

	## HORSE_ONEHAND_SWORD
	chrmgrm2g.SetPathName(path + "horse_onehand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_ONEHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, HORSE_SKILL_SPLASH, "skill_splash.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)

	## HORSE_DUALHAND_SWORD
	chrmgrm2g.SetPathName(path + "horse_dualhand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_DUALHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, HORSE_SKILL_SPLASH, "skill_splash.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_DUALHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)

	## HORSE_BOW
	chrmgrm2g.SetPathName(path + "horse_bow/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_BOW)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, chr.MOTION_WAIT,				"wait.msa", 90)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, chr.MOTION_WAIT,				"wait_1.msa", 9)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, chr.MOTION_WAIT,				"wait_2.msa", 1)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, chr.MOTION_DAMAGE,			"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, chr.MOTION_COMBO_ATTACK_1,	"attack.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, HORSE_SKILL_WILDATTACK,		"skill_wildattack.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BOW, HORSE_SKILL_SPLASH,			"skill_splash.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_BOW, COMBO_TYPE_1, 1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_BOW, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)

	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON, "equip_right")
	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON_LEFT, "equip_left")

def __LoadGameSuraEx(race, path):
	## Sura
	#########################################################################################
	chrmgrm2g.SelectRace(race)

	## GENERAL MOTION MODE
	SetGeneralMotions(chr.MOTION_MODE_GENERAL, path + "general/")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1,	"attack.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1,	"attack_1.msa", 50)

	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, 1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)

	## SKILL
	chrmgrm2g.SetPathName(path + "skill/")
	# chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+4, "geongon.msa")

	for i in xrange(skill.SKILL_EFFECT_COUNT):
		END_STRING = ""
		if i != 0: END_STRING = "_%d" % (i+1)
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+1, "swaeryeong" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+2, "yonggwon" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+3, "gwigeom" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+4, "gongpo" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+5, "jumagap" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+6, "pabeop" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+16, "maryeong" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+17, "hwayeom" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+18, "muyeong" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+19, "heuksin" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+20, "tusok" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+21, "mahwan" + END_STRING + ".msa")

	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLOOD, "guild_yongsinuipi.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLESS, "guild_yongsinuichukbok.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_BLESSARMOR, "guild_seonghwigap.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_SPPEDUP, "guild_gasokhwa.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONWRATH, "guild_yongsinuibunno.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_MAGICUP, "guild_jumunsul.msa")

	## EMOTION
	emotion.RegisterEmotionAnis(path)

	## ONEHAND_SWORD BATTLE
	chrmgrm2g.SetPathName(path + "onehand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_ONEHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WAIT,				"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE,			"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE,			"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE,			"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE_BACK,		"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_DAMAGE_BACK,		"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_1,	"combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_2,	"combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_3,	"combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_4,	"combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_5,	"combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_6,	"combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_7,	"combo_07.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_ONEHAND_SWORD, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_4)

	## FISHING
	chrmgrm2g.SetPathName(path + "fishing/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_FISHING)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WAIT,					"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WALK,					"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_RUN,						"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_THROW,			"throw.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_WAIT,			"fishing_wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_STOP,			"fishing_cancel.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_REACT,			"fishing_react.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_CATCH,			"fishing_catch.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_FAIL,			"fishing_fail.msa")

	## HORSE
	chrmgrm2g.SetPathName(path + "horse/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait.msa", 90)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_1.msa", 9)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_2.msa", 1)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE,			"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE_BACK,		"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_CHARGE,			"skill_charge.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_SPLASH,			"skill_splash.msa")

	## HORSE_ONEHAND_SWORD
	chrmgrm2g.SetPathName(path + "horse_onehand_sword/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_ONEHAND_SWORD)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_ONEHAND_SWORD, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")

	## Bone
	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON, "equip_right")

def __LoadGameShamanEx(race, path):
	## Shaman
	#########################################################################################
	chrmgrm2g.SelectRace(race)

	## GENERAL MOTION MODE
	SetGeneralMotions(chr.MOTION_MODE_GENERAL, path + "general/")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1,	"attack.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_COMBO_ATTACK_1,	"attack_1.msa", 50)

	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, 1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_GENERAL, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)

	## EMOTION
	emotion.RegisterEmotionAnis(path)

	## Fan
	chrmgrm2g.SetPathName(path + "fan/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_FAN)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_WAIT,			"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_WALK,			"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_DAMAGE,			"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_DAMAGE,			"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_DAMAGE_BACK,		"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_DAMAGE_BACK,		"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_COMBO_ATTACK_1,	"combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_COMBO_ATTACK_2,	"combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_COMBO_ATTACK_3,	"combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_COMBO_ATTACK_4,	"combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_COMBO_ATTACK_5,	"combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_COMBO_ATTACK_6,	"combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FAN, chr.MOTION_COMBO_ATTACK_7,	"combo_07.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_FAN, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_4)

	## Bell
	chrmgrm2g.SetPathName(path + "Bell/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_BELL)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_WAIT,			"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_WALK,			"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_RUN,			"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_DAMAGE,			"damage.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_DAMAGE,			"damage_1.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_DAMAGE_BACK,	"damage_2.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_DAMAGE_BACK,	"damage_3.msa", 50)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_COMBO_ATTACK_1,	"combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_COMBO_ATTACK_2,	"combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_COMBO_ATTACK_3,	"combo_03.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_COMBO_ATTACK_4,	"combo_04.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_COMBO_ATTACK_5,	"combo_05.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_COMBO_ATTACK_6,	"combo_06.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_BELL, chr.MOTION_COMBO_ATTACK_7,	"combo_07.msa")

	## Combo Type 1
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_1, 4)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_1, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_4)
	## Combo Type 2
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_2, 5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_2, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_2, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_2, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_2, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_2, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_7)
	## Combo Type 3
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_3, 6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_3, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_3, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_3, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_3, COMBO_INDEX_4, chr.MOTION_COMBO_ATTACK_5)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_3, COMBO_INDEX_5, chr.MOTION_COMBO_ATTACK_6)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_BELL, COMBO_TYPE_3, COMBO_INDEX_6, chr.MOTION_COMBO_ATTACK_4)

	## SKILL
	chrmgrm2g.SetPathName(path + "skill/")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+1,		"bipabu.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+2,		"yongpa.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+3,		"paeryong.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+4,		"hosin_target.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+5,	"boho_target.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+6,	"gicheon_target.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+16,	"noejeon.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+17,	"byeorak.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+18,		"pokroe.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+19,		"jeongeop_target.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+20,		"kwaesok_target.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+21,	"jeungryeok_target.msa")
	#chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+10,	"budong.msa")

	START_INDEX = 0
	#skill.SKILL_EFFECT_COUNT 까지//
	for i in (1, 2, 3):
		END_STRING = ""
		if i != 0: END_STRING = "_%d" % (i+1)
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+1,	"bipabu" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+2,	"yongpa" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+3,	"paeryong" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+4,	"hosin" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+5,	"boho" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+6,	"gicheon" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+16,	"noejeon" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+17,	"byeorak" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+18,	"pokroe" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+19,	"jeongeop" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+20,	"kwaesok" + END_STRING + ".msa")
		chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+21,	"jeungryeok" + END_STRING + ".msa")
		#chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SKILL+(i*skill.SKILL_GRADEGAP)+10,	"budong" + END_STRING + ".msa")

	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLOOD, "guild_yongsinuipi.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONBLESS, "guild_yongsinuichukbok.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_BLESSARMOR, "guild_seonghwigap.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_SPPEDUP, "guild_gasokhwa.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_DRAGONWRATH, "guild_yongsinuibunno.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_GENERAL, GUILD_SKILL_MAGICUP, "guild_jumunsul.msa")

	## FISHING
	chrmgrm2g.SetPathName(path + "fishing/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_FISHING)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WAIT,				"wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_RUN,					"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_THROW,		"throw.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_WAIT,		"fishing_wait.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_STOP,		"fishing_cancel.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_REACT,		"fishing_react.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_CATCH,		"fishing_catch.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_FISHING, chr.MOTION_FISHING_FAIL,		"fishing_fail.msa")

	## HORSE
	chrmgrm2g.SetPathName(path + "horse/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait.msa", 90)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_1.msa", 9)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WAIT,				"wait_2.msa", 1)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_WALK,				"walk.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_RUN,				"run.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE,			"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DAMAGE_BACK,		"damage.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, chr.MOTION_DEAD,				"dead.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_CHARGE,			"skill_charge.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE, HORSE_SKILL_SPLASH,			"skill_splash.msa")

	## HORSE_FAN
	chrmgrm2g.SetPathName(path + "horse_fan/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_FAN)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_FAN, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_FAN, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_FAN, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_FAN, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_FAN, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_FAN, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_FAN, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_FAN, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")

	## HORSE_BELL
	chrmgrm2g.SetPathName(path + "horse_bell/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_HORSE_BELL)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BELL, chr.MOTION_COMBO_ATTACK_1, "combo_01.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BELL, chr.MOTION_COMBO_ATTACK_2, "combo_02.msa")
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BELL, chr.MOTION_COMBO_ATTACK_3, "combo_03.msa")
	chrmgrm2g.ReserveComboAttackNew(chr.MOTION_MODE_HORSE_BELL, COMBO_TYPE_1, 3)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_BELL, COMBO_TYPE_1, COMBO_INDEX_1, chr.MOTION_COMBO_ATTACK_1)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_BELL, COMBO_TYPE_1, COMBO_INDEX_2, chr.MOTION_COMBO_ATTACK_2)
	chrmgrm2g.RegisterComboAttackNew(chr.MOTION_MODE_HORSE_BELL, COMBO_TYPE_1, COMBO_INDEX_3, chr.MOTION_COMBO_ATTACK_3)
	chrmgrm2g.RegisterCacheMotionData(chr.MOTION_MODE_HORSE_BELL, HORSE_SKILL_WILDATTACK, "skill_wildattack.msa")

	## Bone
	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON, "equip_right")
	chrmgrm2g.RegisterAttachingBoneName(chr.PART_WEAPON_LEFT, "equip_left")

def __LoadGameSkill():

	try:
		skill.LoadSkillData()
	except:
		import exception
		exception.Abort("__LoadGameSkill")

def __LoadGameEnemy():
	pass

if app.ENABLE_MYSHOP_DECO:
	def __LoadShopDeco():
		try:
			lines = open(app.GetLocalePath()+"/shop_deco.txt", "r").readlines()
		except:
			import exception
			exception.Abort("__LoadShopDeco")
		
		import uiMyShopDecoration
		
		for line in lines:
			tokens = line[:-1].split("\t")
			if len(tokens) == 0 or not tokens[0]:
				continue
				
			if tokens[0] == "#":
				continue
			
			type = int(tokens[0])
			
			if type == 1 :
				uiMyShopDecoration.DECO_SHOP_MODEL_LIST.append([tokens[1], int(tokens[2])])
			elif type == 2 :
				uiMyShopDecoration.DECO_SHOP_TITLE_LIST.append([tokens[1], tokens[2], tokens[3]])
			
def __LoadGameNPC():
	try:
		lines = open("npclist.txt", "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		tokens = line[:-1].split("\t")
		if len(tokens) == 0 or not tokens[0]:
			continue

		try:
			vnum = int(tokens[0])
		except ValueError:
			import dbg
			dbg.LogBox("LoadGameNPC() - %s - line #%d: %s" % (tokens, lines.index(line), line))
			app.Abort()			

		try:
			if vnum:
				chrmgrm2g.RegisterRaceName(vnum, tokens[1].strip())
			else:
				chrmgrm2g.RegisterRaceSrcName(tokens[1].strip(), tokens[2].strip())
		except IndexError:
			import dbg
			dbg.LogBox("LoadGameNPC() - %d, %s - line #%d: %s " % (vnum, tokens, lines.index(line), line))
			app.Abort()
			
def __LoadRaceHeight():
	try:
		lines = open("race_height.txt", "r").readlines()
	except IOError:
		return

	for line in lines:
	
		tokens = line[:-1].split("\t")
		
		if len(tokens) == 0 or not tokens[0]:
			continue

		vnum = int(tokens[0])
		height = float(tokens[1])
		
		chrmgrm2g.SetRaceHeight(vnum, height)


# GUILD_BUILDING
def LoadGuildBuildingList(filename):
	import uiGuild
	uiGuild.BUILDING_DATA_LIST = []
	
	if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
		guild.ClearGuildObjectList()

	handle = app.OpenTextFile(filename)
	count = app.GetTextFileLineCount(handle)
	for i in xrange(count):
		line = app.GetTextFileLine(handle, i)
		tokens = line.split("\t")

		TOKEN_VNUM = 0
		TOKEN_TYPE = 1
		TOKEN_NAME = 2
		TOKEN_LOCAL_NAME = 3
		NO_USE_TOKEN_SIZE_1 = 4
		NO_USE_TOKEN_SIZE_2 = 5
		NO_USE_TOKEN_SIZE_3 = 6
		NO_USE_TOKEN_SIZE_4 = 7
		TOKEN_X_ROT_LIMIT = 8
		TOKEN_Y_ROT_LIMIT = 9
		TOKEN_Z_ROT_LIMIT = 10
		TOKEN_PRICE = 11
		TOKEN_MATERIAL = 12
		TOKEN_NPC = 13
		TOKEN_GROUP = 14
		TOKEN_DEPEND_GROUP = 15
		TOKEN_ENABLE_FLAG = 16
		LIMIT_TOKEN_COUNT = 17

		if not tokens[TOKEN_VNUM].isdigit():
			continue

		if len(tokens) < LIMIT_TOKEN_COUNT:
			import dbg
			dbg.TraceError("Strange token count [%d/%d] [%s]" % (len(tokens), LIMIT_TOKEN_COUNT, line))
			continue

		ENABLE_FLAG_TYPE_NOT_USE = False
		ENABLE_FLAG_TYPE_USE = True
		ENABLE_FLAG_TYPE_USE_BUT_HIDE = 2

		if ENABLE_FLAG_TYPE_NOT_USE == int(tokens[TOKEN_ENABLE_FLAG]):
			continue

		vnum = int(tokens[TOKEN_VNUM])
		type = tokens[TOKEN_TYPE]
		name = tokens[TOKEN_NAME]
		localName = tokens[TOKEN_LOCAL_NAME]
		xRotLimit = int(tokens[TOKEN_X_ROT_LIMIT])
		yRotLimit = int(tokens[TOKEN_Y_ROT_LIMIT])
		zRotLimit = int(tokens[TOKEN_Z_ROT_LIMIT])
		price = tokens[TOKEN_PRICE]
		material = tokens[TOKEN_MATERIAL]

		folderName = ""
		if "HEADQUARTER" == type:
			folderName = "headquarter"
		elif "FACILITY" == type:
			folderName = "facility"
		elif "OBJECT" == type:
			folderName = "object"
		elif "WALL" == type:
			folderName = "fence"

		materialList = ["0", "0", "0"]
		if material:
			if material[0] == "\"":
				material = material[1:]
			if material[-1] == "\"":
				material = material[:-1]
			for one in material.split("/"):
				data = one.split(",")
				if 2 != len(data):
					continue
				itemID = int(data[0])
				count = data[1]

				if itemID == uiGuild.MATERIAL_STONE_ID:
					materialList[uiGuild.MATERIAL_STONE_INDEX] = count
				elif itemID == uiGuild.MATERIAL_LOG_ID:
					materialList[uiGuild.MATERIAL_LOG_INDEX] = count
				elif itemID == uiGuild.MATERIAL_PLYWOOD_ID:
					materialList[uiGuild.MATERIAL_PLYWOOD_INDEX] = count

		## GuildSymbol 은 일반 NPC 들과 함께 등록한다.
		import chrmgrm2g
		chrmgrm2g.RegisterRaceSrcName(name, folderName)
		chrmgrm2g.RegisterRaceName(vnum, name)

		appendingData = { "VNUM":vnum,
						  "TYPE":type,
						  "NAME":name,
						  "LOCAL_NAME":localName,
						  "X_ROT_LIMIT":xRotLimit,
						  "Y_ROT_LIMIT":yRotLimit,
						  "Z_ROT_LIMIT":zRotLimit,
						  "PRICE":price,
						  "MATERIAL":materialList,
						  "SHOW" : True }

		if ENABLE_FLAG_TYPE_USE_BUT_HIDE == int(tokens[TOKEN_ENABLE_FLAG]):
			appendingData["SHOW"] = False

		uiGuild.BUILDING_DATA_LIST.append(appendingData)
		
		if app.ENABLE_SECOND_GUILDRENEWAL_SYSTEM:
			guild.PushBackGuildObjectVnum(vnum)

	app.CloseTextFile(handle)

# END_OF_GUILD_BUILDING

if app.ENABLE_WOLFMAN_CHARACTER:
	loadGameDataDict={
		"INIT" : __InitData,
		"SOUND" : __LoadGameSound,
		"EFFECT" : __LoadGameEffect,
		"WARRIOR" : __LoadGameWarrior,
		"ASSASSIN" : __LoadGameAssassin,
		"SURA" : __LoadGameSura,
		"SHAMAN" : __LoadGameShaman,
		"WOLFMAN" : __LoadGameWolfman,
		"SKILL" : __LoadGameSkill,
		"ENEMY" : __LoadGameEnemy,
		"NPC" : __LoadGameNPC,
	}
else:
	loadGameDataDict={
		"INIT" : __InitData,
		"SOUND" : __LoadGameSound,
		"EFFECT" : __LoadGameEffect,
		"WARRIOR" : __LoadGameWarrior,
		"ASSASSIN" : __LoadGameAssassin,
		"SURA" : __LoadGameSura,
		"SHAMAN" : __LoadGameShaman,
		"SKILL" : __LoadGameSkill,
		"ENEMY" : __LoadGameEnemy,
		"NPC" : __LoadGameNPC,
	}

if app.ENABLE_MYSHOP_DECO:
	loadGameDataDict["SHOP"] = __LoadShopDeco()

loadGameDataDict["RACE_HEIGHT"] = __LoadRaceHeight()
	
def LoadGameData(name):
	global loadGameDataDict

	load=loadGameDataDict.get(name, 0)
	if load:
		loadGameDataDict[name]=0
		try:
			load()
		except:
			print name
			import exception
			exception.Abort("LoadGameData")
			raise


## NPC

def SetMovingNPC(race, name):
	chrmgrm2g.CreateRace(race)
	chrmgrm2g.SelectRace(race)

	## RESERVED
	chrmgrm2g.SetPathName("d:/ymir work/npc/" + name + "/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WALK, "walk.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_RUN, "run.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD, "die.msa")
	chrmgrm2g.LoadRaceData(name + ".msm")

def SetOneNPC(race, name):
	chrmgrm2g.CreateRace(race)
	chrmgrm2g.SelectRace(race)

	## RESERVED
	chrmgrm2g.SetPathName("d:/ymir work/npc/" + name + "/")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait.msa")
	chrmgrm2g.LoadRaceData(name + ".msm")

def SetGuard(race, name):
	chrmgrm2g.CreateRace(race)
	chrmgrm2g.SelectRace(race)

	## Script Data
	chrmgrm2g.SetPathName("d:/ymir work/npc/" + name + "/")
	chrmgrm2g.LoadRaceData(name + ".msm")

	## GENERAL
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_SPAWN,		"00.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT,			"00.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_RUN,			"03.msa")

	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE,		"30.msa", 50)
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE,		"30_1.msa", 50)

	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_BACK,	"34.msa", 50)
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_BACK,	"34_1.msa", 50)

	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_FLYING,"32.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_STAND_UP,		"33.msa")

	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DAMAGE_FLYING_BACK,	"35.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_STAND_UP_BACK,		"36.msa")

	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD,					"31.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD_BACK,			"37.msa")

	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_NORMAL_ATTACK,		"20.msa")

	## Attacking Data
	chrmgrm2g.RegisterNormalAttack(chr.MOTION_MODE_GENERAL, chr.MOTION_NORMAL_ATTACK)

def SetWarp(race):
	chrmgrm2g.CreateRace(race)
	chrmgrm2g.SelectRace(race)

	chrmgrm2g.SetPathName("d:/ymir work/npc/warp/")
	chrmgrm2g.LoadRaceData("warp.msm")

	## GENERAL
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "wait.msa")

def SetDoor(race, name):
	chrmgrm2g.CreateRace(race)
	chrmgrm2g.SelectRace(race)
	chrmgrm2g.SetPathName("d:/ymir work/npc/"+name+"/")
	chrmgrm2g.LoadRaceData(name + ".msm")
	chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_WAIT, "close_wait.msa")
	chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD, "open.msa")

def SetGuildBuilding(race, name, grade):
	chrmgrm2g.CreateRace(race)
	chrmgrm2g.SelectRace(race)
	chrmgrm2g.SetPathName("d:/ymir work/guild/building/%s/" % name)
	chrmgrm2g.LoadRaceData("%s%02d.msm" % (name, grade))
	#chrmgrm2g.RegisterMotionMode(chr.MOTION_MODE_GENERAL)
	#chrmgrm2g.RegisterMotionData(chr.MOTION_MODE_GENERAL, chr.MOTION_DEAD, name + "_destruction.msa")

def OLD_SetNPC():
	SetOneNPC(9001, "arms")
	SetOneNPC(9002, "defence")
	SetOneNPC(9003, "goods")
	SetOneNPC(9004, "bank")
	SetOneNPC(9005, "hotel_grandfa")
	SetOneNPC(9006, "hotel_grandma")
	SetOneNPC(9007, "arms")
	SetOneNPC(9008, "defence")
	SetOneNPC(9009, "sailor")

	SetMovingNPC(20001, "alchemist")
	SetMovingNPC(20002, "auntie")
	SetMovingNPC(20003, "baby_and_mom")
	SetMovingNPC(20004, "beggar")
	SetMovingNPC(20005, "ceramist")
	SetMovingNPC(20006, "girl_lost_elder_brother")
	SetMovingNPC(20007, "hotel_grandfa")
	SetMovingNPC(20008, "mr_restaurant")
	SetMovingNPC(20009, "oldster")
	SetMovingNPC(20010, "peddler")
	SetMovingNPC(20011, "plant_researcher")
	SetMovingNPC(20012, "rice_cake_seller")
	SetMovingNPC(20013, "sailor")
	SetMovingNPC(20014, "timid_boy")
	SetMovingNPC(20015, "woodcutter")
	SetMovingNPC(20016, "blacksmith")
	SetMovingNPC(20017, "musician")
	SetMovingNPC(20018, "doctor")
	SetMovingNPC(20019, "hunter")
	SetMovingNPC(20020, "old_pirate")
	SetMovingNPC(20021, "widow")
	SetMovingNPC(20022, "young_merchant")
	SetMovingNPC(20023, "bookworm")
	SetMovingNPC(20024, "yu_hwa_rang")
	SetMovingNPC(20041, "beggar")
	SetMovingNPC(20042, "peddler")

	SetGuard(20300, "sinsu_patrol_spear")
	SetGuard(20301, "sinsu_patrol_spear")
	SetGuard(20302, "sinsu_patrol_spear")
	SetGuard(20303, "sinsu_patrol_spear")
	SetGuard(20304, "sinsu_patrol_spear")
	SetGuard(20305, "sinsu_patrol_spear")
	SetGuard(20306, "sinsu_patrol_spear")
	SetGuard(20307, "sinsu_patrol_spear")

	SetGuard(20320, "gangyo_patrol_spear")
	SetGuard(20321, "gangyo_patrol_spear")
	SetGuard(20322, "gangyo_patrol_spear")
	SetGuard(20323, "gangyo_patrol_spear")
	SetGuard(20324, "gangyo_patrol_spear")
	SetGuard(20325, "gangyo_patrol_spear")
	SetGuard(20326, "gangyo_patrol_spear")
	SetGuard(20327, "gangyo_patrol_spear")

	SetGuard(20340, "jinno_patrol_spear")
	SetGuard(20341, "jinno_patrol_spear")
	SetGuard(20342, "jinno_patrol_spear")
	SetGuard(20343, "jinno_patrol_spear")
	SetGuard(20344, "jinno_patrol_spear")
	SetGuard(20345, "jinno_patrol_spear")
	SetGuard(20346, "jinno_patrol_spear")
	SetGuard(20347, "jinno_patrol_spear")

	## Warp
	for i in xrange(18):
		SetWarp(10001 + i)

	SetGuard(11000, "gangyo_patrol_spear")
	SetGuard(11001, "gangyo_patrol_bow")
	SetGuard(11002, "jinno_patrol_spear")
	SetGuard(11003, "jinno_patrol_bow")
	SetGuard(11004, "sinsu_patrol_spear")
	SetGuard(11005, "sinsu_patrol_bow")

	## Campfire (Bonfire)
	chrmgrm2g.CreateRace(12000)
	chrmgrm2g.SelectRace(12000)
	chrmgrm2g.SetPathName("d:/ymir Work/npc/campfire/")
	chrmgrm2g.LoadRaceData("campfire.msm")

	## Door
	SetDoor(13000, "wooden_door")
	SetDoor(13001, "stone_door")
