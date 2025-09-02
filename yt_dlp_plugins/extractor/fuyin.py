import re
import json
import html
from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import (
    ExtractorError,
    urljoin,
)


class FuyinVideoIE(InfoExtractor):
    IE_NAME = 'fuyin:video'
    _VALID_URL = r'https?://www\.fuyin\.tv/content/view/movid/(?P<movid>\d+)/index\.html\?play=(?P<id>\d+)'

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        movid = mobj.group('movid')
        video_id = mobj.group('id')
        
        # 构建API URL获取视频信息，使用type=3参数
        api_url = f'https://www.fuyin.tv/api/api/tv.movie/url?movid={movid}&urlid={video_id}&type=3&lang=zh'
        
        # 调用API获取视频信息
        video_info = self._download_json(api_url, video_id, '获取视频信息')
        
        # 从API响应中提取视频URL
        video_url = video_info.get('data', {}).get('url')
        if not video_url:
            raise ExtractorError('无法获取视频URL', expected=True)
        
        # 获取视频标题
        title = video_info.get('data', {}).get('title', f'第{video_id}讲')
        # 清理标题中的特殊字符并确保文件名合法
        if title:
            title = re.sub(r'[^\w\s\u4e00-\u9fff\-\.]', '', title).strip()
            # 确保标题不过长（Windows文件名限制为255字符）
            title = title[:200] if len(title) > 200 else title
        
        # 确保有文件扩展名
        video_url = video_info.get('data', {}).get('url')
        if not video_url:
            raise ExtractorError('无法获取视频URL', expected=True)
            
        # 获取文件扩展名，如果没有则默认使用mp4
        ext = 'mp4'
        if '.' in video_url.split('/')[-1]:
            ext = video_url.split('.')[-1].split('?')[0].lower()
            if ext not in ['mp4', 'flv', 'mkv', 'webm', 'ts']:
                ext = 'mp4'
        
        return {
            'id': f"{movid}_{video_id}",  # 使用组合ID确保唯一性
            'title': title or f'第{video_id}讲',
            'url': video_url,
            'ext': ext,
            'duration': video_info.get('data', {}).get('duration'),  # 添加持续时间字段
            'filesize_approx': video_info.get('data', {}).get('size'),  # 添加文件大小估算
        }


class FuyinIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?fuyin\.tv/content/view/movid/(?P<movid>\d+)/index\.html'
    
    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        movid = mobj.group('movid')
        
        # 首先尝试获取视频集信息
        try:
            # 获取视频集信息的API
            collection_api = f'https://www.fuyin.tv/api/api/tv.movie/index?movid={movid}&lang=zh'
            collection_info = self._download_json(collection_api, movid, '获取视频集信息')
            
            # 如果返回了视频列表，则创建播放列表
            if collection_info.get('data') and collection_info['data'].get('list'):
                entries = []
                for video in collection_info['data']['list']:
                    video_id = video.get('id')
                    if video_id:
                        video_url = f'https://www.fuyin.tv/content/view/movid/{movid}/index.html?play={video_id}'
                        entries.append({
                            '_type': 'url',
                            'url': video_url,
                            'ie_key': 'FuyinVideoIE',
                            'title': video.get('title'),
                            'id': f"{movid}_{video_id}"
                        })
                
                if entries:
                    return {
                        '_type': 'playlist',
                        'id': movid,
                        'title': collection_info['data'].get('title', f'福音TV视频集_{movid}'),
                        'entries': entries,
                    }
        except ExtractorError as e:
            self.report_warning(f'无法获取视频集信息: {e}')
        
        # 如果无法获取播放列表，则尝试获取单个视频信息
        try:
            # 构造API请求URL - 使用正确的API端点
            api_url = f'https://www.fuyin.tv/api/api/tv.movie/url?movid={movid}&type=3&urlid=0&lang=zh'
            video_info = self._download_json(api_url, movid, '获取视频信息')
            
            # 提取标题、URL等信息
            title = video_info.get('data', {}).get('title', f'福音TV视频_{movid}')
            video_url = video_info.get('data', {}).get('url')
            
            # 如果没有获取到视频URL，尝试通用方法
            if not video_url:
                self.report_warning('无法获取视频URL，尝试通用提取方法')
                return self._extract_generic(url)
            
            # 清理标题中的特殊字符
            if title:
                title = re.sub(r'[^\w\s\u4e00-\u9fff\-\.]', '', title).strip()
                title = title[:200] if len(title) > 200 else title
            
            # 获取文件扩展名
            ext = 'mp4'
            if '.' in video_url.split('/')[-1]:
                ext = video_url.split('.')[-1].split('?')[0].lower()
                if ext not in ['mp4', 'flv', 'mkv', 'webm', 'ts']:
                    ext = 'mp4'
            
            # 返回视频信息
            return {
                'id': movid,
                'title': title,
                'url': video_url,
                'ext': ext,
                'duration': video_info.get('data', {}).get('duration'),
                'filesize_approx': video_info.get('data', {}).get('size'),
            }
        except ExtractorError as e:
            self.report_warning(f'无法获取视频信息: {e}')
            # 如果无法获取视频信息，尝试另一种方法
            return self._extract_generic(url)
    
    def _extract_generic(self, url):
        """当自定义提取失败时，使用通用提取方法"""
        self.report_warning('使用通用提取方法处理URL')
        # 使用yt-dlp的通用提取方法
        return self.url_result(url, ie='Generic')