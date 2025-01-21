import logging
import re

from module.models import Episode

logger = logging.getLogger(__name__)


LAST_BACKET_PATTERN = re.compile(
    r"[\(\（][^\(\)（）]*[\)\）](?!.*[\(\（][^\(\)（）]*[\)\）])"
)


EPISODE_PATTERN = re.compile(
    r"""
    # (?=\b|\s|\+|\-|\[|\]|/|～)
    (第?(\d+?(?:\.\d)?)[话話集]
    |EP?(\d+(?:\.\d)?)
    |-\s(\d+(?:\.\d)?)
    |(\d+(?:\.\d)?).?v\d
    |(\d+(?:\.\d)?).?END
    |(\d+(?:\.\d)?)pre)
    (?=\s|_|\-|\[|\]|$|\.)
""",
    re.VERBOSE | re.IGNORECASE,
)

EPISODE_RE_UNTRUSTED = re.compile(r"[\b\s\[\]]((\d+(?:\.\d)?))[\s\b\[\]]")

SEASON_RE = re.compile(
    r"""
    (?=\b|\s|\+|\-|\[|\]|/|～)
    ( 第(.{1,3})季       # 匹配"第...季"格式
    |第(.{1,3})期        # 匹配"第...期"格式
    |第.{1,3}部分      # 匹配"第...部分"格式
    |[Ss]eason\s(\d{1,2})  # 匹配"Season X"格式
    |[Ss](\d{1,2})         # 匹配"SX"格式
    |(\d+)[r|n]d(?:\sSeason)?  # 匹配"Xnd Season"格式
    |part \d   #part 6
    |(IV|III|II|I)            # 匹配罗马数字
    )
    (?=\b|\s|_|\-|\[|\]|$)  
    """,
    re.VERBOSE,
)

SEASON_PATTERN_UNTRUSTED = re.compile(r"\d+")

VIDEO_TYPE_PATTERN = re.compile(
    r"""
    [\b\s\._\+\-\[\]]# Frame rate
    (23.976FPS
    |24FPS
    |29.97FPS
    |[30|60|120]FPS
    # Video codec
    |8-?BITS?
    |10-?BITS?
    |HI10P?
    |[HX].?26[4|5]
    |AVC
    |HEVC2?
    # Video format
    |AVI
    |RMVB
    |MKV
    |MP4
    # video quailty
    |HD
    |BD
    |UHD
    |SRT[x2].?
    |ASS[x2].? # AAAx2
    |PGS
    |V[123]
    |OVA)(?=\b|\s|_|\-|\+|\[|\]|$) # 不能消耗掉后面的""",
    re.VERBOSE | re.IGNORECASE,
)

AUDIO_INFO = re.compile(
    r"""
    [\b\s_\-\[\]]# Frame rate
    (AAC(?:x2)?
    |FLAC
    |DDP
    )(?=\b|\s|_|\-|\[|\]|$) # 不能消耗掉后面的""",
    re.VERBOSE | re.IGNORECASE,
)

RESOLUTION_RE = re.compile(
    r"""
    (?=\s|\b|\[|\]])
    (\d{3,4}[×X]\d{3,4}
    |1080p?
    |720p?
    |480p?
    |2160p?
    |4K
    )
    (?=\b|\s|_|\-|\[|\]|$) # 不能消耗掉后面的""",
    re.IGNORECASE | re.VERBOSE,
)

SOURCE_RE = re.compile(
    r"""[\s\b\[\]]([Bb]-[Gg]lobal
    |[Bb]aha
    |[Bb]ilibili
    |AT-X
    |W[eE][Bb]-?(?:Rip)?(?:DL)?
    |CR
    |ABEMA
    |viutv[粤语]*?)
    [\s\b\[\]]""",
    re.VERBOSE | re.IGNORECASE,
)

SUB_RE = re.compile(
    r"""[\s_\+\-\[\]/]
    ((?:[(BIG5|CHS|CHT|GB|JP)_简中繁日英外字幕挂内封嵌双语文体]+)
    |CHT
    |CHS
    |BIG5
    |CHI
    |JA?P
    |GB
    |HardSub
    ) (?=\s|_|\-|\[|\]|$/) # 不能消耗掉后面的""",
    re.VERBOSE,
)
PREFIX_RE = re.compile(r"[^\w\s\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff-]")

CHINESE_NUMBER_MAP = {
    "一": 1,
    "二": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}
ROMAN_NUMBERS = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
}

