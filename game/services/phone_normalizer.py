import logging
import re

from utils.exceptions import NormalizationError

logger = logging.getLogger("PhoneNormalizer")


class PhoneNormalizer:
    def _clean_phone(self, phone: str) -> str:
        """
        Очистка номера телефона от лишних символов
        возвращает строку только из цифр
        """
        logger.info("Очистка номера телефона")
        clean_phone = re.sub(r"\D", "", phone)
        return clean_phone

    def normalize_phone(self, phone: str) -> str:
        """
        Нормализация номера телефона
        """
        logger.info("Нормализация  номера телефона")
        clean_phone = self._clean_phone(phone=phone)

        match len(clean_phone):
            case 10:
                logger.info("Длина ввеенного номера 9  цифр")
                if clean_phone.startswith("9"):
                    logger.info("Номер нормализован")
                    return f"+7{clean_phone}"
                logger.warning("Ошибка нормализации некорректный номер")
                raise NormalizationError("Некорректный номер телефона")

            case 11:
                logger.info("Длина введенного номера 10  цифр")
                if clean_phone.startswith("8"):
                    logger.info("Номер нормализован")
                    return f"+7{clean_phone[1:]}"

                elif clean_phone.startswith("7"):
                    logger.info("Номер нормализован")
                    return f"+{clean_phone}"
                logger.warning("Ошибка нормализации некорректный номер")
                raise NormalizationError("Некорректный номер телефона")

            case _:
                logger.warning("Ошибка нормализации некорректный номер")
                raise NormalizationError("Некорректный номер телефона")
