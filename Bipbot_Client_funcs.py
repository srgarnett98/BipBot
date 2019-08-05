import numpy as np
import matplotlib.pyplot
import scipy
import scipy.stats
import time

import discord
import PyQt5

def bipDict(members, game, channel, guild, status):
    bip_status = {}
    bip_status[members] = members
    bip_status[game] = game
    bip_status[channel] = channel
    bip_status[guild] = guild
    bip_status[status] = status

class config:
    def __init__(self):
        self.channels = []
        self.excludes = []
        self.alerts = True
        self.smol_bip = False

class bipHost:
    def __init__:

        

def recieve():

def ping_bipbot():


def bip_message(bip_status):
    message = ""
    message += str(len(bip_status[members])) + " person bip in channel "
    message += str(bip_status[channels]) + ", playing "
    message += str(bip_status[game])

async def bip_change(bip_status, settings):
    if (bip_status[channel] in settings.channels):
        if bip_status[game] in settings.excludes:
            icon_set("orange")
        elif len(bip_status[members]) == 2 and bip_status[game] != 'Various':
            icon_set("blue")
            if settings.smol_bip and settings.alerts:
                alert(bip_message(bip_status))
        elif len(bip_status[members]) > 2:
            icon_set("green")
            if settings.alerts:
                alert(bip_message(bip_status))
        elif len(bip_status[members]) <2:
            icon_set("red")
