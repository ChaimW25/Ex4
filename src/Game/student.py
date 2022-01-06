"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import json

from types import SimpleNamespace
from src.Game.GameManager import GameManager

import pygame
from pygame import *
from pygame import gfxdraw
import time


from src.Game.client import Client


YELLOWPOKENON=pygame.image.load('../Images/pikachu.png')
OurYellow=pygame.transform.scale(YELLOWPOKENON,(50,50))
AGENT=pygame.image.load('../Images/ash.png')
OurAgent=pygame.transform.scale(AGENT,(80,80))
BACKGROUNDIMG=pygame.image.load('../Images/pknature.jpg')
OurImg=pygame.transform.scale(BACKGROUNDIMG,(1080, 720))
ORANGEPOKEMON=pygame.image.load('../Images/orange.png')
OurOrange=pygame.transform.scale(ORANGEPOKEMON,(50,50))






# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
# print the background img
clock = pygame.time.Clock()
pygame.font.init()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))
print(pokemons_obj)
print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('Arial', 20, bold=False)
BIGFONT = pygame.font.SysFont('Arial', 40, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

 # get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)

def button(msg, x, y, w, h, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(screen, (255, 0, 0), (x, y, w, h))
    id_srg = BIGFONT.render(msg, True, Color(0, 0, 0))
    rect4 = id_srg.get_rect(center=((x + (w / 2)), (y + (h / 2))))
    screen.blit(id_srg, rect4)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if click[0] == 1:
            action()

radius = 15
manager = GameManager(client)
# client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":7}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""
pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
# manager = GameManager(client)
# manager.load_pokemon()
# manager.load_agent()
# manager.load_info()
# manager.load_graph()



while client.is_running() == 'true':

    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons

    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents

    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))


    moves = json.loads(client.get_info(),
                       object_hook=lambda d: SimpleNamespace(**d))  # .GameServer



    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.blit(OurImg, (0, 0))
    time_left = int(client.time_to_end())
    seconds, milliseconds = divmod(time_left, 1000)
    screen.blit(BIGFONT.render('Time left: {}.{}'.format(seconds, milliseconds), True, (0, 0, 0)), (30, 0))
    button("STOP", 935, 30, 100, 100, client.start_connection)

    curr_moves = moves.GameServer.moves
    curr_grade = moves.GameServer.grade
    # print moves
    screen.blit(BIGFONT.render('Number of moves: {}'.format(curr_moves), True, (0, 0, 0)), (30, 50))
    # print grade
    screen.blit(BIGFONT.render('Grade: {}'.format(curr_grade), True, (0, 0, 0)), (30, 100))

    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(0, 0, 0))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(0, 0, 0),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        # pygame.draw.circle(screen, Color(122, 61, 23),
        #                    (int(agent.pos.x), int(agent.pos.y)), 10)
        screen.blit(OurAgent,((int(agent.pos.x-50), int(agent.pos.y)-20))) #.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        # pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
        if p.type<0:
            screen.blit(OurYellow,((int(p.pos.x), int(p.pos.y)))) #.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)
        else:
            screen.blit(OurOrange,((int(p.pos.x), int(p.pos.y)))) #.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    manager.update()
    manager.allocate_all_agents()


    # choose next edge
    # for agent in agents:
    #     if agent.dest == -1:
    #         next_node = (agent.src - 1) % len(graph.Nodes)
    #         client.choose_next_edge(
    #             '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
    ttl = client.time_to_end()
    print(ttl, client.get_info())

    client.move()
    time.sleep(0.1)


# game over: