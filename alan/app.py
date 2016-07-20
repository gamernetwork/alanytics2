import json, time
from datetime import datetime
from aiohttp import web

from .analytics import analytics

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
    published_dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S.%f")
    analytics.register(site=site, section=section, path=path, 
        referrer=referrer, published=published_dt, platforms=platforms)
    return web.Response(body="DUN".encode('utf-8'))

async def get_top_articles(request):
    period = request.match_info.get('period', 'last_30_minutes')
    params = request.GET
    site = params.get('site')
    referrer = params.get('referrer')
    platforms = []
    platform_str = params.get('platforms', '')
    if platform_str:
        platforms = platform_str.split(',')
    top_articles = analytics.get_top_articles(period, site=site, referrer=referrer, platforms=platforms)
    body = json.dumps(top_articles, indent=2).encode('utf-8')
    return web.Response(body=body)

async def get_top_articles_histogram(request):
    period = request.match_info.get('period', 'last_hour')
    params = request.GET
    site = params.get('site')
    referrer = params.get('referrer')
    top_articles = analytics.get_top_articles_histogram(period, site=site, referrer=referrer)
    body = json.dumps(top_articles, indent=2).encode('utf-8')
    return web.Response(body=body)

async def get_top_articles_moving_average(request):
    period = request.match_info.get('period', 'last_hour')
    params = request.GET
    site = params.get('site')
    referrer = params.get('referrer')
    top_articles = analytics.get_top_articles_moving_average(period, site=site, referrer=referrer)
    body = json.dumps(top_articles, indent=2).encode('utf-8')
    return web.Response(body=body)

async def get_top_articles_average(request):
    period = request.match_info.get('period', 'last_hour')
    params = request.GET
    site = params.get('site')
    referrer = params.get('referrer')
    top_articles = analytics.get_top_articles_average(period, site=site, referrer=referrer)
    body = json.dumps(top_articles, indent=2).encode('utf-8')
    return web.Response(body=body)

def init(argv):
    app = web.Application()
    app.router.add_route('GET', '/top_articles_average/{period}', 
        get_top_articles_average)
    app.router.add_route('GET', '/top_articles_moving_average/{period}', 
        get_top_articles_moving_average)
    app.router.add_route('GET', '/top_articles_histogram/{period}', 
        get_top_articles_histogram)
    app.router.add_route('GET', '/top_articles/{period}', get_top_articles)
    app.router.add_route('POST', '/record_pageview/', record_pageview)
    return app
