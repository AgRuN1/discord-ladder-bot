import pickle

class Settings(object):
	__datafile = 'settings'
	__instance = None

	def __new__(cls):
		if not isinstance(cls.__instance, cls):
			cls.__instance = object.__new__(cls)
			with open(cls.__datafile, 'rb') as f:
				 cls.__instance.__data = pickle.load(f)

		return cls.__instance

	def __save(self):
		with open(self.__datafile, 'wb') as f:
			pickle.dump(self.__data, f)

	def get(self, key):
		return self.__data[key]

	def set(self, key, value):
		self.__data[key] = value
		self.__save()

	def exists(self, key, value):
		return value in self.__data[key]

	def add(self, key, value):
		self.__data[key].append(value)
		self.__save()

	def remove(self, key, value):
		self.__data[key].remove(value)
		self.__save()