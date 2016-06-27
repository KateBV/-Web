from sqlalchemy import Table, Column, Integer, Text, create_engine, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, backref, relationship

engine = create_engine('sqlite:///kpost.db')
Session = sessionmaker()
Base = declarative_base(bind=engine)

association_table = Table('association', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    fullname = Column(String, nullable = True)
    info = Column(Text, nullable = True)    

    def __repr__(self):
        return self.name + " " + self.password + " " + str(self.access)

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    image = Column(String)
    name = Column(String)
    text = Column(Text)
    info = Column(Text, nullable = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref = backref('posts', lazy='dynamic'))
    tags = relationship("Tag", secondary=association_table, back_populates="posts")

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    posts = relationship("Post", secondary=association_table, back_populates="tags")
    typetag_id = Column(Integer, ForeignKey('typetags.id'))
    typetag = relationship("TypeTag", backref = backref('tags', lazy='dynamic'))

class TypeTag(Base):
    __tablename__ = 'typetags'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    name = Column(String)
