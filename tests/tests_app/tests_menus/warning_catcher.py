"""
Данный модуль рассчитан для создания декоратора по перехватыванию warning сообщений, но функционал не доработан

"""

import warnings
import functools


def log_warnings(logger):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with WarningCollector() as collector:
                result = func(*args, **kwargs)
            for warning in collector.warnings:
                logger.warning(f"Captured warning: {warning}")
            return result

        return wrapper

    return decorator


class WarningCollector:
    """
    Класс для сбора предупреждений.

    Для использования этого сборщика предупреждений в тестовом классе необходимо создать логгер:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    """

    def __init__(self):
        self.warnings = []

    def __enter__(self):
        """
        Вход в контекстный менеджер.

        При использовании контекстного менеджера будет вызываться warnings.showwarning вместо _collect_warning.
        Таким образом, все предупреждения будут перехвачены и сохранены в атрибуте warnings.

        :return: Экземпляр текущего объекта WarningCollector.
        """
        self._showwarning = warnings.showwarning  # Сохраним оригинальную функцию warnings.showwarning
        warnings.showwarning = self._collect_warning  # Перенаправим warnings.showwarning на метод _collect_warning
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Выход из контекстного менеджера.

        При завершении оператора with возвращаем значение оригинальной функции warnings.showwarning обратно,
        чтобы восстановить её функциональность после завершения блока оператора with.

        :param exc_type: Тип исключения, если оно возникло (None в противном случае).
        :param exc_value: Значение исключения, если оно возникло (None в противном случае).
        :param traceback: Объект traceback, представляющий стек вызовов (None в противном случае).
        :return: None
        """
        warnings.showwarning = self._showwarning

    def _collect_warning(self, message, category, filename, lineno, file=None, line=None):
        """
        Метод для сбора предупреждений.

        :param message: Текст предупреждения.
        :param category: Класс категории предупреждения (например, DeprecationWarning).
        :param filename: Имя файла, в котором было вызвано предупреждение.
        :param lineno: Номер строки, в которой было вызвано предупреждение.
        :param file: Объект файла (по умолчанию None).
        :param line: Строка кода, вызвавшая предупреждение (по умолчанию None).
        :return: None
        """
        self.warnings.append(message)