UNUSEFUL_RE = re.compile(
    r"""
    # 匹配无用的片段
    (?<=\s|_|\-|\[|\])   # 前置断言，确保前面是这些字符之一
    (.?[\d一四七十春夏秋冬季]{1,2}月(?:新番|短剧).*?  # 匹配日期和类型
        | 港澳台地区
        | 国漫
        | END
        | 招募.*?
        | \d{4}年\d{1,2}月.*?
        | \d{4}\.\d{1,2}\.\d{1,2}
        |[网盘无水印高清下载迅雷]{4,10}
    )
    (?=\s|_|\-|\[|\]|$)  # 后置断言，确保后面是这些字符之一
    """,
    re.VERBOSE,
)


class RawParser:
    def __init__(self, title: str) -> None:
        self.raw_title = title
        self.title = title
        self.process_title()

    def process_title(self):

        self.title = self.title.replace("\n", " ")

        # self.title = re.sub(LAST_BACKET_PATTERN, "", self.title)
        #

        translation_table = str.maketrans("【】", "[]")
        # translation_table = str.maketrans("【】()（）『』", "[][][][]")
        self.title = self.title.translate(translation_table)
        self.title = self.title.strip()

    # 示例
    # self.title = replace_chars(self.title)
    # self.title = self.title.replace("【", "[").replace("】", "]").replace("(","[").replace(")","]")

    def parser(self):
        episode_info, episode_is_trusted, season_info, season_is_trusted = (
            self.get_episode_info()
        )
        # season_info = self.get_season_info()
        video_info = self.get_video_info()
        source_info = self.get_source_info()
        sub_info = self.get_sub_info()
        resolution_info = self.get_resolution_info()
        unuseful_info = self.get_unuseful_info()
        audio_info = self.get_audio_info()
        self.token = re.split(r"/\[\]", self.title)
        if len(self.token) > 1:
            self.token = self.token[:-1]
        self.token = "[]".join(self.token)
        self.token = re.split(r"[\[\]]", self.token)

        # print(f"{episode_info=}")
        # print(f"{video_info=}")
        # print(f"{unuseful_info=}")
        # print(f"{audio_info=}")
        # print(f"{sub_info=}")
        # print(f"{self.title=}")
        # print(f"{self.token=}")

        group = self.get_group()
        if not season_info:
            season_info, season_is_trusted = self.get_season_info()
        (
            name_en,
            name_zh,
            name_jp,
        ) = self.name_process()
        episode = self.parser_episode(episode_info, episode_is_trusted)
        season, season_raw = self.parse_season(season_info, season_is_trusted)

        source = source_info[0] if source_info else ""
        sub = sub_info[0] if sub_info else ""
        resolution = resolution_info[0] if resolution_info else ""

        return Episode(
            name_en,
            name_zh,
            name_jp,
            season,
            season_raw,
            episode,
            sub,
            group,
            resolution,
            source,
        )

    def findall_sub_title(self, pattern, sym="[]"):
        ans = re.findall(pattern, self.title)
        self.title = re.sub(pattern, sym, self.title)
        return ans

    def get_episode_info(self):
        episode_info = self.findall_sub_title(EPISODE_PATTERN, sym="/[]")
        episode_is_trusted = True
        season_info = self.findall_sub_title(SEASON_RE, sym="/[]")
        season_is_trusted = True
        if not episode_info:
            episode_info = self.findall_sub_title(EPISODE_RE_UNTRUSTED)
            episode_is_trusted = False
        return episode_info, episode_is_trusted, season_info, season_is_trusted

    def parser_episode(self, episode_info: list[tuple[str]], episode_is_trusted: bool):

        un_trusted_episode_list = []
        if not len(episode_info):
            # 实在没找到,返回0
            return 0
        if episode_is_trusted or len(episode_info) == 1:
            # 可信集数 or 长度为1
            # 秉持尽量返回的思想
            return self.episode_info_to_episode(episode_info[0])

        for un_trusted_episode in episode_info:
            un_trusted_episode_list.append(
                self.episode_info_to_episode(un_trusted_episode)
            )

        # 所有的集数一致
        if all(x == un_trusted_episode_list[0] for x in un_trusted_episode_list):
            return un_trusted_episode_list[0]

        if un_trusted_episode_list[1] not in [480, 720, 1080]:
            return un_trusted_episode_list[1]
        return un_trusted_episode_list[0]

    def parse_season(
        self, season_info: list[tuple[str]], season_is_trusted: bool
    ) -> tuple[int, str]:
        if len(season_info):
            season_list = [self.season_info_to_season(s) for s in season_info]
            if season_is_trusted:
                return season_list[0], season_info[0][0]
        return 1, ""

    def episode_info_to_episode(self, episode_info: tuple[str]) -> int | float:
        for episode in episode_info[1:]:
            if episode:
                if "." in episode:
                    return float(episode)
                else:
                    return int(episode)
        # 并不会走到这里
        return 0

    def season_info_to_season(self, season_info: tuple[str]) -> int:
        for season in season_info:
            if season.isdigit():
                return int(season)
            elif season in CHINESE_NUMBER_MAP:
                return CHINESE_NUMBER_MAP[season]
            elif season in ROMAN_NUMBERS:
                return ROMAN_NUMBERS[season]
        return 0

    def get_season_info(self):
        season_info = self.findall_sub_title(SEASON_PATTERN_UNTRUSTED)
        is_trusted = False
        return season_info, is_trusted

    def name_process(self):

        max_len = 10 if len(self.token) > 10 else len(self.token)
        self.token = [
            self.token[i] for i in range(max_len) if (len(self.token[i].strip()) > 1)
        ]

        self.token = self.token[:5]
        token_priority = [len(s) for s in self.token]
        if len(self.token) == 1:
            anime_title = self.token[0]

        elif len(self.token) == 2:
            anime_title = self.token[1]
        else:
            token_priority[1] += 4
            for token, idx in zip(self.token, range(3)):
                if "/" in token:
                    token_priority[idx] += 10
                if "&" in token:
                    token_priority[idx] -= 12
                if "字幕" in token:
                    token_priority[idx] -= 90
                if re.search(r"[a-zA-Z]{3,}", token):
                    token_priority[idx] += 2
                if re.search(r"[\u0800-\u4e00]{2,}", token):
                    token_priority[idx] += 2
                if re.search(r"[\u4e00-\u9fa5]{2,}", token):
                    token_priority[idx] += 2
            # print(token_priority)
            idx = token_priority.index(max(token_priority))
            anime_title = self.token[idx]
            anime_title = anime_title.strip()
        anime_title = re.sub(r"^\\|\\$", "", anime_title)
        anime_title = anime_title.strip()

        name_en, name_zh, name_jp = None, None, None
        split = re.split(r"/|\s{2}|-\s{2}", anime_title)
        while "" in split:
            split.remove("")
        if len(split) == 1:
            if re.search("_{1}", anime_title) is not None:
                split = re.split("_", anime_title)
            elif re.search(" - {1}", anime_title) is not None:
                split = re.split("-", anime_title)
        if len(split) == 1:
            split_space = split[0].split(" ")
            for idx in [0, -1]:
                if re.search(r"^[\u4e00-\u9fa5]{2,}", split_space[idx]) is not None:
                    chs = split_space[idx]
                    split_space.remove(chs)
                    split = [chs, " ".join(split_space)]
                    break
        for token in split:
            if re.search(r"[\u0800-\u4e00]{2,}", token) and not name_jp:
                name_jp = token.strip()
            elif re.search(r"[\u4e00-\u9fa5]{2,}", token) and not name_zh:
                name_zh = token.strip()
            elif re.search(r"[a-zA-Z]{3,}", token) and not name_en:
                name_en = token.strip()
        return name_en, name_zh, name_jp

    def get_group(self):
        for group in self.token:
            if group := group.strip():
                group.replace("/", "")
                group.strip()
                return group
        return ""

    def get_video_info(self):
        video_info = self.findall_sub_title(VIDEO_TYPE_PATTERN)
        return video_info

    def get_resolution_info(self):
        resolution_info = self.findall_sub_title(RESOLUTION_RE)
        return resolution_info

    def get_source_info(self):
        source_info = self.findall_sub_title(SOURCE_RE)
        return source_info

    def get_unuseful_info(self):
        unusefun_info = self.findall_sub_title(UNUSEFUL_RE)
        return unusefun_info

    def get_sub_info(self):
        sub_info = self.findall_sub_title(SUB_RE)
        return sub_info

    def get_audio_info(self):
        audio_info = self.findall_sub_title(AUDIO_INFO)
        return audio_info


