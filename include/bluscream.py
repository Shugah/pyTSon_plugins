from datetime import datetime
from PythonQt.QtGui import QInputDialog, QMessageBox, QDialog
from PythonQt.QtCore import Qt
from ts3plugin import PluginHost
import ts3lib, ts3defines

# GENERAL FUNCTIONS #


def timestamp():
    return '[{:%Y-%m-%d %H:%M:%S}] '.format(datetime.now())

# PARSING #

def channelURL(schid=None, cid=0, name=None):
    if schid == None:
        try: schid = ts3lib.getCurrentServerConnectionHandlerID()
        except: pass
    if name == None:
        try: (error, name) = ts3lib.getChannelVariable(schid, cid, ts3defines.ChannelProperties.CHANNEL_NAME)
        except: name = cid
    return '[b][url=channelid://{0}]"{1}"[/url][/b]'.format(cid, name)

def clientURL(schid=None, clid=0, uid=None, nickname=None):
    if schid == None:
        try: schid = ts3lib.getCurrentServerConnectionHandlerID()
        except: pass
    if uid == None:
        try: (error, uid) = ts3lib.getClientVariable(schid, clid, ts3defines.ClientProperties.CLIENT_UNIQUE_IDENTIFIER)
        except: pass
    if nickname == None:
        try: (error, nickname) = ts3lib.getClientVariable(schid, clid, ts3defines.ClientProperties.CLIENT_NICKNAME)
        except: nickname = uid
    return '[url=client://{0}/{1}]{2}[/url]'.format(clid, uid, nickname)

# GUI #

def inputBox(title, text):
    x = QDialog()
    x.setAttribute(Qt.WA_DeleteOnClose)
    return QInputDialog.getText(x, title, text)

def msgBox(text, icon=QMessageBox.Information):
    x = QMessageBox()
    x.setText(text)
    x.setIcon(icon)
    x.exec()

def confirm(title, message):
    x = QDialog()
    x.setAttribute(Qt.WA_DeleteOnClose)
    _x = QMessageBox.question(x, title, message, QMessageBox.Yes, QMessageBox.No)
    if _x == QMessageBox.Yes: return True if _x == QMessageBox.Yes else False

# AntiFlood

def getAntiFloodSettings(schid):
    (err, cmdblock) = ts3lib.getServerVariable(schid, ts3defines.VirtualServerPropertiesRare.VIRTUALSERVER_ANTIFLOOD_POINTS_NEEDED_COMMAND_BLOCK)
    (err, ipblock) = ts3lib.getServerVariable(schid, ts3defines.VirtualServerPropertiesRare.VIRTUALSERVER_ANTIFLOOD_POINTS_NEEDED_IP_BLOCK)
    (err, afreduce) = ts3lib.getServerVariable(schid, ts3defines.VirtualServerPropertiesRare.VIRTUALSERVER_ANTIFLOOD_POINTS_TICK_REDUCE)
    return (err, cmdblock, ipblock, afreduce)

def calculateInterval(schid, command, name="pyTSon"):
    # ts3lib.requestServerVariables(schid)
    (err, cmdblock, ipblock, afreduce) = getAntiFloodSettings(schid)
    # strange = False
    # for var in [cmdblock, ipblock, afreduce]:
        # if not var or var < 0 or var == "": strange = True
    # if err != ts3defines.ERROR_ok or strange:
        # ts3lib.requestServerVariables(schid)
        # (err, cmdblock, ipblock, afreduce) = getAntiFloodSettings(schid)
    interval = round(1000/((afreduce/command)))
    ts3lib.logMessage("{}: schid = {} | err = {} | afreduce = {} | cmdblock = {} | ipblock = {} | points_per_action = {} |interval = {}".format(name, schid, err, afreduce, cmdblock, ipblock, command, interval), ts3defines.LogLevel.LogLevel_INFO, "pyTSon", 0)
    return interval

# TS3Hook #

def sendCommand(name, cmd, schid=0):
    if PluginHost.cfg.getboolean("general", "verbose"):
        ts3lib.printMessage(ts3lib.getCurrentServerConnectionHandlerID(), '{timestamp} [color=orange]{name}[/color]:[color=white] {message}'.format(timestamp=timestamp(), name=name, message=cmd), ts3defines.PluginMessageTarget.PLUGIN_MESSAGE_TARGET_SERVER)
    cmd = cmd.replace(" ", "~s")
    if schid == 0: schid = ts3lib.getCurrentServerConnectionHandlerID()
    ts3lib.requestSendServerTextMsg(schid, "~cmd{}".format(cmd))

# DEFINES #

