import random

class Mobile_Suit:
    # creates a mobile suit, give it a name, and level. Its max health is determined by its level. Its starting health is its max health and it is not knocked out when it starts.
    def __init__(self, name, era, level = 5, self_healing = False, critical_chance = 0, phrase =" "):
        self.name = name
        self.era = era
        self.level = level
        self.health = level * 5
        self.max_health = level * 5
        self.is_destroyed = False
        self.heal = self_healing
        self.crit_hit = critical_chance
        self.crit_phrase = phrase
        
    def __repr__(self):
        return "This level {level} {name} has {health} hit points. They are from the {era} timeline.".format(level = self.level, name = self.name, health=self.health, era = self.era)
    
    def destroyed(self):
        self.is_destroyed = True
        if self.health != 0:
            self.health = 0
        print("{name} has been destroyed!".format(name = self.name))
        return
        
    def lose_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            #Makes sure the health doesn't become negative
            self.health = 0
            self.destroyed()
        else:
            print("{name} now has {health} health.".format(name = self.name, health = self.health))
        
    def auto_heal(self):
        #if ms has self healing, this will determine if that ms will be able to heal after attacking
        chanceForHealth = random.randint(1, 9)
        if (chanceForHealth % 2 == 0):
            random_number = 2 * random.randint(1, 9)
            self.health += random_number
            if self.health >= self.max_health:
                self.health = self.max_health
            print("{name}'s self healing has activated! It recovered {heal} health points!, total health is now at {maxh} points!".format(name = self.name, heal=random_number, maxh=self.health))
        else:
            print("{name}'s self healing failed to activate!".format(name=self.name))
            
    def second_hit(self):
        #determines if there will be a second attack
        secondHit = random.randint(0, 9)
        if (secondHit % 2 == 0):
            self.crit_attack()
        else:
            self.crit_hit = 0
            self.crit_phrase = "No second hit"
        
    def crit_attack(self):
        #will pick random number and determine how effective second attack will be
        critChance = random.randint(0, 9)
        if (critChance % 2 == 0):
            crit = random.randint(0, 9)
            if crit <= 3:
                #print(self.crit_hit)
                self.crit_hit = .02 * self.level
                self.crit_phrase = "Second hit did {damage} damage. It was an average hit!".format(damage=round(self.crit_hit * self.level))
            elif crit <= 5:
                self.crit_hit = .03 * self.level
                #print(self.crit_hit)
                self.crit_phrase = "Second hit did {damage} damage. It was a good hit!".format(damage=round(self.crit_hit * self.level))
            elif crit <= 9:
                #print(self.crit_hit)
                self.crit_hit = .05 * self.level
                self.crit_phrase = "Second hit did {damage} damage. It was a critical hit!".format(damage=round(self.crit_hit * self.level))
        else:
            #will call itself again to get a number to work
            #should be reworked, combine with second_hit?
            self.crit_attack()

    def attack(self, enemy_ms):
        if self.is_destroyed:
            print("{name} can't attack because it is destroyed!".format(name = self.name))
            return
        #higher level ms does more damage
        if (self.level > enemy_ms.level):
            self.second_hit()
            print("The higher leveled {my_name} attacked {other_name} for {damage} damage. {move}!".format(my_name = self.name, other_name = enemy_ms.name, damage = self.level * 2, crit= self.crit_hit, move=self.crit_phrase))
            enemy_ms.lose_health(self.level * 2)
            enemy_ms.lose_health(self.crit_hit * self.level)
            if self.heal:
                self.auto_heal()
            #lower suit does a bit less damage than normal
        if (self.level < enemy_ms.level):
            self.second_hit()
            print("The lower leveled {my_name} attacked {other_name} for {damage} damage. {move}!".format(my_name = self.name, other_name = enemy_ms.name, damage = round(self.level * .8), crit= self.crit_hit, move=self.crit_phrase))
            enemy_ms.lose_health(round(self.level * .8))
            enemy_ms.lose_health(round(self.crit_hit * self.level))
            if self.heal:
                self.auto_heal()
        if (self.level == enemy_ms.level):
            self.second_hit()
            print("{my_name} attacked {other_name} for {damage} damage. {move}!".format(my_name = self.name, other_name = enemy_ms.name, damage = self.level, crit= round(self.crit_hit * self.level), move=self.crit_phrase))
            enemy_ms.lose_health(self.level)
            enemy_ms.lose_health(round(self.crit_hit * self.level))
            if self.heal:
                self.auto_heal()
                       
class Zaku(Mobile_Suit):
    def __init__(self, level = 5):
        super().__init__("Zaku", "UC", level)

class Guntank(Mobile_Suit):
    def __init__(self, level = 5):
        super().__init__("Guntank", "UC", level)

class Turn_A(Mobile_Suit):
    def __init__(self, level = 5):
        super().__init__("Turn A", "CC", level, True)
        
class Sazabi(Mobile_Suit):
    def __init__(self, level = 5):
        super().__init__("Sazabi", "UC", level)
        
class G_Gundam(Mobile_Suit):
    def __init__(self, level = 5):
        super().__init__("G Gundam", "G", level)
        
class Pilot:
    def __init__(self, current_ms, expierence, fraction, name):
        #expierence should boost some of the ms stats if they are included
        self.ms = current_ms
        self.exp = expierence
        self.fraction = fraction
        self.name = name

    def __repr__(self):
        # returns the name of the pilot, fraction they are part of, years of expiernece, and which mobile suit they are using
        return ("Pilot {name}, of the {fraction}, is ready to go, has {exp} years of ex with this {suit.name}.".format(name = self.name, fraction=self.fraction, exp=self.exp, suit=self.ms))

    def attack_other_pilot(self, enemy_pilot):
        my_mobilesuit = self.ms
        their_mobilesuit = enemy_pilot.ms
        my_mobilesuit.attack(their_mobilesuit)

a = Zaku(20)
b = Guntank(6)
c = Turn_A(20)
d = Sazabi(40)
g = G_Gundam(30)


pilot_one = Pilot(d, 3, "Zeon Fed", "Alex")
pilot_two = Pilot(g, 5, "Earth Fed", "Sara")
pilot_three = Pilot(g, 5, "Moon", "June")

pilot_one.attack_other_pilot(pilot_three)
print("SECOND ATTACK")
pilot_three.attack_other_pilot(pilot_one)
print("third attack")
pilot_three.attack_other_pilot(pilot_one)
