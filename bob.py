import time
import math
from random import seed
from random import randint
from random import random

#### unaffiliated functions ####

# to determine if passed in object evades an attack
def evasion(attackee):
    evaded = False
    evadeRoll = math.trunc(random() * 100)
    evadeWindow = math.trunc((attackee.agility * 3) / 2)
    evadeTarget = math.trunc(random() * 100)
    
    if evadeRoll >= (evadeTarget - evadeWindow) and evadeRoll <= (evadeTarget + evadeWindow):
        evaded = True
    else:
        evaded = False

    return evaded

def critical(attacker):
    critical = False
    critRoll = math.trunc(random() * 100)
    critWindow = math.trunc((attacker.luck * 3) / 2)
    critTarget = math.trunc(random() * 100)
    
    if critRoll >= (critTarget - critWindow) and critRoll <= (critTarget + critWindow):
        critical = True
    else:
        critical = False

    return critical

# do I need an enemycritical function?

def forestPath():
    one = randint(1, 4)
    two = randint(1, 4)
    three = randint(1, 4)
    four = randint(1, 4)
    five = randint(1, 4)
    six = randint(1, 4)
    seven = randint(1, 4)
    eight = randint(1, 4)

    numbers = [one, two, three, four, five, six, seven, eight]
    path = []

    for number in numbers:
        if number == 1:
            path.append('north')
        elif number == 2:
            path.append('south')
        elif number == 3:
            path.append('east')
        else:
            path.append('west')

    return path


# Bob attacking an enemy
def attack(bob, enemy):
    evade = evasion(enemy)
    crit = critical(bob)

    print("You " + bob.equipWeapon.verb + " " + enemy.name + " " + bob.equipWeapon.adverb + " with your " + bob.equipWeapon.name + "!")
    time.sleep(1)

    damage = (bob.strength + bob.equipWeapon.power) - enemy.defense
    if crit:
        damage *= 2

    if not evade:
        if crit:
            print("Noice! Critical hit!")
            time.sleep(1)

        print("You " + bob.equipWeapon.verb + "ed away " + str(damage) + " health from " + enemy.name + "!")
        time.sleep(1)

        enemy.health -= damage

    else:
        print("Blast! " + enemy.name + " deftly dodged your " + bob.equipWeapon.verb + "!")
        time.sleep(1)

# an enemy attacking Bob
def enemyAttack(enemy, bob):
    evade = evasion(bob)

    print(enemy.name + ' ' + enemy.attackDesc)
    time.sleep(1)

    damage = enemy.power - bob.endurance

    if damage <= 0:
        damage = 1

    if not evade:
        print(enemy.name + " " + enemy.verb + " you, inflicting " + str(damage) + " damage.")
        time.sleep(1)

        bob.health -= damage

    else:
        print("The assault narrowly misses, " + bob.equipArmor.gerund + bob.equipArmor.protectDesc + bob.equipArmor.name + "!")
        time.sleep(1)

# using an item 
def useItem(bob, enemy):
    print('')

# a battle is lost
def failure():
    print('')

# a battle is won
def success(bob, enemy):
    money = math.trunc((bob.luck * (enemy.startHealth + enemy.power + enemy.defense + enemy.agility)) - ((random() * 100) - (bob.luck * 10)))
    if money < 1:
        money = 1
    
    window = bob.luck
    exp = enemy.exp
    target = math.trunc(random() * 100)
    roll = math.trunc(random() * 100)

    print(enemy.name + " is vanquished!")
    time.sleep(1)

    if roll >= (target - window) and roll <= (target + window):
        exp *= 2
        print("Lucky! You get double experience.")
        time.sleep(1)

    bob.money += money
    bob.experience += exp
    print("Bob earned " + str(money) + " monies and " + str(exp) + " experience.")
    time.sleep(1)

    enemy.afterFight()

# Bob trying to flee
def flee(bob, enemy):
    window = math.trunc((((bob.agility * 2) * bob.level) - enemy.health) / 2)
    target = math.trunc(random() * 100)
    roll = math.trunc(random() * 100)

    if roll >= (target - window) and roll <= (target + window):
        return True

    else:
        return False

