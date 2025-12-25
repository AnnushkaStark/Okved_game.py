from services.okved_parser import OkvedParser


def test_flatten_okved_recursion() -> None:
    parser = OkvedParser()
    nested_data = [
        {
            "code": "01",
            "name": "Root",
            "items": [
                {
                    "code": "01.1",
                    "name": "Child",
                    "items": [{"code": "01.11.1", "name": "Grandchild"}],
                }
            ],
        }
    ]

    flat_list = parser.flatten_okved(nested_data)
    assert len(flat_list) == 3
    assert flat_list[0]["code"] == "01"
    assert flat_list[2]["code"] == "01111"
    assert flat_list[2]["name"] == "Grandchild"
