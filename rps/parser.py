from .model import RPS

#? Is parsing needed?
class RockPaperScissorParser:
    def __init__(self, choice) -> None:
        choice = choice.lower()
        # parsing to str to RPS
        match choice:
            case RPS.ROCK:
                self.choice = RPS.ROCK
            case RPS.PAPER:
                self.choice = RPS.PAPER
            case RPS.SCISSOR:
                self.choice = RPS.SCISSOR