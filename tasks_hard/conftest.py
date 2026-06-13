# -*- coding: utf-8 -*-
import importlib.util, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_solution(task_id):
    stage = os.environ.get("STAGE", "reference_hard")
    path = os.path.join(ROOT, "outputs", stage, f"{task_id}.py")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Нет решения: {path}")
    spec = importlib.util.spec_from_file_location(f"sol_{task_id}_{stage}", path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m
