import sys
import os
import random
import pickle

from classes.enemy import Enemy
from classes.player import Player
from classes.hats import hats
from images.enemyImages import enemyImages
from images.heroImages import heroImages

# clearing terminal command is different for windows vs mac
def checkOs():
	global clear;
	if sys.platform == 'win32':
		clear = 'cls'
	else:
		clear = 'clear'
	
def mainMenu():
	os.system(clear)
	print("Before you begin please press Alt + Enter to Fullscreen")
	print("\nPress Enter when you are ready to continue...")
	option = input("  ")

	os.system(clear)
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("    Welcome to Orc Crawler!!!    ")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	print("1. Start")
	print("2. Load")
	print("3. Quit")

	option = input(" ")

	if option == "1":
		choosePlayer()
	elif option == "2":
		print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
		nameOfFile = ('orcCrawler-master/saves/') + input("What was the name of the adventurer you would like to load?: ")
		if os.path.exists(nameOfFile) == True:
			print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
			PlayerIG = pickle.load(open(nameOfFile, "rb"))
			os.system(clear)
			print("Loaded saved state...")
			option = input(" ")
			continueGame(PlayerIG)
		else:
			os.system(clear)
			print("There is not a save file named that!")
			option = input(" ")
			mainMenu()
	elif option == "3":                                                              
		exit()
	else:
		mainMenu()

def choosePlayer():
	os.system(clear)
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("        Choose your player     		")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	print("1. Fighter")
	print("2. Wizard")
	print("3. Ranger")

	option = input(" ")
	os.system(clear)
	if option == "1":
							#typ,   maxH,acc,spd,bAC,aUp,aH,aL,attStr, attackName,     weaponName, weapon,      Action, gld,pot,scrl,image
		PlayerIG = Player("Fighter", 120, 3, 4, 10, 2, 8, 1, "1-8", "Slash Your Sword", "sword","your sword", "slash", 0, 3, 0, heroImages["fighter"])
	elif option == "2":
		PlayerIG = Player("Wizard", 100, 5, 2, 10, 2, 10, 1, "1-10", "Cast Firebolt", "wand","a bolt of fire", "blast", 0, 2, 1, heroImages["wizard"])
	elif option == "3":
		PlayerIG = Player("Ranger", 110, 4, 3, 10, 2, 6, 1, "1-6", "Shoot Your Bow", "bow","an arrow from your bow", "pierce", 50, 2, 0, heroImages["ranger"])
	else:
		print("Enter a number to choose your class!")
		option = input(" ")
		choosePlayer()
	os.system(clear)
	PlayerIG.name = input(("What is your name %s?: \n%s\n--->") % (PlayerIG.typing,PlayerIG.image))
	os.system(clear)
	print(("Well %s your adventure starts here! Good Luck!")%(PlayerIG.name))
	print(("%s" )%(PlayerIG.image))
	option = input("  ")
	continueGame(PlayerIG)

def continueGame(player):
	os.system(clear)
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("            The Town 			    		")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	print(("%s's Stats and Inventory:") % (player.name))
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	if player.coolPoints != 0:
		print(("Cool Points: %i") % (player.coolPoints))
	print(("Class: %s") % (player.typing))
	print(("Level: %i || Current XP: %i/%i")%(player.currentLvl, player.currentXp,player.levelUp))
	print(("HP: %i/%i") % (player.currentHealth, player.maxHealth))
	print(("Armor Class: %i")%(player.finalAC))
	print(("Accuracy: +%i")%(player.accuracy))
	print(("Speed: %i")%(player.speed))
	print(("Attack: %s + %i damage from bonus") % (player.attackStr, player.attackUp))
	print(("Gold: %i") % (player.gold))
	print(("Potions: %i") %(player.potion))
	print(("Scrolls: %i || 1-20 Damage\n") % (player.scroll))
	print(("\nWhat would you like to do %s?") % (player.name))
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	print("1. Explore the Dungeon's 1st Floor")
	print("\n2. Drink a Potion")
	print("3. Go to the Shop\n\n\n")
	print("4. Save the Game")
	print("5. Main Menu")
	option = input(" ")
	if option == "1":
		roomGen(player)
	elif option == "2":
		menuDrinkPotion(player)
		continueGame(player)
	elif option == "3":
		store(player)
	elif option == "4":
		pickle.dump(player, open('orcCrawler-master/saves/' + player.name, "wb"))
		os.system(clear)
		print("\nGame has been saved!\n")
		option = input(" ")
		continueGame(player)
	elif option == "5":
		mainMenu()
	else: 
		continueGame(player)

