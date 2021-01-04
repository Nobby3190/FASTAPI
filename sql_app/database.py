from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
#
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
#connect_args={"check_same_thread": False}參數只需要在使用sqlite時加上就好
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 
#在sessionlocal class的instance(object)一但sessionlocal建立起來（使用sessionmaker），他就是一個data session
#命名為sessionlocal是為了跟sqlalchemy的session function區分開來
Base = declarative_base()
