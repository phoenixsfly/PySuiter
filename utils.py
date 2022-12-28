import requests
import urllib.parse
import win32com.client
import winreg
import os
from zipfile import ZipFile
from contextlib import closing


def download_file(url, save_pth, rename=None):
    """下载文件

    Args:
        url (__str__): 下载地址
        save_pth (_str_): 保存路径
        rename (__str__, optional): 下载后文件重命名. Defaults to None.
    """
    if not os.path.exists(save_pth):
        os.makedirs(save_pth)
    with closing(requests.get(url, allow_redirects=True,
                              stream=True)) as downfile:
        save_name = rename if rename != None \
                            else get_file_name(downfile.url, downfile.headers)
        file_size = 0 if "Content-Length" not in downfile.headers else int(
            downfile.headers['Content-Length'])
        with open(os.path.join(save_pth, save_name), "wb") as save_file:
            print(f"正在下载文件: {save_name}, 文件大小: {file_size_convert(file_size)}")
            chunk_size = 1024
            for chunk in downfile.iter_content(chunk_size=chunk_size):
                if chunk:
                    save_file.write(chunk)


def get_file_name(url, headers):
    """自动获取下载文件名"""
    filename = ""
    # 首先查找header是否存在Content-Disposition属性
    if "Content-Disposition" in headers and headers["Content-Disposition"]:
        disposition_split = headers["Content-Disposition"].split(";")
        if len(disposition_split) > 1:
            if disposition_split[1].strip().lower().startswith("filename="):
                file_name = disposition_split[1].split("=")
                if len(file_name) > 1:
                    filename = urllib.parse.unquote(file_name[1])
    # 如果header没有写，则用url末尾作为文件名
    if not filename and os.path.basename(url):
        filename = os.path.basename(url).split("?")[0]
    if not filename:
        filename = "download"
    return filename


def file_size_convert(value):
    units = ["B", "KB", "MB", "GB"]
    base = 1024
    for i in range(len(units)):
        if (value / base**(i + 1)) < 1:
            break
    return "%.2f%s" % (value / base**i, units[i])


def unzip_file(zip_file_pth, target_pth):
    if not os.path.exists(target_pth):
        os.makedirs(target_pth)
    with ZipFile(zip_file_pth, 'r') as zip_file:
        zip_file.extractall(target_pth)


def create_shortcut(src, dst):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(dst)
    target = icon = src
    shortcut.Targetpath = target
    shortcut.IconLocation = icon
    shortcut.save()


def check_webview2():
    #判断webview2是否安装
    key1 = None
    key2 = None
    try:
        key1 = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            "SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
        )
    except:
        pass
    try:
        key2 = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}"
        )
    except:
        pass
    if key1 or key2:
        return True
    else:
        return False
