import bisect
import logging
from typing import Dict
from typing import List
from typing import Optional

from utils.exceptions import MatchingNotFoundError

logger = logging.getLogger("OkvedMatcher")


class OkvedMatcher:
    def __init__(self, flat_data: List[Dict]) -> Optional[Dict]:
        logger.info("Cортировка данных okved.json")
        self.indexed_data = sorted(
            [
                (item["code"][::-1], item)
                for item in flat_data
                if item["code"].isdigit()
            ],
            key=lambda x: x[0],
        )

        self.keys = [x[0] for x in self.indexed_data]

    def find_by_suffix(self, phone: str) -> Optional[Dict]:
        """
        Поиск по суффиксу
        """
        logger.info("Получение суффикса номера")
        target = phone[2:][::-1]

        logger.info("Бинарный поиск по отсортированным данным")
        idx = bisect.bisect_left(self.keys, target)

        best_match = None
        max_len = 0

        logger.info("Проверка индекса и  индекса сдедующего элемента")
        for i in range(max(0, idx - 1), min(len(self.keys), idx + 1)):
            rev_code, item = self.indexed_data[i]

            logger.info("Подстчет длины совпадений")
            match_len = 0
            for c1, c2 in zip(target, rev_code, strict=True):
                if c1 == c2:
                    match_len += 1
                else:
                    break
            logger.info("Проверка максимальной длины совпадений")
            if match_len > max_len:
                logger.info(
                    "Cовпадени найдено переоперделяем код оквед и  максимальную длину"
                )
                max_len = match_len
                best_match = item

        if best_match:
            return {
                "normalized_phone": phone,
                "code": best_match["original_code"],
                "name": best_match["name"],
                "match_len": max_len,
            }

    def fallback_search(
        self, phone: str, flat_data: List[Dict]
    ) -> Optional[Dict]:
        """
        Резервная стратегия: поиск самого длинного кода в начале номера.
        """
        logger.warning(
            "Основной поиск не дал результатов. Запуск резервной стратегии"
        )
        phone_digits = phone[2:]
        logger.info("Получаем номер без +7")

        best_match = None
        max_len = 0

        logger.info("Проверка наличия кода okved в начале номера")
        for item in flat_data:
            code = item["code"]
            if phone_digits.startswith(code):
                if len(code) > max_len:
                    logger.info(
                        "Номер найден макисмальная длина переопределена"
                    )
                    max_len = len(code)
                    best_match = item

        if not best_match:
            return
        return {
            "normalized_phone": phone,
            "code": best_match["original_code"],
            "name": best_match["name"],
            "match_len": max_len,
        }

    def find_match(self, phone: str) -> Optional[Dict]:
        """
        Поиск совпадений
        """
        logger.info("Начинаем посик совпадений")
        if found_match := self.find_by_suffix(phone=phone):
            return found_match
        found_match = self.fallback_search(phone=phone)
