import sys
import os
import subprocess
import re
import requests
requests.packages.urllib3.disable_warnings()
#from pygame import mixer
from PyQt6 import QtCore, QtGui, QtWidgets 
from PyQt6.QtCore import *
from PyQt6.QtGui import *

#------ui------
from GUI.Ui_main import Ui_MainWindow

print(os.path.join(os.path.dirname(__file__)))
    
class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon(self.loadResources('icon.ico')))
        self.setAcceptDrops(True)

        self.action()
        self.LinkStart()


    def loadResources(self,file_name: str) -> str:
        return os.path.join(os.path.dirname(__file__), file_name)
    
    #connect btn
    def action(self):
        self.btnSelectHero_3151.clicked.connect(lambda: self.select_hero(3151))
        self.btnSelectHero_3153.clicked.connect(lambda: self.select_hero(3153))
        self.btnSelectHero_3152.clicked.connect(lambda: self.select_hero(3152))

        self.btnSelectHero_3678.clicked.connect(lambda: self.select_hero(3678))
        self.btnSelectHero_3156.clicked.connect(lambda: self.select_hero(3156))
        self.btnSelectHero_3157.clicked.connect(lambda: self.select_hero(3157))

        self.btnSelectHero_3147.clicked.connect(lambda: self.select_hero(3147))
        self.btnSelectHero_3159.clicked.connect(lambda: self.select_hero(3159))
        self.btnSelectHero_3947.clicked.connect(lambda: self.select_hero(3947))

        self.btnSelectHero_350.clicked.connect(lambda: self.select_hero(350))



        self.btnSelectHero_3151.setIcon(QtGui.QIcon(self.loadResources('res/3151.png')))
        self.btnSelectHero_3153.setIcon(QtGui.QIcon(self.loadResources('res/3153.png')))
        self.btnSelectHero_3152.setIcon(QtGui.QIcon(self.loadResources('res/3152.png')))

        self.btnSelectHero_3678.setIcon(QtGui.QIcon(self.loadResources('res/3678.png')))
        self.btnSelectHero_3156.setIcon(QtGui.QIcon(self.loadResources('res/3156.png')))
        self.btnSelectHero_3157.setIcon(QtGui.QIcon(self.loadResources('res/3157.png')))

        self.btnSelectHero_3147.setIcon(QtGui.QIcon(self.loadResources('res/3147.png')))
        self.btnSelectHero_3159.setIcon(QtGui.QIcon(self.loadResources('res/3159.png')))
        self.btnSelectHero_3947.setIcon(QtGui.QIcon(self.loadResources('res/3947.png')))
        self.btnSelectHero_350.setIcon(QtGui.QIcon(self.loadResources('res/yuumi1.png')))

    def select_hero(self, id):
        self.SelectHero(id)

    def LinkStart(self):
        output = subprocess.check_output("wmic process where caption='LeagueClientUx.exe' get commandline", shell=True)
        output_str = output.decode('utf-8')

        token_pattern = r'--remoting-auth-token=([\w-]+)'
        port_pattern = r'--app-port=(\d+)'

        token_match = re.search(token_pattern, output_str)
        port_match = re.search(port_pattern, output_str)

        token = token_match.group(1) if token_match else 'Token not found'
        port = port_match.group(1) if port_match else 'Port not found'

        self.baseUrl = f"https://riot:{token}@127.0.0.1:{port}"

        #print(self.baseUrl)
        self.get_summoner_data()

    
    def get_summoner_data(self):
        r = requests.get(f'{self.baseUrl}/lol-summoner/v1/current-summoner',verify=False)
        summoner = r.json()

        self.UserInfoText.setText(summoner['displayName'])

    def SelectHero(self,id):
        data={"data":{"championId":id}}
        ret = requests.patch(f'{self.baseUrl}/lol-settings/v2/account/LCUPreferences/STRAWBERRY_LOCAL_SETTINGS_V1', json=data,verify=False)
        #print(ret)

        data=[{"championId":id,"positionPreference":"UNSELECTED","spell1":1,"spell2":1}]
        ret = requests.put(f'{self.baseUrl}/lol-lobby/v1/lobby/members/localMember/player-slots', verify=False, json=data)
        #print(ret)





if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    app.exec()


