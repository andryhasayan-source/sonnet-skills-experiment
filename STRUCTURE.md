# Структура репозитория

```
sonnet-skills-exp/
├── README.md              Итоговый отчёт эксперимента
├── CRITERION.txt          Предрегистрация критерия успеха (до старта)
├── results.csv            Сырые данные всех прогонов
├── EXPERIMENT_LOG.md      Хронологический протокол
│
├── tasks/                 ЛЁГКИЙ банк (16 задач, 95 тестов)
│   ├── P1..P8_task.txt     — условия Python-задач
│   ├── B1..B8_task.txt     — условия бот-задач
│   ├── test_*.py           — автотесты
│   └── conftest.py
│
├── tasks_hard/            ТРУДНЫЙ банк (16 задач, 127 тестов)
│   ├── P1..P8_task.txt
│   ├── B1..B8_task.txt
│   ├── test_*.py
│   ├── conftest.py, _bot_helpers.py
│   └── TASKS_OVERVIEW.md
│
├── skills/
│   └── v1/self_check.md   Тестируемый скил самопроверки
│
├── outputs/               Ответы модели по этапам
│   ├── reference/          — эталоны (лёгкий банк)
│   ├── reference_hard/     — эталоны (трудный банк)
│   ├── baseline/           — Sonnet без скила, лёгкие
│   ├── baseline_hard/      — Sonnet без скила, трудные (+ P4_run1..3)
│   └── iter1_hard/         — Sonnet со скилом (+ *_report.txt — JSON-самопроверки)
│
└── report/
    └── fig1_passrate.png  График результатов
```

## Расшифровка колонок results.csv
task_id, difficulty(easy/mid/hard), domain(python/bot),
split(dev/holdout), stage(этап), skill_version(none/v1),
tests_passed, tests_total, pass(yes/no), notes.

## Этапы (stage)
- baseline        — лёгкий банк, без скила
- baseline_hard   — трудный банк, без скила
- iter1_hard      — трудный банк, со скилом self_check v1
- baseline_rerun  — повторные прогоны P4 без скила (контроль)
