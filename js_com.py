import webview
from copy import deepcopy
import os
import json
import install


class JSInterface:

    def __init__(self, installer, custom_config=False) -> None:
        self.installer = installer
        self.is_custom = custom_config

    def getIsCustom(self):
        return self.is_custom

    def getSettingJSON(self):
        return self.installer.setting_dict

    def setSettingJSON(self, setting_dict):
        self.installer.setting_dict = setting_dict

    def getInstallPath(self):
        return self.installer.target_pth

    def setInstallPath(self, pth):
        self.installer.target_pth = os.path.abspath(pth)

    def execute_install(self):
        self.installer.execute_install()

    def export_setting(self):
        custom_setting_dict = deepcopy(self.installer.setting_dict)
        custom_setting_dict["AUTHOR"] = '未知来源'
        with open("./custom_setting.json", 'w', encoding='utf-8') as f:
            json.dump(custom_setting_dict, f, ensure_ascii=False)

    def getInstallStateText(self):
        if not hasattr(self, 'installer'):
            return "准备安装"
        return self.installer.install_state_text

    def getInstallCompleted(self):
        return hasattr(self, 'installer') and self.installer.install_completed

    def openHelloWorld(self):
        self.installer.open_helloworld_project()