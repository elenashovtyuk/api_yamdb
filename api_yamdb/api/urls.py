from django.urls import include, path
# т.к нам нужно получить коллекцию ссылок на все ресурсы API, то
# нам понадобится стандартный роутер DefaultRouter
# он в отличие от второго базового класса SimpleRouter
# генерирует корневой эндпоинт /,
# GET-запрос к которому вернёт список ссылок на все ресурсы, доcтупные в API.
from rest_framework.routers import DefaultRouter
# Далее импортируем все вьюсеты из приложения api
from .views import CategoryViewSet, GenreViewSet, TitleViewSet
# для всех вьюсетов нужно создать свой роутер
# с помощью роутеров для заданных вьюсетов создаются эндпоинты по маске адреса

# 1. Импортируем класс DefaultRouter.
# Создаем роутер (экземпляр класса DefaultRouter
router = DefaultRouter()

# 2. Для того, чтобы роутер сгенерировал нужный набор эндпоинтов
#  для наших вьюсетов, нужно вызвать метод register
# (зарегистрировать наши эндпоинты).
# для этого вызываем метод register
# и в параметрах передаем префикс и нужный вьюсет
router.register(r'titles',
                TitleViewSet,
                basename='titles')

router.register(r'categories',
                CategoryViewSet,
                basename='categories')

router.register(r'genres',
                GenreViewSet,
                basename='genres')

# после того, как мы зарегистрировали эндпоинты для наших вьюсетов
# нужно добавить их в urlpatterns
urlpatterns = [
    path('v1/', include(router.urls)),
]