# main fight system function
def fight(bob, enemy):
    fleeSuccess = 0
    first = True

    while enemy.health > 0 and bob.health > 0:
        choice = ''

        if first:
            print(enemy.name + enemy.intro)
            time.sleep(1)
            first = False

        print("What will you do?")
        print("Attack?         Observe?        Use item?        Flee?")

        choice = input()

        if choice.lower() == 'attack':
            attack(bob, enemy)
            if not enemy.health <= 0:
                enemyAttack(enemy, bob)

                if bob.health <= 0:
                    failure()
                    break
                else:
                    continue
            else:
                success(bob, enemy)
                break
            

        elif choice.lower() == 'observe':
            print(enemy.describe())
            time.sleep(1)
            continue

        elif choice.lower() == 'use item':
            useItem(bob, enemy)

            if not enemy.health <= 0:
                enemyAttack(enemy, bob)

                if bob.health <= 0:
                    failure()
                    break
                else:
                    continue
            else:
                success(bob, enemy)
                break
        
        elif choice.lower() == 'flee':
            fleeSuccess = flee(bob, enemy)
            time.sleep(2)

            if fleeSuccess:
                money = math.trunc((((bob.agility * 2) * bob.level) - enemy.health))

                if money >= bob.money:
                    money = bob.money

                bob.money -= money

                if money > 1:
                    print("You successfully fleed, you dirty coward! Lost " + str(money) + " monies.")
                    time.sleep(1)
                    break

                elif money == 1:
                    print("You successfully fleed, you dirty coward! Lost " + str(money) + " moni.")
                    time.sleep(1)
                    break

                else:
                    print("You successfully fleed, you dirty coward!")
                    time.sleep(1)
                    break
                    

            else:
                print("You failed to flee, aaand you're about to get smacked.")
                time.sleep(1)

                enemyAttack(enemy, bob)

                if bob.health <= 0:
                    failure()
                    break
                else:
                    continue
        else:
            print("Huh? Try again.")
            time.sleep(1)
            continue

        time.sleep(1)

#### end unaffiliated functions ####

#### classes ####

class weapon:
    def __init__(self, n, p, v, a):
        self.name = n
        self.power = p
        self.verb = v
        self.adverb = a

class armor:
    def __init__(self, n, d, g, pd):
        self.name = n
        self.defense = d
        self.gerund = g
        self.protectDesc = pd

class item:
    def __init__(self, n, d):
        self.name = n
        self.description = d

class location:
    def __init__(self, d, e, s):
        self.description = d
        self.enemies = e
        self.secret = s

    def getEnemy(self):
        random = randint(0, 100)

        if random <= 33:
            newEnemy = self.enemies[0]
            return newEnemy

        elif random <= 66:
            newEnemy = self.enemies[1]
            return newEnemy
            
        elif random <= 99:
            newEnemy = self.enemies[2]
            return newEnemy

        else:
            newEnemy = self.enemies[3]
            return newEnemy

class enemy:
    def __init__(self, i, n, h, h2, p, de, ag, e, desc, v, ad):
        self.intro = i
        self.name = n
        self.health = h
        self.startHealth = h2
        self.power = p
        self.defense = de
        self.agility = ag
        self.exp = e
        self.description = desc
        self.verb = v
        self.attackDesc = ad

    def describe(self):
        return self.name + "\nHealth: " + str(self.health) + "\nPower: " + str(self.power) + "\nDefense: " + str(self.defense) + "\n" + self.description
    
    def afterFight(self):
        self.health = self.startHealth

