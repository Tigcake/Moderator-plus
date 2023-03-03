import nextcord
from nextcord.ext import commands
import datetime
import asyncio
import json
import os
import random

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pass

def setup(bot):
    bot.add_cog(ExampleCog(bot))