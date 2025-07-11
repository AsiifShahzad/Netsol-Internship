import math
import random
import time


class Nim():

    def __init__(self, initial=[1, 3, 5, 7]):
        self.piles = initial.copy()
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, piles):
        actions = set()
        for i, pile in enumerate(piles):
            for j in range(1, pile + 1):
                actions.add((i, j))
        return actions

    @classmethod
    def other_player(cls, player):
        return 0 if player == 1 else 1

    def switch_player(self):
        self.player = Nim.other_player(self.player)

    def move(self, action):
        pile, count = action
        if self.winner is not None:
            raise Exception("Game already won")
        if pile < 0 or pile >= len(self.piles):
            raise Exception("Invalid pile")
        if count < 1 or count > self.piles[pile]:
            raise Exception("Invalid number of objects")
        self.piles[pile] -= count
        self.switch_player()
        if all(p == 0 for p in self.piles):
            self.winner = self.player


class NimAI():

    def __init__(self, alpha=0.5, epsilon=0.1):
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Returns Q-value of (state, action); default = 0 if unseen
        """
        return self.q.get((tuple(state), action), 0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Q-learning update:
        Q'(s,a) = old_q + α * ((reward + future_rewards) - old_q)
        """
        self.q[(tuple(state), action)] = old_q + self.alpha * (
            (reward + future_rewards) - old_q
        )

    def best_future_reward(self, state):
        """
        Float: max Q-value across all available actions from state; 0 if none exist
        """
        actions = Nim.available_actions(state)
        if not actions:
            return 0
        return max(self.get_q_value(state, action) for action in actions)

    def choose_action(self, state, epsilon=True):
        """
        Return selected action:
          - If epsilon=True, choose random action with probability ε
          - Otherwise always select best-Q action
        """
        actions = Nim.available_actions(state)
        if not actions:
            return None

        # Exploration step
        if epsilon and random.random() < self.epsilon:
            return random.choice(list(actions))

        # Exploitation step
        max_q = float('-inf')
        best_actions = []
        for action in actions:
            q_val = self.get_q_value(state, action)
            if q_val > max_q:
                max_q = q_val
                best_actions = [action]
            elif q_val == max_q:
                best_actions.append(action)

        return random.choice(best_actions)


def train(n):
    player = NimAI()

    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Nim()
        last = {0: {"state": None, "action": None},
                1: {"state": None, "action": None}}

        while True:
            state = game.piles.copy()
            action = player.choose_action(game.piles)
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            game.move(action)
            new_state = game.piles.copy()

            if game.winner is not None:
                player.update(state, action, new_state, -1)
                player.update(last[game.player]["state"],
                              last[game.player]["action"],
                              new_state, 1)
                break
            elif last[game.player]["state"] is not None:
                player.update(last[game.player]["state"],
                              last[game.player]["action"],
                              new_state, 0)

    print("Done training")
    return player


def play(ai, human_player=None):
    if human_player is None:
        human_player = random.randint(0, 1)

    game = Nim()
    while True:
        print("\nPiles:")
        for i, pile in enumerate(game.piles):
            print(f"Pile {i}: {pile}")
        print()
        available = Nim.available_actions(game.piles)
        time.sleep(1)

        if game.player == human_player:
            print("Your Turn")
            while True:
                pile = int(input("Choose Pile: "))
                count = int(input("Choose Count: "))
                if (pile, count) in available:
                    break
                print("Invalid move, try again.")
        else:
            print("AI's Turn")
            pile, count = ai.choose_action(game.piles, epsilon=False)
            print(f"AI chose to take {count} from pile {pile}.")

        game.move((pile, count))

        if game.winner is not None:
            print("\nGAME OVER")
            winner = "Human" if game.winner == human_player else "AI"
            print(f"Winner is {winner}")
            return
