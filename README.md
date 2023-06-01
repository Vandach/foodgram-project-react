![This is an image](https://github.com/Vandach/foodgram-project-react/actions/workflows/main.yml/badge.svg) 

### Проект Foodgram: 

 

Проект Foodgram позволяет пользователям добавлять рецепты. Подписываться на других пользователей и добавлять их рецепты в избанные. Также есть возможность скачивания списка необходимых ингредиентов для приготовления рецептов добавленных в корзину. 

 



### Как запустить проект: 

 

Откройте командную строку. 

 

Клонируйте репозиторий: 

 

``` 

git clone git@github.com:Vandach/foodgram-project-react.git 

``` 

 

Перейдите в проект: 

 

``` 

cd foodgram-project-react 

``` 

 

Перейдите в папку с файлои docker-compose: 

 

``` 

cd infra 

``` 

 

 

Запустите контейнеры: 

 

``` 

docker-compose up -d --build 

``` 

 

 

Выполнить миграции: 

 

``` 

docker-compose exec backend python manage.py makemigrations 

 

docker-compose exec backend python manage.py migrate 

``` 

 

Создайте супер пользователя: 

 

``` 

docker-compose exec backend python manage.py createsuperuser 

``` 

 

Собираем статику: 

 

``` 

docker-compose exec backend python manage.py collectstatic --no-input 

``` 

 

Войти в проект можно перейдя на страницу http://localhost/admin/ 

 

 

### Примеры запросов: 

 

Вывод регистация на сайте: 

``` 

http://localhost/signup/ 

``` 

 

Вывод рецептов: 

``` 

http://localhost/recipes/ 

``` 

 

Подписки пользователя: 

``` 

http://localhost/subscriptions/ 

``` 

 

Создание рецепта: 

``` 

http://localhost/recipes/create/ 

``` 

 

Избранные рецепты пользователя: 

``` 

http://localhost/favorites/ 

``` 

 

Список покупок пользователя: 

``` 

http://localhost/cart/ 

``` 

 

### Автор: 

 

Студент Яндекс Практикум  

 

Кирилл Аль-Шаер 

