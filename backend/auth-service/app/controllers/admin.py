from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app import db, logger
from app.models.role import Role, Permission
from app.models.user import User

admin_bp = Blueprint('admin', __name__)

def require_admin():
    """Проверка наличия роли админа"""
    claims = get_jwt()
    if 'admin' not in claims.get('roles', []):
        logger.warning("Unauthorized admin access attempt",
                      user_id=get_jwt_identity(),
                      action="admin_access")
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
    logger.debug("Roles list requested",
                user_id=get_jwt_identity(),
                action="get_roles")
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
        logger.warning("Role creation attempt with invalid data",
                      user_id=get_jwt_identity(),
                      action="create_role",
                      metadata={"received_fields": list(data.keys()) if data else None})
        return jsonify({"error": "Role name is required"}), 400

    if Role.query.filter_by(name=data['name']).first():
        logger.info("Role creation attempt with existing name",
                   user_id=get_jwt_identity(),
                   action="create_role",
                   metadata={"role_name": data['name']})
        return jsonify({"error": "Role already exists"}), 409

    role = Role(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(role)
    db.session.commit()

    logger.info("New role created",
                user_id=get_jwt_identity(),
                action="create_role",
                metadata={"role_name": role.name})

    return jsonify(role.to_dict()), 201

@admin_bp.route('/permissions', methods=['GET'])
@jwt_required()
def get_permissions():
    """Получение списка всех прав"""
    error = require_admin()
    if error:
        return error
    
    permissions = Permission.query.all()
    logger.debug("Permissions list requested",
                user_id=get_jwt_identity(),
                action="get_permissions")
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
        logger.warning("Permission creation attempt with invalid data",
                      user_id=get_jwt_identity(),
                      action="create_permission",
                      metadata={"received_fields": list(data.keys()) if data else None})
        return jsonify({"error": "Permission name is required"}), 400

    if Permission.query.filter_by(name=data['name']).first():
        logger.info("Permission creation attempt with existing name",
                   user_id=get_jwt_identity(),
                   action="create_permission",
                   metadata={"permission_name": data['name']})
        return jsonify({"error": "Permission already exists"}), 409

    permission = Permission(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(permission)
    db.session.commit()

    logger.info("New permission created",
                user_id=get_jwt_identity(),
                action="create_permission",
                metadata={"permission_name": permission.name})

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
        logger.warning("Role permissions update attempt with invalid data",
                      user_id=get_jwt_identity(),
                      action="update_role_permissions",
                      metadata={"role_id": role_id})
        return jsonify({"error": "Permissions list is required"}), 400

    permissions = Permission.query.filter(Permission.name.in_(data['permissions'])).all()
    if len(permissions) != len(data['permissions']):
        logger.warning("Role permissions update with non-existent permissions",
                      user_id=get_jwt_identity(),
                      action="update_role_permissions",
                      metadata={"role_id": role_id, "invalid_permissions": set(data['permissions']) - {p.name for p in permissions}})
        return jsonify({"error": "Some permissions do not exist"}), 400

    role.permissions = permissions
    db.session.commit()

    logger.info("Role permissions updated",
                user_id=get_jwt_identity(),
                action="update_role_permissions",
                metadata={"role_id": role_id, "permissions": [p.name for p in permissions]})

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
        logger.warning("User roles update attempt with invalid data",
                      user_id=get_jwt_identity(),
                      action="update_user_roles",
                      metadata={"target_user_id": user_id})
        return jsonify({"error": "Roles list is required"}), 400

    roles = Role.query.filter(Role.name.in_(data['roles'])).all()
    if len(roles) != len(data['roles']):
        logger.warning("User roles update with non-existent roles",
                      user_id=get_jwt_identity(),
                      action="update_user_roles",
                      metadata={"target_user_id": user_id, "invalid_roles": set(data['roles']) - {r.name for r in roles}})
        return jsonify({"error": "Some roles do not exist"}), 400

    user.roles = roles
    db.session.commit()

    logger.info("User roles updated",
                user_id=get_jwt_identity(),
                action="update_user_roles",
                metadata={"target_user_id": user_id, "roles": [r.name for r in roles]})
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "roles": [role.name for role in user.roles]
    }), 200
