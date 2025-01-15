from app import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Table, ForeignKey, Date, JSON
from sqlalchemy.sql import func
import bcrypt

# Таблица связи пользователей и ролей
user_roles = Table(
    'user_roles',
    db.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(db.Model):
    """Модель пользователя"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)  # Убрали unique=True
    email = Column(String(255), unique=True, nullable=False)
    email_verified = Column(Boolean, default=False, nullable=False)
    password_hash = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login_at = Column(DateTime(timezone=True))
    full_name = Column(String(255))
    phone_number = Column(String(15))
    gender = Column(String(10))
    birth_date = Column(Date)
    provider = Column(String(50))
    provider_user_id = Column(String(255))
    provider_data = Column(JSON)

    # Отношение к ролям
    roles = relationship('Role', secondary=user_roles, lazy='joined',
                        backref=db.backref('users', lazy=True))

    def set_password(self, password):
        """Хеширование пароля"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')

    def check_password(self, password):
        """Проверка пароля"""
        if not self.password_hash:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        """Сериализация пользователя"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login_at': self.last_login_at.isoformat() if self.last_login_at else None,
            'full_name': self.full_name,
            'phone_number': self.phone_number,
            'gender': self.gender,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'provider': self.provider,
            'roles': [role.name for role in self.roles]
        }

    def get_roles(self):
        """Получение списка ролей для JWT токена"""
        return [role.name for role in self.roles]
