import pytest
from module.conf import settings
from module.parser.title_parser import RawParser


class TestTitleParser:
    def test_parse_without_openai(self):
        text = "[梦蓝字幕组]New Doraemon 哆啦A梦新番[747][2023.02.25][AVC][1080P][GB_JP][MP4]"
        result = RawParser.parser(text)
        assert result is not None
        assert result.group_name == "梦蓝字幕组"
        assert result.title_raw == "New Doraemon"
        assert result.dpi == "1080P"
        assert result.season == 1
        assert result.subtitle == "GB_JP"

    # @pytest.mark.skipif(
    #     not settings.experimental_openai.enable,
    #     reason="OpenAI is not enabled in settings",
    # )
    # def test_parse_with_openai(self):
    #     text = "[梦蓝字幕组]New Doraemon 哆啦A梦新番[747][2023.02.25][AVC][1080P][GB_JP][MP4]"
    #     result = RawParser.parser(text)
    #     assert result is not None
    #     assert result.group_name == "梦蓝字幕组"
    #     assert result.title_raw == "New Doraemon"
    #     assert result.dpi == "1080P"
    #     assert result.season == 1
    #     assert result.subtitle == "GB_JP"
