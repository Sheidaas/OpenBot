import app
import constInfo
import background

if app.ENABLE_BATTLE_FIELD:
	import shop

MAP_TRENT02 = "MAP_TRENT02" # �ӽ�
MAP_WL = "MAP_WL" # �ӽ�
MAP_NUSLUCK = "MAP_NUSLUCK" # �ӽ� 
MAP_TREE2 = "MAP_TREE2"

BLEND_POTION_NO_TIME = "BLEND_POTION_NO_TIME"
BLEND_POTION_NO_INFO = "BLEND_POTION_NO_INFO"

APP_TITLE = "METIN2"

GUILD_HEADQUARTER = "Main Building"
GUILD_FACILITY = "Facility"
GUILD_OBJECT = "Object"
GUILD_MEMBER_COUNT_INFINITY = "INFINITY"

LOGIN_FAILURE_WEB_BLOCK = "BLOCK_LOGIN(WEB)"
LOGIN_FAILURE_BLOCK_LOGIN = "BLOCK_LOGIN"
CHANNEL_NOTIFY_FULL = "CHANNEL_NOTIFY_FULL"

GUILD_BUILDING_LIST_TXT = app.GetLocalePath() + "/GuildBuildingList.txt"

GUILD_MARK_MIN_LEVEL = "3"
GUILD_MARK_NOT_ENOUGH_LEVEL = "��巹�� 3�̻� ���� �����մϴ�."

ERROR_MARK_UPLOAD_NEED_RECONNECT = "UploadMark: Reconnect to game"
ERROR_MARK_CHECK_NEED_RECONNECT = "CheckMark: Reconnect to game"

VIRTUAL_KEY_ALPHABET_LOWERS  = r"[1234567890]/qwertyuiop\=asdfghjkl;`'zxcvbnm.,"
VIRTUAL_KEY_ALPHABET_UPPERS  = r'{1234567890}?QWERTYUIOP|+ASDFGHJKL:~"ZXCVBNM<>'
VIRTUAL_KEY_SYMBOLS    = '!@#$%^&*()_+|{}:"<>?~'
VIRTUAL_KEY_NUMBERS    = "1234567890-=\[];',./`"
VIRTUAL_KEY_SYMBOLS_BR    = '!@#$%^&*()_+|{}:"<>?~����������������'

__IS_ENGLISH	= "ENGLISH" == app.GetLocaleServiceName()	
__IS_HONGKONG	= "HONGKONG" == app.GetLocaleServiceName()
__IS_NEWCIBN	= "locale/newcibn" == app.GetLocalePath()
__IS_EUROPE		= "EUROPE" == app.GetLocaleServiceName()		
__IS_CANADA		= "locale/ca" == app.GetLocalePath()
__IS_BRAZIL		= "locale/br" == app.GetLocalePath()
__IS_SINGAPORE	= "locale/sg" == app.GetLocalePath()
__IS_VIETNAM	= "locale/vn" == app.GetLocalePath()
__IS_ARABIC		= "locale/ae" == app.GetLocalePath()
__IS_CIBN10		= "locale/cibn10" == app.GetLocalePath()
__IS_WE_KOREA	= "locale/we_korea" == app.GetLocalePath()
__IS_TAIWAN		= "locale/taiwan" == app.GetLocalePath()
__IS_JAPAN		= "locale/japan" == app.GetLocalePath()	
LOGIN_FAILURE_WRONG_SOCIALID = "ASDF"
LOGIN_FAILURE_SHUTDOWN_TIME = "ASDF"

if __IS_CANADA:
	__IS_EUROPE = True

def IsYMIR():
	return "locale/ymir" == app.GetLocalePath()

def IsJAPAN():
	return "locale/japan" == app.GetLocalePath()

def IsENGLISH():
	global __IS_ENGLISH
	return __IS_ENGLISH

def IsHONGKONG():
	global __IS_HONGKONG
	return __IS_HONGKONG

def IsTAIWAN():
	return "locale/taiwan" == app.GetLocalePath()

def IsNEWCIBN():
	return "locale/newcibn" == app.GetLocalePath()

def IsCIBN10():
	global __IS_CIBN10
	return __IS_CIBN10
	
def IsEUROPE():
	global __IS_EUROPE
	return __IS_EUROPE

def IsCANADA():
	global __IS_CANADA
	return __IS_CANADA

def IsBRAZIL():
	global __IS_BRAZIL
	return __IS_BRAZIL

def IsVIETNAM():
	global __IS_VIETNAM
	return __IS_VIETNAM

def IsSINGAPORE():
	global __IS_SINGAPORE
	return __IS_SINGAPORE
	
def IsARABIC():
	global __IS_ARABIC
	return __IS_ARABIC

def IsWE_KOREA():
	return "locale/we_korea" == app.GetLocalePath()
	
# SUPPORT_NEW_KOREA_SERVER
def LoadLocaleData():
	if IsYMIR():
		import m2netm2g
		SERVER = "�赵 ����"
		if SERVER == m2netm2g.GetServerInfo()[:len(SERVER)]:
			app.SetCHEONMA(0)
			app.LoadLocaleData("locale/we_korea")
			constInfo.ADD_DEF_BONUS_ENABLE = 0
		else:
			app.SetCHEONMA(1)
			app.LoadLocaleData("locale/ymir")
			constInfo.ADD_DEF_BONUS_ENABLE = 1
	else:
		app.LoadLocaleData(app.GetLocalePath())

def IsCHEONMA():
	return IsYMIR()		# ���� YMIR �������� ������ õ��������. õ�������� ���� �ݱ� ������ ���� �� ����.

# END_OF_SUPPORT_NEW_KOREA_SERVER

def mapping(**kwargs): return kwargs

def SNA(text):	
	def f(x):
		return text
	return f

def SA(text):
	def f(x):
		return text % x
	return f
	
def SAA(text):
	def f(x1, x2):
		return text % (x1, x2)
	return f

def SAN(text):
	def f(x1, x2):
		return text % x1
	return f
	
def LoadLocaleFile(srcFileName, localeDict):

	funcDict = {"SA":SA, "SNA":SNA, "SAA":SAA, "SAN":SAN}

	lineIndex = 1

	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		try:		
			tokens = line[:-1].split("\t")
			if len(tokens) == 2:
				localeDict[tokens[0]] = tokens[1]
			elif len(tokens) >= 3:
				type = tokens[2].strip()
				if type:
					localeDict[tokens[0]] = funcDict[type](tokens[1])
				else:
					localeDict[tokens[0]] = tokens[1]
			else:
				raise RuntimeError, "Unknown TokenSize"

			lineIndex += 1
		except:
			import dbg
			dbg.LogBox("%s: line(%d): %s" % (srcFileName, lineIndex, line), "Error")
			raise


	
all = ["locale","error"]

if IsEUROPE()  and  IsBRAZIL()  :
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()
	constInfo.IN_GAME_SHOP_ENABLE = 0
elif IsSINGAPORE() :
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()
	constInfo.IN_GAME_SHOP_ENABLE = 0
elif IsNEWCIBN() :
	##���Ӹ��̱�����.
	APP_TITLE = "������2"
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()
	constInfo.IN_GAME_SHOP_ENABLE = 1
