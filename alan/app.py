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
    db = InfluxDBClient('localhost', 8086, 'root', 'root')
    db.create_database('alan',if_not_exists=True)
    db.switch_database('alan')
    db.create_retention_policy('raw_hits', '1h', 1, database='alan', default=True)
    db.create_retention_policy('workingset', '1h', 1, database='alan', default=False)
    db.create_retention_policy('digest', '1d', 1, database='alan', default=False)
    db.create_retention_policy('trends', '1w', 1, database='alan', default=False)
    db.create_retention_policy('historical', '52w', 1, database='alan', default=False)

    # downsample data into counts per 5 for all articles
    # keep for a 1h
    db.query( "DROP CONTINUOUS QUERY pageview_5s_count ON alan" );
    db.query( "CREATE CONTINUOUS QUERY pageview_5s_count ON alan BEGIN SELECT count(\"duration\") INTO alan.workingset.pageview_5s_bins FROM alan.raw_hits.pageview GROUP BY site, section, url, time(5s) END" );
    # work out pages/sec for all content, updated per minute
    # keep for a day
    db.query( "DROP CONTINUOUS QUERY create_pageview_rate ON alan" );
    db.query( "CREATE CONTINUOUS QUERY create_pageview_rate ON alan BEGIN SELECT sum(\"count\")/60 INTO alan.digest.pageview_rate FROM alan.workingset.pageview_5s_bins GROUP BY site, section, url, time(1m) END" );
    
    return db

#web.run_app(app)

