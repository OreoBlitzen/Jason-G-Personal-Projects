# I made a simple text based rpg party combat game with 3 party members fighting one big boss
# This game utilizes classes and oop in order to simplify the code
# Combat has been optimized to feel like winning should be moderately difficult
import random
import math


class Entity:  # makes base class
    # variables and methods can't have the same names
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
        print(self.name, "took", damage, "damage.", self.name,
              "is now at", self.health, "/", self.maxHealth)
        if (self.health <= 0):
            self.isAlive = False
            print(self.name, "has fallen!")

    def attack(self, enemy):
        enemy.takeDamage(self.attackPower)


class Boss(Entity):
    enraged = False

    def enrage(self):
        self.attackPower = math.ceil(self.attackPower*1.5)
        self.enraged = True
        print(self.name, 'goes into a fury!')


class Ninja(Entity):  # declares base player class
    def levelUp(self):
        self.maxHealth += 8
        self.attackPower += 5

    def playerAction(self, enemy):
        self.isDefending = False
        print('Its', self.name, 'turn. Health:',
              self.health, '/', self.maxHealth)
        act = input('What will they do? [A]ttack or [D]efend: ')
        if act == "a":
            print(self.name, 'attacks', enemy.name)
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
        if (self.mana >= 8):
            healAmount = min((target.maxHealth-target.health),
                             self.healingPower)
            target.health += healAmount
            print(self.name, 'heals', target.name,
                  'for', healAmount, 'health!')
            self.mana -= 8

    def playerAction(self, enemy):
        self.isDefending = False
        print('Its', self.name, 'turn. Health:', self.health, '/',
              self.maxHealth, 'Mana:', self.mana, '/', self.maxMana)
        act = input('What will they do? [A]ttack, [D]efend, or [H]eal: ')
        if act == "a":
            print(self.name, 'attacks', enemy.name)
            self.attack(enemy)
        elif act == "d":
            self.isDefending = True
            print(self.name, 'is defending now')
        elif act == "h" and self.mana >= 8:
            print('Players currently alive are:', alivePlayerNames)
            target = input(
                'Who are you healing? c for Corrin, a for Azura, f for Felicia: ')
            if (target == 'a'):
                self.heal(player2)
            elif (target == 'c' and player1.isAlive):
                self.heal(player1)
            elif (target == 'f' and player3.isAlive):
                self.heal(player3)


# initializes player(s) and first boss
player1 = Myrmidon('Corrin', 100, 15)  # name, health, attack
player2 = Cleric('Azura', 50, 10, 10, 30)
player3 = Ninja('Felicia', 75, 10)
boss = Boss('Anankos', random.randint(500, 600), random.randint(10, 15))
alivePlayers = [player1, player2, player3]
alivePlayerNames = [player1.name, player2.name, player3.name]

# Runs fight until one side is fully downed
while (player1.isAlive or player2.isAlive or player3.isAlive) and boss.isAlive:
    print('')
    if (player1.isAlive):
        player1.playerAction(boss)
        if (boss.isAlive == False):
            break
    if (player2.isAlive):
        player2.manaRegen()
        player2.playerAction(boss)
        if (boss.isAlive == False):
            break
    if (player3.isAlive):
        player3.playerAction(boss)
        if (boss.isAlive == False):
            break
    if (boss.health <= boss.maxHealth*.25 and boss.enraged == False):
        boss.enrage()
    bossAggro = random.choice(alivePlayers)
    print(boss.name, 'attacks', bossAggro.name)
    boss.attack(bossAggro)
    if (bossAggro.isAlive != True):
        alivePlayers.remove(bossAggro)
        alivePlayerNames.remove(bossAggro.name)

# States who wins at the end of the game
if (boss.isAlive):
    print("The fight is over:", boss.name, "wins")
else:
    print("You win. The party wins")