from models import Database, Checker
from models.players import Players

class Call:
	def __init__(self, row):
		self.called = row[0]
		self.called = row[1]
		self.accept = bool(row[2])
		self.date = row[3]

class Calls(Database):

	_table = 'calls'
	_type = Call

	def add_call(self):
		pass

	def get_call(self, user):
		sql = 'SELECT * FROM {} WHERE called=? or called=?'
		self.execute(sql, (user, user))
		res = self._cursor.fetchone()
		if res:
			return self._type(res)
		return res

class CallsChecker(Checker):
	def is_free(self, ctx):
		"""вы не можете вызывать, будучи занятыми в ладдере"""
		return not bool(Calls().get_call(ctx.author.id))

	def is_correct(self, ctx):
		"""некорректный вызов"""
		caller_id = ctx.author.id
		called_id = ctx.message.mentions[0].id
		if caller_id == called_id:
			return False
		players = Players()
		caller = players.get_player(caller_id)
		called = players.get_player(called_id)
		if caller.position < called.position:
			return False
		if caller.position - 3 > called.position:
			return False
		return True