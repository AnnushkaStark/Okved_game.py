class OkvedError(Exception):
    """
    Базовая ошибка
    """

    pass


class NormalizationError(OkvedError):
    """
    Ошибка  нормализации номера
    """

    pass


class DataLoadError(OkvedError):
    """
    Ошибка загрузки json
    """

    pass


class MatchingNotFoundError(OkvedError):
    """
    Ошибка, если не найдено даже резервное совпадение
    """

    pass
