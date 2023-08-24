import pickle

from fastapi import Depends

from app.config import EXPIRATION
from app.db.database_connect import get_redis
from app.db.repositories.submenu_repository import AsyncSubmenuRepository


class CacheRepository:
    """
    Сервисный слой для кеширования запросов
    ПРОПИСАТЬ ТРЕБОВАНИЯ И СХЕМУ РАБОТЫ КЕША:
    Необходимо написать функции для:
    1. Записи меню, подменю и блюд в кеш
    2. Получения всех меню, подменю и блюд из кеша
    3. Записи определенного меню, подменю и блюда по id в кеш
    4. Инвалидации кеша при удалении меню, подменю и блюда
    4.1. Если удаляется блюдо, то инвалидируется кеш только данного блюда по id
    4.2. Если удаляется подменю, то инвалидируется кеш данного подменю и всех блюд
            внутри данного блюда
    4.3. Если удаляется меню, то инвалидируется кеш данного меню, всех подменю и
            блюд внутри данного меню
    5. Если добавляется новое меню, то кеш по получению всех меню должен обновиться
    6. Если добавляется новое подменю, то кеш по получению всех подменю должен
        обновиться
    7. Если добавляется новое блюдо, то кеш по получению всех блюд должен обновиться
    Начать нужно снизу в верх, сначала блюда, подменю, потом меню
    """

    def __init__(self,
                 redis_cacher=Depends(get_redis)):
        self.redis_cacher = redis_cacher

    async def delete_cache_by_mask(self,
                                   link):
        """
        Удаление записей из кеша по маске.

        Принимается маска ключа кеша, к ней добавляется мета-символ '*' и происходит
        удаление всех ключей из кеша, которые подходят под данную маску

        :param link: Маска ключа кеша.
        :return: None
        """
        for key in await self.redis_cacher.keys(link + '*'):
            await self.redis_cacher.delete(key)

    async def delete_list_cache(self,
                                link):
        """
        Удаление записей из кеша по указанной ссылке.

        :param link: Ссылка на ключ кеша, который нужно удалить.
        :return: None
        """
        await self.redis_cacher.delete(link)

    async def set_all_dishes_cache(self,
                                   submenu_id,
                                   dish_list,
                                   menu_id):
        """
        Запись всех блюд в кеш.

        Ключ в Redis будет представлен в виде строки-ссылки на список всех блюд,
        сформированной на основе указанных menu_id и submenu_id.

        Значение в кеше будет представлять список блюд в формате pickle.

        Время жизни данного кеша ограничено переменной app.config.EXPIRATION.

        :param menu_id: ID меню у подменю для данного блюда.
        :param submenu_id: Идентификатор подменю.
        :param dish_list: Список блюд для сохранения в кеш.
        :return: None.
        """
        await self.redis_cacher.set(
            f'/menus/{menu_id}/submenus/{submenu_id}/dishes',
            pickle.dumps(dish_list),
            ex=EXPIRATION
        )

    async def get_all_dishes_cache(self,
                                   menu_id,
                                   submenu_id):
        """
        Получение всех блюд из кеша.

        Из Redis извлекается сериализованный json объект данных.
        Для получения оригинальных данных, этот json объект десериализуется.

        :param menu_id: Идентификатор меню.
        :param submenu_id: Идентификатор подменю.
        :return: Список блюд из кеша, либо None, если кеш не существует.
        """
        cache = await self.redis_cacher.get(
            f'/menus/{menu_id}/submenus/{submenu_id}/dishes'
        )
        if cache:
            dish_list = pickle.loads(cache)
            return dish_list
        return None

    async def set_dish_cache(self,
                             menu_id,
                             submenu_id,
                             dish_info):
        """
        Запись информации о блюде в кеш.

        :param menu_id: ID меню.
        :param submenu_id: ID подменю.
        :param dish_info: Информация о блюде для записи в кеш.
        :return: None
        """
        await self.redis_cacher.set(
            f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_info.id}',
            pickle.dumps(dish_info),
            ex=EXPIRATION
        )

    async def get_dish_cache(self,
                             menu_id,
                             submenu_id,
                             dish_id):
        """
        Получение информации об одном блюде из кеша.

        :param menu_id: ID меню.
        :param submenu_id: ID подменю.
        :param dish_id: ID блюда.
        :return: Информация о блюде или None, если не найдено в кеше.
        """
        cache = await self.redis_cacher.get(
            f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}',
        )
        if cache:
            return pickle.loads(cache)
        return None

    async def create_new_dish_cache(self,
                                    dish_info,
                                    submenu_id,
                                    menu_id):
        """
        Создание новой записи о блюде в кеше.

        Если в БД происходит внесение изменений (в т.ч добавление нового блюда,
        изменение существующего блюда), то должно происходить обновление кеша
        для всех блюд, не задевая кеш для конкретных блюд

        Происходит удаление кеша для списка всех блюд, и создается кеш для создаваемого
        блюда.

        :param menu_id: ID меню у подменю для данного блюда
        :param dish_info: Информация о создаваемом блюде.
        :param submenu_id: ID подменю.
        :return: None
        """
        await self.delete_list_cache(
            link=f'/menus/{menu_id}/submenus/{submenu_id}/dishes'
        )
        await self.set_dish_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_info=dish_info
        )

    async def update_dish_cache(self,
                                dish_info,
                                menu_id,
                                submenu_id):
        """
        Обновление кеша конкретного блюда при изменении этого блюда в БД.

        Если в БД происходит внесение изменений (в т.ч изменение существующего блюда),
        то должно происходить обновление кеша для данного конкретного блюда

        Происходит удаление кеша для данного блюда, повторное создание кеша для данного
        блюда.

        :param dish_info: Информация о блюде.
        :param menu_id: ID меню.
        :param submenu_id: ID подменю.
        :return: None
        """
        await self.delete_cache_by_mask(
            link=f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_info.id}'
        )
        await self.set_dish_cache(
            dish_info=dish_info,
            submenu_id=submenu_id,
            menu_id=menu_id,
        )

    async def delete_dish_cache(self,
                                menu_id: str,
                                submenu_id: str,
                                dish_id: str):
        """
        Удаление кеша в связи с удалением блюда из БД

        :param menu_id: ID меню
        :param submenu_id: ID подменю
        :param dish_id: ID блюда
        :return: None
        """
        await self.delete_cache_by_mask(
            link=f'/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}'
        )
