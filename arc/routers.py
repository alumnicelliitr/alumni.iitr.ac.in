class DBRouter(object):
	def db_for_read(self, model, **hints):
		"""
		Attempts to read auth models go to 'auth_db'.
		"""
		if model._meta.app_label == 'channeli':
			return 'channeli'
		return 'default'

	def db_for_write(self, model, **hints):
		"""
		Attempts to write auth models go to 'auth_db'.
		"""
		if model._meta.app_label == 'channeli':
			return 'channeli'
		return 'default'

	def allow_relation(self, obj1, obj2, **hints):
		"""
		Allow relations if a model in the auth app is involved.
		"""
		if obj1._meta.app_label == 'channeli' or \
		   obj2._meta.app_label == 'channeli':
			return True
		return 'default'

	def allow_migrate(self, db, app_label, model_name=None, **hints):
		"""
		Make sure the auth app only appears in the 'auth_db'
		database.
		"""
		if app_label == 'channeli':
			return db == 'channeli'
		return 'default'