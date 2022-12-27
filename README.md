# Проект YaMDb

## Описание
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).
Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка.
Новые жанры может создавать только администратор.
Пользователи оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг, 
а также пишут комментарии (Comments) к отзывам.

## Используемые технологии

 - Django Rest Framework (библиотека для преобразования Django-приложения в REST API)
 - Postman (графическая программа для тестирования API)

## Ресурсы API YaMDb
**AUTH**: аутентификация.

**USERS**: пользователи.

**TITLES**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).

**CATEGORIES**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").

**GENRES**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.

**REVIEWS**: отзывы на произведения. Отзыв привязан к определённому произведению.

**COMMENTS**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

## Пользовательские роли
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Суперюзер Django** — должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

# Установка

## Клонируем проект

Клонировать репозиторий и перейти в него в командной строке:

git clone git@github.com:elenashovtyuk/api_yamdb.git

```
cd api_yamdb
```

## Разворачиваем проект и окружение

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

 ## Установим зависимости

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

 ## Выполним миграции

```
python3 manage.py migrate
```

 ## Запускаем проект

```
python3 manage.py runserver
```

# Примеры запросов к API

Для доступа к API необходимо зарегистрироваться (получить код подтверждения):

1. Для этого нужно выполнить POST-запрос по указанному эндпоинту с использованием "username" и "email":

```
{
"email": "user@example.com",
"username": "user"
}
```

```
http://127.0.0.1:8000/api/v1/auth/signup/
```
В ответ YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.

2. Отправить POST-запрос по указанному эндпоинту с параметрами "username" и "confirmation_code":

```
{
"username": "user",
"confirmation_code": "string"
}
```

```
http://127.0.0:8000/api/v1/auth/token/
```
В ответ пользователь получает токен (JWT-токен):

```
{
"token": "string"
}
```

3. При желании пользователь может отправить POST-запрос на следующий эндпоинт, заполняет поля в своем профиле:

```
http://127.0.0:8000/api/v1/users/me/
```


Дальше пользователь может работать с API, отправляя этот токен с каждым запросом.
Возможные ресурсы API:

```
/api/v1/categories/ (GET, POST)

/api/v1/categories/{slug}/ (DELETE)

/api/v1/genres/ (GET, POST)

/api/v1/genres/{slug}/ (DELETE)

/api/v1/titles/ (GET, POST)

/api/v1/titles/{titles_id}/ (GET, PATCH, DELETE)

/api/v1/titles/{title_id}/reviews/ (GET, POST)

/api/v1/titles/{title_id}/reviews/{review_id}/ (GET, PATCH, DELETE)

/api/v1/titles/{title_id}/reviews/{review_id}/comments/ (GET, POST)

/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ (GET, PATCH, DELETE)

/api/v1/users/ (GET, POST)

/api/v1/{username}/ (GET, PATCH, DELETE)

/api/v1/users/me/ (GET, PATCH)
```


# Авторы проекта
Шовтюк Елена, Михайлова Мария, Пиголкин Андрей
