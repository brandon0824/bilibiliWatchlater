# Post Timeline Video to Watchlater per half hour.

> 通过RSSHub和requests每半小时将bilibili时间线视频添加到稍后再看列表中

## Install

#### Download python and feedparser

```bash
pip install feedparser
```

#### Config ur following RSS Timeline in  RSSHub Server

> [RSSHub](https://docs.rsshub.app/social-media.html#bilibili)

## Configure

Config your information in info.json (URL is RSSHub Server Domain)

```json
{
    "URL": "123456",
    "sessData": "123456",
    "CSRF": "123456",
    "CSRF_TOKEN": "123456"
}
```

## Run

```bash
python watchlater.py
```

