import app
import constInfo
import background

if app.ENABLE_BATTLE_FIELD:
	import shop

MAP_TRENT02 = "MAP_TRENT02" # ¿”Ω√
MAP_WL = "MAP_WL" # ¿”Ω√
MAP_NUSLUCK = "MAP_NUSLUCK" # ¿”Ω√ 
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
GUILD_MARK_NOT_ENOUGH_LEVEL = "±ÊµÂ∑π∫ß 3¿ÃªÛ ∫Œ≈Õ ∞°¥…«’¥œ¥Ÿ."

ERROR_MARK_UPLOAD_NEED_RECONNECT = "UploadMark: Reconnect to game"
ERROR_MARK_CHECK_NEED_RECONNECT = "CheckMark: Reconnect to game"

VIRTUAL_KEY_ALPHABET_LOWERS  = r"[1234567890]/qwertyuiop\=asdfghjkl;`'zxcvbnm.,"
VIRTUAL_KEY_ALPHABET_UPPERS  = r'{1234567890}?QWERTYUIOP|+ASDFGHJKL:~"ZXCVBNM<>'
VIRTUAL_KEY_SYMBOLS    = '!@#$%^&*()_+|{}:"<>?~'
VIRTUAL_KEY_NUMBERS    = "1234567890-=\[];',./`"
VIRTUAL_KEY_SYMBOLS_BR    = '!@#$%^&*()_+|{}:"<>?~·‡„‚ÈËÍÌÏÛÚÙı˙˘Á'

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
		SERVER = "ƒËµµ º≠πˆ"
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
	return IsYMIR()		# ¿Ã¡¶ YMIR ∑Œƒ…¿œ¿∫ π´¡∂∞« √µ∏∂º≠πˆ¿”. √µ∏∂º≠πˆ∞° πÆ¿ª ¥›±‚ ¿¸±Ó¡ˆ ∫Ø«“ ¿œ æ¯¿Ω.

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
	##∞‘¿”∏Ì¿Ã±˙¡¯¥Ÿ.
	APP_TITLE = "–¬“–ÃÏ2"
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()
	constInfo.IN_GAME_SHOP_ENABLE = 1
elif IsTAIWAN():
	APP_TITLE = "∞´III∞Í"
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()

	constInfo.IN_GAME_SHOP_ENABLE = 1
	
else:
	FN_GM_MARK = "%s/effect/gm.mse"	% app.GetLocalePath()
	LOCALE_FILE_NAME = "%s/locale_game.txt" % app.GetLocalePath()

	constInfo.IN_GAME_SHOP_ENABLE = 1

LoadLocaleFile(LOCALE_FILE_NAME, locals())

########################################################################################################
## NOTE : æ∆¿Ã≈€¿ª πˆ∏±∂ß "π´æ˘¿ª/∏¶ πˆ∏ÆΩ√∞⁄Ω¿¥œ±Ó?" πÆ¿⁄ø≠¿« ¡∂ªÁ º±≈√¿ª ¿ß«— ƒ⁄µÂ
dictSingleWord = {
	"m":1, "n":1, "r":1, "M":1, "N":1, "R":1, "l":1, "L":1, "1":1, "3":1, "6":1, "7":1, "8":1, "0":1,
}