elif IsTAIWAN():
	APP_TITLE = "��III��"
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()

	constInfo.IN_GAME_SHOP_ENABLE = 1
	
else:
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()

	constInfo.IN_GAME_SHOP_ENABLE = 1

LoadLocaleFile(LOCALE_FILE_NAME, locals())

########################################################################################################
## NOTE : �������� ������ "������/�� �����ðڽ��ϱ�?" ���ڿ��� ���� ������ ���� �ڵ�
dictSingleWord = {
	"m":1, "n":1, "r":1, "M":1, "N":1, "R":1, "l":1, "L":1, "1":1, "3":1, "6":1, "7":1, "8":1, "0":1,
}

dictDoubleWord = {
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "�v":1, "��":1, "��":1, "��":1, "�R":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "�x":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "�m":1, "��":1, "��":1, "��":1, "�O":1, "��":1, "��":1, "��":1, "��":1, "�l":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "�u":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "�X":1, "��":1, "��":1, "��":1, "��":1, "��":1, "�o":1, "��":1, "��":1, "��":1, "�y":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "�p":1,
	"¥":1, "¹":1, "¼":1, "��":1, "��":1, "�c":1, "��":1, "��":1, "��":1, "��":1, "°":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "�R":1, "��":1, "��":1, "�n":1,
	"��":1, "í":1, "ó":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "ġ":1, "ä":1, "��":1, "ü":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "�M":1,
	"ī":1, "ļ":1, "Ŀ":1, "��":1, "��":1, "��":1, "��":1, "ť":1, "ũ":1, "Ű":1, "ĳ":1, "�m":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1,
	"Ÿ":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "Ʃ":1, "Ʈ":1, "Ƽ":1, "��":1, "�O":1, "��":1, "��":1, "��":1, "��":1, "��":1, "ơ":1, "��":1, "Ƣ":1, "Ʒ":1,
	"��":1, "��":1, "��":1, "��":1, "��":1, "ǥ":1, "Ǫ":1, "ǻ":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "ǡ":1, "��":1, "Ǵ":1, "�R":1, "ǣ":1, "Ƕ":1, "�c":1,
	"��":1, "��":1, "��":1, "��":1, "ȣ":1, "ȿ":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "��":1, "ȭ":1, "ȳ":1, "��":1, "��":1, "ȸ":1, "��":1, "��":1,
}

locale = mapping(
)


def GetAuxiliaryWordType(text):

	textLength = len(text)

	if textLength > 1:

		singleWord = text[-1]

		if (singleWord >= '0' and singleWord <= '9') or\
			(singleWord >= 'a' and singleWord <= 'z') or\
			(singleWord >= 'A' and singleWord <= 'Z'):
			if not dictSingleWord.has_key(singleWord):
				return 1

		elif dictDoubleWord.has_key(text[-2:]):
			return 1

	return 0



def CutMoneyString(sourceText, startIndex, endIndex, insertingText, backText):

	sourceLength = len(sourceText)

	if sourceLength < startIndex:
		return backText

	text = sourceText[max(0, sourceLength-endIndex):sourceLength-startIndex]

	if not text:
		return backText

	if int(text) <= 0:
		return backText

	text = str(int(text))

	if backText:
		backText = " " + backText

	return text + insertingText + backText
	
if app.ENABLE_GEM_SYSTEM:
	def SecondToHMGolbal(time):
		if time < 60:
			return "00:01"

		minute = int((time / 60) % 60)
		hour = int((time / 60) / 60)

		text = ""

		if hour > 0:
			if hour >= 10:
				text += str(hour) + ":"
			else:
				text += "0" + str(hour) + ":"
		else:
			text += "00:"

		if minute > 0:
			if minute >= 10:
				text += str(minute)
			else:
				text += "0" + str(minute)

		return text


def SecondToDHM(time):
	if time < 60:
		if IsARABIC():
			return "%.2f %s" % (time, SECOND)
		else:
			return "0" + MINUTE
		
	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60) % 24
	day = int(int((time / 60) / 60) / 24)

	text = ""

	if day > 0:
		text += str(day) + DAY
		text += " "

	if hour > 0:
		text += str(hour) + HOUR
		text += " "

	if minute > 0:
		text += str(minute) + MINUTE

	return text

def SecondToHM(time):

	if time < 60:
		if IsARABIC():
			return "%.2f %s" % (time, SECOND)
		else:
			return "0" + MINUTE

	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60)

	text = ""

	if hour > 0:
		text += str(hour) + HOUR
		if hour > 0:
			text += " "

	if minute > 0:
		text += str(minute) + MINUTE

	return text
	
if app.ENABLE_GROWTH_PET_SYSTEM:
	def SecondToDay(time):
		if time < 60:
			return "1" + DAY
			
		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int((time / 60) / 60) % 24
		day = int(int((time / 60) / 60) / 24)
		
		if day < 1:
			day = 1
			
		if day > 9999:
			day = 9999
			
		text = str(day) + DAY
		return text
		
if app.ENABLE_GROWTH_PET_SYSTEM:		
	def SecondToDayNumber(time):
		if time < 60:
			return 1
			
		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int((time / 60) / 60) % 24
		day = int(int((time / 60) / 60) / 24)
		
		if day < 1:
			day = 1
			
		if day > 9999:
			day = 9999
			
		return day
	
if app.ENABLE_GROWTH_PET_SYSTEM:
	def SecondToH(time):			
		hour = int((time / 60) / 60)

		text = ""
		hour = max( 0, hour )
		text += str(hour)

		return text

if app.ENABLE_BATTLE_FIELD:
	def SecondToColonTypeHM(time):			
		if time < 60:
			return "00:00"

		minute = int((time / 60) % 60)
		hour = int((time / 60) / 60)

		return "%02d:%02d" % (hour, minute)
		
if app.ENABLE_GUILD_DRAGONLAIR_PARTY_SYSTEM or app.ENABLE_12ZI:
	def SecondToColonTypeHMS(time):			
		if time < 60:
			return "00:00:%02d" % (time)

		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int((time / 60) / 60)

		return "%02d:%02d:%02d" % (hour, minute, second)

	def SecondToColonTypeMS(time):
	
		second = int(time % 60)
		minute = int((time / 60) % 60)

		return "%02d:%02d" % (minute, second)
		
def GetAlignmentTitleName(alignment):
	if alignment >= 12000:
		return TITLE_NAME_LIST[0]
	elif alignment >= 8000:
		return TITLE_NAME_LIST[1]
	elif alignment >= 4000:
		return TITLE_NAME_LIST[2]
	elif alignment >= 1000:
		return TITLE_NAME_LIST[3]
	elif alignment >= 0:
		return TITLE_NAME_LIST[4]
	elif alignment > -4000:
		return TITLE_NAME_LIST[5]
	elif alignment > -8000:
		return TITLE_NAME_LIST[6]
	elif alignment > -12000:
		return TITLE_NAME_LIST[7]

	return TITLE_NAME_LIST[8]


OPTION_PVPMODE_MESSAGE_DICT = {
	0 : PVP_MODE_NORMAL,
	1 : PVP_MODE_REVENGE,
	2 : PVP_MODE_KILL,
	3 : PVP_MODE_PROTECT,
	4 : PVP_MODE_GUILD,
}

