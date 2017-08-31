from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserAccount(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer,)