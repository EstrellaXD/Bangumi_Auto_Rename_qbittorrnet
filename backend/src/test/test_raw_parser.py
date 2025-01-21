from module.parser.analyser import RawParser


def test_raw_parser():
    content = "【幻樱字幕组】【4月新番】【古见同学有交流障碍症 第二季 Komi-san wa, Komyushou Desu. S02】【22】【GB_MP4】【1920X1080】"
    info = RawParser(content).parser()
    assert info is not None
    assert info.title_en == "Komi-san wa, Komyushou Desu."
    assert info.resolution == "1920X1080"
    assert info.episode == 22
    assert info.season == 2

    content = "[百冬练习组&LoliHouse] BanG Dream! 少女乐团派对！☆PICO FEVER！ / Garupa Pico: Fever! - 26 [WebRip 1080p HEVC-10bit AAC][简繁内封字幕][END] [101.69 MB]"
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "百冬练习组&LoliHouse"
    assert info.title_zh == "BanG Dream! 少女乐团派对！☆PICO FEVER！"
    assert info.resolution == "1080p"
    assert info.episode == 26
    assert info.season == 1

    content = "【喵萌奶茶屋】★04月新番★[夏日重现/Summer Time Rendering][11][1080p][繁日双语][招募翻译]"
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "喵萌奶茶屋"
    assert info.title_en == "Summer Time Rendering"
    assert info.resolution == "1080p"
    assert info.episode == 11
    assert info.season == 1

    content = "[Lilith-Raws] 关于我在无意间被隔壁的天使变成废柴这件事 / Otonari no Tenshi-sama - 09 [Baha][WEB-DL][1080p][AVC AAC][CHT][MP4]"
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "Lilith-Raws"
    assert info.title_zh == "关于我在无意间被隔壁的天使变成废柴这件事"
    assert info.title_en == "Otonari no Tenshi-sama"
    assert info.resolution == "1080p"
    assert info.episode == 9
    assert info.season == 1

    content = (
        "[梦蓝字幕组]New Doraemon 哆啦A梦新番[747][2023.02.25][AVC][1080P][GB_JP][MP4]"
    )
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "梦蓝字幕组"
    assert info.title_zh == "哆啦A梦新番"
    assert info.title_en == "New Doraemon"
    assert info.resolution == "1080P"
    assert info.episode == 747
    assert info.season == 1

    content = (
        "[织梦字幕组][尼尔：机械纪元 NieR Automata Ver1.1a][02集][1080P][AVC][简日双语]"
    )
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "织梦字幕组"
    assert info.title_zh == "尼尔：机械纪元"
    assert info.title_en == "NieR Automata Ver1.1a"
    assert info.resolution == "1080P"
    assert info.episode == 2
    assert info.season == 1

    content = "[MagicStar] 假面骑士Geats / 仮面ライダーギーツ EP33 [WEBDL] [1080p] [TTFC]【生】"
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "MagicStar"
    assert info.title_zh == "假面骑士Geats"
    assert info.title_jp == "仮面ライダーギーツ"
    assert info.resolution == "1080p"
    assert info.episode == 33
    assert info.season == 1

    content = "【极影字幕社】★4月新番 天国大魔境 Tengoku Daimakyou 第05话 GB 720P MP4（字幕社招人内详）"
    info = RawParser(content).parser()
    assert info is not None
    assert info.title_zh == "天国大魔境"
    assert info.title_en == "Tengoku Daimakyou"
    assert info.resolution == "720P"
    assert info.episode == 5
    assert info.season == 1

    content = "【喵萌奶茶屋】★07月新番★[银砂糖师与黑妖精 ~ Sugar Apple Fairy Tale ~][13][1080p][简日双语][招募翻译]"
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "喵萌奶茶屋"
    assert info.title_zh == "银砂糖师与黑妖精"
    assert info.title_en == "~ Sugar Apple Fairy Tale ~"
    assert info.resolution == "1080p"
    assert info.episode == 13
    assert info.season == 1

    content = "[ANi]  16bit 的感动 ANOTHER LAYER - 01 [1080P][Baha][WEB-DL][AAC AVC][CHT][MP4]"
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "ANi"
    assert info.title_zh == "16bit 的感动 ANOTHER LAYER"
    assert info.resolution == "1080P"
    assert info.episode == 1
    assert info.season == 1

    content = "[Billion Meta Lab] 终末列车寻往何方 Shuumatsu Torein Dokoe Iku [12][1080][HEVC 10bit][简繁日内封][END]"
    info = RawParser(content).parser()
    assert info is not None
    assert info.group == "Billion Meta Lab"
    assert info.title_zh == "终末列车寻往何方"
    assert info.title_en == "Shuumatsu Torein Dokoe Iku"
    assert info.episode == 12
    assert info.season == 1
