import json
import logging
from typing import Any
from module.conf import settings
# from openai import AsyncOpenAI
# TODO: 再说吧TVT
logger = logging.getLogger(__name__)

DEFAULT_PROMPT = """\
You will now play the role of a super assistant. 
Your task is to extract structured data from unstructured text content and output it in JSON format. 
If you are unable to extract any information, please keep all fields and leave the field empty or default value like `''`, `None`.
But Do not fabricate data!

the python structured data type is:

```python
@dataclass
class Episode:
    title_en: str|None
    title_zh: str|None
    title_jp: str|None
    season: int
    season_raw: str
    episode: int
    sub: str
    group: str
    resolution: str
    source: str
```

Example:

```
input: "【喵萌奶茶屋】★04月新番★[夏日重现/Summer Time Rendering][11][1080p][繁日双语][招募翻译]"
output: '{"group": "喵萌奶茶屋", "title_en": "Summer Time Rendering", "resolution": "1080p", "episode": 11, "season": 1, "title_zh": "夏日重现", "sub": "", "title_jp": "", "season_raw": "", "source": ""}'

input: "【幻樱字幕组】【4月新番】【古见同学有交流障碍症 第二季 Komi-san wa, Komyushou Desu. S02】【22】【GB_MP4】【1920X1080】"
output: '{"group": "幻樱字幕组", "title_en": "Komi-san wa, Komyushou Desu.", "resolution": "1920X1080", "episode": 22, "season": 2, "title_zh": "古见同学有交流障碍症", "sub": "", "title_jp": "", "season_raw": "", "source": ""}'

input: "[Lilith-Raws] 关于我在无意间被隔壁的天使变成废柴这件事 / Otonari no Tenshi-sama - 09 [Baha][WEB-DL][1080p][AVC AAC][CHT][MP4]"
output: '{"group": "Lilith-Raws", "title_en": "Otonari no Tenshi-sama", "resolution": "1080p", "episode": 9, "season": 1, "source": "WEB-DL", "title_zh": "关于我在无意间被隔壁的天使变成废柴这件事", "sub": "CHT", "title_jp": ""}'
```
"""


# api_key: str,
# api_base: str = "https://api.openai.com/v1",
# model: str = "gpt-3.5-turbo",
class OpenAIParser:
    def __init__(
        self,
        **kwargs,
    ) -> None:
        """OpenAIParser is a class to parse text with openai

        Args:
            api_key (str): the OpenAI api key
            api_base (str):
                the OpenAI api base url, you can use custom url here. \
                Defaults to "https://api.openai.com/v1".
            model (str):
                the ChatGPT model parameter, you can get more details from \
                https://platform.openai.com/docs/api-reference/chat/create. \
                Defaults to "gpt-3.5-turbo".
            kwargs (dict):
                the OpenAI ChatGPT parameters, you can get more details from \
                https://platform.openai.com/docs/api-reference/chat/create.

        Raises:
            ValueError: if api_key is not provided.
        """
        if not settings.experimental_openai.api_key:
            raise ValueError("API key is required.")

        self._api_key = settings.experimental_openai.api_key
        self.api_base = settings.experimental_openai.api_base
        self.model = settings.experimental_openai.model
        self.openai_kwargs = kwargs

    async def parse(
        self, text: str, prompt: str | None = None, asdict: bool = True
    ) -> dict | str:
        """parse text with openai

        Args:
            text (str): the text to be parsed
            prompt (str | None, optional):
                the custom prompt. Built-in prompt will be used if no prompt is provided. \
                Defaults to None.
            asdict (bool, optional):
                whether to return the result as dict or not. \
                Defaults to True.

        Returns:
            dict | str: the parsed result.
        """
        if not prompt:
            prompt = DEFAULT_PROMPT

        params = self._prepare_params(text, prompt)
        print(params)

        # with ThreadPoolExecutor(max_workers=1) as worker:
        #     future = worker.submit(openai.ChatCompletion.create, **params)
        #     resp = future.result()
        #
        #     result = resp["choices"][0]["message"]["content"]

        
        # async with RequestContent() as req:
        #     json_contents = await req.post_data(url)
        #     print(json_contents)
        # if asdict:
        #     try:

        #         result = json.loads(result)
        #     except json.JSONDecodeError:
        #         logger.warning(f"Cannot parse result {result} as python dict.")
        #
        # logger.debug(f"the parsed result is: {result}")

        # return result

    def _prepare_params(self, text: str, prompt: str) -> dict[str, Any]:
        """_prepare_params is a helper function to prepare params for openai library.
        There are some differences between openai and azure openai api, so we need to
        prepare params for them.

        Args:
            text (str): the text to be parsed
            prompt (str): the custom prompt

        Returns:
            dict[str, Any]: the prepared key value pairs.
        """
        params = dict(
            api_key=self._api_key,
            api_base=self.api_base,
            messages=[
                dict(role="system", content=prompt),
                dict(role="user", content=text),
            ],
            # set temperature to 0 to make results be more stable and reproducible.
            temperature=0,
        )

        api_type = self.openai_kwargs.get("api_type", "openai")
        if api_type == "azure":
            params["deployment_id"] = self.openai_kwargs.get("deployment_id", "")
            params["api_version"] = self.openai_kwargs.get("api_version", "2023-05-15")
            params["api_type"] = "azure"
        else:
            params["model"] = self.model

        return params


if __name__ == "__main__":
    import asyncio
    test = OpenAIParser()
    asyncio.run(test.parse("2"))


    test = OpenAIParser()

