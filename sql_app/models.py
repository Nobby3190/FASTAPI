#we will have the file models.py with the SQLAlchemy models
# db的欄位設定、foreignkey跟primarykey、關聯、tablename都在models.py設定

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base #database.py Base class

class User(Base): #define table's name column row
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item",back_populates="owner") #關聯到Item model定義的items table，sqlalchemy會去抓取items的值

class Item(Base):
    __tablename__ = "itemss"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")#關聯到User model定義的users table並指向抓取含有users table Foreign key的欄位的值