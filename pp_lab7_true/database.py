from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin

Base = declarative_base()
metadata = Base.metadata


class Article(Base):
    __tablename__ = 'Article'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer)
    text = Column(String)
    create_date = Column(String)
    last_edit_date = Column(String)
    ready = Column(String)


class Request(Base):
    __tablename__ = 'Request'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    article_id = Column(Integer, ForeignKey("Article.id"))
    user_id = Column(Integer, ForeignKey("User.id"))
    DateTimeOfRequest = Column(String)
    status = Column(String)


class User(Base, UserMixin):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    phone = Column(String)
    role = Column(String)

    def __repr__(self):
        return "<{}:{}>".format(self.id, self.username)

    def set_password(self, password):
        self.password = password


engine = create_engine("postgres://postgres:postgres@localhost/adron")
Base.metadata.create_all(engine)

"""Session = sessionmaker(engine)
session = Session()
session.add(User(username="moderator",
                 email="email@lpnu",
                 password="b'MTQ4ODE0ODg='",
                 phone="88005553535",
                 role="moderator"))

session.commit()"""
