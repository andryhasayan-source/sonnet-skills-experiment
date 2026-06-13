"""Модуль валидации конфигурационного файла JSON."""

import json


def load_config(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise ValueError(f"Файл конфигурации не найден: {path}")
    except OSError as e:
        raise ValueError(f"Не удалось прочитать файл {path}: {e}")

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Файл {path} содержит некорректный JSON: {e}")


def validate_config(config: dict) -> list[str]:
    errors = []

    if not isinstance(config, dict):
        return ["Конфигурация должна быть JSON-объектом (словарём)"]

    # app_name
    if "app_name" not in config:
        errors.append("Отсутствует обязательное поле 'app_name'")
    else:
        app_name = config["app_name"]
        if not isinstance(app_name, str):
            errors.append("Поле 'app_name' должно быть строкой")
        elif len(app_name) == 0:
            errors.append("Поле 'app_name' не должно быть пустым")

    # port
    if "port" not in config:
        errors.append("Отсутствует обязательное поле 'port'")
    else:
        port = config["port"]
        if not isinstance(port, int) or isinstance(port, bool):
            errors.append("Поле 'port' должно быть целым числом")
        elif not (1 <= port <= 65535):
            errors.append("Поле 'port' должно быть в диапазоне от 1 до 65535")

    # debug
    if "debug" not in config:
        errors.append("Отсутствует обязательное поле 'debug'")
    else:
        if not isinstance(config["debug"], bool):
            errors.append("Поле 'debug' должно быть булевым значением (true/false)")

    # database
    if "database" not in config:
        errors.append("Отсутствует обязательное поле 'database'")
    else:
        database = config["database"]
        if not isinstance(database, dict):
            errors.append("Поле 'database' должно быть объектом")
        else:
            # database.host
            if "host" not in database:
                errors.append("Отсутствует обязательное поле 'database.host'")
            else:
                host = database["host"]
                if not isinstance(host, str):
                    errors.append("Поле 'database.host' должно быть строкой")
                elif len(host) == 0:
                    errors.append("Поле 'database.host' не должно быть пустым")

            # database.port
            if "port" not in database:
                errors.append("Отсутствует обязательное поле 'database.port'")
            else:
                db_port = database["port"]
                if not isinstance(db_port, int) or isinstance(db_port, bool):
                    errors.append("Поле 'database.port' должно быть целым числом")
                elif not (1 <= db_port <= 65535):
                    errors.append("Поле 'database.port' должно быть в диапазоне от 1 до 65535")

    # admins
    if "admins" not in config:
        errors.append("Отсутствует обязательное поле 'admins'")
    else:
        admins = config["admins"]
        if not isinstance(admins, list):
            errors.append("Поле 'admins' должно быть списком")
        elif len(admins) == 0:
            errors.append("Поле 'admins' должно содержать хотя бы один email")
        else:
            for i, email in enumerate(admins):
                if not isinstance(email, str):
                    errors.append(f"Элемент 'admins[{i}]' должен быть строкой")
                    continue
                if "@" not in email or "." not in email:
                    errors.append(
                        f"Элемент 'admins[{i}]' ('{email}') не является корректным email "
                        f"(должен содержать '@' и '.')"
                    )

    return errors