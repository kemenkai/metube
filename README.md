# MeTube

> **_NOTE:_**  32-bit ARM builds have been retired (a full year after [other major players](https://www.linuxserver.io/blog/a-farewell-to-arm-hf)), as new Node versions don't support them, and continued security updates and dependencies require new Node versions. Please migrate to a 64-bit OS to continue receiving MeTube upgrades.

![Build Status](https://github.com/alexta69/metube/actions/workflows/main.yml/badge.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/alexta69/metube.svg)

Web GUI for youtube-dl (using the [yt-dlp](https://github.com/yt-dlp/yt-dlp) fork) with playlist support. Allows you to download videos from YouTube and [dozens of other sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md).

![screenshot1](https://github.com/alexta69/metube/raw/master/screenshot.gif)

## Special Site Support

MeTube now includes special handling for certain sites that may not be fully supported by yt-dlp. Currently, the following sites have special support:

- **tingdao.org**: Special audio processing for tingdao.org URLs

When you enter a URL from a specially supported site, MeTube will first attempt to use the special processing logic. If that fails, it will fall back to the standard yt-dlp processing.

## Run using Docker

```bash
docker run -d -p 8081:8081 -v /path/to/downloads:/downloads ghcr.io/alexta69/metube
```

## Run using docker-compose

```yaml
services:
  metube:
    image: ghcr.io/alexta69/metube
    container_name: metube
    restart: unless-stopped
    ports:
      - "8081:8081"
    volumes:
      - /path/to/downloads:/downloads
```

## Configuration

### Environment variables

A few Docker environment variables are available to customize behavior:

| Variable                        | Purpose                                                                                                                                                                                                                   |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DOWNLOAD_DIR`                  | Directory where videos are downloaded. Defaults to `/downloads` inside Docker, and `metube` subdirectory in the current dir outside of Docker.                                                                            |
| `AUDIO_DOWNLOAD_DIR`            | Directory where audio is downloaded. Defaults to `DOWNLOAD_DIR` if not set.                                                                                                                                               |
| `TEMP_DIR`                      | Directory where downloads are processed until completion. Defaults to `DOWNLOAD_DIR` if not set.                                                                                                                          |
| `CUSTOM_DIRS`                   | Allow users to specify custom download subdirectories using the `--paths` parameter. Defaults to `true`.                                                                                                                   |
| `CREATE_CUSTOM_DIRS`            | Automatically create custom download subdirectories. Defaults to `true`.                                                                                                                                                  |
| `DELETE_FILE_ON_TRASHCAN`       | Delete files from disk when clicking the "Delete" button in the UI. Defaults to `false`.                                                                                                                                   |
| `STATE_DIR`                     | Directory where persistent state is stored. Defaults to `DOWNLOAD_DIR` if not set.                                                                                                                                         |
| `URL_PREFIX`                    | Path prefix for the UI. Example: set to `/youtube-dl` to serve the UI at `http://localhost:8081/youtube-dl`. Defaults to `/`.                                                                                              |
| `YTDL_OPTIONS`                  | JSON object with [yt-dlp options](https://github.com/yt-dlp/yt-dlp/blob/master/README.md#usage-and-options) to be passed to all downloads. Example: `'{"proxy":"http://proxy.example.com:3128"}'`                           |
| `YTDL_OPTIONS_FILE`             | Path to a JSON file with yt-dlp options to be passed to all downloads. Example: `/config/ytdl-options.json`. Overrides `YTDL_OPTIONS` if both are set.                                                                     |
| `YTDL_PLUGINS_DIR`              | Path to a directory containing [yt-dlp plugins](https://github.com/yt-dlp/yt-dlp#plugins). Example: `/plugins`. Defaults to `/app/yt_dlp_plugins` if directory exists.                                                      |
| `ROBOTS_TXT`                    | Optional text to write to `robots.txt` served at `http://localhost:8081/robots.txt`.                                                                                                                                       |
| `OUTPUT_TEMPLATE`               | A [yt-dlp output template](https://github.com/yt-dlp/yt-dlp#output-template) for videos. Defaults to `%(title)s.%(ext)s`.                                                                                                  |
| `OUTPUT_TEMPLATE_CHAPTER`       | A [yt-dlp output template](https://github.com/yt-dlp/yt-dlp#output-template) for videos with chapters. Defaults to `%(title)s - %(section_number)s %(section_title)s.%(ext)s`.                                              |
| `OUTPUT_TEMPLATE_PLAYLIST`      | A [yt-dlp output template](https://github.com/yt-dlp/yt-dlp#output-template) for playlists. Defaults to `%(playlist_title)s/%(title)s.%(ext)s`.                                                                            |
| `DEFAULT_OPTION_PLAYLIST_STRICT_MODE` | Enable playlist strict mode by default. Defaults to `false`.                                                                                                                                                         |
| `DEFAULT_OPTION_PLAYLIST_ITEM_LIMIT`  | Set default limit for number of items to download from a playlist. Defaults to `0` (no limit).                                                                                                                       |
| `DEFAULT_THEME`                 | Default theme for the UI. Can be `auto`, `light`, or `dark`. Defaults to `auto`.                                                                                                                                           |
| `HOST`                          | Host to serve UI on. Used for container networking. Defaults to `0.0.0.0`.                                                                                                                                                 |
| `PORT`                          | Port to serve UI on. Used for container networking. Defaults to `8081`.                                                                                                                                                    |
| `HTTPS`                         | Whether to use HTTPS. If `true`, both `CERTFILE` and `KEYFILE` must be set. Defaults to `false`.                                                                                                                           |
| `CERTFILE`                      | Path to a certificate file for HTTPS. Required if `HTTPS` is `true`.                                                                                                                                                       |
| `KEYFILE`                       | Path to a key file for HTTPS. Required if `HTTPS` is `true`.                                                                                                                                                               |
| `BASE_DIR`                      | Base directory for all paths. Defaults to empty string.                                                                                                                                                                    |
| `DOWNLOAD_MODE`                 | Download mode for videos. Can be `concurrent`, `sequential`, or `limited`. Defaults to `limited`.                                                                                                                          |
| `MAX_CONCURRENT_DOWNLOADS`      | Maximum number of downloads to run concurrently. Used only if `DOWNLOAD_MODE` is `limited`. Defaults to `3`.                                                                                                               |
| `LOGLEVEL`                      | Log level for the application. Can be `DEBUG`, `INFO`, `WARNING`, `ERROR`, or `CRITICAL`. Defaults to `INFO`.                                                                                                              |
| `ENABLE_ACCESSLOG`              | Enable access logging. Defaults to `false`.                                                                                                                                                                               |

### yt-dlp Plugins

MeTube supports yt-dlp plugins for extending download capabilities. By default, it includes a plugin for downloading audio from tingdao.org.

To use your own plugins:
1. Place them in a directory on the host
2. Mount that directory to the container
3. Set the `YTDL_PLUGINS_DIR` environment variable to point to that directory

Example:
```bash
docker run -d \
  -p 8081:8081 \
  -v /path/to/downloads:/downloads \
  -v /path/to/plugins:/plugins \
  -e YTDL_PLUGINS_DIR=/plugins \
  ghcr.io/alexta69/metube
```

The included tingdao.org plugin can be used by simply entering URLs like `https://www.tingdao.org/dist/#/Media?device=mobile&id=11869` in the download box.

## Using browser cookies

In case you need to use your browser's cookies with MeTube, for example to download restricted or private videos:

* Add the following to your docker-compose.yml:

```yaml
    volumes:
      - /path/to/cookies:/cookies
    environment:
      - YTDL_OPTIONS={"cookiefile":"/cookies/cookies.txt"}
```

* Install in your browser an extension to extract cookies:
  * [Firefox](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/)
  * [Chrome](https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
* Extract the cookies you need with the extension and rename the file `cookies.txt`
* Drop the file in the folder you configured in the docker-compose.yml above
* Restart the container

## Browser extensions

Browser extensions allow right-clicking videos and sending them directly to MeTube. Please note that if you're on an HTTPS page, your MeTube instance must be behind an HTTPS reverse proxy (see below) for the extensions to work.

__Chrome:__ contributed by [Rpsl](https://github.com/rpsl). You can install it from [Google Chrome Webstore](https://chrome.google.com/webstore/detail/metube-downloader/fbmkmdnlhacefjljljlbhkodfmfkijdh) or use developer mode and install [from sources](https://github.com/Rpsl/metube-browser-extension).

__Firefox:__ contributed by [nanocortex](https://github.com/nanocortex). You can install it from [Firefox Addons](https://addons.mozilla.org/en-US/firefox/addon/metube-downloader) or get sources from [here](https://github.com/nanocortex/metube-firefox-addon).

## iOS Shortcut

[rithask](https://github.com/rithask) created an iOS shortcut to send URLs to MeTube from Safari. Enter the MeTube instance address when prompted which will be saved for later use. You can run the shortcut from Safari’s share menu. The shortcut can be downloaded from [this iCloud link](https://www.icloud.com/shortcuts/66627a9f334c467baabdb2769763a1a6).

## iOS Compatibility

iOS has strict requirements for video files, requiring h264 or h265 video codec and aac audio codec in MP4 container. This can sometimes be a lower quality than the best quality available. To accommodate iOS requirements, when downloading a MP4 format you can choose "Best (iOS)" to get the best quality formats as compatible as possible with iOS requirements.

To force all downloads to be converted to an iOS compatible codec insert this as an environment variable 

```yaml
  environment:
    - 'YTDL_OPTIONS={"format": "best", "exec": "ffmpeg -i %(filepath)q -c:v libx264 -c:a aac %(filepath)q.h264.mp4"}'
```

## Bookmarklet

[kushfest](https://github.com/kushfest) has created a Chrome bookmarklet for sending the currently open webpage to MeTube. Please note that if you're on an HTTPS page, your MeTube instance must be configured with `HTTPS` as `true` in the environment, or be behind an HTTPS reverse proxy (see below) for the bookmarklet to work.

GitHub doesn't allow embedding JavaScript as a link, so the bookmarklet has to be created manually by copying the following code to a new bookmark you create on your bookmarks bar. Change the hostname in the URL below to point to your MeTube instance.

```javascript
javascript:!function(){xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.withCredentials=true;xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function(){if(xhr.status==200){alert("Sent to metube!")}else{alert("Send to metube failed. Check the javascript console for clues.")}}}();
```

[shoonya75](https://github.com/shoonya75) has contributed a Firefox version:

```javascript
javascript:(function(){xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function(){if(xhr.status==200){alert("Sent to metube!")}else{alert("Send to metube failed. Check the javascript console for clues.")}}})();
```

The above bookmarklets use `alert()` as a success/failure notification. The following will show a toast message instead:

Chrome:

```javascript
javascript:!function(){function notify(msg) {var sc = document.scrollingElement.scrollTop; var text = document.createElement('span');text.innerHTML=msg;var ts = text.style;ts.all = 'revert';ts.color = '#000';ts.fontFamily = 'Verdana, sans-serif';ts.fontSize = '15px';ts.backgroundColor = 'white';ts.padding = '15px';ts.border = '1px solid gainsboro';ts.boxShadow = '3px 3px 10px';ts.zIndex = '100';document.body.appendChild(text);ts.position = 'absolute'; ts.top = 50 + sc + 'px'; ts.left = (window.innerWidth / 2)-(text.offsetWidth / 2) + 'px'; setTimeout(function () { text.style.visibility = "hidden"; }, 1500);}xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function() { if(xhr.status==200){notify("Sent to metube!")}else {notify("Send to metube failed. Check the javascript console for clues.")}}}();
```

Firefox:

```javascript
javascript:(function(){function notify(msg) {var sc = document.scrollingElement.scrollTop; var text = document.createElement('span');text.innerHTML=msg;var ts = text.style;ts.all = 'revert';ts.color = '#000';ts.fontFamily = 'Verdana, sans-serif';ts.fontSize = '15px';ts.backgroundColor = 'white';ts.padding = '15px';ts.border = '1px solid gainsboro';ts.boxShadow = '3px 3px 10px';ts.zIndex = '100';document.body.appendChild(text);ts.position = 'absolute'; ts.top = 50 + sc + 'px'; ts.left = (window.innerWidth / 2)-(text.offsetWidth / 2) + 'px'; setTimeout(function () { text.style.visibility = "hidden"; }, 1500);}xhr=new XMLHttpRequest();xhr.open("POST","https://metube.domain.com/add");xhr.send(JSON.stringify({"url":document.location.href,"quality":"best"}));xhr.onload=function() { if(xhr.status==200){notify("Sent to metube!")}else {notify("Send to metube failed. Check the javascript console for clues.")}}})();
```

## Raycast extension

[dotvhs](https://github.com/dotvhs) has created an [extension for Raycast](https://www.raycast.com/dot/metube) that allows adding videos to MeTube directly from Raycast.

## HTTPS support, and running behind a reverse proxy

It's possible to configure MeTube to listen in HTTPS mode. `docker-compose` example:

```yaml
services:
  metube:
    image: ghcr.io/alexta69/metube
    container_name: metube
    restart: unless-stopped
    ports:
      - "8081:8081"
    volumes:
      - /path/to/downloads:/downloads
      - /path/to/ssl/crt:/ssl/crt.pem
      - /path/to/ssl/key:/ssl/key.pem
    environment:
      - HTTPS=true
      - CERTFILE=/ssl/crt.pem
      - KEYFILE=/ssl/key.pem
```

It's also possible to run MeTube behind a reverse proxy, in order to support authentication. HTTPS support can also be added in this way.

When running behind a reverse proxy which remaps the URL (i.e. serves MeTube under a subdirectory and not under root), don't forget to set the URL_PREFIX environment variable to the correct value.

If you're using the [linuxserver/swag](https://docs.linuxserver.io/general/swag) image for your reverse proxying needs (which I can heartily recommend), it already includes ready snippets for proxying MeTube both in [subfolder](https://github.com/linuxserver/reverse-proxy-confs/blob/master/metube.subfolder.conf.sample) and [subdomain](https://github.com/linuxserver/reverse-proxy-confs/blob/master/metube.subdomain.conf.sample) modes under the `nginx/proxy-confs` directory in the configuration volume. It also includes Authelia which can be used for authentication.

### NGINX

```nginx
location /metube/ {
        proxy_pass http://metube:8081;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
}
```

Note: the extra `proxy_set_header` directives are there to make WebSocket work.

### Apache

Contributed by [PIE-yt](https://github.com/PIE-yt). Source [here](https://gist.github.com/PIE-yt/29e7116588379032427f5bd446b2cac4).

```apache
# For putting in your Apache sites site.conf
# Serves MeTube under a /metube/ subdir (http://yourdomain.com/metube/)
<Location /metube/>
    ProxyPass http://localhost:8081/ retry=0 timeout=30
    ProxyPassReverse http://localhost:8081/
</Location>

<Location /metube/socket.io>
    RewriteEngine On
    RewriteCond %{QUERY_STRING} transport=websocket    [NC]
    RewriteRule /(.*) ws://localhost:8081/socket.io/$1 [P,L]
    ProxyPass http://localhost:8081/socket.io retry=0 timeout=30
    ProxyPassReverse http://localhost:8081/socket.io
</Location>
```

### Caddy

The following example Caddyfile gets a reverse proxy going behind [caddy](https://caddyserver.com).

```caddyfile
example.com {
  route /metube/* {
    uri strip_prefix metube
    reverse_proxy metube:8081
  }
}
```

## Updating yt-dlp

The engine which powers the actual video downloads in MeTube is [yt-dlp](https://github.com/yt-dlp/yt-dlp). Since video sites regularly change their layouts, frequent updates of yt-dlp are required to keep up.

There's an automatic nightly build of MeTube which looks for a new version of yt-dlp, and if one exists, the build pulls it and publishes an updated docker image. Therefore, in order to keep up with the changes, it's recommended that you update your MeTube container regularly with the latest image.

I recommend installing and setting up [watchtower](https://github.com/containrrr/watchtower) for this purpose.

## Troubleshooting and submitting issues

Before asking a question or submitting an issue for MeTube, please remember that MeTube is only a UI for [yt-dlp](https://github.com/yt-dlp/yt-dlp). Any issues you might be experiencing with authentication to video websites, postprocessing, permissions, other `YTDL_OPTIONS` configurations which seem not to work, or anything else that concerns the workings of the underlying yt-dlp library, need not be opened on the MeTube project. In order to debug and troubleshoot them, it's advised to try using the yt-dlp binary directly first, bypassing the UI, and once that is working, importing the options that worked for you into `YTDL_OPTIONS`.

In order to test with the yt-dlp command directly, you can either download it and run it locally, or for a better simulation of its actual conditions, you can run it within the MeTube container itself. Assuming your MeTube container is called `metube`, run the following on your Docker host to get a shell inside the container:

```bash
docker exec -ti metube sh
cd /downloads
```

Once there, you can use the yt-dlp command freely.

## Submitting feature requests

MeTube development relies on code contributions by the community. The program as it currently stands fits my own use cases, and is therefore feature-complete as far as I'm concerned. If your use cases are different and require additional features, please feel free to submit PRs that implement those features. It's advisable to create an issue first to discuss the planned implementation, because in an effort to reduce bloat, some PRs may not be accepted. However, note that opening a feature request when you don't intend to implement the feature will rarely result in the request being fulfilled.

## Building and running locally

Make sure you have node.js and Python 3.13 installed.

```bash
cd metube/ui
# install Angular and build the UI
npm install
node_modules/.bin/ng build
# install python dependencies
cd ..
pip3 install pipenv
pipenv install
# run
pipenv run python3 app/main.py
```

A Docker image can be built locally (it will build the UI too):

```bash
docker build -t metube .
```

## Development notes

* The above works on Windows and macOS as well as Linux.
* If you're running the server in VSCode, your downloads will go to your user's Downloads folder (this is configured via the environment in .vscode/launch.json).
