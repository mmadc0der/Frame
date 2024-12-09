from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from passlib.hash import bcrypt

class User(db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    def set_password(self, password):
        """Хеширование пароля"""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password):
        """Проверка пароля"""
        return bcrypt.verify(password, self.password_hash)

    def to_dict(self):
        """Сериализация пользователя"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
