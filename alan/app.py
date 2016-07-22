import json, time
from datetime import datetime
from aiohttp import web

from .analytics import analytics

def get_datetime_isoformat(date_timestamp):
    iso_dateformat = "%Y-%m-%dT%H:%M:%S.%f"
    return datetime.strptime(date_timestamp, iso_dateformat)

async def record_pageview(request):
    data = await request.post()
    path = data['path']
    site = data['site']
    section = data['section']
    referrer = data['referrer']
    published = data['published']
    platforms = None
    if data.get('platforms'):
        platforms = data['platforms'].split(',')
    timestamp = None
    if data.get('timestamp'):
        timestamp = get_datetime_isoformat(data['timestamp'])
    published_dt = get_datetime_isoformat(published)
    await analytics.register(site=site, section=section, path=path, 
        referrer=referrer, published=published_dt, platforms=platforms,
        timestamp=timestamp)
    return web.Response(body="DUN".encode('utf-8'))

async def get_top_articles(request):
    period = request.match_info.get('period', 'last_30_minutes')
    params = request.GET
    site = params.get('site')
    referrer = params.get('referrer')
    platforms = []
    platform_str = params.get('relevant_platforms', '')
    if platform_str:
        platforms = platform_str.split(',')
    timestamp = params.get('timestamp', None)
    if timestamp:
        timestamp = get_datetime_isoformat(timestamp)
    top_articles = await analytics.get_top_articles(period, site=site, referrer=referrer, platforms=platforms, timestamp=timestamp)
    body = json.dumps(top_articles, indent=2).encode('utf-8')
    return web.Response(body=body)


def init(argv):
    app = web.Application()
    app.router.add_route('GET', '/top_articles/{period}', get_top_articles)
    app.router.add_route('POST', '/record_pageview/', record_pageview)
    return app
