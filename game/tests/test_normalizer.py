import pytest
from services.phone_normalizer import PhoneNormalizer
from utils.exceptions import NormalizationError


def test_normalizer_success() -> None:
    normalizer = PhoneNormalizer()
    assert normalizer.normalize_phone("89643164478") == "+79643164478"
    assert normalizer.normalize_phone("+7 964 316 44 78") == "+79643164478"
    assert normalizer.normalize_phone("9643164478") == "+79643164478"


def test_normalizer_fail() -> None:
    normalizer = PhoneNormalizer()
    with pytest.raises(NormalizationError):
        normalizer.normalize_phone("12345")
    with pytest.raises(NormalizationError):
        normalizer.normalize_phone("849512345676")
