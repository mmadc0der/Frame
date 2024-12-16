from app import db
from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

# Таблица связи ролей и прав
role_permissions = Table(
    'role_permissions',
    db.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Permission(db.Model):
    """Модель прав доступа"""
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    def to_dict(self):
        """Сериализация прав"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

class Role(db.Model):
    """Модель роли пользователя"""
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)

    # Отношение к правам
    permissions = relationship('Permission', secondary=role_permissions, lazy='joined',
                             backref=db.backref('roles', lazy=True))

    def to_dict(self):
        """Сериализация роли"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'permissions': [perm.name for perm in self.permissions]
        }