error = mapping(
	CREATE_WINDOW = GAME_INIT_ERROR_MAIN_WINDOW,
	CREATE_CURSOR = GAME_INIT_ERROR_CURSOR,
	CREATE_NETWORK = GAME_INIT_ERROR_NETWORK,
	CREATE_ITEM_PROTO = GAME_INIT_ERROR_ITEM_PROTO,
	CREATE_MOB_PROTO = GAME_INIT_ERROR_MOB_PROTO,
	CREATE_NO_DIRECTX = GAME_INIT_ERROR_DIRECTX,
	CREATE_DEVICE = GAME_INIT_ERROR_GRAPHICS_NOT_EXIST,
	CREATE_NO_APPROPRIATE_DEVICE = GAME_INIT_ERROR_GRAPHICS_BAD_PERFORMANCE,
	CREATE_FORMAT = GAME_INIT_ERROR_GRAPHICS_NOT_SUPPORT_32BIT,
	NO_ERROR = ""
)


GUILDWAR_NORMAL_DESCLIST = [GUILD_WAR_USE_NORMAL_MAP, GUILD_WAR_LIMIT_30MIN, GUILD_WAR_WIN_CHECK_SCORE]
GUILDWAR_WARP_DESCLIST = [GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_WIPE_OUT_GUILD, GUILD_WAR_REWARD_POTION]
GUILDWAR_CTF_DESCLIST = [GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_TAKE_AWAY_FLAG1, GUILD_WAR_WIN_TAKE_AWAY_FLAG2, GUILD_WAR_REWARD_POTION]

MINIMAP_ZONE_NAME_DICT = {
	"metin2_map_a1"  : MAP_A1,
	"map_a2"         : MAP_A2,
	"metin2_map_a3"  : MAP_A3,
	"metin2_map_b1"  : MAP_B1,
	"map_b2"         : MAP_B2,
	"metin2_map_b3"  : MAP_B3,
	"metin2_map_c1"  : MAP_C1,
	"map_c2"         : MAP_C2,
	"metin2_map_c3"  : MAP_C3,
	"map_n_snowm_01" : MAP_SNOW,
	"metin2_map_n_flame_01" : MAP_FLAME,
	"metin2_map_n_desert_01" : MAP_DESERT,
	"metin2_map_milgyo" : MAP_TEMPLE,
	"metin2_map_spiderdungeon" : MAP_SPIDER,
	"metin2_map_deviltower1" : MAP_SKELTOWER,
	"metin2_map_guild_01" : MAP_AG,
	"metin2_map_guild_02" : MAP_BG,
	"metin2_map_guild_03" : MAP_CG,
	"metin2_map_trent" : MAP_TREE,
	"metin2_map_trent02" : MAP_TREE2,
	"season1/metin2_map_WL_01" : MAP_WL,
	"season1/metin2_map_nusluck01" : MAP_NUSLUCK,
    "Metin2_map_CapeDragonHead" : MAP_CAPE,
    "metin2_map_Mt_Thunder" : MAP_THUNDER,
    "metin2_map_dawnmistwood" : MAP_DAWN,
    "metin2_map_BayBlackSand" : MAP_BAY,
}

if app.WJ_SHOW_PARTY_ON_MINIMAP or app.ENABLE_MONSTER_CARD or app.ENABLE_PARTY_MATCH:
	MINIMAP_ZONE_NAME_DICT_BY_IDX = {
		0 : "",
		1 : MAP_A1,
		3 : MAP_A3,
		4 : MAP_GUILD_01,
		5 : MAP_MONKEY_DUNGEON_11,
		6 : GUILD_VILLAGE_01,
		21 : MAP_B1,
		23 : MAP_B3,
		24 : MAP_GUILD_02,
		25 : MAP_MONKEY_DUNGEON_12,
		26 : GUILD_VILLAGE_02,
		41 : MAP_C1,
		43 : MAP_C3,
		44 : MAP_GUILD_03,
		45 : MAP_MONKEY_DUNGEON_13,
		46 : GUILD_VILLAGE_03,
		61 : MAP_N_SNOWM_01,
		62 : MAP_N_FLAME_01,
		63 : MAP_N_DESERT_01,
		64 : MAP_N_THREEWAY,
		65 : MAP_MILGYO,
		66 : MAP_DEVILTOWER1,
		67 : MAP_TRENT,
		68 : MAP_TRENT02,
		69 : MAP_WL_01,
		70 : MAP_NUSLUCK01,
		71 : MAP_SPIDERDUNGEON_02,
		72 : MAP_SKIPIA_DUNGEON_01,
		73 : MAP_SKIPIA_DUNGEON_02,
		74 : MAP_N_SNOWM_02,
		75 : MAP_N_FLAME_02,
		76 : MAP_N_DESERT_02,
		77 : MAP_A2_1,
		78 : MAP_MILGYO_A,
		79 : MAP_TRENT_A,
		80 : MAP_TRENT02_A,
		81 : MAP_WEDDING_01,
		91 : MAP_E,
		92 : MAP_E,
		93 : MAP_E,
		103 : MAP_T1,
		104 : MAP_SPIDERDUNGEON,
		105 : MAP_T2,
		107 : MAP_MONKEY_DUNGEON,
		108 : MAP_MONKEY_DUNGEON2,
		109 : MAP_MONKEY_DUNGEON3,
		110 : MAP_T3,
		111 : MAP_T4,
		112 : MAP_DUEL,
		113 : MAP_OXEVENT,
		114 : MAP_SUNGZI,
		118 : MAP_SUNGZI_FLAME_HILL_01,
		119 : MAP_SUNGZI_FLAME_HILL_02,
		120 : MAP_SUNGZI_FLAME_HILL_03,
		121 : MAP_SUNGZI_SNOW,
		122 : MAP_SUNGZI_SNOW_PASS01,
		123 : MAP_SUNGZI_SNOW_PASS02,
		124 : MAP_SUNGZI_SNOW_PASS03,
		125 : MAP_SUNGZI_DESERT_01,
		126 : MAP_SUNGZI_DESERT_HILL_01,
		127 : MAP_SUNGZI_DESERT_HILL_02,
		128 : MAP_SUNGZI_DESERT_HILL_03,
		130 : GUILD_WAR1,
		131 : GUILD_WAR2,
		132 : GUILD_WAR3,
		133 : GUILD_WAR4,
		180 : METIN_TEST,
		181 : MAP_EMPIREWAR01,
		182 : MAP_EMPIREWAR02,
		183 : MAP_EMPIREWAR03,
		184 : MAP_SKIPIA_DUNGEON_011,
		185 : MAP_SKIPIA_DUNGEON_021,
		186 : MAP_SKIPIA_DUNGEON_012,
		187 : MAP_SKIPIA_DUNGEON_022,
		188 : MAP_SKIPIA_DUNGEON_013,
		189 : MAP_SKIPIA_DUNGEON_023,
		193 : MAP_SPIDERDUNGEON_02_1,
		194 : MAP_HOLYPLACE_FLAME,
		195 : MAP_PATHWAY_FLAME_01,
		196 : MAP_PATHWAY_FLAME_02,
		197 : MAP_PATHWAY_FLAME_03,
		198 : MAP_HOLYPLACE_ICE,
		199 : MAP_PATHWAY_ICE_01,
		200 : MAP_PATHWAY_ICE_02,
		201 : MAP_PATHWAY_ICE_03,
		202 : MAP_HOLYPLACE_DESERT,
		203 : MAP_PATHWAY_DESERT_01,
		204 : MAP_PATHWAY_DESERT_02,
		205 : MAP_PATHWAY_DESERT_03,
		208 : MAP_SKIPIA_DUNGEON_BOSS,
		209 : MAP_SKIPIA_DUNGEON_BOSS_1,
		210 : MAP_SKIPIA_DUNGEON_BOSS_2,
		211 : MAP_SKIPIA_DUNGEON_BOSS_3,
		216 : MAP_DEVILCATACOMB,
		217 : MAP_SPIDERDUNGEON_03,
		301 : MAP_CAPEDRAGONHEAD,
		302 : MAP_DAWNMISTWOOD,
		303 : MAP_BAYBLACKSAND,
		304 : MAP_MT_THUNDER,
		351 : MAP_N_FLAME_DUNGEON_01,
		352 : MAP_N_SNOW_DUNGEON_01,
	}
	if background.IsMapInfoByMapName("metin2_map_dawnmist_dungeon_01"):
		MINIMAP_ZONE_NAME_DICT_BY_IDX[353] = MAP_DAWNMIST_DUNGEON_01
	if background.IsMapInfoByMapName("metin2_map_Mt_Th_dungeon_01"):
		MINIMAP_ZONE_NAME_DICT_BY_IDX[354] = MAP_MT_TH_DUNGEON_01
	if background.IsMapInfoByMapName("metin2_map_n_flame_dragon"):
		MINIMAP_ZONE_NAME_DICT_BY_IDX[356] = MAP_N_FLAME_DRAGON
	if background.IsMapInfoByMapName("metin2_map_battlefied"):
		MINIMAP_ZONE_NAME_DICT_BY_IDX[357] = MAP_BATTLE_FIELD
	if background.IsMapInfoByMapName("metin2_12zi_stage"):
		MINIMAP_ZONE_NAME_DICT_BY_IDX[355] = MAP_CZ_DUNGEON

