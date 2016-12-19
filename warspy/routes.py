# -*- coding: utf-8 -*-

from warspy import views

__author__ = 'lahim'

urls = [
    (r"/", views.IndexView),
    (r"/arena", views.ArenaView),
]
