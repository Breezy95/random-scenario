import discord
import asyncio
import random


class Player:
        def __init__(self,name,Hp,Def,Att):
                self.name = name
                self.Hp = Hp
                self.Def = Def
                self.Att = Att


class Monster:
        def __init__(self,name,Hp,Def,Att):
                self.name = name
                self.Hp = Hp
                self.Def = Def
                self.Att = Att

        def PrintHp(self):
                return self.Hp
        def PrintName(self):
                return self.name
        def PrintDef(self):
                return self.Def
        def PrintAttack(self):
                return self.Att
                



client = discord.Client()

MonsterList = []


def loadMonster(filename):
    file = open(filename, 'r')
    for line in file:
        arg = line.split(' ')
        if 'Monster' in arg:
            newmonster = Monster(arg[1], arg[2], arg[3], arg[4])
            MonsterList.append(newmonster)
            return MonsterList
        if '****' in arg:
            break
        arg[:]


@client.event
async def on_ready():
        print('Logged in as ')
        print(client.user.name)
        print(client.user.id)
        print('----------')

@client.event
async def on_message(message):
        if message.content.upper().startswith('!PLAY'):
                args = message.content.split(" ")
                f = open(args[1],"r")
                await client.send_message(message.channel,f.read())
        elif message.content.upper().startswith('!MINFO'):
                await client.send_message(message.channel,'Monster Info')
                await client.send_message(message.channel, MonsterList[0].PrintName())
        elif message.content.upper().startswith('!LOAD'):
        		arg = message.content.split(" ")
        		MonsterList = loadMonster(arg[1])
        		print(MonsterList[0].name)
        		await client.send_message(message.channel,"Monsters Have been Loaded!")
                        return MonsterList





client.run("Mzk4MjAwOTMzMTYwMzIxMDI0.DS7GSQ.wXB8Xa522JtLjQ1nF9d8v5a4fIU")


                        

			
