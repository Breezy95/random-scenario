import discord
import random
from discord.ext import commands

class Enemy:
        def __init__(self,name, Hp : int, Def : int, Att : int):
                self.name = name
                self.Hp = Hp
                self.Def = Def
                self.Att = Att

        def PrintHp(self):
                print(self.Hp)
                return self.Hp
        def PrintName(self):
                print(self.name)
                return self.name
        def PrintDef(self):
                print(self.Def)
                return self.Def
        def PrintAttack(self):
                print(self.Att)
                return self.Att

        def isAlive(self):
                if self.Hp < 0:
                        return False
                return True

        def CalculateDamage(self):
                #damagemin = self.Att * 1
                #damagemax = self.Att * 10
                return random.randint(1,10)
