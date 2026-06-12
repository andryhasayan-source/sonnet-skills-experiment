# -*- coding: utf-8 -*-
"""
Общий загрузчик решений для тестов эксперимента.

Откуда берётся решение: outputs/<STAGE>/<ID>.py
Этап задаётся переменной окружения STAGE (по умолчанию baseline).

Пример запуска из корня sonnet-skills-exp:
    STAGE=baseline pytest tasks/test_P1.py -v
    STAGE=iter1    pytest tasks/test_P1.py -v
"""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_solution(task_id: str):
    """Импортирует файл решения outputs/<STAGE>/<task_id>.py как модуль."""
    stage = os.environ.get("STAGE", "baseline")
    path = os.path.join(ROOT, "outputs", stage, f"{task_id}.py")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Нет файла решения: {path}\n"
            f"Сохраните код модели в outputs/{stage}/{task_id}.py "
            f"или укажите верный STAGE."
        )
    spec = importlib.util.spec_from_file_location(f"solution_{task_id}", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
