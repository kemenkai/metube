import re
import json
import urllib.parse

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    ExtractorError,
    urljoin,
)


class TingdaoIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?tingdao\.org/dist/#/Media\?.*?\bid=(?P<id>\d+)'
    _TESTS = [{
        'url': 'https://www.tingdao.org/dist/#/Media?device=mobile&id=11869',
        'info_dict': {
            'id': '11869',
            'title': '口袋书-神笔马良01',
        },
        'playlist_count': 1,
    }]

    _API_URL = 'https://www.tingdao.org/Record/exhibitions'

    def _real_extract(self, url):
        video_id = self._match_id(url)
        
        # 从API获取音频信息
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'ypid': video_id
        }

        response = self._download_json(
            self._API_URL, video_id, data=urllib.parse.urlencode(data).encode('utf-8'),
            headers=headers, 
            note='正在获取音频列表')

        if not response.get('list') or not response['list'].get('mediaList'):
            raise ExtractorError('API返回数据不完整或无效', expected=True)

        media_list = response['list']['mediaList']
        
        # 使用第一个音频的标题作为播放列表标题
        first_title = self._clean_title(media_list[0]['title'])
        playlist_title = first_title

        entries = []
        for media in media_list:
            clean_title = self._clean_title(media['title'])
            
            # 获取音频URL
            audio_url = media.get('video_url') or media.get('videos_url') or media.get('url')
            if not audio_url:
                self.report_warning(f'跳过无效的媒体条目: {media["title"]} (缺少有效URL)')
                continue

            entries.append({
                'id': media['id'],
                'title': media['title'],
                'url': audio_url,
                'ext': 'mp3',
                'protocol': 'https',
            })

        if not entries:
            raise ExtractorError('未找到有效的音频文件', expected=True)

        return self.playlist_result(entries, video_id, playlist_title)

    def _clean_title(self, title):
        """清理标题以生成安全的文件名"""
        # 移除文件名中的无效字符
        clean_title = re.sub(r'[^\w\s\u4e00-\u9fff\-_().\[\]]', '', title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()
        return clean_title