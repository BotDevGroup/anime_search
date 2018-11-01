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
            'base_url': 'https://nyaa.si/?page=rss&q='
        }

    def configure(self, config):
        self.config = config
        pass

    def setup_handlers(self, adapter):
        self.add_handler(CommandHandler('anime', self.on_anime, command_description='Searches for anime torrents on Nyaa.si'))

    def setup_schedules(self, adapter):
        pass

    def fetch_anime(self, anime):
        url = "{}{}".format(self.config.get('base_url'), anime)
        response = requests.get(url)
        return response.text

    def parse_anime_search(self, text):
        return xmltodict.parse(text)


    def on_anime(self, update, *args, **kwargs):
        def g_list(l):
            if not l:
                return []
            elif isinstance(l, list):
                return l
            else:
                return [l]

        message = get_message(update)
        fetched_response = self.fetch_anime(anime=message.text)
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

        items = g_list(channel.get('item', None))
        if items is None or len(items) == 0:
            message.reply_text(text="❌ Invalid response.")
            log.error("No item")
            return

        responses = []
        for item in items:
            response = []
            title = item.get('title', '').strip()
            response.append("➡ <b>{}</b>".format(title))
            size = item.get('nyaa:size', '').strip()
            response.append("\n\n<b>Size:</b> {} | ".format(size))
            link = item.get('link','').strip()
            response.append("<b>Download:</b> <a href='{}'>Torrent</a> 🔗".format(link))
            release_date = item.get('pubDate','').strip()
            response.append("\n<b>Date:</b> {}\n".format(release_date))

            responses.append("".join(response))    

        i = 0
        while i < len(responses):
            tmp = responses[i:i+10]
            message.reply_text(text="\n".join(tmp), parse_mode='HTML')
            i = i + 10;