# ĳ����â���� ĳ������ �󱼿� ���콺 ���� ���� �� ������ ������ �� �� JOB_TITLE
if app.ENABLE_WOLFMAN_CHARACTER:
	JOBINFO_TITLE = [
		[JOB_WARRIOR0, JOB_WARRIOR1, JOB_WARRIOR2,],
		[JOB_ASSASSIN0, JOB_ASSASSIN1, JOB_ASSASSIN2,],
		[JOB_SURA0, JOB_SURA1, JOB_SURA2,],
		[JOB_SHAMAN0, JOB_SHAMAN1, JOB_SHAMAN2,],
		[JOB_WOLFMAN0, JOB_WOLFMAN1, JOB_WOLFMAN1,],
	]
else:
	JOBINFO_TITLE = [
		[JOB_WARRIOR0, JOB_WARRIOR1, JOB_WARRIOR2,],
		[JOB_ASSASSIN0, JOB_ASSASSIN1, JOB_ASSASSIN2,],
		[JOB_SURA0, JOB_SURA1, JOB_SURA2,],
		[JOB_SHAMAN0, JOB_SHAMAN1, JOB_SHAMAN2,],
	]


# ĳ����â���� ĳ������ �󱼿� ���콺 ���� ���� �� ������ ����.
JOBINFO_DATA_LIST = [
	[
		["Ÿ�� ��Ͱ� ������ �ʴ� ������",
		"�ⰳ�� ������� ���þ� [����]���",
		"�θ���. ��� ���⿡���� �׵��� ",
		"�ڷ� �������� ������, ��ġ�� ����",
		"�̱� ���� ���Ḧ ���� �ܽ�����",
		"����� ���� �ο�⵵ �Ѵ�. �̵���",
		"�� �ܷõ� ������ ��, ������ ���ݷ�",
		"���� ���� �ּ��ο��� ����������",
		"Ȱ���Ѵ�.                      ",],
		["���� �Ϲ����� ������ �����, ",
		"�������� ���� ���� �������� ����",
		"���� Ȱ���Ѵ�. ���� Ư���� �ٷ���",
		"�������� ���� ����Ʈ�� �����ϵ�, ",
		"�������� ���� ����� / ����",
		"Ȯ���� ���� ü���� �ø���. ����",
		"������ ��Ȯ���� ���̱� ���� ��ø",
		"���� ����Ʈ�� ������ �ʿ䰡 �ִ�.",],
		["��� ������ ���ŷ��� �̿��ϴ�",
		"��/�ٰŸ� ������ �����, �� ���",
		"�ϳ��ϳ��� ���� ���ݷ����� ���忡��",
		"Ȱ���Ѵ�. ���� Ư���� �ٷ��� ����",
		"���� ���� ����Ʈ�� �����ϵ�, ",
		"��/�ٰŸ� ������ ��Ȯ���� ���߷���",
		"���� ��ø�� �ø���. ���� ���� �� ",
		"�� ���ݿ� ���� ����� / ����",
		"Ȯ���� ���� ü�¿��� ����Ʈ��",
		"������ �ʿ䰡 �ִ�.        ",],		
	],
	[
		["�ڰ��� ��� ��Ȳ������ �ڽ���",
		"���� ����� ������ ����� �ӹ���",
		"�����ϸ鼭 ������ ������ �����ϴ�", 
		"�ڵ��̴�. �̵��� ���� ������ �ż�",
		"�ϸ�, ���� �� ���� �����ϰ� ������",
		"�ൿ���� ���� �޼ҿ� ġ��Ÿ�� ����",
		"��, ���忡�� ������ ���� ������",
		"ȭ���� �������� �ڽ��� �����",
		"�����δ�.                   "],
		["�μ� �ܰ��� �ֹ���� �ٷ��, �ż�",
		"�ϰ� ġ�� ������ �ڰ� Ư���� ������",
		"���� ���忡�� Ȱ���Ѵ�. ���� Ư����",
		"��ø�� �������� ���� ����Ʈ�� ����",
		"�ϵ�, �ٷ��� �÷� ���ݷ��� ���δ�.",
		"���� �������� ���� �����/���� ",
		"����� ���� ü�¿��� ����Ʈ��",
		"������ �ʿ䰡 �ִ�.          ",],
		["Ȱ�� �ֹ���� �ٷ��, �� �þ߿�",
		"�����Ÿ��� ���� ���Ÿ� ��������",
		"���忡�� Ȱ���Ѵ�. ���� Ư����",
		"���� �������� ������ ���� ��ø��",
		"�������� �÷��� �ϸ�, ���Ÿ�",
		"������ ������ ������ ���� �ٷ���",
		"�ø� �ʿ䰡 �ִ�. ���� ���鿡��",
		"�����Ǿ��� ��, �� ���ݿ� ��Ƽ��",
		"���� �����/���� ����� ����",
		"ü�¿��� ����Ʈ�� ������ �ʿ䰡",
		"�ִ�.                        ", ],
	],
	[
		["����� [���� ������]�� �Ӽ�����",
		"â���� Ư�� �Ӽ��� �����̴�. ",
		"�׵��� ���忡�� ������ ��⸦ ����",
		"��Ű��, �Ǹ��� ���� ���� ��ź����",
		"���� ��ȥ�� ������ ��������. ����",
		"�̵��� �ڽ��� �˰� ���ʿ� �����",
		"���� �Ǿ�, ���忡�� ���� ���� ����",
		"���ݷ��� �����ϱ⵵ �ϴµ�, ������",
		"�׿���±� ����� ������ ������",
		"������� ���� ���þ� [����]�̶�",
		"�θ��⸦ ���� �ɴ´�."],
		["ȯ������ ����� �Ǹ��� ������",
		"������� ������ ���⳪ ����",
		"�Ǿ� ���� ���� ���� ����������",
		"���忡�� Ȱ���Ѵ�. ���� Ư����",
		"������ ���������� ���� ���", 
		"�Ǹ��� ������ ������ ����ǹǷ�,",
		"���ɰ� �ٷ��� �������� ����",
		"����Ʈ�� �����ϵ�, ������ ����",
		"�����/���� Ȯ���� ���� ü����",
		"�ø���. ���� ������ ��Ȯ����",
		"ȸ�Ǹ� ���ؼ� ��ø���� ����Ʈ��",
		"������ �ʿ䰡 �ִ�.           ",],
		["�渶���� ������� ���� �����",
		"�ֹ��� �Ǹ��� �������� ���忡��",
		"Ȱ���Ѵ�. ���� Ư���� ���� ������",
		"���̹Ƿ� ������ �������� ����",
		"����Ʈ�� �����ϵ�, ���Ÿ� ����",
		"������ ��Ȯ���� ���� ��ø�� �ø���.",
		"���� ���� �Ǿ�����, �� ���ݿ� ����",
		"����� / ���� Ȯ���� ���� ü�¿���",
		"����Ʈ�� ������ �ʿ䰡 �ִ�.    ",],
	],
	[
		["������ ��Ű� �ڿ�, �� �����",
		"���� �ٷ� �� �ִ� ������ �����̴�.",
		"�׵��� �Ĺ濡�� �Ʊ��� �����ϰ�",
		"��ģ ������ �λ��� ȸ�� ��Ű��",
		"������ ��⸦ ��½�Ų��. �׵���",
		"�Ʊ��� ����� �޽��� �����ϴ� �ڸ� ",
		"���� �뼭���� ������, �׷� �ڵ�",
		"���Դ� �� �� ���� ���� �ֹ���",
		"��Ʈ�� �� ������� ���� ¡���Ѵ�.",],
		["õ�決�� ������� ���� ��������",
		"�����ֹ��� ���ϸ�, ���� �� / ����",
		"�������κ��� �Ʊ��� ��Ų��. ����",
		"Ư���� ���� �ɷ��� ���̹Ƿ� ������",
		"�������� ���� ����Ʈ�� �����ϵ�,",
		"�����Ǿ��� ��, �� ���ݿ� ����",
		"����� / ���� Ȯ���� ���� ü����",
		"�ø���. ���� ���Ÿ� ���� ������",
		"��Ȯ���� ���� ��ø���� ����Ʈ��",
		"������ �ʿ䰡 �ִ�.           ",],
		["���ڱ��� ������� �ڿ��� ����",
		"���� �Ʊ��� ȸ���ϰ�, ������ ",
		"������ ������ ���鿡�� ū �����",
		"���� �� �ִ� �̵��̴�. ������",
		"Ư���� ���� �ɷ��� ���̹Ƿ� ������",
		"�������� ���� ����Ʈ�� �����ϵ�,",
		"�����Ǿ�����, �� ���ݿ� ����",
		"����� / ���� Ȯ���� ���� ü����",
		"�ø���. ���� ���Ÿ� ���� ������",
		"��Ȯ���� ���� ��ø���� ����Ʈ��",
		"������ �ʿ䰡 �ִ�.             "],
	],
	[
		["����",],
		["������ [���ǿ� ��]�� �Ӽ�����",
		"â���� �� Ư�� �����̴�.",
		"�׵��� ���忡�� ������ ����, ��������",
		"��⸦ ���Ͻ�Ű�� ������ ���� �߱��.",
		"���δ� �ڽŵ��� ���� ������ ��ȥ�� �̾�",
		"�޾�, ���忡�� ���縦 �ʿ��ϴ� ��������",
		"���ݷ��� �����ϱ⵵ �ϴµ�, ������ ��",
		"����� ��� [���]�� ��� [���]�̶�",
		"�θ��⵵ �Ѵ�."],
		["�ش����"],
	],
]


