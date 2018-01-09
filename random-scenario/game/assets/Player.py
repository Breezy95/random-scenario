import discord
import random
from discord.ext import commands



class Player:
        def __init__(self,name,Hp,Def,Att,ID,hasID):
                self.name = name
                self.Hp = Hp
                self.Def = Def
                self.Att = Att
                self.hasID = False
                self.ID = ''


        def PrintHP(self):
                print(self.Hp)
                return self.Hp

        def PrintName(self):
                print(self.name)
                return self.name

        def printID(self):
                print(self.ID)
                return self.ID

        def hasID(self):
                print(self.hasID)
                return self.hasID
                
        
