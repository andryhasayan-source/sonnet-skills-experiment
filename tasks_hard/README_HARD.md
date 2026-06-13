# Трудный набор — как запускать

Структура (рядом со старым tasks/ и outputs/):
  tasks_hard/            <- задачи, тесты, conftest.py, _bot_helpers.py
  outputs/reference_hard/  <- эталоны (проверка валидности тестов)

Создай пустые папки под прогоны:
  outputs/baseline_hard, outputs/iter1_hard, outputs/iter2_hard,
  outputs/holdout_base_hard, outputs/holdout_skilled_hard

## Проверка валидности (один раз):
  STAGE=reference_hard python -m pytest tasks_hard/ -v
Ожидается: 127 passed.

## Прогон задачи (пример P1, baseline):
1. Новый чат, проект EXP-Baseline, модель Sonnet 4.6
2. Вставить tasks_hard/P1_task.txt дословно
3. Код -> outputs/baseline_hard/P1.py
4. STAGE=baseline_hard python -m pytest tasks_hard/test_P1.py -v
5. Строка в results.csv (этап baseline_hard)

holdout (P6-P8, B6-B8) в baseline прогоняем (нужен их старт),
но НЕ показываем Fable и не трогаем в итерациях.
