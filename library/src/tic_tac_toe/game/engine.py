from dataclasses import dataclass
from typing import Callable, TypeVar, Union

from ..game.players import Player
from ..game.renderers import Renderer
from ..logic.exceptions import InvalidMove
from ..logic.models import GameState, Grid, Mark
from ..logic.validators import validate_players


# Use TypeVar to define a type alias
# Makes it easier to read and understand the code
T = TypeVar("T")
ErrorHandler = Callable[[Exception], T]


@dataclass(frozen=True)
class TicTacToe:
    player1: Player
    player2: Player
    renderer: Renderer
    error_handler: Union[ErrorHandler, None] = None

    def __post_init__(self):
        validate_players(self.player1, self.player2)

    def play(self, starting_mark: Mark = Mark("X")) -> None:
        game_state = GameState(Grid(), starting_mark)
        while True:
            self.renderer.render(game_state)
            if game_state.game_over:
                break
            player = self.get_current_player(game_state)
            try:
                game_state = player.make_move(game_state)
            except InvalidMove as ex:
                if self.error_handler:
                    self.error_handler(ex)

    def get_current_player(self, game_state: GameState) -> Player:
        if game_state.current_mark is self.player1.mark:
            return self.player1
        else:
            return self.player2
