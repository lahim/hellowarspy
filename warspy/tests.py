# -*- coding: utf-8 -*-
from __future__ import absolute_import

from unittest import TestCase

from warspy.models import Arena, Bomb

__author__ = 'lahim'


class ArenaTestCase(TestCase):
    def setUp(self):
        self.arena = Arena.build(20, 20)

    def test_generate_map(self):
        print "ArenaTestCase.test_generate_map <-"
        self.arena.print_map()
        print "ArenaTestCase.test_generate_map ->"

    def test_play_round(self):
        print "ArenaTestCase.test_play_round <-"
        self.arena.play_round()
        print "ArenaTestCase.test_play_round ->"

    def test_bomb_explosion_range(self):
        print "ArenaTestCase.test_bomb_explosion_range <-"

        bomb = Bomb(
            location=[4, 3],
            tte=1,
            explosion_range=6,
            arena=self.arena
        )
        bomb.check()

        print "^" * 80
        self.arena.print_map()
        print "^" * 80

        bomb.check()
        print "^" * 80
        self.arena.print_map()
        print "^" * 80

        print "ArenaTestCase.test_bomb_explosion_range ->"