class bob:
    def __init__(self, n, lo, i, s, e, ag, ar, w, lu, pers):
        self.name = "Bob"
        self.items = []
        self.weapons = [w]
        self.armors = [ar]
        self.location = lo
        self.level = 1
        self.health = 100
        self.intelligence = i
        self.strength = s + w.power
        self.endurance = e + ar.defense
        self.agility = ag
        self.equipArmor = ar
        self.equipWeapon = w
        self.money = 0
        self.luck = lu
        self.experience = 0
        self.personality = pers
        self.secret = n

    def displayStats(self):
        return "Name: Bob\nLevel: " + str(self.level) + "\nHealth: " + str(self.health) + "\nIntelligence: " + str(self.intelligence) + "\nStrength: " + str(self.strength) + "\nEndurance: " + str(self.endurance) + "\nAgility: " + str(self.agility) + "\nMoney: " + str(self.money)

    def addWeapon(self, weapon):
        self.weapons.append(weapon)

    def addArmor(self, armor):
        self.armors.append(armor)

    def changeWeapon(self):
        choice = ''
        changed = False

        print('Weapons:')
        for weapon in self.weapons:
            print(weapon.name)

        print()
        print("Which weapon do you want to equip?")

        choice = input()

        for weapon in self.weapons:
            if choice == weapon.name:
                self.strength -= self.equipWeapon.power
                self.equipWeapon = weapon
                self.strength += weapon.power

                print("Weapon changed to " + weapon.name + ".")
                time.sleep(1)
                print('Current stats:')
                time.sleep(1)
                print(self.displayStats())
                time.sleep(1)
                print()

                changed = True

        if not changed:
            print("Whatever that is, you ain't got it.")
            time.sleep(1)

    def changeArmor(self):
        choice = ''
        changed = False

        print('Armor:')
        for armor in self.armors:
            print(armor.name)

        print()
        print("Which armor do you want to equip?")

        choice = input()

        for armor in self.armors:
            if choice == armor.name:
                self.endurance -= self.equipArmor.defense
                self.equipArmor = armor
                self.endurance += armor.defense

                print('Armor changed to ' + armor.name + '.')
                time.sleep(1)

                print('Current stats:')
                time.sleep(1)
                print(self.displayStats())
                time.sleep(1)
                print()

                changed = True
                
        if not changed:
            print("Whatever that is, you ain't got it.")

#### end classes ####

#### enemies ####

# rare:
chonky = enemy(' bonks onto the scene!', 'Chonky Bonker', 30, 30, 1, 0, 5, 50, 'You could picture almost nothing quite as Chonky and Bonky as this guy.', 'bonks', 'tries to Bonk your Chonks!')

# city:
guy = enemy(' literally just stands there!', 'Regular Guy', 5, 5, 2, 1, 1, 10, 'The normalcy gods have blessed this man with extra-ordinary abilities.', 'derisively smirks at', 'shoots you a furtive, snide glance!')
road = enemy(' was always underneath!', 'Pavement', 10, 10, 1, 0, 0, 20, 'It overwhelms you to consider how every road in existence was once unpaved.', 'applies upward force to', 'makes your feet hurt!')
cat = enemy(' reminds you whose street this is!', 'Street Cat', 5, 5, 3, 0, 3, 15, 'Just a cat, but it has tears tattooed on its face.', 'throws a gang sign toward', 'gets all up in your face!')

# suburb:
ball = enemy(' bounces your way!', 'Stray Ball', 5, 5, 5, 5, 5, 5, 'There\'s something deeply menacing about the frowning parabola of Stray Ball\'s gait.', 'bebops into', 'reminds you of childhood rounds of dodgeball! (you were bad at dodgeball)')
mom = enemy(' calls the manager!', 'Soccer Mom', 5, 6, 7, 5, 5, 3, 'Highly supportive of her only child, her biting gossip is nothing to be trifled with.', 'raises her voice at', 'says, "Don\'t you know who I am!?"')
whacker = enemy(' roars to life!', 'Weed Whacker', 6, 6, 7, 7, 6, 6, 'Surely a sinister, surly, spinning silhouette that sounds solidly sordid.', 'flings lawn detritus toward', 'offends most of your senses!')

# rural:


# forest:


# mountain:


#### end enemies ####

#### enemy arrays ####

cityEnemies = [guy, road, cat, chonky]
suburbEnemies = [ball, mom, whacker]
ruralEnemies = []
forestEnemies = []
mountainEnemies = []

