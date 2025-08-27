from sqlalchemy import Column, Integer, String
from .base import Base
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from config.environment import secret
from sqlalchemy.orm import relationship

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=True)

    teas = relationship('TeaModel', back_populates='user')

    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self):
        payload = {
            "exp": datetime.now(timezone.utc) + timedelta(days=1),
            "iat": datetime.now(timezone.utc),
            "sub": self.id,
        }

        token = jwt.encode(payload, secret, algorithm="HS256")

        return token