dictDoubleWord = {
	"∞°":1, "∞º":1, "∞≈":1, "∞‹":1, "∞Ì":1, "±≥":1, "±∏":1, "±‘":1, "±◊":1, "±‚":1, "∞≥":1, "∞¬":1, "∞‘":1, "∞Ë":1, "∞˙":1, "±•":1, "±≈":1, "±À":1, "±´":1, "±Õ":1, "±·":1,
	"±Ó":1, "≤•":1, "≤®":1, "≤∏":1, "≤ø":1, "≤ÿ":1, "≤Ÿ":1, "≤Û":1, "≤Ù":1, "≥¢":1, "±˙":1, "É∆":1, "≤≤":1, "≤æ":1, "≤ ":1, "≤œ":1, "≤„":1, "≤Á":1, "≤“":1, "≤Ó":1, "Ö ":1,
	"≥™":1, "≥ƒ":1, "≥ ":1, "≥‡":1, "≥Î":1, "¥¢":1, "¥©":1, "¥∫":1, "¥¿":1, "¥œ":1, "≥ª":1, "Üv":1, "≥◊":1, "≥È":1, "≥ˆ":1, "áR":1, "¥≤":1, "¥¥":1, "≥˙":1, "¥µ":1, "¥Ã":1,
	"¥Ÿ":1, "¥Ù":1, "¥ı":1, "µÆ":1, "µµ":1, "µÕ":1, "µŒ":1, "µ‡":1, "µÂ":1, "µ":1, "¥Î":1, "à€":1, "µ•":1, "µ≥":1, "µ¬":1, "µ≈":1, "µ÷":1, "µÿ":1, "µ«":1, "µ⁄":1, "µÔ":1,
	"µ˚":1, "ãx":1, "∂∞":1, "∂≈":1, "∂«":1, "å√":1, "∂—":1, "çè":1, "∂ﬂ":1, "∂Ï":1, "∂ß":1, "ãö":1, "∂º":1, "ãÛ":1, "∂Ã":1, "∂Œ":1, "åÙ":1, "∂ÿ":1, "∂œ":1, "∂Ÿ":1, "∂Á":1,
	"∂Û":1, "∑™":1, "∑Ø":1, "∑¡":1, "∑Œ":1, "∑·":1, "∑Á":1, "∑˘":1, "∏£":1, "∏Æ":1, "∑°":1, "ém":1, "∑π":1, "∑ ":1, "∑÷":1, "èO":1, "∑Ô":1, "∑Ò":1, "∑⁄":1, "∑Ú":1, "êl":1,
	"∏∂":1, "∏œ":1, "∏”":1, "∏Á":1, "∏":1, "π¶":1, "π´":1, "π¬":1, "π«":1, "πÃ":1, "∏≈":1, "êŸ":1, "∏ﬁ":1, "∏Ô":1, "∏˙":1, "ë¿":1, "ππ":1, "πæ":1, "∏˛":1, "πø":1, "íﬁ":1,
	"πŸ":1, "πÚ":1, "πˆ":1, "∫≠":1, "∫∏":1, "∫Ã":1, "∫Œ":1, "∫‰":1, "∫Í":1, "∫Ò":1, "πË":1, "ìé":1, "∫£":1, "∫∂":1, "∫¡":1, "∫ƒ":1, "∫€":1, "∫ﬁ":1, "∫∆":1, "∫ﬂ":1, "ïë":1,
	"∫¸":1, "ª≤":1, "ªµ":1, "ª¿":1, "ª«":1, "ªœ":1, "ª—":1, "ªÿ":1, "ª⁄":1, "ªﬂ":1, "ª©":1, "ï˚":1, "ªæ":1, "ñß":1, "ñÿ":1, "ñÙ":1, "ó®":1, "óƒ":1, "ªŒ":1, "ó‡":1, "òu":1,
	"ªÁ":1, "ª˛":1, "º≠":1, "º≈":1, "º“":1, "ºÓ":1, "ºˆ":1, "Ω¥":1, "Ω∫":1, "Ω√":1, "ªı":1, "º®":1, "ºº":1, "ºŒ":1, "º›":1, "º‚":1, "Ω§":1, "Ω¶":1, "ºË":1, "Ω¨":1, "ö√":1,
	"ΩŒ":1, "õX":1, "Ω·":1, "õ«":1, "ΩÓ":1, "æ§":1, "æ•":1, "ùo":1, "æ≤":1, "ææ":1, "Ωÿ":1, "õy":1, "ΩÍ":1, "õ„":1, "Ω˜":1, "Ω˚":1, "æ¨":1, "æÆ":1, "Ω˝":1, "æØ":1, "æ∫":1,
	"æ∆":1, "æﬂ":1, "æÓ":1, "ø©":1, "ø¿":1, "ø‰":1, "øÏ":1, "¿Ø":1, "¿∏":1, "¿Ã":1, "æ÷":1, "æÍ":1, "ø°":1, "øπ":1, "øÕ":1, "ø÷":1, "øˆ":1, "ø˛":1, "ø‹":1, "¿ß":1, "¿«":1,
	"¿⁄":1, "¿":1, "¿˙":1, "¡Æ":1, "¡∂":1, "¡“":1, "¡÷":1, "¡Í":1, "¡Ó":1, "¡ˆ":1, "¿Á":1, "¿˜":1, "¡¶":1, "¡µ":1, "¡¬":1, "¡»":1, "¡‡":1, "¡‚":1, "¡À":1, "¡„":1, "£p":1,
	"¬•":1, "¬π":1, "¬º":1, "¬«":1, "¬…":1, "ßc":1, "¬ﬁ":1, "¬È":1, "¬Í":1, "¬Ó":1, "¬∞":1, "§ä":1, "¬≈":1, "•ô":1, "¬“":1, "¬÷":1, "¬Â":1, "®R":1, "¬ÿ":1, "¬Ë":1, "©n":1,
	"¬˜":1, "√≠":1, "√≥":1, "√ƒ":1, "√ ":1, "√›":1, "√ﬂ":1, "√Ú":1, "√˜":1, "ƒ°":1, "√§":1, "™â":1, "√º":1, "√«":1, "√“":1, "¨Ç":1, "√Á":1, "√È":1, "√÷":1, "√Î":1, "ØM":1,
	"ƒ´":1, "ƒº":1, "ƒø":1, "ƒ—":1, "ƒ⁄":1, "ƒÏ":1, "ƒÌ":1, "≈•":1, "≈©":1, "≈∞":1, "ƒ≥":1, "∞m":1, "ƒ…":1, "ƒŸ":1, "ƒ‚":1, "ƒË":1, "ƒı":1, "ƒ˘":1, "ƒÍ":1, "ƒ˚":1, "¥î":1,
	"≈∏":1, "≈À":1, "≈Õ":1, "≈ﬂ":1, "≈‰":1, "≈Ù":1, "≈ı":1, "∆©":1, "∆Æ":1, "∆º":1, "≈¬":1, "∂O":1, "≈◊":1, "≈‚":1, "≈Ì":1, "≈Ô":1, "≈˝":1, "∆°":1, "≈":1, "∆¢":1, "∆∑":1,
	"∆ƒ":1, "∆Ÿ":1, "∆€":1, "∆Ï":1, "∆˜":1, "«•":1, "«™":1, "«ª":1, "«¡":1, "««":1, "∆–":1, "ªó":1, "∆‰":1, "∆Û":1, "«°":1, "Ωç":1, "«¥":1, "øR":1, "«£":1, "«∂":1, "¿c":1,
	"«œ":1, "«·":1, "«„":1, "«Ù":1, "»£":1, "»ø":1, "»ƒ":1, "»ﬁ":1, "»Â":1, "»˜":1, "«ÿ":1, "¡Ö":1, "«Ï":1, "«˝":1, "»≠":1, "»≥":1, "»Ã":1, "»—":1, "»∏":1, "»÷":1, "»Ò":1,
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

# ƒ≥∏Ø≈Õ√¢ø°º≠ ƒ≥∏Ø≈Õ¿« æÛ±ºø° ∏∂øÏΩ∫ ø¿πˆ «ﬂ¿ª ∂ß ≥™ø¿¥¬ º≥∏Ì¿« ∏« ¿ß JOB_TITLE
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


# ƒ≥∏Ø≈Õ√¢ø°º≠ ƒ≥∏Ø≈Õ¿« æÛ±ºø° ∏∂øÏΩ∫ ø¿πˆ «ﬂ¿ª ∂ß ≥™ø¿¥¬ º≥∏Ì.
JOBINFO_DATA_LIST = [
	[
		["≈∏∞Ì≥≠ øÎ∏Õ∞˙ ±¡»˜¡ˆ æ ¥¬ π´ªÁ¿«",
		"±‚∞≥∏¶ ªÁ∂˜µÈ¿∫ ¿œƒ√æÓ [øÎ¿⁄]∂Û∞Ì",
		"∫Œ∏•¥Ÿ. æÓ∂∞«— ¿ß±‚ø°º≠µµ ±◊µÈ¿∫ ",
		"µ⁄∑Œ π∞∑Øº≠¡ˆ æ ¿∏∏Á, ¥Ÿƒ°∞Ì øÚ¡˜",
		"¿Ã±‚ »˚µÁ µø∑·∏¶ ¿ß«ÿ ¥‹Ω≈¿∏∑Œ",
		"¿˚µÈ∞˙ ∏∂¡÷ ΩŒøÏ±‚µµ «—¥Ÿ. ¿ÃµÈ¿∫",
		"¿ﬂ ¥‹∑√µ» ±Ÿ¿∞∞˙ »˚, ∞≠∑¬«— ∞¯∞›∑¬",
		"¿∏∑Œ ¿¸¿Â √÷º±µŒø°º≠ ∞¯∞›¡¯¿∏∑Œ",
		"»∞æ‡«—¥Ÿ.                      ",],
		["∞°¿Â ¿œπ›¿˚¿Œ ∞¯∞›«¸ π´ªÁ∑Œ, ",
		"¿˚¡¢¿¸ø° µ˚∏• ¡˜¡¢ ∞¯∞›¿∏∑Œ ¿¸¿Â",
		"ø°º≠ »∞æ‡«—¥Ÿ. ±∫¡˜ ∆Øº∫ªÛ ±Ÿ∑¬¿ª",
		"∏ﬁ¿Œ¿∏∑Œ Ω∫≈› ∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«œµ«, ",
		"¿˚¡¢¿¸ø° µ˚∏• ª˝∏Ì∑¬ / πÊæÓ∑¬",
		"»Æ∫∏∏¶ ¿ß«ÿ √º∑¬¿ª ø√∏∞¥Ÿ. ∂««—",
		"∞¯∞›¿« ¡§»Æº∫¿ª ≥Ù¿Ã±‚ ¿ß«ÿ πŒ√∏",
		"ø°µµ ∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«“ « ø‰∞° ¿÷¥Ÿ.",],
		["ªÛ¥Á ºˆ¡ÿ¿« ¡§Ω≈∑¬¿ª ¿ÃøÎ«œ¥¬",
		"¡ﬂ/±Ÿ∞≈∏Æ ¡¢¿¸«¸ π´ªÁ∑Œ, ∞¢ ±‚º˙",
		"«œ≥™«œ≥™¿« ≥Ù¿∫ ∞¯∞›∑¬¿∏∑Œ ¿¸¿Âø°º≠",
		"»∞æ‡«—¥Ÿ. ±∫¡˜ ∆Øº∫ªÛ ±Ÿ∑¬¿ª ∏ﬁ¿Œ",
		"¿∏∑Œ Ω∫≈» ∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«œµ«, ",
		"¡ﬂ/±Ÿ∞≈∏Æ ∞¯∞›¿« ¡§»Æº∫∞˙ ∏Ì¡ﬂ∑¸¿ª",
		"¿ß«ÿ πŒ√∏¿ª ø√∏∞¥Ÿ. ∂««— ¡¢¿¸ Ω√ ",
		"¿˚ ∞¯∞›ø° µ˚∏• ª˝∏Ì∑¬ / πÊæÓ∑¬",
		"»Æ∫∏∏¶ ¿ß«ÿ √º∑¬ø°µµ ∆˜¿Œ∆Æ∏¶",
		"≈ı¿⁄«“ « ø‰∞° ¿÷¥Ÿ.        ",],		
	],
	[
		["¿⁄∞¥¿∫ æÓ∂∞«— ªÛ»≤ø°º≠µµ ¿⁄Ω≈¿«",
		"∏ˆ¿ª º˚±‚∞Ì ¿∫π–«— æÓµ“¿« ¿”π´∏¶",
		"ºˆ«‡«œ∏Èº≠ ¿¸¿Â¿« »ƒ¿ß∏¶ ¡ˆø¯«œ¥¬", 
		"¿⁄µÈ¿Ã¥Ÿ. ¿ÃµÈ¿∫ æ∆¡÷ ∫¸∏£∞Ì Ω≈º”",
		"«œ∏Á, ∫Ò«“ µ• æ¯¿Ã ∞˙∞®«œ∞Ì ¿˝¡¶µ»",
		"«‡µø¿∏∑Œ ¿˚¿« ±ﬁº“ø° ƒ°∏Ì≈∏∏¶ ≥Ø∏Æ",
		"µ«, ¿¸¿Âø°º± ¿˚¡¯¿ª «‚«ÿ π´ºˆ«—",
		"»≠ªÏ¿ª ≥ªª’¿∏∏Á ¿⁄Ω≈¿« øÎ∏Õ¿ª",
		"º±∫∏¿Œ¥Ÿ.                   "],
		["µŒº’ ¥‹∞À¿ª ¡÷π´±‚∑Œ ¥Ÿ∑Á∏Á, Ω≈º”",
		"«œ∞‘ ƒ°∞Ì ∫¸¡ˆ¥¬ ¿⁄∞¥ ∆Ø¿Ø¿« øÚ¡˜¿”",
		"¿∏∑Œ ¿¸¿Âø°º≠ »∞æ‡«—¥Ÿ. ±∫¡˜ ∆Øº∫ªÛ",
		"πŒ√∏¿ª ∏ﬁ¿Œ¿∏∑Œ Ω∫≈› ∆˜¿Œ∆Æ∏¶ ≈ı¿⁄",
		"«œµ«, ±Ÿ∑¬¿ª ø√∑¡ ∞¯∞›∑¬¿ª ≥Ù¿Œ¥Ÿ.",
		"∂««— ±Ÿ¡¢¿¸ø° µ˚∏• ª˝∏Ì∑¬/πÊæÓ∑¬ ",
		"ªÛΩ¬¿ª ¿ß«ÿ √º∑¬ø°µµ ∆˜¿Œ∆Æ∏¶",
		"≈ı¿⁄«“ « ø‰∞° ¿÷¥Ÿ.          ",],
		["»∞¿ª ¡÷π´±‚∑Œ ¥Ÿ∑Á∏Á, ±‰ Ω√æﬂøÕ",
		"ªÁ¡§∞≈∏Æø° µ˚∏• ø¯∞≈∏Æ ∞¯∞›¿∏∑Œ",
		"¿¸¿Âø°º≠ »∞æ‡«—¥Ÿ. ±∫¡˜ ∆Øº∫ªÛ",
		"∞¯∞› º∫∞¯∑¸¿« ¡ı∞°∏¶ ¿ß«ÿ πŒ√∏¿ª",
		"∏ﬁ¿Œ¿∏∑Œ ø√∑¡æﬂ «œ∏Á, ø¯∞≈∏Æ",
		"∞¯∞›¿« µ•πÃ¡ˆ ¡ı∞°∏¶ ¿ß«ÿ ±Ÿ∑¬¿ª",
		"ø√∏± « ø‰∞° ¿÷¥Ÿ. ∂««— ¿˚µÈø°∞‘",
		"∆˜¿ßµ«æ˙¿ª Ω√, ¿˚ ∞¯∞›ø° πˆ∆º±‚",
		"¿ß«— ª˝∏Ì∑¬/πÊæÓ∑¬ ªÛΩ¬¿ª ¿ß«ÿ",
		"√º∑¬ø°µµ ∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«“ « ø‰∞°",
		"¿÷¥Ÿ.                        ", ],
	],
	[
		["ºˆ∂Û¥¬ [µ∂¿∫ µ∂¿∏∑Œ]¿« º”º∫¿∏∑Œ",
		"√¢º≥µ» ∆Øºˆ º”º∫¿« ±∫¡˜¿Ã¥Ÿ. ",
		"±◊µÈ¿∫ ¿¸¿Âø°º≠ ¿˚µÈ¿« ªÁ±‚∏¶ ¿˙«œ",
		"Ω√≈∞∞Ì, æ«∏∂¿« »˚¿ª Ω«¿∫ ∏∂≈∫¿∏∑Œ",
		"¿˚¿« øµ»•∞˙ ¿∞Ω≈¿ª ¡˛π∂∞µ¥Ÿ. ∂ß∑Œ",
		"¿ÃµÈ¿∫ ¿⁄Ω≈¿« ∞À∞˙ ∞©ø ø° æÓµ“¿«",
		"»˚¿ª Ω«æÓ, ¿¸¿Âø°º≠ π´ªÁ ∏¯¡ˆ æ ¿∫",
		"∞¯∞›∑¬¿ª πﬂ»÷«œ±‚µµ «œ¥¬µ•, ¿˚µÈ¿ª",
		"¡◊ø©¥Î¥¬±◊ ∏Ω¿¿Ã øˆ≥´ø° ≤˚¬Ô«ÿ",
		"ªÁ∂˜µÈ¿∫ ºˆ∂Û∏¶ ¿œƒ√æÓ [∏∂Ω≈]¿Ã∂Û",
		"∫Œ∏£±‚∏¶ ¡÷¿˙ æ…¥¬¥Ÿ."],
		["»Øπ´±∫¿« ºˆ∂Û¥¬ æ«∏∂¿« ææø°º≠",
		"æÚæÓ¡ˆ¥¬ ∏∂∑¬¿ª π´±‚≥™ πÊæÓ±∏ø°",
		"Ω«æÓ π´ªÁ ∏¯¡ˆ æ ¿∫ ¿¸≈ı∑¬¿∏∑Œ",
		"¿¸¿Âø°º≠ »∞æ‡«—¥Ÿ. ±∫¡˜ ∆Øº∫ªÛ",
		"¡ˆ¥…¿Ã ≥Ùæ∆¡˙ºˆ∑œ ¬¯øÎ ¿Â∫Òø°", 
		"Ω«∏Æ¥¬ ∏∂∑¬¿« ¿ß∑¬¿Ã ¡ı¥Îµ«π«∑Œ,",
		"¡ˆ¥…∞˙ ±Ÿ∑¬¿ª ∏ﬁ¿Œ¿∏∑Œ Ω∫≈»",
		"∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«œµ«, ¡¢¿¸ø° µ˚∏•",
		"ª˝∏Ì∑¬/πÊæÓ∑¬ »Æ∫∏∏¶ ¿ß«ÿ √º∑¬¿ª",
		"ø√∏∞¥Ÿ. ∂««— ∞¯∞›¿« ¡§»Æº∫∞˙",
		"»∏««∏¶ ¿ß«ÿº≠ πŒ√∏ø°µµ ∆˜¿Œ∆Æ∏¶",
		"≈ı¿⁄«“ « ø‰∞° ¿÷¥Ÿ.           ",],
		["»Ê∏∂±∫¿« ºˆ∂ÛµÈ¿∫ ∞¢¡æ æÓµ“¿«",
		"¡÷πÆ∞˙ æ«∏∂¿« ∏∂π˝¿∏∑Œ ¿¸¿Âø°º≠",
		"»∞æ‡«—¥Ÿ. ±∫¡˜ ∆Øº∫ªÛ ∏∂π˝ ∞¯∞›¿Ã",
		"¡÷¿Ãπ«∑Œ ¡ˆ¥…¿ª ∏ﬁ¿Œ¿∏∑Œ Ω∫≈›",
		"∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«œµ«, ø¯∞≈∏Æ ∏∂π˝",
		"∞¯∞›¿« ¡§»Æº∫¿ª ¿ß«ÿ πŒ√∏¿ª ø√∏∞¥Ÿ.",
		"∂««— ∆˜¿ß µ«æ˙¿ªΩ√, ¿˚ ∞¯∞›ø° µ˚∏•",
		"ª˝∏Ì∑¬ / πÊæÓ∑¬ »Æ∫∏∏¶ ¿ß«ÿ √º∑¬ø°µµ",
		"∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«“ « ø‰∞° ¿÷¥Ÿ.    ",],
	],
	[
		["π´¥Á¿∫ øÎΩ≈∞˙ ¿⁄ø¨, µŒ ∞Ì¥Î¿«",
		"»˚¿ª ¥Ÿ∑Í ºˆ ¿÷¥¬ ¿Ø¿œ«— ¡˜¡æ¿Ã¥Ÿ.",
		"±◊µÈ¿∫ »ƒπÊø°º≠ æ∆±∫¿ª ∫∏¡∂«œ∞Ì",
		"¥Ÿƒ£ µø∑·¿« ∫ŒªÛ¿ª »∏∫π Ω√≈∞∏Á",
		"∂≥æÓ¡¯ ªÁ±‚∏¶ ªÛΩ¬Ω√≈≤¥Ÿ. ±◊µÈ¿∫",
		"æ∆±∫¿« ºˆ∏È∞˙ »ﬁΩƒ¿ª πÊ«ÿ«œ¥¬ ¿⁄∏¶ ",
		"¿˝¥Î øÎº≠«œ¡ˆ æ ¿∏∏Á, ±◊∑± ¿⁄µÈ",
		"ø°∞‘¥¬ «— ¡° ¡÷¿˙ æ¯¿Ã ¡÷πÆ¿ª",
		"≈Õ∆Æ∑¡ ±◊ ∫Ò∞Ã«‘¿ª æˆ»˜ ¬°∞Ë«—¥Ÿ.",],
		["√µ∑Ê±∫¿« π´¥ÁµÈ¿∫ ∞¢¡æ ∫Œ¿˚º˙∞˙",
		"∫∏¡∂¡÷πÆø° ¥…«œ∏Á, ¿˚¿« ¡˜ / ∞£¡¢",
		"∞¯∞›¿∏∑Œ∫Œ≈Õ æ∆±∫¿ª ¡ˆ≈≤¥Ÿ. ±∫¡˜",
		"∆Øº∫ªÛ ∏∂π˝ ¥…∑¬¿Ã ¡÷¿Ãπ«∑Œ ¡ˆ¥…¿ª",
		"∏ﬁ¿Œ¿∏∑Œ Ω∫≈› ∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«œµ«,",
		"∆˜¿ßµ«æ˙¿ª Ω√, ¿˚ ∞¯∞›ø° µ˚∏•",
		"ª˝∏Ì∑¬ / πÊæÓ∑¬ »Æ∫∏∏¶ ¿ß«ÿ √º∑¬¿ª",
		"ø√∏∞¥Ÿ. ∂««— ø¯∞≈∏Æ ∏∂π˝ ∞¯∞›¿«",
		"¡§»Æº∫¿ª ¿ßø° πŒ√∏ø°µµ ∆˜¿Œ∆Æ∏¶",
		"≈ı¿⁄«“ « ø‰∞° ¿÷¥Ÿ.           ",],
		["±§∑⁄±∫¿« π´¥ÁµÈ¿∫ ¿⁄ø¨¿« »˚¿ª",
		"∫Ù∑¡ æ∆±∫¿ª »∏∫π«œ∞Ì, ≥˙Ω≈¿« ",
		"»˚¿∏∑Œ π–¡˝«— ¿˚µÈø°∞‘ ≈´ √Ê∞›¿ª",
		"¿‘»˙ ºˆ ¿÷¥¬ ¿ÃµÈ¿Ã¥Ÿ. ±∫¡˜¿«",
		"∆Øº∫ªÛ ∏∂π˝ ¥…∑¬¿Ã ¡÷¿Ãπ«∑Œ ¡ˆ¥…¿ª",
		"∏ﬁ¿Œ¿∏∑Œ Ω∫≈› ∆˜¿Œ∆Æ∏¶ ≈ı¿⁄«œµ«,",
		"∆˜¿ßµ«æ˙¿ªΩ√, ¿˚ ∞¯∞›ø° µ˚∏•",
		"ª˝∏Ì∑¬ / πÊæÓ∑¬ »Æ∫∏∏¶ ¿ß«ÿ √º∑¬¿ª",
		"ø√∏∞¥Ÿ. ∂««— ø¯∞≈∏Æ ∏∂π˝ ∞¯∞›¿«",
		"¡§»Æº∫¿ª ¿ßø° πŒ√∏ø°µµ ∆˜¿Œ∆Æ∏¶",
		"≈ı¿⁄«“ « ø‰∞° ¿÷¥Ÿ.             "],
	],
	[
		["ºˆ¿Œ",],
		["ºˆ¿Œ¿∫ [∫˘¿«øÕ ƒË]¿« º”º∫¿∏∑Œ",
		"√¢º≥¿Ã µ» ∆Øºˆ ±∫¡˜¿Ã¥Ÿ.",
		"±◊µÈ¿∫ ¿¸¿Âø°º≠ º±∫¿ø° º≠∏Á, ∏∂π∞µÈ¿«",
		"ªÁ±‚∏¶ ¿˙«œΩ√≈∞∞Ì ¿∞Ω≈¿ª ¬ıæÓ πﬂ±‰¥Ÿ.",
		"∂ß∑Œ¥¬ ¿⁄Ω≈µÈ¿« ∏ˆø° ¥¡¥Î¿« øµ»•¿ª ¿ÃæÓ",
		"πﬁæ∆, ¿¸¿Âø°º≠ π´ªÁ∏¶ √ ø˘«œ¥¬ º¯∞£¿˚¿Œ",
		"∞¯∞›∑¬¿ª πﬂ√Î«œ±‚µµ «œ¥¬µ•, ¿˚µÈ¿∫ ±◊",
		"∏Ω¿¿Ã »ÌªÁ [¥Î∂˚]¿ª ¥‡æ∆ [ªÁΩ≈]¿Ã∂Û",
		"∫Œ∏£±‚µµ «—¥Ÿ."],
		["«ÿ¥Áæ¯¿Ω"],
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
			return "∏¶ "
		else:
			return "¿ª "

	def I(name):
		if GetAuxiliaryWordType(name):
			return "∞° "
		else:
			return "¿Ã "

	def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
		name = sellItemName
		if sellItemCount > 1:
			name += " "
			name += str(sellItemCount)
			name += "∞≥"

		return name + EUL(name) + str(sellItemPrice) + "≥…ø° ∆ƒΩ√∞⁄Ω¿¥œ±Ó?"

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
				name += "∞≥"

			return name + EUL(name) + str(sellItemPrice) + "ø° ªÁΩ√∞⁄Ω¿¥œ±Ó?"

	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName):
		return attachedItemName+EUL(attachedItemName)+"∫Œ¬¯«“ ºˆ æ¯¥¬ æ∆¿Ã≈€¿‘¥œ¥Ÿ"

	def REFINE_FAILURE_NO_SOCKET(attachedItemName):
		return attachedItemName+EUL(attachedItemName)+"∫Œ¬¯«“ ºˆ ¿÷¥¬ º“ƒœ¿Ã æ¯Ω¿¥œ¥Ÿ"	

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName):
		return attachedItemName+EUL(attachedItemName)+"∫Œ¬¯«“ ºˆ ¿÷¥¬ »≤±› º“ƒœ¿Ã æ¯Ω¿¥œ¥Ÿ"	

	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount):
		name = dropItemName
		if dropItemCount > 1:
			name += " "
			name += str(dropItemCount)
			name += "∞≥"

		return name+EUL(name)+"πˆ∏ÆΩ√∞⁄Ω¿¥œ±Ó?"

	def NumberToMoneyString(n):
		if app.ENABLE_CHEQUE_SYSTEM:
			if n <= 0 :
				return "0"

			return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))
		else:
			if n <= 0:
				return "0≥…"

			n = str(n)
			result = CutMoneyString(n, 0, 4, "", "")
			result = CutMoneyString(n, 4, 8, "∏∏", result)
			result = CutMoneyString(n, 8, 12, "æÔ", result)
			result = result + "≥…"

			return result
			
	if app.ENABLE_BATTLE_FIELD:
		def NumberToSecondaryCoinString(number, coinType):
			if number <= 0:
				number = 0

			coinTypeString = ""
			
			if coinType == shop.SHOP_COIN_TYPE_SECONDARY_COIN:
				coinTypeString = "¿¸"
			elif coinType == shop.SHOP_COIN_TYPE_BATTLE_POINT:
				coinTypeString = "πË∆≤∆˜¿Œ∆Æ"
			elif app.ENABLE_10TH_EVENT and coinType == shop.SHOP_COIN_TYPE_10TH_EVENT:
				coinTypeString = "±‚≥‰¡÷»≠"
			else:
				return "Not Valied"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "∏∏", result)
			result = CutMoneyString(number, 8, 12, "æÔ", result)

			return "%s %s" % (result, coinTypeString)
	else:
		def NumberToSecondaryCoinString(number):
			if number <= 0:
				return "0¿¸"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "∏∏", result)
			result = CutMoneyString(number, 8, 12, "æÔ", result)
			result = result + "¿¸"

			return result
	def FISHING_NOTIFY(isFish, fishName):
		if isFish:
			return fishName + I(fishName) + "πÆ µÌ «’¥œ¥Ÿ."
		else:
			return fishName + I(fishName) + "∞…∏∞µÌ «’¥œ¥Ÿ."

	def FISHING_SUCCESS(isFish, fishName):
		if isFish:
			return fishName + EUL(fishName) + "¿‚æ“Ω¿¥œ¥Ÿ!"
		else:
			return fishName + EUL(fishName) + "æÚæ˙Ω¿¥œ¥Ÿ!"

