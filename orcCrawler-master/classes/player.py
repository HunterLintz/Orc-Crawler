import random

class Player():
	def __init__(self,typing,maxHealth,accuracy,speed,baseAC,attackUp,attackHigh,attackLow,attackStr,attackName,weaponName,weapon,weaponAction,gold,potion,scroll,image):
		self.name = ""
		self.typing = typing
		self.coolPoints = 0
		self.maxHealth = maxHealth
		self.currentHealth = self.maxHealth
		self.accuracy = accuracy
		self.speed = speed
		self.baseAC = baseAC
		self.finalAC = (self.baseAC + self.speed)
		self.attackUp = attackUp
		self.attackHigh = attackHigh
		self.attackLow = attackLow
		self.attackStr = attackStr
		self.attackName = attackName
		self.weaponName = weaponName
		self.weapon = weapon
		self.weaponAction = weaponAction
		self.gold = gold
		self.potion = potion
		self.scroll = scroll
		self.currentLvl = 1
		self.currentXp = 0
		self.levelUp = 100
		self.image = image