#### end enemy arrays ####

#### weapons ####

# starter weapons:
nails = weapon('dirty fingernails', 1, 'scratch', 'desperately') # skittish
beaker = weapon('beaker', 1, 'clink', 'carefully') # smart
tKatana = weapon('toy katana', 1, 'doink', 'threateningly') # stalwart
gMCard = weapon('gym membership card', 1, 'swipe', 'haphazardly') # strong
bPhone = weapon('business phone', 1, 'call', 'nervously') # secret

# all others
manholeCover = weapon('manhole cover', 3, 'clang', 'in a manhole sort of way')
mmGun = weapon('sawed-off marshmallow gun', 10, 'shoot', 'accurately')
squatchBlade = weapon('Squatchblade', 30, 'slash', 'thunderously')

#### end weapons ####

#### armor ####

# starter armors:
hShirt = armor('Hawaiian shirt', 1, 'fwipping ', 'against the bright florals of your ') # secret
trench = armor('Trench coat', 1, 'rubbing ', 'gently down the faux leather of your ') # stalwart
snapback = armor('Snapback', 1, 'bouncing ', 'off the bill of your ') # strong
glasses = armor('Thick glasses', 1, 'brushing ', 'across the surface of your ') # smart
tShirt = armor('Novelty t-shirt', 1, 'snagging ', 'on the holes in your ') # skittish

# all others
plaidShorts = armor('Plaid shorts', 3, 'glancing ', 'the dated, gauche patterns of your ')
emptyLog = armor('Empty log', 7, 'splintering ', 'dangerous slivers off of your ')

#### end armor ####

#### locations ####

city = location('City Street', cityEnemies, manholeCover)
suburb = location('Suburban Neighborhood', suburbEnemies, plaidShorts)
rural = location('Hostile Backwoods', ruralEnemies, mmGun)
forest = location('Darkest Forest', forestEnemies, emptyLog)
mountain = location('Steep Mountain', mountainEnemies, squatchBlade)

#### end locations ####

#### functions relating directly to gameplay ####

# ask the player 5 multiple-choice questions to determine Bob stats and variety (smart, strong, stalwart, skittish, secret?)
def characterCreate():

    answers = []

    questions = [
        ["A dirty child approaches you on the street and asks if you have any spare change. Your response:", 
        "A. Stare wide-eyed at the biped, performing calculations to determine variables such as societal status, current earning potential, and able-bodiedness to make an informed decision regarding change-worthiness",
        "B. Bro, that kid probaly dosnt even have mony for protin powder. Give em you're change. If I dont have change tho porbaly see how far i can throw the kid", 
        "C. Shed a single tear, handing dirty child the nickel you were saving to buy a pack of pokemon cards. Tip your fedora to them as you walk away, zipping up your floor-length trench coat.", 
        "D. Ki'ds probbably got A WIRE FROM THE GOVERNMENT!!!! BETTEr pussh the kidd down and run away, fast as possiBLE", "?"],

        ["You are driving a bus, when suddenly, your brakes fail as you approach an intersection where an old lady, a young mother pushing a stroller, and a man in a business suit are crossing the street. What action do you take?", 
        "A. In an effort to mitigate accusations of prejudice, you specifically direct your careening conveyance to impact each individual in the most equitable fashion possible", 
        "B. You climb out the nearest window onto the top of the bus and begin punching it and shouting 'bro, stop!'", 
        "C. You fantasize about how easily this scenario would be solved if you had spiderman powers, unknowingly steering the bus into the nearest municipal building", 
        "D. This is a trick question. You don't have a driver's license because you don't want 'the man' to have pictures of you", "?"],

        ["If a tree falls in the forest and nobody is around to hear it, does it make a sound?", 
        "A. A well-funded research group would likely be able to confirm or refute this yet-unknown inquiry over the course of 4-5 years.", 
        "B. Bro if that tree is under 450 pounds i could bench it", 
        "C. Yes, unless a level 3 druid has place a silence spell on it in the last 48 hours, m'lady.", 
        "D. You can read all about my opinion on this topic in chapter 31 of my upcoming book, 'Why the GOVERNMENT made birDs so thEY COULD SPY ON Us", "?"],

        ["What three words would you use to describe your diet?", 
        "A. Provisional, Ignominious, Surreptitious", 
        "B. Protein Powder, Keto, Taco Bell", 
        "C. Artificial, Kawaii, PizzaRolls", 
        "D. Exclusively, Microwaved, Hotdogs" "?"],

        ["Where is the place that you feel most comfortable?", 
        "A. Chin-deep in a theoretical post-math textbook", 
        "B. Wherever the smell of a locker room can be found", 
        "C. In the comments section of a Youtube video defending the inherent value in telling prospective mates about your sword collection", 
        "D. Under a space blanket in your budget fallout shelter, drifting off to the sound of the 'Aliens are real, Mom!' podcast #326" "?"],

        ["", "", "", "", ""],

        ["", "", "", "", ""],

        ["", "", "", "", ""],

        ["", "", "", "", ""],

        ["", "", "", "", ""]]

    name = ''
    intelligence = 0
    strength = 0
    endurance = 0
    agility = 0
    luck = 0
    armor = hShirt
    weapon = nails

    bob(name, city, intelligence, strength, endurance, agility, luck, armor, weapon)

    return bob

