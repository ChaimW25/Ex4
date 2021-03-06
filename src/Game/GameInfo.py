
class GameInfo:

    def __init__(self, pokemons: int, is_logged_in: bool, moves: int, grade: int,  game_level: int, max_user_level: int, id: int, graph: str, agents: int):

        self.pokemons = pokemons
        self.is_logged_in = is_logged_in
        self.moves = moves
        self.grade = grade
        self.game_level = game_level
        self.max_user_level = max_user_level
        self.id = id
        self.graph = graph
        self.agents = agents

    def num_of_pokemons(self) -> int:
        return self.pokemons

    def num_of_agents(self) -> int:
        return self.agents

    def get_graph_name(self) -> str:
        return self.graph

