# yt-dlp插件包初始化文件

def plugin_load():
    """插件加载函数"""
    from .plugins import register_extractors
    return register_extractors()