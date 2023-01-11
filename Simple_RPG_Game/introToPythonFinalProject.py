# I made a simple text based rpg party combat game with 3 party members fighting one big boss
# This game utilizes classes and oop in order to simplify the code
# Combat has been optimized to feel like winning should be moderately difficult
import random
import math

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
            damage /= 2
        self.health -= damage
        print('     ',self.name, "took", damage, "damage.", self.name,
              "is now at", self.health, "/", self.maxHealth)
        if (self.health <= 0):
            self.isAlive = False
            print('     ',self.name, "has fallen!")

    def attack(self, enemy):
        enemy.takeDamage(self.attackPower)

class Boss(Entity): #declares boss class
    enraged = False
    def enrage(self):
        self.attackPower = math.ceil(self.attackPower*1.5)
        self.enraged = True
        print(self.name, 'goes into a fury!')

    def takeDamage(self, damage):
        self.health -= damage
        print('     ',self.name, "took", damage, "damage.")
        if (self.health <= 0):
            self.isAlive = False
            print('     ',self.name, "has fallen!")

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
        print(color.bold,'Its', self.name, 'turn.',color.end,'Health:',self.health, '/', self.maxHealth)
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
            target = input('   Who are you healing? c for Corrin, a for Azura, f for Felicia, e for everyone: ')
            if (target == 'a'):
                self.heal(player2)
            elif (target == 'c' and player1.isAlive):
                self.heal(player1)
            elif (target == 'f' and player3.isAlive):
                self.heal(player3)
            elif (target == 'e'):
                self.multiHeal=True
                self.healAll()

# initializes player(s) and first boss
player1 = Myrmidon('Corrin', 100, 15)  # name, health, attack
player2 = Cleric('Azura', 50, 10, 10, 30) # name, health, mana, attack, healingPower
player3 = Ninja('Felicia', 75, 12)
boss = Boss('Anankos', random.randint(550, 650), random.randint(12, 17))
alivePlayers = [player1, player2, player3]
alivePlayerNames = [player1.name, player2.name, player3.name]

# Runs fight until one side is fully downed
while (player1.isAlive or player2.isAlive or player3.isAlive) and boss.isAlive:
    print('')
    for i in alivePlayers:
        if(i.isAlive):
            if(type(i)==Cleric):
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