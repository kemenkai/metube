# yt-dlp 插件

此目录包含用于下载特定网站内容的自定义 yt-dlp 插件。

## 支持的网站

### 1. tingdao.org
用于下载天道音频内容。

### 2. fuyin.tv
用于下载福音影视网的视频内容。

## 使用方法

```bash
yt-dlp --plugin-dirs /path/to/yt_dlp_plugins [URL]
```

## 示例

### 下载 tingdao.org 音频
```bash
yt-dlp --plugin-dirs /path/to/yt_dlp_plugins https://www.tingdao.org/dist/#/Media?device=mobile&id=11869
```

### 下载 fuyin.tv 视频集
```bash
yt-dlp --plugin-dirs /path/to/yt_dlp_plugins https://www.fuyin.tv/content/view/movid/3039/index.html
```

## 插件开发

每个插件都需要：
1. 在 `extractor/` 目录中创建提取器类
2. 在 `plugins.py` 中注册提取器
3. 在 `plugin.yaml` 中更新插件信息