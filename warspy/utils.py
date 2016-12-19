# -*- coding: utf-8 -*-

import os
import binascii

__author__ = 'lahim'


def generate_token(length=20):
    """ Generates token.
    :param length: Generates token of selected length (default 20)
    :return: token
    """
    return binascii.hexlify(os.urandom(length)).decode()

