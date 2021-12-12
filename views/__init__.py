from config import conf
from settings import Settings
from helpers import set_channel_id

@set_channel_id(conf('server', 'table_channel'))
async def change_table(ctx, players):
	settings = Settings()
	msg = await ctx.fetch_message(settings.get('table_message'))
	rows = []
	for player in players:
		position = player.position
		user = await player.get_user(ctx.bot)
		rows.append('{}. {}'.format(position, user.mention))

	await msg.edit(content='\n'.join(rows))

log_channel = conf('server', 'log_channel')

@set_channel_id(log_channel)
async def log_new_user(ctx):
	await ctx.send('Пользователь {} записался в ладдер'.format(ctx.author.mention))

@set_channel_id(log_channel)
async def leave_user(ctx):
	await ctx.send('Пользователь {} покидает ладдер'.format(ctx.author.mention))

@set_channel_id(log_channel)
async def log_new_call(ctx, caller, called):
	await ctx.send('Пользователь {} вызывает {}'.format(caller.mention, called.mention))