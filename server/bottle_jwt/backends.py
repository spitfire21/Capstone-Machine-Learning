# -*- coding: utf-8 -*-
"""`bottle_jwt.auth` module.

Main auth providers class implementation.
Mongo DB backend implementation and hashing of passwords utilizes this library
in conjunction woth bottle_jwt
https://github.com/FedericoCeratto/bottle-cork
"""

from __future__ import unicode_literals
from __future__ import print_function
import uuid
import abc
import six
import os
from datetime import datetime
from base64 import b64encode, b64decode
from bottle_jwt.compat import signature
import scrypt
from twilio.rest import Client
import string
import random

from logging import getLogger
log = getLogger(__name__)

__all__ = ['BaseAuthBackend', ]


@six.add_metaclass(abc.ABCMeta)
class BaseAuthBackend(object):
	"""Auth Provider Backend Interface. Defines a standard API for implementation
	in order to work with different backends (SQL, Redis, Filesystem-based, external
	API services, etc.)

	Notes:
		It is not necessary to subclass `BaseAuthBackend` in order to make `bottle-jwt` plugin to
		work, as long as you implement it's API. For example all the following examples are valid.

	Examples:
		>>> class DummyExampleBackend(object):
		...	 credentials = ('admin', 'qwerty')
		...	 user_id = 1
		...
		...	 def authenticate_user(self, username, password):
		...		 if (username, password) == self.credentials
		...			 return {'user': 'admin', 'id': 1}
		...		 return None
		...
		...	 def get_user(self, user_id):
		...		 return {'user': 'admin '} if user_id == self.user_id else None
		...
		>>> class SQLAlchemyExampleBackend(object):
		...	 def __init__(self, some_orm_model):
		...		 self.orm_model = some_orm_model
		...
		...	 def authenticate(self, user_uid, user_password):
		...		 return self.orm_model.get(email=user_uid, password=user_password) or None
		...
		...	 def get_user(self, user_uid):
		...		 return self.orm_model.get(id=user_uid) or None
		"""

	@abc.abstractmethod
	def authenticate_user(self, username, password):  # pragma: no cover
		"""User authentication method. All subclasses must implement the
		`authenticate_user` method with the following specs.

		Args:
			username (str): User identity for the backend (email/username).
			password (str): User secret password.

		Returns:
			A dict representing User record if authentication is succesful else None.

		Raises:
			`bottle_jwt.error.JWTBackendError` if any exception occurs.
		"""
		pass

	@abc.abstractmethod
	def get_user(self, user_uid):  # pragma: no cover
		"""User data retrieval method. All subclasses must implement the
		`get_user` method with the following specs.

		Args:
			user_uid (object): User identity in backend.

		Returns:
			User data (dict) if user exists or None.

		Raises:
			`bottle_jwt.error.JWTBackendError` if any exception occurs.
		"""
		pass

	@classmethod
	def __subclasshook__(cls, subclass):
		"""Useful for checking interface for backends that don't inherit from
		BaseAuthBackend.
		"""
		if cls is BaseAuthBackend:
			try:
				authenticate_user_signature = set(signature(subclass.authenticate_user).parameters)
				get_user_signature = set(signature(subclass.get_user).parameters)

				return authenticate_user_signature.issuperset({'username', 'password'}) and \
					get_user_signature.issuperset({'user_id'})

			except AttributeError:
				return False

		return NotImplemented  # pragma: no cover



	



try:
	import pymongo
	is_pymongo_2 = (pymongo.version_tuple[0] == 2)
except ImportError:  # pragma: no cover
	pass

def ni(*args, **kwargs):
	raise NotImplementedError
class Backend(object):
	"""Base Backend class - to be subclassed by real backends."""
	save_users = ni
	save_roles = ni
	save_pending_registrations = ni

class Table(object):
	"""Base Table class - to be subclassed by real backends."""
	__len__ = ni
	__contains__ = ni
	__setitem__ = ni
	__getitem__ = ni
	__iter__ = ni
	iteritems = ni


class MongoTable(Table):
	"""Abstract MongoDB Table.
	Allow dictionary-like access.
	"""
	def __init__(self, name, key_name, collection):
		self._name = name
		self._key_name = key_name
		self._coll = collection

	def create_index(self):
		"""Create collection index."""
		self._coll.create_index(
			self._key_name,
			drop_dups=True,
			unique=True,
		)

	def __len__(self):
		return self._coll.count()

	def __contains__(self, value):
		r = self._coll.find_one({self._key_name: value})
		return r is not None

	def __iter__(self):
		"""Iter on dictionary keys"""
		if is_pymongo_2:
			r = self._coll.find(fields=[self._key_name,])
		else:
			r = self._coll.find(projection=[self._key_name,])

		return (i[self._key_name] for i in r)

	def iteritems(self):
		"""Iter on dictionary items.
		:returns: generator of (key, value) tuples
		"""
		r = self._coll.find()
		for i in r:
			d = i.copy()
			d.pop(self._key_name)
			d.pop('_id')
			yield (i[self._key_name], d)

	def pop(self, key_val):
		"""Remove a dictionary item"""
		r = self[key_val]
		self._coll.remove({self._key_name: key_val}, w=1)
		return r


