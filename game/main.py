import asyncio
import logging
import sys

from services.okved_mather import OkvedMatcher
from services.okved_parser import OkvedParser
from services.phone_normalizer import PhoneNormalizer
from services.uploader import GitHubClient
from utils.exceptions import DataLoadError
from utils.exceptions import NormalizationError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("OkvedGame")


async def run_game():
    print("\n" + "=" * 50)
    print("🎮 ДОБРО ПОЖАЛОВАТЬ В ОКВЭД-КВЕСТ")
    print("=" * 50)

    logger.info("Инициализация системы...")
    client = GitHubClient()
    parser = OkvedParser()
    noramlizer = PhoneNormalizer()

    try:
        try:
            raw_data = await client.get_okved_data()
        except DataLoadError as error:
            print(f"❌ Ошибка: {error}")

        flat_data = parser.flatten_okved(raw_data)
        matcher = OkvedMatcher(flat_data)

    except Exception as e:
        logger.error(f"Не удалось запустить игру: {e}")
        return

    while True:
        print("\n--- НОВЫЙ ПОИСК ---")
        user_input = input(
            "Введите российский номер телефона (или 'exit' для выхода): "
        ).strip()

        if user_input.lower() in ["exit", "отмена", "ку"]:
            print("Спасибо за игру!")
            break
        try:
            normalized = noramlizer.normalize_phone(phone=user_input)
        except NormalizationError as error:
            print(f"❌ Ошибка: {error}")
            continue

        result = matcher.find_match(normalized)

        if result:
            print("✅ УСПЕХ!")
            print(f"   • Номер: {normalized}")
            print(f"   • ОКВЭД: {result['code']} — {result['name']}")
            print(f"   • Длина совпадения: {result['match_len']} симв.")
        else:
            print("🔍 Ничего не нашли даже в резервах.")

        retry = (
            input("\nХотите проверить другой номер? (да/нет): ")
            .strip()
            .lower()
        )
        if retry not in ["да", "y", "yes", "1"]:
            print("До встречи!")
            break


if __name__ == "__main__":
    try:
        asyncio.run(run_game())
    except KeyboardInterrupt:
        print("\nИгра прервана пользователем.")
        sys.exit(0)
