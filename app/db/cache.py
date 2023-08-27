import pickle

from fastapi import Depends

from app.config import EXPIRATION
from app.db.database_connect import get_redis


class CacheRepository:
    """
    Сервисный слой для кеширования запросов
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

    async def delete_cache_except_dish_keys(self):
        """
        Удаление всех записей из кеша, кроме ключей для конкретных блюд.

        :return: None
        """
        all_keys = await self.redis_cacher.keys('*')

        dish_keys_to_keep = set()
        for key in all_keys:
            key_str = key.decode('utf-8')
            if '/dishes/' in key_str:
                dish_keys_to_keep.add(key)

        keys_to_delete = [key for key in all_keys if key not in dish_keys_to_keep]

        for key in keys_to_delete:
            await self.redis_cacher.delete(key)

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
        await self.delete_cache_except_dish_keys()
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

    async def get_all_submenus_cache(self,
                                     menu_id):
        """
        Получение всех подменю из кеша.

        Из Redis извлекается сериализованный pickle объект данных.
        Для получения оригинальных данных, этот pickle объект десериализуется.

        :param menu_id: Идентификатор меню.
        :return: Список подменю из кеша, либо None, если кеш не существует.
        """
        cache = await self.redis_cacher.get(
            f'/menus/{menu_id}/submenus/'
        )
        if cache:
            return pickle.loads(cache)
        return None

    async def set_all_submenus_cache(self,
                                     menu_id,
                                     submenu_list):
        """
        Запись всех подменю в кеш.

        Ключ в Redis будет представлен в виде строки-ссылки на список всех блюд,
        сформированной на основе указанного menu_id.

        Значение в кеше будет представлять список блюд в формате pickle.

        Время жизни данного кеша ограничено переменной app.config.EXPIRATION.

        :param menu_id: ID меню для данного подменю .
        :param submenu_list: Список подменю для сохранения в кеш.
        :return: None.
        """
        await self.redis_cacher.set(
            f'/menus/{menu_id}/submenus',
            pickle.dumps(submenu_list),
            ex=EXPIRATION
        )

    async def get_submenu_cache(self,
                                menu_id,
                                submenu_id):
        """
        Получение информации об одном подменю из кеша

        :param menu_id: ID меню, в котором находится искомое подменю.
        :param submenu_id: ID получаемого подменю.
        :return: Информация о подменю или None, если нет в кеше.
        """
        cache = await self.redis_cacher.get(
            f'/menus/{menu_id}/submenus/{submenu_id}'
        )
        if cache:
            return pickle.loads(cache)
        return None

    async def set_submenu_cache(self,
                                menu_id,
                                submenu_id,
                                submenu_info):
        """
        Запись информации о подменю в кеш

        :param submenu_info: Информация о подменю.
        :return: None.
        """
        await self.redis_cacher.set(
            f'/menus/{menu_id}/submenus/{submenu_id}',
            pickle.dumps(submenu_info),
            ex=EXPIRATION
        )

    async def create_new_submenu_cache(self,
                                       submenu_info,
                                       menu_id,
                                       submenu_id):
        """
        Создание новой записи о подменю в кеше.

        Если в БД происходит внесение изменений (в т.ч добавление нового подменю),
        то должно происходить обновление кеша для всех подменю, не задевая кеш для
        конкретных подменю

        Происходит удаление кеша для списка всех подменю, и создается кеш для создаваемого
        подменю.

        :param menu_id: ID меню у данного подменю
        :param submenu_info: Информация о создаваемом подменю.
        :return: None
        """
        await self.delete_cache_except_dish_keys()
        await self.set_submenu_cache(
            submenu_info=submenu_info,
            menu_id=menu_id,
            submenu_id=submenu_id
        )

    async def update_submenu_cache(self,
                                   submenu_info,
                                   menu_id: str,
                                   submenu_id: str):
        """
        Обновление кеша конкретного подменю при изменении этого подменю в БД.

        Если в БД происходит внесение изменений (в т.ч изменение существующего подменю),
        то должно происходить обновление кеша для данного конкретного подменю

        Происходит удаление кеша для данного подменю, повторное создание кеша для данного
        подменю.

        :param submenu_info: Информация о подменю.
        :return: None
        """
        await self.delete_cache_by_mask(
            link=f'/menus/{submenu_info.menu_id}/submenus/{submenu_info.id}'
        )
        await self.set_submenu_cache(
            submenu_info=submenu_info,
            menu_id=menu_id,
            submenu_id=submenu_id
        )

    async def delete_submenu_cache(self,
                                   menu_id,
                                   submenu_id):
        """
        Удаление кеша в связи с удалением блюда из БД

        :param submenu_info: Информация об удаляемом подменю
        :return: None
        """
        await self.delete_cache_by_mask(
            link=f'/menus/{menu_id}/submenus/{submenu_id}'
        )

    async def get_all_menus_cache(self):
        """
        Получение всех подменю из кеша.

        Из Redis извлекается сериализованный pickle объект данных.
        Для получения оригинальных данных, этот pickle объект десериализуется.

        :return: Список подменю из кеша, либо None, если кеш не существует.
        """
        cache = await self.redis_cacher.get(f'/menus/')
        if cache:
            return pickle.loads(cache)
        return None

    async def set_all_menus_cache(self,
                                  menu_list):
        """
        Запись всех подменю в кеш.

        Ключ в Redis будет представлен в виде строки-ссылки на список всех блюд,
        сформированной на основе указанного menu_id.

        Значение в кеше будет представлять список блюд в формате pickle.

        Время жизни данного кеша ограничено переменной app.config.EXPIRATION.

        :param menu_list:
        :return: None.
        """
        await self.redis_cacher.set(
            f'/menus/',
            pickle.dumps(menu_list),
            ex=EXPIRATION
        )

    async def get_menu_cache(self,
                             menu_id):
        """
        Получение информации об одном подменю из кеша

        :param menu_id: ID меню, в котором находится искомое подменю.
        :return: Информация о подменю или None, если нет в кеше.
        """
        cache = await self.redis_cacher.get(
            f'/menus/{menu_id}'
        )
        if cache:
            return pickle.loads(cache)
        return None

    async def set_menu_cache(self,
                             menu_id,
                             menu_info):
        """
        Запись информации о подменю в кеш

        :param menu_id:
        :param menu_info: Информация о меню.
        :return: None.
        """
        await self.redis_cacher.set(
            f'/menus/{menu_id}',
            pickle.dumps(menu_info),
            ex=EXPIRATION
        )

    async def create_new_menu_cache(self,
                                    menu_info):
        """
        Создание новой записи о подменю в кеше.

        Если в БД происходит внесение изменений (в т.ч добавление нового подменю),
        то должно происходить обновление кеша для всех подменю, не задевая кеш для
        конкретных подменю

        Происходит удаление кеша для списка всех подменю, и создается кеш для создаваемого
        подменю.

        :param menu_info:
        :return: None
        """
        await self.delete_list_cache(
            link=f'/menus/'
        )
        await self.set_menu_cache(
            menu_info=menu_info,
            menu_id=menu_info.id
        )

    async def update_menu_cache(self,
                                menu_info,
                                menu_id: str):
        """
        Обновление кеша конкретного подменю при изменении этого подменю в БД.

        Если в БД происходит внесение изменений (в т.ч изменение существующего подменю),
        то должно происходить обновление кеша для данного конкретного подменю

        Происходит удаление кеша для данного подменю, повторное создание кеша для данного
        подменю.

        :param menu_id:
        :param menu_info: Информация о подменю.
        :return: None
        """
        await self.delete_cache_by_mask(
            link=f'/menus/{menu_id}'
        )
        await self.set_menu_cache(
            menu_info=menu_info,
            menu_id=menu_id,
        )

    async def delete_menu_cache(self,
                                menu_id):
        """
        Удаление кеша в связи с удалением блюда из БД

        :param menu_id:
        :return: None
        """
        await self.delete_cache_by_mask(
            link=f'/menus/{menu_id}'
        )
