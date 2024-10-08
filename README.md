# MVP макет для системы мониторинга ЧПУ на основе PyQt

Это приложение представляет собой макет системы мониторинга для станка ЧПУ. Оно включает в себя визуализацию данных по температуре двигателей, состоянию осей и сообщениям системы.

## Основные функции

1. **Визуализация температуры двигателей:**
   - Отображение текущей температуры каждого двигателя.
   - Расчет и отображение средней температуры.

2. **Статус осей:**
   - Показ состояния каждой оси станка.
   - Отображение времени последнего изменения состояния.

3. **Отслеживание сообщений:**
   - Отображение различных сообщений системы, таких как ошибки и предупреждения.
   - Возможность фильтрации сообщений по важности и дате.

## Требования к установке

- Python 3.x
- Установленные зависимости из `requirements.txt`


## Установка зависимостей
Перед установкой зависимостей рекомендуется создать виртуальное окружение:

```bash
python -m venv venv
```
Активируйте виртуальное окружение:

На Windows:
```bash
venv\Scripts\activate
```
На Linux или MacOS:
```bash
source venv/bin/activate
```
Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск проекта
Запуск проекта через терминал:

```bash
python PyQt_monitoring_system.py
```