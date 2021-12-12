from models import Database, Checker

class Player:
	def __init__(self, row):
		self.id = row[0]
		self.name = row[1]
		self.position = row[2]

	async def get_user(self, bot):
		user = await bot.fetch_user(self.id)
		return user

	def __str__(self):
		return self.name

class Players(Database):

	_table = 'players'
	_type = Player

	def add_player(self, id, name, position=0):
		if position == 0:
			position = self.count() + 1
		sql = "INSERT INTO {} VALUES(?, ?, ?)"
		self.execute(sql, (id, name, position))
		self.save()

	def get_player(self, player_id):
		sql = 'SELECT * FROM {} WHERE id=?'
		self.execute(sql, (player_id,))
		res = self._cursor.fetchone()
		if res:
			return self._type(res)
		return False

	def delete_player(self, player_id):
		player = self.get_player(player_id)
		sql = 'DELETE FROM {} WHERE id=?'
		self.execute(sql, (player_id,))

		sql = 'UPDATE {} SET position = position - 1 WHERE position > ?'
		self.execute(sql, (player.position,))
		self.save()

class PlayersChecker(Checker):
	def is_mention(self, ctx):
		"""укажите пользователя"""
		return len(ctx.message.mentions) > 0

	def mention_in_ladder(self, ctx):
		"""укажите пользователя из ладдера"""
		user = ctx.message.mentions[0].id
		return bool(Players().get_player(user))

	def in_ladder(self, ctx):
		"""вы должны быть в ладдере для этой команды"""
		return bool(Players().get_player(ctx.author.id))

	def out_ladder(self, ctx):
		"""вы не можете выполнять эту команду будучи в ладдере"""
		return not bool(Players().get_player(ctx.author.id))
