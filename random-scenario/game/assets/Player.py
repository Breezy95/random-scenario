import discord
from discord.ext import commands


class Player:
        def __init__(self,name,Hp,Def,Att):
                self.name = name
                self.Hp = Hp
                self.Def = Def
                self.Att = Att

