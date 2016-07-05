from aiohttp import web

from .analytics import analytics

async def handle(request):
    section = request.match_info.get('section', 'none')
    slug = request.match_info.get('slug', 'none')
    url = section + '/' + slug
    text = "Article, " + slug
    analytics.register(section, slug)
    return web.Response(body=text.encode('utf-8'))

def init(argv):
    app = web.Application()
    app.router.add_route('GET', '/{section}/{slug}', handle)
    return app
