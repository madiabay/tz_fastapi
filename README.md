# Test Task

## Запуск проекта

0. GIT CLONE

1. Установите зависимости:
```bash
pip install -r req.txt
```

2. Применить миграции:
```bash
alembic upgrade head
```

3. Запуск проекта:
```bash
python run.py
```

4. Можно тестить все ендпойнты через адрес:
```bash
http://127.0.0.1:8000/docs
```
