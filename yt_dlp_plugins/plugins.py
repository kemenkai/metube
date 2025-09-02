"""
yt-dlp插件配置文件
"""

def register_extractors():
    """注册自定义提取器"""
    from .extractor import TingdaoIE
    from .extractor import FuyinIE, FuyinVideoIE
    return [TingdaoIE, FuyinIE, FuyinVideoIE]