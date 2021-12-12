import discord
from discord.ext import commands

from config import conf
from commands.ladder import ladderGroup
from helpers import checkers_register, error_handler_register
	
if __name__ == '__main__':
	bot = commands.Bot(command_prefix=conf('bot', 'prefix'))

	checkers_register(bot)
	error_handler_register(bot)

	ladderGroup(bot)
	bot.run(conf('bot', 'token'))