def roomGen(player):
	roomType = random.randint(1,10)
	if 1 <= roomType <= 5:
		emptyRoom(player)
	elif 6 <= roomType <= 8:
		fight(preFight(), player)
	else:
		foundChest(player)

def emptyRoom(player):
	os.system(clear)
	print("\n")
	hatCheck = random.randint(1, 20)
	if hatCheck == 1:
		print("You enter a room that contains a hat salesman.")
		option = input(" ")
		hatSalesman()
	else:
		with open('orcCrawler-master\classes\emptyRooms.txt') as f:
			emptyRoomGen = f.readlines()
			print(random.choice(emptyRoomGen))
			option = input(" ")
	stillExplore(player)

def preFight():
	os.system(clear)
	print("\n")
	enemyChance = random.randint(1,100)
	if enemyChance <= 2:  #2% Dragon Spawn
		enemy = Enemy("Dragon", 60, (10 + enemy.speed), 2, 1, 20, 1, 80, 160, 100, enemyImages["dragon"])
		print("Like a comet, a dragon flys into the ground creating a \nshockwave as it does so... its ready to take you down!")

	elif 3 <= enemyChance <= 12: #10% Bandit Spawn
		enemy = Enemy("Bandit", 30, 10, 4, 3, 12, 1, 15, 70, 80, enemyImages["bandit"])
		print("From the shadows a bandit steps out... He looks ready to \ntake your gold, killing you in the process if necessary.")

	elif 13 <= enemyChance <= 27: #15% Orc Spawn
		enemy = Enemy("Orc", 25, 10, 3, 2, 10, 1, 15, 60, 60, enemyImages["orc"])
		print("You found an orc!")

	elif 28 <= enemyChance <= 47: #20% Goblin Spawn
		enemy = Enemy("Goblin", 20, 10, 2, 5, 8, 1, 10, 40, 40, enemyImages["goblin"])
		print("You found a goblin!")

	elif 48 <= enemyChance <= 71: #24% Skeleton Spawn
		enemy = Enemy("Skeleton", 15, 10, 4, 1, 6, 1, 5, 30, 20, enemyImages["skeleton"])
		print("You found a skeleton!")

	else: #29% Zombie Spawn
		enemy = Enemy("Zombie", 10, 10, 3, -1, 4, 1, 0, 15, 10, enemyImages["zombie"])
		print("You found a zombie!")

	option = input(" ")
	print(enemy.image)
	option = input(" ")
	return enemy;

def foundChest(player):
	os.system(clear)
	print("\n")
	print("You found a chest do you want to open it?")
	print("1. Yes")
	print("2. No")
	option = input(" ")
	if option == "1":
		chestRoom(player)
	elif option == "2":
		stillExplore(player)
	else:
		foundChest(player)

def chestRoom(player):
	os.system(clear)
	print("\n")
	chestGen = random.randint(1,5)
	if chestGen == 1:
		if player.potion == 5:
			print("You found a potion but dont have any room would \nyou like to drink it?")
			print("1. Yes")
			print("2. No")
			option = input(" ")
			if option == "1":
				menuDrinkPotion(player)
				roomGen(player)
			else:
				print(" ")
		else:
			player.potion += 1
			print("You found a potion!")
	elif chestGen == 2:
		if player.attackUp >= 10:
			chestRoom(player)	
		player.attackUp += 1
		print("You open the chest and it's empty...")
		option = input(" ")
		print(("Next thing you know your %s starts glowing! It seems to have been imbued with magic: \nYour %s just became stronger!!! || +1 to your current damage.")%(player.weaponName,player.weaponName))
	elif chestGen == 3:
		chestGold = random.randint(10,200) 
		player.gold += chestGold
		print("You open the chest and gold fills your eyes!!!\nYou just found " + str(chestGold) + " Gold!!!")
	elif chestGen == 4:
		if player.scroll == 3:
			print("you found a scroll but you dont have room for it")	
		else:
			player.scroll += 1
			print("You found a scroll")	
	else:
		print("You try and open the chest...")
		option = input(" ")
		print("Next thing you know the chests eyes open!!!")
		option = input(" ")
		enemy = Enemy("Mimic", 35, 10, 4, 3, 14, 1, 50, 100 , 50, enemyImages["mimic"])
		enemyAttack = random.randint(enemy.attackLow,enemy.attackHigh)
		player.currentHealth -= enemyAttack
		print(("Its a mimic and before you know it makes an attack at you for %i points of damage!!!")%(enemyAttack))
		option = input(" ")
		print(enemy.image)
		option = input("  ")
		fight(enemy, player)

	option = input(" ")
	stillExplore(player)

