# Платформа для публикации платного контента
Данный проект представляет собой сайт для публикации платного контента. 
Проект выполнен с использованием фреймворка Django, фронтэнд часть 
реализована на основе Django Templates.

Возможности данного сайта:
* Просмотр бесплатных публикаций даже неавторизованным пользователям
* Регистрация по номеру телефона с подтверждением через смс
* Возможность приобретать публикации
* Создание своих публикаций
* Просмотр списка публикаций в ленте
* Просмотр страницы каждого пользователя со списком его публикаций

## Установка
### На локальной машине
1. Клонируйте репозиторий с проектом себе на устройство
2. Установите зависимости командой `poetry install`
3. Переименуйте файл .env.sample в .env и заполните **все** поля в нем.
4. Примените миграции командой `python manage.py migrate`
5. Запустите сервер командой `python manage.py runserver`

### С помощью Docker
1. Клонируйте репозиторий с проектом себе на устройство
2. Переименуйте файл .env.sample в .env и заполните все поля в нем.
3. Запустите Docker
4. Соберите и запустите контейнер командой `docker-compose up -d --build`

Готово! Теперь сервис доступен по адресу http://127.0.0.1:8000/

## Использование

Для просмотра бесплатных публикаций вам не обязательно создавать аккаунт,
но вам необходимо будет это сделать, если вы захотите приобретать платные 
публикации или создавать свои.  
Создать аккаунт можно, нажав на кнопку "Зарегистрироваться" в правом верхнем 
углу. При регистрации вам нужно будет придумать уникальное имя пользователя, 
которое будет отображаться в адресной строке браузера. Также нужно указать 
ваш номер телефона: для доступа к сервису нужно будет подтвердить ввести код 
подтверждения, который придет в смс.

///Примечание для разработчиков/// Интеграция с отправкой смс выполнена через
сервис SMS Aero, так что если вы захотите использовать другой сервис, или
отключить данную функцию, то придется покопаться в коде проекта.

После регистрации вас переадресует на страницу вашего профиля. Теперь вы 
можете выкладывать свои публикации! По центру экрана находится кнопка 
"Добавить запись", нажав на которую вас перекинет на форму создания
записи. Заполните поля данными и нажмите "Создать". Готово! Ваша запись уже 
на сайте. 

Если вы захотите приобрести платную публикацию от другого пользователя,
вам нужно будет кликнуть по этой записи, после чего вас переадресует на 
страницу оплаты в сервисе Stripe. После успешной оплаты вас перекинет на 
страницу с этой записью, и в дальнейшем она всегда будет вам доступна.

На сайте так же реализована система переадресаций, которая не позволит вам 
просмотреть неоплаченную запись или оплатить еще раз уже приобретенную.

Для администрирования сайта и доступа в админ-панель вам нужно будет создать 
суперпользователя. Сделать это можно, выполнив следующую команду:

* На локальной машине `python manage.py csu`
* Через Docker `docker exec -it <id_контейнера_с_приложением_app> python manage.py csu`

