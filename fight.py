import random
from time import sleep
import asyncio, os
import discord
from discord.ext import commands
from discord.member import Member



#f2_data = {
#    "member": {
#        "id": 534534534534534,
#        "name": "Goro",
#    },
#
#    "specs": {
#        "lvl":,
#        "hp": 100,
#        "exp": 0,
#        "crt": 10,
#        "dmg": 10,
#    },

#}

attack_quets = {
    "attack": [
        "атакует",
        "бьет",
    ],
    "finish": [
        "добивает",
        "шутит про мамку",
    ],
}

class Fighter():

    def __init__(self, member:dict, specs:dict):
        self.__member = member
        self._specs = specs
        self._new_specs = specs
        self.can_fight = True   

    async def attack(self, target: "Fighter" = None):
        spread = random.randint(0, self._specs["dmg"])
        crit = random.randint(1, 100)
        new_embed = discord.Embed(
            title = "Let the Battle Begins",
            description = f"{self.__member['name']} {attack_quets['attack'][random.randint(0, len(attack_quets['attack']) -1 )]} {target.__member['name']}",
            colour = discord.Colour.dark_blue(),
        )

        if spread > 0:
            new_embed.description += " и наносит"
            if crit > 20:
                target._specs["hp"] -= self._specs["dmg"]
                new_embed.description += f' {self._specs["dmg"]} урона'
            else:
                target._specs["hp"] -= self._specs["dmg"] + self._specs["crt"]
                new_embed.description += f' {self._specs["dmg"] + self._specs["crt"]} урона'

        else:
            new_embed.description += " и промахивается"

        await self.__member["msg"].edit(embed = new_embed)

        if target._specs["hp"] <= 0:
            asyncio.sleep(2)
            new_embed.description = f"{self.__member['name']} {attack_quets['finish'][random.randint(0, len(attack_quets['finish']) -1 )]} {target.__member['name']}!"
            await self.__member["msg"].edit(embed = new_embed)
            target.can_fight = False

        

    async def win(self, target:"Fighter"=None):
        diff = abs(self._specs["lvl"] - target._specs["lvl"])

        if diff < 4:
            self._specs["lvl"] += 10
        elif diff < 9:
            if self._specs["lvl"] > target._specs["lvl"]:
                self._specs["exp"] -= 5
            else:
                self._specs["exp"] += 20
        elif diff >= 9:
            if self._specs["lvl"] > target._specs["lvl"]:
                self._specs["exp"] -= 40
            else:
                self._specs["exp"] += 80
        if self._specs["exp"] >= 100:
            self.__lvl_up()
        
        new_embed = discord.Embed(
            title = "Let the Battle Begins",
            description = f"{self.__member['name']} HAS WON WITH {self.__member['hp']}" ,
            colour = discord.Colour.dark_blue(),
        )

        await self.__member["msg"].edit(embed = new_embed, file =discord.File(os.path.join("./img/result.png")))



    async def __lvl_up():
        pass 

    async def __str__(self):
        return f"Параметры бойца {self.__member['name']}: {self._specs}"


async def fight(f1:Fighter=None, f2:Fighter=None):
    
    turn = True

    while f1.can_fight and f2.can_fight:
        sleep(2)
        if turn:
            turn = False
            await f1.attack(f2)
        else:
            turn = True
            await f2.attack(f1)
    
    if f1.can_fight:
        await f1.win(f2)
    else:
        await f2.win(f1)

async def create_fighters(f1:discord.Member, f2:discord.Member, message:discord.Message):
    f1_data = {
        "member": {
            "id": f1.id,
            "name": f1.display_name,
            "msg": message
        },

        "specs": {
            "lvl": f1.id,
            "hp": 100 + f1.id*10,
            "exp": 0,
            "crt": 20 + f1.id*5,
            "dmg": int(20 + f1.id*1.2),
        },

    }

    f2_data = {
        "member": {
            "id": f2.id,
            "name": f2.display_name,
            "msg": message
        },

        "specs": {
            "lvl": f2.id,
            "hp": 100 + f2.id*10,
            "exp": 0,
            "crt": 20 + f2.id*5,
            "dmg": int(20 + f2.id*1.2),
        },

    }

    fighter1 = Fighter(f1_data["member"], f1_data["specs"])
    fighter2 = Fighter(f1_data["member"], f1_data["specs"])

    await fight(fighter1, fighter2)