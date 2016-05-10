from aiohttp import web
from influxdb import InfluxDBClient

db = False

async def handle(request):
    section = request.match_info.get('section', 'none')
    slug = request.match_info.get('slug', 'none')
    url = section + '/' + slug
    text = "Article, " + slug
    register_alan(section, slug)
    return web.Response(body=text.encode('utf-8'))

def register_alan(section, slug):
    global db
    json_body = [
        {
            "measurement": "pageview",
            "tags": {
                "site": "pudding.bn.gntech.systems",
                "section": section,
                "url": slug
            },
            "fields": {
                "duration": 1.0
            }
        }
    ]
    db.write_points(json_body)

def init(argv):
    init_db()

    app = web.Application()
    app.router.add_route('GET', '/{section}/{slug}', handle)
    return app

def init_db():
    global db
    db = InfluxDBClient('localhost', 8086, 'root', 'root', 'alan_raw_hits')
    db.create_database('alan_raw_hits',if_not_exists=True)
    db.create_retention_policy('oneday', '1d', 1, database='alan_raw_hits', default=True)
    
    return db

#web.run_app(app)

