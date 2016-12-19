# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from warspy import utils

__author__ = 'lahim'

DIRECTION_TYPE = (
    (0, "Up"),
    (1, "Right"),
    (2, "Down"),
    (3, "Left"),
)

ACTION_TYPE = (
    (0, "None"),
    (1, "Drop bomb"),
    (2, "Fire missile"),
)

TILE_TYPE = (
    (0, "Blank"),
    (1, "Brick"),
    (2, "Iron"),
)


class BaseModel(object):
    def to_json(self):
        result = {}
        for field in self.Meta.fields:
            if hasattr(self, field):
                value = getattr(self, field)
                result[field] = value
            elif hasattr(self, "get_%s" % field):
                value = getattr(self, "get_%s" % field)()
                result[field] = value
        return result

    class Meta:
        fields = ()


class Arena(BaseModel):
    instance = None

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._map = self.generate_map()
        self._bots = {}
        self._bombs = []
        self._missiles = []

    def generate_map(self):
        def _random_tile(value):
            value = int(value)
            if value == 1:
                value = random.randrange(0, 3)
            return value

        matrix = [0] * self.height
        for row in xrange(self.height):
            matrix[row] = [_random_tile(x) for x in list("%020d" % int(bin(random.randint(0, 2 ** 20 - 1))[2:]))]
        return matrix

    def print_map(self):
        for x in xrange(self.height):
            print self._map[x]

    def register_bot(self, name, url):
        result = filter(lambda b: b.url == url, self._bots.values())
        if len(result) == 0:
            bot = Bot(name=name, url=url, arena=self)
            self._bots[bot.id] = bot
            return bot
        else:
            raise self.BotAlreadyRegisteredException("Bot with url '%s' is already registered" % url)

    def set_tile(self, value, x, y):
        self._map[y][x] = value

    def tile_explosion(self, x, y):
        value = self._map[y][x]
        if value == 2:
            value = 1
        elif value == 1:
            value = 0
        self._map[y][x] = value

    def get_map(self):
        return self._map

    def get_bot(self, bot_id):
        return self._bots.get(bot_id)

    def get_bots(self):
        return [bot.to_json() for bot in self._bots.values()]

    def get_bombs(self):
        return [bomb.to_json() for bomb in self._bombs]

    def get_size(self):
        return self.width, self.height

    def play_round(self):
        for bot in self._bots.values():
            bot.perform_move()

        for bomb in self._bombs:
            bomb.check()

    @classmethod
    def get_arena(cls):
        if cls.instance is None:
            cls.instance = cls.build(20, 20)
            cls.instance._bombs.append(Bomb([4, 3], 6, 6, cls.instance))
        return cls.instance

    @classmethod
    def build(cls, rows=20, cols=20):
        return cls(rows, cols)

    class Meta(BaseModel.Meta):
        fields = ('size', 'bots', 'bombs', 'missiles', 'map',)

    class BotAlreadyRegisteredException(Exception):
        pass


class Bot(BaseModel):
    def __init__(self, name, url, arena):
        self.id = utils.generate_token()
        self.name = name
        self.url = url
        self.arena = arena
        self.is_winner = False
        self.is_active = True
        self.location = self._generate_location()
        self.move_direction = None
        self.action_type = None
        self.fire_direction = None

    def _generate_location(self):
        loc = [
            random.randrange(0, self.arena.width - 1),
            random.randrange(0, self.arena.height - 1)
        ]
        self.arena.set_tile(TILE_TYPE[0][0], loc[0], loc[1])
        return loc

    def perform_move(self):
        direction = random.randrange(0, 4)

        width = self.arena.width
        height = self.arena.height

        loc = [self.location[0], self.location[1]]

        if direction == 0 and loc[1] > 0:  # up
            loc[1] -= 1

        if direction == 2 and loc[1] < height - 1:  # down
            loc[1] += 1

        if direction == 1 and loc[0] < width - 1:  # right
            loc[0] += 1

        if direction == 3 and loc[0] > 0:  # left
            loc[0] -= 1

        if self.arena.get_map()[loc[1]][loc[0]] == 0:
            self.location = loc

    def __hash__(self):
        return self.id

    class Meta(BaseModel.Meta):
        fields = ('id', 'name', 'url', 'location',)


class Bomb(BaseModel):
    def __init__(self, location, tte, explosion_range, arena):
        self.location = location
        self.explosion_range = explosion_range
        self.arena = arena
        self.tte = tte  # time to explosion
        self._destruction = list()

    def check(self):
        if self.tte >= 0:
            self.tte -= 1

        if self.tte == 0:
            width = self.arena.width
            height = self.arena.height

            x, y = self.location
            for idx in xrange(0, self.explosion_range + 1):
                # right
                _x, _y = x + idx, y
                _x = width - 1 if _x >= width else _x
                self.arena.tile_explosion(_x, _y)
                self._destruction.append((_x, _y))

                # left
                _x, _y = x - idx, y
                _x = 0 if _x <= 0 else _x
                self.arena.tile_explosion(_x, _y)
                self._destruction.append((_x, _y))

                # up
                _x, _y = x, y - idx
                _y = 0 if _y <= 0 else _y
                self.arena.tile_explosion(_x, _y)
                self._destruction.append((_x, _y))

                # down
                _x, _y = x, y + idx
                _y = height if _y >= height else _y
                self.arena.tile_explosion(_x, _y)
                self._destruction.append((_x, _y))

    def get_destruction(self):
        return self._destruction

    class Meta(BaseModel.Meta):
        fields = ("location", "explosion_range", "destruction", "tte",)
