import logging
from typing import Dict
from typing import List

logger = logging.getLogger("OkvedParser")


class OkvedParser:
    def flatten_okved(self, data: List[Dict]) -> List[Dict]:
        """
        Рекурсивный парсинг okved.json в плоскйи список
        """
        flat_list = []
        logger.info("Рекурсивный парсинг okved.json в плоскйи список")

        def walk(items):
            for item in items:
                clean_code = str(item.get("code", "")).replace(".", "")
                flat_list.append(
                    {
                        "code": clean_code,
                        "original_code": item.get("code"),
                        "name": item.get("name"),
                    }
                )
                if "items" in item:
                    walk(item["items"])

        walk(data if isinstance(data, list) else [data])
        return flat_list
