#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.ioloop import IOLoop
from tornado.web import Application

from warspy import routes

__author__ = 'lahim'


def run(port):
    app = Application(routes.urls)
    app.listen(port=port)
    IOLoop.current().start()


if __name__ == "__main__":
    run(port=8000)
