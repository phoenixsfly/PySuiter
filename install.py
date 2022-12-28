import os
import json
import subprocess
import sys
from utils import *

file_pth, _ = os.path.split(__file__)


class Installer:

    def __init__(self, target_pth, setting_dict) -> None:
        self.target_pth = target_pth
        self.setting_dict = setting_dict
        self.added_env = []
        self.install_completed = False
        self.install_state_text = "准备安装"
        self.logfile = open(os.path.join(os.getenv("TEMP"), "install.log"),
                            'w+',
                            encoding='utf-8')
        sys.stdout = self.logfile

    def __del__(self):
        self.logfile.close()

    def _install_python(self):
        setting_dict = self.setting_dict['PYTHON']
        target_pth = os.path.abspath(self.target_pth)
        print(setting_dict)
        pyv = setting_dict["PythonAvailableVersion"][
            setting_dict['PythonSelectVersion']]
        python_down_url = f"https://registry.npmmirror.com/-/binary/python/{pyv}/python-{pyv}-embed-amd64.zip"
        py_install_pth = os.path.join(target_pth,
                                      "Python3" + pyv.split('.')[1])

        #下载并安装python
        self.install_state_text = "正在安装Python解释器"
        print("正在安装python解释器...")
        download_file(python_down_url, os.getenv("Temp"), f"python{pyv}.zip")
        unzip_file(os.path.join(os.getenv("Temp"), f"python{pyv}.zip"),
                   py_install_pth)

        with open(
                os.path.join(py_install_pth,
                             f"python3{pyv.split('.')[1]}._pth"), "a+") as f:
            f.write("import site")

        # 设置环境变量
        self.added_env.append(py_install_pth)
        self.added_env.append(os.path.join(py_install_pth, 'Scripts'))
        os.environ[
            'PATH'] += f";{py_install_pth};{os.path.join(py_install_pth,'Scripts')}"

        # 设置pip源为清华镜像源
        pip_ini_pth = os.path.join(os.getenv("AppData"), "pip")
        if not os.path.exists(pip_ini_pth):
            os.makedirs(pip_ini_pth)
        with open(os.path.join(pip_ini_pth, "pip.ini"), "w") as pip_ini:
            pip_ini.write(
                "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple"
            )
        # 安装pip
        self.install_state_text = "正在安装pip"
        print("正在安装pip...")
        get_pip_pth = os.path.join(file_pth, "third_party", "get-pip.py")
        subprocess.run(
            f"{os.path.join(py_install_pth,'python.exe')} {get_pip_pth}",
            shell=True,
            stdout=self.logfile)
        self.install_state_text = "正在安装扩展库"
        print("正在安装第三方库...")
        subprocess.run(
            f"pip.exe install {' '.join(setting_dict['ExtraModule'])}",
            cwd=os.path.join(py_install_pth, 'Scripts'),
            shell=True,
            stdout=self.logfile)

    def _install_vscode(self):
        self.install_state_text = "正在安装VSCode编辑器"
        setting_dict = self.setting_dict['VSCODE']
        if not setting_dict['Installation']:
            return
        target_pth = os.path.abspath(self.target_pth)
        vsc_install_pth = os.path.join(target_pth, "Microsoft VS Code")
        self.vsc_install_pth = vsc_install_pth
        print("正在安装Visual Studio Code...")
        # 下载VSCode压缩包
        download_file(
            "https://vscode.cdn.azure.cn/stable/e8a3071ea4344d9d48ef8a4df2c097372b0c5161/VSCode-win32-x64-1.74.2.zip",
            os.getenv("Temp"), "vscode.zip")
        unzip_file(os.path.join(os.getenv("Temp"), "vscode.zip"),
                   vsc_install_pth)

        # 设置环境变量
        self.added_env.append(os.path.join(vsc_install_pth, 'bin'))
        os.environ['PATH'] += f";{os.path.join(vsc_install_pth,'bin')}"

        self.install_state_text = "正在安装VSCode插件"
        print("正在安装Visual Studio Code插件")
        subprocess.run(
            "code --install-extension MS-CEINTL.vscode-language-pack-zh-hans",
            cwd=os.path.join(vsc_install_pth, 'bin'),
            shell=True,
            stdout=self.logfile)
        subprocess.run("code --install-extension ms-python.python",
                       cwd=os.path.join(vsc_install_pth, 'bin'),
                       shell=True,
                       stdout=self.logfile)

        # 设置中文
        argv_pth = os.path.join(os.path.expanduser("~"), '.vscode',
                                "argv.json")
        if not os.path.exists(argv_pth):
            with open(argv_pth, "w") as argf:
                argf.write("{\n\"locale\":\"zh-cn\" \n}")
        else:
            with open(argv_pth, "r+") as argf:
                argvs = json.load(argf)
                argvs["locale"] = "zh-cn"
                json.dump(argvs, argf)

        #创建桌面快捷方式
        if setting_dict['Shortcut']:
            print("正在创建桌面快捷方式")
            create_shortcut(
                os.path.join(vsc_install_pth, "Code.exe"),
                os.path.join(os.path.expanduser("~"), 'Desktop',
                             "Visual Studio Code.lnk"))

    def _env_path_configure(self):
        print("正在设置环境变量")
        path_str = ';'.join(self.added_env)
        print(path_str)
        subprocess.run(f"setx PATH \"%PATH%;{path_str}\"",
                       shell=True,
                       stdout=self.logfile)

    def execute_install(self):
        self._install_python()
        self._install_vscode()
        self._env_path_configure()
        self.install_state_text = "完成安装"
        self.install_completed = True

    def open_helloworld_project(self):
        project_pth = os.path.join(os.path.expanduser("~"), "Documents",
                                   "Sources", "HelloWorld")
        if not os.path.exists(project_pth):
            os.makedirs(project_pth)

        with open(os.path.join(project_pth, 'main.py'), 'w',
                  encoding='utf-8') as mainf:
            mainf.write("# 点击右上角三角按钮运行你的第一个程序吧~ \n")
            mainf.write("print('Hello World')")

        # vscode首次启动无论如何都是显示英文，第二次启动才能正确加载语言界面，很是奇怪
        # subprocess.run(f"code --locale=zh-cn",
        #                cwd=os.path.join(self.vsc_install_pth, 'bin'),
        #                shell=True,
        #                stdout=self.logfile)
        subprocess.run(
            f"code --locale=zh-cn -n {project_pth} -g {os.path.join(project_pth,'main.py')} ",
            cwd=os.path.join(self.vsc_install_pth, 'bin'),
            shell=True,
            stdout=self.logfile)
