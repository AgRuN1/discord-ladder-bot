from views import *
from models.players import Players, PlayersChecker
from models.calls import Calls, CallsChecker

def ladderGroup(bot):

	@bot.command(name='addme')
	@PlayersChecker(['out_ladder'])
	async def add(ctx, *args):
		players = Players()
		user = ctx.author
		players.add_player(user.id, user.name)

		await log_new_user(ctx)
		await change_table(ctx, players.get_list())

	@bot.command(name='leave')
	@PlayersChecker(['in_ladder'])
	async def leave(ctx, *args):
		players = Players()
		players.delete_player(ctx.author.id)

		await leave_user(ctx)
		await change_table(ctx, players.get_list())

	@bot.command(name='call')
	@PlayersChecker(['in_ladder', 'is_mention', 'mention_in_ladder'])
	@CallsChecker(['is_free', 'is_correct'])
	async def call(ctx, *args):
		called = ctx.message.mentions[0]
		caller = ctx.author
		
		await log_new_call(ctx, caller, called)