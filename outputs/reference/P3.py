import json
import os

def load_config(path):
    if not os.path.exists(path):
        raise ValueError(f"Файл не найден: {path}")
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Битый JSON: {e}")

def _check_port(value, name, errors):
    if not isinstance(value, int) or isinstance(value, bool):
        errors.append(f"{name}: должен быть int")
    elif not (1 <= value <= 65535):
        errors.append(f"{name}: вне диапазона 1-65535")

def validate_config(config):
    errors = []
    if not isinstance(config, dict):
        return ["конфиг должен быть объектом"]

    app = config.get("app_name")
    if not isinstance(app, str) or not app.strip():
        errors.append("app_name: непустая строка обязательна")

    if "port" not in config:
        errors.append("port: отсутствует")
    else:
        _check_port(config["port"], "port", errors)

    if not isinstance(config.get("debug"), bool):
        errors.append("debug: должен быть bool")

    db = config.get("database")
    if not isinstance(db, dict):
        errors.append("database: отсутствует или не объект")
    else:
        host = db.get("host")
        if not isinstance(host, str) or not host.strip():
            errors.append("database.host: непустая строка обязательна")
        if "port" not in db:
            errors.append("database.port: отсутствует")
        else:
            _check_port(db["port"], "database.port", errors)

    admins = config.get("admins")
    if not isinstance(admins, list) or len(admins) < 1:
        errors.append("admins: список минимум из 1 email")
    else:
        for i, a in enumerate(admins):
            if not isinstance(a, str) or "@" not in a or "." not in a:
                errors.append(f"admins[{i}]: не похоже на email")
    return errors
