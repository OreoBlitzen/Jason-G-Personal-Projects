# I made a simple text based rpg party combat game with 3 party members fighting one big boss
# This game utilizes classes and oop in order to simplify the code
# Combat has been optimized to feel like winning should be moderately difficult
import random
import math
import os

class color:
   purple = '\033[95m'
   cyan = '\033[96m'
   darkcyan = '\033[36m'
   blue = '\033[94m'
   green = '\033[92m'
   yellow = '\033[93m'
   red = '\033[91m'
   bold = '\033[1m'
   underline = '\033[4m'
   end = '\033[0m'

class Entity:  # makes base class
    # ***variables and functions can't have the same names; causes errors
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.maxHealth = health
        self.attackPower = attack
        self.isAlive = True
        self.isDefending = False

    def takeDamage(self, damage):
        if (self.isDefending):
            damage = math.floor(damage//2)
        self.health -= damage
        print('     ',self.name, "took", damage, "damage.", self.name,
              "is now at", self.health, "/", self.maxHealth)
        if (self.health <= 0):
            self.isAlive = False
            print('     ',self.name, "has fallen!")

    def attack(self, enemy):
        enemy.takeDamage(self.attackPower)

class Boss(Entity): #declares boss class
    hurt = False
    enraged = False
    def enrage(self):
        self.attackPower = math.ceil(self.attackPower*1.5)
        self.enraged = True
        print(color.red,'-===',self.name, 'goes into a fury!','===-',color.end)

    def takeDamage(self, damage):
        self.health -= damage
        print('     ',self.name, "took", damage, "damage.")
        if (self.health <= 0):
            self.isAlive = False
            print('     ',self.name, "has fallen!")
        if (self.health <= self.maxHealth//2 and self.hurt==False):
            self.hurt = True
            print(color.purple,'-===',self.name, "is looking rough!",'===-',color.end)

    def bossAction(self):
        print(color.bold,'Its', self.name, 'turn.',color.end)
        if(random.randint(0,100)<15):
            print(' ',color.bold,self.name,color.end,'uses Flame Breath on the party')
            for i in alivePlayers:
                self.attack(i)
                if (i.isAlive != True):
                    alivePlayers.remove(i)
                    alivePlayerNames.remove(i.name)
        else:
            bossAggro = random.choice(alivePlayers)
            print(f"      {boss.name} attacks {bossAggro.name}") #example of fprint and how much cleaner it is
            boss.attack(bossAggro)
            if (bossAggro.isAlive != True):
                alivePlayers.remove(bossAggro)
                alivePlayerNames.remove(bossAggro.name)

class Ninja(Entity):  # declares base player class
    def levelUp(self):
        self.maxHealth += 8
        self.attackPower += 5

    def playerAction(self, enemy):
        self.isDefending = False
        print(color.bold+'Its', self.name, 'turn.',color.end,'Health:',self.health, '/', self.maxHealth)
        act = input('   What will they do? '+color.red+'[A]ttack'+color.blue+' [D]efend: '+color.end)
        if act == "a":
            print('     ',self.name, 'attacks', enemy.name)
            self.attack(enemy)
        elif act == "d":
            self.isDefending = True
            print(self.name, 'is defending now')

class Myrmidon(Ninja):  # declares swordsman class
    def levelUp(self):
        self.maxHealth += 15
        self.attackPower += 7

class Cleric(Ninja):  # declares healer class
    # variables and methods can't have the same names
    def __init__(self, name, health, mana, attack, healingPower):
        self.name = name
        self.health = health
        self.maxHealth = health
        self.attackPower = attack
        self.healingPower = healingPower
        self.isAlive = True
        self.isDefending = False
        self.mana = mana
        self.maxMana = mana

    def levelUp(self):
        self.maxHealth += 10
        self.attackPower += 5
        self.maxMana += 2

    def manaRegen(self):  # regenerates 1 mana per turn
        if (self.mana < self.maxMana):
            self.mana += 1

    def heal(self, target):
        if (self.mana >= 5 and target.isAlive):
            healAmount = min((target.maxHealth-target.health),self.healingPower)
            target.health += healAmount
            print('     ',self.name, 'heals', target.name,'for', healAmount, 'health!')
            if(self.multiHeal==False):
                self.mana -= 5
    
    def healAll(self):
        for i in alivePlayers:
            self.heal(i)
        if(self.multiHeal==True):
            self.mana-=10

    def playerAction(self, enemy):
        self.isDefending = False
        self.multiHeal = False
        print(color.bold,'Its', self.name, 'turn.',color.end,'Health:', self.health, '/',self.maxHealth, 'Mana:', self.mana, '/', self.maxMana)
        act = input('   What will they do?'+color.red+' [A]ttack'+color.blue+' [D]efend'+color.green+' [H]eal: '+color.end)
        if act == "a":
            print('     ',self.name, 'attacks', enemy.name)
            self.attack(enemy)
        elif act == "d":
            self.isDefending = True
            print(self.name, 'is defending now')
        elif act == "h" and self.mana >= 5:
            print('   Players currently alive are:', alivePlayerNames)
            target = input('   Who are you healing? c for Corrin, a for Azura, f for Felicia, r for Robin, or e for everyone: ')
            if (target == 'a'): #azura
                self.heal(player2)
            elif (target == 'c' and player1.isAlive): #corrin
                self.heal(player1)
            elif (target == 'f' and player3.isAlive): #felicia
                self.heal(player3)
            elif(target == 'r' and player4.isAlive):
                self.heal(player4)
            elif (target == 'e' and self.mana >= 10):
                self.multiHeal=True
                self.healAll()

class Mage(Ninja): #declares mage class
    def __init__(self, name, health, mana, attack, magicAttackPower):
        self.name = name
        self.health = health
        self.maxHealth = health
        self.attackPower = attack
        self.magicAttackPower = magicAttackPower
        self.isAlive = True
        self.isDefending = False
        self.mana = mana
        self.maxMana = mana

    def levelUp(self):
        self.maxHealth += 10
        self.attackPower += 5
        self.magicAttack += 10
        self.maxMana += 2

    def manaRegen(self):  # regenerates 2 mana per turn
        if (self.mana < self.maxMana):
            self.mana += 2

    def magicAttack(self, enemy):
        enemy.takeDamage(self.magicAttackPower)

    def playerAction(self, enemy):
        self.isDefending = False
        print(color.bold,'Its', self.name, 'turn.',color.end,'Health:', self.health, '/',self.maxHealth, 'Mana:', self.mana, '/', self.maxMana)
        act = input('   What will they do?'+color.red+' [A]ttack'+color.blue+' [D]efend'+color.yellow+' [M]agic: '+color.end)
        if act == "a":
            print('     ',self.name, 'attacks', enemy.name)
            self.attack(enemy)
        elif act == "d":
            self.isDefending = True
            print(self.name, 'is defending now')
        elif act == "m" and self.mana >= 6:
            print(f"    {self.name} uses fireball on {enemy.name}")
            self.mana -= 6
            self.magicAttack(enemy)

# initializes player(s) and first boss
player1 = Myrmidon('Corrin', 100, 15)  # name, health, attack
player2 = Cleric('Azura', 50, 10, 10, 30) # name, health, mana, attack, healingPower
player3 = Ninja('Felicia', 75, 12)
player4 = Mage('Robin', 50, 10, 5, 25)
boss = Boss('Anankos', random.randint(650, 750), random.randint(12, 17))
alivePlayers = [player1, player2, player3, player4]
alivePlayerNames = [player1.name, player2.name, player3.name, player4.name]
os.system("")
# Runs fight until one side is fully downed
while (alivePlayers and boss.isAlive):
    print('')
    for i in alivePlayers:
        if(i.isAlive):
            if(type(i)==Cleric or type(i)==Mage):
                i.manaRegen()
            i.playerAction(boss)
            if(boss.isAlive==False):
                break
    if(boss.isAlive):        
        if (boss.health <= boss.maxHealth*.25 and boss.enraged == False):
            boss.enrage()
        boss.bossAction()

# States who wins at the end of the game
if (boss.isAlive):
    print("The fight is over:", boss.name, "wins")
else:
    print("You win. The party wins")