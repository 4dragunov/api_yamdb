# api_yamdb
### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».

### Как развернуть проект
- git clone https://github.com/4dragunov/praktikum_REST_API.git
- python -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver
### Алгоритм регистрации пользователей
- Пользователь отправляет запрос с параметром email на /auth/email/.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email .
- Пользователь отправляет запрос с параметрами email и confirmation_code на /auth/token/, в ответе на запрос ему приходит token (JWT-токен).
- При желании пользователь отправляет PATCH-запрос на /users/me/ и заполняет поля в своём профайле (описание полей — в документации).

### Пользовательские роли
- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
- Модератор — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
- Администратор — полные права на управление проектом и всем его содержимым. Может создавать и удалять категории и произведения. Может назначать роли пользователям.
- Администратор Django — те же права, что и у роли Администратор.

### Authentication
Security Scheme Type	API Key
Header parameter name:	Bearer
### Ресурсы API YaMDb
 - Ресурс AUTH: аутентификация.
- Ресурс USERS: пользователи.
- Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Связанные данные и каскадное удаление
- При удалении объекта пользователя User должны удаляться все отзывы и комментарии этого пользователя (вместе с оценками-рейтингами).
- При удалении объекта произведения Title должны удаляться все отзывы к этому произведению и комментарии к ним.
- При удалении объекта категории Category не удалять связанные с этой категорией произведения (Title).
- При удалении объекта жанра Genre не удалять связанные с этим жанром произведения (Title).
- При удалении объекта отзыва Review должны быть удалены все комментарии к этому отзыву.

### Модели
#### AUTH - Аутентификация
- GET Получение JWT-токена в обмен на email и confirmation code
  - - /api/v1/auth/token/
- POST Отправление confirmation_code на переданный email.
  - - /api/v1/auth/email/
#### USERS - Пользователи
- GET Получить список всех пользователей.
  - - /api/v1/users/
  - - Права доступа: Администратор
- POST Создание пользователя.
  - - /api/v1/auth/email/
  - - Права доступа: Администратор
- GET Получить пользователя по username.
  - - /api/v1/users/{username}/
  - - Права доступа: Администратор
- PATCH Изменить данные пользователя по username.
  - - /api/v1/users/{username}/
  - - Права доступа: Администратор
- DEL Удалить пользователя по username. 
  - - /api/v1/users/{username}/
  - - Права доступа: Администратор
- GET Получить данные своей учетной записи.
  - - /api/v1/users/me/
  - - Права доступа: Любой авторизованный пользователь
- PATCH Изменить данные своей учетной записи.
  - - /api/v1/users/me/
  - - Права доступа: Любой авторизованный пользователь
#### REVIEWS - Отзывы
- GET Получить список всех отзывов. 
  - - /api/v1/titles/{title_id}/reviews/
  - - Права доступа: Доступно без токена.
- POST Создать новый отзыв.
  - - /api/v1/titles/{title_id}/reviews/
  - - Права доступа: Аутентифицированные пользователи.
- GET Получить отзыв по id.
  - - /api/v1/titles/{title_id}/reviews/{review_id}/
  - - Права доступа: Доступно без токена.
- PATCH Частично обновить отзыв по id.
  - - /api/v1/titles/{title_id}/reviews/{review_id}/
  - - Права доступа: Автор отзыва, модератор или администратор.
- DEL Удалить отзыв по id.
  - - /api/v1/titles/{title_id}/reviews/{review_id}/
  - - Права доступа: Автор отзыва, модератор или администратор.

#### COMMENTS - Комментарии к отзывам
 - GET Получить список всех комментариев к отзыву по id.
   - - /api/v1/titles/{title_id}/reviews/{review_id}/comments/
   - - Права доступа: Доступно без токена.
 - POST Создать новый комментарий для отзыва.
   - - /api/v1/titles/{title_id}/reviews/{review_id}/comments/
   - - Права доступа: Аутентифицированные пользователи.
 - GET Получить комментарий для отзыва по id.
   - - /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
   - - Права доступа: Доступно без токена.
 - PATCH Частично обновить комментарий к отзыву по id.
   - - /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
   - - Права доступа: Автор комментария, модератор или администратор.
 - DEL Удалить комментарий к отзыву по id.
   - - /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
   - - Права доступа: Автор комментария, модератор или администратор.
#### CATEGORIES - Категории (типы) произведений
  - GET Получить список всех категорий.
    - - /api/v1/categories/
    - - Права доступа: Доступно без токена
  - POST Создать категорию.
    - - /api/v1/categories/
    - - Права доступа: Администратор.
  - DEL Удалить категорию. 
    - - /api/v1/categories/{slug}/
    - - Права доступа: Администратор.
 #### GENRES - Категории жанров
  - GET Получить список всех жанров.
    - - /api/v1/genres/
    - - Права доступа: Доступно без токена
  - POST Создать жанр. 
    - - /api/v1/genres/
    - - Права доступа: Администратор.
  - DEL Удалить жанр.
    - - /api/v1/genres/{slug}/
    - - Права доступа: Администратор.
 #### TITLES - Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
  - GET Получить список всех объектов.
    - - /api/v1/titles/
    - - Права доступа: Доступно без токена
  - POST Создать произведение для отзывов.
    - - /api/v1/titles/
    - - Права доступа: Администратор.
  - GET Информация об объекте.
    - - /api/v1/titles/{titles_id}/
    - - Права доступа: Доступно без токена.
  - PATCH Обновить информацию об объекте.
    - - /api/v1/titles/{titles_id}/
    - - Права доступа: Администратор
  - DEL Удалить произведение. 
    - - /api/v1/titles/{titles_id}/
    - - Права доступа: Администратор.