def get_raw():
    import json
    import random

    with open("./data.jsonl", "r", encoding="utf-8") as file:
        lines = file.readlines()
        line = random.choice(lines).strip()
    raw_name = json.loads(line).get("raw")
    return raw_name


def raw_parser(raw: str) -> Episode | None:
    ret = RawParser(raw).parser()
    return ret


if __name__ == "__main__":

    # title = get_raw()
    title = "赛马娘 (2018) S03E13.mp4"
    title = "[SweetSub][鹿乃子大摇大摆虎视眈眈][Shikanoko Nokonoko Koshitantan][04][WebRip][1080P][AVC 8bit][繁日双语][462.01 MB]"
    title = "[ANi] Make Heroine ga Oosugiru /  败北女角太多了！ - 01 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4]"
    title = "【极影字幕社】★4月新番 天国大魔境 Tengoku Daimakyou 第05话 GB 720P MP4（字幕社招人内详）"
    # title = "海盗战记 (2019) S01E01.mp4"
    # title =  "[SBSUB][CONAN][1082][V2][1080P][AVC_AAC][CHS_JP](C1E4E331).mp4"
    # title = "前辈是男孩子 (2024) S01E02.mp4"
    # title = "[SBSUB][CONAN][1082][V2][1080P][AVC_AAC][CHS_JP](C1E4E331).mp4"
    # title = "海盗战记 S01E01.zh-tw.ass"
    # title = "[百冬练习组&LoliHouse] BanG Dream! 少女乐团派对！☆PICO FEVER！ / Garupa Pico: Fever! - 26 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕][END] [101.69 MB]"
    # title ="【喵萌奶茶屋】★04月新番★[夏日重现/Summer Time Rendering][11][1080p][繁日双语][招募翻译]"
    # title = "【失眠搬运组】放学后失眠的你-Kimi wa Houkago Insomnia - 06 [bilibili - 1080p AVC1 CHS-JP].mp4"
    # title = "[KitaujiSub] Shikanoko Nokonoko Koshitantan [01Pre][WebRip][HEVC_AAC][CHS_JP].mp4"
    title = "[Doomdos] - 白色闪电 - 第02话 - [1080P].mp4"
    title = "Doomdos] -凡人修仙传-第107话-[1080P].mp"
    # title = "[豌豆字幕组&风之圣殿字幕组】★04月新番[鬼灭之刃 柱训练篇 / Kimetsu_no_Yaiba-Hashira_Geiko_Hen][02(57)][简体][1080P][MP4]"
    # title = "迷宮飯 08/[TOC] Delicious in Dungeon [08][1080P][AVC AAC][CHT][MP4].mp4"
    # title = "[喵萌奶茶屋&LoliHouse] 葬送的芙莉莲 / Sousou no Frieren - 06 [WebRip 1080p HEVC-10bit AAC][简繁日内封字幕]"
    # title = "[LoliHouse] Ore wa Subete wo Parry suru - 05 [WebRip 1080p HEVC-10bit AAC SRTx2]"
    # title = " [LoliHouse] 我要【招架】一切 ～反误解的世界最强想成为冒险者～ / Ore wa Subete wo Parry suru - 05 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕] [复制磁连]"
    # title = "北宇治字幕组] 夜晚的水母不会游泳 / Yoru no Kurage wa Oyogenai [01-12 修正合集][WebRip][HEVC_AAC][简繁日内封] [复制磁连]"
    title = "[北宇治字组&霜庭云花Sub&氢气烤肉架]【我推的孩子】/【Oshi no Ko】[18][WebRip][HEVC_AAC][繁日内嵌]"
    # # print(re.findall(RESOLUTION_RE,title))
    # title = "[织梦字幕组][尼尔：机械纪元 NieR Automata Ver1.1a][02集][1080P][AVC][简日双语]"
    # title = "[ANi] Bakemonogatari / 物语系列 第外季＆第怪季 - 06.5 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4][ANi] Bakemonogatari / 物语系列 第外季＆第怪季 - 06.5 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4][217.2 MB]"
    # title = "ANi] 我獨自升級 - 07.5 [1080P][Baha][WEB-DL][AAC AVC][CHT].mp4"
    # title = "[NEO·QSW]古莲泰沙U グレンダイザーU Grendizer U 02[WEBRIP AVC 1080P]（搜索用：巨灵神/克雷飞天神）"
    # title ="地下城里的人们 (2024) S02E10005.mp4"
    # title = "[ANi] 物語系列 第外季＆第怪季 - 06.5 [1080P][Baha][WEB-DL][AAC AVC][CHT].mp4 "
    # title = "物语系列 S05E06.5.mp4 "
    # title = " 【幻月字幕组】【24年日剧】【直到破坏了丈夫的家庭】【第7话】【1080P】【中日双语】.mp4"
    # title = "[LoliHouse] 2.5次元的诱惑 / 2.5-jigen no Ririsa - 01 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕][LoliHouse] 2.5次元的诱惑 / 2.5-jigen no Ririsa - 01 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕][609.59 MB]"
    title = "[ANi] Re：从零开始的异世界生活 第三季 - 01 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4] [复制磁连]"
    title = "[AnimeRep] 蓝箱 / 青之箱 / Blue Box / Ao no Hako- 02 [1080p][简中内嵌]"
    title = "[ANi] Kekkon Surutte Hontou desu ka /  听说你们要结婚！？ - 03 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4]"
    title = "[北宇治字幕组&LoliHouse] 地。-关于地球的运动- / Chi. Chikyuu no Undou ni Tsuite 03 [WebRip 1080p HEVC-10bit AAC ASSx2][简繁日内封字幕] [复制磁连]"
    print(title)

    ret = RawParser(title)
    # #
    print(ret.parser())
    # print(ret.token)
    # print(raw_parser(title))
