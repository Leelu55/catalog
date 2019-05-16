from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
  __tablename__ = 'user'

  name = Column(String(250), nullable = False)
  id = Column(Integer, primary_key = True)
  email = Column(String(250), nullable = False)
  image = Column(String(250))


class Category(Base):
  __tablename__ = 'category'

  name = Column(String(250), nullable = False, index = True)
  id = Column(Integer, primary_key = True)
  image = Column(String)


class Book(Base):
  __tablename__ = 'book'

  title = Column(String, nullable = False, index = True)
  id = Column(Integer, primary_key = True)
  author = Column(String)
  description = Column(String)
  location = Column(String(250), nullable = False)
  image = Column(String)
  number_of_reads = Column(Integer, default = 0)
  category_id =  Column(Integer, ForeignKey('category.id'))
  category = relationship(Category)
  user_id = Column(Integer, ForeignKey('user.id'))
  user = relationship(User)


  @property
  def serialize(self):
    """Return object data in easily serializeable format"""
    return {
       'title'         : self.title,
       'author'         : self.author,
       'id'         : self.id,
       'image'         : self.image,
       'description'  : self.description,
       'number_of_reads'  : self.number_of_reads,
       'location' : self.location
    }


engine = create_engine('sqlite:///library.db')


Base.metadata.create_all(engine)