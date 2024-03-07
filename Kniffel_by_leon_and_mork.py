import random, os

def clear_screen():
    os.system('cls')

def press_enter():
    input("Press ENTER to continue!")

def get_user_input(message):
    result = message
    if result.lower() == 'quit':
        clear_screen()
        quit_code = input("Do you really want to quit?\n[Y / N]\n> ").lower()
        if quit_code == "y":
            quit()
        else:
            return result
    else:
        return result

class Kniffel:
    def __init__(self) -> None:
        self.player_scorecards = {}
        self.categories = ['1', '2', '3', '4', '5', '6', '3pash', '4pash', 'fullhouse', 'kleine_straße', 'große_straße',
                           'kniffel', 'chance']
        self.dice = []
        self.dice = []
        self.reroll_counter = 1

    def ask_playersize(self):
        while True:
            ask_playersize = input("How many players?\n> ")
            result = get_user_input(ask_playersize)
            ask_playersize = result
            try:
                ask_playersize = int(ask_playersize)
                break
            except Exception:
                print("Only numbers please.")
                press_enter()
                clear_screen()
            finally:
                clear_screen()
        for player in range(1, ask_playersize + 1):
            self.player_scorecards[player] = {category: None for category in self.categories}

    def show_category(self):
        pass

    def roll_dice(self):
        self.dice = [random.randint(1, 6) for _ in range(5)]

    def display_dice(self):
        return self.dice

    def reroll(self):
        self.roll_dice()
        max_rerolls = 3
        rerolls_remaining = max_rerolls

        while rerolls_remaining > 0:
            rollagain = input(f"Which dice would you like to re-roll\n{self.display_dice()}\n> ")
            result = get_user_input(rollagain)
            rollagain = result
            if not rollagain:
                break

            try:
                selected_dice = [int(num) - 1 for num in rollagain.split(',')]
                for index in selected_dice:
                    if 0 <= index < 5:
                        self.dice[index] = random.randint(1, 6)
                    else:
                        print("Invalid dice index. Please enter valid indices.")
                        rerolls_remaining += 1

                rerolls_remaining -= 1

            except Exception:
                clear_screen()
                print("Invalid input. Please enter valid dice indices.")
                rerolls_remaining += 1
                press_enter()
                clear_screen()
            finally:
                clear_screen()

    def print_scorecard(self, player):
        print(f"Player {player}'s Scorecard:")
        for category, score in self.player_scorecards[player].items():
            print(f"{category}: {score if score is not None else ''}")
        print()

    def choose_category(self, player):
        while True:
            try:
                self.print_scorecard(player)
                print(self.dice)
                category = input("Choose a category: ")
                result = get_user_input(category)
                category = result

                while self.player_scorecards[player][category] is not None:
                    clear_screen()
                    print("Category already chosen, choose again.")
                    self.print_scorecard(player)
                    print(self.dice)
                    category = input("Choose a category: ")
                    result = get_user_input(category)
                    category = result
                break
            except Exception:
                clear_screen()
                print("Invalid input.")
                press_enter()
                clear_screen()
            finally:
                clear_screen()

        return category

    def calculate_score(self, category):
        if category == '1':
            return self.dice.count(1) * 1
        elif category == '2':
            return self.dice.count(2) * 2
        elif category == '3':
            return self.dice.count(3) * 3
        elif category == '4':
            return self.dice.count(4) * 4
        elif category == '5':
            return self.dice.count(5) * 5
        elif category == '6':
            return self.dice.count(6) * 6
        elif category == '3pash':
            if any(self.dice.count(i) >= 3 for i in range(1, 7)):
                return sum(self.dice)
        elif category == '4pash':
            if any(self.dice.count(i) >= 4 for i in range(1, 7)):
                return sum(self.dice)
        elif category == 'fullhouse':
            if sorted(self.dice.count(i) for i in range(1, 7)) == [2, 3]:
                return 25
        elif category == 'kleine_straße':
            if any(self.dice.count(i) > 0 for i in range(1, 6)) and not any(
                    self.dice.count(i) == 0 for i in range(2, 6)):
                return 30
        elif category == 'große_straße':
            if any(self.dice.count(i) > 0 for i in range(2, 7)) and not any(
                    self.dice.count(i) == 0 for i in range(3, 7)):
                return 40
        elif category == 'kniffel':
            if any(self.dice.count(i) == 5 for i in range(1, 7)):
                return 50
        elif category == 'chance':
            return sum(self.dice)

        return 0

    def add_bonus(self, player):
        upper_section_categories = ['1', '2', '3', '4', '5', '6']
        upper_section_sum = sum(self.player_scorecards[player][category] for category in upper_section_categories if
                                self.player_scorecards[player][category] is not None)

        if upper_section_sum >= 54:
            self.player_scorecards[player]['bonus'] = 35

game = Kniffel()

game.ask_playersize()

for round_num in range(1, len(game.categories) * len(game.player_scorecards) + 1):
    clear_screen()
    print("Round", round_num, "\n")

    for player in range(1, len(game.player_scorecards) + 1):
        game.reroll_counter = 1

        for _ in range(game.reroll_counter):
            print("Player", player)
            game.reroll()
        clear_screen()
        category = game.choose_category(player)

        score = game.calculate_score(category)
        game.player_scorecards[player][category] = score
        print("Score:", score)
        
        if round_num == len(game.categories) * len(game.player_scorecards):
            game.add_bonus(player)
        
        press_enter()
        clear_screen()

print("\nGame Over! Final Scores:")
for player, scorecard in game.player_scorecards.items():
    total_score = sum(scorecard.values())
    print(f"Player {player}: {total_score}")