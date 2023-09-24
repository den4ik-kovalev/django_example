## Техническое задание
См. файл Тестовое задание Сервер.pdf
Реализованы все требования. В текущей реализации каждые 30 секунд страница с событиями обновляется полностью.

## Программные требования
Точно работает на python 3.10
Необходим доступ к базе данных на MySQL Server

## API Endpoints
Доступные методы API (названия говорят сами за себя):
- api/auth/login (POST)
- api/auth/logout (POST)
- api/CreateUser (POST)
- api/CreateEvent (POST)
- api/GetEventList (GET)
- api/AddParticipant (POST)
- api/RemoveParticipant (POST)
- api/DeleteEvent (POST)

## Тестовый сервер
Приложение доступно по адресу http://den4ikkovalev.pythonanywhere.com/
Заходите, регистрируйтесь и пробуйте. Добро пожаловать.
Если не работает, пишите в телеграм - @den4ik_kovalev