#### end functions relating directly to gameplay ####

################### main area #####################

print("Welcome to Bob.")
print()
time.sleep(2)
print("Made by Ethan?") 
print()
time.sleep(2)

#### testing area

bob = characterCreate()

bob.addWeapon(manholeCover)

bob.changeWeapon()

print(bob.displayStats())
bob.changeWeapon()

print(bob.displayStats())

#### end testing area

# the premise: You are Bob. Bob accidentally went into work dressed like it was casual friday, but it wasn't casual friday. Bob is now fired. Bob must find new purpose.

# Location ideas: start in city, progress outward toward mountains. city, suburbs, rural, dark forest, scary mountain?

### main flow of the game: each location is like a puzzle room/scenario you need to figure out how to escape, which leads to the next location. If you lose a fight, you start over at the beginning of the scenario.
### start in the city, where you'll have to fight things in order to earn the money to pay some sleazebag to help you break into a car.
### Car runs out of gas in suburbs (or possibly you wreck because of a stray ball?). Here you'll have to choose the right sequence of commands to progress,(good, bad, and neutral options?) 
### leading you through a series of progressively tougher fights. You fail if you choose a bad sequence of commands or if you lose in a fight.
### After badly freaking out a suburban family (beating up the dad possibly?), you're chased by police into the rural area.
### The rural area has you going down branching paths with certain things at the end. Most paths end in a fight, one with special weapon, one with secret teller, and one with the enlightened hick who directs you to the next scenario.
### The enlightened hick directs you into the woods. Here enemy encounters will be randomized. 
### The correct sequence of directional commands will lead to the next scenario. Chudley Dangis can either be convinced with money or a specific sequence of correct commands
### to give you a map to the mountain, which is the final scenario. He also can give hints to find the Squatchblade, which is necessary to progress a certain way through the final scenario.
### Now 3 (undecided challengers) stand between you and the Summit. You may choose to fight them (almost guaranteed loss if you haven't found the Squatchblade), or participate in 
### their challenges. If you fail a challenge, they take a chunk of your health but if it doesn't kill you you can try again. One will quiz you about the game, one will force you 
### to sacrifice all accumulated points in a certain stat if you haven't accumulated enough money, and the last gives a very difficult riddle. If you have the Squatchblade and choose to fight you must fight all three.
### Also, your blade will be broken at the end. If you get the blade but don't use it you get access to a secret ending at the summit. 
### At the Summit you must fight the final foe or if you have the intact Squatchblade, you have the option to fight or to "end the cycle" (what this means I don't know yet.)
### if you lose you return to the beginning of the mountain scenario.


##### character ideas: 
# Chudley Dangis, shopkeeper who uses weird, fake words/language. Thinks he's funny, but the main character finds him grating. (based off me)