WHISPER_ERROR = {
	1 : CANNOT_WHISPER_NOT_LOGON,
	2 : CANNOT_WHISPER_DEST_REFUSE,
	3 : CANNOT_WHISPER_SELF_REFUSE,
}

NOTIFY_MESSAGE = {
	"CANNOT_EQUIP_SHOP" : CANNOT_EQUIP_IN_SHOP,
	"CANNOT_EQUIP_EXCHANGE" : CANNOT_EQUIP_IN_EXCHANGE,
}


ATTACK_ERROR_TAIL_DICT = {
	"IN_SAFE" : CANNOT_ATTACK_SELF_IN_SAFE,
	"DEST_IN_SAFE" : CANNOT_ATTACK_DEST_IN_SAFE,
}

SHOT_ERROR_TAIL_DICT = {
	"EMPTY_ARROW" : CANNOT_SHOOT_EMPTY_ARROW,
	"IN_SAFE" : CANNOT_SHOOT_SELF_IN_SAFE,
	"DEST_IN_SAFE" : CANNOT_SHOOT_DEST_IN_SAFE,
}

USE_SKILL_ERROR_TAIL_DICT = {	
	"IN_SAFE" : CANNOT_SKILL_SELF_IN_SAFE,
	"NEED_TARGET" : CANNOT_SKILL_NEED_TARGET,
	"NEED_EMPTY_BOTTLE" : CANNOT_SKILL_NEED_EMPTY_BOTTLE,
	"NEED_POISON_BOTTLE" : CANNOT_SKILL_NEED_POISON_BOTTLE,
	"REMOVE_FISHING_ROD" : CANNOT_SKILL_REMOVE_FISHING_ROD,
	"NOT_YET_LEARN" : CANNOT_SKILL_NOT_YET_LEARN,
	"NOT_MATCHABLE_WEAPON" : CANNOT_SKILL_NOT_MATCHABLE_WEAPON,
	"WAIT_COOLTIME" : CANNOT_SKILL_WAIT_COOLTIME,
	"NOT_ENOUGH_HP" : CANNOT_SKILL_NOT_ENOUGH_HP,
	"NOT_ENOUGH_SP" : CANNOT_SKILL_NOT_ENOUGH_SP,
	"CANNOT_USE_SELF" : CANNOT_SKILL_USE_SELF,
	"ONLY_FOR_ALLIANCE" : CANNOT_SKILL_ONLY_FOR_ALLIANCE,
	"CANNOT_ATTACK_ENEMY_IN_SAFE_AREA" : CANNOT_SKILL_DEST_IN_SAFE,
	"CANNOT_APPROACH" : CANNOT_SKILL_APPROACH,
	"CANNOT_ATTACK" : CANNOT_SKILL_ATTACK,
	"ONLY_FOR_CORPSE" : CANNOT_SKILL_ONLY_FOR_CORPSE,
	"EQUIP_FISHING_ROD" : CANNOT_SKILL_EQUIP_FISHING_ROD, 
	"NOT_HORSE_SKILL" : CANNOT_SKILL_NOT_HORSE_SKILL,
	"HAVE_TO_RIDE" : CANNOT_SKILL_HAVE_TO_RIDE,
}

