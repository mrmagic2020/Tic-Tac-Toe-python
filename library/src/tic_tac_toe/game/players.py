import abc
import time
import random
from typing import Union

from tic_tac_toe.logic.exceptions import InvalidMove
from tic_tac_toe.logic.models import GameState, Mark, Move


# An abstract class is a class that is designed to be inherited from
# It is not designed to be instantiated, and does not stand on its own
# Its only purpose is to provide a skeketon for subclasses
class Player(metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark) -> None:
        self.mark = mark

    def make_move(self, game_state: GameState) -> GameState:
        if self.mark is game_state.current_mark:
            if move := self.get_move(game_state):
                return move.after_state
            raise InvalidMove("No more possible moves")
        else:
            raise InvalidMove("It's the other player's turn")

    # An abstract method is a method that is declared, but contains no implementation
    # It is only meant to be overridden in subclasses
    @abc.abstractmethod
    def get_move(self, game_state: GameState) -> Union[Move, None]:
        """Return the current player's move in the given game state."""


class ComputerPlayer(Player, metaclass=abc.ABCMeta):
    def __init__(self, mark: Mark, delay_seconds: float = 0.25) -> None:
        super().__init__(mark)
        self.delay_seconds = delay_seconds

    def get_move(self, game_state: GameState) -> Union[Move, None]:
        time.sleep(self.delay_seconds)
        return self.get_computer_move(game_state)

    @abc.abstractmethod
    def get_computer_move(self, game_state: GameState) -> Union[Move, None]:
        """Return the computer's move in the given game state."""


class RandomComputerPlayer(ComputerPlayer):
    def get_computer_move(self, game_state: GameState) -> Union[Move, None]:
        try:
            return random.choice(game_state.possible_moves)
        except IndexError:
            return None
