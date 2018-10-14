# -*- coding: utf-8 -*-
from marvinbot.utils import get_message
from marvinbot.plugins import Plugin
from marvinbot.handlers import CommandHandler
from bs4 import BeautifulSoup
import logging

import requests
import xmltodict

log = logging.getLogger(__name__)


class AnimeSearch(Plugin):
    def __init__(self):
        super(AnimeSearch, self).__init__('anime_search')

    def get_default_config(self):
        return {
            'short_name': self.name,
            'enabled': True,
            'base_url': 'https://nyaa.si/?page=rss&q=My+Hero+Academia+S3+1080p&u=Golumpa'
        }

    def configure(self, config):
        self.config = config
        pass

    def setup_handlers(self, adapter):
        self.add_handler(CommandHandler('anime', self.on_anime, command_description='Searches for anime torrents on Nyaa.si'))

    def setup_schedules(self, adapter):
        pass

    def fetch_anime(self):
        url = self.config.get('base_url')
        response = requests.get(url)
        return response.text

    def parse_anime_search(self, text):
        return xmltodict.parse(text)


    def on_anime(self, update, *args, **kwargs):
        message = get_message(update)
        fetched_response = self.fetch_anime()
        data = self.parse_anime_search(fetched_response)

        rss = data.get('rss', None)
        if rss is None:
            message.reply_text(text="❌ Invalid response.")
            log.error("No rss")
            return

        channel = rss.get('channel', None)
        if channel is None:
            message.reply_text(text="❌ Invalid response.")
            log.error("No channel")
            return

        item = channel.get('item', None)
        if item is None:
            message.reply_text(text="❌ Invalid response.")
            log.error("No item")
            return

        responses = []
        title = item.get('title', '').strip()
        responses.append("<b>{}</b>".format(title))
        size = item.get('nyaa:size', '').strip()
        responses.append("\n\n<b>Size:</b> {} | ".format(size))
        link = item.get('link','').strip()
        responses.append("<b>Download:</b> <a href='{}'>Torrent</a>".format(link))
        release_date = item.get('pubDate','').strip()
        responses.append("\n<b>Date:</b> {}".format(release_date))
        message.reply_text(text="".join(responses), parse_mode='HTML')
