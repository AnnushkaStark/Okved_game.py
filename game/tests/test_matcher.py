from services.okved_mather import OkvedMatcher


def test_matcher_max_suffix(matcher: OkvedMatcher) -> None:
    result = matcher.find_by_suffix("+79000000515")
    assert result["code"] == "26.51.5"
    assert result["match_len"] == 3


def test_matcher_fallback(matcher: OkvedMatcher, mock_data) -> None:
    result = matcher.fallback_search("+70111000000", mock_data)
    assert result["code"] == "01.11"
