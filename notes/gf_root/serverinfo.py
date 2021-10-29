import os
import app
import localeInfo
import debugInfo

CHINA_PORT = 50000
import dbg
def LoadLoginInfo(REGION_NAME_DICT, REGION_AUTH_SERVER_DICT, REGION_DICT, MARKADDR_DICT, loginInfoFileName):
	def getValue(element, name, default):
		if [] != element.getElementsByTagName(name):
			return element.getElementsByTagName(name).item(0).firstChild.nodeValue
		else:
			return default
	try:
		from xml.dom.minidom import parse
		f = open(loginInfoFileName, "r")
		dom = parse(f)
		serverLst = dom.getElementsByTagName("server")

	except IOError:
		return

	regionIdx = len(REGION_DICT) - 1
	for server in serverLst:
		for i in range(0,server.attributes.length):
			item = server.attributes.item(i)
 
		name = server.attributes.getNamedItem("name").nodeValue
		auth_ip = server.getAttribute("auth_ip")
		auth_port = int(server.getAttribute("auth_port"))
		channelLst = server.getElementsByTagName("channel")
		channelDict = {}
		for idx, channel in enumerate(channelLst):
			channelInfo = {}
			channelInfo["key"] = int(channel.getAttribute("key"))
			channelInfo["name"] = channel.getAttribute("name")
			if channelInfo["name"] == "":
				channelInfo["name"] = "channel %d" % (idx + 1)
			channelInfo["ip"] = channel.getAttribute("ip")
			port = int(channel.getAttribute("port"))
			channelInfo["tcp_port"] = port
			channelInfo["udp_port"] = port
			channelInfo["state"] = STATE_NONE
			channelDict[idx + 1] = channelInfo
		serverIdx = len(REGION_DICT[regionIdx]) + 1
		REGION_AUTH_SERVER_DICT[regionIdx][serverIdx] = { "ip" : auth_ip, "port" : auth_port, }
		if app.ENABLE_SERVER_SELECT_RENEWAL:
			state = server.getAttribute("state")
			REGION_DICT[regionIdx][serverIdx] = { "name" : name, "channel" : channelDict, "state" : state }
		else:
			REGION_DICT[regionIdx][serverIdx] = { "name" : name, "channel" : channelDict, }
		MARKADDR_DICT[serverIdx * 10] = { 
							"ip" : channelDict[1]["ip"], "tcp_port" : channelDict[1]["tcp_port"], 
							"udp_port" : channelDict[1]["udp_port"],
							"mark" : "01.tga", "symbol_path" : str(serverIdx * 10), }

def BuildServerList(orderList):
	retMarkAddrDict = {}
	retAuthAddrDict = {}
	retRegion0 = {}

	ridx = 1
	for region, auth, mark, channels in orderList:
		cidx = 1
		channelDict = {}
		for channel in channels:
			key = ridx * 10 + cidx
			channel["key"] = key
			channelDict[cidx] = channel
			cidx += 1

		region["channel"] = channelDict

		retRegion0[ridx] = region
		retAuthAddrDict[ridx] = auth
		retMarkAddrDict[ridx*10] = mark
		ridx += 1

	return retRegion0, retAuthAddrDict, retMarkAddrDict

app.ServerName = None

if app.ENABLE_SERVER_SELECT_RENEWAL:
	STATE_NONE = localeInfo.CHANNEL_STATUS_OFFLINE
	STATE_DICT = {	0 : localeInfo.CHANNEL_STATUS_OFFLINE,
					1 : localeInfo.CHANNEL_STATUS_VACANT,
					2 : localeInfo.CHANNEL_STATUS_RECOMMENDED,
					3 : localeInfo.CHANNEL_STATUS_BUSY,
					4 : localeInfo.CHANNEL_STATUS_FULL,
					}

	STATE_REVERSE_DICT = {}
	STATE_COLOR_DICT = { "..." : 0xffdadada}	# ∆€∫Ì∏Æº≈ø°º≠ channelªÛ≈¬ø° ...¿ª ¿Ø¡ˆ«œµµ ¿÷æÓº≠ πÆ¡¶∞° πﬂª˝.
	STATE_COLOR_LIST = [ 0xffffffff, 0xffdadada, 0xff00ff00, 0xffffc000, 0xffff0000 ]
	
	idx = 0
	for key, value in STATE_DICT.items():
		STATE_REVERSE_DICT[value] = key
		STATE_COLOR_DICT[value] = STATE_COLOR_LIST[idx%len(STATE_COLOR_LIST)]
		idx += 1
	
	SERVER_STATE_DICT = { "NONE" : 0, "NEW" : 1, "SPECIAL" : 2, "CLOSE" : 3}