class MongoSingleValueTable(MongoTable):
	"""MongoDB table accessible as a simple key -> value dictionary.
	Used to store roles.
	"""
	# Values are stored in a MongoDB "column" named "val"
	def __init__(self, *args, **kw):
		super(MongoSingleValueTable, self).__init__(*args, **kw)

	def __setitem__(self, key_val, data):
		assert not isinstance(data, dict)
		spec = {self._key_name: key_val}
		data = {self._key_name: key_val, 'val': data}
		if is_pymongo_2:
			self._coll.update(spec, {'$set': data}, upsert=True, w=1)
		else:
			self._coll.update_one(spec, {'$set': data}, upsert=True)

	def __getitem__(self, key_val):
		r = self._coll.find_one({self._key_name: key_val})
		if r is None:
			raise KeyError(key_val)

		return r['val']

class MongoMutableDict(dict):
	"""Represent an item from a Table. Acts as a dictionary.
	"""
	def __init__(self, parent, root_key, d):
		"""Create a MongoMutableDict instance.
		:param parent: Table instance
		:type parent: :class:`MongoTable`
		"""
		super(MongoMutableDict, self).__init__(d)
		self._parent = parent
		self._root_key = root_key

	def __setitem__(self, k, v):
		super(MongoMutableDict, self).__setitem__(k, v)
		spec = {self._parent._key_name: self._root_key}
		if is_pymongo_2:
			r = self._parent._coll.update(spec, {'$set': {k: v}}, upsert=True)
		else:
			r = self._parent._coll.update_one(spec, {'$set': {k: v}}, upsert=True)



class MongoMultiValueTable(MongoTable):
	"""MongoDB table accessible as a dictionary.
	"""
	def __init__(self, *args, **kw):
		super(MongoMultiValueTable, self).__init__(*args, **kw)

	def __setitem__(self, key_val, data):
		assert isinstance(data, dict)
		key_name = self._key_name
		if key_name in data:
			assert data[key_name] == key_val
		else:
			data[key_name] = key_val

		spec = {key_name: key_val}
		if u'_id' in data:
			del(data[u'_id'])

		if is_pymongo_2:
			self._coll.update(spec, {'$set': data}, upsert=True, w=1)
		else:
			self._coll.update_one(spec, {'$set': data}, upsert=True)

	def __getitem__(self, key_val):
		r = self._coll.find_one({self._key_name: key_val})
		if r is None:
			raise KeyError(key_val)

		return MongoMutableDict(self, key_val, r)
class BackendIOException(Exception):
	"""Generic Backend I/O Exception"""
	pass

def ni(*args, **kwargs):
	raise NotImplementedError





class MongoDBBackend(Backend):
	def __init__(self, db_name='cork', hostname='localhost', port=27017, initialize=False, username=None, password=None):
		"""Initialize MongoDB Backend"""
		connection = pymongo.MongoClient(host=hostname, port=port)
		db = connection[db_name]
		if username and password:
			db.authenticate(username, password)
		self.users = MongoMultiValueTable('users', 'login', db.users)
		self.pending_registrations = MongoMultiValueTable(
			'pending_registrations',
			'pending_registration',
			db.pending_registrations
		)
		self.roles = MongoSingleValueTable('roles', 'role', db.roles)

		if initialize:
			self._initialize_storage()

	def _initialize_storage(self):
		"""Create MongoDB indexes."""
		for c in (self.users, self.roles, self.pending_registrations):
			c.create_index()

	def save_users(self):
		pass

	def save_roles(self):
		pass

	def save_pending_registrations(self):
		pass
		
