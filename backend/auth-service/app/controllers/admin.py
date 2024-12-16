from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from app.models.role import Role, Permission
from app.models.user import User

admin_bp = Blueprint('admin', __name__)

def require_admin():
    """Проверка наличия роли админа"""
    claims = get_jwt()
    if 'admin' not in claims.get('roles', []):
        return jsonify({"error": "Admin access required"}), 403
    return None

@admin_bp.route('/roles', methods=['GET'])
@jwt_required()
def get_roles():
    """Получение списка всех ролей"""
    error = require_admin()
    if error:
        return error
    
    roles = Role.query.all()
    return jsonify([role.to_dict() for role in roles]), 200

@admin_bp.route('/roles', methods=['POST'])
@jwt_required()
def create_role():
    """Создание новой роли"""
    error = require_admin()
    if error:
        return error

    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Role name is required"}), 400

    if Role.query.filter_by(name=data['name']).first():
        return jsonify({"error": "Role already exists"}), 409

    role = Role(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(role)
    db.session.commit()

    return jsonify(role.to_dict()), 201

@admin_bp.route('/permissions', methods=['GET'])
@jwt_required()
def get_permissions():
    """Получение списка всех прав"""
    error = require_admin()
    if error:
        return error
    
    permissions = Permission.query.all()
    return jsonify([perm.to_dict() for perm in permissions]), 200

@admin_bp.route('/permissions', methods=['POST'])
@jwt_required()
def create_permission():
    """Создание нового права"""
    error = require_admin()
    if error:
        return error

    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Permission name is required"}), 400

    if Permission.query.filter_by(name=data['name']).first():
        return jsonify({"error": "Permission already exists"}), 409

    permission = Permission(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(permission)
    db.session.commit()

    return jsonify(permission.to_dict()), 201

@admin_bp.route('/roles/<int:role_id>/permissions', methods=['PUT'])
@jwt_required()
def update_role_permissions(role_id):
    """Обновление прав для роли"""
    error = require_admin()
    if error:
        return error

    role = Role.query.get_or_404(role_id)
    data = request.get_json()
    
    if not data or 'permissions' not in data:
        return jsonify({"error": "Permissions list is required"}), 400

    permissions = Permission.query.filter(Permission.name.in_(data['permissions'])).all()
    if len(permissions) != len(data['permissions']):
        return jsonify({"error": "Some permissions do not exist"}), 400

    role.permissions = permissions
    db.session.commit()

    return jsonify(role.to_dict()), 200

@admin_bp.route('/users/<int:user_id>/roles', methods=['PUT'])
@jwt_required()
def update_user_roles(user_id):
    """Обновление ролей пользователя"""
    error = require_admin()
    if error:
        return error

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data or 'roles' not in data:
        return jsonify({"error": "Roles list is required"}), 400

    roles = Role.query.filter(Role.name.in_(data['roles'])).all()
    if len(roles) != len(data['roles']):
        return jsonify({"error": "Some roles do not exist"}), 400

    user.roles = roles
    db.session.commit()

    return jsonify(user.to_dict()), 200
