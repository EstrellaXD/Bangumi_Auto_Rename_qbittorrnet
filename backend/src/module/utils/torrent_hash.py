import base64
import urllib.parse

from torrentool.bencode import Bencode
from torrentool.torrent import Torrent


def from_torrent(content: bytes):
    torrent = Torrent(Bencode.decode(content))
    return torrent.info_hash


def from_magnet(magnet_link: str):
    magnet_params = urllib.parse.urlparse(magnet_link)
    magnet_params = urllib.parse.parse_qs(magnet_params.query)
    for info_hash in magnet_params.get("xt", []):
        if info_hash.startswith("urn:btih:"):
            info_hash = info_hash.lstrip("urn:btih:")
            if len(info_hash) == 32:
                info_hash = base64.b32decode(info_hash).hex()
        elif info_hash.startswith("urn:btmh:1220"):
            info_hash = info_hash.lstrip("urn:btmh:1220")
        else:
            continue
        return info_hash
    return None
