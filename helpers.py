import traceback

from discord.ext.commands import CommandNotFound, CheckFailure

from config import conf

def checkers_register(bot):
	@bot.check
	def guild_checker(ctx):
		server_id = int(conf('server', 'id'))
		return server_id == ctx.guild.id

def error_handler_register(bot):
	@bot.event
	async def on_command_error(ctx, error):
		if isinstance(error, CommandNotFound):
			return
		elif isinstance(error, CheckFailure):
			await ctx.reply(content='Ошибка в команде: %s' % str(error))
		else:
			with open('log.error', 'a') as f:
				traceback.print_exception(type(error), error, error.__traceback__, file=f)
		

def set_channel_id(channel_id):
	def decor(view):
		async def wrapper(ctx,  *args, **kwargs):
			native_id = ctx.channel.id
			ctx.channel.id = channel_id
			await view(ctx, *args, **kwargs)
			ctx.channel.id = native_id
		return wrapper
	return decor