LEVEL_LIST=["", HORSE_LEVEL1, HORSE_LEVEL2, HORSE_LEVEL3]

HEALTH_LIST=[
	HORSE_HEALTH0,
	HORSE_HEALTH1, 
	HORSE_HEALTH2,
	HORSE_HEALTH3,
]


USE_SKILL_ERROR_CHAT_DICT = {	
	"NEED_EMPTY_BOTTLE" : SKILL_NEED_EMPTY_BOTTLE,
	"NEED_POISON_BOTTLE" : SKILL_NEED_POISON_BOTTLE, 
	"ONLY_FOR_GUILD_WAR" : SKILL_ONLY_FOR_GUILD_WAR,
}

if app.ENABLE_BATTLE_FIELD:
	SHOP_ERROR_DICT = {
		"NOT_ENOUGH_MONEY" : SHOP_NOT_ENOUGH_MONEY,
		"SOLDOUT" : SHOP_SOLDOUT,
		"INVENTORY_FULL" : SHOP_INVENTORY_FULL,
		"INVALID_POS" : SHOP_INVALID_POS,
		"NOT_ENOUGH_MONEY_EX" : SHOP_NOT_ENOUGH_MONEY_EX,
		"NOT_ENOUGH_BP" : SHOP_NOT_ENOUGH_BATTLE_POINT,
		"EXCEED_LIMIT_TODAY" : SHOP_EXCEED_LIMIT_TODAY,
	}
else:
	SHOP_ERROR_DICT = {
		"NOT_ENOUGH_MONEY" : SHOP_NOT_ENOUGH_MONEY,
		"SOLDOUT" : SHOP_SOLDOUT,
		"INVENTORY_FULL" : SHOP_INVENTORY_FULL,
		"INVALID_POS" : SHOP_INVALID_POS,
		"NOT_ENOUGH_MONEY_EX" : SHOP_NOT_ENOUGH_MONEY_EX,
	}
if app.ENABLE_10TH_EVENT:
	SHOP_ERROR_DICT["NOT_ENOUGH_10TH_COIN"] = SHOP_NOT_ENOUGH_10TH_COIN
	
if app.ENABLE_12ZI:
	SHOP_ERROR_DICT["LIMITED_PURCHASE_OVER"] = SHOP_LIMITED_PURCHASE_OVER
	SHOP_ERROR_DICT["LIMITED_DATA_LOADING"] = SHOP_LIMITED_DATA_LOADING

STAT_MINUS_DESCRIPTION = {
	"HTH-" : STAT_MINUS_CON,
	"INT-" : STAT_MINUS_INT,
	"STR-" : STAT_MINUS_STR,
	"DEX-" : STAT_MINUS_DEX,
}

MODE_NAME_LIST = ( PVP_OPTION_NORMAL, PVP_OPTION_REVENGE, PVP_OPTION_KILL, PVP_OPTION_PROTECT, )
TITLE_NAME_LIST = ( PVP_LEVEL0, PVP_LEVEL1, PVP_LEVEL2, PVP_LEVEL3, PVP_LEVEL4, PVP_LEVEL5, PVP_LEVEL6, PVP_LEVEL7, PVP_LEVEL8, )

def GetLetterImageName():
	return "season1/icon/scroll_close.tga"
def GetLetterOpenImageName():
	return "season1/icon/scroll_open.tga"
def GetLetterCloseImageName():
	return "season1/icon/scroll_close.tga"
	
if app.ENABLE_MONSTER_BACK or app.ENABLE_CARNIVAL2016:
	def GetBlueLetterImageName():
		return "icon/item/scroll_close_blue.tga"
	def GetBlueLetterOpenImageName():
		return "icon/item/scroll_open_blue.tga"
	def GetBlueLetterCloseImageName():
		return "icon/item/scroll_close_blue.tga"

if 949 == app.GetDefaultCodePage():
	def EUL(name):
		if GetAuxiliaryWordType(name):
			return "�� "
		else:
			return "�� "

	def I(name):
		if GetAuxiliaryWordType(name):
			return "�� "
		else:
			return "�� "

	def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
		name = sellItemName
		if sellItemCount > 1:
			name += " "
			name += str(sellItemCount)
			name += "��"

		return name + EUL(name) + str(sellItemPrice) + "�ɿ� �Ľðڽ��ϱ�?"

	if app.ENABLE_CHEQUE_SYSTEM:
		def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice, sellItemCheque = 0):
			if sellItemCheque > 0:
				if buyItemCount > 1 :
					return DO_YOU_BUY_ITEM4 % ( buyItemName, buyItemCount, sellItemCheque, buyItemPrice )
				else:
					return DO_YOU_BUY_ITEM3 % ( buyItemName, sellItemCheque, buyItemPrice )			
			else:
				if buyItemCount > 1 :
					return DO_YOU_BUY_ITEM2 % ( buyItemName, buyItemCount, buyItemPrice )
				else:
					return DO_YOU_BUY_ITEM1 % ( buyItemName, buyItemPrice )
	else:
		def DO_YOU_BUY_ITEM(sellItemName, sellItemCount, sellItemPrice):
			name = sellItemName
			if sellItemCount > 1:
				name += " "
				name += str(sellItemCount)
				name += "��"

			return name + EUL(name) + str(sellItemPrice) + "�� ��ðڽ��ϱ�?"

	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName):
		return attachedItemName+EUL(attachedItemName)+"������ �� ���� �������Դϴ�"

	def REFINE_FAILURE_NO_SOCKET(attachedItemName):
		return attachedItemName+EUL(attachedItemName)+"������ �� �ִ� ������ �����ϴ�"	

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName):
		return attachedItemName+EUL(attachedItemName)+"������ �� �ִ� Ȳ�� ������ �����ϴ�"	

	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount):
		name = dropItemName
		if dropItemCount > 1:
			name += " "
			name += str(dropItemCount)
			name += "��"

		return name+EUL(name)+"�����ðڽ��ϱ�?"

	def NumberToMoneyString(n):
		if app.ENABLE_CHEQUE_SYSTEM:
			if n <= 0 :
				return "0"

			return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))
		else:
			if n <= 0:
				return "0��"

			n = str(n)
			result = CutMoneyString(n, 0, 4, "", "")
			result = CutMoneyString(n, 4, 8, "��", result)
			result = CutMoneyString(n, 8, 12, "��", result)
			result = result + "��"

			return result
			
	if app.ENABLE_BATTLE_FIELD:
		def NumberToSecondaryCoinString(number, coinType):
			if number <= 0:
				number = 0

			coinTypeString = ""
			
			if coinType == shop.SHOP_COIN_TYPE_SECONDARY_COIN:
				coinTypeString = "��"
			elif coinType == shop.SHOP_COIN_TYPE_BATTLE_POINT:
				coinTypeString = "��Ʋ����Ʈ"
			elif app.ENABLE_10TH_EVENT and coinType == shop.SHOP_COIN_TYPE_10TH_EVENT:
				coinTypeString = "�����ȭ"
			else:
				return "Not Valied"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "��", result)
			result = CutMoneyString(number, 8, 12, "��", result)

			return "%s %s" % (result, coinTypeString)
	else:
		def NumberToSecondaryCoinString(number):
			if number <= 0:
				return "0��"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "��", result)
			result = CutMoneyString(number, 8, 12, "��", result)
			result = result + "��"

			return result
	def FISHING_NOTIFY(isFish, fishName):
		if isFish:
			return fishName + I(fishName) + "�� �� �մϴ�."
		else:
			return fishName + I(fishName) + "�ɸ��� �մϴ�."

	def FISHING_SUCCESS(isFish, fishName):
		if isFish:
			return fishName + EUL(fishName) + "��ҽ��ϴ�!"
		else:
			return fishName + EUL(fishName) + "������ϴ�!"

