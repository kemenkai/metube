FROM node:lts-alpine as builder

WORKDIR /metube
COPY ui ./
RUN npm ci && \
    node_modules/.bin/ng build --configuration production


FROM python:3.13-alpine

WORKDIR /app

COPY Pipfile* ./docker-entrypoint.sh ./

# Use sed to strip carriage-return characters from the entrypoint script (in case building on Windows)
# Install dependencies
RUN sed -i 's/\r$//g' docker-entrypoint.sh && \
    chmod +x docker-entrypoint.sh && \
    apk add --update ffmpeg aria2 coreutils shadow su-exec curl tini && \
    apk add --update --virtual .build-deps gcc g++ musl-dev libffi-dev git && \
    pip install --no-cache-dir pipenv && \
    pipenv lock --pre -r > requirements.txt && \
    python -m pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/* && \
    mkdir /.cache && chmod 777 /.cache

# Create directory for yt-dlp plugins
RUN mkdir -p /app/yt_dlp_plugins

COPY app ./app
COPY yt_dlp_plugins/ ./yt_dlp_plugins/
COPY --from=builder /metube/dist/metube ./ui/dist/metube

ENV UID=1000
ENV GID=1000
ENV UMASK=022

# Set environment variable for yt-dlp plugins directory
ENV YTDL_PLUGINS_DIR=/app/yt_dlp_plugins

ENV DOWNLOAD_DIR /downloads
ENV STATE_DIR /downloads/.metube
ENV TEMP_DIR /downloads
VOLUME /downloads
EXPOSE 8081

# Add build-time argument for version
ARG VERSION=dev
ENV METUBE_VERSION=$VERSION

ENTRYPOINT ["/sbin/tini", "-g", "--", "./docker-entrypoint.sh"]
