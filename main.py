class Powers:
    all_powers = {'Quick Attack': 10,
                  'Outrage': 20,
                  'Electro Ball': 50,
                  'Bolt Strike': 120,
                  'Smack': 10,
                  'Acrobatics': 40,
                  'Fast Punch': 60,
                  'Extra Sensory': 20,
                  'Rock Tomb': 90}

    def __init__(self):
        self.powers = {}

    def add_power(self, power):
        self.powers[power] = Powers().all_powers[power]

    def get_total_damage(self):
        values = self.powers.values()
        return sum(values)



class Pokemon:
    def __init__(self, name, energy_type="", cost=0, hp=0, weakness=(None, 1), num_wins = 0, taken=False):
        self.name = name
        self.cost = cost
        self.hp = hp
        self.num_wins = 0
        self.energy_type = energy_type
        self.weakness = weakness
        self.powers = Powers()
        self.num_wins = num_wins
        self.taken = taken

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cost(self):
        return self.cost

    def set_cost(self, cost):
        self.cost = cost

    def get_hp(self):
        return self.hp

    def set_hp(self, hp):
        self.hp = hp

    def get_energy_type(self):
        return self.energy_type

    def set_energy_type(self, energy_type):
        self.energy_type = energy_type

    def get_weakness(self):
        return self.weakness

    def set_weakness(self, weakness):
        self.weakness = weakness

    def get_powers(self):
        return self.powers

    def set_powers(self, powers):
        self.powers = powers

    def get_num_wins(self):
        return self.num_wins

    def set_num_wins(self, num_wins):
        self.num_wins = num_wins

    def get_taken(self):
        return self.taken

    def set_taken(self ,taken):
        self.taken = taken

    def receive_damage(self, damage_received):
        self.hp -= damage_received

    def is_healthy(self):
        return self.hp > 0

    def add_power(self, power_name):
        self.powers.add_power(power_name)

    def make_attack(self):
        return self.powers.get_total_damage()

    def battle_step(self, other):
        if self.energy_type == other.weakness[0]:
            other.receive_damage(self.make_attack()*other.weakness[1])
        else:
            other.receive_damage(self.make_attack())

        if self.weakness[0] == other.energy_type:
            self.receive_damage(other.make_attack()*self.weakness[1])
        else:
            self.receive_damage(other.make_attack())

    def battle(self, other):
        while self.is_healthy() and other.is_healthy():
            self.battle_step(other)
        if self.is_healthy():
            self.num_wins += 1
        elif other.is_healthy():
            other.num_wins += 1



    def __str__(self):
        if self.is_healthy():
            hp_string = self.hp
        else:
            hp_string = "is defeated"

        return f"name: {self.name}, hp: {hp_string},  num_wins: {self.num_wins}, taken: False"



class EvolvedPokemon(Pokemon):
    def __init__(self, name, energy_type, cost, hp, weakness=(None,1), damage_booster=0, damage_reducer=0):
        Pokemon.__init__(self, name, energy_type, cost, hp, weakness=(None, 1), num_wins = 0)
        self.damage_booster = damage_booster
        self.damage_reducer = damage_reducer
        self.energy_type = energy_type
        self.weakness = weakness
        self.powers = Powers()

    def set_damage_booster(self, damage_booster):
        self.damage_booster = damage_booster

    def set_damage_reducer(self, damage_reducer):
        self.damage_reducer = damage_reducer

    def get_damage_booster(self):
        return self.damage_booster

    def get_damage_reducer(self):
        return self.damage_reducer

    def make_attack(self):
        return self.powers.get_total_damage() + self.damage_booster

    def receive_damage(self, damage_received):
        self.hp -= (damage_received - self.damage_reducer)



class Trainer:
    def __init__(self, name, xp):
        self.name = name
        self.xp = xp
        self.pokemons = []

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_xp(self):
        return self.xp

    def set_xp(self, xp):
        self.xp = xp

    def get_pokemons(self):
        return self.pokemons

    def set_pokemons(self, pokemons):
        self.pokemons = pokemons

    def add_pokemon(self, other):
        if not other.get_taken():
            if other.cost < self.xp:
                self.pokemons.append(other)
                other.set_taken(True)
                self.xp -= other.cost

    def are_all_defeated(self):
        temp_bool = True
        for i in self.pokemons:
            if i.is_healthy():
                temp_bool = False
        return temp_bool

    def fight(self, other):
        while len(self.pokemons) > 0 and len(other.pokemons) > 0:
            self.pokemons[0].battle(other.pokemons[0])
            if not self.pokemons[0].is_healthy():
                del self.pokemons[0]
            if not other.pokemons[0].is_healthy():
                del other.pokemons[0]
        if len(self.pokemons) > 0:
            print(f"{self.get_name()} wins the fight!")
        if len(other.pokemons) > 0:
            print(f"{other.get_name()} wins the fight!")




if __name__ == '__main__':
    pikachu = Pokemon(name='pikachu', energy_type='Lightning', cost=100, hp=60, weakness=('Fighting', 2))
    pikachu.add_power('Quick Attack')
    pikachu.add_power('Electro Ball')

    raichu = EvolvedPokemon('Raichu', 'Lightning', 800, 90, weakness=('Fighting', 2), damage_booster=30,
                            damage_reducer=0)
    raichu.add_power('Quick Attack')
    raichu.add_power('Electro Ball')

    meloetta = Pokemon('Meloetta', 'Fighting', 100, 80, ('Psychic', 2))
    meloetta.add_power('Smack')
    meloetta.add_power('Acrobatics')

    landorus = EvolvedPokemon('Landorus', 'Fighting', 400, 110, ('Psychic', 2), 20, 20)
    landorus.add_power('Smack')
    landorus.add_power('Acrobatics')

    # create a trainer
    ash = Trainer('Ash', 200)

    # add some pokemon to ash
    ash.add_pokemon(pikachu)
    ash.add_pokemon(raichu)  # Should print "Ash does not have enough xp to get Raichu! Ash has only 100 xp."

    # create another
    gary = Trainer('Gary', 1000)

    # add some pokemon to gary
    gary.add_pokemon(landorus)

    ash.fight(gary)  # Should print "Gary wins the fight!"