elif 932 == app.GetDefaultCodePage():
	def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
		if sellItemCount > 1 :
			return "%s %s �� %s�ɔ���܂����H" % ( sellItemName, sellItemCount, NumberToMoneyString(sellItemPrice) )
		else:
			return "%s �� %s�Ŕ���܂����H" % (sellItemName, NumberToMoneyString(sellItemPrice) )

	def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice) :
		if buyItemCount > 1 :
			return "%s %s�� %s�Ŕ����܂����H" % ( buyItemName, buyItemCount, buyItemPrice )
		else:
			return "%s�� %s�Ŕ����܂����H" % ( buyItemName, buyItemPrice )
			
	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName) :
		return "%s�𑕒��ł��Ȃ��A�C�e?�ł��B" % (attachedItemName)

	def REFINE_FAILURE_NO_SOCKET(attachedItemName) :
		return "%s�𑕒�����?�P�b�g������܂���B" % (attachedItemName)

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName) :
		return "%s�𑕒��ł��鉩��?�P�b�g������܂���B" % (attachedItemName)
		
	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount) :
		if dropItemCount > 1 :
			return "%s %d ���̂Ă܂����H" % (dropItemName, dropItemCount)
		else :	
			return "%s���̂Ă܂����H" % (dropItemName)

	def FISHING_NOTIFY(isFish, fishName) :
		if isFish :
			return "%s ���H�������悤�ł�" % ( fishName )
		else :
			return "%s �����������悤�ł�" % ( fishName )

	def FISHING_SUCCESS(isFish, fishName) :
		if isFish :
			return "%s ��߂܂��܂����I" % (fishName)
		else :
			return "%s ����ɓ���܂����I" % (fishName)
			
	def NumberToMoneyString(number) :
		if number <= 0 :
			return "0��"

		number = str(number)
		result = CutMoneyString(number, 0, 4, "", "")
		result = CutMoneyString(number, 4, 8, "��", result)
		result = CutMoneyString(number, 8, 12, "��", result)
		result = result + "��"

		return result

	if app.ENABLE_BATTLE_FIELD:
		def NumberToSecondaryCoinString(number, coinType) :
			if number <= 0:
				number = 0

			coinTypeString = ""
			
			if coinType == shop.SHOP_COIN_TYPE_SECONDARY_COIN:
				coinTypeString = "jun"
			elif coinType == shop.SHOP_COIN_TYPE_BATTLE_POINT:
				coinTypeString = "battlePoint"
			elif app.ENABLE_10TH_EVENT and coinType == shop.SHOP_COIN_TYPE_10TH_EVENT:
				coinTypeString = "10thCoin"
			else:
				return "Not Valied"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "��", result)
			result = CutMoneyString(number, 8, 12, "��", result)

			return "%s %s" % (result, coinTypeString)
	else:
		def NumberToSecondaryCoinString(number) :
			if number <= 0 :
				return "0jun"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "��", result)
			result = CutMoneyString(number, 8, 12, "��", result)
			result = result + "jun"

			return result

elif IsHONGKONG():
	def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
		if sellItemCount > 1 :
			return DO_YOU_SELL_ITEM2 % (sellItemName, sellItemCount, NumberToMoneyString(sellItemPrice) )
		else:
			return DO_YOU_SELL_ITEM1 % (sellItemName, NumberToMoneyString(sellItemPrice) )

	def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice) :
		if buyItemCount > 1 :
			return DO_YOU_BUY_ITEM2 % ( buyItemName, buyItemCount, buyItemPrice )
		else:
			return DO_YOU_BUY_ITEM1 % ( buyItemName, buyItemPrice )
			
	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName) :
		return REFINE_FAILURE_CAN_NOT_ATTACH0 % (attachedItemName)

	def REFINE_FAILURE_NO_SOCKET(attachedItemName) :
		return REFINE_FAILURE_NO_SOCKET0 % (attachedItemName)

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName) :
		return REFINE_FAILURE_NO_GOLD_SOCKET0 % (attachedItemName)
		
	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount) :
		if dropItemCount > 1 :
			return HOW_MANY_ITEM_DO_YOU_DROP2 % (dropItemName, dropItemCount)
		else :	
			return HOW_MANY_ITEM_DO_YOU_DROP1 % (dropItemName)

	def FISHING_NOTIFY(isFish, fishName) :
		if isFish :
			return FISHING_NOTIFY1 % ( fishName )
		else :
			return FISHING_NOTIFY2 % ( fishName )

	def FISHING_SUCCESS(isFish, fishName) :
		if isFish :
			return FISHING_SUCCESS1 % (fishName)
		else :
			return FISHING_SUCCESS2 % (fishName)
			
	def NumberToMoneyString(number) :
		if number <= 0 :
			return "0 %s" % (MONETARY_UNIT0)

		number = str(number)
		result = CutMoneyString(number, 0, 4, 	"", "")
		result = CutMoneyString(number, 4, 8, 	MONETARY_UNIT1, result)
		result = CutMoneyString(number, 8, 12, 	MONETARY_UNIT2, result)
		result = result + MONETARY_UNIT0

		return result

	if app.ENABLE_BATTLE_FIELD:
		def NumberToSecondaryCoinString(number, coinType) :
			if number <= 0:
				number = 0

			coinTypeString = ""
			
			if coinType == shop.SHOP_COIN_TYPE_SECONDARY_COIN:
				coinTypeString = MONETARY_UNIT_JUN
			elif coinType == shop.SHOP_COIN_TYPE_BATTLE_POINT:
				coinTypeString = "BP"
			elif app.ENABLE_10TH_EVENT and coinType == shop.SHOP_COIN_TYPE_10TH_EVENT:
				coinTypeString = "10thCoin"
			else:
				return "Not Valied"

			number = str(number)
			result = CutMoneyString(number, 0, 4, 	"", "")
			result = CutMoneyString(number, 4, 8, 	MONETARY_UNIT1, result)
			result = CutMoneyString(number, 8, 12, 	MONETARY_UNIT2, result)

			return "%s %s" % (result, coinTypeString)
	else:
		def NumberToSecondaryCoinString(number) :
			if number <= 0 :
				return "0 %s" % (MONETARY_UNIT_JUN)

			number = str(number)
			result = CutMoneyString(number, 0, 4, 	"", "")
			result = CutMoneyString(number, 4, 8, 	MONETARY_UNIT1, result)
			result = CutMoneyString(number, 8, 12, 	MONETARY_UNIT2, result)
			result = result + MONETARY_UNIT_JUN

			return result