def fight(enemy, player):
	os.system(clear)
	print("\n")
	print (("%s's HP: %i/%i     %s's HP:%i/%i") % (player.name, player.currentHealth, player.maxHealth, enemy.name, enemy.currentHealth, enemy.maxHealth))
	print("\nInventory:")
	print("~~~~~~~~~~~~")
	print(("Scrolls: %i") % (player.scroll))
	print(("Potions: %i") % (player.potion))
	print("\n\nActions:")
	print("~~~~~~~~~~~~")
	print(("1. %s") % (player.attackName))
	print("2. Use Scroll")
	print("3. Drink Potion")
	print("4. Run")
	option = input(" ")
	if option == "1":
		preAttack(enemy, player)
	elif option == "2":
		scrollAttack(enemy, player)
	elif option == "3":
		fightDrinkPotion(enemy, player)
		fight(enemy, player)
	elif option == "4":
		run(enemy, player)
	else:
		fight(enemy, player)

def preAttack(enemy,player):
	if player.speed > enemy.speed:
		attackPlayer(enemy,player)
	elif player.speed < enemy.speed:
		attackEnemy(enemy,player)
	elif player.speed == enemy.speed:
		firstUp = random.randint(1,2)
		if firstUp == 1:
			attackPlayer(enemy,player)
		else:
			attackEnemy(enemy,player)

def attackPlayer(enemy, player):
	os.system(clear)
	print("\n")
	playerHit = random.randint(1,20) + player.accuracy
	enemyHit = random.randint(1,20) + enemy.accuracy
	# player.enemyName = enemy.name
	if playerHit > enemy.finalAC:
		playerAttack = random.randint(player.attackLow,player.attackHigh)
		playerAttackF = playerAttack + player.attackUp
		print (("You %s the %s with %s for %i points of damage!!!") % ( player.weaponAction, enemy.name, player.weapon,playerAttackF))
		enemy.currentHealth -= playerAttackF
		if enemy.currentHealth <= 0:
			option = input(" ")
			resolve(enemy,player)
	else:
		print (("You miss the %s with %s!!!") % (enemy.name, player.weapon))
		 
	option = input(" ")

	if enemyHit > player.finalAC:
		enemyAttack = random.randint(enemy.attackLow,enemy.attackHigh)
		print (("The %s hit you for %i points of damage!!!") % (enemy.name,enemyAttack))
		player.currentHealth -= enemyAttack
		if player.currentHealth <= 0:
			option = input(" ")
			resolve(enemy, player)
	else:
		print(("The %s missed you!!!") % (enemy.name))

	option = input(" ")

	resolve(enemy, player)

def attackEnemy(enemy, player):

	os.system(clear)
	print("\n")
	playerHit = random.randint(1,20) + player.accuracy
	enemyHit = random.randint(1,20) + enemy.accuracy
	if enemyHit > player.finalAC:
		enemyAttack = random.randint(enemy.attackLow,enemy.attackHigh)
		print (("The %s hit you for %i points of damage!!!") % (enemy.name, enemyAttack))
		player.currentHealth -= enemyAttack
		if player.currentHealth <= 0:
			option = input(" ")
			resolve(enemy, player)
	else:
		print(("The %s missed you!!!") % (enemy.name))

	option = input(" ")

	if playerHit > enemy.finalAC:
		playerAttack = random.randint(player.attackLow,player.attackHigh)
		playerAttackF = playerAttack + player.attackUp
		print (("You %s the %s with %s for %i points of damage!!!") % ( player.weaponAction, enemy.name, player.weapon, playerAttackF))
		enemy.currentHealth -= playerAttackF
		if enemy.currentHealth <= 0:
			option = input(" ")
			resolve(enemy,player)
	else:
		print (("You miss the %s with %s!!!") % (enemy.name, player.weapon))
		 
	option = input(" ")
	resolve(enemy, player)

