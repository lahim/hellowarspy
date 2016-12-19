# -*- coding: utf-8 -*-
from __future__ import absolute_import

from tornado.web import RequestHandler, escape

from warspy.models import Arena

__author__ = 'lahim'


class View(RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def data_received(self, chunk):
        pass

    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, *args, **kwargs):
        ctx = self.get_context_data(**kwargs)
        self.write(ctx)

    def send_error(self, status_code=500, **kwargs):
        self.write({
            "error_code": kwargs.get("error_code", 400),
            "error_message": kwargs.get("error_message"),
        })


class IndexView(View):
    def get_context_data(self, **kwargs):
        ctx = {
            "message": "It works!",
            "status": "OK"
        }
        return ctx


class ArenaView(View):
    def get_context_data(self, **kwargs):
        arena = Arena.get_arena()

        arena.play_round()

        return arena.to_json()

    def post(self, *args, **kwargs):
        post_data = escape.json_decode(self.request.body)

        # todo: validate post date
        bot_name = post_data.get("name")
        bot_url = post_data.get("url")

        self.add_header("Content-Type", "application/json")

        if bot_name and bot_url:
            arena = Arena.get_arena()
            try:
                bot = arena.register_bot(name=bot_name, url=bot_url)
            except Arena.BotAlreadyRegisteredException, e:
                self.send_error(status_code=400, error_message=e.message)
                return
            else:
                response_data = bot.to_json()
                self.write(response_data)
        else:
            self.send_error(status_code=400, error_message="Name or url was not defined")
            return
