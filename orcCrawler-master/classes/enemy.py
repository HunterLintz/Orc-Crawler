import random

class Enemy():
	def __init__(self,name,maxHealth,baseAC,accuracy,speed,attackHigh,attackLow,goldGainLow,goldGainHigh,xpGive,image):
		self.name = name
		self.maxHealth = maxHealth
		self.currentHealth = self.maxHealth
		self.baseAC = baseAC
		self.accuracy = accuracy
		self.speed = speed
		self.finalAC = (self.baseAC + self.speed)
		self.attackHigh = attackHigh
		self.attackLow = attackLow
		self.goldGainLow = goldGainLow
		self.goldGainHigh = goldGainHigh
		self.xpGive = xpGive
		self.image = image