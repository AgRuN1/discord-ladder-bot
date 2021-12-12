import sqlite3
from abc import ABCMeta, abstractmethod
from threading import Lock

from discord.ext.commands import CheckFailure

class Database(metaclass=ABCMeta):
	@property
	@abstractmethod
	def _table(self):
		pass

	@property
	@abstractmethod
	def _type(self):
		pass

	__lock = Lock()

	def __init__(self):
		Database.__lock.acquire()
		self.__connection = sqlite3.connect('database.db')
		self._cursor = self.__connection.cursor()

	def save(self):
		self.__connection.commit()

	def __del__(self):
		self.__connection.close()
		Database.__lock.release()

	def execute(self, sql, params=0):
		sql = sql.format(self._table)
		if params:
			self._cursor.execute(sql, params)
		else:
			self._cursor.execute(sql)

	def count(self):
		sql = 'SELECT COUNT(*) FROM {}'
		self.execute(sql)
		return self._cursor.fetchone()[0]

	def get_list(self):
		sql = 'SELECT * FROM {} ORDER BY position'
		self.execute(sql)
		for row in self._cursor.fetchall():
			yield self._type(row)

class Checker:
	def __init__(self, checkers):
		self.__checkers = checkers

	def __call__(self, func):
		async def wrapper(ctx, *args, **kwargs):
			for checker_name in self.__checkers:
				checker_method = getattr(self, checker_name)
				if not checker_method(ctx):
					raise CheckFailure(checker_method.__doc__)
			await func(ctx, *args, **kwargs)

		return wrapper