elif 932 == app.GetDefaultCodePage():
	def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
		if sellItemCount > 1 :
			return "%s %s å¬Ç %sÇ…îÑÇËÇ‹Ç∑Ç©ÅH" % ( sellItemName, sellItemCount, NumberToMoneyString(sellItemPrice) )
		else:
			return "%s Ç %sÇ≈îÑÇËÇ‹Ç∑Ç©ÅH" % (sellItemName, NumberToMoneyString(sellItemPrice) )

	def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice) :
		if buyItemCount > 1 :
			return "%s %så¬Ç %sÇ≈îÉÇ¢Ç‹Ç∑Ç©ÅH" % ( buyItemName, buyItemCount, buyItemPrice )
		else:
			return "%sÇ %sÇ≈îÉÇ¢Ç‹Ç∑Ç©ÅH" % ( buyItemName, buyItemPrice )
			
	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName) :
		return "%sÇëïíÖÇ≈Ç´Ç»Ç¢ÉAÉCÉe?Ç≈Ç∑ÅB" % (attachedItemName)

	def REFINE_FAILURE_NO_SOCKET(attachedItemName) :
		return "%sÇëïíÖÇ∑ÇÈ?ÉPÉbÉgÇ™Ç†ÇËÇ‹ÇπÇÒÅB" % (attachedItemName)

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName) :
		return "%sÇëïíÖÇ≈Ç´ÇÈâ©ã‡?ÉPÉbÉgÇ™Ç†ÇËÇ‹ÇπÇÒÅB" % (attachedItemName)
		
	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount) :
		if dropItemCount > 1 :
			return "%s %d å¬ÇéÃÇƒÇ‹Ç∑Ç©ÅH" % (dropItemName, dropItemCount)
		else :	
			return "%sÇéÃÇƒÇ‹Ç∑Ç©ÅH" % (dropItemName)

	def FISHING_NOTIFY(isFish, fishName) :
		if isFish :
			return "%s Ç™êHÇ¢Ç¬Ç¢ÇΩÇÊÇ§Ç≈Ç∑" % ( fishName )
		else :
			return "%s Ç™Ç©Ç©Ç¡ÇΩÇÊÇ§Ç≈Ç∑" % ( fishName )

	def FISHING_SUCCESS(isFish, fishName) :
		if isFish :
			return "%s ÇïﬂÇ‹Ç¶Ç‹ÇµÇΩÅI" % (fishName)
		else :
			return "%s ÇéËÇ…ì¸ÇÍÇ‹ÇµÇΩÅI" % (fishName)
			
	def NumberToMoneyString(number) :
		if number <= 0 :
			return "0óº"

		number = str(number)
		result = CutMoneyString(number, 0, 4, "", "")
		result = CutMoneyString(number, 4, 8, "ñú", result)
		result = CutMoneyString(number, 8, 12, "â≠", result)
		result = result + "óº"

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
			result = CutMoneyString(number, 4, 8, "ñú", result)
			result = CutMoneyString(number, 8, 12, "â≠", result)

			return "%s %s" % (result, coinTypeString)
	else:
		def NumberToSecondaryCoinString(number) :
			if number <= 0 :
				return "0jun"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "ñú", result)
			result = CutMoneyString(number, 8, 12, "â≠", result)
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
			return "»∑∂®“™∞—%s∏ˆ%s“‘%sΩ±“¬ÙµÙ¬£ø" % (str(sellItemCount), sellItemName, str(sellItemPrice))
		else:
			return "»∑∂®“™∞—%s“‘%sΩ±“¬ÙµÙ¬£ø" % (sellItemName, str(sellItemPrice))

	def DO_YOU_BUY_ITEM(sellItemName, sellItemCount, sellItemPrice):
		if sellItemCount>1:
			return "»∑∂®“™∞—%s∏ˆ%s“‘%sΩ±“¬ÚΩ¯¬£ø" % (str(sellItemCount), sellItemName, str(sellItemPrice))
		else:
			return "»∑∂®“™∞—%s“‘%sΩ±“¬ÚΩ¯¬£ø" % (sellItemName, str(sellItemPrice))

	def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName):
		return "Œﬁ∑®œ‚«∂%s µƒ◊∞±∏" % (attachedItemName)

	def REFINE_FAILURE_NO_SOCKET(attachedItemName):
		return "√ª”–ø…“‘œ‚«∂%s µƒø◊" % (attachedItemName)

	def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName):
		return "√ª”–ø…“‘œ‚«∂%s µƒª∆Ωø◊" % (attachedItemName)

	def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount):
		if dropItemCount>1:
			return "»∑∂®“™»”µÙ%d∏ˆ%s¬?" % (dropItemCount, dropItemName)
		else:
			return "»∑∂®“™»”µÙ%s¬?" % (dropItemName)

	def FISHING_NOTIFY(isFish, fishName):
		if isFish:
			return fishName # ∫ª∑° ø©±‚ø° æÓ∂≤ ∏ª¿Ã ∫ŸæÓ¿÷¥¬µ•, ¿Œƒ⁄µ˘¿Ã ±˙¡Æ¿÷æÓº≠ ∫πø¯«“ ºˆ∞° æ¯¥Ÿ §–§–... cythonø°º≠ ¿Œƒ⁄µ˘ ø°∑Ø ≥™º≠ ¡ˆøˆπˆ∏≤...
		else:
			return "µˆ◊≈" + fishName + "¡À°£"

	def FISHING_SUCCESS(isFish, fishName):
		if isFish:
			return "µˆ◊≈" + fishName + "¡À°£"
		else:
			return "ªÒµ√" + fishName + "¡À°£"

	def NumberToMoneyString(number):

		if number <= 0:
			return "0¡Ω"

		number = str(number)
		result = CutMoneyString(number, 0, 4, "", "")
		result = CutMoneyString(number, 4, 8, "ÕÚ", result)
		result = CutMoneyString(number, 8, 12, "“⁄", result)
		result = result + "¡Ω"

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
			result = CutMoneyString(number, 4, 8, "ÕÚ", result)
			result = CutMoneyString(number, 8, 12, "“⁄", result)

			return "%s %s" % (result, coinTypeString)
	else:
		def NumberToSecondaryCoinString(number):

			if number <= 0:
				return "0JUN"

			number = str(number)
			result = CutMoneyString(number, 0, 4, "", "")
			result = CutMoneyString(number, 4, 8, "ÕÚ", result)
			result = CutMoneyString(number, 8, 12, "“⁄", result)
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