class AuthBackend(object):

	"""Implementing an auth backend class with at least two methods.
	"""
	
	def __init__(self, db):
		self._store = MongoDBBackend(db_name=db, initialize=True)
		self.saltlength = { 'scrypt':32}
	
		
		
	def authenticate_user(self, username, password):
		"""Authenticate User by username and password.

		Returns:
			A dict representing User Record or None.
		"""
		if username in self._store.users:
			
			salted_hash = self._store.users[username]['hash']
			if hasattr(salted_hash, 'encode'):
				salted_hash = salted_hash.encode('ascii')
			authenticated = self._verify_password(
				username,
				password,
				salted_hash,
			)
			if authenticated:
				self._store.users[username]['last_login'] = str(
					datetime.utcnow())
				self._store.save_users()
				return self._store.users[username]
				
			else:
				return None
		return None
		
	
	def register(self, username, password, email_addr, phone, ssid, twilio, role='user',
				 max_level=50, subject="Signup confirmation",
				 email_template='views/registration_email.tpl',
				 description=None, **kwargs):
		"""Register a new user account. An email with a registration validation
		is sent to the user.
		WARNING: this method is available to unauthenticated users
		:param username: username
		:type username: str.
		:param password: cleartext password
		:type password: str.
		:param role: role (optional), defaults to 'user'
		:type role: str.
		:param max_level: maximum role level (optional), defaults to 50
		:type max_level: int.
		:param email_addr: email address
		:type email_addr: str.
		:param subject: email subject
		:type subject: str.
		:param email_template: email template filename
		:type email_template: str.
		:param description: description (free form)
		:type description: str.
		:raises: AssertError or AAAException on errors
		"""
		assert username, "Username must be provided."
		assert password, "A password must be provided."
		assert email_addr, "An email address must be provided."
		if username in self._store.users:
			raise UserExists("User is already existing.")
		if role not in self._store.roles:
			raise AAAException("Nonexistent role")
		if self._store.roles[role] > max_level:
			raise AAAException("Unauthorized role")
		size = 6
		self.ssid = ssid
		self.phone = phone
		self.twilio = twilio
		chars=string.ascii_uppercase + string.digits
		registration_code = ''.join(random.choice(chars) for _ in range(size))
		 
		
		creation_date = str(datetime.utcnow())
		
		self.sendText(registration_code)
		 
		"""
		
		self.mailer.send_email(email_addr, subject, email_text)

		# store pending registration
		h = self._hash(username, password)
		h = h.decode('ascii')
		self._store.pending_registrations[registration_code] = {
			'username': username,
			'role': role,
			'hash': h,
			'email_addr': email_addr,
			'desc': description,
			'creation_date': creation_date,
		}
		self._store.save_pending_registrations()
		
		
		"""
		h = self._hash_scrypt(username, password)
		h = h.decode('ascii')
		
		self._store.pending_registrations[registration_code] = {
			'username': username,
			'role': role,
			'hash': h,
			'email_addr': email_addr,
			'desc': description,
			'creation_date': creation_date,
		}
		self._store.save_pending_registrations()
		return self._store.pending_registrations[registration_code]
		
		
		
	def validate_registration(self, registration_code):
		"""Validate pending account registration, create a new account if
		successful.
		:param registration_code: registration code
		:type registration_code: str.
		"""
		try:
			data = self._store.pending_registrations.pop(registration_code)
			
		except KeyError:
			raise AuthException("Invalid registration code.")
		
		username = data['username']
		if username in self._store.users:
			raise UserExists("User is already existing.")

		# the user data is moved from pending_registrations to _users
		self._store.users[username] = {
			'role': data['role'],
			'hash': data['hash'],
			'email_addr': data['email_addr'],
			'desc': data['desc'],
			'creation_date': data['creation_date'],
			'last_login': str(datetime.utcnow())
		}
		self._store.save_users()
		return self._store.users[username]
		
	def get_user(self, user_id):
		"""Retrieve User By ID.

		Returns:
			A dict representing User Record or None.
		"""
		if user_id in self._store.users:
			
			return {k: self._store.users[k] for k in self._store.users if k != 'password'}
		return None
		
	def _verify_password(self, username, pwd, salted_hash):
		"""Verity username/password pair against a salted hash
		:returns: bool
		"""
		assert isinstance(salted_hash, type(b''))
		decoded = b64decode(salted_hash)
		hash_type = decoded[0]
		if isinstance(hash_type, int):
			hash_type = chr(hash_type)

		

		if hash_type == 's':  # scrypt
			saltend = self.saltlength['scrypt']+1
			salt = decoded[1:saltend]
			h = self._hash_scrypt(username, pwd, salt)
			return salted_hash == h

	

		raise RuntimeError("Unknown hashing algorithm in hash: %r" % decoded)
		
	def _hash_scrypt(self, username, pwd, salt=None):
		 
		"""Hash username and password, generating salt value if required
		Use scrypt.
		:returns: base-64 encoded str.
		"""
		

		if salt is None:
			salt = os.urandom(self.saltlength['scrypt'])

		assert len(salt) == self.saltlength['scrypt'], "Incorrect salt length"
		 
		username = username.encode('utf-8')
		assert isinstance(username, bytes)

		pwd = pwd.encode('utf-8')
		assert isinstance(pwd, bytes)

		cleartext = "%s\0%s" % (username, pwd)
		
		h = scrypt.hash(cleartext.encode('utf-8'), salt)
		# 's' for scrypt
		hashed = b's' + salt + h
		return b64encode(hashed)
	
	def sendText(self, code):	
		client = Client(self.ssid, self.twilio)
		try:
			message = client.messages.create(
		to="+1"+self.phone, 
		from_="+17205360930", 
		body=code)
		except Exception as inst:
			print(inst)
		
	
		
		
		
		
	
	
