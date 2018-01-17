import discord
import random
from discord.ext import commands



class DPlayer:
        def __init__(self,name, Hp : int , Def : int, Att : int,ID ,hasID ):
                self.name = name
                self.Hp = Hp
                self.Def = Def
                self.Att = Att
                self.ID = ID
                self.hasID = False


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
        def isAlive(self):
                if self.Hp < 0:
                        return False
                return True
        def CalculateDamage(self):
                x = int(self.Att * 0.1)
                y = self.Att * 1
                return random.randint(x,y)
        def Whoami(self):
                return "DPlayer"
               


               
                
        