if (localeInfo.IsEUROPE() and app.GetLocalePath() == "locale/vn"):
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."

			STATE_DICT = {
				0 : "....",
				1 : "NORM",
				2 : "BUSY",
				3 : "FULL"
				}

	SERVER01_CHANNEL_DICT = {
		1:{"key":11,"name":"CH1   ","ip":"121.160.9.68","tcp_port":13002,"udp_port":13002,"state":STATE_NONE,},	
	}
	
	REGION_NAME_DICT = {
		0 : "Vietnam",		
	}

	REGION_AUTH_SERVER_DICT = {
		0 : {
			1 : { "ip":"121.160.9.68", "port":11002, },
	
		}		
	}

	REGION_DICT = {
		0 : {
			1 : { "name" :"Vietnam1", "channel" : SERVER01_CHANNEL_DICT, },						
		},
	}

	MARKADDR_DICT = {
		10 : { "ip" : "121.160.9.68", "tcp_port" : 13002, "mark" : "10.tga", "symbol_path" : "10", },
	}

	TESTADDR = { "ip" : "210.123.10.153", "tcp_port" : 50000, "udp_port" : 50000, }

if (localeInfo.IsEUROPE() and app.GetLocalePath() == "locale/sg"):
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."

			STATE_DICT = {
				0 : "....",
				1 : "NORM",
				2 : "BUSY",
				3 : "FULL"
				}

	SERVER01_CHANNEL_DICT = {
		1:{"key":11,"name":"CH1   ","ip":"120.29.208.231","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		2:{"key":12,"name":"CH2   ","ip":"120.29.208.232","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		3:{"key":13,"name":"CH3   ","ip":"120.29.208.233","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		4:{"key":14,"name":"CH4   ","ip":"120.29.208.234","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
	}
	
	REGION_NAME_DICT = {
		0 : "Singapore",		
	}

	REGION_AUTH_SERVER_DICT = {
		0 : {
			1 : { "ip":"120.29.208.227", "port":11000, },
	
		}		
	}

	REGION_DICT = {
		0 : {
			1 : { "name" :"Singapore", "channel" : SERVER01_CHANNEL_DICT, },						
		},
	}

	MARKADDR_DICT = {
		10 : { "ip" : "120.29.208.231", "tcp_port" : 13000, "mark" : "10.tga", "symbol_path" : "10", },
	}

	TESTADDR = { "ip" : "210.123.10.153", "tcp_port" : 50000, "udp_port" : 50000, }

if (localeInfo.IsEUROPE() and app.GetLocalePath() == "locale/ca"):
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."

			STATE_DICT = {
				0 : "....",
				1 : "NORM",
				2 : "BUSY",
				3 : "FULL"
				}

	SERVER01_CHANNEL = [
		{"name":"CH11   ","ip":"74.200.6.201","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH12   ","ip":"74.200.6.202","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH13   ","ip":"74.200.6.203","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH14   ","ip":"74.200.6.204","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH15   ","ip":"74.200.6.205","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH16   ","ip":"74.200.6.206","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
	]
	SERVER02_CHANNEL =[
		{"name":"CH21   ","ip":"74.200.6.211","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH22   ","ip":"74.200.6.212","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH23   ","ip":"74.200.6.213","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH24   ","ip":"74.200.6.214","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH25   ","ip":"74.200.6.215","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"CH26   ","ip":"74.200.6.216","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
	]
	
	SERVER01_MARK = { "ip" : "74.200.6.202", "tcp_port" : 13000, "mark" : "10.tga", "symbol_path" : "10",}
	SERVER02_MARK = { "ip" : "74.200.6.212", "tcp_port" : 13000, "mark" : "20.tga", "symbol_path" : "20",}

	SERVER01_AUTH = {  "ip":"74.200.6.209", "port":11001, }			#Freekingdom
	SERVER02_AUTH = {  "ip":"74.200.6.209", "port":11002, }			#new world

	SERVER01 = { "name" : "FREE KINGDOM" } 
	SERVER02 = { "name" : "NEW WORLD" } 

	TESTADDR = { "ip" : "210.123.10.153", "tcp_port" : 50000, "udp_port" : 50000, }

	REGION0_ORDER_LIST = [
		(SERVER02, SERVER02_AUTH, SERVER02_MARK, SERVER02_CHANNEL),
		(SERVER01, SERVER01_AUTH, SERVER01_MARK, SERVER01_CHANNEL),
		]
		
	# BUILD
	NEW_REGION0, NEW_REGION0_AUTH_SERVER_DICT, NEW_MARKADDR_DICT = BuildServerList(REGION0_ORDER_LIST)

	# RESULT
	NEW_REGION_NAME_DICT = {
		0 : "CANADA",		
	}

	NEW_REGION_AUTH_SERVER_DICT = {
		0 : NEW_REGION0_AUTH_SERVER_DICT,
	}

	NEW_REGION_DICT = {
		0 : NEW_REGION0,
	}

	MARKADDR_DICT = NEW_MARKADDR_DICT
	REGION_DICT = NEW_REGION_DICT
	REGION_NAME_DICT = NEW_REGION_NAME_DICT
	REGION_AUTH_SERVER_DICT = NEW_REGION_AUTH_SERVER_DICT

if (localeInfo.IsEUROPE() and app.GetLocalePath() == "locale/br"):
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."

			STATE_DICT = {
				0 : "....",
				1 : "NORM",
				2 : "BUSY",
				3 : "FULL"
				}

	YAMI_CHANNEL = [
		{"name":"YAMI-1   ","ip":"201.77.235.51","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"YAMI-2   ","ip":"201.77.235.51","tcp_port":13100,"udp_port":13100,"state":STATE_NONE,},	
		{"name":"YAMI-3   ","ip":"201.77.235.52","tcp_port":13200,"udp_port":13200,"state":STATE_NONE,},	
		{"name":"YAMI-4   ","ip":"201.77.235.52","tcp_port":13400,"udp_port":13400,"state":STATE_NONE,},	
		{"name":"YAMI-5   ","ip":"201.77.235.53","tcp_port":13500,"udp_port":13500,"state":STATE_NONE,},	
	]

	HIKARI_CHANNEL = [
		{"name":"HIKARI-1   ","ip":"201.77.235.54","tcp_port":13000,"udp_port":13000,"state":STATE_NONE,},	
		{"name":"HIKARI-2   ","ip":"201.77.235.54","tcp_port":13100,"udp_port":13100,"state":STATE_NONE,},	
		{"name":"HIKARI-3   ","ip":"201.77.235.55","tcp_port":13200,"udp_port":13200,"state":STATE_NONE,},	
		{"name":"HIKARI-4   ","ip":"201.77.235.55","tcp_port":13400,"udp_port":13400,"state":STATE_NONE,},	
		{"name":"HIKARI-5   ","ip":"201.77.235.56","tcp_port":13500,"udp_port":13500,"state":STATE_NONE,},	
	]

	YAMI_MARK = { "ip" : "201.77.235.51", "tcp_port" : 13000, "mark" : "10.tga", "symbol_path" : "10", }	
	HIKARI_MARK = { "ip" : "201.77.235.54", "tcp_port" : 13000, "mark" : "10.tga", "symbol_path" : "10", }	
		
	YAMI_AUTH = { "ip":"201.77.235.50", "port":11001, }
	HIKARI_AUTH = { "ip":"201.77.235.50", "port":11002, }
	

	YAMI = { "name" : "YAMI" }						
	HIKARI = { "name" : "HIKARI"}					


	TESTADDR = { "ip" : "210.123.10.153", "tcp_port" : 50000, "udp_port" : 50000, }
	
	REGION0_ORDER_LIST = [
		(YAMI, YAMI_AUTH, YAMI_MARK, YAMI_CHANNEL),
		(HIKARI, HIKARI_AUTH, HIKARI_MARK, HIKARI_CHANNEL),
		]
	# BUILD
	NEW_REGION0, NEW_REGION0_AUTH_SERVER_DICT, NEW_MARKADDR_DICT = BuildServerList(REGION0_ORDER_LIST)

	# RESULT
	NEW_REGION_NAME_DICT = {
		0 : "BRAZIL",		
	}

	NEW_REGION_AUTH_SERVER_DICT = {
		0 : NEW_REGION0_AUTH_SERVER_DICT,
	}

	NEW_REGION_DICT = {
		0 : NEW_REGION0,
	}

	MARKADDR_DICT = NEW_MARKADDR_DICT
	REGION_DICT = NEW_REGION_DICT
	REGION_NAME_DICT = NEW_REGION_NAME_DICT
	REGION_AUTH_SERVER_DICT = NEW_REGION_AUTH_SERVER_DICT

if localeInfo.IsNEWCIBN():
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Œ¨ª§÷–"
			STATE_DICT = { 0 : "Œ¨ª§÷–", 1 : "’˝≥£",	2 : "∑±√¶",	3 : "±¨¬˙" }
			STATE_COLOR_DICT = { "Œ¨ª§÷–" : 0xffdadada, "’˝≥£" : 0xff00ff00, "∑±√¶" : 0xffffff00, "±¨¬˙" : 0xffff0000}
		else:
			STATE_NONE = "..."
						
			STATE_DICT = {
				0 : "Œ¨ª§÷–",
				1 : "’˝≥£",
				2 : "∑±√¶",
				3 : "±¨¬˙"
			}


	TE1_CHANNELS = [
		{"name":"“ªœﬂ","ip":"118.26.152.83","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
		{"name":"∂˛œﬂ","ip":"118.26.152.84","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
		{"name":"»˝œﬂ","ip":"118.26.152.85","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
		{"name":"Àƒœﬂ","ip":"118.26.152.88","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},
	]

	TE2_CHANNELS = [
		{"name":"“ªœﬂ","ip":"118.26.152.86","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
		{"name":"∂˛œﬂ","ip":"118.26.152.87","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
		{"name":"»˝œﬂ","ip":"118.26.152.143","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
		{"name":"Àƒœﬂ","ip":"118.26.152.144","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
		{"name":"ŒÂœﬂ","ip":"118.26.152.146","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
#		{"name":"¡˘œﬂ","ip":"118.26.152.146","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},	
	]

	TE1_MARK = { "ip" : "118.26.152.83",	"tcp_port" : 11000, "mark" : "50.tga", "symbol_path" : "50", }
	TE2_MARK = { "ip" : "118.26.152.86",	"tcp_port" : 11000, "mark" : "50.tga", "symbol_path" : "50", }

	TE1_AUTH = { "ip":"218.240.37.93",	"port":10001, }
	TE2_AUTH = { "ip":"218.240.37.94",	"port":10001, }

	TE1 = { "name" : "÷¬πÃÏœ¬[»´Õ¯] <∫œ>"}
	TE2 = { "name" : "ŒÂ–€’˘∞‘[»´Õ¯] <–¬>"}

	TESTADDR = { "ip" : "218.99.6.74", "tcp_port" : 11000, "udp_port" : 11000, }

	# ORDER
	REGION0_ORDER_LIST = [
		(TE2, TE2_AUTH, TE2_MARK, TE2_CHANNELS),
		(TE1, TE1_AUTH, TE1_MARK, TE1_CHANNELS),
	]

	# BUILD
	NEW_REGION0, NEW_REGION0_AUTH_SERVER_DICT, NEW_MARKADDR_DICT = BuildServerList(REGION0_ORDER_LIST)

	# RESULT
	NEW_REGION_NAME_DICT = {
		0 : "CHINA_NEWCIBN",		
	}

	NEW_REGION_AUTH_SERVER_DICT = {
		0 : NEW_REGION0_AUTH_SERVER_DICT,
	}

	NEW_REGION_DICT = {
		0 : NEW_REGION0,
	}

	MARKADDR_DICT = NEW_MARKADDR_DICT
	REGION_DICT = NEW_REGION_DICT
	REGION_NAME_DICT = NEW_REGION_NAME_DICT
	REGION_AUTH_SERVER_DICT = NEW_REGION_AUTH_SERVER_DICT

elif localeInfo.IsJAPAN():
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."
					
			STATE_DICT = {
				0 : "...",
				1 : "ê≥èÌ",
				2 : "ç¨éG",
				3 : "FULL"
			}

	SERVER01_CHANNEL_DICT = {
		1:{"key":11,"name":"CHANNEL1   ","ip":"202.229.16.24","tcp_port":11000,"udp_port":11000,"state":STATE_NONE,},
		#2:{"key":12,"name":"CHANNEL2   ","ip":"202.229.16.24","tcp_port":12000,"udp_port":12000,"state":STATE_NONE,},
	}

	MARKADDR_DICT = {
		10 : { "ip" : "202.229.16.24", "tcp_port" : 11000, "mark" : "10.tga", "symbol_path" : "10", },
	}

	REGION_NAME_DICT = {
		0 : "JAPAN",
	}

	REGION_AUTH_SERVER_DICT = {
		0 : {
			1 : { "ip":"202.229.16.24", "port":10001, },
		}
	}

	REGION_DICT = {
		0 : {
			1 : { "name" : "âûó≥", "channel" : SERVER01_CHANNEL_DICT, },
		},
	}

	TESTADDR = { "ip" : "202.229.16.4", "tcp_port" : 50000, "udp_port" : 50000, }


elif localeInfo.IsYMIR():
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."	
					
			STATE_DICT = {
			0 : "¡°∞À",
			1 : "∫∏≈Î",
			2 : "»•¿‚",
			3 : "FULL"
			}

	SERVER01_CHANNEL_DICT = {
		1:{"key":11,"name":"√§≥Œ 1   ","ip":"202.31.212.51","tcp_port":50010,"udp_port":51000,"state":STATE_NONE,},
		2:{"key":12,"name":"√§≥Œ 2   ","ip":"202.31.212.51","tcp_port":50020,"udp_port":52000,"state":STATE_NONE,},
		3:{"key":13,"name":"√§≥Œ 3   ","ip":"202.31.212.51","tcp_port":50030,"udp_port":50030,"state":STATE_NONE,},
		4:{"key":14,"name":"√§≥Œ 4   ","ip":"202.31.212.51","tcp_port":50040,"udp_port":50040,"state":STATE_NONE,},
#		5:{"key":15,"name":"√§≥Œ 5   ","ip":"202.31.212.51","tcp_port":50051,"udp_port":50051,"state":STATE_NONE,},		
#		5:{"key":15,"name":"π´«—¥Î¿¸ ","ip":"220.95.239.35","tcp_port":50100,"udp_port":50100,"state":STATE_NONE,},		
	}

	#6:{"key":16,"name":"¥Î∑√ ¿Ã∫•∆Æ","ip":"220.95.239.35","tcp_port":50100,"udp_port":50100,"state":STATE_NONE,},

	REGION_NAME_DICT = {
		0 : "KOREA",		
	}

	REGION_AUTH_SERVER_DICT = {
		0 : {
			1 : { "ip":"202.31.212.51", "port":51000, },
			2 : { "ip":"202.31.212.15", "port":51000, },
		}		
	}

	REGION_DICT = {
		0 : {
			1 : { "name" : "√µ∏∂ º≠πˆ", "channel" : SERVER01_CHANNEL_DICT, },
		},
	}

	MARKADDR_DICT = {
		10 : { "ip" : "202.31.212.51", "tcp_port" : 50040, "mark" : "01.tga", "symbol_path" : "10", },
	}

	TESTADDR = { "ip" : "220.95.239.62", "tcp_port" : 50000, "udp_port" : 50000, }

elif localeInfo.IsWE_KOREA():
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."
						
						
			STATE_DICT = {
				0 : "¡°∞À",
				1 : "∫∏≈Î",
				2 : "»•¿‚",
				3 : "FULL"
			}


	SERVER01_CHANNEL_DICT = {
		1:{"key":11,"name":"√§≥Œ 1   ","ip":"202.31.212.15","tcp_port":50010,"udp_port":50010,"state":STATE_NONE,},	
		2:{"key":12,"name":"√§≥Œ 2   ","ip":"202.31.212.15","tcp_port":50020,"udp_port":50020,"state":STATE_NONE,},	
	}

	REGION_NAME_DICT = {
		0 : "KOREA",		
	}

	REGION_AUTH_SERVER_DICT = {
		0 : {
			1 : { "ip":"202.31.212.15", "port":51000, },
		}		
	}

	REGION_DICT = {
		0 : {
			1 : { "name" : "ƒËµµ º≠πˆ", "channel" : SERVER01_CHANNEL_DICT, },
		},
	}

	MARKADDR_DICT = {
		10 : { "ip" : "202.31.212.15", "tcp_port" : 50040, "mark" : "02.tga", "symbol_path" : "20", },
	}

	TESTADDR = { "ip" : "220.95.239.62", "tcp_port" : 50000, "udp_port" : 50000, }

elif localeInfo.IsTAIWAN():
	if not app.ENABLE_SERVER_SELECT_RENEWAL:
		if app.ENABLE_CHANNEL_LIST:
			STATE_NONE = "Offline"
			STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
			STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
		else:
			STATE_NONE = "..."

			STATE_DICT = {
				0 : "....",
				1 : "NORM",
				2 : "BUSY",
				3 : "FULL"
			}

	SERVER01_CHANNEL_DICT = {
		1:{"key":11,"name":"CHANNEL1   ","ip":"203.69.141.201","tcp_port":50010,"udp_port":50010,"state":STATE_NONE,},
		2:{"key":12,"name":"CHANNEL2   ","ip":"203.69.141.201","tcp_port":50020,"udp_port":50020,"state":STATE_NONE,},
	}

	MARKADDR_DICT = {
		10 : { "ip" : "203.69.141.201", "tcp_port" : 50010, "mark" : "10.tga", "symbol_path" : "10", },
	}

	REGION_NAME_DICT = {
		0 : "TAIWAN",
	}

	REGION_AUTH_SERVER_DICT = {
		0 : {
			1 : { "ip":"203.69.141.201", "port":51000, },
		}
	}

	REGION_DICT = {
		0 : {
			1 : { "name" : "¿sæs", "channel" : SERVER01_CHANNEL_DICT, },
		},
	}

	TESTADDR = { "ip" : "203.69.141.201", "tcp_port" : 50000, "udp_port" : 50000, }
			
if localeInfo.IsEUROPE():
	name = app.GetLocalePath().replace("/", "_") + ".addr"
	path = os.sep.join(("pack", name))
	if os.access(path, os.R_OK):
		print "load_locale_addr:", path

		data = app.LoadLocaleAddr(path)

		import cPickle
		import cStringIO
		info = cPickle.load(cStringIO.StringIO(data))


		if not app.ENABLE_SERVER_SELECT_RENEWAL:
			if app.ENABLE_CHANNEL_LIST:
				STATE_NONE = "Offline"
				STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
				STATE_COLOR_DICT = { "..." : 0xffdadada, "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
			else:
				STATE_NONE = "..."

				STATE_DICT = {
					0 : "....",
					1 : "NORM",
					2 : "BUSY",
					3 : "FULL"
					}
		
		SERVER_ID_DICT = info["SERVERID"]
		REGION_NAME_DICT = info["NAME"]
		REGION_AUTH_SERVER_DICT = info["AUTHADDR"]
		REGION_DICT = info["GAMEADDR"]
		MARKADDR_DICT = info["MARKADDR"]
		
LoadLoginInfo(REGION_NAME_DICT, REGION_AUTH_SERVER_DICT, REGION_DICT, MARKADDR_DICT, "logininfo.xml")
