from utils import *
import os
import json
import webview
import install
import js_com

debug_mode = False

setting_window_handler = None


def open_setting_windows():
    global setting_window_handler
    win = webview.create_window("高级选项",
                                "./html/setting.html",
                                js_api=jsi,
                                width=575,
                                height=500)
    win.expose(close_setting_windows)
    setting_window_handler = win


def close_setting_windows():
    if setting_window_handler:
        setting_window_handler.destroy()


def quit_software():
    os._exit(0)


if __name__ == "__main__":
    custom_config = False
    custom_setting_pth = os.path.join(os.getcwd(), "custom_setting.json")
    # 判断是否加载自定义配置
    if os.path.exists(custom_setting_pth):
        with open(custom_setting_pth, 'r', encoding='utf-8') as fs:
            setting_dict = json.load(fs)
        if setting_dict["VERSION"] == 1:
            custom_config = True
    if not custom_config:
        default_setting_pth = os.path.join(install.file_pth, "config",
                                           "default_setting.json")
        with open(default_setting_pth, 'r', encoding='utf-8') as fs:
            setting_dict = json.load(fs)
    installer = install.Installer(
        os.path.join(os.getenv("APPDATA"), "PySuiter"), setting_dict)
    jsi = js_com.JSInterface(installer, custom_config)

    if check_webview2():
        main_ui = './html/index.html'
        render_core = 'edgechromium'
    else:
        main_ui = './html/index_ie.html'
        render_core = 'mshtml'

    main_windows = webview.create_window('PySuiter——一键安装python环境',
                                         main_ui,
                                         js_api=jsi,
                                         width=640,
                                         height=420,
                                         resizable=False)
    main_windows.expose(open_setting_windows, close_setting_windows,
                        quit_software)
    webview.start(debug=debug_mode, gui=render_core)