elif IsNEWCIBN() or IsCIBN10():
	def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
		if sellItemCount>1:
			return "ȷ��Ҫ��%s��%s��%s���������" % (str(sellItemCount), sellItemName, str(sellItemPrice))
		else:
			return "ȷ��Ҫ��%s��%s���������" % (sellItemName, str(sellItemPrice))

	def DO_YOU_BUY_ITEM(sellItemName, sellItemCount, sellItemPrice):
		if sellItemCount>1:
			return "ȷ��Ҫ��%s��%s��%s��������" % (str(sellItemCount), sellItemName, str(sellItemPrice))
		else:
			return "ȷ��Ҫ��%s��%s��������" % (sellItemName, str(sellItemPrice))

	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName):
		return "�޷���Ƕ%s ��װ��" % (attachedItemName)

	def REFINE_FAILURE_NO_SOCKET(attachedItemName):
		return "û�п�����Ƕ%s �Ŀ�" % (attachedItemName)

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName):
		return "û�п�����Ƕ%s �Ļƽ��" % (attachedItemName)

	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount):
		if dropItemCount>1:
			return "ȷ��Ҫ�ӵ�%d��%s��?" % (dropItemCount, dropItemName)
		else:
			return "ȷ��Ҫ�ӵ�%s��?" % (dropItemName)

	def FISHING_NOTIFY(isFish, fishName):
		if isFish:
			return fishName # ���� ���⿡ � ���� �پ��ִµ�, ���ڵ��� �����־ ������ ���� ���� �Ф�... cython���� ���ڵ� ���� ���� ��������...
		else:
			return "����" + fishName + "�ˡ�"

	def FISHING_SUCCESS(isFish, fishName):
		if isFish:
			return "����" + fishName + "�ˡ�"
		else:
			return "���" + fishName + "�ˡ�"

	def NumberToMoneyString(number):

		if number <= 0:
			return "0��"

		number = str(number)
		result = CutMoneyString(number, 0, 4, "", "")
		result = CutMoneyString(number, 4, 8, "��", result)
		result = CutMoneyString(number, 8, 12, "��", result)
		result = result + "��"

		return result

	if app.ENABLE_BATTLE_FIELD:
		def NumberToSecondaryCoinString(number, coinType):

			if number <= 0:
				number = 0
	
			coinTypeString = ""
			
			if coinType == shop.SHOP_COIN_TYPE_SECONDARY_COIN:
				coinTypeString = "JUN"
			elif coinType == shop.SHOP_COIN_TYPE_BATTLE_POINT:
				coinTypeString = "BP"
			elif app.ENABLE_10TH_EVENT and coinType == shop.SHOP_COIN_TYPE_10TH_EVENT:
				coinTypeString = "10thCoin"
			else:
				return "Not Valied"
			
			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "��", result)
			result = CutMoneyString(number, 8, 12, "��", result)

			return "%s %s" % (result, coinTypeString)
	else:
		def NumberToSecondaryCoinString(number):

			if number <= 0:
				return "0JUN"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "��", result)
			result = CutMoneyString(number, 8, 12, "��", result)
			result = result + "JUN"

			return result			
elif IsEUROPE() and not IsWE_KOREA() and not IsYMIR():
	def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
		if sellItemCount > 1 :
			return DO_YOU_SELL_ITEM2 % (sellItemName, sellItemCount, NumberToMoneyString(sellItemPrice) )
		else:
			return DO_YOU_SELL_ITEM1 % (sellItemName, NumberToMoneyString(sellItemPrice) )

	if app.ENABLE_CHEQUE_SYSTEM:
		def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice, sellItemCheque = 0):
			if sellItemCheque > 0:
				if buyItemCount > 1 :
					return DO_YOU_BUY_ITEM4 % ( buyItemName, buyItemCount, sellItemCheque, buyItemPrice )
				else:
					return DO_YOU_BUY_ITEM3 % ( buyItemName, sellItemCheque, buyItemPrice )			
			else:
				if buyItemCount > 1 :
					return DO_YOU_BUY_ITEM2 % ( buyItemName, buyItemCount, buyItemPrice )
				else:
					return DO_YOU_BUY_ITEM1 % ( buyItemName, buyItemPrice )
	else:
		def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice) :
			if buyItemCount > 1 :
				return DO_YOU_BUY_ITEM2 % ( buyItemName, buyItemCount, buyItemPrice )
			else:
				return DO_YOU_BUY_ITEM1 % ( buyItemName, buyItemPrice )
			
	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName) :
		return REFINE_FAILURE_CAN_NOT_ATTACH0 % (attachedItemName)

	def REFINE_FAILURE_NO_SOCKET(attachedItemName) :
		return REFINE_FAILURE_NO_SOCKET0 % (attachedItemName)

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName) :
		return REFINE_FAILURE_NO_GOLD_SOCKET0 % (attachedItemName)
		
	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount) :
		if dropItemCount > 1 :
			return HOW_MANY_ITEM_DO_YOU_DROP2 % (dropItemName, dropItemCount)
		else :	
			return HOW_MANY_ITEM_DO_YOU_DROP1 % (dropItemName)

	def FISHING_NOTIFY(isFish, fishName) :
		if isFish :
			return FISHING_NOTIFY1 % ( fishName )
		else :
			return FISHING_NOTIFY2 % ( fishName )

	def FISHING_SUCCESS(isFish, fishName) :
		if isFish :
			return FISHING_SUCCESS1 % (fishName)
		else :
			return FISHING_SUCCESS2 % (fishName)

	if app.ENABLE_CHEQUE_SYSTEM:
		def NumberToMoneyString(n) :
			if n <= 0 :
				return "0"

			return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ])) 
	else:			
		def NumberToMoneyString(n) :
			if n <= 0 :
				return "0 %s" % (MONETARY_UNIT0)

			return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), MONETARY_UNIT0) 

	if app.ENABLE_BATTLE_FIELD:
		def NumberToSecondaryCoinString(n, coinType) :
	
			if n <= 0:
				n = 0

			coinTypeString = ""
				
			if coinType == shop.SHOP_COIN_TYPE_SECONDARY_COIN:
				coinTypeString = MONETARY_UNIT_JUN
			elif coinType == shop.SHOP_COIN_TYPE_BATTLE_POINT:
				coinTypeString = BATTLE_POINT
			elif app.ENABLE_10TH_EVENT and coinType == shop.SHOP_COIN_TYPE_10TH_EVENT:
				coinTypeString = TENTH_COIN
			else:
				return "Not Valied"
	
			return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), coinTypeString) 		
	else:
		def NumberToSecondaryCoinString(n) :
			if n <= 0 :
				return "0 %s" % (MONETARY_UNIT_JUN)

			return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), MONETARY_UNIT_JUN) 
