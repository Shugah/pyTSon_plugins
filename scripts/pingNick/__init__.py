import ts3defines, ts3lib
from ts3plugin import ts3plugin
from datetime import datetime
from PythonQt.QtCore import QTimer


class pingNick(ts3plugin):
    name = "Ping Nickname"

    apiVersion = 22
    requestAutoload = False
    version = "1.0"
    author = "Bluscream"
    description = "Automatically enable channel commander when switching channels.\n\nCheck out https://r4p3.net/forums/plugins.68/ for more plugins."
    offersConfigure = False
    commandKeyword = ""
    infoTitle = None
    menuItems = [(ts3defines.PluginMenuType.PLUGIN_MENU_TYPE_GLOBAL, 0, "Toggle Auto Ping as nickname", "")]
    hotkeys = []
    timer = None
    debug = False
    prefix = ""
    suffix = "ms :O"
    int = 0
    lastPing = 0

    @staticmethod
    def timestamp(): return '[{:%Y-%m-%d %H:%M:%S}] '.format(datetime.now())

    def __init__(self):
        if self.debug: ts3lib.printMessageToCurrentTab("{0}[color=orange]{1}[/color] Plugin for pyTSon by [url=https://github.com/{2}]{2}[/url] loaded.".format(self.timestamp(),self.name,self.author))

    def onMenuItemEvent(self, schid, atype, menuItemID, selectedItemID):
        if menuItemID == 0:
            if self.timer == None:
                self.timer = QTimer()
                self.timer.timeout.connect(self.tick)
            if self.timer.isActive():
                self.timer.stop()
                self.timer = None
                ts3lib.printMessageToCurrentTab('Timer stopped!')
            else:
                self.timer.start(1000)
                ts3lib.printMessageToCurrentTab('Timer started!')
            ts3lib.printMessageToCurrentTab("{0}Set {1} to [color=yellow]{2}[/color]".format(self.timestamp(),self.name,self.toggle))

    def tick(self,schid=0, clid=0):
        if schid == 0: schid = ts3lib.getCurrentServerConnectionHandlerID()
        if clid == 0: (err, clid) = ts3lib.getClientID(schid)
        if schid == 0 or clid == 0: return
        if self.debug: self.int += 1;ts3lib.printMessageToCurrentTab('Tick %s'%self.int)
        (err, ping) = ts3lib.getConnectionVariableAsUInt64(schid, clid, ts3defines.ConnectionProperties.CONNECTION_PING)
        if ping == self.lastPing: return
        ts3lib.setClientSelfVariableAsString(schid, ts3defines.ClientProperties.CLIENT_NICKNAME, "{0}{1}{2}".format(self.prefix, ping, self.suffix))
        ts3lib.flushClientSelfUpdates(schid)
        self.lastPing = ping