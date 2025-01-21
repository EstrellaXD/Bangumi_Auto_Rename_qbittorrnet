import importlib
import logging

from module.conf import settings
from module.downloader.client.expection import AuthorizationError
from .base_downloader import BaseDownloader

download_type = settings.downloader.type
package_path = f"module.downloader.client.{download_type}"
downloader = importlib.import_module(package_path)
Downloader = downloader.Downloader
__all__ = ["Downloader", "AuthorizationError", "BaseDownloader"]
