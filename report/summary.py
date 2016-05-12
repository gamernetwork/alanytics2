from influxdb import InfluxDBClient
from tabulate import tabulate

db = False

def init_db():
    global db
    db = InfluxDBClient('localhost', 8086, 'root', 'root')
    db.switch_database('alan')

init_db()

res = db.query("select top(sum,site,section,url,10) from alan.digest.pageview_rate where time > now() - 3m")
print (tabulate(res['pageview_rate']))
