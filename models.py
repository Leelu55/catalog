from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    image = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    name = Column(String(250), nullable=False, index=True)
    id = Column(Integer, primary_key=True)
    image = Column(String, default="cat_default.jpg")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
             'name': self.name,
             'id': self.id,
             'image': self.image,
        }


class Book(Base):
    __tablename__ = 'book'

    title = Column(String, nullable=False, index=True)
    book_id = Column(Integer, primary_key=True)
    author = Column(String)
    description = Column(String)
    image = Column(String, default="default_book.jpg")
    number_of_reads = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    created_date = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
             'title': self.title,
             'author': self.author,
             'book_id': self.book_id,
             'image': self.image,
             'description': self.description,
             'number_of_reads': self.number_of_reads,
             'created_date': self.created_date
        }


engine = create_engine('sqlite:///library.db')


Base.metadata.create_all(engine)
