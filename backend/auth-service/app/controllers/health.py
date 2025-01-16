from flask import Blueprint, jsonify
from datetime import datetime
from sqlalchemy import text
from app import db, redis_client, logger

health_bp = Blueprint('health', __name__, url_prefix='/auth')

@health_bp.route('/health', methods=['GET'])
def health_check():
    status = "ok"
    checks = {
        "database": "ok",
        "redis": "ok",
        "timestamp": datetime.utcnow().isoformat(),
    }
    
    # Проверка базы данных
    try:
        db.session.execute(text('SELECT 1'))
        db.session.commit()
    except Exception as e:
        checks["database"] = str(e)
        status = "error"
    
    # Проверка Redis
    try:
        redis_client.ping()
    except Exception as e:
        checks["redis"] = str(e)
        status = "error"
    
    response = {
        "status": status,
        "service": "auth-service",
        "checks": checks
    }
    
    # Логируем результат проверки
    logger.info(
        "Health check performed",
        extra={
            "service": "auth-service",
            "status": status,
            "checks": checks
        }
    )
    
    return jsonify(response), 200 if status == "ok" else 503

@health_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "auth-service"
    }), 200