def scrollAttack(enemy, player):
	os.system(clear)
	print("\n")
	scrollAttack = (random.randint(1,6)+random.randint(1,6)+random.randint(1,6)+random.randint(1,6))
	enemyHit = random.randint(1,20) +enemy.accuracy
	if player.scroll == 0:
		print("You don't have any scrolls left!")
		option = input(" ")
		fight(enemy, player)
	else:
		print(("You read the scroll conjuring forth a fireball blasting the %s!!!") % (enemy.name))
		enemy.currentHealth -= scrollAttack
		player.scroll -= 1
		option = input(" ")
		print(("You burn the enemy for %i points of damage") % (scrollAttack))
		option = input(" ")
		if enemy.currentHealth <= 0:
			resolve(enemy,player)
		if enemyHit > player.finalAC:
			enemyAttack = random.randint(enemy.attackLow,enemy.attackHigh)
			player.currentHealth -= enemyAttack
			print (("The %s hit you for %s points of damage!!!") % (enemy.name,enemyAttack))
		elif player.currentHealth <= 0:
			option = input(" ")
			resolve(enemy, player)
		else:
			print(("The %s missed you!!!") % (enemy.name))

	option = input(" ")
	resolve(enemy, player)

def menuDrinkPotion(player):
	os.system(clear)
	enemyHit = random.randint(1,2)
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	if player.currentHealth == player.maxHealth:
		print("You dont need to use a potion!")
		option = input(" ")
	elif player.potion == 0:
		print("You dont have any potions left!")
		option = input(" ")
	else:
		healthReceived = (random.randint(1,10) + random.randint(1,10) + 5)
		player.currentHealth += healthReceived
		print(("You gained %i health!") % (healthReceived))
		player.potion -= 1
		option = input(" ")
		if player.currentHealth >= player.maxHealth:
			player.currentHealth = player.maxHealth

def fightDrinkPotion(enemy, player):
	os.system(clear)
	enemyHit = random.randint(1,20) + enemy.accuracy
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
	if player.currentHealth == player.maxHealth:
		print("You dont need to use a potion!")
		option = input(" ")
	elif player.potion == 0:
		print("You dont have any potions left!")
		option = input(" ")
	else:
		healthReceived = (random.randint(1,10) + random.randint(1,10) + 5)
		player.currentHealth += healthReceived
		print(("You gained %i health!") % (healthReceived))
		player.potion -= 1
		option = input(" ")
		if player.currentHealth >= player.maxHealth:
			player.currentHealth = player.maxHealth
		if enemyHit > player.finalAC:
			enemyAttack = random.randint(enemy.attackLow,enemy.attackHigh)
			player.currentHealth -= enemyAttack
			print (("The %s hit you for %i points of damage!!!") % (enemy.name,enemyAttack))
		if player.currentHealth <= 0:
			option = input(" ")
			resolve(enemy, player)
		elif enemyHit <= player.finalAC:
			print(("The %s missed you!!!") % (enemy.name))
		option = input("  ")

def run(enemy, player):
	os.system(clear)
	getAway = random.randint(1,3)
	if random.randint(1,3) == 1:
		print("\nYou got away!")
		option = input(" ")
		continueGame(player)
	else:
		print("\nYou didn't get away!")
		print (("The %s hit you!!!") % ( enemy.name))
		enemyAttack = random.randint(enemy.attackLow,enemy.attackHigh)
		player.currentHealth -= enemyAttack
		option = input(" ")
	resolve(enemy, player)
	
def resolve(enemy, player):
	os.system(clear)
	print("\n")
	if player.currentHealth <= 0:
		print("You Died...")
		option = input(" ")
		os.system(clear)
		if player.gold == 0:
			print("I didn't think it was possible... you found literally 0 gold...")
		else:
			print(("At least you found %i gold coins in your adventure!") % (player.gold))
		quit()
	if enemy.currentHealth <= 0:
		os.system(clear)
		print(("You killed the %s") % (enemy.name))
		option = input("  ")
		enemy.currentHealth = enemy.maxHealth
		goldGive = random.randint(enemy.goldGainLow,enemy.goldGainHigh)
		player.gold += goldGive
		os.system(clear)
		print(("You found %i gold on the %s") % (goldGive, enemy.name))
		option = input(" ")
		player.currentXp += enemy.xpGive
		os.system(clear)
		print(("You gained %i experience points")%(enemy.xpGive))
		option = input("  ")
		if player.currentXp >= player.levelUp:
			xpOverflow = player.currentXp - player.levelUp
			player.currentLvl += 1
			player.levelUp *= 2
			player.currentXp = xpOverflow
			print(("You leveled up! You are now level %i") % (player.currentLvl))
			option = input("  ")
			levelUp(player)

		stillExplore(player)
	else:
		fight(enemy, player)

