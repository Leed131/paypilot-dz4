# Наступні кроки — ДЗ_4

Пакет є підготовкою. Модельні результати нового набору ще не отримані.

## 1. Окремі локальні коміти ДО запусків

У терміналі папки paypilot-dz4:

```bash
git init -b main
git add .gitignore l05_dialogs.jsonl multi-turn-test-plan.md evidence reports traces scripts NEXT-STEPS.md
git commit -m "Prepare HW4 dialogue cases and preserve laboratory evidence"
git add README.md
git commit -m "Record HW4 forecast before model runs"
git log -1 --format=%H
```

Не змінюйте прогноз після прогонів. SHA другого коміту потім внесемо у результати.
Якщо Git просить ім’я та email, задайте власні для цього репозиторію.

## 2. Підготувати виконання

```bash
cp -n l05_dialogs.jsonl ../l05/sets/l05_dialogs.jsonl
cd ../l05
STAND_DIR=../paypilot-stand-shared docker compose run --rm eval --set l05_dialogs --gate release --dry-run
```

Хеш повинен збігтися з README. Якщо loader відхиляє invariant/probe_turns,
спочатку перевіряємо версію кіту; не запускаємо модель із невалідним набором.

## 3. Запуски

Команди є в README. Спочатку clean з --traces; після завершення зберегти JSON.
Потім lesson-05 з --traces. П’ять повторів задано всередині кожного кейса.
Без глобального summarize-after: H04 має поріг 20, решта 2.

## 4. Завершення

Додати нові сирі reports/*.json та traces до цього репозиторію. Заповнити фактичні
частки FAIL, результати 5/10 кроків, розбіжність із прогнозом і остаточну рекомендацію.
Створити окремий публічний GitHub-репозиторій paypilot-dz4 та запушити main.
Через доступні підключені інструменти створення нового репозиторію недоступне;
це можна зробити на https://github.com/new . Старі репозиторії ДЗ не змінюємо.
