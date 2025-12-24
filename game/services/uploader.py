import json
import logging
import os
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from typing import Dict
from typing import List

import aiofiles
from dotenv import load_dotenv
from httpx import AsyncClient
from utils.exceptions import DataLoadError

load_dotenv()


logger = logging.getLogger("GitHubClient")


class GitHubClient:
    json_url = "/bergstar/testcase/master/okved.json"
    cache_file = "okved_cache.json"

    @asynccontextmanager
    async def _get_client(self) -> AsyncGenerator[AsyncClient, None]:
        git_hub_client = AsyncClient(base_url=os.getenv("GITHUB_URL"))
        yield git_hub_client

    async def _load_okved_json(self) -> List[Dict[str, str]]:
        """
        Загрузка файла okved.json
        """
        async with self._get_client() as client:
            logger.info("Загрузка файла okved.json")
            response = await client.get(self.json_url)

            if response.status_code != 200:
                logger.error("Ошибка загрузки файла")
                raise DataLoadError("Ошибка загрузки файла")

            logger.info("Определение наличия записей okved")
            data = json.loads(response.content.decode("utf-8-sig"))
            if data == [] or data == [{}]:
                logger.error("Загружуен пустой файл")
                raise DataLoadError("Загружен пустой файл")

            logger.info("Запись okved.json")
            async with aiofiles.open(
                self.cache_file, "w", encoding="utf-8"
            ) as f: 
                json.dump(data, f, ensure_ascii=False, indent=4)

                return data

    async def _read_okved_json(self) -> List[Dict[str, str]]:
        """
        Чтение файла okved.json
        """
        logger.info("Чтение okved.json")
        async with aiofiles.open(self.cache_file, "r", encoding="utf-8") as f:
            content = await f.read() 
            return json.load(content)

    async def get_okved_data(self) -> List[Dict[str, str]]:
        """
        Получение okved.json
        """
        logger.info("Получение  okved.json")
        if os.path.exists(self.cache_file):
            logger.info("Провекра обновлений okved.json")
            file_age = time.time() - os.path.getmtime(self.cache_file)

            if file_age < 86400:
                return await self._read_okved_json()
            
        return await self._load_okved_json()
    