def levelUp(player):
	os.system(clear)
	print("What would you like to upgrade?")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("1.Health   || +10")
	print("2.Damage   || +2")
	print("3.Accuracy || +1")
	print("4.Speed    || +1")
	option = input("  ")
	os.system(clear)
	if  option == "1":
		player.maxHealth += 10
		print("Your Max Health has just been increased by 10!")
	elif option == "2":
		player.attackUp += 2
		print("Your Attack Bonus has just been increased by 2!")
	elif option == "3":
		player.accuracy += 1
		print("Your Accruacy has just been increased by 1!")
	elif option == "4":
		player.speed += 1
		print("Your Speed has just been increased by 1!")
	else:
		levelUp(player)
	option = input("  ")
	stillExplore(player)



def store(player):
	os.system(clear)
	print(("Welcome to my shop %s! What would you like?\n") % (player.name))
	print("Your Inventory:")
	print(("Gold: %i") % (player.gold))
	print(("Scrolls: %i") % (player.scroll))
	print(("Potions: %i") % (player.potion))
	print("\nThe Shops Inventory:")
	print("1. 1 Potion || Cost: 30 Gold")
	print("2. 1 scroll || Cost: 50 Gold")
	print("3. Leave Store")
	option = input(" ")
	if option == "1":
		if player.gold < 30:
			print("Sorry you dont have enough for a potion.")
			option = input(" ")
		elif player.potion > 5:
			print("Sorry it doesnt look like you have any more room for potions.")
			option = input(" ")
		else:
			print("Thank you for your purchase. Here is the potion!")
			option = input(" ")
			print("You have gained 1 potion!!!")
			option = input(" ")
			player.potion += 1
			player.gold -= 30
		store(player)
	elif option == "2":
		if player.gold < 50:
			print("Sorry you dont have enough for a scroll.")
			option = input(" ")
		elif player.scroll > 3:
			print("Sorry it doesnt look like you have any more room for a scroll.")
			option = input(" ")
		else:
			print("Thank you for your purchase. Here is the scroll!")
			option = input(" ")
			print("You have gained 1 scroll!!!")
			option = input(" ")
			player.scroll += 1
			player.gold -= 50
		store(player)
	elif option == "3":
		print("Alrighty! have a nice day!")
		option = input(" ")
		continueGame(player)
	else:
		store(player)

def hatSalesman(player):
	os.system(clear)
	global hatIndex
	print('"Would you like to see my wares?" He says.')
	print("1.Yes")
	print("2.No")
	option = input(" ")
	if option == "1":
		hatIndex = 0
		hatSale(player)
	elif option == "2":
		print("Alrighty have a nice day!!!")
		option = input(" ")
		stillExplore(player)
	else:
		hatSalesman(player)

def hatSale(player):
	global hatIndex
	os.system(clear)
	option = input(("Would you like a %s for %s gold?\n1. Yes\n2. No\n") % (hats[hatIndex]["hatType"],(hats[hatIndex]["cost"])))

	if option == "1":

		print(("Alright thank you! have a nice day!\n \nA %s has been added into you inventory!") %(hats[hatIndex]["hatType"]))
		if hats[hatIndex]["coolPoints"] < 0:
			print(("\nYou just lost %s cool points...") % (hats[hatIndex]["coolNum"]))
		else:
			print(("\nYou just gained %s cool points!") % (hats[hatIndex]["coolNum"]))

		player.coolPoints += (hats[hatIndex]["coolPoints"])
		hatIndex = 0
		option = input(" ")
		stillExplore(player)

	elif option == "2":
		if hatIndex >= 3:
			hatIndex = 0

		else:
			hatIndex += 1

		hatSale(player)

	else:
		hatSale(player)

def stillExplore(player):
	os.system(clear)
	print("\n")
	print("1. Keep Exploring the Dungeon")
	print("2. Go Back to Town")
	option = input(" ")
	if option == "1":
		roomGen(player)
	elif option == "2":
		continueGame(player)
	else:
		stillExplore(player)

def quit():
	sys.exit

checkOs()

mainMenu()




#orcCrawler - cloud - branch: master (deployed code - consumer interacts with)
#bugs-123

#git checkout master
#git checkout -b bug-123
#bug-123

#git commit -m "updated os sytem clear function"
#git push bugs-123