class AntiFloodPoints(object):
    AUTH = 0
    BANADD = 25
    BANCLIENT = 25
    BANDEL = 5
    BANDELALL = 5
    BANLIST = 25
    BINDINGLIST = 0
    CHANNELADDPERM = 5
    CHANNELCLIENTADDPERM = 5
    CHANNELCLIENTDELPERM = 5
    CHANNELCLIENTLIST = 0
    CHANNELCLIENTPERMLIST = 5
    CHANNELCONNECTINFO = 0
    CHANNELCREATE = 25
    CHANNELCREATEPRIVATE = 25
    CHANNELDELETE = 25
    CHANNELDELPERM = 5
    CHANNELEDIT = 25
    CHANNELFIND = 0
    CHANNELGETDESCRIPTION = 0
    CHANNELGROUPADD = 5
    CHANNELGROUPADDPERM = 5
    CHANNELGROUPCLIENTLIST = 5
    CHANNELGROUPCOPY = 5
    CHANNELGROUPDEL = 5
    CHANNELGROUPDELPERM = 5
    CHANNELGROUPLIST = 5
    CHANNELGROUPPERMLIST = 5
    CHANNELGROUPRENAME = 5
    CHANNELINFO = 0
    CHANNELLIST = 0
    CHANNELMOVE = 25
    CHANNELPERMLIST = 5
    CHANNELSUBSCRIBE = 15
    CHANNELSUBSCRIBEALL = 20
    CHANNELUNSUBSCRIBE = 5
    CHANNELUNSUBSCRIBEALL = 25
    CHANNELVARIABLE = 0
    CLIENTADDPERM = 5
    CLIENTCHATCLOSED = 5
    CLIENTCHATCOMPOSING = 0
    CLIENTDBDELETE = 25
    CLIENTDBEDIT = 25
    CLIENTDBFIND = 50
    CLIENTDBINFO = 0
    CLIENTDBLIST = 25
    CLIENTDELPERM = 5
    CLIENTDISCONNECT = 0
    CLIENTEDIT = 25
    CLIENTFIND = 0
    CLIENTGETDBIDFROMUID = 5
    CLIENTGETIDS = 5
    CLIENTGETNAMEFROMDBID = 5
    CLIENTGETNAMEFROMUID = 5
    CLIENTGETUIDFROMCLID = 5
    CLIENTGETVARIABLES = 0
    CLIENTINFO = 0
    CLIENTINIT = 0
    CLIENTINITIV = 0
    CLIENTKICK = 25
    CLIENTLIST = 0
    CLIENTMOVE = 10
    CLIENTMUTE = 10
    CLIENTNOTIFYREGISTER = 0
    CLIENTNOTIFYUNREGISTER = 0
    CLIENTPERMLIST = 5
    CLIENTPOKE = 25
    CLIENTSETSERVERQUERYLOGIN = 25
    CLIENTSITEREPORT = 0
    CLIENTUNMUTE = 10
    CLIENTUPDATE = 15
    CLIENTVARIABLE = 0
    COMPLAINADD = 25
    COMPLAINDEL = 5
    COMPLAINDELALL = 25
    COMPLAINLIST = 25
    CONNECTIONINFOAUTOUPDATE = 0
    CURRENTSCHANDLERID = 0
    CUSTOMINFO = 0
    CUSTOMSEARCH = 50
    DUMMY_CONNECTFAILED = 0
    DUMMY_CONNECTIONLOST = 0
    DUMMY_NEWIP = 0
    FTCREATEDIR = 5
    FTDELETEFILE = 5
    FTGETFILEINFO = 5
    FTGETFILELIST = 0
    FTINITDOWNLOAD = 0
    FTINITUPLOAD = 0
    FTLIST = 5
    FTRENAMEFILE = 5
    FTSTOP = 5
    GETCONNECTIONINFO = 0
    GM = 50
    HASHPASSWORD = 0
    HELP = 0
    INSTANCEEDIT = 25
    INSTANCEINFO = 0
    LOGADD = 0
    LOGIN = 0
    LOGOUT = 0
    LOGVIEW = 50
    MESSAGEADD = 25
    MESSAGEDEL = 5
    MESSAGEGET = 20
    MESSAGELIST = 25
    MESSAGEUPDATEFLAG = 5
    PERMFIND = 0
    PERMGET = 0
    PERMIDGETBYNAME = 0
    PERMISSIONLIST = 5
    PERMOVERVIEW = 5
    PERMRESET = 0
    PLUGINCMD = 5
    PRIVILEGEKEYADD = 0
    PRIVILEGEKEYDELETE = 0
    PRIVILEGEKEYLIST = 0
    PRIVILEGEKEYUSE = 0
    QUIT = 0
    SERVERCONNECTINFO = 0
    SERVERCONNECTIONHANDLERLIST = 0
    SERVERCREATE = 0
    SERVERDELETE = 0
    SERVEREDIT = 5
    SERVERGETVARIABLES = 0
    SERVERGROUPADD = 5
    SERVERGROUPADDCLIENT = 25
    SERVERGROUPADDPERM = 5
    SERVERGROUPAUTOADDPERM = 0
    SERVERGROUPAUTODELPERM = 0
    SERVERGROUPCLIENTLIST = 5
    SERVERGROUPCOPY = 5
    SERVERGROUPDEL = 5
    SERVERGROUPDELCLIENT = 25
    SERVERGROUPDELPERM = 5
    SERVERGROUPLIST = 5
    SERVERGROUPPERMLIST = 5
    SERVERGROUPRENAME = 5
    SERVERGROUPSBYCLIENTID = 5
    SERVERIDGETBYPORT = 0
    SERVERINFO = 0
    SERVERLIST = 0
    SERVERNOTIFYREGISTER = 0
    SERVERNOTIFYUNREGISTER = 0
    SERVERPROCESSSTOP = 0
    SERVERQUERYCMD = 5
    SERVERREQUESTCONNECTIONINFO  = 0
    SERVERSNAPSHOTCREATE = 0
    SERVERSNAPSHOTDEPLOY = 0
    SERVERSTART = 0
    SERVERSTOP = 0
    SERVERTEMPPASSWORDADD = 5
    SERVERTEMPPASSWORDDEL = 5
    SERVERTEMPPASSWORDLIST = 5
    SERVERVARIABLE = 0
    SETCLIENTCHANNELGROUP = 25
    SETCONNECTIONINFO = 0
    SETWHISPERLIST = 0
    TEXTMESSAGESEND = 15
    TOKENADD = 5
    TOKENDELETE = 5
    TOKENLIST = 5
    TOKENUSE = 5
    USE = 0
    VERIFYCHANNELPASSWORD = 5
    VERIFYSERVERPASSWORD = 5
    VERSION = 0
    WHOAMI = 0
