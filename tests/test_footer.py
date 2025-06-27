from writer_bot.prompt import parse_footer


def test_parse_footer_success():
    footer = "\n```json\n{\"words\": 1180, \"done\": false}\n```\n"
    meta = parse_footer(footer)
    assert meta["words"] == 1180
    assert meta["done"] is False


def test_parse_footer_failure():
    bad = "nonsense"
    assert parse_footer(bad) == {}
