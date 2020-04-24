import datetime
import sqlalchemy
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .session import SqlAlchemyBase


class User(UserMixin, SqlAlchemyBase):
	__tablename__ = 'users'

	id = sqlalchemy.Column(
		sqlalchemy.Integer, primary_key=True, autoincrement=True)

	name = sqlalchemy.Column(sqlalchemy.String)
	surname = sqlalchemy.Column(sqlalchemy.String)

	age = sqlalchemy.Column(sqlalchemy.Integer)
	position = sqlalchemy.Column(sqlalchemy.String)
	speciality = sqlalchemy.Column(sqlalchemy.String)
	address = sqlalchemy.Column(sqlalchemy.String)

	email = sqlalchemy.Column(sqlalchemy.String, unique=True)

	password_hash = sqlalchemy.Column(sqlalchemy.String)
	modified_date = sqlalchemy.Column(
		sqlalchemy.DateTime, default=datetime.datetime.now)

	jobs = orm.relation("Jobs", back_populates='user')

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return f"<Colonist> {self.id} {self.surname} {self.name}"


def userFabric(data) -> User:
	user = User()
	return user